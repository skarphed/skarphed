#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import base64

from data.Generic import GenericSkarphedObject

class Template(GenericSkarphedObject):
    def __init__(self,parent, data = {}):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        self.data = data
        self.data['available'] = []
        self.getRepoTemplates()
        self.load()
    
    def getName(self):
        return "Templates"
    
    def refresh(self,data):
        self.data.update(data)
        self.getSkarphed().getSites().refresh()
        self.getSkarphed().getViews().refresh()
        self.getRepoTemplates()
        self.updated()

    def loadCallback(self,res):
        self.refresh(res)
    
    def load(self):
        self.getApplication().doRPCCall(self.getSkarphed(),self.loadCallback, "getCurrentTemplate")
    
    def uploadCallback(self,res):
        severe_error_happened = False
        for error in res:
            if error['severity'] > 0:
                severe_error_happened = True
                break
        #TODO: SOMEHOW DISPLAY ERRORLOG
        if not severe_error_happened:
            self.load()
            self.getSkarphed().getMaintenanceMode()
    
    def upload(self, filepath):
        template_file = open(filepath,'r')
        templatedata = base64.b64encode(template_file.read())
        self.getApplication().doRPCCall(self.getSkarphed(),self.uploadCallback, "installTemplate", [templatedata])
        template_file.close()

    def repoTemplatesCallback(self, json):
        self.data['available'] = json
        self.updated()

    def getRepoTemplates(self):
        self.getApplication().doRPCCall(self.getSkarphed(),self.repoTemplatesCallback, "refreshAvailableTemplates")

    def getAvailableTemplates(self):
        return self.data['available']

    def installFromRepoCallback(self, res=None):
        self.getRepoTemplates()
        self.load()
        self.getSkarphed().getMaintenanceMode()

    def installFromRepo(self, nr):
        self.getApplication().doRPCCall(self.getSkarphed(),self.installFromRepoCallback, "installTemplateFromRepo", [nr])

    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()