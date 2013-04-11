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

import fdb

from config import Config


class DatabaseMiddleware(object):
    def __init__(self, wrap_app):
        self._wrap_app = wrap_app

    def __call__(self, environ, start_response):
        config = Config()
        environ['db'] = DatabaseConnection(config['db.ip'], config['db.name'],
                config['db.user'], config['db.password'])
        return self._wrap_app(environ, start_response)


class DatabaseException(Exception):
    pass


class DatabaseConnection(object):
    def __init__(self, ip, dbname, user, password):
        self._ip = ip
        self._dbname = dbname
        self._user = user
        self._password = password
        self._connection = None

    def __del__(self):
        self._disconnect()


    def _connect(self):
        if not self._connection:
            try:
                self._connection = fdb.connect(
                            host = self._ip,
                            database = '/var/lib/firebird/2.5/data/' + self._dbname,
                            user = self._user,
                            password = self._password)
            except fdb.fbcore.DatabaseError, e:
                raise DatabaseException(str(e))


    def _disconnect(self):
        if self._connection:
            self._connection.close()


    def _params_to_tuple(self, params):
        if type(params) == tuple:
            return params
        else:
            return (params,)


    def query(self, statement, params = (), forceNoCache=False, commit = False):
        self._connect()
        cursor = self._connection.cursor()
        try:
            cursor.execute(statement, self._params_to_tuple(params))
            if commit:
                self._connection.commit()
            return cursor
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))

    def get_seq_next(self, sequence_id):
        """
        Yields the next value of a given sequence (e.g. 'MOD_GEN') 
        and increments it
        """
        self._connect()
        cur = self._connection.cursor()
        statement = 'SELECT GEN_ID (%s , 1) FROM RDB$DATABASE;' % str(sequence_id)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]

    def get_seq_current(self, sequence_id):
        """
        Yields the current value of a given sequence (e.g. 'MOD_GEN') 
        without incrementing it
        """
        self._connect()
        cur = self._connection.cursor()
        statement = 'SELECT GEN_ID (%s , 0) FROM RDB$DATABASE;' % str(sequence_id)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]
