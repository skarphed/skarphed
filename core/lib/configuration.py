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

from json import JSONDecoder

from common.errors import ConfigurationException


class Configuration(object):
    """
    Holds the Configuration-Values of Skarphed.
    It inherits from:
    1. /etc/skarphed/skarphed.conf 
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
        self._configuration["global.binary_cache"] = coreconfig["SCV_BINARY_CACHEPATH"]
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
        stmnt = """ SELECT CNF_PARAM, CNF_VAL, MOD_NAME , NULL AS CNO_WGT_ID
                        FROM CONFIG INNER JOIN CONFIGOWNERS ON (CNF_CNO_ID = CNO_ID) 
                        INNER JOIN MODULES ON (CNO_MOD_ID = MOD_ID)
                            WHERE CNO_MOD_ID IS NOT NULL AND CNO_WGT_ID IS NULL
                        UNION
                    SELECT CNF_PARAM, CNF_VAL, MOD_NAME, CNO_WGT_ID
                        FROM CONFIG INNER JOIN CONFIGOWNERS ON (CNF_CNO_ID = CNO_ID)
                        INNER JOIN WIDGETS ON (CNO_WGT_ID = WGT_ID)
                        INNER JOIN MODULES ON (WGT_MOD_ID = MOD_ID)
                            WHERE CNO_MOD_ID IS NULL AND CNO_WGT_ID IS NOT NULL
                        UNION
                    SELECT CNF_PARAM, CNF_VAL, NULL AS MOD_NAME, NULL AS CNO_WGT_ID
                        FROM CONFIG INNER JOIN CONFIGOWNERS ON (CNF_CNO_ID = CNO_ID)
                            WHERE CNO_MOD_ID IS NULL AND CNO_WGT_ID IS NULL ;
                """

        


        cur = db.query(self._core, stmnt)
        for res in cur.fetchallmap():
            if res["CNO_WGT_ID"] is not None:
                prefix = res["MOD_NAME"]+"::"+str(res["CNO_WGT_ID"])+"::"
            elif res["MOD_NAME"] is not None:
                prefix = res["MOD_NAME"]+"::"
            else:
                prefix = ""
            self._configuration[prefix+res["CNF_PARAM"]] = res["CNF_VAL"]
        self._state = self.CONF_LOAD_DB

    def get_entry(self, entry, module=None, widget=None):
        """
        Returns a entry of this core's configuration
        """
        if module is not None:
            prefix = module.get_name()+"::"
        elif widget is not None:
            prefix = widget.get_module().get_name()+"::"+str(widget.get_id())+"::"
        else:
            prefix = ""

        entry = prefix+entry    
        if entry in self._configuration.keys():
            return self._configuration[entry]
        raise ConfigurationException(ConfigurationException.get_msg(1))

    def set_entry(self, entry, value, module=None, widget=None):
        """
        Sets an entry of this core's configuration
        """
        if entry not in self._local_config_keys:
            db = self._core.get_db()
            if module is not None:
                stmnt = "SELECT CNF_PARAM, CNO_ID FROM CONFIG INNER JOIN CONFIGOWNERS ON (CNF_CNO_ID = CNO_ID) \
                            WHERE CNF_PARAM = ? AND CNO_MOD_ID = ? ;"
                res = db.query(self._core, stmnt, (str(entry), module.get_id()))
                row = res.fetchonemap()
                if row is not None:
                    cnf_relation_id = row["CNO_ID"]
                    stmnt = "UPDATE CONFIG SET CNF_VAL = ? WHERE CNF_CNO_ID = ? ;"
                    db.query(self._core, stmnt, (str(value), cnf_relation_id), commit=True)
                else:
                    cnf_relation_id = db.get_seq_next("CNO_GEN")
                    stmnt = "INSERT INTO CONFIGOWNERS (CNO_ID, CNO_MOD_ID, CNO_WGT_ID) VALUES (?,?,NULL) ;"
                    db.query(self._core, stmnt, (cnf_relation_id, module.get_id()),commit=True)
                    stmnt = "INSERT INTO CONFIG (CNF_PARAM, CNF_VAL, CNF_CNO_ID) VALUES (?,?,?) ;"
                    db.query(self._core, stmnt, (str(entry), str(value), str(cnf_relation_id)), commit=True)

            elif widget is not None:
                stmnt = "SELECT CNF_PARAM, CNO_ID FROM CONFIG INNER JOIN CONFIGOWNERS ON (CNF_CNO_ID = CNO_ID) \
                            WHERE CNF_PARAM = ? AND CNO_WGT_ID = ? ;"
                res = db.query(self._core, stmnt, (str(entry), widget.get_id()))
                row = res.fetchonemap()
                if row is not None:
                    cnf_relation_id = row["CNO_ID"]
                    stmnt = "UPDATE CONFIG SET CNF_VAL = ? WHERE CNF_CNO_ID = ? ;"
                    db.query(self._core, stmnt, (str(value), cnf_relation_id), commit=True)
                else:
                    cnf_relation_id = db.get_seq_next("CNO_GEN")
                    stmnt = "INSERT INTO CONFIGOWNERS (CNO_ID, CNO_MOD_ID, CNO_WGT_ID) VALUES (?,NULL,?) ;"
                    db.query(self._core, stmnt, (cnf_relation_id, widget.get_id()),commit=True)
                    stmnt = "INSERT INTO CONFIG (CNF_PARAM, CNF_VAL, CNF_CNO_ID) VALUES (?,?,?) ;"
                    db.query(self._core, stmnt, (str(entry), str(value), str(cnf_relation_id)), commit=True)

            else:
                stmnt = "SELECT CNF_PARAM, CNO_ID FROM CONFIG INNER JOIN CONFIGOWNERS ON (CNF_CNO_ID = CNO_ID) \
                            WHERE CNF_PARAM = ? AND CNO_MOD_ID IS NULL AND CNO_WGT_ID IS NULL;"
                res = db.query(self._core, stmnt, (str(entry),))
                row = res.fetchonemap()
                if row is not None:
                    cnf_relation_id = row["CNO_ID"]
                    stmnt = "UPDATE CONFIG SET CNF_VAL = ? WHERE CNF_CNO_ID = ? ;"
                    db.query(self._core, stmnt, (str(value), cnf_relation_id), commit=True)
                else:
                    cnf_relation_id = db.get_seq_next("CNO_GEN")
                    stmnt = "INSERT INTO CONFIGOWNERS (CNO_ID, CNO_MOD_ID, CNO_WGT_ID) VALUES (?,NULL,NULL) ;"
                    db.query(self._core, stmnt, (cnf_relation_id),commit=True)
                    stmnt = "INSERT INTO CONFIG (CNF_PARAM, CNF_VAL, CNF_CNO_ID) VALUES (?,?,?) ;"
                    db.query(self._core, stmnt, (str(entry), str(value), str(cnf_relation_id)), commit=True)
                
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
