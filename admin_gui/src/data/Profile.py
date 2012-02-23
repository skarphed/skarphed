#!/usr/bin/python
#-*- coding: utf-8 -*-

import Crypto.Cipher.AES
import json
import os
import data.Server

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
            self.data['server'].append({'ip':server.ip,
                                    'username':server.username,
                                    'password':server.password,
                                    'ssh_username':server.ssh_username,
                                    'ssh_password':server.ssh_password})
          
            
        