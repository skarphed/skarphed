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


from Generic import GenericScovilleObject

class Instance(GenericScovilleObject):
    def __init__(self, par):
        self.par = par
        self.instanceTypeName = None
        self.displayName = None
        GenericScovilleObject.__init__(self)
    def establishConnections(self):
        pass
    def setUrl(self):
        pass
    def getUrl(self):
        pass
    
class InstanceType():
    def __init__(self, typename, displayname):
        self.instanceTypeName = typename
        self.displayName = displayname