#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

from Module import Module
import json


class Modules(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.modules = []
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        #HERE BE DRAGONS!
        data = json.JSONDecoder().decode(data)
        modulenames = [m.getModuleName() for m in self.modules]
        for module in data:
            if module['name'] not in modulenames:
                self.modules.append(Module(self,module))
            else:
                self.getUserByName(module['name']).refresh(module)
                
    
    def getModuleByName(self,name):
        for module in self.modules:
            if module.getModuleName() == name:
                return module
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getServer(),self.refreshCallback, "getModules")
    
    def getName(self):
        return "Modules"
    
    def getPar(self):
        return self.par
    
    def getServer(self):
        return self.getPar()