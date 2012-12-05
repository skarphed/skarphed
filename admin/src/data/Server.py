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


import socket
import re


from Generic import GenericScovilleObject
from Generic import ObjectStore

class Server(GenericScovilleObject):
    STATE_OFFLINE = 0
    STATE_ONLINE = 1
    
    SSH_LOCKED = 0
    SSH_UNLOCKED = 1
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
     
    instanceTypesLoaded=False
     
    def __init__(self):
        if not Server.instanceTypesLoaded:
            import scoville
            import scoville_repo
            Server.instanceTypesLoaded = True
            
        GenericScovilleObject.__init__(self)
        self.state = self.STATE_OFFLINE
        self.ssh_loggedin = self.SSH_LOCKED
        self.load = self.LOADED_NONE
        self.data = {}
        
        self.ip = ""
        self.ssh_username = ""
        self.ssh_password = ""

    def setName(self,name):
        self.name = name

    def setIp(self,ip):
        self.ip= ip
        self.updated()
    
    def getIp(self):
        return self.ip
        
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

    def connectSSH(self):
        self.getApplication().getSSHConnection(self)
    
    def establishConnections(self):
        self.connectSSH()
    
    def getName(self):
        if self.ip is not None:
            if self.name is not None:
                return self.ip+" [ "+self.name+" ]"
            return self.ip
        else:
            return "Unknown Server"
            
    def loadProfileInfo(self,profileInfo):
        pass
    
    def getSSHState(self):
        return self.ssh_loggedin
    
    def isOnline(self):
        return self.state==self.STATE_ONLINE
    
    def getServer(self):
        return self
    
    def createInstance(self,instanceType, url, username, password):
        instance = None
        exec "from "+instanceType.instanceTypeName+"."+instanceType.instanceTypeName.capitalize()+\
             " import "+instanceType.instanceTypeName.capitalize()
        exec "instance = "+instanceType.instanceTypeName.capitalize()+"(self, url, username, password)"
        self.addChild(instance)
        self.updated()
        instance.establishConnections()
        
    def removeInstance(self, instance):
        if instance in self.children:
            self.children.remove(instance)
            instance.destroy()
            self.getApplication().activeProfile.updateProfile()
    
    def getInstances(self):
        return self.children

class DNSError(Exception):
    pass

def getServers():
    return ObjectStore().getServers()

def createServer():
    return Server()

def createServerFromInstanceUrl(instanceurl):
    instanceurl = re.sub(r'^[A-Za-z]+:\//','',instanceurl)
    instanceurl = re.sub(r'/.+$|/$','',instanceurl)
    instanceurl = re.sub(r':\d{1,5}$','',instanceurl)
    
    if not re.match(r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',instanceurl):
        try:
            ip = socket.gethostbyaddr(instanceurl)
        except socket.gaierror:
            raise DNSError("Couldn't resolve")
    else:
        ip = instanceurl
    for server in getServers():
        if ip == server.getIp():
            return server
    server = Server()
    server.setIp(ip)
    server.setName("Neuer Server")
    return server