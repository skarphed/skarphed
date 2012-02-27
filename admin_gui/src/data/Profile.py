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

import Crypto.Cipher.AES
import json
import os
import data.Server
from Instance import InstanceType

class ProfileException(Exception):pass

class Profile(object):
    STATE_EMPTY = 0
    STATE_LOADED = 1
    
    DATA_STRUCT = {
                   'server':[]
                   }
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.state = self.STATE_EMPTY  
        self.data = {}
        
    def create(self):
        if os.path.exists(os.path.expanduser('~/.scovilleadmin/'+self.username)):
            raise ProfileException("Profile exists")
        assert len(self.password)%16 == 0 , "Password not divisible by 16"
        profilefile = open(os.path.expanduser('~/.scovilleadmin/'+self.username),'w')
        
        self.data=self.DATA_STRUCT
        
        aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
        js = json.encoder.JSONEncoder()
        clear = "SCOV"+js.encode(self.data)
        padding = "X"*(16-(len(clear)%16))
        profilefile.write(aes.encrypt(clear+padding))
        profilefile.close()
    
    def load(self):
        if not os.path.exists(os.path.expanduser('~/.scovilleadmin/'+self.username)):
            raise ProfileException("Profile does not exist")
        profilefile = open(os.path.expanduser('~/.scovilleadmin/'+self.username),'r')
        cipher = profilefile.read()
        aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
        clear = aes.decrypt(cipher)
        if clear[0:4]=="SCOV":
            js = json.decoder.JSONDecoder()
            clear = clear.rstrip("X")
            self.data = js.decode(clear[4:])
            self.state = self.STATE_LOADED
            profilefile.close()
            for server in self.data['server']:
                srv = data.Server.createServer()
                srv.setIp(server['ip'])
                srv.setSSHName(server['ssh_username'])
                srv.setSSHPass(server['ssh_password'])
                srv.establishConnections()
                for instance in server['instances']:
                    instanceType = InstanceType(instance['typename'],instance['typedisp'])
                    srv.createInstance(instanceType,instance['url'],instance['username'],instance['password'])
                 
        else:
            profilefile.close()
            raise ProfileException("Could not Decode")
    
    def save(self):
        if self.state == self.STATE_LOADED:
            self.updateProfile()
            profilefile = open(os.path.expanduser('~/.scovilleadmin/'+self.username),'w')
            aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
            js = json.encoder.JSONEncoder()
            clear = "SCOV"+js.encode(self.data)
            padding = "X"*(16-(len(clear)%16))
            profilefile.write(aes.encrypt(clear+padding))
            profilefile.close()
    
    def updateProfile(self):
        self.data['server'] = []
        for server in data.Server.getServers():
            instances = []
            for instance in server.getInstances():
                instances.append({'typename':instance.instanceTypeName,
                            'typedisp':instance.displayName,
                            'url':instance.getUrl(),
                            'username':instance.getUsername(),
                            'password':instance.getPassword()})
            self.data['server'].append({'ip':server.ip,
                                    'ssh_username':server.ssh_username,
                                    'ssh_password':server.ssh_password,
                                    'instances':instances})
            
                
          
            
        