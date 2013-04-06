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
from Cookie import CookieError
from helper import datetime2fdbTimestamp

class SessionMiddleware(object):
    def __init__(self, wrap_app):
        self._wrap_app = wrap_app

    def __call__(self, environ, start_response):
        session = self.get_session(environ)
        set_cookie = session == None 
        if not session:
            session = Session()
            session.store(environ)

        def session_start_response(status, headers, exc_info=None):
            if set_cookie:
                cookie = SimpleCookie()
                cookie['session_id'] = session.get_id()
                cookiestr = cookie.output().replace('Set-Cookie: ', '', 1)
                headers.append(('Set-Cookie', cookiestr))
            return start_response(status, headers, exc_info)

        environ['session'] = session
        return self._wrap_app(environ, session_start_response)

    def get_session(self, environ):
        try:
            cookie = SimpleCookie(environ['HTTP_COOKIE'])
            session_id = cookie['session_id'].value
            cur = environ['db'].query('SELECT SES_EXPIRES, SES_IS_ADMIN FROM SESSIONS \
                    WHERE SES_ID = ?;', session_id)
            result = cur.fetchonemap()
            if not result:
                return None
            expiration = result['SES_EXPIRES']
            is_admin = result['SES_IS_ADMIN']
            session = Session(session_id, expiration, is_admin)
            if expiration < datetime.now():
                session.delete(environ)
                session = None
            return session
        except KeyError, e:
            return None


class Session(object):
    def _generateRandomString(self, length):
        """
        generate  a random string 
        TODO: outsource this function to some kind of helpers module (other occurence in database.py)
        """
        ret = ""
        for i in range(length):
            x = -1
            while x in (-1,91,92,93,94,95,96,60,61,62,58,59,63,64):
                x = randrange(48,123)
            ret += chr(x)
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
    
    def get_id(self):
        return self._id

    def is_admin(self):
        return self._is_admin
    
    def set_admin(self, is_admin):
        self._is_admin = is_admin

    def store(self, environ):
        exp = datetime2fdbTimestamp(self._expiration)
        is_admin = 0
        if self._is_admin:
            is_admin = 1
        environ['db'].query('UPDATE OR INSERT INTO SESSIONS \
               (SES_ID, SES_EXPIRES, SES_IS_ADMIN) VALUES (?,?,?);',
               (self._id, exp, is_admin), commit = True)

    def delete(self, environ):
        environ['db'].query('DELETE FROM SESSIONS WHERE SES_ID = ?;',
                self._id, commit = True)
