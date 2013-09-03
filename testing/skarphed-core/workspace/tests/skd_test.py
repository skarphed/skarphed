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

import sys
import os
import unittest

cfgfile = open("/etc/skarphed/skarphed.conf","r").read().split("\n")
cfg = {}
for line in cfgfile:
    if line.startswith("#") or line.find("=") == -1:
        continue
    key, value = line.split("=")
    cfg[key]=value

del(cfgfile)

LIBPATH=cfg["SCV_LIBPATH"]

class CoreTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        cfgfile = open("/etc/skarphed/skarphed.conf","r").read().split("\n")
        cfg = {}
        for line in cfgfile:
            if line.startswith("#") or line.find("=") == -1:
                continue
            key, value = line.split("=")
            cfg[key]=value

        del(cfgfile)

        #HERE BE DRAGONS:
        #Currently only supports one testinstance with the instanceID 0
        p = cfg["SCV_WEBPATH"]+"0"
        sys.path.append(p)

        from instanceconf import SCV_INSTANCE_SCOPE_ID
        cfg["SCV_INSTANCE_SCOPE_ID"] = SCV_INSTANCE_SCOPE_ID

        sys.path.append(cfg["SCV_LIBPATH"])

        from scv import Core

        self._core = Core(cfg)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def setSessionUser(self, permissions=[]):
        """
        Set a sessionuser and give him a list of permissions
        """
        if type(permissions)!=list:
            permissions = [permissions]

        user_manager = self._core.get_user_manager()
        session_user = user_manager.create_user("session_user","password")
        session_manager = self._core.get_session_manager()
        session = session_manager.create_session(session_user)
        session_manager.set_current_session(session)
        for permission in permissions:
            session_user.grant_permission(permission,ignore_check=True)
        self._session_user = session_user
        self._session = session

    def unsetSessionUser(self):
        session_manager.set_current_session(None)
        self._session.delete()
        self._session_user.delete()

    def assertFail(self, msg=""):
        """
        Execute assertFail() to let a test fail instantly
        """
        self.assertTrue(False,msg)

    def setUpTestModule(self):
        """
        Set up a module in the database for testing purposes.
        Returns the generated module.
        """
        db = self._core.get_db()
        nr = db.get_seq_next("MOD_GEN")
        stmnt = "INSERT INTO MODULES (MOD_ID, MOD_NAME, MOD_DISPLAYNAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_JSMANDATORY) \
                      VALUES (?,?,?,?,?,?,?) ;"
        db.query(self._core,stmnt,(nr,"testprogrammer_testmodule","TestModule",
                                   10,11,
                                   1337,common.enums.JSMandatory.NO),
                 commit=True)
        module_manager = self._core.get_module_manager()
        return module_manager.get_module(nr)

    def tearDownTestModule(self, module=None):
        """
        Tear down a testmodule and erase it from the database.
        Removes every module if called without parameters.
        if parameter module is given, removes only that module
        """
        db = self._core.get_db()
        if module is None:
            db.query(self._core,"DELETE FROM MODULES;",commit=True)
        else:
            stmnt = "DELETE FROM MODULES WHERE MOD_ID = ? ;"
            db.query(self._core,stmnt,(module.get_id(),),commit=True)
        return
