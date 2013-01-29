#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Scoville.
#
# Scoville is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Scoville is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Scoville. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


import pygtk
pygtk.require("2.0")
import gtk

import IconStock

class ObjectCombo(gtk.ComboBox):
    def __init__(self, par, objectType, selectedObject=None, selectFirst=False):
        gtk.ComboBox.__init__(self)
        self.par = par

        self.selectFirst = selectFirst
        self.firstSelected = False

        if type(objectType) != str:
            self.objectType = objectType.__class__.__name__
        else:
            self.objectType = objectType

        self.selectedObjectId = None
        if selectedObject is not None:
            self.selectedObjectId = selectedObject.getLocalId()

        self.model = gtk.ListStore(gtk.gdk.Pixbuf,str,int)
        
        self.set_model(self.model)
        self.iconrenderer = gtk.CellRendererPixbuf()
        self.pack_start(self.iconrenderer, True)
        self.add_attribute(self.iconrenderer, "pixbuf", 0)
        self.namerenderer = gtk.CellRendererText()
        self.pack_start(self.namerenderer, False)
        self.add_attribute(self.namerenderer, "text", 1)

        self.getApplication().getObjectStore().addCallback(self.render)
        self.render()

    def render(self):
        def search(model, path, rowiter, processed):
            val = model.get_value(rowiter,2)
            if val not in processed:
                model.itersToRemove.append(rowiter)
        
        objs = self.getApplication().getObjectStore().getAllOfClass(self.objectType)

        if len(objs)>=1 and self.selectFirst and self.selectedObjectId is None and not self.firstSelected:
            self.selectedObjectId = objs[0].getLocalId()
            self.firstSelected = True



        processedObjectIds = []
        for obj in objs:
            rowiter = self.getIterById(self.model, obj.getLocalId()) 
            if rowiter is None:
                self.model.append((IconStock.getAppropriateIcon(obj),obj.getName(),obj.getLocalId()))
            else:
                self.model.set_value(rowiter,0,IconStock.getAppropriateIcon(obj))
                self.model.set_value(rowiter,1,obj.getName())
            processedObjectIds.append(obj.getLocalId())


        if self.selectedObjectId is not None:
            activeiter = self.getIterById(self.model, self.selectedObjectId) 
            self.set_active_iter(activeiter)
        self.model.itersToRemove = []
        self.model.foreach(search, processedObjectIds)
        for rowiter in self.model.itersToRemove:
            self.model.remove(rowiter)

    def getIterById(self, objlist, objectId):
        def search(model, path, rowiter, objectId):
            val = model.get_value(rowiter,2)
            if val == objectId:
                model.tempiter = rowiter
        
        objlist.tempiter = None
        objlist.foreach(search, objectId)
        rowiter=objlist.tempiter
        if rowiter is not None:
            return rowiter
        else:
            return None

    def getSelected(self):
        active_iter = self.get_active_iter()
        objId = self.model.get_value(active_iter,2)
        obj = self.getApplication().getObjectStore().getLocalObjectById(objId)
        return obj

    def setSelected(self, obj):
        if obj.__class__.__name__ != self.objectType:
            raise TypeError()
        activeiter = self.getIterById(self.model, obj.getLocalId()) 
        self.set_active_iter(activeiter)
        self.selectedObjectId = obj.getLocalId()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
