#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk


class Tree(gtk.TreeView):
    def __init__(self, parent):
        gtk.TreeView.__init__(self)
        self.par = parent
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()