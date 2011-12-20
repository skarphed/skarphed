#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

class ViewPasswordButton(gtk.Button):
    def __init__(self, entry=None):
        gtk.Button.__init__(self)
        self.set_label("View Passwords")
        self.entries = []
        if entry is not None:
            self.entries.append(entry)
        self.connect("clicked", self.cb)
    
    def addEntry(self, entry):
        self.entries.append(entry)
    
    def cb(self,widget=None,data=None):
        for entry in self.entries:
            entry.set_visibility(not entry.get_visibility())