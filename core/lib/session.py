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

from hashlib import sha256
from datetime import datetime, timedelta
from random import randrange
from Cookie import SimpleCookie
from helper import datetime2fdbTimestamp

from skarphedcore.configuration import Configuration
from skarphedcore.database import Database
from skarphedcore.core import Core
from skarphedcore.user import User

from common.errors import SessionException

class Session(object):
    """
    Handles clientsessions by a given session_id
    TODO: Session saves environmental variablees
    TODO: Session takes env-vars in account when verifying the id of the client
    """
    CURRENT_SESSION = None

    @classmethod
    def get_session(cls,cookies):
        """
        returns the session if it's not expired or nonexistant
        """
        cookie = SimpleCookie(cookies)
        session_id = cookie['session_id'].value
        
        db = Database()
        stmnt = "SELECT SES_USR_ID, SES_EXPIRES FROM SESSIONS WHERE SES_ID = ? ;"

        cur = db.query(stmnt,(session_id,))
        row = cur.fetchonemap()

        session=None

        if row is not None:
            user = User.get_user_by_id(row["SES_USR_ID"])
            session = Session(user)
            session._id = session_id
            expiration = row["SES_EXPIRES"]
            if expiration < datetime.now():
                raise SessionException(SessionException.get_msg(0))    
            session._expiration = row["SES_EXPIRES"]
        else:
            raise SessionException(SessionException.get_msg(2))
        return session

    @classmethod
    def create_session(cls, user):
        """
        creates a session for a given user
        """
        s = Session(user)
        cookie = SimpleCookie()
        cookie["session_id"] = s.get_id()
        Core().response_header.append(
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

    @classmethod
    def get_current_session_user(cls):
        """
        returns the user of the current clientsession
        """
        return cls.CURRENT_SESSION.get_user()

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

    def __init__(self, user):
        """
        initializes a session
        """
        #TODO: Introduce Configvalue sessionduration

        self._id = sha256(self._generateRandomString(24)).hexdigest()
        self._user = user.get_id()
        self._expiration = datetime.now()+timedelta(0,int(Configuration().get_entry("core.session_duration"))*3600)

    def get_id(self):
        """
        returns the current session session id, a 64byte string
        """
        return self._id

    def extend(self):
        """
        extends this session by a timespan defined as "core.session_extend" in hours in configuration
        """
        self._expiration += timedelta(0,int(Configuration().get_entry("core.session_extend"))*3600)

    def get_user(self):
        """
        returns this session's user
        """
        return User.get_user_by_id(self._user)

    def set_user(self,user):
        """
        set the user of this session
        """
        if type(user) == int:
            self._user = user
        elif user.__class__.__name__ == "User":
            self._user = user.get_id()
        else:
            raise SessionException(SessionException.get_msg(1))

    def store(self):
        """
        stores this session in database
        """
        if self._user is None:
            raise SessionException(SessionException.get_msg(3))
        else:
            db = Database()
            stmnt = "UPDATE OR INSERT INTO SESSIONS (SES_ID, SES_USR_ID, SES_EXPIRES) VALUES (?,?,?) MATCHING (SES_ID) ;"
            
            exp = datetime2fdbTimestamp(self._expiration)

            db.query(stmnt,(self._id,self._user,exp),commit=True)

    def delete(self):
        """
        deletes this session
        """
        db = Database()
        stmnt = "DELETE FROM SESSIONS WHERE SES_ID = ? ;"
        db.query(stmnt,(self._id,),commit=True)
