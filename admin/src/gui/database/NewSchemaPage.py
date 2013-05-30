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

from threading import Thread
from time import sleep

from data.Generic import GenericObjectStoreException

from gui.DefaultEntry import DefaultEntry

from lng import _

class NewSchemaPage(gtk.Frame):
    class Pulse(Thread):
        def __init__(self, window):
            Thread.__init__(self)
            self.window = window

        def run(self):
            while True:
                if self.window.working:
                    self.window.progress.pulse()
                if not self.window.working:
                    break
                sleep(0.1)


    def __init__(self,par,database):
        gtk.Frame.__init__(self, _("Scoville Admin PRO :: New Schema"))
        self.par = par

        self.databaseId = database.getLocalId()

        self.working = True

        self.table = gtk.Table(4,2,False)
        
        self.instruction = gtk.Label(_("Enter the name of the new schema.\n\
         The first user (root) of the new scoville db will have the password 'root'.\n\
         Please change this password after your first login."))

        self.name_label = gtk.Label(_("Name:"))
        self.name_entry = DefaultEntry(default_message=_("new_database_name"))
        self.buttonhbox = gtk.HBox()
        self.progress = gtk.ProgressBar()
        self.cancel = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        self.buttonhbox.add(self.cancel)
        self.buttonhbox.add(self.ok)
        
        self.table.attach(self.instruction,0,2,0,1)
        self.table.attach(self.name_label,0,1,1,2)
        self.table.attach(self.name_entry,1,2,1,2)
        self.table.attach(self.buttonhbox,1,2,3,4)

        self.ok.connect("clicked", self.cb_Ok)
        self.cancel.connect("clicked", self.cb_Cancel)
        self.connect("delete-event", self.cb_Cancel)

        database.addCallback(self.render)

        self.table.set_border_width(10)
        self.add(self.table)
        self.getApplication().getMainWindow().openDialogPane(self)


    def cb_Ok(self,widget=None,data=None):
        database = self.getApplication().getLocalObjectById(self.databaseId)
        self.Pulse(self).start()
        database.createSchema(self.name_entry.get_text())

    def cb_Cancel(self, widget=None, data=None):
        self.getApplication().getMainWindow().closeDialogPane()

    def render(self):
        try:
            database = self.getApplication().getLocalObjectById(self.databaseId)
        except GenericObjectStoreException:
            self.getApplication().getMainWindow().closeDialogPane()
        if database.installFinished is not None and database.installFinished:
            self.working=False
            self.getApplication().getMainWindow().closeDialogPane()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
