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

from hashlib import sha256
from datetime import datetime, timedelta
from random import randrange
from Cookie import SimpleCookie
from helper import datetime2fdbTimestamp

"""
class RepoMiddleware(object):
    def __init__(self, wrap_app):
        self._wrap_app = wrap_app

    def __call__(self, environ, start_response):

        return wrap_app(environ, start_response):

class Session(object):
    def _generateRandomString(self,length):
"""
   #     generate  a random string 
    #    TODO: outsource this function to some kind of helpers module (other occurence in database.py)
"""
        ret = ""
        for i in range(length):
            x = -1
            while x in (-1,91,92,93,94,95,96,60,61,62,58,59,63,64):
                x = randrange(48,123)
            ret+=chr(x)
        return ret

    def __init__(self, id = None, expiration = None, is_admin = False):
        if id:
            self._id = id
        else:
            self._id = sha256(self._generateRandomString(24)).hexdigest()
        if expiration:
            self._expiration = expiration
        else:
            self._expiration = datetime.now()+timedelta(0,2*3600)
        self._is_admin = is_admin
"""
class SessionException(Exception):
    ERRORS = {
        0:"""SessionError: Session Expired""",
        1:"""SessionError: Can only attach user to session""",
        2:"""SessionError: This Session does not exist"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "SE_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class Session(object):
    """
    Handles clientsessions by a given session_id
    TODO: Session saves environmental variablees
    TODO: Session takes env-vars in account when verifying the id of the client
    """

    @classmethod
    def get_session(cls,repository,session_id):
        """
        returns the session if it's not expired or nonexistant
        """
        db = repository.get_db()
        stmnt = "SELECT SES_EXPIRES, SES_IS_ADMIN FROM SESSIONS WHERE SES_ID = ? ;"

        cur = db.query(stmnt,(session_id,))
        row = cur.fetchonemap()

        session=None

        if row is not None:
            session = Session(repository)
            session._id = session_id
            expiration = row["SES_EXPIRES"]
            if expiration < datetime.now():
                raise SessionException(SessionException.get_msg(0))    
            session._expiration = row["SES_EXPIRES"]
            session._is_admin = bool(row["SES_IS_ADMIN"])
        else:
            raise SessionException(SessionException.get_msg(2))
        return session

    @classmethod
    def create_session(cls, repository, response_header):
        """
        creates a session for a given user
        """
        s = Session(repository)
        cookie = SimpleCookie()
        cookie["session_id"] = s.get_id()
        response_header.append(
                ("Set-Cookie", cookie.output().replace("Set-Cookie: ","",1))
            )
        s.store()
        return s

    @classmethod
    def set_current_session(cls, session):
        """
        sets the session of the current user
        """
        cls.CURRENT_SESSION = session

    @classmethod
    def get_current_session(cls):
        """
        returns the current session of the current client
        """
        return cls.CURRENT_SESSION

    def _generateRandomString(self,length):
        """
        generate  a random string 
        TODO: outsource this function to some kind of helpers module (other occurence in database.py)
        """
        ret = ""
        for i in range(length):
            x = -1
            while x in (-1,91,92,93,94,95,96,60,61,62,58,59,63,64):
                x = randrange(48,123)
            ret+=chr(x)
        return ret

    def __init__(self, repository, id = None, expiration = None, is_admin = False):
        """
        initializes a session
        """
        self._repository = repository
        if id:
            self._id = id
        else:
            self._id = sha256(self._generateRandomString(24)).hexdigest()
        if expiration:
            self._expiration = expiration
        else:
            self._expiration = datetime.now()+timedelta(0,2*3600)
        self._is_admin = is_admin

    def get_id(self):
        """
        returns the current session session id, a 64byte string
        """
        return self._id

    def extend(self):
        """
        extends this session by 2 hours
        """
        self._expiration += timedelta(0,2*3600)

    def set_admin(self, is_admin):
        """
        trivial
        """
        self._is_admin = is_admin

    def store(self):
        """
        stores this session in database
        """
        
        db = self._repository.get_db()
        stmnt = "UPDATE OR INSERT INTO SESSIONS (SES_ID, SES_EXPIRES, SES_IS_ADMIN) VALUES (?,?,?) MATCHING (SES_ID) ;"
        
        exp = datetime2fdbTimestamp(self._expiration)

        db.query(stmnt,(self._id,exp,int(self._is_admin)),commit=True)

    def delete(self):
        """
        deletes this session
        """
        db = self._repository.get_db()
        stmnt = "DELETE FROM SESSIONS WHERE SES_ID = ? ;"
        db.query(stmnt,(self._id,),commit=True)
