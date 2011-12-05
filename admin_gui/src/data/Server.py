#!/usr/bin/python
#-*- coding: utf-8 -*-


class Server(object):
    STATE_OFFLINE = 0
    STATE_LOCKED = 1
    STATE_AUTHENTICATED =2
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
    
     
    def __init__(self):
        self.state = self.STATE_OFFLINE
        self.load = self.LOADED_NONE
        self.data = {}
        
        self.ip = ""
        self.password = ""
            
    def loadProfileInfo(self,profileInfo):
        pass
    
    