import json

from database import DatabaseConnection

class Repository(object):
    def __init__(self):
        self.config = self.read_config('config.json')

    def read_config(self, path):
        with open(path, 'r') as f:
            config = json.loads(f.read())
            return config

    def establish_connection(self):
        self.connection = DatabaseConnection(
                self.config['db.ip'],
                self.config['db.name'],
                self.config['db.user'],
                self.config['db.password']
            )
        self.connection.connect()

    def get_all_modules(self):
        self.establish_connection()
        result = self.connection.execute('SELECT mod_displayname, mod_md5, mod_signature, mod_name,' +
                'mod_versionmajor, mod_versionminor, mod_versionrev ' +
				'FROM modules JOIN (SELECT mod_name vername ' +
				',MAX(mod_versionmajor*10000000 ' +
				'+mod_versionminor*100000 ' +
				'+mod_versionrev) ver ' +
				'FROM modules ' +
				'GROUP BY mod_name) ' + 
				'ON vername = mod_name ' + 
				'AND ver = mod_versionmajor*10000000 ' + 
				'+mod_versionminor*100000 ' +
				'+mod_versionrev')

        modules = [{'name' : m['mod_name'],
                    'hrname' : m['mod_displayname'],
                    'version_major' : m['mod_versionmajor'],
                    'version_minor' : m['mod_versionminor'],
                    'revision' : m['mod_versionrev'],
                    'signature' : m['mod_signature']} for m in result]
        return modules

    def get_versions_of_module(self, module):
        self.establish_connection()

        result = self.connection.execute('SELECT mod_name, mod_displayname, mod_signature, mod_id, ' +
                'mod_versionmajor, mod_versionminor, mod_versionrev ' +
                'FROM modules ' +
                'WHERE mod_name = %s;' % module['name'])
        modules = [{'name' : m['mod_name'],
                    'hrname' : m['mod_displayname'],
                    'version_major' : m['mod_versionmajor'],
                    'version_minor' : m['mod_versionminor'],
                    'revision' : m['mod_versionrev'],
                    'signature' : m['mod_signature']} for m in result]
        return modules

    def resolveDependenciesDownwards(self, module):
        self.establish_connection()
        result = self.connection.execute('SELECT mod_id ' + 
                'FROM modules ' +
                'WHERE mod_name = %s AND mod_versionmajor = %s AND mod_versionminor = %s AND ' +
                'mod_versionrev = %s AND mod_signature = %s;' %
                (module['name'], module['version_major'], module['version_minor'], module['revision'],
                module['signature']))
        if result:
           mod = result[0]
           modid = mod['mod_id']

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
