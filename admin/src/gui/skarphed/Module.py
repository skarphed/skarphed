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
from GenericObject import ObjectPageAbstract

import pygtk
pygtk.require("2.0")
import gtk

from glue.lng import _
from glue.paths import MODULEGUI

class ModulePage(ObjectPageAbstract):
    def __init__(self,par,module):
        ObjectPageAbstract.__init__(self, par, module)

        self.moduleGuiLoaded = False

        self.label = gtk.Label(_("Wait a Second. Loading GUI"))
        self.add(self.label)

        if not module.isGuiAvailable():
            module.loadGui()
        if not MODULEGUI in sys.path:
            sys.path.append(MODULEGUI)

        self.render()

    def render(self):
        module = self.getMyObject()
        if not module:
            return

        if module.isGuiAvailable() and not self.moduleGuiLoaded:
            self.label.destroy()
            
            exec "from %s.%s.module import ModulePage as ImplementedModulePage"%(module.getModuleName(),
                                                                            module.getVersionFolderString())
            modulePage = ImplementedModulePage(self, module)
            self.add(modulePage)
            self.show_all()
            self.moduleGuiLoaded = True
