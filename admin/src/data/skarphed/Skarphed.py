#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


from data.Generic import ObjectStore, GenericSkarphedObject
from data.Instance import Instance, InstanceType

from Users import Users
from Modules import Modules
from Roles import Roles
from Sites import Sites
from Template import Template
from Operation import OperationManager, OperationDaemon
from View import Views

from threading import Thread
import json 
import base64
import os
import os.path
import shutil
import tarfile
import random
import gobject
from net.MultiPartForm import MultiPartForm
from net.SkarphedUpload import SkarphedUpload

import logging

class AbstractInstaller(GenericSkarphedObject):
    class InstallThread(Thread):
        def __init__(self, installer):
            Thread.__init__(self)
            self.installer = installer

        def run(self):
            self.installer.execute_installation()


    def __init__(self,data,server):
        GenericSkarphedObject.__init__(self)
        self.server=server
        self.data  = data
        self.domain = ""
        self.installationId = int(random.random()*1000)
        self.BUILDPATH = "/tmp/scvinst"+str(self.installationId)+"/"
        self.installThread = self.InstallThread(self)
        self.status = 0

    def execute_installation(self):
        pass #To be implemented in realization

    def addInstanceToServer(self):
        if self.domain != "":
            self.server.createInstance(InstanceType("skarphed","Skarphed"), "http://"+self.domain, "root", "root")
        else:
            self.server.createInstance(InstanceType("skarphed","Skarphed"), "http://"+self.server.getIp(), "root", "root")
        self.destroy()

    def getName(self):
        return "Skarphed Installer"

    def getStatus(self):
        return self.status

    def install(self):
        self.installThread.start()

