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



def setApplicationReference(app):
    global APPLICATION
    APPLICATION = app

APPLICATION = None
    

class GenericObjectStoreException(Exception): pass

class ObjectStore(object):
    localObjects = {}
    localIDcounter = 0
    callbacks = []
    mainTreeCallback = None
    
    
    def getLocalObjectById(self,obj_id):
        try:
            return ObjectStore.localObjects[obj_id]
        except Exception:
            raise GenericObjectStoreException("Object does not exist")
    
    def getChildrenOf(self,obj):
        res = []
        for element in ObjectStore.localObjects.values():
            if element.getLocalId() == obj.getLocalId():
                res.append(element)
        return res

    def setMainTreeCallback(self, cb):
        ObjectStore.mainTreeCallback = cb
        ObjectStore.callbacks.append(cb)

    def addCallback(self, cb):
        ObjectStore.callbacks.append(cb)
    
    def removeCallback(self, cb):
        if cb in ObjectStore.callbacks:
            ObjectStore.callbacks.remove(cb)
    
    def updated(self):
        for cb in ObjectStore.callbacks:
            cb()
    
    def getAllOfClass(self, obj, parent=None):
        if type(obj) != str:
            obj = obj.__class__.__name__
        res = []
        #TODO: Add performance by using parent.children if parent is set instead of ObjectStore.localObjects
        for element in ObjectStore.localObjects.values():
            if element.__class__.__name__ == obj:
                if parent is not None and not element.isChildOf(parent):
                    continue
                res.append(element)
        return res

    def getServers(self):
        return self.getAllOfClass("Server")
    
    def clear(self):
        """
        TODO: Eventually linear object deletion causes the errors. recursive deletion should work
        new plan: find all without parent, delete those ones recursively
        """
        rootelements = []
        for element in ObjectStore.localObjects.values():
            try:
                par = element.getPar()
            except GenericObjectStoreException:
                rootelements.append(element)

        for element in rootelements:
            element.destroy()
        ObjectStore.callbacks = [ObjectStore.mainTreeCallback]
        
        ObjectStore.localIDcounter = 0
        self.updated()
        
    def getAllOperations(self):
        ret = []
        for element in ObjectStore.localObjects.values():
            if element.__class__.__name__ == 'OperationManager':
                ret.extend(element.getOperationsRecursive)
        
class GenericSkarphedObject(object):  
    def __init__(self):
        assert APPLICATION is not None, "Initialize Applicationreference for Datalayer first!"
        self.app = APPLICATION
        ObjectStore.localIDcounter+=1 
        self.localId = ObjectStore.localIDcounter
        ObjectStore.localObjects[self.localId] = self
        if not hasattr(self, 'par'):
            self.par = None
        self.updateCallbacks = []
        self.children = []
        
        self.name = "GenericObject"
        
    def destroy(self):
        self.__del__()
        
    def __del__(self):
        for child in self.children:
            child.destroy()
        if hasattr(self, 'localId') and ObjectStore.localObjects.has_key(self.localId):
            del (ObjectStore.localObjects[self.localId])
        self.updated()
    
    def addChild(self,child):
        if child not in self.children:
            self.children.append(child)

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)
    
    def getPar(self):
        if self.par is None:
            raise GenericObjectStoreException("This object has no parent")
        else:
            return self.par
    
    def getApplication (self):
        return self.app
    
    def setPar(self,parent):
        self.par = parent

    def isChildOf(self, obj):
        par = None
        try:
            par = self.getPar()
        except GenericObjectStoreException:
            return False
        if self.getPar() == obj:
            return True
        else:
            return self.getPar().isChildOf(obj)
    
    def isParentOf(self, obj):
        for child in self.children:
            if child == obj:
                return True
            if child.isParentOf(obj):
                return True
        return False

    def addCallback(self, callback):
        if callback not in self.updateCallbacks:
            self.updateCallbacks.append(callback)
    
    def removeCallback(self, callback):
        if callback in self.updateCallbacks:
            self.updateCallbacks.remove(callback)
    
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
    

    