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

class GenericObjectPage(gtk.VBox):
    def __init__(self,parent,obj,iconstock=None):
        gtk.VBox.__init__(self,spacing = 10)
        self.par = parent
        
    def render(self):
        pass
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class PageFrame(gtk.Frame):
    def __init__(self,parent, text, icon=None):
        gtk.Frame.__init__(self)
        self.set_border_width(10)
        self.set_label_widget(FrameLabel(self,text,icon))
        
        

class FrameLabel(gtk.HBox):
    def __init__(self,parent, text, icon=None):
        self.par = parent
        gtk.HBox.__init__(self)
        self.set_spacing(10)
        assert type(text) == str, "text must be string"
        
        self.icon = gtk.Image()
        if icon is not None:
            self.icon.set_from_pixbuf(icon)
        self.label = gtk.Label()
        self.label.set_text(text)
        
        self.pack_start(self.icon,False)
        self.pack_start(self.label,True)
        self.show_all()
    
    def setText(self,text):
        self.label.set_text(text)

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

        
    
    
    
