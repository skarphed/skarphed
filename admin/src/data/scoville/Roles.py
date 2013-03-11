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

from Role import Role

class Roles(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        roleIds = [r.getId() for r in self.children]
        for role in data:
            if role['id'] not in roleIds:
                self.addChild(Role(self,role))
            else:
                self.getRoleById(role['id']).refresh(role)
                
    
    def getRoleById(self,id):
        for role in self.children:
            if role.getId() == id:
                return role
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getScoville(),self.refreshCallback, "getRoles")
    
    def getName(self):
        return "Roles"
    
    def createRoleCallback(self,json):
        self.refresh()
    
    def createRole(self,name):
        self.getApplication().doRPCCall(self.getScoville(),self.createRoleCallback, "createRole", [{'name':name}])
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()