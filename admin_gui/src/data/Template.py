#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

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
    
    def getUsers(self):
        return self.getPar()