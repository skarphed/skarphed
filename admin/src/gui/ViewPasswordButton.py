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

from lng import _

class ViewPasswordButton(gtk.Button):
    def __init__(self, entry=None):
        gtk.Button.__init__(self)
        self.set_label(_("View Passwords"))
        self.entries = []
        if entry is not None:
            self.entries.append(entry)
        self.connect("clicked", self.cb)
    
    def addEntry(self, entry):
        self.entries.append(entry)
    
    def cb(self,widget=None,data=None):
        for entry in self.entries:
            entry.set_visibility(not entry.get_visibility())