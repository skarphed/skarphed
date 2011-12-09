#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

class GenericObject(gtk.VBox):
    def __init__(self,parent,object):
        gtk.VBox.__init__(self)
        self.par = parent
        
    def render(self):
        print "REDNERERD"
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()