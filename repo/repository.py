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
import cStringIO
import hashlib
import json
import random
import tarfile

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from database import DatabaseConnection

from session import Session

class Repository(object):
    def __init__(self, environ):
        self.environ = environ
        self.config = self.read_config('/etc/scvrepo/config.json')
        self.connection = DatabaseConnection(
                self.config['db.ip'],
                self.config['db.name'],
                self.config['db.user'],
                self.config['db.password']
            )
        self.connection.connect()

    
    def __del__(self):
        if self.connection:
            self.connection.disconnect()

    def get_db(self):
        return self.connection

    def read_config(self, path):
        f = open(path, 'r')
        config = json.loads(f.read())
        f.close()
        return config


    def verify_admin(self):
        # TODO use own session class, get rid of beaker
        try:
            if not self.environ['beaker.session']['privileged']:
                raise Exception('You are no admin')
        except Exception, e:
            raise Exception('You are no admin')


    def generate_salt(self):
        salt = ""
        length = random.randint(128, 255)
        for i in range(0, length):
            salt += chr(random.randint(0, 255))
        return salt


    def get_all_modules(self):
        result = self.connection.query('SELECT MOD_DISPLAYNAME, MOD_MD5, MOD_SIGNATURE, MOD_NAME, \
                MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV \
                FROM MODULES JOIN (SELECT MOD_NAME VERNAME \
                ,MAX(MOD_VERSIONMAJOR*10000000 \
                +MOD_VERSIONMINOR*100000 \
                +MOD_VERSIONREV) vER \
                FROM MODULES \
                GROUP BY MOD_NAME) \ 
                ON VERNAME = MOD_NAME \ 
                AND VER = MOD_VERSIONMAJOR*10000000 \ 
                +MOD_VERSIONMINOR*100000 \
                +MOD_VERSIONREV;')
        result = result.fetchallmap()
        modules = [{'name' : m['MOD_NAME'],
                    'hrname' : m['MOD_DISPLAYNAME'],
                    'version_major' : m['MOD_VERSIONMAJOR'],
                    'version_minor' : m['MOD_VERSIONMINOR'],
                    'revision' : m['MOD_VERSIONREV'],
                    'signature' : m['MOD_SIGNATURE']} for m in result]
        return modules


    def get_versions_of_module(self, module):
        result = self.connection.query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, ' +
                'MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV ' +
                'FROM MODULES ' +
                'WHERE MOD_NAME = ?;', module['name'])
        result = result.fetchallmap()
        modules = [{'name' : m['MOD_NAME'],
                    'hrname' : m['MOD_DISPLAYNAME'],
                    'version_major' : m['MOD_VERSIONMAJOR'],
                    'version_minor' : m['MOD_VERSIONMINOR'],
                    'revision' : m['MOD_VERSIONREV'],
                    'signature' : m['MOD_SIGNATURE']} for m in result]
        return modules


    def resolve_dependencies_downwards(self, module):
        result = self.connection.query('SELECT MOD_ID FROM MODULES WHERE MOD_NAME = ? ' +
                'AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? AND MOD_VERSIONREV = ? ' +
                'AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod_id = result[0]['MOD_ID']
            result = self.connection.query('SELECT DISTINCT DEP_MOD_DEPENDSOn ' +
                    'FROM DEPENDENCIES ' +
                    'WHERE DEP_MOD_ID = ?;', mod_id)
            result = result.fetchallmap()
            mod_ids = [mod_id]

            while result:
                for mod in result:
                    mod_ids.append(mod['DEP_MOD_DEPENDSOn'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = self.connection.query('SELECT DEP_MOD_DEPENDSON ' +
                        'FROM DEPENDENCIES ' +
                        'WHERE DEP_MOD_ID IN ? AND DEP_MOD_DEPENDSON NOT IN ?;', 
                        (mod_ids_str, mod_ids_str));
                result = result.fetchallmap()
            result = self.connection.query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, ' +
                    'MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV ' +
                    'FROM MODULES WHERE MOD_ID IN (?) AND MOD_ID != ?;', 
                    (','.join(map(str, mod_ids)), mod_id));
            result = result.fetchallmap()
            modules = [{'name' : m['MOD_NAME'],
                        'hrname' : m['MOD_DISPLAYNAME'],
                        'version_major' : m['MOD_VERSIONMAJOR'],
                        'version_minor' : m['MOD_VERSIONMINOR'],
                        'revision' : m['MOD_VERSIONREV'],
                        'signature' : m['MOD_SIGNATURE']} for m in result]
            return modules

        else:
            raise Exception('Module does not exist: %s' % module['name'])


    def resolve_dependencies_upwards(self, module):
        result = self.connection.query('SELECT MOD_ID ' +
                'FROM MODULES ' +
                'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? ' +
                'AND MOD_VERSIONREV = ? AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod_id = result[0]['MOD_ID']
            result = self.connection.query('SELECT DISTINCT DEP_MOD_ID ' +
                    'FROM DEPENDENCIES ' +
                    'WHERE DEP_MOD_DEPENDSON = ?;', mod_id);
            result = result.fetchallmap()
            mod_ids = [mod_id]
            while result:
                for mod in result:
                    mod_ids.append(mod['DEP_MOD_ID'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = self.connection.query('SELECT DEP_MOD_ID ' +
                        'FROM DEPENDENCIES ' +
                        'WHERE DEP_MOD_DEPENDSON IN ? AND DEP_MOD_ID NOT IN ?;',
                        (mod_ids_str, mod_ids_str))
                result = result.fetchallmap()

            result = self.connection.query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, ' +
                    'MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV ' +
                    'FROM MODULES ' +
                    'WHERE MOD_ID IN (?) AND MOD_ID != ?;',
                    (','.join(map(str, mod_ids)), mod_id))
            result = result.fetchallmap()
            modules = [{'name' : m['MOD_NAME'],
                        'hrname' : m['MOD_DISPLAYNAME'],
                        'version_major' : m['MOD_VERSIONMAJOR'],
                        'version_minor' : m['MOD_VERSIONMINOR'],
                        'revision' : m['MOD_VERSIONREV'],
                        'signature' : m['MOD_SIGNATURE']} for m in result]
            return modules
        else:
            raise Exception('Module does not exist: %s' % module['name'])


    def download_module(self, module):
        result = self.connection.query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_ID, MOD_VERSIONMAJOR, ' +
                'MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_DATA, MOD_SIGNATURE ' +
                'FROM MODULES ' +
                'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? ' +
                'AND MOD_VERSIONREV = ? AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod = result[0]
            # TODO fix reading from blob mod_data
            result_mod = {'name' : mod['MOD_NAME'],
                        'hrname' : mod['MOD_DISPLAYNAME'],
                        'version_major' : mod['MOD_VERSIONMAJOR'],
                        'version_minor' : mod['MOD_VERSIONMINOR'],
                        'revision' : mod['MOD_VERSIONREV'],
                        'signature' : mod['mod_signature']}
            return (result_mod, mod['MOD_DATA'])
        else:
            raise Exception('Module does not exist: %s' % module['name'])


    def get_latest_version(self, module):
        result = self.connection.query('SELECT MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_NAME, ' +
                'MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV ' +
                'FROM MODULES JOIN (SELECT MOD_NAME VERNAME, ' +
                'MAX(MOD_VERSIONMAJOR*10000000+MOD_VERSIONMINOR*100000+MOD_VERSIONREV) VER ' + 
                'FROM MODULES' + 
                'GROUP BY MOD_NAME) ' +  
                'ON VERNAME = MOD_NAME ' + 
                'AND VER = MOD_VERSIONMAJOR*10000000+MOD_VERSIONMINOR*100000+MOD_VERSIONREV ' +
                'WHERE MOD_NAME = ?;', module['name']);
        result = result.fetchallmap()
        if result:
            mod = result[0]
            result_mod = {'name' : mod['MOD_NAME'],
                        'hrname' : mod['MOD_DISPLAYNAME'],
                        'version_major' : mod['MOD_VERSIONMAJOR'],
                        'version_minor' : mod['MOD_VERSIONMINOR'],
                        'revision' : mod['MOD_VERSIONREV'],
                        'signature' : mod['MOD_SIGNATURE']}
            return result_mod
        else:
            raise Exception('Module does not exist: %s' % module['name'])


    def login(self, password, response_header):
        result = self.connection.query("SELECT VAL FROM CONFIG \
                WHERE PARAM = 'password' OR PARAM = 'salt' ORDER BY PARAM ASC;")
        result = result.fetchallmap()

        db_hash = result[0]['VAL']
        salt = base64.b64decode(result[1]['VAL'])
        hashvalue = hashlib.sha512(password.encode('utf-8')  + salt).hexdigest()
        is_valid = hashvalue == db_hash
        
        session = Session.create_session(self, response_header)
        session.set_admin(is_valid)
        session.store()
        return is_valid


    def logout(self):
        try:
            #TODO use own session class, get rid of beaker
            self.environ['beaker.session'].delete()
        except KeyError, e:
            pass


    def change_password(self, password):
        self.verify_admin()
        
        salt = self.generate_salt()
        hashvalue = hashlib.sha512(password + salt).hexdigest()
        salt = base64.b64encode(salt)
        self.connection.query('UPDATE CONFIG SET VAL = ? WHERE PARAM = \'password\';', hashvalue, commit=True)
        self.connection.query('UPDATE CONFIG SET VAL = ? WHERE PARAM = \'salt\';', salt, commit=True)
    

    def register_developer(self, name, fullname, publickey):
        self.verify_admin()

        dev_id = self.connection.get_seq_next('DEV_GEN')
        self.connection.query('INSERT INTO DEVELOPER (DEV_ID, DEV_NAME, DEV_FULLNAME, DEV_PUBLICKEY) ' +
                'VALUES (?, ?, ?, ?);', (dev_id, name, fullname, publickey), commit=True)


    def unregister_developer(self, dev_id):
        self.verify_admin()

        self.connection.query('UPDATE DEVELOPER SET DEV_PUBLICKEY = \'\' ' +
                'WHERE DEV_ID = ?;', dev_id, commit=True)


    def upload_module(self, data, signature):
        result = self.connection.query('SELECT DEV_ID, DEV_NAME, DEV_PUBLICKEY ' +
                'FROM DEVELOPER;')
        valid = False
        hashobj = SHA256.new(data)
        for dev in result:
            key = RSA.importKey(dev['DEV_PUBLICKEY'])
            verifier = PKCS1_v1_5.new(key)
            valid = verifier.verify(hashobj, signature)
            if valid:
                dev_id = dev['DEV_ID']
                break;
        if not valid:
            raise Exception('Signature verification failed')
        
        print ("DEVID: " + str(dev_id)) #TODO debug output

        datafile = cStringIO.StringIO(data)
        tar = tarfile.open(fileobj = datafile, mode = 'r:gz') 
        try:
            manifestdata = tar.extractfile('manifest.json').read()
        except Exception, e:
            raise Exception('Error while reading manifest')
        manifest = json.loads(manifestdata)

        result = self.connection.query('SELECT MAX(MOD_VERSIONREV) AS MAXREVISION ' +
                'FROM MODULES ' +
                'WHERE MOD_NAME = ?;', manifest['name'])
        result = result.fetchallmap()
        if result:
            revision = result['MAXREVISION'] + 1
        else:
            revision = 0
        mod_id = self.connection.get_seq_next('MOD_GEN')
        md5 = hashlib.md5(data).hexdigest()

        key = RSA.importKey(self.get_private_key())
        hashobj = SHA256.new(data)
        signer = PKCS1_v1_5.new(key)
        repo_signature = base64.b64_encode(signer.sign(hashobj))
        
        # TODO blob working?
        self.connection.query('INSERT INTO MDOULES (MOD_ID, MOD_NAME, MOD_DISPLAYNAME, ' +
                'MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_MD5, MOD_SIGNATURE, ' +
                'MOD_DATA VALUE (?,?,?,?,?,?,?,?,?);',
                (mod_id, manifest['name'], manifest['hrname'], manifest['version_major'],
                manifest['version_minor'], revision, md5, repo_signature, cStringIO.StringIO(data)),commit=True)


    def delete_module(self, identifier, major=None, minor=None, revision=None):
        self.verify_admin()

        if major:
            if minor:
                if revision:
                    self.connection.query('DELETE FROM MODULES ' +
                            'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND ' +
                            'MOD_VERSIONMINOR = ? AND MOD_VERSIONREV = ?;',
                            (identifier, major, minor, revision), commit=True)
                else:
                    self.connection.query('DELETE FROM MODULES ' +
                            'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND ' +
                            'MOD_VERSIONMINOR = ?;',
                            (identifier, major, minor), commit=True)    
            else:
                self.connection.query('DELETE FROM MODULES ' +
                        'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ?;',
                        (identifier, major), commit=True)    
        else:
            self.connection.query('DELETE FROM MODULES ' +
                    'WHERE MOD_NAME = ?;',
                    identifier, commit=True)    


    def get_developers(self):
        self.verify_admin()

        result = self.connection.query('SELECT DEV_ID, DEV_NAME, DEV_FULLNAME ' +
                'FROM DEVELOPER;')
        result = result.fetchallmap()
        developers = [{'devId' : d['DEV_ID'],
                        'name' : d['DEV_NAME'],
                        'fullName' : d['DEV_FULLNAME']} for d in result]
        return developers


    def get_public_key(self):
        result = self.connection.query('SELECT VAL ' +
                'FROM CONFIG ' +
                'WHERE PARAM = \'publickey\'')
        result = result.fetchallmap()
        if result:
            return result[0]['VAL']
        return None


    def get_private_key(self):
        result = self.connection.query('SELECT VAL ' +
                'FROM CONFIG ' +
                'WHERE PARAM = \'privatekey\'')
        result = result.fetchallmap()
        if result:
            return result[0]['VAL']
        return None
