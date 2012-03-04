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

class InputBox(gtk.Window):
    inputBoxOpen = False
    def __init__(self,par,text,callback,typeWanted=False):
        self.par = par
        gtk.Window.__init__(self)
        
        self.set_title("Scoville Admin")
        self.set_border_width(10)
        
        self.label = gtk.Label(text)
        self.entry = gtk.Entry()
        self.space = gtk.Label()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        
        self.hbox = gtk.HBox()
        self.vbox = gtk.VBox()
        
        self.hbox.pack_start(self.space,True)
        self.hbox.pack_start(self.ok,False)
        
        self.vbox.pack_start(self.label,True)
        self.vbox.pack_start(self.entry,False)
        self.vbox.pack_start(self.hbox,False)
        
        self.ok.connect("clicked", self.okCallback)
        self.cb = callback()
        self.typeWanted = typeWanted
        
        self.add(self.vbox)
        self.show_all()
    
    def okCallback(self,widget=None,data=None):
        def errorMessage(msgId):
            msgs = ("This is not a valid int number",
                    )
            dia = gtk.MessageDialog(parent=self.getPar().getPar(), flags=0, type=gtk.MESSAGE_WARNING, \
                                  buttons=gtk.BUTTONS_OK, message_format=msgs[msgId])
            dia.run()
            dia.destroy()
        
        value = self.entry.get_text()
        
        if self.typeWanted == int:
            try:
                value = int(value)
            except ValueError:
                errorMessage(0)
                return
        self.destroy()
        self.cb(value)
        
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
