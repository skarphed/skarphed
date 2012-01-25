#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from GenericObject import GenericObjectPage
from GenericObject import PageFrame
from GenericObject import FrameLabel

import gui.IconStock

class RepositoryPage(GenericObjectPage):
    def __init__(self,parent,obj):
        GenericObjectPage.__init__(self,parent,object)
        self.repo = obj
        
        self.headline = gtk.Label()
        self.pack_start(self.headline,False)
        
        self.info = PageFrame(self,"Information", gui.IconStock.REPO)
        self.infobox = gtk.VBox()
        self.info_table = gtk.Table(2,2,False)
        self.info_labelName = gtk.Label("name:")
        self.info_labelHost = gtk.Label("host:")
        self.info_displayName = gtk.Label()
        self.info_displayHost = gtk.Label()
        self.info_table.attach(self.info_labelName,0,1,0,1)
        self.info_table.attach(self.info_displayName,1,2,0,1)
        self.info_table.attach(self.info_labelHost,0,1,1,2)
        self.info_table.attach(self.info_displayHost,1,2,1,2)
        self.infobox.pack_start(self.info_table,False)
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.mod = PageFrame(self,"available and installed modules", gui.IconStock.MODULE)
        self.modbox = gtk.Table(5,2,False)
        self.modbox.set_row_spacings(10)
        self.modbox.set_col_spacings(10)
        self.modbox.set_border_width(10)
        
        self.mod_label = gtk.Label("please drag a module into the opposing list to install/uninstall it:\n")
        self.mod_labelInstalled = gtk.Label("installed modules")
        self.mod_labelAvailable = gtk.Label("available modules")
        self.mod_labelProcessed = gtk.Label("currently processed modules")
        
        self.mod_IList = gtk.TreeView()
        self.mod_IListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        self.mod_IList.set_model(self.mod_IListStore)
        self.mod_IList_col_module = gtk.TreeViewColumn('module name')
        self.mod_IList_ren_icon = gtk.CellRendererPixbuf()
        self.mod_IList_ren_name = gtk.CellRendererText()
        self.mod_IList.append_column(self.mod_IList_col_module)
        self.mod_IList_col_module.pack_start(self.mod_IList_ren_icon)
        self.mod_IList_col_module.pack_start(self.mod_IList_ren_name)
        self.mod_IList_col_module.add_attribute(self.mod_IList_ren_icon,'pixbuf',0)
        self.mod_IList_col_module.add_attribute(self.mod_IList_ren_name,'text',1)
        
        self.mod_AList = gtk.TreeView()
        self.mod_AListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        self.mod_AList.set_model(self.mod_AListStore)
        self.mod_AList_col_module = gtk.TreeViewColumn('module name')
        self.mod_AList_ren_icon = gtk.CellRendererPixbuf()
        self.mod_AList_ren_name = gtk.CellRendererText()
        self.mod_AList.append_column(self.mod_AList_col_module)
        self.mod_AList_col_module.pack_start(self.mod_AList_ren_icon)
        self.mod_AList_col_module.pack_start(self.mod_AList_ren_name)
        self.mod_AList_col_module.add_attribute(self.mod_AList_ren_icon,'pixbuf',0)
        self.mod_AList_col_module.add_attribute(self.mod_AList_ren_name,'text',1)
        
        
        self.modbox.attach(self.mod_label,0,2,0,1)
        self.modbox.attach(self.mod_labelInstalled,0,1,1,2)
        self.modbox.attach(self.mod_labelAvailable,1,2,1,2)
        self.modbox.attach(self.mod_IList,0,1,2,3)
        self.modbox.attach(self.mod_AList,1,2,2,3)
        self.modbox.attach(self.mod_labelProcessed,0,2,3,4)
        self.modbox.attach(gtk.Label("KOMMT HIER HIN OPERATIONVIEW. ALTER!"),0,2,4,5)
        
        
        self.mod.add(self.modbox)
        self.pack_start(self.mod,False)
        
        self.show_all()
        
        self.render()
        obj.addCallback(self.render)
        
    def render(self):
        self.headline.set_markup("<b>Repository: "+self.repo.getName()+"</b>")
        
        
    
    