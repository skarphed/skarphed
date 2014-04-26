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

import sys
import os
from GenericObject import ObjectPageAbstract
from skarphedadmin.data.Generic import GenericObjectStoreException

import pygtk
pygtk.require("2.0")
import gtk

from skarphedadmin.glue.lng import _

class WidgetPage(ObjectPageAbstract):
    def __init__(self,par,widget):
        ObjectPageAbstract.__init__(self, par, widget)

        self.widgetGuiLoaded = False

        self.label = gtk.Label(_("Wait a Second. Loading GUI"))
        self.add(self.label)

        module = widget.getModule()
        
        if not module.isGuiAvailable():
            module.addCallback(self.render)
            module.loadGui()
        if not os.path.expanduser("~/.skarphedadmin/modulegui") in sys.path:
            sys.path.append(os.path.expanduser("~/.skarphedadmin/modulegui"))

        self.render()

    def render(self):
        widget = self.getMyObject()
        if not widget:
            return

        module = widget.getModule()

        if module.isGuiAvailable() and not self.widgetGuiLoaded:
            module.removeCallback(self.render)
            self.label.destroy()
            
            exec "from %s.%s.widget import WidgetPage as ImplementedWidgetPage"%(module.getModuleName(),
                                                                            module.getVersionFolderString())
            widgetPage = ImplementedWidgetPage(self, widget)
            self.add(widgetPage)
            self.show_all()
            self.widgetGuiLoaded = True
