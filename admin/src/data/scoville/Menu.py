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

class Menu(GenericScovilleObject):
    def __init__(self,par, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = par
        self.data = data
        self.updated()
        self.loadMenuItems()
        
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return "Unknown Menu"
    
    def update(self,data):
        self.data = data
        self.updated()
        
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None    
    
    def getMenuItemById(self,menuItemId):
        for menuItem in self.children:
            if menuItem.getId() == menuItemId:
                return menuItem
        return None
    
    def loadMenuItemsCallback(self,json):
        menuItemIds = [mi.getId() for mi in self.children]
        for menuItem in json:
            if menuItem['id'] not in menuItemIds:
                self.children.append(MenuItem(self,menuItem))
            else:
                self.getMenuItemById(menuItem['id']).update(menuItem)
        self.updated()
        
    def loadMenuItems(self):
        self.getApplication().doRPCCall(self.getSite().getSites().getScoville(),
                                        self.loadMenuItemsCallback,"getMenuItemsOfMenu",[self.getId()])
        
    def getMenuItemsRecursive(self):
        ret = self.children
        for menuItem in self.children:
            ret.extend(menuItem.getMenuItemsRecursive())
        return ret
        
    def getMenuItems(self):
        return self.children
    
    
    def getPar(self):
        return self.par
    
    def getSite(self):
        return self.getPar()
    
class MenuItem(GenericScovilleObject):
    def __init__(self,par, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = par
        self.data = data
        self.updated()
        self.loadMenuItems()
        
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return "Unknown MenuItem"
    
    def update(self,data):
        self.data = data
        self.updated()
        
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None  
    
    def getOrder(self):
        if self.data.has_key('order'):
            return self.data['order']
        else:
            return -1
    
    def getMenuItemById(self,menuItemId):
        for menuItem in self.children:
            if menuItem.getId() == menuItemId:
                return menuItem
        return None
    
    def loadMenuItemsCallback(self,json):
        menuItemIds = [mi.getId() for mi in self.children]
        for menuItem in json:
            if menuItem['id'] not in menuItemIds:
                self.children.append(MenuItem(self,menuItem))
            else:
                self.getMenuItemById(menuItem['id']).update(menuItem)
        self.updated()
        
    def loadMenuItems(self):
        self.getApplication().doRPCCall(self.getMenu().getSite().getSites().getScoville(),
                                        self.loadMenuItemsCallback,"getMenuItemsOfMenuItem",[self.getId()])
    
    def getMenuItemsRecursive(self):
        ret = self.children
        for menuItem in self.children:
            ret.extend(menuItem.getMenuItemsRecursive())
        return ret
    
    def orderCallback(self,json):
        self.getPar().loadMenuItems()
    
    def increaseOrder(self):
        self.getApplication().doRPCCall(self.getMenu().getSite().getSites().getScoville(),
                                        self.orderCallback,"increaseMenuItemOrder",[self.getId()])
    
    def decreaseOrder(self):
        self.getApplication().doRPCCall(self.getMenu().getSite().getSites().getScoville(),
                                        self.orderCallback,"decreaseMenuItemOrder",[self.getId()])
    
    def moveToTop(self):
        self.getApplication().doRPCCall(self.getMenu().getSite().getSites().getScoville(),
                                        self.orderCallback,"moveToTopMenuItemOrder",[self.getId()])
    
    def moveToBottom(self):
        self.getApplication().doRPCCall(self.getMenu().getSite().getSites().getScoville(),
                                        self.orderCallback,"moveToBottomMenuItemOrder",[self.getId()])
    
    def getMenuItems(self):
        return self.children
    
    def getPar(self):
        return self.par
    
    def getSite(self):
        return self.getPar()
    
    def getMenu(self):
        if self.getPar().__class__.__name__ == 'Menu':
            return self.getPar()
        else:
            return self.getPar().getMenu()

class Action():pass

class ActionList():pass