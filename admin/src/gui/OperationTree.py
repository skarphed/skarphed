#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import pygtk
pygtk.require("2.0")
import gtk

from OperationStore import OperationStore
from TreeContextMenu import TreeContextMenu

from glue.lng import _

class OperationTree(gtk.TreeView):
    def __init__(self, parent, server=None):
        '''Constructor --'''
        gtk.TreeView.__init__(self)
        self.par = parent
        
        #self.context = MatchTreeContextMenu(self.app,self)
        
        if server is not None:
            self.serverId = server.getLocalId()
            self.store = OperationStore(gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, str,str ,int, parent=self.par, server=server, objectStore=self.getApplication().getObjectStore()) #Icon, Name, ID, type
        else:
            self.serverId = None
            self.store = OperationStore(gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, str,str ,int, parent=self.par, objectStore=self.getApplication().getObjectStore()) #Icon, Name, ID, type
        self.context = TreeContextMenu(self)
        self.set_model(self.store)
        
        
        self.col_active = gtk.TreeViewColumn('')
        self.col_name = gtk.TreeViewColumn(_("Operation"))
        self.col_invoked = gtk.TreeViewColumn(_("Invoked"))
        self.append_column(self.col_active)
        self.append_column(self.col_name)
        self.append_column(self.col_invoked)
        self.renderer_active = gtk.CellRendererPixbuf()
        self.renderer_name = gtk.CellRendererText()
        self.renderer_icon = gtk.CellRendererPixbuf()
        self.renderer_invoked = gtk.CellRendererText()
        
        self.col_active.pack_start(self.renderer_active,False)
        self.col_name.pack_start(self.renderer_icon,False)
        self.col_name.pack_start(self.renderer_name,True)
        self.col_invoked.pack_start(self.renderer_invoked,True)
        self.col_active.add_attribute(self.renderer_active,'pixbuf',0)
        self.col_name.add_attribute(self.renderer_icon,'pixbuf',1)
        self.col_name.add_attribute(self.renderer_name,'text',2)
        self.col_invoked.add_attribute(self.renderer_invoked,'text',3)
        #self.col_name.set_cell_data_func(self.renderer_id,self.renderId)
        
        self.col_name.set_sort_column_id(1)
        self.col_invoked.set_resizable(True)
        self.col_name.set_resizable(True)
        self.set_search_column(1)
        self.set_rules_hint(True)
        
        
        #self.connect("row-activated",self.cb_RowActivated)
        #self.connect("row-expanded",self.cb_RowExpanded)
        self.connect("button_press_event",self.cb_ButtonPressed)
  
    def cb_ButtonPressed(self, widget = None, event = None, data = None):
        if event.button==3:
            x = int(event.x)
            y = int(event.y)
            pathinfo = self.get_path_at_pos(x,y)
            if pathinfo is not None:
                try:
                    self.grab_focus()
                    self.set_cursor(pathinfo[0],pathinfo[1],0) 
                    selection = self.get_selection()
                    rowiter = selection.get_selected()[1]
                    objid = self.store.get_value(rowiter,4)
                    obj = self.store.objectStore.getLocalObjectById(objid)
                    self.context.popup(obj,event.button,event.get_time())
                except:
                    pass
        
    def getCurrentOperation(self):
        selection = self.get_selection()
        rowiter = selection.get_selected()[1]
        if rowiter is None:
            return None
        opId = self.store.get_value(rowiter,4)
        if opId >= 0:
            obj = self.getApplication().getLocalObjectById(opId)
            return obj
        else:
            return None
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()