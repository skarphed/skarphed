#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Scoville.
#
# Scoville is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Scoville is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Scoville. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


from data.Generic import GenericScovilleObject

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
        self.cssPropertySet = json
        self.updated()
    
    def loadCssPropertySet(self):
        id = self.getId()
        if id is not None:
            self.getApplication().doRPCCall(self.getModule().getModules().getScoville(),self.loadCssPropertySetCallback, "getCssPropertySet", [None,id,None])
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,json):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self.getModule().getModules().getScoville(),self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])
    
    def deleteCallback(self,json):
        self.getModule().loadWidgets()
        self.destroy()
    
    def delete(self):
        self.getApplication().doRPCCall(self.getModule().getModules().getScoville(),self.deleteCallback, "deleteWidget", [self.getId()])
    
    def getPar(self):
        return self.par
    
    def getModule(self):
        return self.getPar()