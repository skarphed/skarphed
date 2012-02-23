#!/usr/bin/python
#-*- coding: utf-8 -*-

from data.Generic import GenericScovilleObject

from User import User

class Users(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        userIds = [u.getUserId() for u in self.children]
        for user in data:
            if user['id'] not in userIds:
                self.addChild(User(self,user))
            else:
                self.getUserById(user['id']).refresh(user)
                
    def getUserById(self,userId):
        for u in self.children:
            if u.getUserId() == userId:
                return u
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getScoville(),self.refreshCallback, "getUsers")
    
    def getName(self):
        return "Users"
    
    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()