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

from data.Generic import GenericObjectStoreException

from IconStock import CSS

class CssEditor(gtk.Window):
    def __init__(self, par, obj):
        gtk.Window.__init__(self)
        self.par = par
        self.objId = obj.getLocalId()
        
        self.set_title("Scoville Admin PRO :: CssEditor :: "+obj.getName())
        self.set_icon(CSS)
        self.set_size_request(600,500)
        
        self.set_border_width(10)
        self.cssframe = PageFrame(self,"Css-Properties",CSS)
        self.label = gtk.Label("Edit CSS Settings for "+obj.getName())
        self.store = CssStore(str, str, str, bool, bool, parent=self)
        self.listview = CssView(self)
        self.listview.set_model(self.store)
        self.listviewscroll = gtk.ScrolledWindow()
        self.listviewscroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.vbox = gtk.VBox()
        self.framevbox = gtk.VBox()
        
        self.toolbar = gtk.Toolbar()
        self.tool_add=gtk.ToolButton()
        self.tool_add.set_stock_id(gtk.STOCK_ADD)
        self.tool_add.connect("clicked",self.addCallback)
        self.toolbar.add(self.tool_add)
        self.tool_save = gtk.ToolButton()
        self.tool_save.set_stock_id(gtk.STOCK_SAVE)
        self.tool_save.connect("clicked",self.saveCallback)
        self.toolbar.add(self.tool_save)
        self.vbox.pack_start(self.toolbar,False)
        self.tool_refresh = gtk.ToolButton()
        self.tool_refresh.set_stock_id(gtk.STOCK_REFRESH)
        self.tool_refresh.connect("clicked",self.refreshCallback)
        self.toolbar.add(self.tool_refresh)
        
        self.listviewscroll.add(self.listview)
        self.framevbox.pack_start(self.label,False)
        self.framevbox.pack_start(self.listviewscroll,True)
        self.cssframe.add(self.framevbox)
        
        self.vbox.pack_start(self.cssframe,True)
        self.add(self.vbox)
        
        self.connect("delete-event",self.closeCallback)
        
        self.show_all()
        
        obj.addCallback(self.render)
        obj.loadCssPropertySet()
    
    def closeCallback(self,widget=None,data=None):
        try:
            obj = self.getApplication().getLocalObjectById(self.objId)
        except GenericObjectStoreException:
            self.destroy()
            return
        self.getPar().closeCssEditor(obj)
    
    def saveCallback(self,widget=None,data=None):
        def loop(model,path,rowiter):
            if model.get_value(rowiter,4) == 0:
                selector = model.get_value(rowiter,0)
                prop = model.get_value(rowiter,1)
                value = model.get_value(rowiter,2)
                inherited = model.get_value(rowiter,3)
                model.newPropertySet[selector+"?"+prop] = {'v':value,'i':inherited}
        self.store.newPropertySet = {}
        self.store.foreach(loop)
        obj = self.getApplication().getLocalObjectById(self.objId)
        obj.setCssPropertySet(self.store.newPropertySet)
        obj.saveCssPropertySet()
    
    def addCallback(self,widget=None,data=None):
        self.store.append(('','','',False,False))
    
    def refreshCallback(self,widget=None,data=None):
        obj = self.getApplication().getLocalObjectById(self.objId)
        obj.loadCssPropertySet()
        
    def render(self):
        try:
            obj = self.getApplication().getLocalObjectById(self.objId)
        except GenericObjectStoreException:
            self.destroy()
            return
        propertySet = obj.getCssPropertySet()
        self.store.clear()
        self.listview.model_selector.clear()
        self.listview.model_property.clear()
        self.listview.model_value.clear()
        print propertySet
        print type(propertySet)
        
        addedToSelectorList = {}
        addedToPropertyList = {}
        addedToValueList = {}
        
        for identifier,value in propertySet['properties'].items():
            selector, property = identifier.split("?")
            self.store.append((selector,property,value['v'],value['i'],False))
            if not addedToSelectorList.has_key(selector):
                self.listview.model_selector.append((selector,))
                addedToSelectorList[selector]=1
            if not addedToPropertyList.has_key(property):
                self.listview.model_property.append((property,))
                addedToPropertyList[property]=1
            if not addedToValueList.has_key(value['v']):
                self.listview.model_value.append((value['v'],))
                addedToValueList[value['v']]=1
        
        
    
    def getObject(self):
        return self.getApplication().getLocalObjectById(self.objId)
    
    def getPar(self):
        return self.par
    
    def getApplication(self):
        return self.par.getApplication()

