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
from data.skarphed.Skarphed import rpc

class Role(GenericSkarphedObject):
    def __init__(self,parent, data = {}):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.permissiondata = None
        self.data = data
        self.updated()
    
    def getName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return "Unknown Role"
    
    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']
        else:
            return None
    
    def fetchPermissionsCallback(self,data):
        #dragons

        self.permissiondata=data
        self.updated()
    
    @rpc(fetchPermissionsCallback)
    def getRightsForRolePage(self, roleId):
        pass

    def fetchPermissions(self):
        self.getRightsForRolePage(self.getId())
    
    def assignPermissionCallback(self,data):
        self.fetchPermissions()

    @rpc(assignPermissionCallback)
    def grantRightToRole(self, roleId, permission):
        pass
    
    def assignPermission(self,perm):
        self.grantRightToRole(self.getId(),perm)
    
    def removePermissionCallback(self,data):
        self.fetchPermissions()

    @rpc(removePermissionCallback)
    def revokeRightFromRole(self, roleId, permission):
        pass
    
    def removePermission(self,perm):
        self.revokeRightFromRole(self.getId(),perm)
    
    def deleteCallback(self,json):
        self.destroy()
    
    @rpc(deleteCallback)
    def deleteRole(self, roleId):
        pass

    def delete(self):
        self.deleteRole(self.getId())
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def getPar(self):
        return self.par
    
    def getRoles(self):
        return self.getPar()