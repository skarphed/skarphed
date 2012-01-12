#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

from Role import Role
import json


class Roles(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        data = json.JSONDecoder().decode(data)
        roleIds = [r.getId() for r in self.children]
        for role in data:
            if role['id'] not in roleIds:
                self.addChild(Role(self,role))
            else:
                self.getRoleByName(role['id']).refresh(role)
                
    
    def getRoleById(self,id):
        for role in self.children:
            if role.getId() == id:
                return role
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getServer(),self.refreshCallback, "getRoles")
    
    def getName(self):
        return "Roles"
    
    def getPar(self):
        return self.par
    
    def getServer(self):
        return self.getPar()