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

import re
import fdb
from scv import Core

class DatabaseException(Exception):
    ERRORS = {
        1:"""At least one Parameter for the Connection is missing""",
        2:"""Could not Query: No Connection""",
        3:"""Could not resolve Tables:"""
    }

    def getMsg(self,nr, info):
        return "DB_"+str(nr)+": "+self.ERRORS[nr]+" "+info
    

class Database(object):
    def __init__(self):
        self._connection = None
        self._ip = None
        self._dbname = None
        self._user = None
        self._password = None

        self._queryCache = QueryCache()

        core = Core()
        config = core.getConfig()
        self.setIp(config.getEntry('db.ip'))
        self.setDbName(config.getEntry('db.name'))
        self.setUser(config.getEntry('db.user'))
        self.setPassword(config.getEntry('db.password'))
        self.connect()

    def connect(self):
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

    def setIp(self, ip):
        self._ip = str(ip)

    def setDbName(self, dbname):
        self._dname = str(dbname)

    def setUser(self, user):
        self._user = str(user)

    def setPassword(self, password):
        self._password = str(password)

    def getConnection(self):
        return self._connection

    def commit(self):
        self._connection.commit()

    def query(self, module, statement, args=(), forceNoCache=False):
        if self._connection is None:
            raise DatabaseException(DatabaseException.getMsg(2))
        if module.getName() != "de.masterprogs.scoville.core":
            statement = self._replaceModuleTables(module,statement)
        cur = self._connection.cursor()    
        prepared = self._queryCache(cur, statement)
        try:
            cur.execute(prepared,args)
        except fdb.fbcore.DatabaseError,e:
            raise DatabaseException(e.value)
        return cur

    def _replacemoduleTables(self, module, query):
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

    def getSeqNext(self,sequenceId):
        cur = self._connection.cursor()
        statement = "SELECT GEN_ID ( %s , 1) FROM DUAL ;"%str(sequenceId)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]

    def getSeqCurrent(self,sequenceId):
        cur = self._connection.cursor()
        statement = "SELECT GEN_ID ( %s , 0) FROM DUAL ;"%str(sequenceId)
        cur.execute(statement)
        res = cur.fetchone()
        return res[0]

    def removeTablesForModule(module, tables):
        pass #TODO Implement

    def createTablesForModule(module, tables):
        pass

    def updateTablesForModule(module, tables):
        pass


class QueryCache(object):
    RANK = 0
    PREP = 1
    MAX_QUERIES = 20
    def __init__(self):
        self.queries = {}

    def __call__(self, cur, query):
        if query not in self.queries:
            if len(self.queries) >= self.MAX_QUERIES:
                lowest = self._getLowestUseQuery()
                del(self.queries[lowest])
            self.queries[query] = {self.RANK:0,self.PREP:cur.prep(query)}
        self.queres[query][self.RANK] += 1
        return self.queries[query]


    def _getLowestUseQuery(self):
        lowest = None
        lquery = None
        for query, querydict in self.queries.items():
            if lowest is None or querydict[self.RANK] < lowest:
                lowest = querydict[self.RANK]
                lquery = query
        return lquery