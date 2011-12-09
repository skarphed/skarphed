#!/usr/bin/python
#-*- coding: utf-8 -*-



class GenericObjectStoreException(Exception): pass

class GenericScovilleObject(object):
    localObjects = {}
    localIDcounter = 0
    def __init__(self):
        GenericScovilleObject.localIDcounter+=1 
        self.localId = GenericScovilleObject.localIDcounter
        self.localObjects[self.localId] = self
        self.par = None
        
        self.name = "GenericObject"
        
    def __del__(self):
        del (self.localObjects[self.localId])
    
    def getPar(self):
        if self.par is None:
            raise GenericObjectStoreException("This object has no parent")
        else:
            return self.par
    
    def setPar(self,parent):
        self.par = parent
    
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