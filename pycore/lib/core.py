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

from configuration import Configuration
from database import Database
from user import UserManager
from permissions import PermissionManager
from operation import OperationManager
from module import ModuleManager

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

        self._configuration = Configuration()
        self._database = Database()
        self._user_manager = None
        self._permission_manager = None
        self._operation_manager = None
        self._module_manager = None

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

    def get_operation_manager(self):
        if self._operation_manager is None:
            self._operation_manager = OperationManager(self)
        return self._operation_manager

    def get_module_manager(self):
        if self._module_manager is None:
            self._module_manager = ModuleManager(self)
        return self._module_manager
        
    def get_name(self):
        return "de.masterprogs.scoville.core"
