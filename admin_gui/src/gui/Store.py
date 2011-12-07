#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk


class Store(gtk.TreeStore):
    '''The Matchstore class is holding and managing the Data for the MatchTree. It communicates with the database'''
    def __init__(self,*args,**kwargs):
        '''Constructor --'''
        gtk.TreeStore.__init__(self,*args)
  
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
