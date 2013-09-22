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


from data.Generic import GenericSkarphedObject
from data.skarphed.Skarphed import rpc

from threading import Thread
from time import sleep

class OperationManager(GenericSkarphedObject):
    class RefreshThread(Thread):
        def __init__(self, operationManager):
            Thread.__init__(self)
            self.opm = operationManager
            
        def run(self):
            while True:
                sleep(0.5)
                if self.opm.periodicRefresh:
                    self.opm.refresh()
                if self.opm.getApplication().quitrequest:
                    break
            
    def __init__(self, parent):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.refresh()
        self.periodicRefresh = False
        self.refreshThread = self.RefreshThread(self)
        self.refreshThread.start()
        
        
    def getOperationsRecursive(self):
        ret = []
        for op in self.children:
            if op.__class__.__name__ == 'Operation':
                ret.extend(op.getChildOperations())
                ret.append(op)
        return ret
    
    def refreshCallback(self,json):
        ids = [o.getId() for o in self.children]
        if type(json) == list:
            json = {}
        processedOperations = []
        for operation in json.values():
            if operation['id'] not in ids:
                if operation['parent'] is not None:
                    parent = self.getOperationById(operation['parent'])
                    parent.addChild(Operation(parent,operation))
                else:
                    self.addChild(Operation(self,operation))
            else:
                self.getOperationById(operation['id']).update(operation)
            processedOperations.append(operation['id'])
        for operation in self.children:
            if operation.getId() not in processedOperations:
                typ = operation.data['type']
                if typ in ('ModuleInstallOperation','ModuleUninstallOperation','ModuleUpdateOperation'):
                    operation.getOperationManager().getSkarphed().getModules().refresh()
                self.children.remove(operation)
                operation.destroy()
        self.updated()
        
        if len(self.children) > 0:
            self.periodicRefresh = True
        else:
            self.periodicRefresh = False
                
    def getOperationById(self, operationId):
        for operation in self.children:
            if operation.data['id'] == operationId:
                return operation
        return None

    @rpc(refreshCallback)
    def getOperations(self):
        pass
                
    def refresh(self):
        self.getOperations()
    
    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
    
class Operation(GenericSkarphedObject):
    PENDING = 0
    ACTIVE = 1
    FAILED = 2
    def __init__(self,parent,data):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.data = data
        self.updated()
    
    def update(self,data):
        self.data=data
        self.updated()
    
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None
    
    def getChildOperations(self):
        ret = []
        for op in self.children:
            if op.__class__.__name__ == 'Operation':
                ret.extend(op.getChildOperations())
                ret.append(op)
        return ret
    
    def operationCommandCallback(self,json):
        self.updated()
    
    @rpc(operationCommandCallback)
    def cancelOperation(self, operationId):
        pass

    def cancel(self):
        self.cancelOperation(self.getId())
    
    @rpc(operationCommandCallback)
    def dropOperation(self, operationId):
        pass

    def drop(self):
        self.dropOperation(self.getId())
    
    @rpc(operationCommandCallback)
    def retryOperation(self, operationId):
        pass

    def retry(self):
        self.retryOperation(self.getId())
    
    def getName(self):
        return "Operation"
    
    def getPar(self):
        return self.par
    
    def getOperationManager(self):
        par = self.getPar()
        if par.__class__.__name__ == "Operation":
            return par.getOperationManager()
        else: # OperationManager
            return par

class OperationDaemon(GenericSkarphedObject):
    def __init__(self,par):
        GenericSkarphedObject.__init__(self)
        self.par = par
        self.status = False
        self.refresh()

    def getStatus(self):
        return self.status

    def refreshCallback(self, res):
        self.status = res
        self.updated()

    @rpc(refreshCallback)
    def getOperationDaemonStatus(self):
        pass

    def refresh(self):
        self.getOperationDaemonStatus()

    def opCallback(self, res):
        self.refresh()

    @rpc(opCallback)
    def startOperationDaemon(self):
        pass

    def start(self):
        self.startOperationDaemon()

    @rpc(opCallback)
    def stopOperationDaemon(self):
        pass

    def stop(self):
        self.stopOperationDaemon()

    @rpc(opCallback)
    def restartOperationDaemon(self):
        pass

    def restart(self):
        self.restartOperationDaemon()

    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
        
