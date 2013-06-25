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

import base64
import cStringIO
import hashlib
import json
import os
import random
import tarfile
import time

from cStringIO import StringIO

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from database import DatabaseConnection

from session import Session

from common.enums import JSMandatory

class RepositoryErrorCode:
    """
    An enumeration of all response error codes of the repository.
    """
    OK = 0
    UNKNOWN_ERROR = 1
    DATABASE_ERROR = 2
    AUTH_FAILED = 3
    INVALID_JSON = 4
    MODULE_NOT_FOUND = 5
    UPLOAD_INVALID_SIGNATURE = 6
    UPLOAD_MANIFEST = 7
    UPLOAD_DEV_PREFIX = 8
    UPLOAD_DEPENDENCIES = 9
    UPLOAD_CORRUPTED = 10
    DEVELOPER_NO_VALID_KEY = 11
    DEVELOPER_ALREADY_EXISTS = 12
    TEMPLATE_NOT_FOUND = 13
    UPLOAD_JS_MANDATORY = 14

class RepositoryException(Exception):
    """
    An exception that stores an error json object. The global repository exception
    handler will catch this exception and send the exception's error json as response.
    """

    def __init__(self, error_json):
        """
        Initializes a RepositoryException with an error json object.
        """
        self._error_json = error_json

    def get_error_json(self):
        """
        Returns the error json object.
        """
        return self._error_json


