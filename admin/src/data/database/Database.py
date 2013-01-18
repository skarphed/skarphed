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

from hashlib import sha512
from random import randrange

from threading import Thread

import gobject

class Database(GenericScovilleObject):
    class GenerateSchemaThread(Thread):
        def __init__(self, database, name):           
            Thread.__init__(self)
            self.database = database
            self.name = name

        def run(self):
            self.database.executeCreateSchema(self.name)

    def __init__(self, par, url="", dba_user="", dba_password=""):
        GenericScovilleObject.__init__(self)
        self.par = par
        self.instanceTypeName = "database"
        self.displayName = "Database"
        self.dba_user = dba_user
        self.dba_password = dba_password

    def createSchema(self,name):
        self.GenerateSchemaThread(self,name).start()

    def executeCreateSchema(self, name):
        username = self._generateRandomString(8)
        password = self._generateRandomString(8)

        schemaroot_pw , schemaroot_salt = self.generateSaltedPassword('root')

        con = self.getServer().getSSH()

        sql = open("../installer/_database/scvdb.sql","r").read()
        sql = sql%{'USER':username,'PASSWORD':schemaroot_pw, 'SALT':schemaroot_salt, 'NAME':name}

        #HERE BE DRAGONS
        command = """echo "add %(user)s -pw %(pass)s" | gsec -user %(user_dba)s -pass %(pass_dba)s ;
                                                       cd /var/lib/firebird/2.5/data ;
                                                       echo "%(sql)s" | isql-fb -user %(user)s -password %(pass)s
                                                                                   """%{'user': username,
                                                                                        'pass':password,
                                                                                        'user_dba':self.dba_user,
                                                                                        'pass_dba':self.dba_password,
                                                                                        'sql':sql}
        con_in, con_out, conn_err = con.exec_command(command)

        schema = Schema(self, name, username, password)
        self.children.append(schema)
        self.installFinished = True
        gobject.idle_add(self.updated)

    def registerSchema(self, name, user, password):
        schema = Schema(self,name,user,password)
        self.children.append(schema)
        self.updated()

    def establishConnections(self):
        pass 

    def destroySchema(self,schema):
        con = self.getServer().getSSH()
        command ="""cd /var/lib/firebird/2.5/data ; 
                    echo "CONNECT '%(name)s.fdb'; DROP DATABASE;" | isql-fb -user %(user_dba)s -pass %(pass_dba)s ;
                    echo "del %(user)s" | gsec -user %(user_dba)s -pass %(pass_dba)s """%{'name':schema.db_name,
                                                                                    'user_dba':self.dba_user,
                                                                                    'pass_dba':self.dba_password,
                                                                                    'user':schema.db_user }
        con_in, con_out, con_err = con.exec_command(command)
        self.unregisterSchema(schema)

    def unregisterSchema(self, schema):
        self.children.remove(schema)
        schema.destroy()
        self.updated()

    def updateSchemata(self):
        con = self.getServer().getSSH()


    def generateSaltedPassword(self, password):
        salt = self._generateRandomString(128)
        pw = "root"
        h = sha512()
        h.update(pw+salt)
        pw = h.hexdigest()
        return (pw, salt)

    def _generateRandomString(self,length):
        ret = ""
        for i in range(length):
            x = -1
            while x in (-1,91,92,93,94,95,96,60,61,62,58,59,63,64):
                x = randrange(48,123)
            ret+=chr(x)
        return ret

    def getUsername(self):
        return self.dba_user

    def getPassword(self):
        return self.dba_password

    def setUsername(self,username):
        self.dba_user = username

    def setPassword(self,password):
        self.dba_password = password

    def getSchemas(self):
        return self.children

    def getPar(self):
        return self.par

    def getName(self):
        return "Firebird 2.5 Database"
    
    def getServer(self):
        return self.getPar()
