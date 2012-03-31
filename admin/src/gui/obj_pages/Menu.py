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
from gui import IconStock
pygtk.require("2.0")
import gtk

from GenericObject import GenericObjectPage
from GenericObject import PageFrame

class MenuPage(GenericObjectPage):
    def __init__(self, par, menu):
        GenericObjectPage.__init__(self,par,menu)
        self.par = par
        self.menu = menu
        
        self.info = PageFrame(self, "Name", IconStock.SITE)
        self.infobox = gtk.HBox()
        self.info_labelName = gtk.Label("Name:")
        self.info_entryName = gtk.Entry()
        self.infobox.pack_start(self.info_labelName,False)
        self.infobox.pack_start(self.info_entryName,True)
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.edit = PageFrame(self, "Edit Items", IconStock.MENU)
        self.editbox = gtk.HPaned()
        self.edit_left_box = gtk.VBox()
        self.edit_toolbar = gtk.Toolbar()
        
        self.addbutton=gtk.ToolButton()
        self.addbutton.set_stock_id(gtk.STOCK_ADD)
        self.addbutton.connect("clicked", self.cb_Add)
        self.removebutton=gtk.ToolButton()
        self.removebutton.set_stock_id(gtk.STOCK_REMOVE)
        self.removebutton.connect("clicked", self.cb_Remove)
        self.increasebutton=gtk.ToolButton()
        self.increasebutton.set_stock_id(gtk.STOCK_GO_UP)
        self.increasebutton.connect("clicked", self.cb_Increase)
        self.decreasebutton=gtk.ToolButton()
        self.decreasebutton.set_stock_id(gtk.STOCK_GO_DOWN)
        self.decreasebutton.connect("clicked", self.cb_Decrease)
        self.topbutton=gtk.ToolButton()
        self.topbutton.set_stock_id(gtk.STOCK_GOTO_TOP)
        self.topbutton.connect("clicked", self.cb_Top)
        self.bottombutton=gtk.ToolButton()
        self.bottombutton.set_stock_id(gtk.STOCK_GOTO_BOTTOM)
        self.bottombutton.connect("clicked", self.cb_Bottom)
        self.edit_toolbar.add(self.addbutton)
        self.edit_toolbar.add(self.removebutton)
        self.edit_toolbar.add(self.increasebutton)
        self.edit_toolbar.add(self.decreasebutton)
        self.edit_toolbar.add(self.topbutton)
        self.edit_toolbar.add(self.bottombutton)
        
        self.edit_menutree = MenuItemTree(self,menu)
        self.edit_right_box = gtk.Frame("ACTIONS")
        self.edit_left_box.pack_start(self.edit_toolbar,False)
        self.edit_left_box.pack_start(self.edit_menutree,True)
        self.editbox.add(self.edit_left_box)
        self.editbox.add(self.edit_right_box)
        self.edit.add(self.editbox)
        self.pack_start(self.edit)
        
        self.menu.addCallback(self.render)
        self.show_all()
        
    
    def render(self):
        self.info_labelName.set_text(self.menu.getName())
    
    def cb_Add(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().createMenuItem()
    
    def cb_Remove(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().delete()
    
    def cb_Increase(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().increaseOrder()
        
    def cb_Decrease(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().decreaseOrder()
    
    def cb_Top(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().moveToTop()
        
    def cb_Bottom(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().moveToBottom()
    
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
class ActionWidget(gtk.Expander):
    def __init__(self, par, menu):
        gtk.Expander.__init__(self)
        self.par = par

class ActionWidgetLabel(gtk.HBox):
    pass

class ActionWidgetConfig(gtk.VBox):
    pass

class MenuItemTree(gtk.TreeView):
    def __init__(self, par, menu=None):
        gtk.TreeView.__init__(self)
        self.par = par
        self.menu = menu
        
        self.store = MenuItemStore(gtk.gdk.Pixbuf,str,int,int,parent=self.par, objectStore = self.getApplication().getObjectStore(),menu=menu)
        
        self.set_model(self.store)
        self.col_name = gtk.TreeViewColumn("MenuItem")
        self.append_column(self.col_name)
        self.renderer_icon = gtk.CellRendererPixbuf()
        self.renderer_name = gtk.CellRendererText()
        self.renderer_name.set_property('editable',True)
        self.col_name.pack_start(self.renderer_icon,False)
        self.col_name.pack_start(self.renderer_name,True)
        self.col_name.add_attribute(self.renderer_icon,'pixbuf',0)
        self.col_name.add_attribute(self.renderer_name,'text',1)
        self.renderer_name.connect('edited', self.renamedCallback)

        
        self.set_search_column(1)
        
    def getSelectedMenuItem(self):
        selection = self.get_selection()
        rowiter = selection.get_selected()[1]
        obj_id = self.store.get_value(rowiter,2)
        obj = self.getApplication().getLocalObjectById(obj_id)
        return obj
    
    def renamedCallback(self, cell, path, name):
        obj_id = self.store[path][2]
        obj = self.getApplication().getLocalObjectById(obj_id)
        if obj.__class__.__name__ == 'MenuItem':
            obj.rename(name)    
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
class MenuItemStore(gtk.TreeStore):
    WHITELISTED_CLASSES = ("Menu","MenuItem")
    def __init__(self,*args,**kwargs):
        assert kwargs['objectStore'] is not None, "need objectStore!"
        gtk.TreeStore.__init__(self,*args)
        self.par = kwargs['parent']
        self.objectStore = kwargs['objectStore']
        self.menu = kwargs['menu']
        
        self.menu.addCallback(self.render)
        self.busy = False # Prevent threadcollisions 
        self.root = self.append(None,(IconStock.MENU,self.menu.getName(),self.menu.getLocalId(),0))
        self.render()

    def getIterById(self, obj_id):
        def search(model, path, rowiter, obj_id):
                val = model.get_value(rowiter,2)
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
            pass
            #raise StoreException("store is busy")
    
    def addObject(self,obj,addToRootIfNoParent=True):
        if obj.__class__.__name__ not in self.WHITELISTED_CLASSES:
            return True
        try:
            parent = obj.getPar()
            if parent.__class__.__name__ == "MenuItem" or parent.__class__.__name__ == "Menu":
                parentIter = self.getIterById(parent.getLocalId())
                self.append(parentIter,(IconStock.MENUITEM, obj.getName(), obj.getLocalId(),obj.getOrder()))
                return True
            else:
                raise Exception()
        except:
            if addToRootIfNoParent : 
                root = self.getIterById(-2)
                self.append(root,(IconStock.MENUITEM, obj.getName(), obj.getLocalId(),obj.getOrder()))
                return True
            return False
    

    def render(self):
        def search(model, path, rowiter):
            obj_id = model.get_value(rowiter,2)
            if obj_id >= 0:
                try:
                    obj = self.objectStore.getLocalObjectById(obj_id)
                #except data.Generic.GenericObjectStoreException,e:
                except Exception:
                    self.itersToRemove.append(rowiter)
                else:
                    if obj.__class__.__name__=="MenuItem":
                        model.set_value(rowiter,0,IconStock.MENUITEM)
                        model.set_value(rowiter,1,obj.getName())
                        model.set_value(rowiter,3,obj.getOrder())
                        self.objectsToAllocate.remove(obj)
                    else:
                        model.set_value(rowiter,0,IconStock.MENU)
                        model.set_value(rowiter,1,obj.getName())
                        self.objectsToAllocate.remove(obj)
                
        objectsAllocated = 1
        self.objectsToAllocate = self.menu.getMenuItemsRecursive()
        self.objectsToAllocate.append(self.menu)
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
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
        
        
    