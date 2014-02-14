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


from data.Generic import ObjectStore, GenericSkarphedObject, GenericObjectStoreException
from data.Instance import Instance, InstanceType
import net.HTTPRpc

def rpc(callback=None, errorhandler=None):
    """
    This decorator is used to declare that a function
    exists at a core-site that can be called via rpc.

    for example: if you have a function doStuff()
    in core/lib/rpc.py, and want to call that function, write 
    like this in GUI-code:

    def doStuffCallback(self, data):
        print data 
        # do something with data

    @rpc(doStuffCallback)
    def doStuff(self, param1, param2, param3, param4="default"):
        pass

    calling doStuff("a","b","c") will cause the gui to do an
    rpc call to the skarphed-instance and deliver the result
    to doStuffCallback

    IMPORTANT: kwargs do _not_ work as expected here. you can only
      specify a default-argument for this function that will be
      transmitted _everytime_. You CANNOT overwrite them by using
      a different kwarg in your call
      As in our example, param4 will allways be "default".
    """
    def inner_rpc(func):
        def tortilla(*args, **kwargs):
            def cleanupArgs(*args, **kwargs):
                retargs = list(args)
                del(retargs[0])
                if func.__defaults__ is not None:
                    retargs.extend(func.__defaults__)
                return retargs

            handled_object = skarphed = args[0]
            while type(skarphed) != Skarphed:
                skarphed = skarphed.getPar()
            functionToCall = func.__name__
            args = cleanupArgs(*args,**kwargs)
            skarphed.doRPCCall(callback, functionToCall, handled_object, args, errorhandler)
        return tortilla
    return inner_rpc

def module_rpc(callback=None, errorhandler=None):
    """
    Module-RPC-Decorator.
    Basically the same thing as the regular rpc-decorator
    except, that this decorator is used to acces rpc-methods
    of the module that calls them.

    if the module on server-side has a methode retrieveId()
    you can write on the client-implementation of your module:

    def getIdCallback(self,data):
        pass
        #do tings with data

    @module_rpc(getIdCallback)
    def retrieveId(self):
        pass

    """
    def inner_rpc(func):
        def tortilla(*args, **kwargs):
            def cleanupArgs(*args, **kwargs):
                retargs = list(args)
                del(retargs[0])
                if func.__defaults__ is not None:
                    retargs.extend(func.__defaults__)
                return retargs

            handled_object = obj = args[0]
            application = args[0].getApplication()

            widget = None
            module = None
            while type(obj) != Skarphed:
                if obj.__class__.__name__ == "WidgetPage":
                    try:
                        widget = application.getLocalObjectById(obj.widgetId)
                        obj = widget.getPar()
                    except GenericObjectStoreException:
                        return
                if obj.__class__.__name__ == "ModulePage":
                    try:
                        module = application.getLocalObjectById(obj.moduleId)
                        obj = module.getPar()
                    except GenericObjectStoreException:
                        return
                if obj.__class__.__name__ == "Module":
                    module = obj
                obj = obj.getPar()
            skarphed = obj
            functionToCall = func.__name__
            args = cleanupArgs(*args,**kwargs)
            print widget
            print module
            print skarphed
            if widget is not None:
                args.insert(0, widget.getId())
            skarphed.doRPCCall(callback, "executeModuleMethod", handled_object, [module.getId(), functionToCall, args], errorhandler)
        return tortilla
    return inner_rpc

from Users import Users
from Modules import Modules
from Roles import Roles
from Sites import Sites
from Template import Template
from Operation import OperationManager, OperationDaemon
from View import Views

import gobject
from threading import Thread
import base64
import random
import os
from time import sleep

from common.errors import RepositoryException
from common.enums import ActivityType

#from glue.threads import KillableThread

class AbstractInstaller(GenericSkarphedObject):
    class InstallThread(Thread):
        def __init__(self, installer):
            Thread.__init__(self)
            self.installer = installer

        def run(self):
            self.installer.execute_installation()


    def __init__(self,data,server):
        GenericSkarphedObject.__init__(self)
        self.server=server
        self.data  = data
        self.domain = ""
        self.installationId = int(random.random()*1000)
        self.BUILDPATH = os.path.join("/","tmp","scvinst"+str(self.installationId))
        self.installThread = self.InstallThread(self)
        self.status = 0

    def execute_installation(self):
        pass #To be implemented in realization

    def addInstanceToServer(self):
        if self.domain != "":
            self.server.createInstance(InstanceType("skarphed","Skarphed"), "http://"+self.domain, "root", "root")
        else:
            self.server.createInstance(InstanceType("skarphed","Skarphed"), "http://"+self.server.getIp(), "root", "root")
        self.destroy()

    def getName(self):
        return "Skarphed Installer"

    def getStatus(self):
        return self.status

    def install(self):
        self.installThread.start()

