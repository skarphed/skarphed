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

from data.Generic import GenericObjectStoreException

class WidgetPage(gtk.VBox):
    def __init__(self, parent, widget):
        self.par = parent
        gtk.VBox.__init__(self)
        self.widgetId = widget.getLocalId()

        self._title = None
        self._html = None

        path = os.path.realpath(__file__)
        path = path.replace("widget.pyc","")
        self._path = path.replace("widget.py","")

        self.builder = gtk.Builder()
        self.builder.add_from_file(self._path+"widget.glade")

        handlers = {'save_cb':self.saveCallback}
        self.builder.connect_signals(handlers)

        self.content = self.builder.get_object("widget")
        self.add(self.content)
        self.loadContent()

    def render(self):
        buff = self.builder.get_object("html_buffer")
        buff.set_text(self._html)
        title_entry = self.builder.get_object("title_entry")
        title_entry.set_text(self._title)

    def loadContentCallback(self, data):
        self._html = data['html']
        self._title = data['title']
        self.render()

    def loadContent(self):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException, e:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getSkarphed()
        scv.doRPCCall(self.loadContentCallback, "executeModuleMethod", [module.getId(), "get_content", [widget.getId()]])

    def setContentCallback(self, data):
        self.loadContent()

    def saveCallback(self, widget=None, data=None):
        buff = self.builder.get_object("html_buffer")
        html = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        title_entry = self.builder.get_object("title_entry")
        title = title_entry.get_text()
        
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException, e:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getSkarphed()
        scv.doRPCCall(self.setContentCallback, "executeModuleMethod", [module.getId(), "set_content", [widget.getId(), html, title]])        

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
