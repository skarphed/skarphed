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

from Site import Site

class Sites(GenericSkarphedObject):
    def __init__(self,parent):
        GenericSkarphedObject.__init__(self)
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

    def getMenuById(self,nr):
        for site in self.children:
            menu = site.getMenuById(nr)
            if menu is not None:
                return menu
        return None
    
    def refresh(self):
        self.getApplication().doRPCCall(self.getSkarphed(),self.refreshCallback, "getSites")
    
    def getSites(self):
        return self.children
    
    def getName(self):
        return "Sites"
    
    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()