class AbstractDestroyer(GenericSkarphedObject):
    class DestroyThread(Thread):
        def __init__(self, destroyer):
            Thread.__init__(self)
            self.destroyer = destroyer

        def run(self):
            self.destroyer.execute_destruction()

    def __init__(self, instanceid, instance):
        GenericSkarphedObject.__init__(self)
        self.instanceid = instanceid
        self.instance = instance
        self.status = 0
        self.destroyThread = self.DestroyThread(self)

    def execute_destruction(self):
        pass

    def removeInstanceFromServer(self):
        server = self.instance.getServer()
        server.removeInstance(self.instance)
        self.destroy()

    def getName(self):
        return "Skarphed Destroyer"

    def getStatus(self):
        return self.status

    def takedown(self):
        self.destroyThread.start()

class PokeThread(Thread):
    """
    This thread is repsonsible for poking the skarphed-core
    to get information about whether the skarphed-core has
    new information to display. For example when another
    user that operates on that server made some changes
    """
    POKEYNESS_MAX = 10
    POKEYNESS_MIN = 1
    def __init__(self, skarphed):
        Thread.__init__(self)
        self.pokeyness = 1.0
        self.last_amount = 0
        self.skarphed = skarphed
        self.lock = False
        if PokeThread.POKEYNESS_MAX < PokeThread.POKEYNESS_MIN:
            raise Exception("Pokeyness MAX mustbe greater or equal MIN")

    
    def run(self):
        while True:
            if self.skarphed.getApplication().quitrequest:
                break
            sleep(1/self.pokeyness*3)
            self.poke()
            self.lock = True
            while self.lock:
                sleep(0.2)

    def poke_callback(self, data):
        amount = data["amount"]
        activity_types = data["activity_types"]
        delta = self.last_amount-amount
        self.pokeyness -= 0.2
        if self.pokeyness < PokeThread.POKEYNESS_MIN:
            self.pokeyness = PokeThread.POKEYNESS_MIN
        if delta > 2:
            self.pokeyness += 2
            if self.pokeyness > PokeThread.POKEYNESS_MAX:
                self.pokeyness = PokeThread.POKEYNESS_MAX


        to_execute = []

        if ActivityType.USER in activity_types:
            to_execute.append(self.skarphed.getUsers().refresh)
            
        if ActivityType.MODULE in activity_types:
            to_execute.append(self.skarphed.getModules().refresh)

        if ActivityType.WIDGET in activity_types:
            for module in self.skarphed.getModules().getAllModules():
                to_execute.append(module.loadWidgets)

        if ActivityType.ROLE in activity_types:
            to_execute.append(self.skarphed.getRoles().refresh)

        if ActivityType.REPOSITORY in activity_types:
            to_execute.append(self.skarphed.getRepository)

        if ActivityType.PERMISSION in activity_types:
            if self.skarphed.getRoles().refresh not in to_execute:
                to_execute.append(self.skarphed.getRoles().refresh)


        if ActivityType.MENU in activity_types:
            for site in self.skarphed.getSites().getSites():
                to_execute.append(site.loadMenus)

        if ActivityType.VIEW in activity_types:
            views = self.skarphed.getViews().getViews()
            for view in views:
                if view.isFullyLoaded():
                    to_execute.append(view.loadFull)
            to_execute.append(self.skarphed.getViews().refresh)

        if ActivityType.REPOSITORY in activity_types:
            pass

        if ActivityType.TEMPLATE in activity_types:
            to_execute.append(self.skarphed.getTemplate().load)

        for method in to_execute:
            gobject.idle_add(method)

        self.lock = False

    @rpc(poke_callback)
    def poke(self):
        pass

    def getPar(self):
        return self.skarphed