class CssView(gtk.TreeView):
    def __init__(self, par):
        gtk.TreeView.__init__(self)
        self.par = par
        
        self.col_selector = gtk.TreeViewColumn('selector')
        self.col_property = gtk.TreeViewColumn('property')
        self.col_value = gtk.TreeViewColumn('value')
        self.col_inherited = gtk.TreeViewColumn('inherited')
        self.col_delete = gtk.TreeViewColumn('delete')
        
        self.append_column(self.col_selector)
        self.append_column(self.col_property)
        self.append_column(self.col_value)
        self.append_column(self.col_inherited)
        self.append_column(self.col_delete)
        
        
        self.model_selector = gtk.ListStore(str)
        self.model_property = gtk.ListStore(str)
        self.model_value = gtk.ListStore(str)
        
        self.renderer_selector = gtk.CellRendererCombo()
        self.renderer_property = gtk.CellRendererCombo()
        self.renderer_value = gtk.CellRendererCombo()
        self.renderer_inherited = gtk.CellRendererToggle()
        self.renderer_delete = gtk.CellRendererToggle()
        
        self.col_selector.pack_start(self.renderer_selector,False)
        self.col_property.pack_start(self.renderer_property,False)
        self.col_value.pack_start(self.renderer_value,True)
        self.col_inherited.pack_start(self.renderer_inherited,False)
        self.col_delete.pack_start(self.renderer_delete,False)
        
        self.renderer_selector.set_property('model',self.model_selector)
        self.renderer_property.set_property('model',self.model_property)
        self.renderer_value.set_property('model',self.model_value)
        self.renderer_selector.set_property('text-column',0)
        self.renderer_property.set_property('text-column',0)
        self.renderer_value.set_property('text-column',0)
        self.renderer_selector.set_property('editable',True)
        self.renderer_property.set_property('editable',True)
        self.renderer_value.set_property('editable',True)
        
        self.col_selector.add_attribute(self.renderer_selector,'text',0)
        self.col_property.add_attribute(self.renderer_property,'text',1)
        self.col_value.add_attribute(self.renderer_value,'text',2)
        self.col_inherited.add_attribute(self.renderer_inherited,'active',3)
        self.col_delete.add_attribute(self.renderer_delete,'active',4)
        
        self.renderer_delete.set_activatable(True)
        
        self.col_selector.set_resizable(True)
        self.col_property.set_resizable(True)
        self.col_value.set_resizable(True)
        self.col_inherited.set_resizable(True)
        self.col_delete.set_resizable(True)
        
        self.renderer_selector.connect("changed", self.changedSelectorCallback)
        self.renderer_property.connect("changed", self.changedPropertyCallback)
        self.renderer_value.connect("changed", self.changedValueCallback)
        self.renderer_selector.connect("edited", self.editedSelectorCallback)
        self.renderer_property.connect("edited", self.editedPropertyCallback)
        self.renderer_value.connect("edited", self.editedValueCallback)
        self.renderer_delete.connect("toggled",self.toggledDeleteCallback)
        
        self.col_selector.set_sort_column_id(1)
        self.set_search_column(1)
        self.set_rules_hint(True)
        self.show_all()
        
    def toggledDeleteCallback(self,render=None,path=None):
        rowiter = self.get_model().get_iter(path)
        val = 1-self.get_model().get_value(rowiter,4)
        self.get_model().set_value(rowiter,4,val)
        
    def editedSelectorCallback(self, renderer, path, value):
        liststore = self.get_model()
        rowiter = liststore.get_iter(path)
        liststore.set_value(rowiter,0,value)
        
    def changedSelectorCallback(self, combo, path, comboiter):
        combomodel = combo.get_property('model')
        liststore = self.get_model()
        rowiter = liststore.get_iter(path)
        liststore.set_value(rowiter,0,combomodel.get_value(comboiter,0))
    
    def editedPropertyCallback(self, renderer, path, value):
        liststore = self.get_model()
        rowiter = liststore.get_iter(path)
        liststore.set_value(rowiter,1,value)
    
    def changedPropertyCallback(self, combo, path, comboiter):
        combomodel = combo.get_property('model')
        liststore = self.get_model()
        rowiter = liststore.get_iter(path)
        liststore.set_value(rowiter,1,combomodel.get_value(comboiter,0))
    
    def editedValueCallback(self, renderer, path, value):
        liststore = self.get_model()
        rowiter = liststore.get_iter(path)
        liststore.set_value(rowiter,2,value)
        
    def changedValueCallback(self, combo, path, comboiter):
        combomodel = combo.get_property('model')
        liststore = self.get_model()
        rowiter = liststore.get_iter(path)
        liststore.set_value(rowiter,2,combomodel.get_value(comboiter,0))

class CssStore(gtk.ListStore):
    def __init__(self,*args,**kwargs):
        gtk.ListStore.__init__(self,*args)
        self.par = kwargs['parent']
        
    def getPar(self):
        return self.par
    
    def getApplication(self):
        return self.par.getApplication()    


class FrameLabel(gtk.HBox):
    def __init__(self,parent, text, icon=None):
        self.par = parent
        gtk.HBox.__init__(self)
        assert type(text) == str, "text must be string"
        
        self.icon = gtk.Image()
        if icon is not None:
            self.icon.set_from_pixbuf(icon)
        self.label = gtk.Label()
        self.label.set_text(text)
        
        self.pack_start(self.icon,False)
        self.pack_start(self.label,True)
        self.show_all()
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class PageFrame(gtk.Frame):
    def __init__(self,parent, text, icon=None):
        gtk.Frame.__init__(self)
        self.set_border_width(10)
        self.set_label_widget(FrameLabel(self,text,icon))
        
        
