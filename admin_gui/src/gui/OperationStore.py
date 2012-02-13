#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

import IconStock

class StoreException(Exception):pass

class OperationStore(gtk.TreeStore):
    '''The Matchstore class is holding and managing the Data for the MatchTree. It communicates with the database'''
    WHITELISTED_CLASSES = ("Operation",)
    def __init__(self,*args,**kwargs):
        '''Constructor --'''
        assert kwargs['objectStore'] is not None, "brauhe nen objectstore, verdammtnochmal!"
        gtk.TreeStore.__init__(self,*args)
        
        if kwargs['server'] is not None:
            self.server = kwargs['server']
        else:
            self.server = None
        self.par = kwargs['parent']
        self.objectStore  = kwargs['objectStore']
        self.objectStore.addCallback(self.render)
        self.busy = False # Prevent threadcollisions 
        root = self.append(None,(IconStock.ERROR,IconStock.OPERATION,"Operationtree","",-2))
        #self.append(root,(IconStock.SCOVILLE,'Scoville Infrastructure',-2))
  
    def getPar(self):
        return self.par 

    def getApplication(self):
        return self.par.getApplication()
    
    def getIterById(self, id):
        def search(model, path, iter, id):
                val = model.get_value(iter,4)
                if val == id:
                    model.tempiter = iter
            
        if not self.busy:
            self.busy = True
                    
            self.tempiter = None
            self.foreach(search, id)
            
            iter=self.tempiter
            self.busy = False
            if iter is not None:
                return iter
            else:
                return None
        else:
            raise StoreException("store is busy")

    def addObject(self,obj,addToRootIfNoParent=True):
        if obj.__class__.__name__ not in self.WHITELISTED_CLASSES:
            return True
        try:
            parent = obj.getPar()
            if parent.__class__.__name__ == "Operation":
                parentIter = self.getIterById(parent.getLocalId())
                self.append(parentIter,(IconStock.ERROR,IconStock.OPERATION, obj.getName(), obj.data['invoked'],obj.getLocalId()))
                return True
            else:
                raise Exception()
        except:
            if addToRootIfNoParent or obj.data['parent'] is None: 
                root = self.getIterById(-2)
                self.append(root,(IconStock.ERROR,IconStock.OPERATION, obj.getName(), obj.data['invoked'],obj.getLocalId()))
                return True
            return False
    

    def render(self):
        def search(model, path, iter):
            id = model.get_value(iter,4)
            #print id
            if id >= 0:
                try:
                    obj = self.objectStore.getLocalObjectById(id)
                #except data.Generic.GenericObjectStoreException,e:
                except Exception,e:
                    self.itersToRemove.append(iter)
                else:
                    model.set_value(iter,0,obj.data['status'] == 1)
                    model.set_value(iter,1,IconStock.OPERATION)
                    model.set_value(iter,2,obj.getName())
                    model.set_value(iter,3,obj.data['invoked'])
                    model.set_value(iter,4,id)
                    self.objectsToAllocate.remove(obj)
                
        objectsAllocated = 1
        if self.server is not None:
            self.objectsToAllocate = self.server.getOperationManager().getOperationsRecursive()
        else:
            self.objectsToAllocate = self.objectStore.getAllOperations()
        self.itersToRemove= []
        self.foreach(search)
        
        for iter in self.itersToRemove:
            self.remove(iter)
        
        while objectsAllocated > 0:
            objectsAllocated = 0
            for obj in self.objectsToAllocate:
                if self.addObject(obj, False):
                    self.objectsToAllocate.remove(obj)
                    objectsAllocated+=1
        
        for obj in self.objectsToAllocate:
            self.addObject(obj, True)
        
        