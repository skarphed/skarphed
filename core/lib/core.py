#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import os
import logging

from configuration import Configuration
from database import Database
from users import UserManager
from permissions import PermissionManager
from operation import OperationManager
from module import ModuleManager
from session import SessionManager
from css import CSSManager
from action import ActionManager
from binary import BinaryManager
from view import ViewManager, PageManager, ViewException
from rpc import Rpc
from template import TemplateManager
from pki import PkiManager

from maintenance import MAINTENANCE_HTML

from common.errors import CoreException

class Core(object):
    """
    The Core class is the interface to the world of Skarphed
    """
    def __init__(self, core_config):
        """
        Initialize configuration and database-connection
        """
        self._core_config = core_config

        self._configuration = Configuration(self)
        self._database = Database(self)
        self._configuration.init_from_db()
        self._user_manager = None
        self._permission_manager = None
        self._operation_manager = None
        self._module_manager = None
        self._session_manager = None
        self._css_manager = None
        self._action_manager = None
        self._binary_manager = None
        self._view_manager = None
        self._page_manager = None
        self._template_manager = None
        self._pki_manager = None

    def get_core_config(self,obj):
        """
        Passes the core config on to the Configuration class.
        This is the only time in a skarphed lifetime, that this happens.
        """
        if obj.__class__.__name__ != "Configuration":
            raise CoreException(CoreException.get_msg(1))
        else:
            return self._core_config

    def get_configuration(self):
        """
        Returns the instance of Configuration
        """
        return self._configuration

    def get_db(self):
        return self._database

    def get_user_manager(self):
        if self._user_manager is None:
            self._user_manager = UserManager(self)
        return self._user_manager

    def get_permission_manager(self):
        if self._permission_manager is None:
            self._permission_manager = PermissionManager(self)
        return self._permission_manager

    def get_session_manager(self):
        if self._session_manager is None:
            self._session_manager = SessionManager(self)
        return self._session_manager

    def get_operation_manager(self):
        if self._operation_manager is None:
            self._operation_manager = OperationManager(self)
        return self._operation_manager

    def get_module_manager(self):
        if self._module_manager is None:
            self._module_manager = ModuleManager(self)
        return self._module_manager
     
    def get_css_manager(self):
        if self._css_manager is None:
            self._css_manager = CSSManager(self)
        return self._css_manager

    def get_action_manager(self):
        if self._action_manager is None:
            self._action_manager = ActionManager(self)
        return self._action_manager

    def get_binary_manager(self):
        if self._binary_manager is None:
            self._binary_manager = BinaryManager(self)
        return self._binary_manager

    def get_view_manager(self):
        if self._view_manager is None:
            self._view_manager = ViewManager(self)
        return self._view_manager

    def get_page_manager(self):
        if self._page_manager is None:
            self._page_manager = PageManager(self)
        return self._page_manager

    def get_template_manager(self):
        if self._template_manager is None:
            self._template_manager = TemplateManager(self)
        return self._template_manager

    def get_pki_manager(self):
        if self._pki_manager is None:
            self._pki_manager = PkiManager(self)
        return self._pki_manager

    def get_name(self):
        return "de.masterprogs.skarphed.core"

    def log(self, message):
        if hasattr(self,"environment"):
            print >> self.environment["wsgi.errors"] , "SCVDEBUG>>>"+str(message)
        else:
            if not hasattr(self, "logging_initialized"):
                configuration = self.get_configuration()
                logging.basicConfig(filename=configuration.get_entry("core.webpath")+"/generic.log",level=logging.DEBUG)
                self.logging_initialized = True
            
            logging.debug(message)

    def activate_maintenance_mode(self):
        configuration = self.get_configuration()
        configuration.set_entry("core.maintenance_mode", "True")

    def deactivate_maintenance_mode(self):
        configuration = self.get_configuration()
        configuration.set_entry("core.maintenance_mode", "False")

    def set_rendermode(self, mode):
        if not mode in ("pure", "ajax"):
            raise CoreException(CoreException.get_msg(2,mode))

        configuration = self.get_configuration()
        configuration.set_entry("core.rendermode", mode)

    def get_rendermode(self):
        configuration = self.get_configuration()
        return configuration.get_entry("core.rendermode")

    def is_maintenance_mode(self):
        configuration = self.get_configuration()
        val = configuration.get_entry("core.maintenance_mode")
        return val == "True"

    def rpc_call(self, environment):
        if self.get_configuration().get_entry("core.debug") == True:
            self.environment = environment

        self.response_body = []
        self.response_header = []
        if environment.has_key("HTTP_COOKIE"):
            session_manager =  self.get_session_manager()
            session_manager.set_current_session(session_manager.get_session(environment['HTTP_COOKIE']))

        try:
            request_body_size = int(environment.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environment['wsgi.input'].read(request_body_size)

        rpc = Rpc(self)
        rpc(request_body)

        return {"body":self.response_body, "header":self.response_header}

    def web_call(self, environment):
        if self.get_configuration().get_entry("core.debug") == True:
            self.environment = environment

        self.response_body = []
        self.response_header = []

        if self.is_maintenance_mode():
            self.response_body.append(MAINTENANCE_HTML.encode('utf-8'))
            return {"body":self.response_body,"header":self.response_header}

        if environment.has_key("HTTP_COOKIE"):
            session_manager =  self.get_session_manager()
            session_manager.set_current_session(session_manager.get_session(environment['HTTP_COOKIE']))

        view_manager = self.get_view_manager()

        if environment["PATH_INFO"] in ("/",""):
            view = view_manager.get_default_view()
        else:
            view = None

        viewname = environment["PATH_INFO"].replace("/web/","",1)

        if len(viewname) > 0 and view is None:
            try:
                view = view_manager.get_from_name(viewname)
            except ViewException:
                view = None
        
        if view is None:
            try:
                view = view_manager.get_from_json(environment["QUERY_STRING"])
            except ViewException, e:
                self.log(str(e)+"Q:: "+environment["QUERY_STRING"])
                view = None # Maybe get some cool error-view in the future


        ext = view.render(environment)

        self.response_body.append(ext.encode('utf-8'))

        return {"body":self.response_body, "header":self.response_header}
