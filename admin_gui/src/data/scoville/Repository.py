#!/usr/bin/python
#-*- coding: utf-8 -*-

from data.Generic import GenericScovilleObject

class Repository(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.ip = '192.168.0.23'
        self.updated()
    
    def getName(self):
        if self.ip is not None:
            return "Repository [%s]"%self.ip
        else:
            return "(No Repository)"
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()