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

from hashlib import md5 as md5hash

class BinaryException(Exception):
    """
    Exceptions for Database-Module
    """
    ERRORS = {
        0:"""Load: The Binary with this ID does not exist: """,
        1:"""LoadMD5: No Binary found with the hash: """,
        2:"""Store: Not allowed to store this binary"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "BIN_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class BinaryManager(object):
    def __init__(self,core):
        self._core = core

        Binary.set_core(core)

        self.create = Binary.create
        self.load = Binary.load
        self.load_md5 = Binary.load_md5



class Binary(object):
    """
    This class handles binary data that is to be displayed
    or linked on websites.
    """
    @classmethod
    def set_core(cls, core):
        self._core = core

    @classmethod
    def create(cls, mime, data, permission):
        return Binary(cls._core, None, mime,data, permission)

    @classmethod
    def load(cls, nr):
        db = cls._core.get_db()
        stmnt = "SELECT BIN_MIME, BIN_RIG_ID, BIN_DATA FROM BINARYS WHERE BIN_ID = ? ;"
        cur = db.query(cls._core , stmnt, (nr,))
        row = cur.fetchonemap()
        if row is not None:
            return Binary(cls._core, nr, row["BIN_MIME"], row["BIN_DATA"], row["BIN_RIG_ID"])
        else:
            raise BinaryException(BinaryException.get_msg(0, nr))

    @classmethod
    def load_md5(cls, md5):
        db = cls._core.get_db()
        stmnt = "SELECT BIN_ID, BIN_MIME, BIN_DATA, BIN_RIG_ID FROM BINARYS WHERE BIN_MD5 = ? ;"
        cur = db.query(cls._core , stmnt, (md5,))
        row = cur.fetchonemap()
        if row is not None:
            return Binary(cls._core, row["BIN_ID"], row["BIN_MIME"], row["BIN_DATA"], row["BIN_RIG_ID"])
        else:
            raise BinaryException(BinaryException.get_msg(1, md5))

    def __init__(self, core, nr, mime, data, permission_id):
        self._core = core

        self._id = None
        self._mime = mime
        self._data = data
        self._permission = permission_id

    def get_id(self):
        return self._id

    def get_mime(self):
        return self._mime

    def set_mime(self,mime):
        self._mime = mime

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def get_permission(self):
        return self._permission

    def set_permission(self, permission):
        self._permission = permission

    def store(self):
        """
        Stores this binary into the database
        """
        db = self._core.get_db()
        md5 = md5hash(self._data).hexdigest()
        if self._id is None:
            self._id = db.get_seq_next("BIN_GEN")
            user_id = self._core.get_user_manager().get_session_user().get_id()
            #TODO: Anonymous user muss datei hochladen koennen
            stmnt = "INSERT INTO BINARYS (BIN_ID, BIN_MIME, BIN_USR_ID_OWNER, \
                       BIN_USR_ID_LASTCHANGE, \
                       BIN_DATE_LASTCHANGE, BIN_RIG_ID, BIN_MD5, BIN_DATA) \
                     VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?) ;"
            db.query(self._core,stmnt, (self._id, self._mime, user_id, user_id, self._permission, md5, self._data))
        else:
            if self._permission is None:
                stmnt = "SELECT 1 FROM BINARYS WHERE BIN_MD5 = ? AND BIN_MIME = ? AND BIN_RIG_ID IS NULL ;"
                cur = db.query(self._core,stmnt, (md5,self._mime))
            else:
                stmnt = "SELECT 1 FROM BINARYS WHERE BIN_MD5 = ? AND BIN_MIME = ? AND BIN_RIG_ID = ? ;"
                cur = db.query(self._core,stmnt, (md5, self._mime, self._permission))
            row = cur.fetchonemap()
            if row is None:
                stmnt = "UPDATE BINARYS SET BIN_MD5 = ?, BIN_MIME = ?, BIN_RIG_ID = ?, BIN_DATA = ? WHERE BIN_ID = ? ;"
                db.query(self._core,stmnt, (md5,self._mime,self._permission, data, self._id))
            else:
                raise BinaryException(BinaryException.get_msg(2))

class Image(Binary):
    def resize(self, w, h):
        pass

    def get_image_size(self):
        pass

    def generate_thumbnail(self):
        pass