class Skarphed(Instance):
    STATE_OFFLINE = 0
    STATE_ONLINE = 1

    SCV_LOCKED = 0
    SCV_UNLOCKED = 1
    
    LOADED_NONE = 0
    LOADED_PROFILE = 1
    LOADED_SERVERDATA = 2
    



    def __init__(self, server, url="", username="", password=""):
        Instance.__init__(self,server)
        self.instanceTypeName = "skarphed"
        self.displayName = "Skarphed"
        self.state = self.STATE_OFFLINE
        self.scv_loggedin = self.SCV_LOCKED
        self.load = self.LOADED_NONE
        self.data = {}
        self.refreshSessionState = False
        
        self.url = url
        self.username = username
        self.password = password
        self.publickey = None
        
        self.repo_url = ""

        self.users = None
        self.template = None
        self.roles = None
        self.modules = None
        self.sites = None
        self.operationManager = None
        self.operationDaemon = None

        self.maintenance_mode = True
        self.rendermode = None

        self.cssPropertySet = None

    def invokeDestructionCallback(self, data):
        instanceId = data
        if instanceId == None:
            print "No sufficient rights only root can destroy"
            return
        target = self.getServer().getTarget()
        destroyer = target.getDestroyer()(int(instanceId), self)
        destroyer.takedown()

    @rpc(invokeDestructionCallback)
    def getInstanceId(self):
        #HERE BE DRAGONS: invoke destruction is currently the only use
        #                 of getInstanceId, but this may change in the
        #                 future. Works for now, but likely won't always.
        pass

    def invokeDestruction(self):
        self.getInstanceId()

    def setRefreshSessionFlag(self):
        self.refreshSessionState = True

    def unsetRefreshSessionFlag(self):
        self.refreshSessionState = False

    def isRefreshingSession(self):
        return self.refreshSessionState

    def setUrl(self,url):
        self.url= url
        self.updated()
    
    def getUrl(self,without_proto=False):
        if without_proto:
            return self.url.replace("http://","",1)
        else:
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

    def setPublicKey(self, publickey):
        self.publickey = publickey

    def getPublickey(self):
        return self.publickey

    def loadPublicKeyCallback(self, result):
        if self.publickey == None:
            self.publickey = result
        else:
            if self.publickey == result:
                return
            else:
                pass #TODO Implement Error behaviour. this means, the publickey changed since last login

    @rpc(loadPublicKeyCallback)
    def getPublicKey(self):
        pass

    def loadPublicKey(self):
        self.getPublicKey()
    
    def getServerInfoCallback(self, result):
        self.data['name'] = result
        self.load = self.LOADED_SERVERDATA
        self.state = self.STATE_ONLINE
        self.updated()
    
    @rpc(getServerInfoCallback)
    def getServerInfo(self):
        pass
    
    def loadServerInfo(self):
        self.getServerInfo()

    def getMaintenanceModeCallback(self,data):
        self.maintenance_mode = data
        self.updated()

    @rpc(getMaintenanceModeCallback)
    def retrieveMaintenanceMode(self):
        pass

    def getMaintenanceMode(self):
        self.retrieveMaintenanceMode()

    def setMaintenanceModeCallback(self,data):
        self.getMaintenanceMode()

    @rpc(setMaintenanceModeCallback)
    def changeMaintenanceMode(self, state):
        pass

    def setMaintenanceMode(self, active):
        self.changeMaintenanceMode(active)    

    def isMaintenanceMode(self):
        return self.maintenance_mode

    def loadRendermodeCallback(self, data):
        self.rendermode = data
        self.updated()

    @rpc(loadRendermodeCallback)
    def retrieveRendermode(self):
        pass

    def loadRendermode(self):
        self.retrieveRendermode()

    def setRendermodeCallback(self, data):
        self.loadRendermode()

    @rpc(setRendermodeCallback)
    def changeRendermode(self, mode):
        pass

    def setRendermode(self, mode):
        self.changeRendermode(mode)

    def getRendermode(self):
        return self.rendermode

    def loadSkarphedChildren(self):
        self.loadPublicKey()
        self.getMaintenanceMode()
        self.loadRendermode()
        if 'skarphed.users.view' in self.serverRights:
            self.users = Users(self)
            self.addChild(self.users)
        if 'skarphed.modules.install' in self.serverRights or 'skarphed.modules.uninstall' in self.serverRights:
            self.modules = Modules(self)
            self.addChild(self.modules)
        if 'skarphed.roles.view' in self.serverRights:
            self.roles = Roles(self)
            self.addChild(self.roles)
        if True: #'skarphed.sites.view' in self.serverRights
            self.sites = Sites(self)
            self.addChild(self.sites)
        if True:
            self.views = Views(self)
            self.addChild(self.views)
        if True: #'skarphed.template.modify' in self.serverRights
            self.template = Template(self)
            self.addChild(self.template)
        if True: #'skarphed.operation.modify' in self.serverRights
            self.operationManager = OperationManager(self)
        
        #TODO: Fix Poke-GUI-hangup bug and uncomment following lines
        #self.pokethread = PokeThread(self)
        #self.pokethread.start()
    
    def authenticateCallback(self, result):
        if result == False:
            self.scv_loggedin = self.SCV_LOCKED
            self.serverRights = []
        else:
            self.scv_loggedin = self.SCV_UNLOCKED
            self.serverRights = result
        self.updated()
        self.loadSkarphedChildren()

    @rpc(authenticateCallback)
    def authenticateUser(self, username, password):
        pass

    def authenticate(self):
        self.authenticateUser(self.username,self.password)
    
    def checkPermission(self, permission):
        return permission in self.serverRights
    
    def establishConnections(self):
        self.loadServerInfo()
        self.authenticate()
    
    def getName(self):
        if self.load == self.LOADED_SERVERDATA:
            return self.data['name']+" [ "+self.url+" ]"
        elif self.load == self.LOADED_PROFILE:
            return " [ "+self.url+" ]"
        else:
            return "Unknown SkarphedServer"
    
    def getRepoURL(self):
        return self.repo_url    

    def getRepositoryCallback(self, data):
        self.repo_url = data["ip"]+":"+str(data["port"])
        self.updated()

    @rpc(getRepositoryCallback)
    def retrieveRepository(self):
        pass

    def getRepository(self):
        self.retrieveRepository()
        
    def setRepositoryCallback(self,res):
        self.modules.refresh()

    @rpc(setRepositoryCallback)
    def changeRepository(self, hostname, port):
        pass

    def setRepository(self,repostring):
        hostname = ""
        port = 80

        splitted = repostring.split(":")
        if len(splitted)==2:
            try:
                port = int(splitted[1])
            except ValueError:
                raise RepositoryException(RepositoryException.get_msg(101))
            if port > 65535 or port < 1:
                raise RepositoryException(RepositoryException.get_msg(101))
            hostname=splitted[0]
        elif len(splitted)==1:
            hostname=splitted[0]
        else:
            raise RepositoryException(RepositoryException.get_msg(100))

        if hostname == "":
            raise RepositoryException(RepositoryException.get_msg(102))

        self.changeRepository(hostname,port)
        self.repo_url = hostname+":"+str(port)
        
    def loadProfileInfo(self,profileInfo):
        pass
    
    def getSCVState(self):
        return self.scv_loggedin
    
    def isOnline(self):
        return self.state==self.STATE_ONLINE
    
    def loadCssPropertySetCallback(self,res):
        self.cssPropertySet = res
        self.updated()
    
    @rpc(loadCssPropertySetCallback)
    def getCssPropertySet(self, module_id=None, widget_id=None, session_id=None):
        pass

    def loadCssPropertySet(self):
        self.getCssPropertySet()
    
    def updateModulesCallback(self):
        self.modules.refresh()
    
    @rpc(updateModulesCallback)
    def invokeUpdateModules(self):
        pass

    def updateModules(self):
        self.invokeUpdateModules()
    
    def getCssPropertySetForGui(self):
        return self.cssPropertySet
    
    def setCssPropertySetFromGui(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,res):
        self.loadCssPropertySet()

    @rpc(saveCssPropertySetCallback)
    def setCssPropertySet(self, csspropertyset):
        pass
    
    def saveCssPropertySet(self):
        self.setCssPropertySet(self.cssPropertySet)
    
    def getOperationManager(self):
        return self.operationManager

    def getOperationDaemon(self):
        if self.operationDaemon is None:
            self.operationDaemon = OperationDaemon(self)
        return self.operationDaemon

    def uploadBinaryCallback(self, res):
        # res is the new ID of the uploaded binary file
        return res

    @rpc(uploadBinaryCallback)
    def storeBinary(self, data, filename):
        pass

    def uploadBinary(self, filepath):
        f = open(filepath, 'r')
        data = f.read()
        f.close()
        data = base64.b64encode(data)
        filename = filepath.split("/")[1:]
        self.storeBinary(data, filename)

    def getTemplate(self):
        return self.template
    
    def getModules(self):
        return self.modules

    def getSites(self):
        return self.sites

    def getViews(self):
        return self.views

    def getUsers(self):
        return self.users

    def getRoles(self):
        return self.roles

    def doRPCCall(self, callback, method, handled_object, params=[], errorcallback=None):
        """
        sends an http-call to this instance
        """
        call = net.HTTPRpc.SkarphedRPC(self,callback, method, handled_object, params, errorcallback)
        call.start()
    
    def getServer(self):
        pass
        return self.par.getServer()
    
    def getParent(self):
        return self.par
    
def getServers():
    return ObjectStore().getServers()

def createServer():
    return Skarphed()

