#!/usr/bin/python
#-*- coding: utf-8 -*-


def setApplicationReference(app):
    global APPLICATION
    APPLICATION = app

APPLICATION = None
    

class GenericObjectStoreException(Exception): pass

class GenericScovilleObject(object):
    localObjects = {}
    localIDcounter = 0
    
    
    
    
    def __init__(self):
        assert APPLICATION is not None, "Initialize Applicationreference for Datalayer first!"
        GenericScovilleObject.localIDcounter+=1 
        self.localId = GenericScovilleObject.localIDcounter
        self.localObjects[self.localId] = self
        self.par = None
        self.updateCallbacks = []
        
        
        self.name = "GenericObject"
        
    def __del__(self):
        if hasattr(self, 'localId'):
            del (self.localObjects[self.localId])
    
    def getPar(self):
        if self.par is None:
            raise GenericObjectStoreException("This object has no parent")
        else:
            return self.par
    
    def setPar(self,parent):
        self.par = parent
    
    def addCallback(self, callback):
        if callback not in self.updateCallbacks:
            self.updateCallbacks.append(callback)
    
    def updated(self):
        for cb in self.updateCallbacks:
            cb()
    
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name= name
        
    def getLocalId(self):
        return self.localId
    
    def getLocalObjectById(id):
        try:
            return GenericScovilleObject.localObjects[id]
        except Exception ,e :
            raise GenericObjectStoreException("Object does not exist")