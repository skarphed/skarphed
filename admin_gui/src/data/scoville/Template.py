#!/usr/bin/python
#-*- coding: utf-8 -*-

from data.Generic import GenericScovilleObject

class Template(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.updated()
    
    def getName(self):
        return "Templates"
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()