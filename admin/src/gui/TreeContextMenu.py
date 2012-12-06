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


import pygtk
pygtk.require("2.0")
import gtk

import IconStock

from ServerPropertyWindow import ServerPropertyWindow
from NewScoville import NewScoville
from InputBox import InputBox

class TreeContextMenu(gtk.Menu):
    def __init__(self,parent):
        gtk.Menu.__init__(self)

        self.par = parent
        self.concernedIter = None

        removeServerI = gtk.Image()
        removeServerI.set_from_pixbuf(IconStock.DELETE)
        self.removeServer = gtk.ImageMenuItem()
        self.removeServer.set_image(removeServerI)
        gtk.MenuItem.__init__(self.removeServer,"Remove Server")
        self.append(self.removeServer)
        self.removeServer.connect("activate",self.cb_removeServer)
        
        
        connectServerI = gtk.Image()
        connectServerI.set_from_pixbuf(IconStock.SCOVILLE)
        self.connectServer = gtk.ImageMenuItem()
        self.connectServer.set_image(connectServerI)
        gtk.MenuItem.__init__(self.connectServer,"Attempt Connection")
        self.append(self.connectServer)
        self.connectServer.connect("activate", self.cb_connectServer)
        
        propertiesI = gtk.Image()
        propertiesI.set_from_pixbuf(IconStock.SCOVILLE)
        self.properties = gtk.ImageMenuItem()
        self.properties.set_image(propertiesI)
        gtk.MenuItem.__init__(self.properties, "Properties...")
        self.append(self.properties)
        self.properties.connect("activate", self.cb_Properties)
        
        cssEditorI = gtk.Image()
        cssEditorI.set_from_pixbuf(IconStock.CSS)
        self.cssEditor = gtk.ImageMenuItem()
        self.cssEditor.set_image(cssEditorI)
        gtk.MenuItem.__init__(self.cssEditor, "CSS-editor")
        self.append(self.cssEditor)
        self.cssEditor.connect("activate", self.cb_cssEditor)
        
        deleteUserI = gtk.Image()
        deleteUserI.set_from_pixbuf(IconStock.DELETE)
        self.deleteUser = gtk.ImageMenuItem()
        self.deleteUser.set_image(deleteUserI)
        gtk.MenuItem.__init__(self.deleteUser, "Delete")
        self.append(self.deleteUser)
        self.deleteUser.connect("activate", self.cb_deleteUser)
        
        createUserI = gtk.Image()
        createUserI.set_from_pixbuf(IconStock.USER)
        self.createUser = gtk.ImageMenuItem()
        self.createUser.set_image(createUserI)
        gtk.MenuItem.__init__(self.createUser, "Create User")
        self.append(self.createUser)
        self.createUser.connect("activate", self.cb_createUser)
        
        createInstanceI = gtk.Image()
        createInstanceI.set_from_pixbuf(IconStock.SCOVILLE)
        self.createInstance = gtk.ImageMenuItem()
        self.createInstance.set_image(createInstanceI)
        gtk.MenuItem.__init__(self.createInstance,"Create Instance")
        self.append(self.createInstance)
        self.createInstance.connect("activate",self.cb_createInstance)

        destroyInstanceI = gtk.Image()
        destroyInstanceI.set_from_pixbuf(IconStock.DELETE)
        self.destroyInstance = gtk.ImageMenuItem()
        self.destroyInstance.set_image(destroyInstanceI)
        gtk.MenuItem.__init__(self.destroyInstance,"Create Instance")
        self.append(self.destroyInstance)
        self.destroyInstance.connect("activate",self.cb_destroyInstance)

        removeInstanceI = gtk.Image()
        removeInstanceI.set_from_pixbuf(IconStock.DELETE)
        self.removeInstance = gtk.ImageMenuItem()
        self.removeInstance.set_image(removeInstanceI)
        gtk.MenuItem.__init__(self.removeInstance,"Remove Instance")
        self.append(self.removeInstance)
        self.removeInstance.connect("activate",self.cb_removeInstance)
        
        createWidgetI = gtk.Image()
        createWidgetI.set_from_pixbuf(IconStock.WIDGET)
        self.createWidget = gtk.ImageMenuItem()
        self.createWidget.set_image(createWidgetI)
        gtk.MenuItem.__init__(self.createWidget,"Create Widget")
        self.append(self.createWidget)
        self.createWidget.connect("activate",self.cb_createWidget)
        
        deleteWidgetI = gtk.Image()
        deleteWidgetI.set_from_pixbuf(IconStock.WIDGET)
        self.deleteWidget = gtk.ImageMenuItem()
        self.deleteWidget.set_image(deleteWidgetI)
        gtk.MenuItem.__init__(self.deleteWidget,"Delete Widget")
        self.append(self.deleteWidget)
        self.deleteWidget.connect("activate",self.cb_deleteWidget)
        
        createMenuI = gtk.Image()
        createMenuI.set_from_pixbuf(IconStock.MENU)
        self.createMenu = gtk.ImageMenuItem()
        self.createMenu.set_image(createMenuI)
        gtk.MenuItem.__init__(self.createMenu,"Create Menu")
        self.append(self.createMenu)
        self.createMenu.connect("activate",self.cb_createMenu)
        
        deleteMenuI = gtk.Image()
        deleteMenuI.set_from_pixbuf(IconStock.MENU)
        self.deleteMenu = gtk.ImageMenuItem()
        self.deleteMenu.set_image(deleteMenuI)
        gtk.MenuItem.__init__(self.deleteMenu,"Delete Menu")
        self.append(self.deleteMenu)
        self.deleteMenu.connect("activate",self.cb_deleteMenu)
        
        createRoleI = gtk.Image()
        createRoleI.set_from_pixbuf(IconStock.ROLE)
        self.createRole = gtk.ImageMenuItem()
        self.createRole.set_image(createRoleI)
        gtk.MenuItem.__init__(self.createRole,"Create Role")
        self.append(self.createRole)
        self.createRole.connect("activate",self.cb_createRole)
        
        deleteRoleI = gtk.Image()
        deleteRoleI.set_from_pixbuf(IconStock.ROLE)
        self.deleteRole = gtk.ImageMenuItem()
        self.deleteRole.set_image(deleteRoleI)
        gtk.MenuItem.__init__(self.deleteRole,"Delete Role")
        self.append(self.deleteRole)
        self.deleteRole.connect("activate",self.cb_deleteRole)
        
        updateModulesI = gtk.Image()
        updateModulesI.set_from_pixbuf(IconStock.MODULE_UPDATEABLE)
        self.updateModules = gtk.ImageMenuItem()
        self.updateModules.set_image(updateModulesI)
        gtk.MenuItem.__init__(self.updateModules,"Update Modules")
        self.append(self.updateModules)
        self.updateModules.connect("activate",self.cb_updateModules)
        
        self.show_all()
        
    def hide_buttons(self):
        for element in self.get_children():
            element.set_visible(False)
        
    def cb_removeServer(self,data=None):
        self.currentObject.destroy()
  
    def cb_connectServer(self,data=None):
        self.currentObject.establishConnections()
        
    def cb_Properties(self,data=None):
        if self.currentObject.__class__.__name__ == "Server":
            ServerPropertyWindow(self.getPar().getPar(),server=self.currentObject)
    
    def cb_createInstance(self,data=None):
        if self.currentObject.__class__.__name__ == "Server":
            NewScoville(self.getPar().getPar(),server=self.currentObject)

    def cb_destroyInstance(self,data=None):
        pass

    def cb_removeInstance(self,data=None):
        self.currentObject.getServer().removeInstance(self.currentObject)
    
    def cb_cssEditor(self,data=None):
        cn = self.currentObject.__class__.__name__
        if cn in ("Server", "Module",  "Widget"):
            self.getApplication().mainwin.openCssEditor(self.currentObject)
    
    def cb_createUser(self,data=None):
        InputBox(self,"what should be the name of the new User?", self.currentObject.createUser)
    
    def cb_deleteUser(self,data=None):
        self.currentObject.delete()        
    
    def cb_createWidget(self,data=None):
        InputBox(self,"what should be the name of the new Widget?", self.currentObject.createWidget)
    
    def cb_deleteWidget(self, data=None):
        self.currentObject.delete()
    
    def cb_createMenu(self, data=None):
        self.currentObject.createMenu()
        
    def cb_deleteMenu(self, data=None):
        self.currentObject.delete()
        
    def cb_createRole(self, data=None):
        InputBox(self,"what should be the name of the new Widget?", self.currentObject.createRole)
    
    def cb_deleteRole(self, data=None):
        self.currentObject.delete()
    
    def cb_updateModules(self, data=None):
        self.currentObject.updateModules()
    
    def popup(self,obj,button,time):
        self.hide_buttons()
        itemtype = obj.__class__.__name__
        if itemtype == "Server":
            self.removeServer.set_visible(True)
            self.connectServer.set_visible(True)
            self.properties.set_visible(True)
            self.createInstance.set_visible(True)
            self.cssEditor.set_visible(True)
            self.connectServer.set_sensitive(not obj.isOnline())
        elif itemtype == "Module":
            self.cssEditor.set_visible(True)
            self.createWidget.set_visible(True)
        elif itemtype == "Widget":
            self.cssEditor.set_visible(True)
            self.deleteWidget.set_visible(True)
        elif itemtype == "GenericScovilleObject":
            pass
        elif itemtype == "User":
            self.deleteUser.set_visible(True)
        elif itemtype == "Users":
            self.createUser.set_visible(True)
        elif itemtype == "Role":
            self.deleteRole.set_visible(True)
        elif itemtype == "Roles":
            self.createRole.set_visible(True)
        elif itemtype == "Scoville": # HERE BE DRAGONS
            self.removeInstance.set_visible(True)
            self.destroyInstance.set_visible(True)
            self.updateModules.set_visible(True)
        elif itemtype == "Site":
            self.createMenu.set_visible(True)
        elif itemtype == "Menu":
            self.deleteMenu.set_visible(True)
        else: 
            return
        self.currentObject = obj
        gtk.Menu.popup(self,None,None,None,button,time,None)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()