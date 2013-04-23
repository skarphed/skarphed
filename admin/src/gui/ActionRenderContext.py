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

from ServerPropertyPage import ServerPropertyPage
from NewScoville import NewScoville
from gui.database.NewDatabasePage import NewDatabasePage
from gui.database.NewSchema import NewSchema
from gui.database.RegisterSchemaPage import RegisterSchemaPage
from InputBox import InputBox
from YesNoDialog import YesNoDialog
import IconStock 

class ActionRenderContext(object):
    """
    An action render context defines wich actions
    can be performed by or with this object.
    """
    def __init__(self, parent, obj):
        self.actions = []
        self.obj = obj
        self.par = parent

    def addAction(self, name, icon, callback):
        if name not in [a.getName() for a in self.actions]:
            self.actions.append(Action(name, icon, callback))

    def removeAction(self, name):
        for action in self.actions:
            if action.getName() == name:
                self.actions.remove(action)

    def getActions(self):
        return self.actions

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class Action(object):
    def __init__(self, name, icon, cb):
        self.name = name
        self.icon = icon
        self.callback = cb

    def getName(self):
        return self.name

    def getIcon(self):
        return self.icon

    def getCallback(self):
        return self.callback


class ServerARC(ActionRenderContext):
    def __init__(self, par, server):
        ActionRenderContext.__init__(self, par, server)

        self.addAction('Remove', IconStock.DELETE, self.removeServer)
        self.addAction('Connect', IconStock.WIDGET, self.connectServer)
        self.addAction('Properties', IconStock.SERVER, self.Properties)
        self.addAction('Create Instance', IconStock.SCOVILLE, self.createInstance)
        self.addAction('Register Database', IconStock.DATABASE, self.registerDatabase)

    def removeServer(self,data=None):
        def execute():
            self.obj.destroy()
        YesNoDialog(self.getApplication().mainwin, "Do you really want to remove this Server?", execute)
  
    def connectServer(self,data=None):
        self.obj.establishConnections()
        
    def Properties(self,data=None):
        ServerPropertyPage(self.getPar().getPar(),server=self.obj)
    
    def createInstance(self,data=None):
        NewScoville(self.getPar().getPar(),server=self.obj)
    
    def registerDatabase(self, data=None):
        NewDatabasePage(self.getPar().getPar(), self.obj)

class ScovilleARC(ActionRenderContext):
    def __init__(self, par, scoville):
        ActionRenderContext.__init__(self, par,scoville)

        self.addAction('Destroy', IconStock.DELETE, self.destroyInstance)
        self.addAction('Remove', IconStock.DELETE, self.removeInstance)
        self.addAction('CSS Editor', IconStock.CSS, self.cssEditor)
        self.addAction('Update Modules', IconStock.MODULE_UPDATEABLE, self.updateModules)

    def destroyInstance(self,data=None):
        pass

    def removeInstance(self,data=None):
        def execute():
            self.obj.getServer().removeInstance(self.obj)
        YesNoDialog(self.getApplication().mainwin, "Do you really want to delete this Instance?", execute)
    
    def cssEditor(self,data=None):
        self.getApplication().mainwin.openCssEditor(self.obj)

    def updateModules(self, data=None):
        self.obj.updateModules()


class UsersARC(ActionRenderContext):
    def __init__(self, par, users):
        ActionRenderContext.__init__(self, par,users)

        self.addAction('Create User', IconStock.USER, self.createUser)

    def createUser(self,data=None):
        InputBox(self,"what should be the name of the new User?", self.obj.createUser)
    
class UserARC(ActionRenderContext):
    def __init__(self, par, user):
        ActionRenderContext.__init__(self, par,user)

        self.addAction('Delete', IconStock.DELETE, self.deleteUser)

    def deleteUser(self,data=None):
        def execute():
            self.obj.delete()        
        YesNoDialog(self.getApplication().mainwin, "Do you really want to delete this User?", execute)