class Skarphed(Instance):
    STATE_OFFLINE = 0
    STATE_ONLINE = 1

    SCV_LOCKED = 0
    SCV_UNLOCKED = 1
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
    
    @classmethod
    def installNewSkarphed(cls, data, server, target):
        installer = SkarphedInstaller(data,server,target)
        installer.install()
        return installer

    def __init__(self, server, url="", username="", password=""):
        Instance.__init__(self,server)
        self.instanceTypeName = "skarphed"
        self.displayName = "Skarphed"
        self.state = self.STATE_OFFLINE
        self.scv_loggedin = self.SCV_LOCKED
        self.load = self.LOADED_NONE
        self.data = {}
        
        self.url = url
        self.username = username
        self.password = password
        self.publickey = None
        
        self.repo_url = ""

        self.users = None
        self.template = None
        self.roles = None
        self.modules = None
        self.sites = None
        self.operationManager = None
        self.operationDaemon = None

        self.maintenance_mode = True
        self.rendermode = None

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
    
    def setUsername(self,username):
        return self.setScvName(username)
    
    def setPassword(self,password):
        return self.setScvPass(password)

    def setPublicKey(self, publickey):
        self.publickey = publickey

    def getPublicKey(self):
        return self.publickey

    def loadPublicKeyCallback(self, result):
        if self.publickey == None:
            self.publickey = result
        else:
            if self.publickey == result:
                return
            else:
                pass #TODO Implement Error behaviour. this means, the publickey changed since last login

    def loadPublicKey(self):
        self.getApplication().doRPCCall(self,self.loadPublicKeyCallback, "getPublicKey")
    
    def getServerInfoCallback(self, result):
        self.data['name'] = result
        self.load = self.LOADED_SERVERDATA
        self.state = self.STATE_ONLINE
        self.updated()
    
    def getServerInfo(self):
        self.getApplication().doRPCCall(self,self.getServerInfoCallback, "getServerInfo")
    
    def getMaintenanceModeCallback(self,data):
        self.maintenance_mode = data
        self.updated()

    def getMaintenanceMode(self):
        self.getApplication().doRPCCall(self,self.getMaintenanceModeCallback, "getMaintenanceMode")

    def setMaintenanceModeCallback(self,data):
        self.getMaintenanceMode()

    def setMaintenanceMode(self, active):
        self.getApplication().doRPCCall(self,self.setMaintenanceModeCallback, "setMaintenanceMode", [active])    

    def isMaintenanceMode(self):
        return self.maintenance_mode

    def loadRendermodeCallback(self, data):
        self.rendermode = data
        self.updated()

    def loadRendermode(self):
        self.getApplication().doRPCCall(self,self.loadRendermodeCallback, "getRendermode")

    def setRendermodeCallback(self, data):
        self.loadRendermode()

    def setRendermode(self, mode):
        self.getApplication().doRPCCall(self,self.setRendermodeCallback, "setRendermode", [mode])

    def getRendermode(self):
        return self.rendermode

    def loadSkarphedChildren(self):
        self.loadPublicKey()
        self.getMaintenanceMode()
        self.loadRendermode()
        if 'skarphed.users.view' in self.serverRights:
            self.users = Users(self)
            self.addChild(self.users)
        if 'skarphed.modules.install' in self.serverRights or 'skarphed.modules.uninstall' in self.serverRights:
            self.modules = Modules(self)
            self.addChild(self.modules)
        if 'skarphed.roles.view' in self.serverRights:
            self.roles = Roles(self)
            self.addChild(self.roles)
        if True: #'skarphed.sites.view' in self.serverRights
            self.sites = Sites(self)
            self.addChild(self.sites)
        if True:
            self.views = Views(self)
            self.addChild(self.views)
        if True: #'skarphed.template.modify' in self.serverRights
            self.template = Template(self)
            self.addChild(self.template)
        if True: #'skarphed.operation.modify' in self.serverRights
            self.operationManager = OperationManager(self)
        # if True: # 'skarphed.compositing' in self.serverRights
        #     self.compositing = Compositing(self)
        #     self.addChild(self.compositing)
        
        #TODO: restliche implementieren
    
    def authenticateCallback(self, result):
        if result == False:
            self.scv_loggedin = self.SCV_LOCKED
            self.serverRights = []
        else:
            self.scv_loggedin = self.SCV_UNLOCKED
            self.serverRights = result
        self.updated()
        self.loadSkarphedChildren()

    def checkPermission(self, permission):
        return permission in self.serverRights
        
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
            return "Unknown SkarphedServer"
    
    def setRepositoryCallback(self,res):
        self.modules.refresh()
        
    def setRepository(self,host,port):
        self.getApplication().doRPCCall(self,self.setRepositoryCallback, "setRepository", [host,port])
        self.repo_url = host+":"+str(port)
        
    def loadProfileInfo(self,profileInfo):
        pass
    
    def getSCVState(self):
        return self.scv_loggedin
    
    def isOnline(self):
        return self.state==self.STATE_ONLINE
    
    def loadCssPropertySetCallback(self,res):
        self.cssPropertySet = res
        self.updated()
    
    def loadCssPropertySet(self):
        self.getApplication().doRPCCall(self,self.loadCssPropertySetCallback, "getCssPropertySet", [None,None,None])
    
    def updateModulesCallback(self):
        self.modules.refresh()
    
    def updateModules(self):
        self.getApplication().doRPCCall(self,self.updateModulesCallback, "updateModules")
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,res):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self,self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])
    
    def getOperationManager(self):
        return self.operationManager

    def getOperationDaemon(self):
        if self.operationDaemon is None:
            self.operationDaemon = OperationDaemon(self)
        return self.operationDaemon

    def uploadBinaryCallback(self, res):
        # res is the new ID of the uploaded binary file
        return res

    def uploadBinary(self, filepath):
        f = open(filepath, 'r')
        data = f.read()
        f.close()
        data = base64.b64encode(data)
        filename = filepath.split("/")[1:]
        self.getApplication().doRPCCall(self,self.uploadBinaryCallback, "uploadBinary", [data, filename])

    def getTemplate(self):
        return self.template
    
    def getModules(self):
        return self.modules

    def getSites(self):
        return self.sites

    def getViews(self):
        return self.views
    
    def getServer(self):
        pass
        return self.par.getServer()
    
    def getParent(self):
        return self.par
    
def getServers():
    return ObjectStore().getServers()

def createServer():
    return Skarphed()