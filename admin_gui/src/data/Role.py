#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

import json

class Role(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
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
        data = json.JSONDecoder().decode(data)
        self.permissiondata=data
        self.updated()
    
    def fetchPermissions(self):
        self.getApplication().doRPCCall(self.getRoles().getServer(),self.fetchPermissionsCallback, "getRightsForRolePage", [self.getId()])
    
    def assignPermissionCallback(self,data):
        self.fetchPermissions()
    
    def assignPermission(self,perm):
        self.getApplication().doRPCCall(self.getRoles().getServer(),self.assignPermissionCallback, "grantRightToRole", [self.getId(),perm])
    
    def removePermissionCallback(self,data):
        self.fetchPermissions()
    
    def removePermission(self,perm):
        self.getApplication().doRPCCall(self.getRoles().getServer(),self.removePermissionCallback, "revokeRightFromRole", [self.getId(),perm])
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def getPar(self):
        return self.par
    
    def getRoles(self):
        return self.getPar()