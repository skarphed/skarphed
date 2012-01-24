#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

import json as jayson

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
    
    def getId(self):
        if self.data.has_key('serverModuleId'):
            return self.data['serverModuleId']
        else:
            return None
    
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
    
    def loadCssPropertySetCallback(self,json):
        self.cssPropertySet = jayson.JSONDecoder().decode(json)
        self.updated()
    
    def loadCssPropertySet(self):
        id = self.getId()
        if id is not None:
            self.getApplication().doRPCCall(self.getModules().getServer(),self.loadCssPropertySetCallback, "getCssPropertySet", [id,None,None])
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,json):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self.getModules().getServer(),self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])
    
    
    def getPar(self):
        return self.par
    
    def getModules(self):
        return self.getPar()