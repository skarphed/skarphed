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

class Schema(GenericScovilleObject):
    def __init__(self, par, db_name="", db_user="", db_password=""):
        GenericScovilleObject.__init__(self)
        self.par = par
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def getName(self):
        return self.db_name

    def getUser(self):
        return self.db_user

    def getPassword(self):
        return self.db_password

    def getPar(self):
        return self.par
    
    def getDatabase(self):
        return self.getPar()
