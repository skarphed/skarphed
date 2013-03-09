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

import os

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

class CoreException(Exception):
    ERRORS = {
        1:"""Only the Configuration-class is authorized to access this variable"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "DB_"+str(nr)+": "+cls.ERRORS[nr]+" "+info


class Core(object):
    """
    The Core class is the interface to the world of Scoville
    """
    def __init__(self, core_config):
        """
        Initialize configuration and database-connection
        """
        self._core_config = core_config

        self._configuration = Configuration(self)
        self._database = Database(self)
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

    def get_core_config(self,obj):
        """
        Passes the core config on to the Configuration class.
        This is the only time in a scoville lifetime, that this happens.
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

    def get_name(self):
        return "de.masterprogs.scoville.core"

    def log(self, message):
        if hasattr(self,"environment"):
            print >> self.environment["wsgi.errors"] , "SCVDEBUG>>>"+str(message)

    def rpc_call(self, environment):
        if self.get_configuration().get_entry("core.debug") == True:
            self.environment = environment

        self.response_body = []
        self.response_header = []
        if environment.has_key("HTTP_COOKIE"):
            session_manager =  self.get_session_manager()
            cookies = environment["HTTP_COOKIE"].split("; ")
            sessioncookie = cookies[0].split("=")
            if sessioncookie[0] == "session_id":
                session_manager.set_current_session(session_manager.get_session(sessioncookie[1]))

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
        if environment.has_key("HTTP_COOKIE"):
            session_manager =  self.get_session_manager()
            cookies = environment["HTTP_COOKIE"].split("; ")
            sessioncookie = cookies[0].split("=")
            if sessioncookie[0] == "session_id":
                session_manager.set_current_session(session_manager.get_session(sessioncookie[1]))

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
            except ViewException:
                view = None # Maybe get some cool error-view in the future

        ext = view.render()
        self.log(type(ext))
        self.response_body.append(ext.encode('utf-8'))

        return {"body":self.response_body, "header":self.response_header}

