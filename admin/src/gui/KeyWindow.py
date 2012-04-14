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


from IconStock import SCOVILLE
from ViewPasswordButton import ViewPasswordButton
from InstanceWindow import InstanceWindow
from data.Generic import GenericObjectStoreException

class KeyWindow(gtk.Window):
    addWindowOpen=False
    def __init__(self,parent, profile=None):
        if KeyWindow.addWindowOpen:
            self.destroy()
            return
        gtk.Window.__init__(self)
        self.par = parent
        self.serverId = None
        self.profile = profile
        self.set_title("Scoville Admin Pro :: Public Key Infrastructure")
        
        self.label = gtk.Label('Scoville uses public keys to sign modules. If you are a developer' + \
                               ' and want to submit modules to Scoville repositories, you can create and' +\
                               ' view your public Keys here.')
        
        self.generateButton = gtk.Button("Generate PKI")
        self.closeButton = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.generateButton.connect("clicked", self.cb_generateKeys)
        self.closeButton.connect("clicked", self.cb_close)
        
        self.publicview = gtk.TextView()
        self.privateview = gtk.TextView()
        
        self.publicframe = gtk.Frame("Public Key")
        self.privateframe = gtk.Frame("Private Key")
        
        self.publicframe.add(self.publicview)
        self.privateframe.add(self.privateview)
        
        self.vbox = gtk.VBox()
        self.hbox = gtk.HBox()
        self.dummy = gtk.Label("")
        
        self.vbox.pack_start(self.label,False)
        self.vbox.pack_start(self.publicframe,True)
        self.vbox.pack_start(self.privateframe,True)
        self.hbox.pack_start(self.dummy, True)
        self.hbox.pack_start(self.generateButton,False)
        self.hbox.pack_start(self.closeButton,False)
        self.vbox.pack_start(self.hbox,False)
        self.set_border_width(10)
        self.vbox.set_border_width(10)
        self.add(self.vbox)
        
        self.connect("delete-event", self.cb_close)
        self.show_all()
        KeyWindow.addWindowOpen = True
        self.render()
    
    def render(self):
        if self.profile.hasKeys():
            self.privateview.get_buffer().set_text(self.profile.getPrivateKey())
            self.publicview.get_buffer().set_text(self.profile.getPublicKey())
            self.generateButton.set_sensitive(False)
        else:
            self.generateButton.set_sensitive(True)
    
    def cb_generateKeys(self,widget=None,data=None):
        self.profile.generateKeyPair()
        self.render()
    
    def cb_close(self,widget=None,data=None):
        KeyWindow.addWindowOpen = False
        self.destroy()
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
         