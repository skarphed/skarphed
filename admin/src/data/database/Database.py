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
from data.database.Schema import Schema

class Database(GenericScovilleObject):
    def __init__(self, par, dba_user="", dba_password=""):
        GenericScovilleObject.__init__(self)
        self.par = par
        self.schemes = []
        self.dba_user = dba_user
        self.dba_password = dba_password

    def createSchema(self, name):
        username = "ABCDEFGH"
        password = "abcdefgh"
        con = self.getServer().getSSH()
        # Threadauslagerung
        con_in, con_out, conn_err = con.exec_comand("gsec -user %s -pass %s add -username %s -password %s"%(self.dba_user,
                                                                                        self.dba_password,
                                                                                        name))
        schema = Schema(self, username, password)
        self.schemes.append(schema)

    def deleteSchema(self):
        con = self.getServer().getSSH()

    def updateSchemata(self):
        con = self.getServer().getSSH()

    def getPar(self):
        return self.par

    def getName(self):
        return "Firebird 2.5 Database"
    
    def getServer(self):
        return self.getPar()
