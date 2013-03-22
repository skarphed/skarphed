import json

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
    def __init__(self, json):
        self.repository = Repository()
        self.subject = json.loads(json)

    def execute(self):
        c = subject['c']
        if c == CommandType.GET_ALL_MODULES:
        elif c == CommandType.GET_VERSIONS_OF_MODULE:
        elif c == CommandType.RESOLVE_DEPENDENCIES_DOWNWARDS:
        elif c == CommandType.RESOLVE_DEPENDENCIES_UPWARDS:
        elif c == CommandType.DOWNLOAD_MODULE:
        elif c == CommandType.GET_PUBLICKEY:
        elif c == CommandType.GET_LATEST_VERSION:
        
        elif c == CommandType.LOGIN:
        elif c == CommandType.LOGOUT:
        elif c == CommandType.CHANGE_PASSWORD:
        elif c == CommandType.REGISTER_DEVELOPER:
        elif c == CommandType.UNREGISTER_DEVELOPER:
        elif c == CommandType.UPLOAD_MODULE:
        elif c == CommandType.DELETE_MODULE:
        elif c == CommandType.GET_DEVELOPERS:
