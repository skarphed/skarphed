#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

import json

class User(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
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
        # HERE BE DRAGONS
        data = json.JSONDecoder().decode(data)
        self.permissiondata = data
        self.updated()
    
    def fetchRightsData(self):
        self.getApplication().doRPCCall(self.getUsers().getServer(),
                                      self.fetchRightsDataCallback,
                                      "getRightsForUserPage",
                                      [self.getName()]
                                      )
    
    def fetchRoleDataCallback(self,data):
        # HERE BE DRAGONS
        data = json.JSONDecoder().decode(data)
        self.roledata = data
        self.updated()
    
    def fetchRoleData(self):
        self.getApplication().doRPCCall(self.getUsers().getServer(),
                                      self.fetchRoleDataCallback,
                                      "getRolesForUserPage",
                                      [self.getName()]
                                      )
    
    def assignRoleCallback(self,data):
        self.fetchRoleData()
    
    def assignRole(self,role):
        self.getApplication().doRPCCall(self.getUsers().getServer(),
                                      self.assignRoleCallback,
                                      "assignRoleToUser",
                                      [self.getName(),role]
                                      )
    
    def removeRoleCallback(self,data):
        self.fetchRoleData()
    
    def removeRole(self,role):
        self.getApplication().doRPCCall(self.getUsers().getServer(),
                                      self.removeRoleCallback,
                                      "revokeRoleFromUser",
                                      [self.getName(),role]
                                      )
    
    def assignPermissionCallback(self,data):
        self.fetchRightsData()
    
    def assignPermission(self,right):
        self.getApplication().doRPCCall(self.getUsers().getServer(),
                                      self.assignPermissionCallback,
                                      "grantRightToUser",
                                      [self.getName(),right]
                                      )
    
    def removePermissionCallback(self,data):
        self.fetchRightsData()
    
    def removePermission(self,role):
        self.getApplication().doRPCCall(self.getUsers().getServer(),
                                      self.removePermissionCallback,
                                      "revokeRightFromUser",
                                      [self.getName(),role]
                                      )
    
    
    def getPar(self):
        return self.par
    
    def getUsers(self):
        return self.getPar()