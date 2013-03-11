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


from data.Generic import GenericScovilleObject

from Module import Module

class Modules(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
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
    
    def getModuleById(self,moduleId):
        for module in self.children:
            if module.getId() == moduleId:
                return module
        return None
    
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getScoville(),self.refreshCallback, "getModules",[False])
    
    def getName(self):
        return "Modules"
    
    def getAllModules(self):
        return self.children
    
    def getAllWidgets(self):
        ret = []
        for module in self.getAllModules():
            ret.extend(module.getAllWidgets())
        return ret
    
    def moduleOperationCallback(self,json=None):
        self.updated()
        self.refresh()
        self.getScoville().getOperationManager().refresh()
    
    def installModule(self, module):
        self.getApplication().doRPCCall(self.getScoville(),self.moduleOperationCallback, "installModule",[module.data])       
    
    def uninstallModule(self, module):
        self.getApplication().doRPCCall(self.getScoville(),self.moduleOperationCallback, "uninstallModule",[module.data])
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()