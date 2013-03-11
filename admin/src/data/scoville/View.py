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

class View(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        viewIds = [s.getId() for s in self.children]
        for view in data:
            if view['id'] not in viewIds:
                self.addChild(View(self,view))
            else:
                self.getviewById(view['id']).refresh(view)                
    
    def getViewById(self,nr):
        for view in self.children:
            if view.getId() == nr:
                return view
        return None
    
    def refresh(self,data):
        self.data = data
    
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return "Unknown View"
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()

class Views(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        viewIds = [s.getId() for s in self.children]
        for view in data:
            if view['id'] not in viewIds:
                self.addChild(View(self,view))
            else:
                self.getviewById(view['id']).refresh(view)                
    
    def getViewById(self,nr):
        for view in self.children:
            if view.getId() == nr:
                return view
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getScoville(),self.refreshCallback, "getViews")
    
    def getViews
    (self):
        return self.children
    
    def getName(self):
        return "Views"
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()