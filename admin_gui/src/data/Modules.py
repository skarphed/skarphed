#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

from Module import Module
import json


class Modules(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        #HERE BE DRAGONS!
        data = json.JSONDecoder().decode(data)
        modulenames = [m.getModuleName() for m in self.children]
        for module in data:
            if module['name'] not in modulenames:
                self.addChild(Module(self,module))
            else:
                self.getModuleByName(module['name']).refresh(module)
        self.updated()       
    
    def getModuleByName(self,name):
        for module in self.children:
            if module.getModuleName() == name:
                return module
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getServer(),self.refreshCallback, "getModules",[False])
    
    def getName(self):
        return "Modules"
    
    def getAllModules(self):
        return self.children
    
    def moduleOperationCallback(self,json=None):
        self.updated()
        self.refresh()
        self.getServer().getOperationManager().refresh()
    
    def installModule(self, module):
        self.getApplication().doRPCCall(self.getServer(),self.moduleOperationCallback, "installModule",[module.data,0])       
    
    def uninstallModule(self, module):
        self.getApplication().doRPCCall(self.getServer(),self.moduleOperationCallback, "uninstallModule",[module.data,0])
    
    def getPar(self):
        return self.par
    
    def getServer(self):
        return self.getPar()