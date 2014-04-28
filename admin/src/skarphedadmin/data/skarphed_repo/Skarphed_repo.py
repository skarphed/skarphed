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


from skarphedadmin.data.Generic import ObjectStore
from skarphedadmin.data.Instance import Instance
from skarphedadmin.net.SkarphedRepository import SkarphedRepository
import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
import base64

class Skarphed_repo(Instance):
    STATE_OFFLINE = 0
    STATE_ONLINE = 1

    SCV_LOCKED = 0
    SCV_UNLOCKED = 1
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
     
    def __init__(self, server, url="", username="", password=""):
        Instance.__init__(self,server)
        self.instanceTypeName = "skarphed_repo"
        self.displayName = "Skarphed Repository"
        self.state = self.STATE_OFFLINE
        self.loggedin = self.SCV_LOCKED
        self.load = self.LOADED_NONE
        self.data = {'modules':[], 'developers':[], 'templates':[]}
        
        self.url = url
        self.username = username
        self.password = password

        self.newPassword = None
        
    def setUrl(self,url):
        self.url= url
        self.updated()
    
    def getUrl(self):
        return self.url
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def setUsername(self,username):
        self.username = str(username)
    
    def setPassword(self,password):
        self.password = str(password)

    def authenticateCallback(self, result):
        if bool(result['r']) == True:
            self.loggedin = self.SCV_LOCKED
        else:
            self.loggedin = self.SCV_UNLOCKED
        if self.loggedin == self.SCV_UNLOCKED:
            self.loadDevelopers()
        self.loadModules()
        self.loadTemplates()
        self.updated()
        
    def authenticate(self):
        SkarphedRepository(self, {'c':100,'dxd':self.getPassword()}, self.authenticateCallback).start()
    
    def loadModulesCallback(self,result):
        result = result['r']
        modulenames = [m['name'] for m in self.data['modules']]
        for module in result:
            if module['name'] not in modulenames:
                self.data['modules'].append(module)
        self.updated()       

    def loadTemplatesCallback(self,result):
        result = result['r']
        template_ids = [t['id'] for t in self.data['templates']]
        for template in result:
            if template['id'] not in template_ids:
                self.data['templates'].append(template)
        res_template_ids = [t['id'] for t in result]
        for template in self.data['templates']:
            if template['id'] not in res_template_ids:
                self.data['templates'].remove(template)
        self.updated()

    def loadModules(self):
        SkarphedRepository(self, {'c':1}, self.loadModulesCallback).start()
    
    def loadTemplates(self):
        SkarphedRepository(self, {'c':8}, self.loadTemplatesCallback).start()

    def getModules(self):
        return self.data['modules']

    def getTemplates(self):
        return self.data['templates']
    
    def loadDevelopersCallback(self, result):
        result = result['r']
        developernames = [d['name'] for d in self.data['developers']]
        for developer in result:
            if developer['name'] not in developernames:
                self.data['developers'].append(developer)
        self.updated()       
    
    def loadDevelopers(self):
        SkarphedRepository(self, {'c':107}, self.loadDevelopersCallback).start()
    
    def getDevelopers(self):
        return self.data['developers']
    
    def establishConnections(self):
        self.authenticate()
    
    def changePasswordCallback(self,result):
        #TODO: check for error
        self.password = self.newPassword
        self.newPassword = None
        self.updated()
    
    def changePassword(self, password):
        SkarphedRepository(self, {'c':102,'dxd':password}, self.changePasswordCallback).start()
        self.newPassword = password
        
    def developerCallback(self,result):
        self.loadDevelopers()
    
    def registerDeveloper(self, name, fullname, publickey):
        SkarphedRepository(self, {'c':103,'name':name,'fullName':fullname,'publicKey':publickey}, self.developerCallback).start()
    
    def unregisterDeveloper(self, devId):
        SkarphedRepository(self, {'c':104,'devId':devId}, self.developerCallback).start()
    
    def moduleCallback(self,result):
        self.loadModules()
    
    def uploadModule(self, filepath):
        privatekey = self.getApplication().activeProfile.getPrivateKey()
        
        moduleFile = open(filepath,'r')
        data = moduleFile.read()
        moduleFile.close()
        
        key = RSA.importKey(privatekey)
        dataHash = SHA256.new(data)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(dataHash)
        signature = base64.b64encode(signature)
        
        SkarphedRepository(self, {'c':105,'data':base64.b64encode(data), 'signature':signature}, self.moduleCallback).start()

    def templateCallback(self,result):
        self.loadTemplates()
    
    def uploadTemplate(self, filepath):
        privatekey = self.getApplication().activeProfile.getPrivateKey()
        
        moduleFile = open(filepath,'r')
        data = moduleFile.read()
        moduleFile.close()
        
        key = RSA.importKey(privatekey)
        dataHash = SHA256.new(data)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(dataHash)
        signature = base64.b64encode(signature)
        
        SkarphedRepository(self, {'c':108,'data':base64.b64encode(data), 'signature':signature}, self.templateCallback).start()
    
    def deleteTemplate(self, template_id):
        SkarphedRepository(self, {'c':109,'id':int(template_id)}, self.templateCallback).start()    

    #TODO: Check if legacy or needed
    def deleteModule(self,moduleName):
        SkarphedRepository(self, {'c':106,'moduleIdentifier':moduleName}, self.moduleCallback).start()
    
    def getName(self):
        if self.url is not None:
            return "Repository [ "+self.url+" ]"
        else:
            return "Unknown SkarphedRepository"

    def getState(self):
        return self.loggedin
    
    def isOnline(self):
        return self.state==self.STATE_ONLINE

    def isAuthenticated(self):
        return self.loggedin == self.SCV_UNLOCKED
  
    def getServer(self):
        return self.par.getServer()
    
    def getParent(self):
        return self.par
 
class OfficialRepo(Skarphed_repo):
    def __init__(self):
        Skarphed_repo.__init__(self, None, "http://repo.skarphed.org")
    def getName(self):
        return "The skarphed.org Repository"
   
def getServers():
    return ObjectStore().getServers()

def createServer():
    return Skarphed_repo()
