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

class Repository(GenericScovilleObject):
    def __init__(self,parent,host,port,name, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.host = host
        if port is not None:
            self.port = port
        else:
            self.port = 80
        self.name = name
        self.updated()
    
    def getName(self):
        if self.host is not None and self.name is not None:
            return self.name+" ["+self.host+"]"
        elif self.host is not None:
            return "Repository ["+self.host+"]"
        else:
            return "(No Repository)"
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def getURL(self):
        if self.host is not None and self.port is not None:
            return self.host+":"+str(self.port)
        else:
            return ""
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()