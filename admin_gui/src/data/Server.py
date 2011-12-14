#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

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
        self.load = self.LOADED_NONE
        self.data = {}
        
        self.ip = ""
        self.username = ""
        self.password = ""
        self.ssh_username = ""
        self.ssh_password = ""
    
    def setIp(self,ip):
        self.ip= ip
        self.updated()
    
    def getIp(self):
        return self.ip
    
    def getName(self):
        if self.load == self.LOADED_SERVERDATA:
            return self.data['name']+" [ "+self.ip+" ]"
        elif self.load == self.LOADED_PROFILE:
            return " [ "+self.ip+" ]"
        else:
            return "Unknown ScovilleServer"
        
            
    def loadProfileInfo(self,profileInfo):
        pass
    
    