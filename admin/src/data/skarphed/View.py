#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


from data.Generic import GenericSkarphedObject

class View(GenericSkarphedObject):
    def __init__(self,parent, data):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.data = data
        self.loaded_fully = False
        if not self.data.has_key('space_widget_mapping'):
            self.data['space_widget_mapping'] = {}
        if not self.data.has_key('widget_param_mapping'):
            self.data['widget_param_mapping'] = {}
        if not self.data.has_key('page_id'):
            self.data['page_id'] = None
        self.updated()
        
    def loadFullCallback(self,data):
        self.data = data
        self.loaded_fully = True
        self.updated()

    def loadFull(self):
        self.getApplication().doRPCCall(self.getViews().getSkarphed(),self.loadFullCallback, "getView", [self.getId()])

    def isFullyLoaded(self):
        return self.loaded_fully

    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None
    
    def getPage(self):
        if self.data.has_key('site'):
            page = self.getViews().getSkarphed().getSites().getSiteById(self.data['site'])
            return page
        else:
            return None

    def refresh(self,data):
        self.data.update(data)
    
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return "Unknown View"

    def getSpaceWidgetMapping(self, widget=None):
        if self.data.has_key('space_widget_mapping'):
            return self.data['space_widget_mapping']
        else:
            self.loadFull()

    def getWidgetParamMapping(self, widget=None):
        if self.data.has_key('widget_param_mapping'):
            if widget is not None:
                if self.data['widget_param_mapping'].has_key(str(widget.getId())):
                    return self.data['widget_param_mapping'][str(widget.getId())]
                else:
                    return {}
            return self.data['widget_param_mapping']
        else:
            self.loadFull()

    def changeWidgetCallback(self, json):
        self.loadFull()

    def setWidgetParamMapping(self, widget, mapping):
        self.getApplication().doRPCCall(self.getViews().getSkarphed(),self.changeWidgetCallback, "setWidgetParamMapping", [self.getId(), widget.getId(), mapping])

    def setSpaceWidgetMapping(self, mapping):
        self.getApplication().doRPCCall(self.getViews().getSkarphed(),self.changeWidgetCallback, "setSpaceWidgetMapping", [self.getId(), mapping])

    #def setWidgetIntoSpace(self, space_id, widget):
    #    self.getApplication().doRPCCall(self.getViews().getSkarphed(),self.changeWidgetCallback, "assignWidgetToSpace", [self.getId(), space_id, widget.getId()])

    #def removeWidgetFromSpace(self, space_id):
    #    self.getApplication().doRPCCall(self.getViews().getSkarphed(),self.changeWidgetCallback, "removeWidgetFromSpace", [self.getId(), space_id])
    
    def getPar(self):
        return self.par
    
    def getViews(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()

class Views(GenericSkarphedObject):
    def __init__(self,parent):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        viewIds = [s.getId() for s in self.children]
        for view in data:
            if view['id'] not in viewIds:
                self.addChild(View(self,view))
            else:
                existing_view = self.getViewById(view['id'])
                existing_view.refresh(view)                
    
    def getViewById(self,nr):
        for view in self.children:
            if view.getId() == nr:
                return view
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getSkarphed(),self.refreshCallback, "getViews")
    
    def getViews(self):
        return self.children
    
    def getName(self):
        return "Views"
    
    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()