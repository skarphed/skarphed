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
                
    
    def getModuleByName(self,name):
        for module in self.children:
            if module.getModuleName() == name:
                return module
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getServer(),self.refreshCallback, "getModules",[True])
    
    def getName(self):
        return "Modules"
    
    def getPar(self):
        return self.par
    
    def getServer(self):
        return self.getPar()