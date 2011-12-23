#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

import IconStock

class StoreException(Exception):pass

class Store(gtk.TreeStore):
    '''The Matchstore class is holding and managing the Data for the MatchTree. It communicates with the database'''
    def __init__(self,*args,**kwargs):
        '''Constructor --'''
        assert kwargs['objectStore'] is not None, "brauhe nen objectstore, verdammtnochmal!"
        gtk.TreeStore.__init__(self,*args)
        self.par = kwargs['parent']
        self.objectStore  = kwargs['objectStore']
        self.objectStore.addCallback(self.render)
        self.busy = False # Prevent threadcollisions 
        root = self.append(None,(IconStock.SCOVILLE,"Scoville Infrastructure",-2))
        #self.append(root,(IconStock.SCOVILLE,'Scoville Infrastructure',-2))
  
    def getPar(self):
        return self.par 

    def getApplication(self):
        return self.par.getApplication()
    
    def getIterById(self, id):
        def search(model, path, iter, id):
                if model.get_value(iter,2) == id:
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
        obj = self.objectStore.getLocalObjectById(obj)
        try:
            parentIter = self.getIterById(obj.getPar().getLocalId())
            self.append(parentIter,(IconStock.SERVER, obj.getName(),obj.getLocalId()))
            return True
        except:
            if addToRootIfNoParent or obj.par is None: 
                root = self.getIterById(-2)
                self.append(root,(IconStock.SERVER, obj.getName(),obj.getLocalId()))
                return True
            return False
        

    def render(self):
        def search(model, path, iter):
            id = model.get_value(iter,2)
            print id
            if id >= 0:
                try:
                    obj = self.objectStore.getLocalObjectById(model.get_value(iter,2))
                #except data.Generic.GenericObjectStoreException,e:
                except Exception,e:
                    self.itersToRemove.append(iter)
                else:
                    if hasattr(obj,'data') and type(obj.data) == dict \
                    and obj.data.has_key('name') and type(obj.data['name']) == unicode:
                        model.set_value(iter,1,obj.data['name']) 
                    self.objectsToAllocate.remove(id)
                
        objectsAllocated = 1
        self.objectsToAllocate = self.objectStore.localObjects.keys()    
        self.itersToRemove= []
        self.foreach(search)
        
        for iter in self.itersToRemove:
            self.remove(iter)
        
        while objectsAllocated > 0:
            objectsAllocated = 0
            for id in self.objectsToAllocate:
                if self.addObject(id, False):
                    self.objectsToAllocate.remove(id)
                    objectsAllocated+=1
        
        for id in self.objectsToAllocate:
            self.addObject(id, True)
        
        