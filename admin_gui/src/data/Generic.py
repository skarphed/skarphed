#!/usr/bin/python
#-*- coding: utf-8 -*-

class GenericObjectStoreException(Exception): pass

class GenericScovilleObject(object):
    localObjects = {}
    localIDcounter = 0
    def __init__(self):
        self.localIDcounter+=1
        self.localId = self.localIDcounter
        self.localObjects[self.localId] = self
    def __del__(self):
        del (self.localObjects[self.localId])
    def getLocalObjectById(id):
        try:
            return GenericScovilleObject.localObjects[id]
        except Exception ,e :
            raise GenericObjectStoreException("Object does not exist")