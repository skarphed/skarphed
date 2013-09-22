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

import pygtk
pygtk.require("2.0")
import gtk

import os

from gui.ObjectCombo import ObjectCombo
from data.Generic import GenericObjectStoreException

from data.skarphed.Skarphed import module_rpc

class WidgetPage(gtk.VBox):
    HORIZONTALLY = 0
    VERTICALLY = 1

    def __init__(self, parent, widget):
        self.par = parent
        gtk.VBox.__init__(self)
        self.widgetId = widget.getLocalId()

        self._menuId = None

        path = os.path.realpath(__file__)
        path = path.replace("widget.pyc","")
        self._path = path.replace("widget.py","")

        self.builder = gtk.Builder()
        self.builder.add_from_file(self._path+"widget.glade")

        handlers = {'save_cb':self.saveCallback}
        self.builder.connect_signals(handlers)

        self.structure_table = self.builder.get_object("structure_table")
        self.content = self.builder.get_object("widget")
        self.menu_selector = ObjectCombo(self, 
                                    "Menu",
                                    selectFirst=True,
                                    virtualRootObject=widget.getModule().getModules().getSkarphed().getSites())
        self.structure_table.attach(self.menu_selector,1,2,1,2, gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK,0,0)

        self.menu_selector.connect("changed", self.menuChangedCallback)

        self.add(self.content)
        self.loadContent()

    def render(self):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()

        if self._menuId is not None:
            pages = widget.getModule().getModules().getSkarphed().getSites()    
            menu = pages.getMenuById(self._menuId)
            self.menu_selector.setSelected(menu)

    def menuChangedCallback(self, widget=None, data=None):
        menu = widget.getSelected()
        if menu is not None:
            self._menuId = menu.getId()

    def loadContentCallback(self, data):
        self._menuId = data['menuId']
        self.render()

    @module_rpc(loadContentCallback)
    def get_content(self):
        pass

    def loadContent(self):
        self.get_content()

    def setContentCallback(self, data):
        self.loadContent()

    @module_rpc(setContentCallback)
    def set_content(self, menuId):
        pass

    def saveCallback(self, widget=None, data=None):
        menu = self.menu_selector.getSelected()
        menuId = menu.getId()
        
        self.set_content(menuId)        

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
