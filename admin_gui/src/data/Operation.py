#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

import json

class OperationManager(GenericScovilleObject):
    def __init__(self, parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
    
    def refreshCallback(self,json):
        ids = [o.getId() for o in self.children]
        for operation in json:
            if operation['id'] not in ids:
                self.addChild(Operation(self,operation))
            else:
                self.getOperationById(operation['id']).update(operation)
        
    def refresh(self):
        self.getApplication().doRPCCall(self.getServer(),self.refreshCallback, "getOperations")
    
    def getPar(self):
        return self.par
    
    def getServer(self):
        return self.getPar()
    
class Operation(GenericScovilleObject):
    def __init__(self,parent,data):
        GenericScovilleObject.__init__(self)
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
    
    def operationCommandCallback(self,json):
        self.updated()
    
    def cancel(self):
        self.getApplication().doRPCCall(self.getOperationManager().getServer(),self.operationCommandCallback, "cancelOperation",[self.getId()])
    
    def drop(self):
        self.getApplication().doRPCCall(self.getOperationManager().getServer(),self.operationCommandCallback, "dropOperation",[self.getId()])
    
    def retry(self):
        self.getApplication().doRPCCall(self.getOperationManager().getServer(),self.operationCommandCallback, "retryOperation",[self.getId()])
    
    def getName(self):
        return "Operation"
    
    def getPar(self):
        return self.par
    
    def getOperationManager(self):
        return self.getPar()