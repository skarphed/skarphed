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

###########################################################
# Rewrite from PHP status
# 
# Class Database
# - private  functio __construct               --done 
# - public function setIp                      --done  
# - public function setDbName                  --done  
# - public function setUser                    --done
# - public function setPassword                --done
# - public function connect                    --done
# - private function getLowestUseQuery         --done QueryCache
# - private function generateZeros             --obsolete
# - private function replaceModuleTables       --done
# - private function createQueryInCache        --obsolete QueryCache
# - public function getConnection              --done
# - public function fetchArray                 --obsolete
# - public function fetchObject                --obsolete
# - public function commit                     --done
# - public function createTablesForModule      TODO
# - public function updateTablesForModule      TODO
# - public function createTableForModule       TODO
# - public function removeTableForModule       TODO
# - public function removeTablesForModule      TODO
# - public function getSeqNext                 --done
# - public function getSeqCurrent              --done
# - public function createBlob                 --obsolete
# - public function getInfo                    TODO
###########################################################

import re
import fdb
from scv import Core

class DatabaseException(Exception):
    """
    Exceptions for Database-Module
    """
    ERRORS = {
        1:"""At least one Parameter for the Connection is missing""",
        2:"""Could not Query: No Connection""",
        3:"""Could not resolve Tables:"""
    }

    def getMsg(self,nr, info):
        return "DB_"+str(nr)+": "+self.ERRORS[nr]+" "+info
    

class Database(object):
    """
    The Database-Class handles the connection to a Firebird 2.5+ Database
    """
    def __init__(self):
        """
        The Database loads connectiondata to the database from the config of Core
        """
        self._connection = None
        self._ip = None
        self._dbname = None
        self._user = None
        self._password = None

        self._queryCache = QueryCache()

        core = Core()
        config = core.getConfig()
        self.set_ip(config.getEntry('db.ip'))
        self.set_db_name(config.getEntry('db.name'))
        self.set_user(config.getEntry('db.user'))
        self.set_password(config.getEntry('db.password'))
        self.connect()

    def connect(self):
        """
        The class actually connects to the database and stores the 
        connection in _connection
        """
        if None in (self.user, self.ip, self.dbname, self.password):
            raise DatabaseException(DatabaseException.getMsg(1))
            #TODO: Globally Definable DB-Path
        try:
            self._connection = fdb.connect(
                        host=self._ip, 
                        database='/var/lib/firebird/2.5/data/'+self._dbname,
                        user=self._user, 
                        password=self._password)
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(e.value)
        return

    def set_ip(self, ip):
        """
        trivial
        """
        self._ip = str(ip)

    def set_db_name(self, dbname):
        """
        trivial
        """
        self._dname = str(dbname)

    def set_user(self, user):
        """
        trivial
        """
        self._user = str(user)

    def set_password(self, password):
        """
        trivial
        """
        self._password = str(password)

    def get_connection(self):
        """
        trivial
        """
        return self._connection

    def commit(self):
        """
        commits a pending transaction to the database
        """
        self._connection.commit()

    def query(self, module, statement, args=(), forceNoCache=False):
        """
        execute a query on the database. be sure to deliver the module.
        it is necessary to determine tablenames
        """
        if self._connection is None:
            raise DatabaseException(DatabaseException.getMsg(2))
        if module.getName() != "de.masterprogs.scoville.core":
            statement = self._replace_module_tables(module,statement)
        cur = self._connection.cursor()    
        prepared = self._queryCache(cur, statement)
        try:
            cur.execute(prepared,args)
        except fdb.fbcore.DatabaseError,e:
            raise DatabaseException(e.value)
        return cur

    def _replace_module_tables(self, module, query):
        """
        replaces module-based tablenames like
         'de.grinhold.scoville.news.news'
        with an actual SQL-table like
         'TAB_000004'
        """
        tagpattern = re.compile('\$\{[A-Za-z0-9.]+\}')
        matches = tagpattern.findall(query)
        matches = list(set(matches)) # making matches unique
        matches = map(lambda s: s[2:-1], matches)

        matchesRaw = list(matches)

        modules = [module.getName()]

        for match in matches:
            splitted = match.split(".")
            if len(splitted) > 1:
                matches.append(splitted[-1])
                matches.remove(match)
                splitted.remove(splitted[-1])
                modules.append(".".join(splitted))

        tableQuery = """SELECT MDT_ID, MDT_NAME, MOD_NAME
                     FROM MODULETABLES 
                      INNER JOIN MODULES ON (MDT_MOD_ID = MOD_ID )
                     WHERE MOD_NAME IN (?) 
                      AND MDT_NAME IN (?) ;"""
        cur = self._connection.cursor()
        tableQuery = self._queryCache(cur,tableQuery)
        cur.execute(tableQuery,("'"+"','".join(modules)+"'","'"+"','".join(matches)+"'"))

        replacementsDone = []
        for res in cur.fetchmapall():
            pattern = "${"+res["MOD_NAME"]+"."+res["MDT_NAME"]+"}"
            tableId = str(res["MDT_ID"])
            tableId = "TAB_"+"0"*(6-len(tableId))+tableId
            query = query.replace(pattern, tableId)
            replacementsDone.append(res["MOD_NAME"]+"."+res["MDT_NAME"])
            if res["MOD_NAME"] == module.getName():
                query = query.replace("${"+res["MDT_NAME"]+"}", tableId)

        if len(matchesRaw) != len(replacementsDone):
            for replacement in replacementsDone:
                matchesRaw.remove(replacement)
            raise DatabaseException(DatabaseException.getMsg(3,str(matchesRaw)))
        return query

    def get_seq_next(self,sequenceId):
        """
        Yields the next value of a given sequence (e.g. 'MOD_GEN') 
        and increments it
        """
        cur = self._connection.cursor()
        statement = "SELECT GEN_ID ( %s , 1) FROM DUAL ;"%str(sequenceId)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]

    def get_seq_current(self,sequenceId):
        """
        Yields the current value of a given sequence (e.g. 'MOD_GEN') 
        without incrementing it
        """
        cur = self._connection.cursor()
        statement = "SELECT GEN_ID ( %s , 0) FROM DUAL ;"%str(sequenceId)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]

    def remove_tables_for_module(module, tables):
        """
        remove tables as part of module uninstallation
        """
        pass #TODO Implement

    def create_tables_for_module(module, tables):
        """
        create tables as part of module installation
        """
        pass #TODO Implement

    def update_tables_for_module(module, tables):
        """
        update tables as part of module update
        """
        pass #TODO Implement


class QueryCache(object):
    """
    caches prepared statements and delivers them on demand
    """
    RANK = 0
    PREP = 1
    MAX_QUERIES = 20
    def __init__(self):
        """
        trivial
        """
        self.queries = {}

    def __call__(self, cur, query):
        """
        looks if the given query is in the cache, if not, creates and returns
        it. if the number of cached query exceeds the MAX_QUERIES, it deletes
        the less used query
        """
        if query not in self.queries:
            if len(self.queries) >= self.MAX_QUERIES:
                lowest = self._get_lowest_use_query()
                del(self.queries[lowest])
            self.queries[query] = {self.RANK:0,self.PREP:cur.prep(query)}
        self.queres[query][self.RANK] += 1
        return self.queries[query]


    def _get_lowest_use_query(self):
        """
        returns the query that has been used the fewest times.
        """
        lowest = None
        lquery = None
        for query, querydict in self.queries.items():
            if lowest is None or querydict[self.RANK] < lowest:
                lowest = querydict[self.RANK]
                lquery = query
        return lquery