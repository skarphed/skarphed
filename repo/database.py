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

class DatabaseException(Exception):
    pass


class DatabaseConnection(object):
    def __init__(self, ip, dbname, user, password):
        self.ip = ip
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None


    def connect(self):
        try:
            self.connection = fdb.connect(
                        host = self.ip,
                        database = '/var/lib/firebird/2.5/data/' + self.dbname,
                        user = self.user,
                        password = self.password)
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))
        return


    def disconnect(self):
        if self.connection:
            self.connection.close()


    def params_to_tuple(self, params):
        if type(params) == tuple:
            return params
        else:
            return (params,)


    def query(self, statement, params = (), forceNoCache=False, commit = False):
        if self.connection is None:
            raise DatabaseException('No Connection')
        cursor = self.connection.cursor()
        try:
            cursor.execute(statement, self.params_to_tuple(params))
            if commit:
                self.connection.commit()
            return cursor
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))

    def get_seq_next(self,sequenceId):
        """
        Yields the next value of a given sequence (e.g. 'MOD_GEN') 
        and increments it
        """
        cur = self._connection.cursor()
        statement = "SELECT GEN_ID ( %s , 1) FROM RDB$DATABASE ;"%str(sequenceId)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]

    def get_seq_current(self,sequenceId):
        """
        Yields the current value of a given sequence (e.g. 'MOD_GEN') 
        without incrementing it
        """
        cur = self._connection.cursor()
        statement = "SELECT GEN_ID ( %s , 0) FROM RDB$DATABASE ;"%str(sequenceId)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]