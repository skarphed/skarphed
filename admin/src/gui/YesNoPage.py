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

class YesNoPage(gtk.Frame):
    def __init__(self, par, message, callback):
        gtk.Frame.__init__(self, message)
        self.par = par
        self.hbox = gtk.HBox()
        self.yes = gtk.Button("Yes");
        self.no = gtk.Button("No")
        self.hbox.pack_start(self.yes)
        self.hbox.pack_start(self.no)
        self.add(self.hbox)

        self.callback = callback

        self.yes.connect('clicked', self.yes_callback)
        self.no.connect('clicked', self.no_callback)

        self.getApplication().getMainWindow().openDialogPane(self)

    def no_callback(self, button, data=None):
        self.getApplication().getMainWindow().closeDialogPane()

    def yes_callback(self, button, data=None):
        if self.callback:
            self.callback()
        self.getApplication().getMainWindow().closeDialogPane()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
