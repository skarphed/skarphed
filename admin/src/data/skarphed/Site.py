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

import hashlib
import base64
import os

from Menu import Menu

class Site(GenericSkarphedObject):
    def __init__(self,parent, data = {}):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.data = data
        self.updated()
        self.loadMenus()
    
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return "Unknown Site"
    
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None
    
    def getDescription(self):
        if self.data.has_key('description'):
            return self.data['description']
        else:
            return ""
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def update(self):
        self.getSkarphed().doRPCCall(self.refresh,"getSite",[self.getId()])
    
    def getWidgetInSpace(self, spaceId):
        if self.data['spaces'][str(spaceId)] == 0:
            return None
        else:
            modules = self.getSites().getSkarphed().modules.getModuleById(self.data['spaces'][str(spaceId)]['moduleId'])
            return modules.getWidgetById(self.data['spaces'][str(spaceId)]['id'])
    
    def getNameOfSpace(self, spaceId):
        return self.data['spaces'][spaceId]

    def getSpaces(self):
        return self.data['spaces']

    def getBoxes(self):
        return self.data['boxes']

    def getBox(self, box_id):
        return self.data['boxes'][str(box_id)]
    
    def getUsedWidgetIds(self):
        ret = []
        if not self.data.has_key('spaces'):
            return ret
        for space in self.data['spaces'].values():
            if space != 0:
                ret.append(space['id'])
        return ret
    
    def getSpaceCount(self):
        return len(self.data['spaces'])
    
    def getMinimap(self):
        if self.data.has_key('minimap'):
            md5 = hashlib.md5()
            raw = base64.b64decode(self.data['minimap'])
            md5.update(raw)
            tempfilename = md5.hexdigest()
            try:
                open('/tmp/skarphed/'+tempfilename,'r')
            except:
                pass
            else:
                return '/tmp/skarphed'+tempfilename
            try:
                os.mkdir('/tmp/skarphed/')
            except OSError,e :
                pass
            tempfile = open('/tmp/skarphed/'+tempfilename,'w')
            tempfile.write(raw)
            tempfile.close()
            return '/tmp/skarphed/'+tempfilename
    
    def getMenuById(self,menuId):
        for menu in self.children:
            if menu.getId() == menuId:
                return menu
        return None
    
    def loadMenusCallback(self,json):
        menuIds = [m.getId() for m in self.children]
        for menu in json:
            if menu['id'] not in menuIds:
                self.children.append(Menu(self,menu))
            else:
                self.getMenuById(menu['id']).update(menu)
        self.updated()
        
    def loadMenus(self):
        self.getSkarphed().doRPCCall(self.loadMenusCallback, "getMenusOfSite", [self.getId()])
    
    def createMenuCallback(self,json):
        self.loadMenus()
        
    def createMenu(self):
        self.getSkarphed().doRPCCall(self.createMenuCallback, "createMenuForSite", [self.getId()])
    
    def getPar(self):
        return self.par
    
    def getSites(self):
        return self.getPar()
    
    def getSkarphed(self):
        return self.getPar().getSkarphed()