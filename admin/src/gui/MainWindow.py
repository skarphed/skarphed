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
import sys

from ServerPropertyPage import ServerPropertyPage
from LoginPage import LoginPage
from KeyWindow import KeyWindow
from Toolbar import Toolbar
from Tree import Tree
from Tabs import Tabs
from CssEditor import CssEditor
from DefaultEntry import DefaultEntry

from glue.lng import _

class GetParentException(Exception):pass

class MainWindow(gtk.Window):
    WEBSITE = "http://www.temporary.invalid"
    def __init__(self,app):
        gtk.Window.__init__(self)
        
        self.app = app
        self.openCssEditors = {}
        
        self._dialogObjectStack = []

        self.set_title(_("Scoville Admin PRO"))
        self.set_icon_from_file("../data/icon/mp_logo.png")
        self.maximize()
        
        self.table = gtk.Table(4,1,False)
        self.menu = gtk.MenuBar()
        self.tool = Toolbar(self)
        self.pane = gtk.HPaned()
        self.treescroll = gtk.ScrolledWindow()
        self.treescroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.tree = Tree(self)
        self.treeBox = gtk.VBox()
        self.treeFilter = DefaultEntry(default_message="Filter")
        self.tabs = Tabs(self)
        self.status = gtk.Statusbar()
        self.progress = gtk.ProgressBar()
        self.progress.set_text(_("No Processes"))
        self.progress.set_pulse_step(0.01)
                
        #testkrempel
        self.testmenu = gtk.MenuItem(_("Server"))
        self.testmenu.connect("activate", self.cb_ServerClicked)
        
        
        #menue
        self.menu_help_ = gtk.Menu()
        self.menu_help = gtk.MenuItem(_("Help"))
        self.menu_help.set_submenu(self.menu_help_)
        self.menu_help_about = gtk.MenuItem(_("About..."))
        self.menu_help_about.connect("activate", self.cb_AboutClicked)
        self.menu_help_.add(self.menu_help_about)
        
        
        self.menu.add(self.testmenu)
        self.menu.add(self.menu_help)
        self.treescroll.add(self.tree)
        self.treescroll.set_size_request(250,0)
        self.treeBox.pack_start(self.treeFilter,False)
        self.treeBox.pack_start(self.treescroll,True)
        self.pane.add(self.treeBox)
        self.pane.add(self.tabs)
        
        self.status.pack_end(gtk.LinkButton(MainWindow.WEBSITE,_("See website for further information and support")),False)
        self.status.pack_end(self.progress,False)
        
        self.table.attach(self.menu,0,1,1,2,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.tool,0,1,2,3,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.table.attach(self.pane,0,1,3,4,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.EXPAND,0,0)
        self.table.attach(self.status,0,1,4,5,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.SHRINK,0,0)
        self.add(self.table)
        
        self.treeFilter.connect("changed", self.cb_changedFilter)
        self.connect("delete_event",self.cb_Close)
        self.show_all()

        LoginPage(self)
    
    def openDialogPane(self, dialog):
        self._dialogObjectStack.append(dialog)
        self.pane.remove(self.pane.get_child2()) 
        self.pane.add2(dialog)
        self.tree.set_sensitive(False)
        self.tool.set_sensitive(False)
        self.menu.set_sensitive(False)
        self.show_all()

    def closeDialogPane(self): # TODO implement close all feature
        if self._dialogObjectStack:
            dialog = self._dialogObjectStack.pop()
            self.pane.remove(dialog)
            dialog.destroy()
            if self._dialogObjectStack:
                self.pane.add2(self._dialogObjectStack[-1])
            else:
                self.pane.add2(self.tabs)
                self.tree.set_sensitive(True)
                self.tool.set_sensitive(True)
                self.menu.set_sensitive(True)
            self.show_all()

    def cb_changedFilter(self, widget=None, data=None):
        self.tree.render()

    def getFilterText(self):
        return self.treeFilter.get_text()

    def cb_ServerClicked(self,widget=None,data=None):        
        raise Exception("LOLOLOL")
    
    def cb_AboutClicked(self,widget=None,data=None):
        about = gtk.AboutDialog()
        about.set_program_name(_("Scoville Admin PRO"))
        about.set_version(_("0.1"))
        about.set_copyright(_("© Masterprogs"))
        about.set_comments(_("Scoville Admin PRO is a professional tool to manage your Scoville installations"))
        about.set_website(MainWindow.WEBSITE)
        about.set_logo(gtk.gdk.pixbuf_new_from_file(sys.path[0]+"/../data/login.png"))
        about.set_border_width(0)
        about.run()
        about.destroy()
    
    
    def cb_LogoutButton(self,widget=None,data=None):
        #try:
        self.getApplication().logout()
        #except Exception, e:
            #raise e
        #else:
        LoginPage(self)
    
    def cb_AddServerButton(self,widget=None,data=None):
        ServerPropertyPage(self)
    
    def cb_pkiButton(self,widget=None,data=None):
        KeyWindow(self, self.getApplication().activeProfile)
    
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
    
    def openCssEditor(self,obj):
        id = obj.getLocalId()
        if self.openCssEditors.has_key(id):
            self.openCssEditors[id].grab_focus()
        else:
            self.openCssEditors[id] = CssEditor(self,obj)
        
    def closeCssEditor(self,obj):
        id = obj.getLocalId()
        if self.openCssEditors.has_key(id):
            del(self.openCssEditors[id])

    def getToolbar(self):
        return self.tool

    def getTree(self):
        return self.tree
    
    def getApplication(self):
        return self.app
    
    def getPar(self):
        raise GetParentException()
    
    def pulseProgress(self,tracker):
        count = tracker.getThreadcount()
        if count == 0:
            self.progress.set_text(_("No Processes"))
            self.progress.set_fraction(0)
        elif count == 1:
            self.progress.set_text(_("1 Process"))
            self.progress.pulse()
        else:
            self.progress.set_text(str(count)+_(" Processes"))
            self.progress.pulse()
