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

import fdb

from config import Config


class DatabaseMiddleware(object):
    """
    A WSGI middleware that supplies a database connection in environ['db'].
    """

    def __init__(self, wrap_app):
        """
        Initializes the DatabaseMiddleware with the wrapped application.
        """
        self._wrap_app = wrap_app

    def __call__(self, environ, start_response):
        """
        Creates a database connection in environ['db'] and calls the wrapped application.
        """
        config = Config()
        environ['db'] = DatabaseConnection(config['db.ip'], config['db.name'],
                config['db.user'], config['db.password'])
        return self._wrap_app(environ, start_response)


class DatabaseException(Exception):
    """
    A database exception.
    """
    pass


class DatabaseConnection(object):
    """
    A connection to a database. The actual connection to the database is only established
    if query is called.
    """

    def __init__(self, ip, dbname, user, password):
        """
        Initializes this database with the given values.
        """
        self._ip = ip
        self._dbname = dbname
        self._user = user
        self._password = password
        self._connection = None

    def __del__(self):
        """
        Destroys this database connection.
        """
        self._disconnect()


    def _connect(self):
        """
        Establishes a connection to the database.
        """
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
        """
        Closes the database connection.
        """
        if self._connection:
            self._connection.close()


    def _params_to_tuple(self, params):
        """
        If params is no tuple a tuple with the given params will be returned. Otherwise
        params itself is returned.
        """
        if type(params) == tuple:
            return params
        else:
            return (params,)


    def query(self, statement, params = (), commit = False):
        """
        Executes a statement with given params and returns a cursor to the result.
        If commit the transaction will be committed to the database. If there is no
        connection yet, it will be established now.
        """
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
        Yields the next value of a given sequence (e.g. 'MOD_GEN') and increments it.
        """
        try:
            self._connect()
            cur = self._connection.cursor()
            statement = 'SELECT GEN_ID (%s , 1) FROM RDB$DATABASE;' % str(sequence_id)
            cur.execute(statement)
            res = cur.fetchone()
            return res[0]
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))
