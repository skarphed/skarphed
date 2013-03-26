import base64
import hashlib
import json
import random

from database import DatabaseConnection

class Repository(object):
    def __init__(self):
        self.config = self.read_config('config.json')
        self.connection = None


    def read_config(self, path):
        with open(path, 'r') as f:
            config = json.loads(f.read())
            return config


    def verify_admin(self):
        # TODO check for admin
        pass


    def generate_salt(self):
        salt = ""
        length = random.randint(128, 255)
        for i in range(0, length):
            salt += chr(random.randint(0, 255))
        return salt


    def establish_connection(self):
        if not self.connection:
            self.connection = DatabaseConnection(
                    self.config['db.ip'],
                    self.config['db.name'],
                    self.config['db.user'],
                    self.config['db.password']
                )
            self.connection.connect()

    def close_connection(self):
        if self.connection:
            self.connection.disconnect()


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
                '+mod_versionrev;')

        modules = [{'name' : m['mod_name'],
                    'hrname' : m['mod_displayname'],
                    'version_major' : m['mod_versionmajor'],
                    'version_minor' : m['mod_versionminor'],
                    'revision' : m['mod_versionrev'],
                    'signature' : m['mod_signature']} for m in result]
        self.close_connection()
        return modules


    def get_versions_of_module(self, module):
        self.establish_connection()

        result = self.connection.execute('SELECT mod_name, mod_displayname, mod_signature, mod_id, ' +
                'mod_versionmajor, mod_versionminor, mod_versionrev ' +
                'FROM modules ' +
                'WHERE mod_name = \'%s\';' % module['name'])
        modules = [{'name' : m['mod_name'],
                    'hrname' : m['mod_displayname'],
                    'version_major' : m['mod_versionmajor'],
                    'version_minor' : m['mod_versionminor'],
                    'revision' : m['mod_versionrev'],
                    'signature' : m['mod_signature']} for m in result]
        self.close_connection()
        return modules


    def resolve_dependencies_downwards(self, module):
        self.establish_connection()
        # todo string formatting
        result = self.connection.execute('SELECT mod_id FROM modules WHERE mod_name = \'' + module['name'] + '\' AND mod_versionmajor = ' +
                str(module['version_major']) + ' AND mod_versionminor = ' + str(module['version_minor']) +
                ' AND mod_versionrev = ' + str(module['revision']) + ' AND mod_signature = \'' + module['signature'] + '\';')

        if result:
            mod_id = result[0]['mod_id']
            result = self.connection.execute('SELECT DISTINCT dep_mod_dependson ' +
                    'FROM dependencies ' +
                    'WHERE dep_mod_id = %d;' % mod_id)
            mod_ids = [mod_id]

            while result:
                for mod in result:
                    mod_ids.append(mod['dep_mod_dependson'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = self.connection.execute('SELECT dep_mod_dependson ' +
                        'FROM dependencies ' +
                        'WHERE dep_mod_id IN (%s) AND dep_mod_dependson NOT IN (%s);' % 
                        (mod_ids_str, mod_ids_str));

            result = self.connection.execute('SELECT mod_name, mod_displayname, mod_signature, mod_id, ' +
                    'mod_versionmajor, mod_versionminor, mod_versionrev ' +
                    'FROM modules WHERE mod_id IN (%s) AND mod_id != %d;' %
                    (','.join(map(str, mod_ids)), mod_id));
            modules = [{'name' : m['mod_name'],
                        'hrname' : m['mod_displayname'],
                        'version_major' : m['mod_versionmajor'],
                        'version_minor' : m['mod_versionminor'],
                        'revision' : m['mod_versionrev'],
                        'signature' : m['mod_signature']} for m in result]
            self.close_connection()
            return modules

        else:
            self.close_connection()
            raise Exception('Module does not exist: %s' % module['name'])


    def resolve_dependencies_upwards(self, module):
        self.establish_connection()
        # todo string formatting
        result = self.connection.execute('SELECT mod_id ' +
                'FROM modules ' +
                'WHERE mod_name = \'' + module['name'] + '\' AND mod_versionmajor = ' + str(module['version_major']) +
                ' AND mod_versionminor = ' + str(module['version_minor']) + ' AND mod_versionrev = ' +
                str(module['revision']) + ' AND mod_signature = \'' + module['signature'] + '\';')

        if result:
            mod_id = result[0]['mod_id']
            result = self.connection.execute('SELECT DISTINCT dep_mod_id ' +
                    'FROM dependencies ' +
                    'WHERE dep_mod_dependson = %d;' % mod_id);
            mod_ids = [mod_id]
            while result:
                for mod in result:
                    mod_ids.append(mod['dep_mod_id'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = self.connection.execute('SELECT dep_mod_id ' +
                        'FROM dependencies ' +
                        'WHERE dep_mod_dependson IN (%s) AND dep_mod_id NOT IN (%s);' %
                        (mod_ids_str, mod_ids_str))

            result = self.connection.execute('SELECT mod_name, mod_displayname, mod_signature, mod_id, ' +
                    'mod_versionmajor, mod_versionminor, mod_versionrev ' +
                    'FROM modules ' +
                    'WHERE mod_id IN (%s) and mod_id != %d;' %
                    (','.join(map(str, mod_ids)), mod_id))
            modules = [{'name' : m['mod_name'],
                        'hrname' : m['mod_displayname'],
                        'version_major' : m['mod_versionmajor'],
                        'version_minor' : m['mod_versionminor'],
                        'revision' : m['mod_versionrev'],
                        'signature' : m['mod_signature']} for m in result]
            self.close_connection()
            return modules
        else:
            self.close_connection()
            raise Exception('Module does not exist: %s' % module['name'])


    def download_module(self, module):
        self.establish_connection()
        result = self.connection.execute('SELECT mod_name, mod_displayname, mod_id, mod_versionmajor, ' +
                'mod_versionminor, mod_versionrev, mod_data, mod_signature ' +
                'FROM modules ' +
                'WHERE mod_name = \'' + module['name'] + '\' AND mod_versionmajor = ' + str(module['version_major']) +
                ' AND mod_versionminor = ' + str(module['version_minor']) + ' AND mod_versionrev = ' +
                str(module['revision']) + ' AND mod_signature = \'' + module['signature'] + '\';')

        if result:
            mod = result[0]
            # TODO fix reading from blob mod_data
            result_mod = {'name' : mod['mod_name'],
                        'hrname' : mod['mod_displayname'],
                        'version_major' : mod['mod_versionmajor'],
                        'version_minor' : mod['mod_versionminor'],
                        'revision' : mod['mod_versionrev'],
                        'signature' : mod['mod_signature']}
            self.close_connection()
            return (result_mod, mod['mod_data'])
        else:
            self.close_connection()
            raise Exception('Module does not exist: %s' % module['name'])


    def login(self, password):
        pass


    def logout(self, password):
        pass


    def change_password(self, password):
        self.verify_admin()
        
        self.establish_connection()
        salt = self.generate_salt()
        hashvalue = hashlib.sha512(password + salt).hexdigest()
        salt = base64.b64encode(salt)
        self.connection.execute('UPDATE config SET val = %s WHERE param = \'password\';' % hashvalue,
                commit = True)
        self.connection.execute('UPDATE config SET val = %s WHERE param = \'salt\';' % salt,
                commit = True)
        self.close_connection()
    

    def register_developer(self, name, fullname, publickey):
        self.verify_admin()

        self.establish_connection()
        dev_id = 0 # TODO get next dev id
        self.connection.execute('INSERT INTO developer (dev_id, dev_name, dev_fullname, dev_publickey) ' +
                'VALUES (%d, %s, %s, %s);' % (dev_id, name, fullname, publickey),
                commit = True)
        self.close_connection();


    def unregister_developer(self, dev_id):
        self.verify_admin()

        self.establish_connection()
        self.connection.execute('UPDATE developer SET dev_publickey = \'\' '
                'WHERE dev_id = %d;' % dev_id,
                commit = True)
        self.close_connection()


    def upload_module(self, signature):
        pass


    def delete_module(self, identifier, major=None, minor=None, revision=None):
        pass


    def get_developers(self):
        self.verify_admin()

        self.establish_connection()
        result = self.connection.execute('SELECT dev_id, dev_name, dev_fullname ' +
                'FROM developer;')
        developers = [{'devId' : d['dev_id'],
                        'name' : d['dev_name'],
                        'fullName' : d['dev_fullname']} for d in result]
        self.close_connection()
        return developers


    def get_public_key(self):
        self.establish_connection()
        result = self.connection.execute('SELECT val ' +
                'FROM config ' +
                'WHERE param = \'publickey\'')
        self.close_connection()
        
        if result:
            return result[0]['val']
        return None


    def get_private_key(self):
        self.establish_connection()
        result = self.connection.execute('SELECT val ' +
                'FROM config ' +
                'WHERE param = \'privatekey\'')
        self.close_connection()
        
        if result:
            return result[0]['val']
        return None
