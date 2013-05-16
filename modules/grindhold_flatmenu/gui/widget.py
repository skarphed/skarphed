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

import os

from gui.ObjectCombo import ObjectCombo
from data.Generic import GenericObjectStoreException

class WidgetPage(gtk.VBox):
    HORIZONTALLY = 0
    VERTICALLY = 1

    def __init__(self, parent, widget):
        self.par = parent
        gtk.VBox.__init__(self)
        self.widgetId = widget.getLocalId()

        self._pageId = None
        self._menuId = None
        self._orientation = None

        path = os.path.realpath(__file__)
        path = path.replace("widget.pyc","")
        self._path = path.replace("widget.py","")

        self.builder = gtk.Builder()
        self.builder.add_from_file(self._path+"widget.glade")

        handlers = {'save_cb':self.saveCallback}
        self.builder.connect_signals(handlers)

        self.structure_table = self.builder.get_object("structure_table")
        self.content = self.builder.get_object("widget")
        self.page_selector = ObjectCombo(self, 
                                    "Site",
                                    selectFirst=True,
                                    virtualRootObject=widget.getModule().getModules().getScoville())
        self.menu_selector = ObjectCombo(self, 
                                    "Menu",
                                    selectFirst=True,
                                    virtualRootObject=self.page_selector.getSelected())
        self.structure_table.attach(self.page_selector,1,2,0,1, gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK,0,0)
        self.structure_table.attach(self.menu_selector,1,2,1,2, gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK,0,0)

        self.page_selector.connect("changed", self.pageChangedCallback)
        self.menu_selector.connect("changed", self.menuChangedCallback)

        self.add(self.content)
        self.loadContent()

    def render(self):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()

        page = None
        if self._pageId is not None:
            page = widget.getModule().getModules().getScoville().getSites().getSiteById(self._pageId)
            if page != self.page_selector.getSelected():
                self.page_selector.setSelected(page)
                self.menu_selector.destroy()
                self.menu_selector = ObjectCombo(self, 
                                     "Menu",
                                     selectFirst=True,
                                     virtualRootObject=page)
                self.menu_selector.connect("changed", self.menuChangedCallback)
                self.structure_table.attach(self.menu_selector,1,2,1,2)

        if self._menuId is not None:
            if page is not None:
                menu = page.getMenuById(self._menuId)
                self.menu_selector.setSelected(menu)

        if self._orientation == WidgetPage.HORIZONTALLY:
            self.builder.get_object("radio_horizontal").set_active(True)
            self.builder.get_object("radio_vertical").set_active(False)
        else:
            self.builder.get_object("radio_horizontal").set_active(False)
            self.builder.get_object("radio_vertical").set_active(True)

    def menuChangedCallback(self, widget=None, data=None):
        menu = widget.getSelected()
        if menu is not None:
            self._menuId = menu.getId()

    def pageChangedCallback(self, widget=None, data=None):
        page = widget.getSelected()
        if page is not None:
            self._pageId = page.getId()
            self.render()

    def loadContentCallback(self, data):
        self._pageId = data['pageId']
        self._menuId = data['menuId']
        self._orientation = data['orientation']
        self.render()

    def loadContent(self):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getScoville()
        self.getApplication().doRPCCall(scv, self.loadContentCallback, "executeModuleMethod", [module.getId(), "get_content", [widget.getId()]])

    def setContentCallback(self, data):
        self.loadContent()

    def saveCallback(self, widget=None, data=None):
        page = self.page_selector.getSelected()
        pageId = page.getId()
        menu = self.menu_selector.getSelected()
        menuId = menu.getId()
        
        if self.builder.get_object("radio_horizontal").get_active():
            orientation = WidgetPage.HORIZONTALLY
        else:
            orientation = WidgetPage.VERTICALLY
        
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getScoville()
        self.getApplication().doRPCCall(scv, self.setContentCallback, "executeModuleMethod", [module.getId(), "set_content", [widget.getId(), pageId, menuId, orientation]])        

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
