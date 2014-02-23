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
from data.skarphed.Skarphed import rpc

class Media(GenericSkarphedObject):
    def __init__(self, parent):
        GenericSkarphedObject.__init__(self)
        self.par = parent
        print "going to load media"
        self.loadMedia()

    def getBinaries(self):
        return self.children

    def getName(self):
        return "Media"

    def loadMediaCallback(self, data):
        print "ohai loaded"
        binaryIds = [b.getId() for b in self.children]
        for binary in data:
            if binary['id'] not in binaryIds:
                self.addChild(Binary(self, binary))
            else:
                self.getBinaryById(binary['id']).refresh(binary)
        self.updated()

    @rpc(loadMediaCallback)
    def loadMedia(self):
        pass

    def getBinaryById(self, nr):
        for binary in self.children:
            if binary.getId() == nr:
                return binary
        return None

class Binary(GenericSkarphedObject):
    def __init__(self, parent, data={}):
        GenericSkarphedObject.__init__(self)
        self.data = data

    def getData():
        """ Return actual data of binary """
        if self.data.has_key('data'):
            return self.data['data']

    def getId(self):
        if self.data.has_key('id'):
            return self.data['id']

    def getName(self):
        return self.getFilename()

    def getFilename(self):
        if self.data.has_key('filename'):
            return self.data['filename']
    
    def getMime(self):
        if self.data.has_key('mime'):
            return self.data['mime']

    def getSize(self):
        if self.data.has_key('size'):
            return self.data['size']

    def refresh(self, dataset):
        self.data = dataset



