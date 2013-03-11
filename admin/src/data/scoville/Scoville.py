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


from data.Generic import ObjectStore, GenericScovilleObject
from data.Instance import Instance, InstanceType

from Users import Users
from Modules import Modules
from Roles import Roles
from Sites import Sites
from Repository import Repository
from Template import Template
from Operation import OperationManager, OperationDaemon

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
from net.ScovilleUpload import ScovilleUpload

class ScovilleInstaller(GenericScovilleObject):
    class InstallThread(Thread):
        def __init__(self, installer):
            Thread.__init__(self)
            self.installer = installer

        def run(self):
            if self.installer.target=="Debian6/Apache2":
                self.installer.installDebian6()

    def __init__(self,data,server,target):
        GenericScovilleObject.__init__(self)
        self.server=server
        self.target=target
        self.data  = data
        self.installationId = int(random.random()*1000)
        self.BUILDPATH = "/tmp/scvinst"+str(self.installationId)+"/"
        self.installThread = self.InstallThread(self)
        self.status = 0

    def installDebian6(self):
        os.mkdir(self.BUILDPATH)

        apache_template = open("../installer/debian6_apache2/apache2.conf","r").read()
        apache_domain = ""
        if self.data['apache.domain'] != "":
            apache_domain = "ServerName "+self.data['apache.domain']
        apache_subdomain = ""
        if self.data['apache.subdomain'] != "":
            apache_subdomain = "ServerAlias "+self.data['apache.subdomain']
        apacheconf = apache_template%(self.data['apache.ip'],
                                      self.data['apache.port'],
                                      apache_domain,
                                      apache_subdomain)
        apacheconfresult = open(self.BUILDPATH+"apache2.conf","w")
        apacheconfresult.write(apacheconf)
        apacheconfresult.close()

        self.status = 10
        gobject.idle_add(self.updated)


        scv_config = {}
        for key,val in self.data.items():
            if key.startswith("core.") or key.startswith("db."):
                if key == "db.name":
                    scv_config[key] = val+".fdb"
                    continue
                scv_config[key] = val

        scv_config_defaults = {
            "core.session_duration":2,
            "core.session_extend":1,
            "core.cookielaw":1,
            "core.rendermode":"pure",
            "core.css_folder":"/static/css",
            "core.debug":True
        }

        scv_config.update(scv_config_defaults)

        jenc = json.JSONEncoder()
        config_json = open(self.BUILDPATH+"config.json","w")
        config_json.write(jenc.encode(scv_config))
        config_json.close()

        shutil.copyfile("../installer/debian6_apache2/instanceconf.py",self.BUILDPATH+"instanceconf.py")
        shutil.copyfile("../installer/debian6_apache2/scoville.conf",self.BUILDPATH+"scoville.conf")
        shutil.copyfile("../installer/debian6_apache2/install.sh", self.BUILDPATH+"install.sh")

        self.status = 30
        gobject.idle_add(self.updated)

        shutil.copytree("../../core/web",self.BUILDPATH+"web")
        shutil.copytree("../../core/lib",self.BUILDPATH+"lib")
        #shutil.copytree("../../python-jsonrpc",self.BUILDPATH+"python-jsonrpc")

        tar = tarfile.open(self.BUILDPATH+"scv_install.tar.gz","w:gz")
        tar.add(self.BUILDPATH+"apache2.conf")
        tar.add(self.BUILDPATH+"config.json")
        tar.add(self.BUILDPATH+"instanceconf.py")
        tar.add(self.BUILDPATH+"scoville.conf")
        tar.add(self.BUILDPATH+"install.sh")
        tar.add(self.BUILDPATH+"web")
        tar.add(self.BUILDPATH+"lib")
        #tar.add(self.BUILDPATH+"python-jsonrpc")
        tar.close()

        self.status = 45
        gobject.idle_add(self.updated)

        con = self.server.getSSH()
        con_stdin, con_stdout, con_stderr = con.exec_command("mkdir /tmp/scvinst"+str(self.installationId))

        self.status = 50
        gobject.idle_add(self.updated)


        con = self.server.getSSH()
        ftp = con.open_sftp()
        ftp.put(self.BUILDPATH+"scv_install.tar.gz","/tmp/scvinst"+str(self.installationId)+"/scv_install.tar.gz")
        ftp.close()

        self.status = 65
        gobject.idle_add(self.updated)


        con = self.server.getSSH()
        con_stdin, con_stdout, con_stderr = con.exec_command("cd /tmp/scvinst"+str(self.installationId)+"; tar xvfz scv_install.tar.gz -C / ; chmod 755 install.sh ; ./install.sh ")

        print con_stdout.read()
        
        shutil.rmtree(self.BUILDPATH)
        self.status = 100
        gobject.idle_add(self.updated)
        gobject.idle_add(self.addInstanceToServer)

    def addInstanceToServer(self):
        self.server.createInstance(InstanceType("scoville","Scoville"), "http://"+self.data['apache.domain'], "root", "root")
        self.destroy()


    def getName(self):
        return "Scoville Installer"

    def getStatus(self):
        return self.status

    def install(self):
        self.installThread.start()

