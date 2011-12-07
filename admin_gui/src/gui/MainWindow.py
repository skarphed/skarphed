#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import sys

from LoginWindow import LoginWindow

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
        self.status = gtk.Statusbar()
        
        #testkrempel
        self.label1 = gtk.Label("Test1")
        self.label2 = gtk.Label("Test2")
        self.testmenu = gtk.MenuItem("Server")
        self.testtoolbutton = gtk.ToolButton()
        self.testtoolbutton.set_stock_id(gtk.STOCK_ABOUT)
        self.menu.add(self.testmenu)
        self.tool.add(self.testtoolbutton)
        self.pane.add1(self.label1)
        self.pane.add2(self.label2)
        
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