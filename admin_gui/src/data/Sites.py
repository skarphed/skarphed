#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

from Site import Site

class Sites(GenericScovilleObject):
    def __init__(self,parent):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.updated()
        self.refresh()
    
    def refreshCallback(self,data):
        siteIds = [s.getId() for s in self.children]
        for site in data:
            if site['id'] not in siteIds:
                self.addChild(Site(self,site))
            else:
                self.getSiteById(site['id']).refresh(site)                
    
    def getSiteById(self,id):
        for site in self.children:
            if site.getId() == id:
                return site
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getServer(),self.refreshCallback, "getSites")
    
    def getName(self):
        return "Sites"
    
    def getPar(self):
        return self.par
    
    def getServer(self):
        return self.getPar()