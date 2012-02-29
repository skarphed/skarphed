#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Scoville.
#
# Scoville is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Scoville is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Scoville. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


from data.Generic import ObjectStore
from data.Instance import Instance

from Users import Users
from Modules import Modules
from Roles import Roles
from Sites import Sites
from Repository import Repository
from Template import Template
from Operation import OperationManager

import json as jayson #HERE BE DRAGONS
import os.path
from net.MultiPartForm import MultiPartForm
from net.ScovilleUpload import ScovilleUpload

class Scoville(Instance):
    STATE_OFFLINE = 0
    STATE_ONLINE = 1

    SCV_LOCKED = 0
    SCV_UNLOCKED = 1
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
     
    def __init__(self, server, url="", username="", password=""):
        Instance.__init__(self,server)
        self.instanceTypeName = "scoville"
        self.displayName = "Scoville"
        self.state = self.STATE_OFFLINE
        self.scv_loggedin = self.SCV_LOCKED
        self.load = self.LOADED_NONE
        self.data = {}
        
        self.url = url
        self.username = username
        self.password = password
        
        self.users = None
        self.template = None
        self.roles = None
        self.modules = None
        self.sites = None
        self.repo = None
        self.operationManager = None
        
        self.cssPropertySet = None
        
    def setUrl(self,url):
        self.url= url
        self.updated()
    
    def getUrl(self):
        return self.url
    
    def setScvName(self,name):
        self.username = name
        
    def setScvPass(self, password):
        self.password = password
    
    def getScvName(self):
        return self.username
        
    def getScvPass(self):
        return self.password
    
    def getUsername(self):
        return self.getScvName()
    
    def getPassword(self):
        return self.getScvPass()
    
    def getServerInfoCallback(self, result):
        self.data['name'] = result
        self.load = self.LOADED_SERVERDATA
        self.state = self.STATE_ONLINE
        self.updated()
    
    def getServerInfo(self):
        self.getApplication().doRPCCall(self,self.getServerInfoCallback, "getServerInfo")
    
    def loadScovilleChildren(self):
        if 'scoville.users.view' in self.serverRights:
            self.users = Users(self)
            self.addChild(self.users)
        if 'scoville.modules.install' in self.serverRights or 'scoville.modules.uninstall' in self.serverRights:
            self.modules = Modules(self)
            self.addChild(self.modules)
        if 'scoville.roles.view' in self.serverRights:
            self.roles = Roles(self)
            self.addChild(self.roles)
        if True: #'scoville.sites.view' in self.serverRights
            self.sites = Sites(self)
            self.addChild(self.sites)
        if 'scoville.modules.install' in self.serverRights or 'scoville.modules.uninstall' in self.serverRights:
            self.repo = Repository(self)
            self.addChild(self.repo)
        if True: #'scoville.template.modify' in self.serverRights
            self.loadTemplate()
        if True: #'scoville.operation.modify' in self.serverRights
            self.operationManager = OperationManager(self)
        
        #TODO: restliche implementieren
    
    def authenticateCallback(self, result):
        if result == False:
            self.scv_loggedin = self.SCV_LOCKED
            self.serverRights = []
        else:
            self.scv_loggedin = self.SCV_UNLOCKED
            self.serverRights = result
            print self.serverRights
        self.updated()
        self.loadScovilleChildren()
        
    def authenticate(self):
        self.getApplication().doRPCCall(self,self.authenticateCallback, "authenticateUser", [self.username,self.password])
    
    def establishConnections(self):
        self.getServerInfo()
        self.authenticate()
    
    def getName(self):
        if self.load == self.LOADED_SERVERDATA:
            return self.data['name']+" [ "+self.url+" ]"
        elif self.load == self.LOADED_PROFILE:
            return " [ "+self.url+" ]"
        else:
            return "Unknown ScovilleServer"
    
    def loadTemplateCallback(self,json):
        if self.template is None:
            self.template = Template(self,json)
            self.children.append(self.template)
        else:
            self.template.refresh(json)
    
    
    def loadTemplate(self):
        self.getApplication().doRPCCall(self,self.loadTemplateCallback, "getCurrentTemplate")
    
    def uploadTemplateCallback(self,res):
        if res != ScovilleUpload.RESULT_ERROR:
            self.loadTemplate()
    
    def uploadTemplate(self, filepath):
        form = MultiPartForm()
        templateHandle = open(filepath,'r')
        filename = os.path.basename(filepath)
        form.add_file('uploadfile',filename,templateHandle,'application/x-gzip')
        upload = ScovilleUpload(self, ScovilleUpload.TYPE_TEMPLATE, form, self.uploadTemplateCallback)
        upload.start()
        templateHandle.close()
        
    def loadProfileInfo(self,profileInfo):
        pass
    
    def getSCVState(self):
        return self.scv_loggedin
    
    def isOnline(self):
        return self.state==self.STATE_ONLINE
    
    def loadCssPropertySetCallback(self,json):
        self.cssPropertySet = jayson.JSONDecoder().decode(json)
        self.updated()
    
    def loadCssPropertySet(self):
        self.getApplication().doRPCCall(self,self.loadCssPropertySetCallback, "getCssPropertySet", [None,None,None])
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,json):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self,self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])
    
    def getOperationManager(self):
        return self.operationManager
    
    def getModules(self):
        return self.modules
    
    def getServer(self):
        pass
        return self.par.getServer()
    
    def getParent(self):
        return self.par
    
def getServers():
    return ObjectStore().getServers()

def createServer():
    return Scoville()