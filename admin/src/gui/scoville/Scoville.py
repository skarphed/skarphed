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

from GenericObject import GenericObjectPage
from GenericObject import PageFrame
from GenericObject import FrameLabel
from data.Generic import GenericObjectStoreException
from OperationDaemonControl import OperationDaemonControl
import gui.IconStock

class ScovillePage(GenericObjectPage):
    def __init__(self,par,scoville):
        GenericObjectPage.__init__(self,par,scoville)
        self.scovilleId = scoville.getLocalId()
        
        self.headline = gtk.Label("Scoville Instance")
        self.pack_start(self.headline,False)
        
        self.repo = PageFrame(self,"Repository", gui.IconStock.REPO)
        self.repoDummy = gtk.Label("")
        self.repoHBox = gtk.HBox()
        self.repotable = gtk.Table(2,3)
        self.repoLabel = gtk.Label("Repository")
        self.repoEntry = gtk.Entry()
        self.repoInfoLabel = gtk.Label("Please enter Repository URL here:")
        self.repoOkButton = gtk.Button(stock=gtk.STOCK_OK)
        self.repoOkButton.connect("clicked", self.cb_changeRepo)
        
        self.repotable.attach(self.repoInfoLabel,0,2,0,1)
        self.repotable.attach(self.repoLabel,0,1,1,2)
        self.repotable.attach(self.repoEntry,1,2,1,2)
        self.repotable.attach(self.repoOkButton,1,2,2,3)
        self.repoHBox.pack_start(self.repotable,False)
        self.repoHBox.pack_start(self.repoDummy,True)
        self.repo.add(self.repoHBox)

        self.pack_start(self.repo,False)

        self.opd = OperationDaemonControl(self,scoville.getOperationDaemon())
        self.pack_start(self.opd,False)
        
        self.pki = PageFrame(self, "Public Key", gui.IconStock.CREDENTIAL)
        self.pki_label = gtk.Label("Instance Public Key:")
        self.pki_textview = gtk.TextView()
        self.pki_textbuffer = gtk.TextBuffer()
        self.pki_textview.set_buffer(self.pki_textbuffer)
        self.pki_vbox = gtk.VBox()
        self.pki_vbox.pack_start(self.pki_label,False)
        self.pki_vbox.pack_start(self.pki_textview,True)
        self.pki.add(self.pki_vbox)
        self.pack_start(self.pki, False)

        self.show_all()
        
        self.render()
        scoville.addCallback(self.render)
    
    def render(self):
        try:
            scoville = self.getApplication().getLocalObjectById(self.scovilleId)
        except GenericObjectStoreException, e:
            self.destroy()
            return
        repo = scoville.getRepository()
        try:
            self.repoEntry.set_text(repo.getURL())
        except AttributeError:
            pass
        public_key = scoville.getPublicKey()
        if public_key is not None:
            self.pki_textbuffer.set_text(public_key)
        else:
            self.pki_textbuffer.set_text("")    
        
    def cb_changeRepo(self, widget=None, data=None):
        scoville = self.getApplication().getLocalObjectById(self.scovilleId)
        repostring = self.repoEntry.get_text()
        host,port = repostring.split(":")
        port = int(port)        
        scoville.setRepository(host,port)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

        
