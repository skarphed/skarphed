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


from skarphedadmin.data.Generic import GenericSkarphedObject
from skarphedadmin.data.skarphed.Skarphed import rpc


class User(GenericSkarphedObject):
    def __init__(self,parent, data = {}):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.data = data
        self.roledata = None
        self.permissiondata = None
        self.updated()
    
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return "Unknown User"
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None
        
    def fetchRightsDataCallback(self,data):
        self.permissiondata = data
        self.updated()
    
    @rpc(fetchRightsDataCallback)
    def getRightsForUserPage(self, userId):
        pass

    def fetchRightsData(self):
        self.getRightsForUserPage(self.getId())
    
    def fetchRoleDataCallback(self,data):
        self.roledata = data
        self.updated()

    @rpc(fetchRoleDataCallback)
    def getRolesForUserPage(self, username):
        #TODO: Fetch rights with id instead of name
        pass
    
    def fetchRoleData(self):
        self.getRolesForUserPage(self.getName())
    
    def assignRoleCallback(self,data):
        self.fetchRightsData()
        self.fetchRoleData()

    @rpc(assignRoleCallback)
    def assignRoleToUser(self, username, role):
        #TODO: Fetch rights with id instead of name
        pass
    
    def assignRole(self,role):
        self.assignRoleToUser(self.getName(),role)
    
    def removeRoleCallback(self,data):
        self.fetchRightsData()
        self.fetchRoleData()
    
    @rpc(removeRoleCallback)
    def revokeRoleFromUser(self, username, role):
        #TODO: Fetch rights with id instead of name
        pass

    def removeRole(self,role):
        self.revokeRoleFromUser(self.getName(),role)
    
    def changePermissionCallback(self,data):
        self.fetchRightsData()
    
    @rpc(changePermissionCallback)
    def grantRightToUser(self, userId, permission):
        pass

    def assignPermission(self,right):
        self.grantRightToUser(self.getId(),right)

    @rpc(changePermissionCallback)
    def revokeRightFromUser(self, userId, permission):
        pass

    def removePermission(self,permission):
        self.revokeRightFromUser(self.getId(),permission)

    def deleteCallback(self,json):
        self.destroy()
    
    @rpc(deleteCallback)
    def deleteUser(self, userId):
        pass

    def delete(self):
        self.deleteUser(self.getId())

    def changePasswordCallback(self, json):
        return True
    
    @rpc(changePasswordCallback)
    def alterPassword(self, userId, newPassword, oldPassword):
        pass

    def changePassword(self, new_password, old_password=None):
        self.alterPassword(self.getId(), new_password, old_password)

    def getPar(self):
        return self.par
    
    def getUsers(self):
        return self.getPar()
