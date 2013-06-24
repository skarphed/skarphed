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

class ModulePage(gtk.VBox):
    def __init__(self, parent, module):
        self.par = parent
        gtk.VBox.__init__(self)
        self.moduleId = module.getLocalId()

        path = os.path.realpath(__file__)
        path = path.replace("module.pyc","")
        self._path = path.replace("module.py","")

        self.builder = gtk.Builder()
        self.builder.add_from_file(self._path+"module.glade")

        self.content = self.builder.get_object("module")
        self.add(self.content)

    def render(self):
        pass

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()