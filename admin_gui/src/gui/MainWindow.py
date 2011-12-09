#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import sys

from LoginWindow import LoginWindow
from Tree import Tree
from Tabs import Tabs

class GetParentException(Exception):pass

class MainWindow(gtk.Window):
    def __init__(self,app):
        gtk.Window.__init__(self)
        
        self.app = app
        
        self.set_title("Scoville Admin PRO")
        self.maximize()
        
        self.table = gtk.Table(5,1,False)
        self.headerbox = gtk.HBox()
        self.header = gtk.image_new_from_file("../data/header.png")
        self.menu = gtk.MenuBar()
        self.tool = gtk.Toolbar()
        self.pane = gtk.HPaned()
        self.tree = Tree(self)
        self.tabs = Tabs(self)
        self.status = gtk.Statusbar()
        
        #testkrempel
        self.label1 = gtk.Label("Test1")
        self.label2 = gtk.Label("Test2")
        self.testmenu = gtk.MenuItem("Server")
        self.testtoolbutton = gtk.ToolButton()
        self.testtoolbutton.set_stock_id(gtk.STOCK_ABOUT)
        self.menu.add(self.testmenu)
        self.tool.add(self.testtoolbutton)
        self.pane.add(self.tree)
        self.pane.add(self.tabs)
        
        #Toolbar:
        self.logoutbutton=gtk.ToolButton()
        self.logoutbutton.set_stock_id(gtk.STOCK_QUIT)
        self.logoutbutton.connect("clicked", self.cb_LogoutButton)
        self.tool.add(self.logoutbutton)
        
        self.headerbox.pack_start(self.header, False)
        self.table.attach(self.headerbox,0,1,0,1,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.menu,0,1,1,2,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.tool,0,1,2,3,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.pane,0,1,3,4,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.EXPAND,0,0)
        self.table.attach(self.status,0,1,4,5,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.add(self.table)
        
        self.loginwindow = LoginWindow(self)
        
        self.show_all()
        
        srv = self.getApplication().createTestserver()
        srv2 = self.getApplication().createTestserver()
        srv3 = self.getApplication().createTestserver()
        srv4 = self.getApplication().createTestserver()
        srv4.setPar(srv3)
        self.tabs.openPage(srv4)
        srv.load = srv.LOADED_PROFILE
        self.tabs.openPage(srv)
        self.tabs.openPage(srv)
        self.tabs.openPage(srv2)
        
    def cb_LogoutButton(self,widget=None,data=None):
        try:
            self.getApplication().logout()
        except Exception, e:
            pass
        else:
            self.loginwindow = LoginWindow(self)
        
    def getApplication(self):
        return self.app
    
    def getPar(self):
        raise GetParentException()