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

from skd_test import CoreTestCase
from skd_test import LIBPATH
import sys
import os
sys.path.append(LIBPATH)

from common.errors import TemplateException

class TestViewFunctions(CoreTestCase):
    def setUp(self):
        CoreTestCase.setUp(self)

    def test_install_template(self):
        testpermissions = ["skarphed.sites.create",
                           "skarphed.sites.delete",
                           "skarphed.sites.modify"]
        self.setSessionUser(testpermissions)

        templatefile = open("testdata/default_template.tgz","r")
        templatedata = templatefile.read()
        templatefile.close()

        template_manager = self._core.get_template_manager()
        self.assertFalse(template_manager.is_template_installed())

        template_manager.install_from_data(templatedata)

        self.assertTrue(template_manager.is_template_installed())
        self.unsetSessionUser()

    def tearDown(self):
        CoreTestCase.tearDown(self)
