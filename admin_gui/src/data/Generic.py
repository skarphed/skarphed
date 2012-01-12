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
                res.append(element)
        return res
    def addCallback(self, cb):
        ObjectStore.callbacks.append(cb)
    
    def updated(self):
        for cb in ObjectStore.callbacks:
            cb()
    
    def getServers(self):
        res = []
        for element in ObjectStore.localObjects.values():
            if element.__class__.__name__ == 'Server':
                res.append(element)
        return res
    
    def clear(self):
        for element in ObjectStore.localObjects.keys():
            ObjectStore.localObjects[element].destroy()
        ObjectStore.localIDcounter = 0
        self.updated()
        
class GenericScovilleObject(object):  
    def __init__(self):
        assert APPLICATION is not None, "Initialize Applicationreference for Datalayer first!"
        self.app = APPLICATION
        ObjectStore.localIDcounter+=1 
        self.localId = ObjectStore.localIDcounter
        ObjectStore.localObjects[self.localId] = self
        self.par = None
        self.updateCallbacks = []
        self.children = []
        
        self.name = "GenericObject"
        
    def destroy(self):
        self.__del__()
        
    def __del__(self):
        for child in self.children:
            child.destroy()
        if hasattr(self, 'localId'):
            del (ObjectStore.localObjects[self.localId])
        self.updated()
    
    def addChild(self,child):
        if child not in self.children:
            self.children.append(child)
    
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
    

    