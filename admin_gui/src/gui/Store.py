#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

import IconStock

class Store(gtk.TreeStore):
    '''The Matchstore class is holding and managing the Data for the MatchTree. It communicates with the database'''
    def __init__(self,*args,**kwargs):
        '''Constructor --'''
        gtk.TreeStore.__init__(self,*args)
        self.par = kwargs['parent']
        root = self.append(None,(IconStock.SCOVILLE,"Scoville Infrastructure",-2))
        #self.append(root,(IconStock.SCOVILLE,'Scoville Infrastructure',-2))
  
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
