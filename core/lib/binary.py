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
from hashlib import md5 as md5hash
from hashlib import sha256 as sha256hash
import Image as PILImage
from StringIO import StringIO
import base64 #TODO: The whole thing should work without base64. find out why it doesnt here

from skarphedcore.configuration import Configuration
from skarphedcore.session import Session

from common.errors import BinaryException

class Binary(object):
    """
    This class handles binary data that is to be displayed
    or linked on websites.
    """
    @classmethod
    def create(cls, mime, data, filename=""):
        bin = Binary()
        
        filename = md5hash(data).hexdigest()[:6]+"_"+filename

        bin.set_filename(filename)
        bin.set_mime(mime)
        bin.set_data(data)

        return bin

    @classmethod
    def get_by_filename(cls, filename):
        data_fetched = False
        configuration = Configuration()
        binary_cache_path = os.path.join(configuration.get_entry("global.binary_cache"),
                                         configuration.get_entry("core.instance_id"))

        if not os.path.exists(binary_cache_path):
            os.mkdir(binary_cache_path,True)

        db = Database()
        if os.path.exists(os.path.join(binary_cache_path, filename)):
            cachefile = open(os.path.join(binary_cache_path, filename),"rb")
            data = cachefile.read()
            cachefile.close()

            md5 = md5hash(data).hexdigest()
            sha256 = sha256hash(data).hexdigest()

            stmnt = "SELECT BIN_ID, BIN_MIME,   \
                     (SELECT BIN_DATA FROM BINARIES WHERE BIN_FILENAME = ? AND BIN_MD5 != ? AND BIN_SHA256 != ?) AS BIN_DATA \
                     FROM BINARIES WHERE BIN_FILENAME = ?  ;"
            cur = db.query(stmnt, (filename, md5, sha256, filename))
            row = cur.fetchonemap()
            if row is not None:
                data_fetched = True
                if row["BIN_DATA"] is None:
                    bin = Binary()
                    bin.set_id(row["BIN_ID"])
                    bin.set_filename(filename)
                    bin.set_mime(row["BIN_MIME"])
                    bin.set_data(data)
                    return bin
            else:
                raise BinaryException(BinaryException.get_msg(0, filename))
        if not data_fetched:
            stmnt = "SELECT BIN_ID, BIN_MIME, BIN_DATA FROM BINARIES WHERE BIN_FILENAME = ? ;"
            cur = db.query(stmnt, (filename,))
            row = cur.fetchonemap()
        if row is not None:
            bin = Binary()
            bin.set_id(row["BIN_ID"])
            bin.set_filename(filename)
            bin.set_mime(row["BIN_MIME"])
            bin.set_data(base64.b64decode(row["BIN_DATA"]))

            cachefile = open(os.path.join(binary_cache_path, filename),"wb")
            cachefile.write(bin.get_data())
            cachefile.close()

            return bin
        else:
            raise BinaryException(BinaryException.get_msg(0, filename))

    @classmethod
    def get_by_id(cls, nr):
        db = Database()
        stmnt = "SELECT BIN_FILENAME, BIN_MIME, BIN_DATA FROM BINARIES WHERE BIN_ID = ? ;"
        cur = db.query(stmnt, (nr,))
        row = cur.fetchonemap()
        if row is not None:
            bin = Binary()
            bin.set_id(nr)
            bin.set_filename(row["BIN_FILENAME"])
            bin.set_mime(row["BIN_MIME"])
            bin.set_data(base64.b64decode(row["BIN_DATA"]))
            return bin
        else:
            raise BinaryException(BinaryException.get_msg(0, nr))

    @classmethod
    def get_by_md5(cls, md5):
        db = Database()
        stmnt = "SELECT BIN_FILENAME, BIN_ID, BIN_MIME, BIN_DATA FROM BINARIES WHERE BIN_MD5 = ? ;"
        cur = db.query(stmnt, (md5,))
        row = cur.fetchonemap()
        if row is not None:
            bin = Binary()
            bin.set_id(row["BIN_ID"])
            bin.set_filename(row["BIN_FILENAME"])
            bin.set_mime(row["BIN_MIME"])
            bin.set_data(base64.b64decode(row["BIN_DATA"]))
            return bin
        else:
            raise BinaryException(BinaryException.get_msg(1, md5))

    def __init__(self):
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
        db = Database()
        data_io = base64.b64encode(self._data)
        md5 = md5hash(self._data).hexdigest()
        sha256 = sha256hash(self._data).hexdigest()
        if self._id is None:
            self.set_id(db.get_seq_next("BIN_GEN"))

        user_id = Session.get_current_session_user().get_id()
        stmnt = "UPDATE OR INSERT INTO BINARIES (BIN_ID, BIN_FILENAME, BIN_MIME, BIN_USR_OWNER, \
                   BIN_USR_LASTCHANGE, \
                   BIN_DATE_LASTCHANGE, BIN_SHA256, BIN_MD5, BIN_DATA) \
                 VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ? ) MATCHING (BIN_ID) ;"
        db.query(stmnt, (self._id, self._filename, self._mime, user_id, user_id, sha256, md5, data_io),commit=True)

    def delete(self):
        db = Database()
        stmnt = "DELETE FROM BINARIES WHERE BIN_ID = ? ;"
        db.query(stmnt, (self.get_id(),), commit=True)
        configuration = Configuration()
        binary_cache_path = os.path.join(configuration.get_entry("global.binary_cache"),
                                         configuration.get_entry("core.instance_id"))
        os.unlink(os.path.join(binary_cache_path, self.get_filename()))

    @classmethod    
    def get_binaries_for_gui(cls):
        #TODO: Check permission
        db = Database()
        stmnt = "SELECT BIN_ID, BIN_FILENAME, BIN_MIME, OCTET_LENGTH(BIN_DATA) AS BIN_SIZE \
                 FROM BINARIES ;"
        cur = db.query(stmnt, ())
        ret = []
        for dataset in cur.fetchallmap():
            ret.append({'filename': dataset['BIN_FILENAME'],
                        'size': dataset['BIN_SIZE'],
                        'mime': dataset['BIN_MIME'],
                        'id': dataset['BIN_ID']})
        return ret

    @classmethod
    def delete_binaries(cls, binaryIds):
        db = Database()
        stmnt = "DELETE FROM BINARIES WHERE BIN_ID = ? ;"
        for binaryId in binaryIds:
            db.query(stmnt, (binaryId,), commit=True)
        

class Image(Binary,PILImage):
    def __init__(self):
        PILImage.__init__(self)
        Binary.__init__(self)

