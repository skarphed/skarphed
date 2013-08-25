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

from OperationTree import OperationTree

class OperationTool(gtk.VBox):
    def __init__(self,par,server=None):
        self.par = par
        gtk.VBox.__init__(self)
        
        self.operationTree = OperationTree(self,server)
        self.operationTreeScroll = gtk.ScrolledWindow()
        self.operationTreeScroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.drop = gtk.Button(stock=gtk.STOCK_MEDIA_STOP)
        self.retry = gtk.Button(stock=gtk.STOCK_MEDIA_PLAY)
        
        self.cancel.connect("clicked", self.cancelOperation)
        self.drop.connect("clicked", self.dropOperation)
        self.retry.connect("clicked", self.retryOperation)
        
        self.operationTree.connect("cursor-changed", self.newTreeSelection)
                
        self.buttonbox = gtk.HBox()
        self.buttonbox.pack_end(self.cancel,False)
        self.buttonbox.pack_end(self.drop,False)
        self.buttonbox.pack_end(self.retry,False)
        
        self.operationTreeScroll.add(self.operationTree)
        self.pack_start(self.operationTreeScroll,True)
        self.pack_start(self.buttonbox,False)
        
        if server is not None:
            server.getOperationManager().addCallback(self.render)
        else:
            self.getApplication().getObjectStore().addCallback(self.render)
        
        self.set_size_request(400,200)
        
        self.show_all()
    
    def newTreeSelection(self, widget=None, data=None):
        op = widget.getCurrentOperation()
        if op is None:
            self.cancel.set_sensitive(False)
            self.drop.set_sensitive(False)
            self.retry.set_sensitive(False)
            return
            
        if op.data['status'] == op.PENDING:
            self.cancel.set_sensitive(True)
            self.drop.set_sensitive(False)
            self.retry.set_sensitive(False)
        elif op.data['status'] == op.ACTIVE:
            self.cancel.set_sensitive(False)
            self.drop.set_sensitive(False)
            self.retry.set_sensitive(False)
        elif op.data['status'] == op.FAILED:
            self.cancel.set_sensitive(False)
            self.drop.set_sensitive(True)
            self.retry.set_sensitive(True)
        
    def cancelOperation(self, widget=None, data=None):
        op = self.operationTree.getCurrentOperation()
        op.cancel()
        
    def dropOperation(self, widget=None, data=None):
        op = self.operationTree.getCurrentOperation()
        op.drop()
    
    def retryOperation(self, widget=None, data=None):
        op = self.operationTree.getCurrentOperation()
        op.retry()
    
    def render(self):
        self.newTreeSelection(self.operationTree)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()