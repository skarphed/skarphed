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
sys.path.append(LIBPATH)

from common.errors import UserException

class TestUserFunctions(CoreTestCase):
    def setUp(self):
        CoreTestCase.setUp(self)
        user_manager = self._core.get_user_manager()
        self.testuser = user_manager.create_user("testuser","testpassword")

    def test_create_user(self):
        user_manager = self._core.get_user_manager()
        user = user_manager.create_user("testuser2","testpassword")
        self.assertEqual(user.get_name(),"testuser2")

        stored_user = user_manager.get_user_by_name("testuser2")
        self.assertEqual(user_manager.get_user_by_name("testuser2").get_id(),user.get_id())

    def test_get_user_by_name(self):
        user_manager = self._core.get_user_manager()
        self.assertEqual(user_manager.get_user_by_name("testuser").get_id(),self.testuser.get_id())

    def test_get_user_by_id(self):
        nr = self.testuser.get_id()
        user_manager = self._core.get_user_manager()
        self.assertEqual(user_manager.get_user_by_id(nr).get_id(),self.testuser.get_id())        

    def test_authenticate(self):
        self.assertTrue(self.testuser.authenticate("testpassword"))

    def test_authenticate_false(self):
        try:
            self.testuser.authenticate("falsepassword")
        except UserException, e:
            pass
        else:
            self.assertFalse(True)

    def test_alter_password(self):
        self.testuser.alter_password("newtestpassword","testpassword")
        self.assertTrue(self.testuser.authenticate("newtestpassword"))
        self.testuser.alter_password("testpassword","newtestpassword")
        self.assertTrue(self.testuser.authenticate("testpassword"))

    def test_alter_password_false(self):
        try:
            self.testuser.alter_password("newtestpassword","falsepassword")
        except UserException, e:
            pass
        else:
            self.assertFalse(True)

    def tearDown(self):
        CoreTestCase.tearDown(self)
        self.testuser.delete()
