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
        """
        Instals and tears down a correct template
        """
        testpermissions = ["skarphed.sites.create",
                           "skarphed.sites.delete",
                           "skarphed.sites.modify"]
        self.setSessionUser(testpermissions)

        templatefile = open("testdata/default_template.tgz","r")
        templatedata = templatefile.read()
        templatefile.close()

        template_manager = self._core.get_template_manager()
        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        errorlog = template_manager.install_from_data(templatedata)

        self.assertEqual(errorlog,[])
        self.assertTrue(template_manager.is_template_installed())

        template = template_manager.get_current_template()
        self.assertIsNotNone(template)

        template.uninstall()
        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()
        self.assertFalse(template_manager.is_template_installed())        

        self.unsetSessionUser()

    def test_install_incomplete_template(self):
        """
        Tries installing a defective module that lacks some files
        """
        testpermissions = ["skarphed.sites.create",
                           "skarphed.sites.delete",
                           "skarphed.sites.modify"]
        self.setSessionUser(testpermissions)

        templatefile = open("testdata/default_template_incomplete.tgz","r")
        templatedata = templatefile.read()
        templatefile.close()

        template_manager = self._core.get_template_manager()
        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        errorlog = template_manager.install_from_data(templatedata)

        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        self.assertEqual([{'severity':1,
                               'type':'PageFile',
                               'msg':'File not in Package mainsite.html'}],errorlog)
        self.unsetSessionUser()


    def test_install_corrupt_manifest(self):
        """
        Tries installing a template with a defective manifest
        """
        testpermissions = ["skarphed.sites.create",
                           "skarphed.sites.delete",
                           "skarphed.sites.modify"]
        self.setSessionUser(testpermissions)

        templatefile = open("testdata/default_template_corrupt.tgz","r")
        templatedata = templatefile.read()
        templatefile.close()

        template_manager = self._core.get_template_manager()
        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        errorlog = template_manager.install_from_data(templatedata)

        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        self.assertEqual([{'severity':1,
                           'type':'PackageFile',
                           'msg':'JSON seems to be corrupt'}],errorlog)
        self.unsetSessionUser()

    def test_install_multiple_errors(self):
        """
        Tries to install a template that has various malfunctions
        """
        testpermissions = ["skarphed.sites.create",
                           "skarphed.sites.delete",
                           "skarphed.sites.modify"]
        self.setSessionUser(testpermissions)

        templatefile = open("testdata/default_template_multiple.tgz","r")
        templatedata = templatefile.read()
        templatefile.close()

        template_manager = self._core.get_template_manager()
        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        errorlog = template_manager.install_from_data(templatedata)

        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        self.assertEqual([{'severity':1,
                           'type':'PackageFile',
                           'msg':'File not in Package general.css'},
                          {'severity': 1, 
                           'type': 'CSS-Data', 
                           'msg': "General CSS File does not Contain Valid CSS local variable 'general_css' referenced before assignment"},
                          {'severity':1,
                           'type':'PageData',
                           'msg':'Invalid format (allowed is .html and .htm: corruptsite.xml'},
                          {'severity':1,
                           'type':'PageFile',
                           'msg':'File not in Package corruptsite.xml'}],errorlog)
        self.unsetSessionUser()

    def test_install_missing_pagecss(self):
        """
        Tries to install a template with a page that has no CSS file
        """
        testpermissions = ["skarphed.sites.create",
                           "skarphed.sites.delete",
                           "skarphed.sites.modify"]
        self.setSessionUser(testpermissions)

        templatefile = open("testdata/default_template_nopagecss.tgz","r")
        templatedata = templatefile.read()
        templatefile.close()

        template_manager = self._core.get_template_manager()
        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        errorlog = template_manager.install_from_data(templatedata)

        self.assertFalse(template_manager.is_template_installed())

        try:
            template_manager.get_current_template()
        except TemplateException:
            pass
        else:
            self.assertFail()

        self.assertEqual([{'severity':1,
                               'type':'PageFile',
                               'msg':'File not in Package static/mainsite.css'}],errorlog)
        self.unsetSessionUser()

    def tearDown(self):
        CoreTestCase.tearDown(self)
