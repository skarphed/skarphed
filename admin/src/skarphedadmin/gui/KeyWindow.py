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


from ViewPasswordButton import ViewPasswordButton
from skarphedadmin.data.Generic import GenericObjectStoreException

from skarphedadmin.glue.lng import _

class KeyWindow(gtk.Frame):
    addWindowOpen=False
    def __init__(self,parent, profile=None):
        gtk.Frame.__init__(self)
        self.par = parent
        self.serverId = None
        self.profile = profile
 #       self.set_title(_("Skarphed Admin Pro :: Public Key Infrastructure"))
        
        self.label = gtk.Label(_('Skarphed uses public keys to sign modules. If you are a developer\
 and want to submit modules to Skarphed repositories, you can create and\
 view your public Keys here.'))
        
        self.generateButton = gtk.Button(_("Generate PKI"))
        self.closeButton = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.generateButton.connect("clicked", self.cb_generateKeys)
        self.closeButton.connect("clicked", self.cb_close)
        
        self.publicview = gtk.TextView()
        self.privateview = gtk.TextView()
        
        self.publicframe = gtk.Frame(_("Public Key"))
        self.privateframe = gtk.Frame(_("Private Key"))
        
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
        self.getApplication().getMainWindow().openDialogPane(self)
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
        self.getApplication().getMainWindow().closeDialogPane()
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
         
