#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


import pygtk
pygtk.require("2.0")
import gtk

class DefaultEntry(gtk.Entry):
    def __init__(self, *args, **kwargs):
        if "default_message" in kwargs.keys():
            defaultMessage = kwargs["default_message"]
            del(kwargs["default_message"])
        else:
            defaultMessage = ""
        gtk.Entry.__init__(self, *args, **kwargs)
        self._isDefaultMessage = False
        self._defaultMessage = defaultMessage
        self.connect("focus-in-event", self.cb_focus_in)
        self.connect("focus-out-event", self.cb_focus_out)
        if self._defaultMessage != "":
            self.cb_focus_out()

    def set_default_message(self, default_message):
        self._defaultMessage = default_message
        self.cb_focus_out()

    def cb_focus_in(self, widget=None, data=None):
        if self._isDefaultMessage:
            self._isDefaultMessage = False
            gtk.Entry.set_text(self, "")
            self.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))

    def cb_focus_out(self, widget=None, data=None):
        if gtk.Entry.get_text(self) == "":
            self._isDefaultMessage = True
            gtk.Entry.set_text(self, self._defaultMessage)
            self.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#AAAAAA"))
    
    def get_text(self):
        if not self._isDefaultMessage:
            return gtk.Entry.get_text(self)
        else:
            return ""

    def set_text(self,text):
        gtk.Entry.set_text(self,text)
        self.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))
        self._isDefaultMessage = False