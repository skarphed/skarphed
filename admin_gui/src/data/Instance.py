#!/usr/bin/python
#-*- coding: utf-8 -*-

from Generic import GenericScovilleObject

class Instance(GenericScovilleObject):
    def __init__(self, par):
        self.par = par
        GenericScovilleObject.__init__(self)
    def establishConnections(self):
        pass
    
class InstanceType():
    def __init__(self, typename, displayname):
        self.instanceTypeName = typename
        self.displayName = displayname