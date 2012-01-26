from Generic import GenericScovilleObject

import json as jayson

class Widget(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.updated()
    
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return None
    
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
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
            self.getApplication().doRPCCall(self.getModule().getModules().getServer(),self.loadCssPropertySetCallback, "getCssPropertySet", [None,id,None])
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,json):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self.getModule().getModules().getServer(),self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])
    
    
    def getPar(self):
        return self.par
    
    def getModule(self):
        return self.getPar()