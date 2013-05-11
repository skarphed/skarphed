#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Scoville.
#
# Scoville is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Scoville is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Scoville. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

from data.Generic import GenericScovilleObject

class Template(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.data['available'] = []
        self.getRepoTemplates()
        self.updated()
    
    def getName(self):
        return "Templates"
    
    def refresh(self,data):
        self.data.update(data)
        self.getScoville().getSites().refresh()
        self.getScoville().getViews().refresh()
        self.getRepoTemplates()
        self.updated()
    
    def repoTemplatesCallback(self, json):
        self.data['available'] = json
        self.updated()

    def getRepoTemplates(self):
        self.getApplication().doRPCCall(self.getScoville(),self.repoTemplatesCallback, "refreshAvailableTemplates")

    def getAvailableTemplates(self):
        return self.data['available']

    def installFromRepoCallback(self, res=None):
        self.getRepoTemplates()
        self.getScoville().loadTemplate()

    def installFromRepo(self, nr):
        self.getApplication().doRPCCall(self.getScoville(),self.installFromRepoCallback, "installTemplateFromRepo", [nr])

    def getPar(self):
        return self.par
    
    def getScoville(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()