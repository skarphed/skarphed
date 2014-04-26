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


from skarphedadmin.data.Generic import GenericSkarphedObject
from skarphedadmin.data.skarphed.Skarphed import rpc


class Menu(GenericSkarphedObject):
    def __init__(self,par, data = {}):
        GenericSkarphedObject.__init__(self)
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
                menuItemIds.remove(menuItem['id'])
        for mi in self.children:
            if mi.getId() in menuItemIds:
                self.children.remove(mi)
                mi.destroy()
        self.updated()

    @rpc(loadMenuItemsCallback)
    def getMenuItemsOfMenu(self, menuId):
        pass
    
    def loadMenuItems(self):
        self.getMenuItemsOfMenu(self.getId())
        
    def getMenuItemsRecursive(self):
        ret = [c.getLocalId() for c in self.children]
        for menuItem in self.children:
            ret.extend(menuItem.getMenuItemsRecursive())
        return ret
        
    def getMenuItems(self):
        return self.children
    
    def deleteCallback(self,json):
        self.destroy()

    @rpc(deleteCallback)
    def deleteMenu(self, menuId):
        pass
        
    def delete(self):
        self.deleteMenu(self.getId())
    
    def createMenuItemCallback(self,json):
        self.loadMenuItems()

    @rpc(createMenuItemCallback)
    def createMenuItem(self, parent_id, parent_type='menu'):
        pass
        
    def createNewMenuItem(self):
        self.createMenuItem(self.getId(),'menu')
    
    def deleteMenuItemCallback(self,json):
        self.loadMenuItems()
    
    @rpc(deleteMenuItemCallback)
    def deleteMenuItem(self, menuItemId):
        pass

    def deleteChildItem(self,menuItem):
        if menuItem in self.children:
            self.deleteMenuItem(menuItem.getId())

    def renameCallback(self,json):
        self.getSite().loadMenus()

    @rpc(renameCallback)
    def renameMenu(self, menuId, name):
        pass
    
    def rename(self,name):
        self.renameMenu(self.getId(),name)
    
    def getPar(self):
        return self.par
    
    def getSite(self):
        return self.getPar()
    
class MenuItem(GenericSkarphedObject):
    def __init__(self,par, data = {}):
        GenericSkarphedObject.__init__(self)
        self.par = par
        self.data = data
        self.actionList = None
        self.updated()
        self.loadActionList()
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
                menuItemIds.remove(menuItem['id'])
        for mi in self.children:
            if mi.getId() in menuItemIds:
                self.children.remove(mi)
                mi.destroy()
        self.updated()
        self.getMenu().updated()
    
    @rpc(loadMenuItemsCallback)
    def getMenuItemsOfMenuItem(self, menuItemId):
        pass

    def loadMenuItems(self):
        self.getMenuItemsOfMenuItem(self.getId())
    
    def getMenuItemsRecursive(self):
        ret = [c.getLocalId() for c in self.children]
        for menuItem in self.children:
            ret.extend(menuItem.getMenuItemsRecursive())
        return ret
    
    def orderCallback(self,json):
        self.getPar().loadMenuItems()
    
    @rpc(orderCallback)
    def increaseMenuItemOrder(self, menuItemId):
        pass

    def increaseOrder(self):
        self.increaseMenuItemOrder(self.getId())
    
    @rpc(orderCallback)
    def decreaseMenuItemOrder(self, menuItemId):
        pass

    def decreaseOrder(self):
        self.decreaseMenuItemOrder(self.getId())

    @rpc(orderCallback)
    def moveToTopMenuItemOrder(self, menuItemId):
        pass
    
    def moveToTop(self):
        self.moveToTopMenuItemOrder(self.getId())
    
    @rpc(orderCallback)
    def moveToBottomMenuItemOrder(self, menuItemId):
        pass

    def moveToBottom(self):
        self.moveToBottomMenuItemOrder(self.getId())
    
    def getMenuItems(self):
        return self.children
    
    def deleteCallback(self, json):
        for child in self.children:
            child.destroy()
        self.getPar().loadMenuItems()
    
    @rpc(deleteCallback)
    def deleteMenuItem(self, menuItemId):
        pass
    
    def delete(self):
        self.deleteMenuItem(self.getId())

    def createMenuItemCallback(self,json):
        self.loadMenuItems()
        
    @rpc(createMenuItemCallback)
    def createMenuItem(self, parent_id, parent_type='menuItem'):
        pass
    
    def createNewMenuItem(self):
        self.createMenuItem(self.getId())
    
    def renameCallback(self, json):
        self.getPar().loadMenuItems()

    @rpc(renameCallback)
    def renameMenuItem(self, menuItemId, newName):
        pass

    def rename(self, name):
        self.renameMenuItem(self.getId(),name)
    
    def getActionList(self):
        return self.actionList
    
    def loadActionListCallback(self,json):
        if self.actionList is None:
            self.actionList = ActionList(self,json)
        else:
            self.actionList.update(json)
        self.updated()

    @rpc(loadActionListCallback)
    def getActionListForMenuItem(self, menuItemId):
        pass

    def loadActionList(self):
        self.getActionListForMenuItem(self.getId())
    
    def deleteMenuItemCallback(self,json):
        self.loadMenuItems()
    
    def deleteChildItem(self,menuItem):
        if menuItem in self.children:
            self.deleteMenuItem(menuItem.getId())
    
    def getPar(self):
        return self.par

    def getMenu(self):
        if self.getPar().__class__.__name__ == 'Menu':
            return self.getPar()
        else:
            return self.getPar().getMenu()

