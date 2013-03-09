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
from hashlib import sha256 as sha256hash
from StringIO import StringIO
import base64 #TODO: The whole thing should work without base64. find out why it doesnt here

class BinaryException(Exception):
    """
    Exceptions for Database-Module
    """
    ERRORS = {
        0:"""Get By Id: The Binary with this ID does not exist: """,
        1:"""Get By MD5: No Binary found with the hash: """,
        2:"""Store: Not allowed to store this binary""",
        3:"""Get By Filename: No Binary found with the filename: """
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        if type(info) != str:
            info=str(info)
        return "BIN_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class BinaryManager(object):
    def __init__(self,core):
        self._core = core

        Binary.set_core(core)

        self.create = Binary.create
        self.get_by_id = Binary.get_by_id
        self.get_by_md5 = Binary.get_by_md5
        self.get_by_filename = Binary.get_by_filename

class Binary(object):
    """
    This class handles binary data that is to be displayed
    or linked on websites.
    """
    @classmethod
    def set_core(cls, core):
        cls._core = core

    @classmethod
    def create(cls, mime, data, filename=""):
        bin = Binary(cls._core)
        
        filename = md5hash(data).hexdigest()[:6]+"_"+filename

        bin.set_filename(filename)
        bin.set_mime(mime)
        bin.set_data(data)

        return bin

    @classmethod
    def get_by_filename(cls, filename):
        db = cls._core.get_db()
        stmnt = "SELECT BIN_ID, BIN_MIME, BIN_DATA FROM BINARIES WHERE BIN_FILENAME = ? ;"
        cur = db.query(cls._core , stmnt, (filename,))
        row = cur.fetchonemap()
        if row is not None:
            bin = Binary(cls._core)
            bin.set_id(row["BIN_ID"])
            bin.set_filename(filename)
            bin.set_mime(row["BIN_MIME"])
            bin.set_data(base64.decodestring(row["BIN_DATA"]))
            return bin
        else:
            raise BinaryException(BinaryException.get_msg(0, filename))

    @classmethod
    def get_by_id(cls, nr):
        db = cls._core.get_db()
        stmnt = "SELECT BIN_FILENAME, BIN_MIME, BIN_DATA FROM BINARIES WHERE BIN_ID = ? ;"
        cur = db.query(cls._core , stmnt, (nr,))
        row = cur.fetchonemap()
        if row is not None:
            bin = Binary(cls._core)
            bin.set_id(nr)
            bin.set_filename(row["BIN_FILENAME"])
            bin.set_mime(row["BIN_MIME"])
            bin.set_data(base64.decodestring(row["BIN_DATA"]))
            return bin
        else:
            raise BinaryException(BinaryException.get_msg(0, nr))

    @classmethod
    def get_by_md5(cls, md5):
        db = cls._core.get_db()
        stmnt = "SELECT BIN_FILENAME, BIN_ID, BIN_MIME, BIN_DATA FROM BINARIES WHERE BIN_MD5 = ? ;"
        cur = db.query(cls._core , stmnt, (md5,))
        row = cur.fetchonemap()
        if row is not None:
            bin = Binary(cls._core)
            bin.set_id(row["BIN_ID"])
            bin.set_filename(row["BIN_FILENAME"])
            bin.set_mime(row["BIN_MIME"])
            bin.set_data(base64.decodestring(row["BIN_DATA"]))
            return bin
        else:
            raise BinaryException(BinaryException.get_msg(1, md5))

    def __init__(self, core):
        self._core = core

        self._id = None
        self._filename = None
        self._mime = None
        self._data = None

    def get_id(self):
        return self._id

    def set_id(self, nr):
        self._id = int(nr)

    def get_mime(self):
        return self._mime

    def set_mime(self,mime):
        self._mime = mime

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def get_filename(self):
        return self._filename

    def set_filename(self, filename):
        self._filename = str(filename)

    def store(self):
        """
        Stores this binary into the database
        """
        db = self._core.get_db()
        data_io = StringIO(base64.encodestring(self._data))
        md5 = md5hash(self._data).hexdigest()
        sha256 = sha256hash(self._data).hexdigest()
        if self._id is None:
            self.set_id(db.get_seq_next("BIN_GEN"))

        user_id = self._core.get_session_manager().get_current_session_user().get_id()
        stmnt = "UPDATE OR INSERT INTO BINARIES (BIN_ID, BIN_FILENAME, BIN_MIME, BIN_USR_OWNER, \
                   BIN_USR_LASTCHANGE, \
                   BIN_DATE_LASTCHANGE, BIN_SHA256, BIN_MD5, BIN_DATA) \
                 VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ? ) MATCHING (BIN_ID) ;"
        db.query(self._core,stmnt, (self._id, self._filename, self._mime, user_id, user_id, sha256, md5, data_io),commit=True)
        data_io.close()

    def delete(self):
        db = self._core.get_db()
        stmnt = "DELETE FROM BINARIES WHERE BIN_ID = ? ;"
        db.query(self._core, stmnt, (self.get_id(),), commit=True)
        

class Image(Binary):
    def resize(self, w, h):
        pass

    def get_image_size(self):
        pass

    def generate_thumbnail(self):
        pass

