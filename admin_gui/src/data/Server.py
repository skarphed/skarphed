#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject
from Generic import ObjectStore

from Users import Users
from Modules import Modules
from Roles import Roles
from Sites import Sites
from Repository import Repository
from Template import Template
from Operation import OperationManager

import json as jayson #HERE BE DRAGONS

class Server(GenericScovilleObject):
    STATE_OFFLINE = 0
    STATE_ONLINE = 1
    
    SSH_LOCKED = 0
    SSH_UNLOCKED = 1
    
    SCV_LOCKED = 0
    SCV_UNLOCKED = 1
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
     
    def __init__(self):
        GenericScovilleObject.__init__(self)
        self.state = self.STATE_OFFLINE
        self.scv_loggedin = self.SCV_LOCKED
        self.ssh_loggedin = self.SSH_LOCKED
        self.load = self.LOADED_NONE
        self.data = {}
        
        self.ip = ""
        self.username = ""
        self.password = ""
        self.ssh_username = ""
        self.ssh_password = ""
        
        self.users = None
        self.templates = None
        self.roles = None
        self.modules = None
        self.sites = None
        self.repo = None
        self.operationManager = None
        
        self.cssPropertySet = None
        
    def setIp(self,ip):
        self.ip= ip
        self.updated()
    
    def getIp(self):
        return self.ip
    
    def setScvName(self,name):
        self.username = name
        
    def setScvPass(self, password):
        self.password = password
    
    def getScvName(self):
        return self.username
        
    def getScvPass(self):
        return self.password
        
    def setSSHName(self, name):
        self.ssh_username = name
        
    def setSSHPass(self, password):
        self.ssh_password = password
    
    def getSSHName(self):
        return self.ssh_username

    def getSSHPass(self):
        return self.ssh_password
    
    def setSSHState(self,state):
        self.ssh_loggedin = state
    
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
            self.templates = Template(self)
            self.addChild(self.templates)
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
    
    def connectSSH(self):
        self.getApplication().getSSHConnection(self)
    
    def establishConnections(self):
        self.getServerInfo()
        self.authenticate()
        self.connectSSH()
    
    def getName(self):
        if self.load == self.LOADED_SERVERDATA:
            return self.data['name']+" [ "+self.ip+" ]"
        elif self.load == self.LOADED_PROFILE:
            return " [ "+self.ip+" ]"
        else:
            return "Unknown ScovilleServer"
        
            
    def loadProfileInfo(self,profileInfo):
        pass
    
    def getSSHState(self):
        return self.ssh_loggedin
    
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
    
def getServers():
    return ObjectStore().getServers()

def createServer():
    return Server()