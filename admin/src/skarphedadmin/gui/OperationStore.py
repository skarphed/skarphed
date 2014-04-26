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

import pygtk
pygtk.require("2.0")
import gtk

from skarphedadmin.gui import IconStock

from skarphedadmin.glue.lng import _

class StoreException(Exception):pass

class OperationStore(gtk.TreeStore):
    '''The Matchstore class is holding and managing the Data for the MatchTree. It communicates with the database'''
    WHITELISTED_CLASSES = ("Operation",)
    def __init__(self,*args,**kwargs):
        '''Constructor --'''
        assert kwargs['objectStore'] is not None, _("Need ObjectStore")
        gtk.TreeStore.__init__(self,*args)
        self.par = kwargs['parent']
        self.objectStore  = kwargs['objectStore']
        
        if kwargs['server'] is not None:
            self.server = kwargs['server']
            self.server.getOperationManager().addCallback(self.render)
        else:
            self.server = None
            self.objectStore.addCallback(self.render)
                
        self.busy = False # Prevent threadcollisions 
        self.root = self.append(None,(IconStock.ERROR,IconStock.OPERATION,_("Operationtree"),"",-2))
        #self.append(root,(IconStock.SKARPHED,'Skarphed Infrastructure',-2))
  
    def getPar(self):
        return self.par 

    def getApplication(self):
        return self.par.getApplication()
    
    def getIterById(self, obj_id):
        def search(model, path, rowiter, obj_id):
                val = model.get_value(rowiter,4)
                if val == obj_id:
                    model.tempiter = rowiter
            
        if not self.busy:
            self.busy = True
                    
            self.tempiter = None
            self.foreach(search, obj_id)
            
            rowiter=self.tempiter
            self.busy = False
            if rowiter is not None:
                return rowiter
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
        def search(model, path, rowiter):
            obj_id = model.get_value(rowiter,4)
            if obj_id >= 0:
                try:
                    obj = self.objectStore.getLocalObjectById(obj_id)
                #except data.Generic.GenericObjectStoreException,e:
                except Exception:
                    self.itersToRemove.append(rowiter)
                else:
                    model.set_value(rowiter,0,IconStock.ERROR)
                    model.set_value(rowiter,1,IconStock.OPERATION)
                    model.set_value(rowiter,2,obj.data['type'])
                    model.set_value(rowiter,3,obj.data['invoked'])
                    model.set_value(rowiter,4,obj_id)
                    self.objectsToAllocate.remove(obj)
                
        objectsAllocated = 1
        if self.server is not None:
            self.objectsToAllocate = self.server.getOperationManager().getOperationsRecursive()
        else:
            self.objectsToAllocate = self.objectStore.getAllOperations()
        self.itersToRemove= []
        self.foreach(search)
        
        for rowiter in self.itersToRemove:
            self.remove(rowiter)

        while objectsAllocated > 0:
            objectsAllocated = 0
            for obj in self.objectsToAllocate:
                if self.addObject(obj, False):
                    self.objectsToAllocate.remove(obj)
                    objectsAllocated+=1
        
        for obj in self.objectsToAllocate:
            self.addObject(obj, True)
        
        
