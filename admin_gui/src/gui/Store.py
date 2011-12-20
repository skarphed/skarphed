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
        gtk.TreeStore.__init__(self,*args)
        self.par = kwargs['parent']
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
        
    
    def addServer(self,server):
        root = self.getIterById(-2)
        ip = server.getIp()
        if server.data.has_key('name'):
            name = server.data['name']
        else:
            name = "< adsfadsf >"
        self.append(root,(IconStock.SERVER, name+" [ "+ip+" ] ",server.getLocalId()))
        server.addCallback(self.render)
    
    def render(self):
        def search(model, path, iter):
            app = self.getApplication()
            try:
                obj = app.getLocalObjectById(model.get_value(iter,2))
            except data.Generic.GenericObjectStoreException,e:
                model.remove(iter)
                return
            if obj.hasAttribute('data') and type(obj.data) == 'dict' \
            and obj.data.has_key('name') and type(obj.data['name']) == 'str':
                model.set_value(iter,1,obj.data['name']) 
            
        self.foreach(search)
        