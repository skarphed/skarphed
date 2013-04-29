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

from ActionRenderContext import getAppropriateARC

class Toolbar(gtk.Toolbar):
    def __init__(self, parent):
        self.par = parent
        gtk.Toolbar.__init__(self)

        self.logoutbutton=gtk.ToolButton()
        self.logoutbutton.set_stock_id(gtk.STOCK_QUIT)
        self.logoutbutton.connect("clicked", self.getPar().cb_LogoutButton)

        self.addserverbutton=gtk.ToolButton()
        self.addserverbutton.set_stock_id(gtk.STOCK_ADD)
        self.addserverbutton.connect("clicked", self.getPar().cb_AddServerButton)
        
        self.pkibutton=gtk.ToolButton()
        self.pkibutton.set_stock_id(gtk.STOCK_PROPERTIES)
        self.pkibutton.connect("clicked", self.getPar().cb_pkiButton)

        self.add(self.logoutbutton)
        self.add(self.addserverbutton)
        self.add(self.pkibutton)

        self.add(gtk.SeparatorToolItem())

        self.contextButtons = []    

    def renderContextButtons(self, obj):
        for item in self.contextButtons:
            self.remove(item)
        self.contextButtons = []

        arc = getAppropriateARC(self, obj)

        for action in arc.getActions():
            image = gtk.Image()
            image.set_from_pixbuf(action.getIcon())
            item = gtk.ToolButton(image,action.getName())
            item.connect("clicked", action.getCallback())
            self.insert(item,-1)
            self.contextButtons.append(item)

        self.show_all()

    def clearButtons(self):
        for item in self.contextButtons:
            self.remove(item)
        self.contextButtons = []

        self.show_all()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()