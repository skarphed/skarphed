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

import base64
import json

from repository import *

class CommandType:
    """
    An enumeration of all command ids that can be passed via the "c" key of
    the request json.
    """
    #calls from skarphed to repository
    GET_ALL_MODULES = 1
    GET_VERSIONS_OF_MODULE = 2
    RESOLVE_DEPENDENCIES_DOWNWARDS = 3
    RESOLVE_DEPENDENCIES_UPWARDS = 4
    DOWNLOAD_MODULE = 5
    GET_PUBLICKEY = 6
    GET_LATEST_VERSION = 7
    GET_ALL_TEMPLATES = 8
    DOWNLOAD_TEMPLATE = 9
    
    #calls from admin-gui to repository
    LOGIN = 100
    LOGOUT = 101
    CHANGE_PASSWORD = 102
    REGISTER_DEVELOPER = 103
    UNREGISTER_DEVELOPER = 104
    UPLOAD_MODULE = 105
    DELETE_MODULE = 106
    GET_DEVELOPERS = 107
    UPLOAD_TEMPLATE = 108
    DELETE_TEMPLATE = 109

class ProtocolHandler(object):
    """
    The protocol handler verifies that a json request are wellformatted and delegates the request
    to the repository. The results of the repository will be converted to a json response.
    """

    def __init__(self, repository, jsonstr):
        """
        Initializes a protocol handler with a repository and the incoming request.
        """
        self.repository = repository
        try:
            self.subject = json.loads(jsonstr)
        except ValueError, e:
            raise create_repository_exception(RepositoryErrorCode.INVALID_JSON)

    def verify_module(self, need_signature=True):
        """
        Verifies that the json 'm' key's value is a valid modules, that means it contains the following keys:
        name, hrname, version_major, version_minor, revision, signature
        """
        try:
            module = self.subject['m']
            keys = ['name', 'hrname', 'version_major', 'version_minor', 'revision']
            if need_signature:
                keys.append('signature')
            if not all([module[key] != None for key in keys]):
                raise create_repository_exception(RepositoryErrorCode.INVALID_JSON)
        except KeyError, e:
            raise create_repository_exception(RepositoryErrorCode.INVALID_JSON)


    def check_set(self, keys, errmsg):
        """
        Check whether the specified keys are set in the request json. If not an exception
        with the given error message will be thrown.
        """
        try:
            if not all([self.subject[key] != None for key in keys]):
                raise create_repository_exception(RepositoryErrorCode.INVALID_JSON)
        except KeyError, e:
            raise create_repository_exception(RepositoryErrorCode.INVALID_JSON)

    def execute(self, environ):
        """
        Executes the request and returns a json response. If the specified command is unknown an exception
        will be thrown.
        """
        c = self.subject['c']
        if c == CommandType.GET_ALL_MODULES:
            modules = self.repository.get_all_modules(environ)
            return json.dumps({'r' : modules})

        elif c == CommandType.GET_VERSIONS_OF_MODULE:
            self.verify_module()
            modules = self.repository.get_versions_of_module(environ, self.subject['m'])
            return json.dumps({'r' : modules})

        elif c == CommandType.RESOLVE_DEPENDENCIES_DOWNWARDS:
            self.verify_module()
            modules = self.repository.resolve_dependencies_downwards(environ, self.subject['m'])
            return json.dumps({'r' : modules})
        
        elif c == CommandType.RESOLVE_DEPENDENCIES_UPWARDS:
            self.verify_module()
            modules = self.repository.resolve_dependencies_upwards(environ, self.subject['m'])
            return json.dumps({'r' : modules})
        
        elif c == CommandType.DOWNLOAD_MODULE:
            self.verify_module()
            (module, data) = self.repository.download_module(environ, self.subject['m'])
            return json.dumps({'r' : module, 'data' : data})
        
        elif c == CommandType.GET_PUBLICKEY:
            publickey = self.repository.get_public_key(environ)
            return json.dumps({'r' : publickey})
        
        elif c == CommandType.GET_LATEST_VERSION:
            self.verify_module(False)
            module = self.repository.get_latest_version(environ, self.subject['m'])
            return json.dumps({'r' : module})

        elif c == CommandType.GET_ALL_TEMPLATES:
            templates = self.repository.get_all_templates(environ)
            return json.dumps({'r' : templates})

        elif c == CommandType.DOWNLOAD_TEMPLATE:
            self.check_set(['id'], 'Template id missing')
            (data, signature) = self.repository.download_template(environ, self.subject['id'])
            return json.dumps({'r' : data, 'signature' : signature})
        
        elif c == CommandType.LOGIN:
            self.check_set(['dxd'], 'Password not set')
            self.repository.login(environ, self.subject['dxd'])
            return json.dumps({'r' : 0})
             
        elif c == CommandType.LOGOUT:
            self.repository.logout(environ)
            return json.dumps({'r' : 0})

        elif c == CommandType.CHANGE_PASSWORD:
            self.check_set(['dxd'], 'Password not set')
            self.repository.change_password(environ, self.subject['dxd'])
            return json.dumps({'r' : 0})
        
        elif c == CommandType.REGISTER_DEVELOPER:
            self.check_set(['name', 'fullName', 'publicKey'], 'Invalid registration data')
            self.repository.register_developer(environ, self.subject['name'], self.subject['fullName'],
                    self.subject['publicKey'])
            return json.dumps({'r' : 0})
        
        elif c == CommandType.UNREGISTER_DEVELOPER:
            self.check_set(['devId'], 'Need developer id')
            self.repository.unregister_developer(environ, self.subject['devId'])
            return json.dumps({'r' : 0})
        
        elif c == CommandType.UPLOAD_MODULE:
            self.check_set(['data', 'signature'], 'Not valid data')
            self.repository.upload_module(environ, base64.b64decode(self.subject['data']),
                    base64.b64decode(self.subject['signature']))
            return json.dumps({'r' : 0})
        
        elif c == CommandType.DELETE_MODULE:
            self.check_set(['moduleIdentifier'], 'Need module to delete')
            self.repository.delete_module(environ, self.subject['moduleIdentifier'])
            return json.dumps({'r' : 0})
        
        elif c == CommandType.GET_DEVELOPERS:
            developers = self.repository.get_developers(environ)
            return json.dumps({'r' : developers})

        elif c == CommandType.UPLOAD_TEMPLATE:
            self.check_set(['data', 'signature'], 'Not valid data')
            self.repository.upload_template(environ, base64.b64decode(self.subject['data']),
                    base64.b64decode(self.subject['signature']))
            return json.dumps({'r' : 0})

        elif c == CommandType.DELETE_TEMPLATE:
            self.check_set(['id'], 'Need template to delete')
            self.repository.delete_template(environ, self.subject['id'])
            return json.dumps({'r' : 0})

        else:
            raise create_repository_exception(RepositoryErrorCode.INVALID_JSON)
