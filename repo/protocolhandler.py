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
    def __init__(self, jsonstr):
        self.repository = Repository()
        self.subject = json.loads(jsonstr)

    def verify_module(self):
        try:
            module = self.subject['m']
            if None in [val for (key,val) in module if key not in ['name', 'hrname', 'version_major', 'version_minor', 'revision', 'signature']]:
                raise Exception('Not a valid module!')
        except KeyError, e:
            raise Exception('Not a valid module!')

    def execute(self):
        c = self.subject['c']
        if c == CommandType.GET_ALL_MODULES:
            modules = self.repository.get_all_modules()
            return json.dumps({'r' : modules})
        elif c == CommandType.GET_VERSIONS_OF_MODULE:
            self.verify_module()
            modules = self.repository.get_versions_of_module(self.subject['m'])
            return json.dumps({'r' : modules})
        elif c == CommandType.RESOLVE_DEPENDENCIES_DOWNWARDS:
            pass
        elif c == CommandType.RESOLVE_DEPENDENCIES_UPWARDS:
            pass
        elif c == CommandType.DOWNLOAD_MODULE:
            pass
        elif c == CommandType.GET_PUBLICKEY:
            pass
        elif c == CommandType.GET_LATEST_VERSION:
            pass
        
        elif c == CommandType.LOGIN:
            pass
        elif c == CommandType.LOGOUT:
            pass
        elif c == CommandType.CHANGE_PASSWORD:
            pass
        elif c == CommandType.REGISTER_DEVELOPER:
            pass
        elif c == CommandType.UNREGISTER_DEVELOPER:
            pass
        elif c == CommandType.UPLOAD_MODULE:
            pass
        elif c == CommandType.DELETE_MODULE:
            pass
        elif c == CommandType.GET_DEVELOPERS:
            pass