def create_repository_exception(code, *args):
    """
    Creates a new RepositoryException with the given error code and
    error arguments.
    """
    return RepositoryException({"c":code,"args":args})


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
            raise create_repository_exception(RepositoryErrorCode.AUTH_FAILED)


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
                MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_JSMANDATORY \
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
                    'js_mandatory': m['MOD_JSMANDATORY'],
                    'signature' : m['MOD_SIGNATURE']} for m in result]
        return modules


    def get_versions_of_module(self, environ, module):
        """
        Returns a list of all versions of the specified module.
        """
        result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, \
                MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_JSMANDATORY \
                FROM MODULES \
                WHERE MOD_NAME = ?;', module['name'])
        result = result.fetchallmap()
        modules = [{'name' : m['MOD_NAME'],
                    'hrname' : m['MOD_DISPLAYNAME'],
                    'version_major' : m['MOD_VERSIONMAJOR'],
                    'version_minor' : m['MOD_VERSIONMINOR'],
                    'revision' : m['MOD_VERSIONREV'],
                    'js_mandatory' : m['MOD_JSMANDATORY'],
                    'signature' : m['MOD_SIGNATURE']} for m in result]
        return modules


    def resolve_dependencies_downwards(self, environ, module):
        """
        Returns a list of all downward dependencies of a module. Downward dependencies are all
        modules that are necessary for the specified module to work.
        """
        result = environ['db'].query('SELECT MOD_ID FROM MODULES WHERE MOD_NAME = ? \
                AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? AND MOD_VERSIONREV = ? \
                AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod_id = result[0]['MOD_ID']
            result = environ['db'].query('SELECT DISTINCT DEP_MOD_DEPENDSON \
                    FROM DEPENDENCIES \
                    WHERE DEP_MOD_ID = ?;', mod_id)
            result = result.fetchallmap()
            mod_ids = [mod_id]

            while result:
                for mod in result:
                    mod_ids.append(mod['DEP_MOD_DEPENDSON'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = environ['db'].query('SELECT DEP_MOD_DEPENDSON \
                        FROM DEPENDENCIES \
                        WHERE DEP_MOD_ID IN ? AND DEP_MOD_DEPENDSON NOT IN ?;', 
                        (mod_ids_str, mod_ids_str));
                result = result.fetchallmap()
            result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, \
                    MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV \
                    FROM MODULES WHERE MOD_ID IN (?) AND MOD_ID != ?;', 
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
            raise create_repository_exception(RepositoryErrorCode.MODULE_NOT_FOUND, module)


    def resolve_dependencies_upwards(self, environ, module):
        """
        Returns a list of all upward dependencies of a module. Upward dependencies are all
        modules that needs the specified module to work.
        """
        result = environ['db'].query('SELECT MOD_ID \
                FROM MODULES \
                WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? \
                AND MOD_VERSIONREV = ? AND MOD_SIGNATURE = ?;',
                (module['name'], module['version_major'], module['version_minor'],
                module['revision'], module['signature']))
        result = result.fetchallmap()
        if result:
            mod_id = result[0]['MOD_ID']
            result = environ['db'].query('SELECT DISTINCT DEP_MOD_ID \
                    FROM DEPENDENCIES \
                    WHERE DEP_MOD_DEPENDSON = ?;', mod_id);
            result = result.fetchallmap()
            mod_ids = [mod_id]
            while result:
                for mod in result:
                    mod_ids.append(mod['DEP_MOD_ID'])
                mod_ids_str = ','.join(map(str, mod_ids))
                result = environ['db'].query('SELECT DEP_MOD_ID \
                        FROM DEPENDENCIES \
                        WHERE DEP_MOD_DEPENDSON IN ? AND DEP_MOD_ID NOT IN ?;',
                        (mod_ids_str, mod_ids_str))
                result = result.fetchallmap()

            result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_ID, \
                    MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV \
                    FROM MODULES \
                    WHERE MOD_ID IN (?) AND MOD_ID != ?;',
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
            raise create_repository_exception(RepositoryErrorCode.MODULE_NOT_FOUND, module)


    def download_module(self, environ, module):
        """
        Returns the specified module with its binary data.
        """
        result = environ['db'].query('SELECT MOD_NAME, MOD_DISPLAYNAME, MOD_ID, MOD_VERSIONMAJOR, \
                MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_DATA, MOD_JSMANDATORY, MOD_SIGNATURE \
                FROM MODULES \
                WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? \
                AND MOD_VERSIONREV = ? AND MOD_SIGNATURE = ?;',
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
                        'js_mandatory': mod['MOD_JSMANDATORY'],
                        'signature' : mod['MOD_SIGNATURE']}
            return (result_mod, mod['MOD_DATA'])
        else:
            raise create_repository_exception(RepositoryErrorCode.MODULE_NOT_FOUND, module)


    def get_latest_version(self, environ, module):
        """
        Returns the latest version of the specified module.
        """
        result = environ['db'].query('SELECT MOD_DISPLAYNAME, MOD_SIGNATURE, MOD_NAME, \
                MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_JSMANDATORY \
                FROM MODULES JOIN (SELECT MOD_NAME VERNAME, \
                MAX(MOD_VERSIONMAJOR*10000000+MOD_VERSIONMINOR*100000+MOD_VERSIONREV) VER \
                FROM MODULES \
                GROUP BY MOD_NAME) \
                ON VERNAME = MOD_NAME \
                AND VER = MOD_VERSIONMAJOR*10000000+MOD_VERSIONMINOR*100000+MOD_VERSIONREV \
                WHERE MOD_NAME = ?;', module['name']);
        result = result.fetchallmap()
        if result:
            mod = result[0]
            result_mod = {'name' : mod['MOD_NAME'],
                        'hrname' : mod['MOD_DISPLAYNAME'],
                        'version_major' : mod['MOD_VERSIONMAJOR'],
                        'version_minor' : mod['MOD_VERSIONMINOR'],
                        'revision' : mod['MOD_VERSIONREV'],
                        'js_mandatory': mod['MOD_JSMANDATORY'],
                        'signature' : mod['MOD_SIGNATURE']}
            return result_mod
        else:
            raise create_repository_exception(RepositoryErrorCode.MODULE_NOT_FOUND, module)


    def get_all_templates(self, environ):
        cur = environ['db'].query('SELECT TMP_ID, TMP_NAME, TMP_DESCRIPTION, TMP_AUTHOR, \
                TMP_SIGNATURE FROM TEMPLATES;')
        result = cur.fetchallmap()
        templates = [{'id' : t['TMP_ID'],
                    'name' : t['TMP_NAME'],
                    'description' : t['TMP_DESCRIPTION'],
                    'author' : t['TMP_AUTHOR'],
                    'signature' : t['TMP_SIGNATURE']} for t in result]
        return templates


    def download_template(self, environ, ident):
        cur = environ['db'].query('SELECT TMP_DATA, TMP_SIGNATURE \
                FROM TEMPLATES \
                WHERE TMP_ID = ?;', ident)
        result = cur.fetchallmap()
        if result:
            result = result[0]
            return (result['TMP_DATA'], result['TMP_SIGNATURE'])
        else:
            raise create_repository_exception(RepositoryErrorCode.TEMPLATE_NOT_FOUND,
                    {'id' : ident})


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
        else:
            raise create_repository_exception(RepositoryErrorCode.AUTH_FAILED)


    def logout(self, environ):
        """
        Deletes the current session.
        """
        environ['session'].delete(environ)


    def change_password(self, environ, password):
        """
        Changes the repositories admin password.
        Needs administrator privileges.
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
        Needs administrator privileges.
        """
        self.verify_admin(environ)
        
        try:
            key = RSA.importKey(publickey)
        except (ValueError, IndexError, TypeError), e:
            raise create_repository_exception(RepositoryErrorCode.DEVELOPER_NO_VALID_KEY)

        # hack to check whether developer exists, TODO let it do the database
        cur = environ['db'].query('SELECT COUNT(*) AS DEVCOUNT FROM DEVELOPER WHERE DEV_NAME = ?;', name)
        result = cur.fetchonemap()
        if result['DEVCOUNT'] != 0:
            raise create_repository_exception(RepositoryErrorCode.DEVELOPER_ALREADY_EXISTS)

        dev_id = environ['db'].get_seq_next('DEV_GEN')
        environ['db'].query('INSERT INTO DEVELOPER (DEV_ID, DEV_NAME, DEV_FULLNAME, DEV_PUBLICKEY) \
                VALUES (?, ?, ?, ?);', (dev_id, name, fullname, publickey), commit=True)


    def unregister_developer(self, environ, dev_id):
        """
        Removes a developer of this repository. Only the public key is removed, so that this
        developer can no longer upload modules. This is necessary to keep the developer information
        for modules that have been uploaded before.
        Needs administrator privileges.
        """
        self.verify_admin(environ)

        environ['db'].query('UPDATE DEVELOPER SET DEV_PUBLICKEY = \'\' \
                WHERE DEV_ID = ?;', dev_id, commit=True)


    def _check_manifest(self, manifest, keys):
        """
        Checks whether a manifest.json is valid. If not, an exception will be thrown.
        """
        has_keys = all([manifest.has_key(key) for key in keys])
        if not has_keys:
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_MANIFEST)


    def _match_developer_signature(self, environ, data, signature):
        cur = environ['db'].query('SELECT DEV_NAME, DEV_PUBLICKEY \
                FROM DEVELOPER WHERE DEV_PUBLICKEY IS NOT NULL;')
        result = cur.fetchallmap()
        valid = False
        hashobj = SHA256.new(data)
        for dev in result:
            key = RSA.importKey(dev['DEV_PUBLICKEY'])
            verifier = PKCS1_v1_5.new(key)
            valid = verifier.verify(hashobj, signature)
            if valid:
                dev_name = dev['DEV_NAME']
                break;
        if not valid:
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_INVALID_SIGNATURE)
        return dev_name


    def upload_module(self, environ, data, signature):
        """
        Uploads a modules. data is the module's archive. It must contain a manifest.json file
        in order to provide module meta information.
        """
        # check if the signature matches a registered developer
        dev_name = self._match_developer_signature(environ, data, signature)
        
        # extract the module's manifest from the module's archive
        datafile = StringIO(data)
        try:
            tar = tarfile.open(fileobj = datafile, mode = 'r:gz') 
            manifestdata = tar.extractfile('manifest.json').read()
        except Exception, e:
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_CORRUPTED)
        
        # checks whether the manifest is a valid json a contains all necessary keys
        try:
            manifest = json.loads(manifestdata)
            self._check_manifest(manifest, ['name', 'hrname', 'version_major', 'version_minor'])
        except Exception, e:
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_MANIFEST)

        # checks whether the modules developer prefix matches the developer name
        if not manifest['name'].startswith(dev_name + '_'):
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_DEV_PREFIX)

        # Checks if module supports js and indicates it. if not, assume, the module is a pure html module
        js_mandatory = 0
        if manifest.has_key('js_mandatory') and manifest['js_mandatory'] in (JSMandatory.NO,JSMandatory.SUPPORTED,JSMandatory.MANDATORY):
            js_mandatory = manifest['js_mandatory']
        else:
            manifest['js_mandatory'] = 0

        # checks whether all dependencies are available
        dependencies = []
        if 'dependencies' in manifest:
            dependencies = manifest['dependencies']
            missing = []
            for dep in dependencies:
                cur = environ['db'].query('SELECT COUNT(*) AS DEPCOUNT \
                        FROM MODULES \
                        WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? \
                        AND MOD_VERSIONMINOR = ?;',
                        (dep['name'], dep['version_major'], dep['version_minor']))
                result = cur.fetchonemap()
                if result['DEPCOUNT'] == 0:
                    missing.append({'name' : dep['name'],
                            'version_major' : dep['version_major'],
                            'version_minor' : dep['version_minor']})
            if missing:
                raise create_repository_exception(RepositoryErrorCode.UPLOAD_DEPENDENCIES, *missing)
        
        # calculate the new revision of the module and write it to the manifest
        cur = environ['db'].query('SELECT MAX(MOD_VERSIONREV) AS MAXREVISION \
                FROM MODULES \
                WHERE MOD_NAME = ?;', manifest['name'])
        result = cur.fetchonemap()
        maxrevision = result['MAXREVISION']
        if maxrevision is not None:
            revision = maxrevision + 1
        else:
            revision = 0
        manifest['revision'] = revision

        # creates the new module archive with the new revision
        datafile = StringIO()
        try:
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
        except Exception, e:
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_CORRUPTED) # TODO check different error cases

        # generates a new module id and sign the module with the repositories
        # private key
        mod_id = environ['db'].get_seq_next('MOD_GEN')

        key = RSA.importKey(self.get_private_key(environ))
        hashobj = SHA256.new(newdata)
        signer = PKCS1_v1_5.new(key)
        repo_signature = base64.b64encode(signer.sign(hashobj))
        
        # stores the new module in the database
        environ['db'].query('INSERT INTO MODULES (MOD_ID, MOD_NAME, MOD_DISPLAYNAME, \
                MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_SIGNATURE, \
                MOD_JSMANDATORY, MOD_DATA) VALUES (?,?,?,?,?,?,?,?,?);',
                (mod_id, manifest['name'], manifest['hrname'], manifest['version_major'],
                manifest['version_minor'], revision, repo_signature, js_mandatory, base64.b64encode(newdata)), commit=True)

        # stores the dependencies of this module in the database
        for dep in dependencies:
            dep_id = environ['db'].get_seq_next('DEP_GEN')
            
            cur =  environ['db'].query('SELECT MOD_ID \
                    FROM MODULES M \
                    JOIN (SELECT MOD_NAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MAX(MOD_VERSIONREV) AS MAXREV \
                        FROM MODULES \
                        GROUP BY MOD_NAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR) REV \
                    ON M.MOD_NAME = REV.MOD_NAME AND M.MOD_VERSIONMAJOR = REV.MOD_VERSIONMAJOR AND \
                        M.MOD_VERSIONMINOR = REV.MOD_VERSIONMINOR AND M.MOD_VERSIONREV = REV.MAXREV \
                    WHERE M.MOD_NAME = ? AND M.MOD_VERSIONMAJOR = ? AND M.MOD_VERSIONMINOR = ?;',
                    (dep['name'], dep['version_major'], dep['version_minor']))
            result = cur.fetchonemap()
            dependson_id = result['MOD_ID']

            environ['db'].query('INSERT INTO DEPENDENCIES (DEP_ID, DEP_MOD_ID, DEP_MOD_DEPENDSON) \
                    VALUES (?,?,?);', (dep_id, mod_id, dependson_id), commit=True) 


    def delete_module(self, environ, identifier, major=None, minor=None, revision=None):
        """
        Deletes the specified module(s) from this repository.
        Needs administrator privileges.
        """
        self.verify_admin(environ)

        if major:
            if minor:
                if revision:
                    environ['db'].query('DELETE FROM MODULES \
                            WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND \
                            MOD_VERSIONMINOR = ? AND MOD_VERSIONREV = ?;',
                            (identifier, major, minor, revision), commit=True)
                else:
                    environ['db'].query('DELETE FROM MODULES \
                            WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND \
                            MOD_VERSIONMINOR = ?;',
                            (identifier, major, minor), commit=True)    
            else:
                environ['db'].query('DELETE FROM MODULES \
                        WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ?;',
                        (identifier, major), commit=True)    
        else:
            environ['db'].query('DELETE FROM MODULES \
                    WHERE MOD_NAME = ?;',
                    identifier, commit=True)    


    def get_developers(self, environ):
        """
        Returns a list of all registered developers.
        Needs administrator privileges.
        """
        self.verify_admin(environ)

        result = environ['db'].query('SELECT DEV_ID, DEV_NAME, DEV_FULLNAME \
                FROM DEVELOPER;')
        result = result.fetchallmap()
        developers = [{'devId' : d['DEV_ID'],
                        'name' : d['DEV_NAME'],
                        'fullName' : d['DEV_FULLNAME']} for d in result]
        return developers


    def upload_template(self, environ, data, signature):
        """
        Uploads a templates. data is the templates's archive. It must contain a manifest.json file
        in order to provide template meta information.
        """

        # check if the signature matches a registered developer
        dev_name = self._match_developer_signature(environ, data, signature)

        # extract the template's manifest from the template's archive
        datafile = StringIO(data)
        try:
            tar = tarfile.open(fileobj = datafile, mode = 'r:gz') 
            manifestdata = tar.extractfile('manifest.json').read()
        except Exception, e:
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_CORRUPTED)

        # checks whether the manifest is a valid json a contains all necessary keys
        try:
            manifest = json.loads(manifestdata)
            self._check_manifest(manifest, ['name', 'description', 'author'])
        except Exception, e:
            raise create_repository_exception(RepositoryErrorCode.UPLOAD_MANIFEST)

        # generates a new template id and sign the template with the repositories
        # private key
        tmp_id = environ['db'].get_seq_next('TMP_GEN')

        key = RSA.importKey(self.get_private_key(environ))
        hashobj = SHA256.new(data)
        signer = PKCS1_v1_5.new(key)
        repo_signature = base64.b64encode(signer.sign(hashobj))

        # stores the new template in the database
        environ['db'].query('INSERT INTO TEMPLATES (TMP_ID, TMP_NAME, TMP_DESCRIPTION, \
                TMP_AUTHOR, TMP_SIGNATURE, TMP_DATA) VALUES (?,?,?,?,?,?);',
                (tmp_id, manifest['name'], manifest['description'], manifest['author'],
                repo_signature, base64.b64encode(data)), commit=True)


    def delete_template(self, environ, ident):
        """
        Removes a template from this repository
        """
        environ['db'].query('DELETE FROM TEMPLATES \
                WHERE TMP_ID = ?;', ident, commit=True)


    def get_public_key(self, environ):
        """
        Returns the public key of this repository.
        """
        result = environ['db'].query('SELECT VAL \
                FROM CONFIG \
                WHERE PARAM = \'publickey\'')
        result = result.fetchonemap()
        if result:
            return result['VAL']
        else:
            raise create_repository_exception(RepositoryErrorCode.UNKNOWN_ERROR,
                    {'traceback':'No public key'})


    def get_private_key(self, environ):
        """
        Returns the public key of this repository.
        """
        result = environ['db'].query('SELECT VAL \
                FROM CONFIG \
                WHERE PARAM = \'privatekey\'')
        result = result.fetchonemap()
        if result:
            return result['VAL']
        else:
            raise create_repository_exception(RepositoryErrorCode.UNKNOWN_ERROR,
                    {'traceback':'No private key'})
