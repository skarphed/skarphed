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

import base64
import json

from repository import Repository

class CommandType:
    #calls from scoville to repository
    GET_ALL_MODULES = 1
    GET_VERSIONS_OF_MODULE = 2
    RESOLVE_DEPENDENCIES_DOWNWARDS = 3
    RESOLVE_DEPENDENCIES_UPWARDS = 4
    DOWNLOAD_MODULE = 5
    GET_PUBLICKEY = 6
    GET_LATEST_VERSION = 7
    
    #calls from admin-gui to repository
    LOGIN = 100
    LOGOUT = 101
    CHANGE_PASSWORD = 102
    REGISTER_DEVELOPER = 103
    UNREGISTER_DEVELOPER = 104
    UPLOAD_MODULE = 105
    DELETE_MODULE = 106
    GET_DEVELOPERS = 107

class ProtocolHandler(object):
    def __init__(self, repository, jsonstr, response_header):
        logfile = open('/tmp/scvrepolog.log','a')
        logfile.write(jsonstr+"\n")
        logfile.close()
        self.repository = repository
        self.subject = json.loads(jsonstr)
        self.response_header = response_header

    def verify_module(self):
        try:
            module = self.subject['m']
            if not all([module[key] != None for key in ['name', 'hrname', 'version_major', 'version_minor', 'revision', 'signature']]):
                raise Exception('Not a valid module!')
        except KeyError, e:
            raise Exception('Not a valid module!')


    def check_set(self, keys, errmsg):
        try:
            if not all([self.subject[key] != None for key in keys]):
                raise Exception(errmsg)
        except KeyError, e:
            raise Exception(errmsg)

    def execute(self, environ):
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
            return json.dumps({'r' : module, 'data' : base64.b64encode(data)})
        
        elif c == CommandType.GET_PUBLICKEY:
            publickey = self.repository.get_public_key(environ)
            return json.dumps({'r' : publickey})
        
        elif c == CommandType.GET_LATEST_VERSION:
            self.verify_module()
            module = self.repository.get_latest_version(environ, self.subject['m'])
            return json.dumps({'r' : module})
        
        elif c == CommandType.LOGIN:
            self.check_set(['dxd'], 'Password not set')
            if self.repository.login(environ, self.subject['dxd'], self.response_header):
                return json.dumps({'r' : 0})
            return json.dumps({'r' : 1})
        
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

        else:
            raise Exception('Unknown command identifier: %d' % subject['c'])
