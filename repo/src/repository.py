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
import time

from cStringIO import StringIO

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from database import DatabaseConnection

from session import Session

class Repository(object):
    """
    A repository handles incoming requests.
    """

    def verify_admin(self, environ):
        """
        Verifies if the current session has admin rights. If not an exception will be thrown.
        """
        session = environ['session']
        if not session.is_admin():
            raise Exception('You are no admin')


    def generate_salt(self):
        """
        Generates a random salt for password hashing.
        """
        salt = ""
        length = random.randint(128, 255)
        for i in range(0, length):
            salt += chr(random.randint(0, 255))
        return salt


    def get_all_modules(self, environ):
        """
        Returns a list of all modules.
        """
        result = environ['db'].query('SELECT MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_NAME, \
                MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV \
                FROM MODULES JOIN (SELECT MOD_NAME VERNAME \
                ,MAX(MOD_VERSIONMAJOR*10000000 \
                +MOD_VERSIONMINOR*100000 \
                +MOD_VERSIONREV) VER \
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


    def get_versions_of_module(self, environ, module):
        """
        Returns a list of all versions of the specified module.
        """
        result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, ' +
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


    def resolve_dependencies_downwards(self, environ, module):
        """
        Returns a list of all downward dependencies of a module. Downward dependencies are all
        modules that are necessary for the specified module to work.
        """
        result = environ['db'].query('SELECT MOD_ID FROM MODULES WHERE MOD_NAME = ? ' +
                'AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? AND MOD_VERSIONREV = ? ' +
                'AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod_id = result[0]['MOD_ID']
            result = environ['db'].query('SELECT DISTINCT DEP_MOD_DEPENDSOn ' +
                    'FROM DEPENDENCIES ' +
                    'WHERE DEP_MOD_ID = ?;', mod_id)
            result = result.fetchallmap()
            mod_ids = [mod_id]

            while result:
                for mod in result:
                    mod_ids.append(mod['DEP_MOD_DEPENDSOn'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = environ['db'].query('SELECT DEP_MOD_DEPENDSON ' +
                        'FROM DEPENDENCIES ' +
                        'WHERE DEP_MOD_ID IN ? AND DEP_MOD_DEPENDSON NOT IN ?;', 
                        (mod_ids_str, mod_ids_str));
                result = result.fetchallmap()
            result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, ' +
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


    def resolve_dependencies_upwards(self, environ, module):
        """
        Returns a list of all upward dependencies of a module. Upward dependencies are all
        modules that needs the specified module to work.
        """
        result = environ['db'].query('SELECT MOD_ID ' +
                'FROM MODULES ' +
                'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? ' +
                'AND MOD_VERSIONREV = ? AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod_id = result[0]['MOD_ID']
            result = environ['db'].query('SELECT DISTINCT DEP_MOD_ID ' +
                    'FROM DEPENDENCIES ' +
                    'WHERE DEP_MOD_DEPENDSON = ?;', mod_id);
            result = result.fetchallmap()
            mod_ids = [mod_id]
            while result:
                for mod in result:
                    mod_ids.append(mod['DEP_MOD_ID'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = environ['db'].query('SELECT DEP_MOD_ID ' +
                        'FROM DEPENDENCIES ' +
                        'WHERE DEP_MOD_DEPENDSON IN ? AND DEP_MOD_ID NOT IN ?;',
                        (mod_ids_str, mod_ids_str))
                result = result.fetchallmap()

            result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, ' +
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


    def download_module(self, environ, module):
        """
        Returns the specified module with its binary data.
        """
        result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_ID, MOD_VERSIONMAJOR, ' +
                'MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_DATA, MOD_SIGNATURE ' +
                'FROM MODULES ' +
                'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? ' +
                'AND MOD_VERSIONREV = ? AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod = result[0]
            result_mod = {'name' : mod['MOD_NAME'],
                        'hrname' : mod['MOD_DISPLAYNAME'],
                        'version_major' : mod['MOD_VERSIONMAJOR'],
                        'version_minor' : mod['MOD_VERSIONMINOR'],
                        'revision' : mod['MOD_VERSIONREV'],
                        'signature' : mod['mod_signature']}
            return (result_mod, mod['MOD_DATA'])
        else:
            raise Exception('Module does not exist: %s' % module['name'])


    def get_latest_version(self, environ, module):
        """
        Returns the latest version of the specified module.
        """
        result = environ['db'].query('SELECT MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_NAME, ' +
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


    def login(self, environ, password):
        """
        Login with a password to grant admin rights. This session will be stored.
        """
        result = environ['db'].query("SELECT VAL FROM CONFIG \
                WHERE PARAM = 'password' OR PARAM = 'salt' ORDER BY PARAM ASC;")
        result = result.fetchallmap()

        db_hash = result[0]['VAL']
        salt = base64.b64decode(result[1]['VAL'])
        hashvalue = hashlib.sha512(password.encode('utf-8')  + salt).hexdigest()
        is_valid = hashvalue == db_hash
        
        if is_valid:
            session = environ['session']
            session.set_admin(is_valid)
            session.store(environ)
        return is_valid


    def logout(self, environ):
        """
        Deletes the current session.
        """
        environ['session'].delete(environ)


    def change_password(self, environ, password):
        """
        Changes the repositories admin password.
        Needs admin rights.
        """
        self.verify_admin(environ)
        
        salt = self.generate_salt()
        hashvalue = hashlib.sha512(password.encode('utf-8') + salt).hexdigest()
        salt = base64.b64encode(salt)
        environ['db'].query('UPDATE CONFIG SET VAL = ? WHERE PARAM = \'password\';', hashvalue, commit=True)
        environ['db'].query('UPDATE CONFIG SET VAL = ? WHERE PARAM = \'salt\';', salt, commit=True)
    

    def register_developer(self, environ, name, fullname, publickey):
        """
        Registers a new developer at this repository.
        Needs admin rights.
        """
        self.verify_admin(environ)

        dev_id = environ['db'].get_seq_next('DEV_GEN')
        environ['db'].query('INSERT INTO DEVELOPER (DEV_ID, DEV_NAME, DEV_FULLNAME, DEV_PUBLICKEY) ' +
                'VALUES (?, ?, ?, ?);', (dev_id, name, fullname, publickey), commit=True)


    def unregister_developer(self, environ, dev_id):
        """
        Removes a developer of this repository. Only the public key is removed, so that this
        developer can no longer upload modules. This is necessary to keep the developer information
        for modules that have been uploaded before.
        Needs admin rights.
        """
        self.verify_admin(environ)

        environ['db'].query('UPDATE DEVELOPER SET DEV_PUBLICKEY = \'\' ' +
                'WHERE DEV_ID = ?;', dev_id, commit=True)


    def upload_module(self, environ, data, signature):
        """
        Uploads a modules. data is the tared and gzipped module. It must contain a manifest.json file
        in order to provide module meta information.
        """
        cur = environ['db'].query('SELECT DEV_ID, DEV_NAME, DEV_PUBLICKEY ' +
                'FROM DEVELOPER;')
        result = cur.fetchallmap()
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
        
        datafile = StringIO(data)
        tar = tarfile.open(fileobj = datafile, mode = 'r:gz') 
        try:
            manifestdata = tar.extractfile('manifest.json').read()
        except Exception, e:
            raise Exception('Error while reading manifest')
        manifest = json.loads(manifestdata)

        cur = environ['db'].query('SELECT MAX(MOD_VERSIONREV) AS MAXREVISION ' +
                'FROM MODULES ' +
                'WHERE MOD_NAME = ?;', manifest['name'])
        result = cur.fetchonemap()
        maxrevision = result['MAXREVISION']
        if maxrevision is not None:
            revision = maxrevision + 1
        else:
            revision = 0
        manifest['revision'] = revision

        datafile = StringIO()
        newtar = tarfile.open(fileobj = datafile, mode = 'w:gz')
        for member in tar:
            if member.isfile():
                if member.name != 'manifest.json':
                    f = tar.extractfile(member)
                    newtar.addfile(member, f)
                else:
                    manifestdata = json.dumps(manifest)
                    info = tarfile.TarInfo(name = 'manifest.json')
                    info.size = len(manifestdata)
                    info.mtime = time.time()
                    newtar.addfile(tarinfo = info, fileobj = StringIO(manifestdata))
        newtar.close()
        tar.close()
        newdata = datafile.getvalue()

        mod_id = environ['db'].get_seq_next('MOD_GEN')

        key = RSA.importKey(self.get_private_key(environ))
        hashobj = SHA256.new(newdata)
        signer = PKCS1_v1_5.new(key)
        repo_signature = base64.b64encode(signer.sign(hashobj))
        
        environ['db'].query('INSERT INTO MODULES (MOD_ID, MOD_NAME, MOD_DISPLAYNAME, ' +
                'MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_SIGNATURE, ' +
                'MOD_DATA) VALUES (?,?,?,?,?,?,?,?);',
                (mod_id, manifest['name'], manifest['hrname'], manifest['version_major'],
                manifest['version_minor'], revision, repo_signature, base64.b64encode(newdata)), commit=True)


    def delete_module(self, environ, identifier, major=None, minor=None, revision=None):
        """
        Deletes the specified module(s) from this repository.
        Needs admin rights.
        """
        self.verify_admin(environ)

        if major:
            if minor:
                if revision:
                    environ['db'].query('DELETE FROM MODULES ' +
                            'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND ' +
                            'MOD_VERSIONMINOR = ? AND MOD_VERSIONREV = ?;',
                            (identifier, major, minor, revision), commit=True)
                else:
                    environ['db'].query('DELETE FROM MODULES ' +
                            'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND ' +
                            'MOD_VERSIONMINOR = ?;',
                            (identifier, major, minor), commit=True)    
            else:
                environ['db'].query('DELETE FROM MODULES ' +
                        'WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ?;',
                        (identifier, major), commit=True)    
        else:
            environ['db'].query('DELETE FROM MODULES ' +
                    'WHERE MOD_NAME = ?;',
                    identifier, commit=True)    


    def get_developers(self, environ):
        """
        Returns a list of all registered developers.
        Needs admin rights.
        """
        self.verify_admin(environ)

        result = environ['db'].query('SELECT DEV_ID, DEV_NAME, DEV_FULLNAME ' +
                'FROM DEVELOPER;')
        result = result.fetchallmap()
        developers = [{'devId' : d['DEV_ID'],
                        'name' : d['DEV_NAME'],
                        'fullName' : d['DEV_FULLNAME']} for d in result]
        return developers


    def get_public_key(self, environ):
        result = environ['db'].query('SELECT VAL ' +
                'FROM CONFIG ' +
                'WHERE PARAM = \'publickey\'')
        result = result.fetchonemap()
        if result:
            return result['VAL']
        return None


    def get_private_key(self, environ):
        result = environ['db'].query('SELECT VAL ' +
                'FROM CONFIG ' +
                'WHERE PARAM = \'privatekey\'')
        result = result.fetchonemap()
        if result:
            return result['VAL']
        return None