class ModuleARC(ActionRenderContext):
    def __init__(self, par, module):
        ActionRenderContext.__init__(self, par, module)

        self.addAction('Create Widget', IconStock.WIDGET, self.createWidget)
    
    def createWidget(self,data=None):
        InputBox(self,"what should be the name of the new Widget?", self.obj.createWidget)

class WidgetARC(ActionRenderContext):
    def __init__(self, par, widget):
        ActionRenderContext.__init__(self, par, widget)

        self.addAction('Delete', IconStock.DELETE, self.deleteWidget)

    def deleteWidget(self, data=None):
        def execute():
            self.obj.delete()
        YesNoDialog(self.getApplication().mainwin, "Do you really want to delete this Widget?", execute)
    
class SiteARC(ActionRenderContext):
    def __init__(self, par, site):
        ActionRenderContext.__init__(self, par, site)

        self.addAction('Create Menu', IconStock.MENU, self.createMenu)

    def createMenu(self, data=None):
        self.obj.createMenu()

class MenuARC(ActionRenderContext):
    def __init__(self, par, menu):
        ActionRenderContext.__init__(self, par, menu)

        self.addAction('Delete Menu', IconStock.DELETE, self.deleteMenu)

    def deleteMenu(self, data=None):
        def execute():
            self.obj.delete()
        YesNoDialog(self.getApplication().mainwin, "Do you really want to delete this Menu?", execute)

class RolesARC(ActionRenderContext):
    def __init__(self, par, roles):
        ActionRenderContext.__init__(self, par, roles)

        self.addAction('Create Role', IconStock.ROLE, self.createRole)

    def createRole(self, data=None):
        InputBox(self,"what should be the name of the new Widget?", self.obj.createRole)
    
class RoleARC(ActionRenderContext):
    def __init__(self, par, role):
        ActionRenderContext.__init__(self, par, role)

        self.addAction('Delete Role', IconStock.DELETE, self.deleteRole)

    def deleteRole(self, data=None):
        def execute():
            self.obj.delete()
        YesNoDialog(self.getApplication().mainwin, "Do you really want to delete this Role?", execute)
    
class DatabaseARC(ActionRenderContext):
    def __init__(self, par, database):
        ActionRenderContext.__init__(self, par, database)

        self.addAction('Register Schema', IconStock.SCHEMA, self.registerSchema)
        self.addAction('Create Schema', IconStock.SCHEMA, self.createSchema)

    def registerSchema(self, data=None):
        RegisterSchemaPage(self.getPar().getPar(), self.obj)

    def createSchema(self, data=None):
        NewSchema(self.getPar().getPar(), self.obj)

class SchemaARC(ActionRenderContext):
    def __init__(self, par,schema):
        ActionRenderContext.__init__(self, par, schema)

        self.addAction('Unregister Schema', IconStock.DELETE, self.unregisterSchema)
        self.addAction('Destroy Schema', IconStock.DELETE, self.destroySchema)

    def unregisterSchema(self, data=None):
        def execute():
            self.obj.getPar().unregisterSchema(self.obj)
        YesNoDialog(self.getApplication().mainwin, "Do you really want to remove this Schema?", execute)

    def destroySchema(self, data=None):
        def execute():
            self.obj.getPar().destroySchema(self.obj)
        YesNoDialog(self.getApplication().mainwin, "Do you really want to destroy this Schema?", execute)

ARCMAP = {
                   "Server"           : ServerARC,
                   "Users"            : UsersARC,
                   "User"             : UserARC,
                   "Module"           : ModuleARC,
                   "Roles"            : RolesARC,
                   "Role"             : RoleARC,
                   "Site"             : SiteARC,
                   "Widget"           : WidgetARC,
                   "Menu"             : MenuARC,
                   "Database"         : DatabaseARC,
                   "Schema"           : SchemaARC,
                   "Scoville"         : ScovilleARC
                   }

def getAppropriateARC(parent, obj):
    if ARCMAP.has_key(obj.__class__.__name__):
        return ARCMAP[obj.__class__.__name__](parent, obj)
    else:
        return ActionRenderContext(parent, None)
