#!/usr/bin/python
#-*- coding: utf-8 -*-

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