#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import pygtk
pygtk.require("2.0")
import gtk

from skarphedadmin.glue.lng import _

class MessagePage(gtk.Frame):
    def __init__(self, par, message, callback=None):
        gtk.Frame.__init__(self, _("Message"))
        self.par = par
        self.hbox = gtk.HBox()
        self.vbox = gtk.VBox()
        self.dummy = gtk.Label("")
        self.label = gtk.Label(message)
        self.ok = gtk.Button(stock=gtk.STOCK_OK);
        self.hbox.pack_start(self.ok)
        self.vbox.pack_start(self.label,False)
        self.vbox.pack_start(self.hbox,False)
        self.vbox.pack_start(self.dummy,True)
        self.vbox.set_spacing(30)
        self.alignment = gtk.Alignment(0.5,0.5,0.5,0.5)
        self.alignment.add(self.vbox)
        self.add(self.alignment)

        self.callback=callback

        self.ok.connect('clicked', self.ok_callback)

        self.getApplication().getMainWindow().openDialogPane(self)

    def ok_callback(self, button, data=None):
        self.getApplication().getMainWindow().closeDialogPane()
        if self.callback is not None:
            self.callback()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
