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

import os
from StringIO import StringIO
from hashlib import sha512
from random import randrange

from module import AbstractModule

class ModuleException(Exception): 
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used""",
        1:"""Need initialized password hash and salt to verify Password!"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "DB_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class Module(AbstractModule):
    def __init__(self, core):
        AbstractModule.__init__(self,core)
        self._path = os.path.dirname(__file__)
        self._load_manifest()

        """
        BEGIN IMPLEMENTING YOUR MODULE HERE
        """
        User.init(self._core,self)


class User(object):
    @classmethod
    def init(cls, core, module):
        cls._core = core
        cls._module = module

    @classmethod
    def create_user(cls, username, password):
        user = User(cls._core, cls._module)
        user.set_name(username)
        user.alter_password(password)
        user.store()
        return user

    @classmethod
    def get_user(cls, nr):
        db = cls._core.get_db()
        stmnt = "SELECT PUS_NICK, PUS_EMAIL, PUS_PASSWORD, PUS_SALT FROM ${users} WHERE PUS_ID = ? ;"
        cur = db.query(cls._module, stmnt, (int(nr),))
        row = cur.fetchonemap()
        if row is None:
            return None
        else:
            user = User()
            user.set_id(nr)
            user.set_name(row["PUS_NICK"])
            user.set_email(row["PUS_EMAIL"])
            user.set_password(row["PUS_PASSWORD"])
            user.set_salt(row["PUS_SALT"])
            return user

    def __init__(self, core, module):
        self._module = module
        self._core = core
        self._id = None
        self._name = None
        self._email = None
        self._password = None
        self._salt = None

    def set_id(self,nr):
        self._id = int(nr)

    def get_id(self):
        return self._id

    def set_name(self, name):
        self._name = str(name)

    def get_name(self):
        return self._name

    def set_email(self, email):
        self._email = email

    def get_email(self):
        return self._email

    def alter_password(self, password):
        pw, salt = self._generateSaltedPassword(password)
        self._password = pw
        self._salt = salt

    def set_password(self, password):
        self._password = password

    def set_salt(self, salt):
        self._salt = salt
    
    def get_password(self, password):
        return self._password

    def get_salt(self, salt):
        return self._salt

    def verify_password(self, password):
        if self._salt is not None and self._password is not None:
            return sha512(password+self.get_salt()).hexdigest() == self.get_password()
        else:
            raise ModuleException(ModuleException.get_msg(1))


    def _generateSaltedPassword(self, password):
        """
        Creates a new Password consisting of pw-hash (sha512) and a 128bit salt
        """
        salt = self._generateRandomString(128)
        pw = sha512(password+salt).hexdigest()
        return (pw, salt)          

    def _generateRandomString(self,length=8):
        """
        generates a random string with a given length. printable chars only
        """
        ret = ""
        for i in range(length):
            x = -1
            while x in (-1,91,92,93,94,95,96,60,61,62,58,59,63,64):
                x = randrange(48,123)
            ret+=chr(x)
        return ret

    def store(self):
        db = self._core.get_db()
        if self._id is None:
            self._id = db.get_seq_next("${grindhold_pageusers.users}")
        stmnt = "UPDATE OR INSERT INTO ${users} (PUS_ID, PUS_NICK, PUS_EMAIL, PUS_PASSWORD, PUS_SALT) \
                 VALUE (?, ?, ?, ?, ?) MATCHING (PUS_ID) ;"
        db.query(self._module, stmnt, (self._id, self._name, self._email, self._password, self._salt),commit=True)

    def delete(self):
        if self._id is None:
            return
        else:
            db = self._core.get_db()
            stmnt = "DELETE FROM ${users} WHERE PUS_ID = ? ;"
            db.query(self._module, stmnt, (self._id,), commit=True)