class Action(GenericSkarphedObject):
    def __init__(self,par, data = {}):
        GenericSkarphedObject.__init__(self)
        self.par = par
        self.data = data
        self.updated()
    
    def update(self,data):
        self.data=data
        self.updated()
    
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None
    
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return None
    
    def getOrder(self):
        if self.data.has_key('order'):
            return self.data['order']
        else:
            return None
    
    
    def orderCallback(self,json):
        self.getPar().loadActions()
    
    @rpc(orderCallback)
    def increaseActionOrder(self, actionId):
        pass

    def increaseOrder(self):
        self.increaseActionOrder(self.getId())
    
    @rpc(orderCallback)
    def decreaseActionOrder(self, actionId):
        pass

    def decreaseOrder(self):
        self.decreaseActionOrder(self.getId())
    
    @rpc(orderCallback)
    def moveToTopActionOrder(self, actionId):
        pass

    def moveToTop(self):
        self.moveToTopActionOrder(self.getId())
    
    @rpc(orderCallback)
    def moveToBottomActionOrder(self, actionId):
        pass

    def moveToBottom(self):
        self.moveToBottomActionOrder(self.getId())
    
    
    def setNewTargetCallback(self,json):
        self.getPar().loadActions()
    
    @rpc(setNewTargetCallback)
    def setActionUrl(self, actionId, url):
        pass

    def setUrl(self,url):
        self.setActionUrl(self.getId(), url)
    
    @rpc(setNewTargetCallback)
    def setActionWidgetSpaceConstellation(self, actionId, widgetId, space):
        pass

    def setWidgetSpaceConstellation(self, widgetId, space):
        widget = self.getApplication().getLocalObjectById(widgetId)
        self.setActionWidgetSpaceConstellation (self.getId(),widget.getId(),space)
    
    @rpc(setNewTargetCallback)
    def setActionView(self, actionId, viewId):
        pass

    def setView(self,viewId):
        view = self.getApplication().getLocalObjectById(viewId)
        self.setActionView(self.getId(),view.getId())

    def getSpaceId(self):
        return self.data['space']
    
    def getWidgetId(self):
        return self.data['widgetId']

    def getWidget(self):
        return self.getActionList().getMenuItem().getMenu().getSite().getSkarphed().getModules().getWidgetById(self.getWidgetId())
    
    def getViewId(self):
        return self.data['viewId']

    def getView(self):
        return self.getActionList().getMenuItem().getMenu().getSite().getSkarphed().getViews().getViewById(self.getViewId())

    def getPar(self):
        return self.par
    
    def getActionList(self):
        return self.getPar()
    

class ActionList(GenericSkarphedObject):
    def __init__(self,par, data = {}):
        GenericSkarphedObject.__init__(self)
        self.par = par
        self.data = data
        self.updated()
        self.loadActions()
    
    def update(self,data):
        self.data = data
        self.updated()
    
    def getActions(self):
        return self.children
    
    def getActionById(self, obj_id):
        for action in self.children:
            if action.getId() == obj_id:
                return action
        return None
    
    def loadActionsCallback(self,json):
        actionIds = [a.getId() for a in self.children]
        for action in json:
            if action['id'] not in actionIds:
                self.children.append(Action(self,action))
            else:
                self.getActionById(action['id']).update(action)
        result_action_ids = [a['id'] for a in json]
        for action in self.children:
            if action.getId() not in result_action_ids:
                self.removeChild(action)
        self.updated()
            
    @rpc(loadActionsCallback)
    def getActionsOfActionList(self, actionId):
        pass

    def loadActions(self):
        self.getActionsOfActionList(self.getId())
    
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None
    
    def addActionCallback(self,json):
        self.loadActions()
    
    @rpc(addActionCallback)
    def addActionToActionList(self, actionId):
        pass

    def addAction(self):
        self.addActionToActionList(self.getId())
    
    def deleteActionCallback(self,json):
        self.loadActions()
        
    @rpc(deleteActionCallback)
    def deleteAction(self, actionId):
        pass

    def deleteChildAction(self,action):
        self.deleteAction(action.getId())
        self.children.remove(action)
        action.destroy()
    
    def getPar(self):
        return self.par
    
    def getMenuItem(self):
        return self.getPar()
