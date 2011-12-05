#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygt.require("2.0")
import gtk

class MainWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("Scoville Admin PRO")
        self.maximize()
        
        self.table = gtk.Table(5,1,False)
        self.headerbox = gtk.HBox()
        self.header = gtk.image_new_from_file("../../data/header.png")
        self.menu = gtk.MenuBar()
        self.tool = gtk.Toolbar()
        self.pane = gtk.HPaned()
        self.status = gtk.Statusbar()
        
        
        self.label1 = gtk.Label("Test1")
        self.label2 = gtk.Label("Test2")
        self.testmenu = gtk.MenuItem("Server")
        self.testtoolbutton = gtk.ToolButton()
        self.testtoolbutton.set_stock_id(gtk.STOCK_ABOUT)
        self.menu.add(self.testmenu)
        self.tool.add(self.testtoolbutton)
        self.pane.add1(self.label1)
        self.pane.add2(self.label2)
        
        
        self.headerbox.pack_start(self.header, False)
        self.table.attach(self.header,0,1,0,1,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.menu,0,1,1,2,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.tool,0,1,2,3,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.pane,0,1,3,4,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.EXPAND,0,0)
        self.table.attach(self.status,0,1,4,5,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        
        self.show_all()
        