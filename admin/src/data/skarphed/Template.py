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

import base64

from data.Generic import GenericSkarphedObject
from data.skarphed.Skarphed import rpc

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
    
    @rpc(loadCallback)
    def getCurrentTemplate(self):
        pass

    def load(self):
        self.getCurrentTemplate()
    
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
    
    @rpc(uploadCallback)
    def installTemplate(self, template_data):
        pass

    def upload(self, filepath):
        template_file = open(filepath,'r')
        templatedata = base64.b64encode(template_file.read())
        self.installTemplate(templatedata)
        template_file.close()

    def repoTemplatesCallback(self, json):
        self.data['available'] = json
        self.updated()

    @rpc(repoTemplatesCallback)
    def refreshAvailableTemplates(self):
        pass

    def getRepoTemplates(self):
        self.refreshAvailableTemplates()

    def getAvailableTemplates(self):
        return self.data['available']

    def installFromRepoCallback(self, res=None):
        self.getRepoTemplates()
        self.load()
        self.getSkarphed().getMaintenanceMode()

    @rpc(installFromRepoCallback)
    def installTemplateFromRepo(self, template_nr):
        pass

    def installFromRepo(self, nr):
        self.installTemplateFromRepo(nr)

    def getPar(self):
        return self.par
    
    def getSkarphed(self):
        return self.getPar()
    
    def getServer(self):
        return self.getPar().getServer()
