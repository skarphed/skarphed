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


from skarphedadmin.data.Generic import GenericSkarphedObject
from skarphedadmin.data.skarphed.Skarphed import rpc

from Module import Module

class Modules(GenericSkarphedObject):
    def __init__(self,parent):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self._repo_state = False
        self.updated()
        self.refresh()

    def refreshCallback(self,data):
        remote_modules = data['modules']
        self._repo_state = data['repostate']
        modulenames = [m.getModuleName() for m in self.children]
        for module in remote_modules:
            if module['name'] not in modulenames:
                self.addChild(Module(self,module))
            else:
                self.getModuleByName(module['name']).refresh(module)
        result_modulenames = [m['name'] for m in remote_modules]
        for module in self.children:
            if module.getModuleName() not in result_modulenames:
                self.removeChild(module)
        self.updated()
        self.getApplication().getObjectStore().updated()

    @rpc(refreshCallback)
    def getModules(self, installed_only=False):
        pass

    def refresh(self):
        self.getModules()
    
    def getRepoState(self):
        return self._repo_state
    
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
    
    def getName(self):
        return "Modules"
    
    def getAllModules(self):
        return self.children
    
    def getAllWidgets(self):
        ret = []
        for module in self.getAllModules():
            ret.extend(module.getAllWidgets())
        return ret

    def getWidgetById(self, nr):
        for module in self.getAllModules():
            widget = module.getWidgetById(nr)
            if widget is not None:
                return widget
        return None
    
    def moduleOperationCallback(self,json=None):
        self.updated()
        self.refresh()
        self.getSkarphed().getOperationManager().refresh()
    
    @rpc(moduleOperationCallback)
    def installModule(self, moduledata):
        pass
    
    @rpc(moduleOperationCallback)
    def uninstallModule(self, moduledata):
        pass
    
    def invokeInstallModule(self, module):
        self.installModule(module.data)

    def invokeUninstallModule(self, module):
        self.uninstallModule(module.data)

    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()
