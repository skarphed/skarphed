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


from data.Generic import GenericSkarphedObject

from User import User

class Users(GenericSkarphedObject):
    def __init__(self,parent):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        userIds = [u.getId() for u in self.children]
        for user in data:
            if user['id'] not in userIds:
                self.addChild(User(self,user))
            else:
                self.getUserById(user['id']).refresh(user)
                
    def getUserById(self,userId):
        for u in self.children:
            if u.getId() == userId:
                return u
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getSkarphed(),self.refreshCallback, "getUsers")
    
    def getName(self):
        return "Users"
    
    def createUserCallback(self,json):
        self.refresh()
    
    def createUser(self,name):
        self.getApplication().doRPCCall(self.getSkarphed(),self.createUserCallback, "createUser", [name,"default"])
    
    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()