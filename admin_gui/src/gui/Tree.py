#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from Store import Store

class Tree(gtk.TreeView):
    def __init__(self, parent):
        '''Constructor --'''
        gtk.TreeView.__init__(self)
        self.par = parent
        
        #self.context = MatchTreeContextMenu(self.app,self)
        
        self.store = Store(gtk.gdk.Pixbuf, str,int ,parent=self.par, objectStore=self.getApplication().getObjectStore()) #Icon, Name, ID, type
        self.set_model(self.store)
        
        self.col_id = gtk.TreeViewColumn('')
        self.col_name = gtk.TreeViewColumn("ObjectId")
        self.append_column(self.col_id)
        self.append_column(self.col_name)
        self.renderer_name = gtk.CellRendererText()
        self.renderer_icon = gtk.CellRendererPixbuf()
        self.renderer_id = gtk.CellRendererText()
        
        self.col_id.pack_start(self.renderer_icon,False)
        self.col_id.pack_start(self.renderer_name,True)
        self.col_name.pack_start(self.renderer_id,True)
        self.col_id.add_attribute(self.renderer_icon,'pixbuf',0)
        self.col_id.add_attribute(self.renderer_name,'text',1)
        self.col_name.add_attribute(self.renderer_id,'text',2)
        #self.col_name.set_cell_data_func(self.renderer_id,self.renderId)
        
        self.col_name.set_sort_column_id(1)
        self.col_id.set_resizable(True)
        self.col_name.set_resizable(True)
        self.set_search_column(1)
        self.set_rules_hint(True)
        
        self.connect("row-activated",self.cb_RowActivated)
        #self.connect("row-expanded",self.cb_RowExpanded)
        #self.connect("button_press_event",self.cb_ButtonPressed)
        
    
    def cb_RowActivated(self,treeview,iter,path,wdata=None): 
        '''This callbackmethod defines behaviour after doubleclicking a row. It is calling open match
           if the currently selected treeelement is representing a match'''
        selection = self.get_selection()
        iter = selection.get_selected()[1]
        id = self.store.get_value(iter,2)
        if id >= 0:
            object = self.getApplication().getLocalObjectById(id)
            self.getPar().getTabs().openPage(object)
        
        
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()