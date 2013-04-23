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

class TreeContextMenu(gtk.Menu):
    def __init__(self,parent):
        gtk.Menu.__init__(self)

        self.par = parent
        self.concernedIter = None

        self.currentItems = []

        self.show_all()

    def popup(self,obj,button,time):
        for item in self.currentItems:
            self.remove(item)
        self.currentItems = []
        
        arc = getAppropriateARC(self, obj)

        for action in arc.getActions():
           image = gtk.Image()
           image.set_from_pixbuf(action.getIcon()) 
           item = gtk.ImageMenuItem()
           item.set_image(image)
           gtk.MenuItem.__init__(item, action.getName())
           item.connect("activate", action.getCallback())
           self.currentItems.append(item)

        for item in self.currentItems:
            self.append(item)

        gtk.Menu.popup(self,None,None,None,button,time,None)

        self.show_all()
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()