#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

class Module(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.updated()
    
    def getName(self):
        if self.data.has_key('hrname'):
            return self.data['hrname']+" ["+self.getPrintableVersion()+"]"
        else:
            return "Unknown Module"
    
    def getPrintableVersion(self):
        return str(self.data['version_major'])+"."+str(self.data['version_minor'])+"."+str(self.data['revision'])
    
    def getModuleName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return None
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def getPar(self):
        return self.par
    
    def getUsers(self):
        return self.getPar()