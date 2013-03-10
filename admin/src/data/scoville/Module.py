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
from Widget import Widget

import json as jayson

class Module(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.updated()
        self.loadWidgets()
    
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
        obj_id = self.getId()
        if obj_id is not None:
            self.getApplication().doRPCCall(self.getModules().getScoville(),self.loadCssPropertySetCallback, "getCssPropertySet", [obj_id,None,None])
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,json):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self.getModules().getScoville(),self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])
    
    def loadWidgetsCallback(self,data):
        widgetIds = [w.getId() for w in self.children]
        for widget in data:
            if widget['id'] not in widgetIds:
                self.addChild(Widget(self,widget))
            else:
                self.getWidgetById(widget['id']).refresh(widget)
                widgetIds.remove(widget['id'])
        for wgt in self.children:
            if wgt.getId() in widgetIds:
                self.children.remove(wgt)
                wgt.destroy()
        self.updated()
        self.getModules().updated()
        
    def loadWidgets(self):
        self.getApplication().doRPCCall(self.getModules().getScoville(),self.loadWidgetsCallback, "getWidgetsOfModule", [self.getId()])
    
    def createWidgetCallback(self, json):
        self.loadWidgets()
    
    def createWidget(self,name):
        self.getApplication().doRPCCall(self.getModules().getScoville(),self.createWidgetCallback, "createWidget", [self.getId(),name])
    
    def getWidgetById(self,obj_id):
        for widget in self.children:
            if widget.getId() == obj_id:
                return widget
        return None
    
    def getAllWidgets(self):
        return self.children
    
    def getPar(self):
        return self.par
    
    def getModules(self):
        return self.getPar()
    
