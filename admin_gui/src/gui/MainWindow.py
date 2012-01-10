#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import sys

from ServerPropertyWindow import ServerPropertyWindow
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
        self.treescroll = gtk.ScrolledWindow()
        self.treescroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.tree = Tree(self)
        self.tabs = Tabs(self)
        self.status = gtk.Statusbar()
        self.progress = gtk.ProgressBar()
        self.progress.set_text("No Processes")
        self.progress.set_pulse_step(0.01)
                
        #testkrempel
        self.testmenu = gtk.MenuItem("Server")
        self.testmenu.connect("activate", self.cb_ServerClicked)
        
        
        self.menu.add(self.testmenu)
        self.treescroll.add(self.tree)
        self.treescroll.set_size_request(250,0)
        self.pane.add(self.treescroll)
        self.pane.add(self.tabs)
        
        #Toolbar:
        self.logoutbutton=gtk.ToolButton()
        self.logoutbutton.set_stock_id(gtk.STOCK_QUIT)
        self.logoutbutton.connect("clicked", self.cb_LogoutButton)
        self.addserverbutton=gtk.ToolButton()
        self.addserverbutton.set_stock_id(gtk.STOCK_ADD)
        self.addserverbutton.connect("clicked", self.cb_AddServerButton)
        
        self.tool.add(self.logoutbutton)
        self.tool.add(self.addserverbutton)
        
        self.status.pack_end(gtk.LinkButton("http://www.masterprogs.de/","See masteprogs.de for further information and support"),False)
        self.status.pack_end(self.progress,False)
        
        self.headerbox.pack_start(self.header, False)
        self.table.attach(self.headerbox,0,1,0,1,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.menu,0,1,1,2,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.tool,0,1,2,3,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.pane,0,1,3,4,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.EXPAND,0,0)
        self.table.attach(self.status,0,1,4,5,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.add(self.table)
        
        self.loginwindow = LoginWindow(self)
        
        self.connect("delete_event",self.cb_Close)
        
        self.show_all()
    
    def cb_ServerClicked(self,widget=None,data=None):        
        raise Exception("LOLOLOL")
    
    
    def cb_LogoutButton(self,widget=None,data=None):
        try:
            self.getApplication().logout()
        except Exception, e:
            pass
        else:
            self.loginwindow = LoginWindow(self)
    
    def cb_AddServerButton(self,widget=None,data=None):
        ServerPropertyWindow(self)
    
    def cb_Close(self, widget=None, data=None):
        try:
            self.getApplication().logout()
        except Exception, e:
            pass
        self.getApplication().setQuitRequest(True)
        gtk.main_quit()
        sys.exit(0)
        
    def getTreeStore(self):
        return self.tree.get_model()
    
    def getTabs(self):
        return self.tabs
    
    def getApplication(self):
        return self.app
    
    def getPar(self):
        raise GetParentException()
    
    def pulseProgress(self,count):
        if count == 0:
            self.progress.set_text("No Processes")
            self.progress.set_fraction(0)
        elif count == 1:
            self.progress.set_text("1 Process")
            self.progress.pulse()
        else:
            self.progress.set_text(str(count)+" Processes")
            self.progress.pulse()
