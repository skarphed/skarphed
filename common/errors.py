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

class SkarphedException(Exception):
    ERRORS = {}
    PREFIX = "GENERIC"
    def __init__(self, message):
        Exception.__init__(self, message)
        self.tracebackstring = None

    @classmethod
    def get_msg(cls,nr, info=""):
        return cls.PREFIX+"_"+str(nr)+": "+cls.ERRORS[nr]+" "+str(info)

    def set_tracebackstring(self, tb):
        self.tracebackstring = tb

    def get_tracebackstring(self):
        return self.tracebackstring
    
class UnknownCoreException(SkarphedException):pass
"""
If a exception comes from the core to the admingui via RPC.
it will be packed into this object to be passed on to the 
final "critical"-excepthook
"""

class ActionException(SkarphedException):
    """
    Exceptions for Database-Module
    """
    PREFIX = "ACT"
    ERRORS = {
        0:"""Action Exception"""        
    }


class BinaryException(SkarphedException):
    """
    Exceptions for Database-Module
    """
    PREFIX = "BIN"
    ERRORS = {
        0:"""Get By Id: The Binary with this ID does not exist: """,
        1:"""Get By MD5: No Binary found with the hash: """,
        2:"""Store: Not allowed to store this binary""",
        3:"""Get By Filename: No Binary found with the filename: """
    }

class ConfigurationException(SkarphedException):
    PREFIX = "CONF"
    ERRORS = {
        1:"""This Configurationentry does not exist!""",
        2:"""Can only override entries in database"""
    }

class CoreException(SkarphedException):
    PREFIX = "CORE"
    ERRORS = {
        1:"""Only the Configuration-class is authorized to access this variable""",
        2:"""There is no such render_mode as """
    }


class CSSException(SkarphedException):
    PREFIX = "CSS"
    ERRORS = {
        0:"""Get CSSPropertySet: This Widget does not exist""",
        1:"""Edit Value: The general propertyset does not have inherited values""",
        2:"""Invalid Propertyset: GENERAL type set must not have any Ids""",
        3:"""Invalid Propertyset: MODULE type set must not have any Ids but must have ModuleId""",
        4:"""Invalid Propertyset: WIDGET type set must not have any Ids but must have WidgetId""",
        5:"""Invalid Propertyset: SESSION type set must not have any Ids but must have Session""",
        6:"""Invalid Propertyset: Invalid type:"""
    }
    
class DatabaseException(SkarphedException):
    """
    Exceptions for Database-Module
    """
    PREFIX = "DB"
    ERRORS = {
        1:"""At least one Parameter for the Connection is missing""",
        2:"""Could not Query: No Connection""",
        3:"""Could not resolve Tables:"""
    }

class ModuleCoreException(SkarphedException):
    PREFIX = "CMOD"
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used""",
        1:"""This Widgets needs a module, to be saved into database""",
        2:"""Module could not be downloaded""",
        3:"""Module signature is not valid! Packet may be compromised""",
        4:"""Can't delete Repo with null-id! """,
        5:"""Module already exists!""",
        6:"""This module does not exist""",
        7:"""This widget does not exist""",
        8:"""Template Signature is not valid! Packet may be compromised""",
        9:"""Error HTTP-Requesting Repository""",
        10:"""Cant create a widget with an empty name"""
    }

class OperationException(SkarphedException):
    """
    Exceptions for Operation-Module
    """
    PREFIX = "OP"
    ERRORS = {
        0:"""Could not remove Lock!""",
    }

class PageException(Exception):
    PREFIX = "PAG"
    ERRORS = {
        0:"""Create: This Page has no spaces. As useless as you.""",
        1:"""Space: There is no space with that name."""
    }

class PermissionException(SkarphedException):
    """
    Exceptions for Permission-Module
    """
    PREFIX ="PERM"
    ERRORS = {
        0:"""Create Role: Can't save a role without Id""",
        1:"""Create Role: Can't save a role without a Name""",
        2:"""Create Role: This user is not allowed to create Roles""",
        3:"""Add Permission: This user is not allowed to modify Roles""",
        4:"""Add Permission: User Cannot edit a permission that he does not possess himself!""",
        5:"""Delete Role : This user is not allowed to delete Roles""",
        6:"""Grant Role: This user is not allowed to grant or revoke Roles""",
        7:"""Grant Role: You can only allow Roles you possess yourself OR roles, that can be made up of the permissions you own.""",
        8:"""This role does not seem to exist (Shouldnt happen)""",
        9:"""Permissions can only be checked of users or userIds""",
        10:"""Create Role: Cannot Create role without roleData""",
        11:"""Create Role: Cannot Create a role without a name""",
        12:"""Create Role: User is not permitted to create roles""",
        13:"""Create Role: This role already exists: """,
        14:"""Get Role: There is no role with this ID: """,
        15:"""Insufficient Permissions: User does not have permission """
    }

