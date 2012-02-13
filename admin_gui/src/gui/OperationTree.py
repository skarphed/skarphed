#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from OperationStore import OperationStore
from TreeContextMenu import TreeContextMenu

class OperationTree(gtk.TreeView):
    def __init__(self, parent, server=None):
        '''Constructor --'''
        gtk.TreeView.__init__(self)
        self.par = parent
        
        #self.context = MatchTreeContextMenu(self.app,self)
        
        if server is not None:
            self.server = server
            self.store = OperationStore(gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, str,str ,int, parent=self.par, server=server, objectStore=self.getApplication().getObjectStore()) #Icon, Name, ID, type
        else:
            self.server = None
            self.store = OperationStore(gtk.gdk.Pixbuf, gtk.gdk.Pixbuf, str,str ,int, parent=self.par, objectStore=self.getApplication().getObjectStore()) #Icon, Name, ID, type
        self.context = TreeContextMenu(self)
        self.set_model(self.store)
        
        
        self.col_active = gtk.TreeViewColumn('')
        self.col_name = gtk.TreeViewColumn("Operation")
        self.col_invoked = gtk.TreeViewColumn("Invoked")
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
        
        
        self.connect("row-activated",self.cb_RowActivated)
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
                    iter = selection.get_selected()[1]
                    id = self.store.get_value(iter,4)
                    obj = self.store.objectStore.getLocalObjectById(id)
                    self.context.popup(obj,event.button,event.get_time())
                except:
                    pass
    
    def cb_RowActivated(self,treeview,iter,path,wdata=None): 
        '''This callbackmethod defines behaviour after doubleclicking a row. It is calling open match
           if the currently selected treeelement is representing a match'''
        selection = self.get_selection()
        iter = selection.get_selected()[1]
        id = self.store.get_value(iter,4)
        if id >= 0:
            object = self.getApplication().getLocalObjectById(id)
            self.getPar().getTabs().openPage(object)
        
        
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()