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
from NewScovillePage import NewScovillePage
from gui.database.NewDatabasePage import NewDatabasePage
from gui.database.NewSchemaPage import NewSchemaPage
from gui.database.RegisterSchemaPage import RegisterSchemaPage
from InputBox import InputBox
from YesNoPage import YesNoPage
import IconStock 

from glue.lng import _

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

        self.addAction(_('Remove...'), IconStock.DELETE, self.removeServer)
        self.addAction(_('Connect...'), IconStock.WIDGET, self.connectServer)
        self.addAction(_('Properties...'), IconStock.SERVER, self.Properties)
        self.addAction(_('Create Instance...'), IconStock.SCOVILLE, self.createInstance)
        self.addAction(_('Register Database...'), IconStock.DATABASE, self.registerDatabase)

    def removeServer(self,data=None):
        def execute():
            self.obj.destroy()
        YesNoPage(self.getApplication().mainwin, _("Do you really want to remove this Server?"), execute)
  
    def connectServer(self,data=None):
        self.obj.establishConnections()
        
    def Properties(self,data=None):
        ServerPropertyPage(self.getPar().getPar(),server=self.obj)
    
    def createInstance(self,data=None):
        NewScovillePage(self.getPar().getPar(),server=self.obj)
    
    def registerDatabase(self, data=None):
        NewDatabasePage(self.getPar().getPar(), self.obj)

class ScovilleARC(ActionRenderContext):
    def __init__(self, par, scoville):
        ActionRenderContext.__init__(self, par,scoville)

        self.addAction(_('Destroy...'), IconStock.DELETE, self.destroyInstance)
        self.addAction(_('Remove...'), IconStock.DELETE, self.removeInstance)
        self.addAction(_('CSS Editor...'), IconStock.CSS, self.cssEditor)
        self.addAction(_('Update Modules'), IconStock.MODULE_UPDATEABLE, self.updateModules)

    def destroyInstance(self,data=None):
        pass

    def removeInstance(self,data=None):
        def execute():
            self.obj.getServer().removeInstance(self.obj)
        YesNoPage(self.getApplication().mainwin, _("Do you really want to delete this Instance?"), execute)
    
    def cssEditor(self,data=None):
        self.getApplication().mainwin.openCssEditor(self.obj)

    def updateModules(self, data=None):
        self.obj.updateModules()


class UsersARC(ActionRenderContext):
    def __init__(self, par, users):
        ActionRenderContext.__init__(self, par,users)

        self.addAction(_('Create User...'), IconStock.USER, self.createUser)

    def createUser(self,data=None):
        InputBox(self,_("What should be the name of the new User?"), self.obj.createUser,notEmpty=True)
    
class UserARC(ActionRenderContext):
    def __init__(self, par, user):
        ActionRenderContext.__init__(self, par,user)

        self.addAction(_('Delete...'), IconStock.DELETE, self.deleteUser)

    def deleteUser(self,data=None):
        def execute():
            self.obj.delete()        
        YesNoPage(self.getApplication().mainwin, _("Do you really want to delete this User?"), execute)

class ModuleARC(ActionRenderContext):
    def __init__(self, par, module):
        ActionRenderContext.__init__(self, par, module)

        self.addAction(_('Create Widget...'), IconStock.WIDGET, self.createWidget)
        self.addAction(_('CSS Editor...'), IconStock.CSS, self.cssEditor)
        if module.isUpdateable():
            self.addAction(_('Update'), IconStock.UPDATE, self.update)
    
    def createWidget(self,data=None):
        InputBox(self,_("what should be the name of the new Widget?"), self.obj.createWidget, notEmpty=True)

    def cssEditor(self,data=None):
        self.getApplication().mainwin.openCssEditor(self.obj)
    
    def update(self, data=None):
        self.obj.update()

class ModulesARC(ActionRenderContext):
    def __init__(self, par, module):
        ActionRenderContext.__init__(self, par, module)

        self.addAction(_('Refresh'), IconStock.RELOAD, self.refresh)
    
    def refresh(self,data=None):
        self.obj.refresh()
    
class WidgetARC(ActionRenderContext):
    def __init__(self, par, widget):
        ActionRenderContext.__init__(self, par, widget)

        self.addAction(_('Delete...'), IconStock.DELETE, self.deleteWidget)
        self.addAction(_('CSS Editor...'), IconStock.CSS, self.cssEditor)

    def deleteWidget(self, data=None):
        def execute():
            self.obj.delete()
        YesNoPage(self.getApplication().mainwin, _("Do you really want to delete this Widget?"), execute)

    def cssEditor(self,data=None):
        self.getApplication().mainwin.openCssEditor(self.obj)
    
class SiteARC(ActionRenderContext):
    def __init__(self, par, site):
        ActionRenderContext.__init__(self, par, site)

        self.addAction(_('Create Menu'), IconStock.MENU, self.createMenu)

    def createMenu(self, data=None):
        self.obj.createMenu()

class MenuARC(ActionRenderContext):
    def __init__(self, par, menu):
        ActionRenderContext.__init__(self, par, menu)

        self.addAction(_('Delete Menu...'), IconStock.DELETE, self.deleteMenu)

    def deleteMenu(self, data=None):
        def execute():
            self.obj.delete()
        YesNoPage(self.getApplication().mainwin, _("Do you really want to delete this Menu?"), execute)

class RolesARC(ActionRenderContext):
    def __init__(self, par, roles):
        ActionRenderContext.__init__(self, par, roles)

        self.addAction(_('Create Role...'), IconStock.ROLE, self.createRole)

    def createRole(self, data=None):
        InputBox(self,_("What should be the name of the new Widget?"), self.obj.createRole)
    
class RoleARC(ActionRenderContext):
    def __init__(self, par, role):
        ActionRenderContext.__init__(self, par, role)

        self.addAction(_('Delete Role...'), IconStock.DELETE, self.deleteRole)

    def deleteRole(self, data=None):
        def execute():
            self.obj.delete()
        YesNoPage(self.getApplication().mainwin, _("Do you really want to delete this Role?"), execute)
    
class DatabaseARC(ActionRenderContext):
    def __init__(self, par, database):
        ActionRenderContext.__init__(self, par, database)

        self.addAction(_('Register Schema...'), IconStock.SCHEMA, self.registerSchema)
        self.addAction(_('Create Schema...'), IconStock.SCHEMA, self.createSchema)

    def registerSchema(self, data=None):
        RegisterSchemaPage(self.getPar().getPar(), self.obj)

    def createSchema(self, data=None):
        NewSchemaPage(self.getPar().getPar(), self.obj)

class SchemaARC(ActionRenderContext):
    def __init__(self, par,schema):
        ActionRenderContext.__init__(self, par, schema)

        self.addAction(_('Unregister Schema...'), IconStock.DELETE, self.unregisterSchema)
        self.addAction(_('Destroy Schema...'), IconStock.DELETE, self.destroySchema)

    def unregisterSchema(self, data=None):
        def execute():
            self.obj.getPar().unregisterSchema(self.obj)
        YesNoPage(self.getApplication().mainwin, _("Do you really want to remove this Schema?"), execute)

    def destroySchema(self, data=None):
        def execute():
            self.obj.getPar().destroySchema(self.obj)
        YesNoPage(self.getApplication().mainwin, _("Do you really want to destroy this Schema?"), execute)

ARCMAP = {
                   "Server"           : ServerARC,
                   "Users"            : UsersARC,
                   "User"             : UserARC,
                   "Module"           : ModuleARC,
                   "Modules"          : ModulesARC,
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
