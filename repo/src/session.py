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
from Cookie import SimpleCookie
from Cookie import CookieError
from helper import datetime_to_fdb_timestamp, generate_random_string
from logger import logger
from config import Config

class SessionMiddleware(object):
    """
    A WSGI middleware that handles cookie-based sessions. The session object can be accessed
    via the WSGI environment. On top of this middleware the DatabaseMiddleware must be used in
    order to supply a database for session storage.
    """

    def __init__(self, wrap_app):
        """
        Initializes the SessionMiddleware with a wrapped application.
        """
        self._wrap_app = wrap_app

    def __call__(self, environ, start_response):
        """
        Manages sessions and calls the wrapped application.
        """
        session = self.get_session(environ)
        if not session:
            session = Session()

        def session_start_response(status, headers, exc_info=None):
            """
            A start_response function that append a session cookie to the response headers if necessary.
            """
            if session.stored():
                cookie = SimpleCookie()
                cookie['session_id'] = session.get_id()
                cookiestr = cookie.output().replace('Set-Cookie: ', '', 1)
                headers.append(('Set-Cookie', cookiestr))
            return start_response(status, headers, exc_info)

        environ['session'] = session
        return self._wrap_app(environ, session_start_response)

    def get_session(self, environ):
        """
        Returns the session whose id is stored in the cookie or None if there is no cookie.
        """
        try:
            cookie = SimpleCookie(environ['HTTP_COOKIE'])
            session_id = cookie['session_id'].value
            cur = environ['db'].query('SELECT SES_EXPIRES, SES_IS_ADMIN FROM SESSIONS \
                    WHERE SES_ID = ?;', session_id)
            result = cur.fetchonemap()
            if not result:
                return None
            expiration = result['SES_EXPIRES']
            is_admin = bool(result['SES_IS_ADMIN'])
            session = Session(session_id, expiration, is_admin)
            if expiration < datetime.now():
                logger.info('session expired: %s' % session_id)
                session.delete(environ)
                session = None
            logger.info('loaded session: %s' % session_id)
            return session
        except KeyError, e:
            return None


class Session(object):
    """
    A session stores its id, its expiration time and whether the user is privileged for admin actions.
    """

    def __init__(self, id = None, expiration = None, is_admin = False):
        """
        Initializes a session object with the given values. If no values are specified, hardcoded
        default values will be used.
        """
        config = Config()
        if id:
            self._id = id
        else:
            self._id = sha256(generate_random_string(24)).hexdigest()
            logger.debug('created session: %s' % self._id)
        if expiration:
            self._expiration = expiration
        else:
            self._expiration = datetime.now()+timedelta(0,config['session.expires'])
        self._is_admin = is_admin
        self._stored = False
    
    def get_id(self):
        """
        Returns the session id.
        """
        return self._id

    def is_admin(self):
        """
        Returns whether this session is privileged for admin actions.
        """
        return self._is_admin
    
    def set_admin(self, is_admin):
        """
        Sets the admin flag.
        """
        self._is_admin = is_admin

    def store(self, environ):
        """
        Stores this session in the database.
        """
        exp = datetime_to_fdb_timestamp(self._expiration)
        is_admin = 0
        if self._is_admin:
            is_admin = 1
        environ['db'].query('UPDATE OR INSERT INTO SESSIONS \
               (SES_ID, SES_EXPIRES, SES_IS_ADMIN) VALUES (?,?,?);',
               (self._id, exp, is_admin), commit = True)
        self._stored = True

    def delete(self, environ):
        """
        Removes this session from the database.
        """
        environ['db'].query('DELETE FROM SESSIONS WHERE SES_ID = ?;',
                self._id, commit = True)

    def stored(self):
        """
        Returns whether this session has been stored.
        """
        return self._stored
