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

from json import JSONDecoder

class ConfigurationException(Exception):
    ERRORS = {
        1:"""This Configurationentry does not exist!""",
        2:"""Can only override entries in database"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "CONF_"+str(nr)+": "+cls.ERRORS[nr]+" "+info


class Configuration(object):
    """
    Holds the Configuration-Values of Scoville.
    It inherits from:
    1. /etc/scoville/scoville.conf 
    2. <SCVWEBPATH>/config.json
    3. <SCVWEBPATH>/instanceconf.py
    4. Configuration values in CONFIG-Table of Database
    It is initialized in this order
    """

    CONF_NOT_LOAD = 0
    CONF_LOAD_GLOBAL = 1
    CONF_LOAD_LOCAL = 2
    CONF_LOAD_DB = 3

    def __init__(self, core):
        """
        Initializes global-and local-level config
        """
        self._core = core

        self._configuration = {}
        self._state = self.CONF_NOT_LOAD

        coreconfig = self._core.get_core_config(self)
        self._configuration["global.libpath"] = coreconfig["SCV_LIBPATH"]
        self._configuration["global.webpath"] = coreconfig["SCV_WEBPATH"]
        self._configuration["core.instance_id"] = coreconfig["SCV_INSTANCE_SCOPE_ID"]
        self._configuration["core.webpath"] = self._configuration["global.webpath"]+ self._configuration["core.instance_id"]
        self._state = self.CONF_LOAD_GLOBAL

        configjson = open(self._configuration["core.webpath"]+"/config.json").read()
        self._configuration.update(JSONDecoder().decode(configjson))
        self._local_config_keys = self._configuration.keys()
        self._state = self.CONF_LOAD_LOCAL

    def init_from_db(self):
        """
        Loads the values vom the table CONFIG into the config
        """
        db = self._core.get_db()
        cur = db.query(self._core, "SELECT PARAM,VAL FROM CONFIG ;")
        for res in cur.fetchallmap():
            self._configuration[res["PARAM"]] = res["VAL"]
        self._state = self.CONF_LOAD_DB

    def get_entry(self, entry):
        """
        Returns a entry of this core's configuration
        """
        if entry in self._configuration.keys():
            return self._configuration[entry]
        raise ConfigurationException(ConfigurationException.get_msg(1))

    def set_entry(self, entry, value):
        """
        Sets an entry of this core's configuration
        """
        if entry not in self._local_config_keys:
            db = self._core.get_db()
            stmnt = "UPDATE OR INSERT INTO CONFIG (PARAM,VAL) VALUES (?,?) MATCHING (PARAM) ;"
            db.query(self._core,stmnt,(entry,str(value)),commit=True)
        else:
            raise ConfigurationException(ConfigurationException.get_msg(2))

    def get_parent(self):
        """
        returns Confiuration's coreobject
        """
        return self._core

    def get_core(self):
        """
        returns Confiuration's coreobject
        """
        return self._core
