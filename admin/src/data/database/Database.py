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

from data.Generic import GenericScovilleObject

class Database(GenericScovilleObject):
    def __init__(self, par):
        GenericScovilleObject.__init__(self)
        self.par = par
        self.schemes = []

    def createSovilleSchema(self, rootname, rootpw):
        pass

    def deleteScovilleSchema(self):
        pass

    def updateSchemata(self):
        pass

    def getPar(self):
        return self.par
    
    def getModules(self):
        return self.getPar()
