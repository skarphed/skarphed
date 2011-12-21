#!/usr/bin/python
#-*- coding: utf-8 -*-

import Crypto.Cipher.AES
import json
import os
import Server

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
        file = open(os.path.expanduser('~/.scovilleadmin/'+self.username),'w')
        
        self.data=self.DATA_STRUCT
        
        aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
        js = json.encoder.JSONEncoder()
        clear = "SCOV"+js.encode(self.data)
        padding = "X"*(16-(len(clear)%16))
        file.write(aes.encrypt(clear+padding))
        file.close()
    
    def load(self):
        if not os.path.exists(os.path.expanduser('~/.scovilleadmin/'+self.username)):
            raise ProfileException("Profile does not exist")
        file = open(os.path.expanduser('~/.scovilleadmin/'+self.username),'r')
        cipher = file.read()
        aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
        clear = aes.decrypt(cipher)
        if clear[0:4]=="SCOV":
             js = json.decoder.JSONDecoder()
             clear = clear.rstrip("X")
             self.data = js.decode(clear[4:])
             self.state = self.STATE_LOADED
             file.close()
             for server in self.data['server']:
                 srv = Server.createServer()
                 srv.setIp(server['ip'])
                 srv.setScvName(server['username'])
                 srv.setScvPass(server['password'])
                 srv.setSSHName(server['ssh_username'])
                 srv.setSSHPass(server['ssh_password'])
                 
        else:
            file.close()
            raise ProfileException("Could not Decode")
    
    def save(self):
        if self.state == self.STATE_LOADED:
            file = open(os.path.expanduser('~/.scovilleadmin/'+self.username),'w')
            aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
            js = json.encoder.JSONEncoder()
            clear = "SCOV"+js.encode(self.data)
            padding = "X"*(16-(len(clear)%16))
            file.write(aes.encrypt(clear+padding))
            file.close()
    
    def storeServer(self,server):
        for storedServer in self.data['server']:
            if storedServer['ip'] == server.ip:
                return
        self.data['server'].append({'ip':server.ip,
                                    'username':server.username,
                                    'password':server.password,
                                    'ssh_username':server.ssh_username,
                                    'ssh_password':server.ssh_password})
        self.save()    
            
        