class PokeException(SkarphedException):
    """
    Exceptions that concern the Poke-system
    """
    PREFIX="POKE"
    ERRORS={
        0:"""There is no such ActivityType: """
    }

class ProfileException(SkarphedException):
    """
    Exceptions that may occur related to userprofiles in GUI
    """
    PREFIX ="PRO"
    ERRORS = {
        0:"""Profile already exists.""",
        1:"""No publickey defined!""",
        2:"""No privatekey defined!""",
        3:"""Profile does not exist.""",
        4:"""Wrong password!"""
    }

class RepositoryException(SkarphedException):
    PREFIX ="REPO"
    ERRORS = {
        100:"""Not a valid repository URL""",
        101:"""Port must be a number between 1 and 65535""",
        102:"""Hostname must not be empty"""
    }

class SessionException(SkarphedException):
    PREFIX ="SE"
    ERRORS = {
        0:"""SessionError: Session Expired""",
        1:"""SessionError: Can only attach user to session""",
        2:"""SessionError: This Session does not exist""",
        3:"""SessionError: Cannot Store a userless Session"""
    }

class TemplateException(SkarphedException):
    """
    Exceptions for Database-Module
    """
    PREFIX = "TPL"
    ERRORS = {
        0:"""At least one Parameter for the Connection is missing""",
        1:"""There is no Template at the moment"""        
    }

class UserException(SkarphedException):
    """
    Exceptions for User-Module
    """
    PREFIX = "USR"
    ERRORS = {
        0:"""The password has not been assigned properly. This shouldnt happen""",
        1:"""Could not set Password: Old password is wrong""",
        2:"""Authentication failed: Wrong Password""",
        3:"""This user is not authorized to delete users""",
        4:"""Granting Permission: This user is not allowed to grant permissions!""",
        5:"""Granting Permission: There is no such permission as """,
        6:"""A User cannot assign a permission that he does not possess himself""",
        7:"""Revoking Permission: This Sessionuser is not allowed to grant or revoke Permissions!""",
        8:"""A User cannot revoke a permission that he does not possess himself""",
        9:"""There is no user with the name """,
        10:"""Get Users: This user is not allowed to view users""",
        11:"""There is no user with the ID """,
        12:"""Cant create an user with an empty username""",
        13:"""Cant create an user with an empty password""",
        14:"""One does not simply delete the root user""",
        15:"""User already exists: """,
        16:"""One does not simply remove a permission from the root user"""
    }

class ViewException(SkarphedException):
    PREFIX = "VIE"
    ERRORS = {
        0:"""Get By Name: No such view""",
        1:"""Invalid input type to specify Space""",
        2:"""Invalid input type to specify Widget""",
        3:"""There is no default view""",
        4:"""Cannot set Parameters for Widget that is not in this view!""",
        5:"""A view must have a space-widget-mapping ('v')""",
        6:"""A view must have a page to render on ('s')""",
        7:"""This is not a valid view-JSON""",
        8:"""Each widget can only show up once in a view. This widget exists more than one time: """,
        9:"""This Box does not exist"""
    }

ERRORNAMES = {
    'SkarphedException':SkarphedException,
    'CoreException':CoreException,
    'CSSException':CSSException,
    'ActionException':ActionException,
    'BinaryException':BinaryException,
    'ConfigurationException':ConfigurationException,
    'DatabaseException':DatabaseException,
    'ModuleCoreException':ModuleCoreException,
    'OperationException':OperationException,
    'PageException':PageException,
    'PermissionException':PermissionException,
    'ProfileException':ProfileException,
    'RepositoryException':RepositoryException,
    'SessionException':SessionException,
    'TemplateException':TemplateException,
    'UserException':UserException,
    'ViewException':ViewException
}

def getAppropriateException(name):
    try:
        return ERRORNAMES[name]
    except KeyError:
        return None

def getCommonExceptions():
    return ERRORNAMES.values()
