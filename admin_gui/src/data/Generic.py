#!/usr/bin/python
#-*- coding: utf-8 -*-


def setApplicationReference(app):
    global APPLICATION
    APPLICATION = app

APPLICATION = None
    

class GenericObjectStoreException(Exception): pass

class ObjectStore(object):
    localObjects = {}
    localIDcounter = 0
    callbacks = []
    
    
    def getLocalObjectById(self,id):
        try:
            return ObjectStore.localObjects[id]
        except Exception ,e :
            raise GenericObjectStoreException("Object does not exist")
    
    def getChildrenOf(self,obj):
        res = []
        for element in ObjectStore.localObjects.values():
            if element.getLocalId() == obj.getLocalId():
                result.append(element)
        return res
    def addCallBack(self, cb):
        ObjectStore.callbacks.append(cb)
    
    def updated(self):
        for cb in ObjectStore.callbacks:
            cb()
    
class GenericScovilleObject(object):  
    def __init__(self):
        assert APPLICATION is not None, "Initialize Applicationreference for Datalayer first!"
        self.app = APPLICATION
        ObjectStore.localIDcounter+=1 
        self.localId = ObjectStore.localIDcounter
        ObjectStore.localObjects[self.localId] = self
        self.par = None
        self.updateCallbacks = []
        
        
        self.name = "GenericObject"
        
    def __del__(self):
        if hasattr(self, 'localId'):
            del (ObjectStore.localObjects[self.localId])
    
    def getPar(self):
        if self.par is None:
            raise GenericObjectStoreException("This object has no parent")
        else:
            return self.par
    
    def getApplication (self):
        return self.app
    
    def setPar(self,parent):
        self.par = parent
    
    def addCallback(self, callback):
        if callback not in self.updateCallbacks:
            self.updateCallbacks.append(callback)
    
    def updated(self):
        for cb in self.updateCallbacks:
            cb()
        ObjectStore().updated()
    
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name= name
        
    def getLocalId(self):
        return self.localId
    

    