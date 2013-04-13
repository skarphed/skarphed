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

class YesNoDialog(gtk.MessageDialog):
    def __init__(self, par, message, callback):
        gtk.MessageDialog.__init__(self,parent=par, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO)
        self.set_markup(message)
        self.par = par
        self.callback = callback

        self.connect('response', self.response_callback)
        self.connect('close', self.close_callback)
        self.run()

    def close_callback(self):
        self.destroy()

    def response_callback(self, dialog, resp):
        if resp == gtk.RESPONSE_YES:
            self.callback()
        self.destroy()
