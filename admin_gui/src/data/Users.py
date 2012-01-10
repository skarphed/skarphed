#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

from User import User

class Users(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.users = []
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        userIds = [u.getUserId() for u in self.users]
        for user in data:
            if user['id'] not in userIds:
                self.users.append(User(self,user))
            else:
                self.getUserById(user['id']).refresh(user)
                
    def getUserById(self,id):
        for u in self.users:
            if u.getUserId() == id:
                return u
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getServer(),self.refreshCallback, "getUsers")
    
    def getName(self):
        return "Users"
    
    def getPar(self):
        return self.par
    
    def getServer(self):
        return self.getPar()