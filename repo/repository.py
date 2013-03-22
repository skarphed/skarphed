import json

class Repository(object):
    def __init__(self):
        self.config = read_config('config.json')

    def read_config(self, path):
        with open(path, 'r') as f:
            config = json.loads(f.read())

    def getAllModules(self):
        pass

    def getLatestVersion(self, module):
        pass

    def getVersionsOfModule(self, module):
        pass

    def resolveDependenciesDownwards(self, module):
        pass

    def resolveDependenciesUpwards(self, module):
        pass

    def downloadModule(self, module):
        pass

    def login(self, password):
        pass

    def logout(self, password):
        pass

    def changePassword(self, password):
        pass

    def registerDeveloper(self, name, fullname, publickey):
        pass

    def unregisterDeveloper(self, devid):
        pass

    def uploadModule(self, signature):
        pass

    def deleteModule(self, identifier, major=None, minor=None, revision=None):
        pass

    def getDevelopers(self):
        pass