class Scoville(Instance):
    STATE_OFFLINE = 0
    STATE_ONLINE = 1

    SCV_LOCKED = 0
    SCV_UNLOCKED = 1
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
    
    @classmethod
    def installNewScoville(cls, data, server, target):
        installer = ScovilleInstaller(data,server,target)
        installer.install()
        return installer

    def __init__(self, server, url="", username="", password=""):
        Instance.__init__(self,server)
        self.instanceTypeName = "scoville"
        self.displayName = "Scoville"
        self.state = self.STATE_OFFLINE
        self.scv_loggedin = self.SCV_LOCKED
        self.load = self.LOADED_NONE
        self.data = {}
        
        self.url = url
        self.username = username
        self.password = password
        
        self.users = None
        self.template = None
        self.roles = None
        self.modules = None
        self.sites = None
        self.repo = None
        self.operationManager = None
        self.operationDaemon = None
        
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
        self.loadRepository()
        if True: #'scoville.template.modify' in self.serverRights
            self.loadTemplate()
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
    
    def establishConnections(self):
        self.getServerInfo()
        self.authenticate()
    
    def getName(self):
        if self.load == self.LOADED_SERVERDATA:
            return self.data['name']+" [ "+self.url+" ]"
        elif self.load == self.LOADED_PROFILE:
            return " [ "+self.url+" ]"
        else:
            return "Unknown ScovilleServer"
    
    def loadTemplateCallback(self,res):
        if self.template is None:
            self.template = Template(self,res)
            self.children.append(self.template)
        else:
            self.template.refresh(res)
    
    
    def loadTemplate(self):
        self.getApplication().doRPCCall(self,self.loadTemplateCallback, "getCurrentTemplate")
    
    def getRepository(self):
        return self.repo
    
    def loadRepositoryCallback(self,res):
        repo = Repository(self,res['ip'],res['port'],res['name'])
        self.repo = repo
        self.updated()
    
    def loadRepository(self):
        self.getApplication().doRPCCall(self,self.loadRepositoryCallback, "getRepository")
    
    def setRepositoryCallback(self,res):
        self.loadRepository()
        
    def setRepository(self,host,port):
        self.getApplication().doRPCCall(self,self.setRepositoryCallback, "setRepository", [host,port])
    
    def uploadTemplateCallback(self,res):
        severe_error_happened = False
        for error in res:
            if error['severity'] > 0:
                severe_error_happened = True
                break
        #TODO: SOMEHOW DISPLAY ERRORLOG
        if not severe_error_happened:
            self.loadTemplate()
    
    def uploadTemplate(self, filepath):
        template_file = open(filepath,'r')
        templatedata = base64.encodestring(template_file.read())
        self.getApplication().doRPCCall(self,self.uploadTemplateCallback, "installTemplate", [templatedata])
        template_file.close()
        
    def loadProfileInfo(self,profileInfo):
        pass
    
    def getSCVState(self):
        return self.scv_loggedin
    
    def isOnline(self):
        return self.state==self.STATE_ONLINE
    
    def loadCssPropertySetCallback(self,res):
        self.cssPropertySet = json.JSONDecoder().decode(res)
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
    
    def getModules(self):
        return self.modules
    
    def getServer(self):
        pass
        return self.par.getServer()
    
    def getParent(self):
        return self.par
    
def getServers():
    return ObjectStore().getServers()

def createServer():
    return Scoville()