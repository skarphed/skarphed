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
sys.path.append(cfg["SCV_LIBPATH"])

import common as _common
common = _common

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
