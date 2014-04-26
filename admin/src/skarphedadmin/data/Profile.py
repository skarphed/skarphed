#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import Crypto.Cipher.AES
import Crypto.PublicKey.RSA as RSA
import json
import os
import skarphedadmin.data.Server
from Instance import InstanceType

from skarphedcommon.errors import ProfileException

class Profile(object):
    STATE_EMPTY = 0
    STATE_LOADED = 1
    
    DATA_STRUCT = {
                   'privateKey':'',
                   'publicKey':'',
                   'server':[]
                   }
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.state = self.STATE_EMPTY  
        self.data = {}
        
    def create(self):
        if not os.path.exists(os.path.expanduser('~/.skarphedadmin')):
            os.mkdir(os.path.expanduser('~/.skarphedadmin'))
        if os.path.exists(os.path.expanduser('~/.skarphedadmin/'+self.username)):
            raise ProfileException(ProfileException.get_msg(0))
        assert len(self.password)%16 == 0 , "Password not divisible by 16"
        profilefile = open(os.path.expanduser('~/.skarphedadmin/'+self.username),'w')
        
        self.data=self.DATA_STRUCT
        
        aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
        js = json.encoder.JSONEncoder()
        clear = "SCOV"+js.encode(self.data)
        padding = "X"*(16-(len(clear)%16))
        profilefile.write(aes.encrypt(clear+padding))
        profilefile.close()
    
    def getPublicKey(self):
        if self.data.has_key('publickey') and self.data['publickey'] != '':
            return self.data['publickey']
        else:
            raise ProfileException(ProfileException.get_msg(1))
    
    def getPrivateKey(self):
        if self.data.has_key('privatekey') and self.data['privatekey'] != '':
            return self.data['privatekey']
        else:
            raise ProfileException(ProfileException.get_msg(2))
    
    def hasKeys(self):
        if self.data.has_key('privatekey') and self.data['privatekey'] != ''\
            and self.data.has_key('publickey') and self.data['publickey'] != '':
            
            return True
        return False
    
    def generateKeyPair(self):
        if (not self.data.has_key('privatekey') or self.data['privatekey'] == '')\
            and (not self.data.has_key('publickey') or self.data['publickey'] == ''):
            
            key = RSA.generate(1024, os.urandom)
            pubkey = key.publickey()
            self.data['privatekey'] = key.exportKey()
            self.data['publickey'] = pubkey.exportKey()
            self.save()
        
    def load(self):
        if not os.path.exists(os.path.expanduser('~/.skarphedadmin/'+self.username)):
            raise ProfileException(ProfileException.get_msg(3))
        profilefile = open(os.path.expanduser('~/.skarphedadmin/'+self.username),'rb')
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
                srv = skarphedadmin.data.Server.createServer()
                srv.setIp(server['ip'])
                srv.setName(server['name'])
                srv.setSSHName(server['ssh_username'])
                srv.setSSHPass(server['ssh_password'])
                srv.setTarget(server['target'])
                srv.establishConnections()
                for instance in server['instances']:
                    instanceType = InstanceType(instance['typename'],instance['typedisp'])
                    createdInstance = srv.createInstance(instanceType,instance['url'],instance['username'],instance['password'])
                    if createdInstance is None or createdInstance == False:
                        continue
                    if instance['typename'] == "database":
                        for schema in instance['schemas']:
                            createdInstance.registerSchema(schema['name'], schema['user'], schema['pass'])
                    elif instance['typename'] == "skarphed":
                        createdInstance.setPublicKey(instance['publickey'])
                    #elif instance['typename'] == "skarphed_repo":
                    #    createdInstance.establishConnections()
                 
        else:
            profilefile.close()
            raise ProfileException(ProfileException.get_msg(4))
    
    def save(self):
        self.updateProfile()
        if not os.path.exists(os.path.expanduser('~/.skarphedadmin')):
            os.mkdir(os.path.expanduser('~/.skarphedadmin'))
        profilefile = open(os.path.expanduser('~/.skarphedadmin/'+self.username),'wb')
        aes = Crypto.Cipher.AES.new(self.password, Crypto.Cipher.AES.MODE_ECB)
        js = json.encoder.JSONEncoder()
        clear = "SCOV"+js.encode(self.data)
        padding = "X"*(16-(len(clear)%16))
        profilefile.write(aes.encrypt(clear+padding))
        profilefile.close()
    
    def updateProfile(self, save=False):
        self.data['server'] = []
        for server in skarphedadmin.data.Server.getServers():
            instances = []
            for instance in server.getInstances():
                if instance.instanceTypeName == "database":
                    schemas = []
                    for schema in instance.getSchemas():
                        schemas.append({'name':schema.getName(),
                                        'user':schema.getUser(),
                                        'pass':schema.getPassword()})
                    instances.append({'typename':instance.instanceTypeName,
                            'typedisp':instance.displayName,
                            'url':'',
                            'schemas':schemas,
                            'username':instance.getUsername(),
                            'password':instance.getPassword()})
                elif instance.instanceTypeName == "skarphed":
                    instances.append({'typename':instance.instanceTypeName,
                            'typedisp':instance.displayName,
                            'url':instance.getUrl(),
                            'username':instance.getUsername(),
                            'password':instance.getPassword(),
                            'publickey':instance.getPublickey()})
                else:
                    instances.append({'typename':instance.instanceTypeName,
                            'typedisp':instance.displayName,
                            'url':instance.getUrl(),
                            'username':instance.getUsername(),
                            'password':instance.getPassword()})
            self.data['server'].append({'ip':server.ip,
                                    'name':server.getRawName(),
                                    'ssh_username':server.ssh_username,
                                    'ssh_password':server.ssh_password,
                                    'instances':instances,
                                    'target':server.getTarget().getName()})
        if save:
            self.save()
                
          
            
        
