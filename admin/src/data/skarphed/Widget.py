#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


from data.Generic import GenericSkarphedObject

class Widget(GenericSkarphedObject):
    def __init__(self,parent, data = {}):
        GenericSkarphedObject.__init__(self)
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

    def getBaseView(self):
        if self.data['baseview'] is None:
            return None
        else:
            return self.getModule().getModules().getSkarphed().getViews().getViewById(self.data['baseview'])

    def getBaseSpaceId(self):
        if self.data['basespace'] is None:
            return None
        else:
            return self.data['basespace']
    
    def loadCssPropertySetCallback(self,json):
        self.cssPropertySet = json
        self.updated()
    
    def loadCssPropertySet(self):
        nr = self.getId()
        if nr is not None:
            self.getApplication().doRPCCall(self.getModule().getModules().getSkarphed(),self.loadCssPropertySetCallback, "getCssPropertySet", [None,nr,None])
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,json):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self.getModule().getModules().getSkarphed(),self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])

    def activateGeneratingViewsCallback(self, data):
        self.getModule().loadWidgets()

    def activateGeneratingViews(self, view, spaceId):
        self.getApplication().doRPCCall(self.getModule().getModules().getSkarphed(),self.activateGeneratingViewsCallback, "widgetActivateViewGeneration", [self.getId(), view.getId(), spaceId])

    def deactivateGeneratingViewsCallback(self, data):
        self.getModule().loadWidgets()

    def deactivateGeneratingViews(self):
        self.getApplication().doRPCCall(self.getModule().getModules().getSkarphed(),self.deactivateGeneratingViewsCallback, "widgetDeactivateViewGeneration", [self.getId()])

    def isGeneratingViews(self):
        return self.data['gviews']
    
    def deleteCallback(self,json):
        self.getModule().loadWidgets()
        # update views because viewmappings with this widgets have been deleted
        self.getModule().getModules().getSkarphed().getViews().refresh()
        # update actionlists because viewmappings with this widgets have been deleted
        actionlists = self.getApplication().getObjectStore().getAllOfClass("ActionList",parent=self.getModule().getModules().getSkarphed())
        for actionlist in actionlists:
            actionlist.loadActions()
        self.destroy()
    
    def delete(self):
        self.getApplication().doRPCCall(self.getModule().getModules().getSkarphed(),self.deleteCallback, "deleteWidget", [self.getId()])
    
    def getPar(self):
        return self.par
    
    def getModule(self):
        return self.getPar()