#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

#import json

class OperationManager(GenericScovilleObject):
    def __init__(self, parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.refresh()
        
    def getOperationsRecursive(self):
        ret = []
        for op in self.children:
            if op.__class__.__name__ == 'Operation':
                ret.extend(op.getChildOperations())
                ret.append(op)
        return ret
    
    def refreshCallback(self,json):
        ids = [o.getId() for o in self.children]
        for operation in json.values():
            if operation['id'] not in ids:
                if operation['parent'] is not None:
                    parent = self.getOperationById(operation['parent'])
                    parent.addChild(Operation(parent,operation))
                else:
                    self.addChild(Operation(self,operation))
            else:
                self.getOperationById(operation['id']).update(operation)
                
    def getOperationById(self, operationId):
        for operation in self.children:
            if operation.data['id'] == operationId:
                return operation
        return None    
                
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
    
    def getChildOperations(self):
        ret = []
        for op in self.children:
            if op.__class__.__name__ == 'Operation':
                ret.extend(op.getChildOperations())
                ret.append(op)
        return ret
    
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