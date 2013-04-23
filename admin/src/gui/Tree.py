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

from Store import Store
from TreeContextMenu import TreeContextMenu

class Tree(gtk.TreeView):
    def __init__(self, parent):
        '''Constructor --'''
        gtk.TreeView.__init__(self)
        self.par = parent
        
        #self.context = MatchTreeContextMenu(self.app,self)
        
        self.store = Store(gtk.gdk.Pixbuf, str,int ,parent=self.par, objectStore=self.getApplication().getObjectStore()) #Icon, Name, ID, type
        self.context = TreeContextMenu(self)
        self.set_model(self.store)
        
        self.col_id = gtk.TreeViewColumn('Environment')
        #self.col_name = gtk.TreeViewColumn("ObjectId")
        self.append_column(self.col_id)
        #self.append_column(self.col_name)
        self.renderer_name = gtk.CellRendererText()
        self.renderer_icon = gtk.CellRendererPixbuf()
        #self.renderer_id = gtk.CellRendererText()
        
        self.col_id.pack_start(self.renderer_icon,False)
        self.col_id.pack_start(self.renderer_name,True)
        #self.col_name.pack_start(self.renderer_id,True)
        self.col_id.add_attribute(self.renderer_icon,'pixbuf',0)
        self.col_id.add_attribute(self.renderer_name,'text',1)
        #self.col_name.add_attribute(self.renderer_id,'text',2)
        #self.col_name.set_cell_data_func(self.renderer_id,self.renderId)
        
        #self.col_name.set_sort_column_id(1)
        self.col_id.set_resizable(True)
        #self.col_name.set_resizable(True)
        self.set_search_column(1)
        self.set_rules_hint(True)
        
        self.connect("row-activated",self.cb_RowActivated)
        #self.connect("row-expanded",self.cb_RowExpanded)
        self.connect("button_press_event",self.cb_ButtonPressed)
        self.connect("cursor-changed",self.cb_CursorChanged)
  
    def cb_CursorChanged(self,data):
        selection = self.get_selection()
        rowiter = selection.get_selected()[1]
        nr = self.store.get_value(rowiter,2)
        obj = self.store.objectStore.getLocalObjectById(nr)
        self.getPar().getToolbar().renderContextButtons(obj)
        self.getPar().getTabs().openPage(obj,False)
            

    def cb_ButtonPressed(self, widget = None, event = None, data = None):
        if event.button==3:
            x = int(event.x)
            y = int(event.y)
            pathinfo = self.get_path_at_pos(x,y)
            if pathinfo is not None:
                self.grab_focus()
                self.set_cursor(pathinfo[0],pathinfo[1],0) 
                selection = self.get_selection()
                rowiter = selection.get_selected()[1]
                nr = self.store.get_value(rowiter,2)
                obj = self.store.objectStore.getLocalObjectById(nr)
                self.context.popup(obj,event.button,event.get_time())
                self.getPar().getToolbar().renderContextButtons(obj)
            
    
    def cb_RowActivated(self,treeview,iter,path,wdata=None): 
        '''This callbackmethod defines behaviour after doubleclicking a row. It is calling open match
           if the currently selected treeelement is representing a match'''
        selection = self.get_selection()
        iter = selection.get_selected()[1]
        id = self.store.get_value(iter,2)
        if id >= 0:
            object = self.getApplication().getLocalObjectById(id)
            self.getPar().getTabs().openPage(object)

    def setActiveObject(self, obj):
        rowiter = self.store.getIterById(obj.getLocalId())
        path = self.store.get_path(rowiter)
        self.set_cursor(path)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
