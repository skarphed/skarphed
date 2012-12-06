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
import os

class NewScoville(gtk.Window):
    def __init__(self,par,server):
        self.par = par

        self.handlers = {
            "cb_Ok":self.cb_Ok,
            "cb_Cancel":self.cb_Cancel
        }

        builder = gtk.Builder()
        builder.add_from_file(os.path.dirname(__file__)+"/NewScoville.ui")
        print type(self.cb_Ok)
        print type(self.cb_Cancel)
        builder.connect_signals(self.handlers)

        self = builder.get_object("window1")
        self.serverId = server.getLocalId()
        self.show_all()
        


    def cb_Ok(self,widget=None,data=None):
        print "OK GELECKT"

    def cb_Cancel(self,widget=None,data=None):
        print "ABBRECHEN GELECKT"

    def render():
        pass

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()