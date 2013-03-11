#!/usr/bin/python
#-*- coding: utf-8 -*-

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

from json import JSONDecoder, JSONEncoder
from urllib2 import urlopen, quote
import base64
import Crypto.PublicKey.RSA as RSA
import os
import tarfile
import shutil

from operation import ModuleInstallOperation, ModuleUninstallOperation, ModuleUpdateOperation, ModuleOperation

class ModuleCoreException(Exception):
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used""",
        1:"""This Widgets needs a module, to be saved into database""",
        2:"""Module could not be downloaded""",
        3:"""Module signature is not valid! Packet may be compromised""",
        4:"""Can't delete Repo with null-id! """,
        5:"""Module already exists!""",
        6:"""This module does not exist""",
        7:"""This widget does not exist"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "MOD_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class AbstractModule(object):
    def __init__(self,core):
        self._core=core

        self._id = None
        self._name = None
        self._hrname = None
        self._version_major = None
        self._version_minor = None
        self._revision = None
        self._permissions = [] 
        self._tables = []

    def set_id(self, nr):
        self._id = nr

    def get_id(self):
        return self._id

    def _load_manifest(self):
        """
        loads metadata into the module from the modules manifest.json-file
        """
        manifest_file = open(self._path+"manifest.json")
        manifest_data = manifest_file.read()
        manifest_file.close()
        manifest = JSONDecoder().decode(manifest_data)
        self._name = manifest["name"]
        self._hrname = manifest["hrname"]
        self._version_major = manifest["version_major"]
        self._version_minor = manifest["version_minor"]
        self._revision = manifest["revision"]
        self._permissions = manifest["permissions"]
        self._tables = manifest["tables"]

    def get_tables(self):
        """
        returns this module's table-definitions
        """ 
        return self._tables

    def get_permissions(self):
        """
        returns this module's permission-definitions
        """
        return self._permissions

    def get_name(self):
        """
        returns the core-handle-name for this module
        """
        return self._name

    def get_hrname(self):
        """
        returns the human readable name for this module
        """
        return self._hrname

    def get_version(self,part=None):
        """
        returns the modules version or a part of its components
        """
        if part == "major":
            return self._version_major
        elif part == "minor":
            return self._version_minor
        elif part == "revision":
            return self._revision
        else:
            return (self._version_major,self._version_minor,self._revision)

    def create_widget(self, name=""):
        """
        cretes a widget of this module and returns it
        """
        w = Widget(self._core, self)
        w.set_name(name)
        w.store()

    def get_widget(self,widget_id):
        """
        returns an instance of thre requested module with a set instanceId
        """
        db = self._core.get_db()
        stmnt = "SELECT WGT_ID, WGT_NAME FROM WIDGETS WHERE WGT_MOD_ID = ? AND WGT_ID = ? ;"
        cur = db.query(self._core, stmnt, (self._id,widget_id))

        row = cur.fetchonemap()
        if row is not None:
            widget = Widget(self._core, self, row["WGT_ID"])
            widget.set_name(row["WGT_NAME"])
            return widget
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(7))

    def get_widgets(self):
        """
        returns an instance of thre requested module with a set instanceId
        """
        db = self._core.get_db()
        stmnt = "SELECT WGT_ID, WGT_NAME FROM WIDGETS WHERE WGT_MOD_ID = ? ;"
        cur = db.query(self._core, stmnt, (self._id,))

        widgets = []
        for row in cur.fetchallmap():
            widget = Widget(self._core, self, row["WGT_ID"])
            widget.set_name(row["WGT_NAME"])
            widgets.append(widget)        
        return widgets

class Widget(object):
    def __init__(self, core, module, nr=None):
        self._core= core
        self._id = nr
        self._module= module
        self._name = None
        self._space = None
        self._site_id = None

    def set_id(self,nr):
        self._id = int(nr)

    def set_name(self,name):
        self._name=str(name)

    def set_site(self,site):
        if type(site)==int:
            self._site_id = site
        elif site.__class__.__name__ == "Site":
            self._site_id = site.get_id()

    def set_space(self,space):
        self._space = int(space)

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_space(self):
        return self._space

    def get_site_id(self):
        return self._site_id

    def render_pure_html(self,args={}):
        self._module.render_pure_html(self._id,args)

    def render_html(self,args={}):
        self._module.render_html(self._id,args)

    def render_javascript(self,args={}):
        self._module.render_javascript(self._id,args)

    def store(self):
        db = self._core.get_db()

        if self._id is None:
            self._id = db.get_seq_next('WGT_GEN')

        if self._module is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(1))

        stmnt = "UPDATE OR INSERT INTO WIDGETS (WGT_ID, WGT_NAME, WGT_SIT_ID, WGT_MOD_ID, WGT_SPACE) \
                    VALUES (?,?,?,?,?) MATCHING (WGT_ID) ;"
        db.query(self._core,stmnt,(self._id,self._name, self._site_id,self._module.get_id(), self._space ),commit=True)

    def delete(self):
        db = self._core.get_db()

        if self._id is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(2))

        stmnt = "DELETE FROM WIDGETS WHERE WGT_ID = ? ;"
        db.query(self._core,stmnt,(self._id,),commit=True)


class ModuleManager(object):
    def __init__(self,core):
        self._core = core

    def get_module(self,module_id):
        """
        returns an instance of the requested module
        """
        module_id = int(module_id)
        db = self._core.get_db()
        stmnt = "SELECT MOD_NAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV FROM MODULES WHERE MOD_ID = ? ;"
        cur = db.query(self._core,stmnt,(module_id,))
        row = cur.fetchonemap()
        if row is not None:
            exec "from %s.v%d_%d_%d import Module as ModuleImplementation"%(row["MOD_NAME"], row["MOD_VERSIONMAJOR"], row["MOD_VERSIONMINOR"], row["MOD_VERSIONREV"])
            module = ModuleImplementation(self._core) 
            module.set_id(module_id)
            return module
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(6))

    def get_module_by_name(self,name):
        nr = self._get_module_id_from_name(name)
        return self.get_module(nr)
    
    def get_widget(self,widget_id):
        """
        returns an instance of thre requested module with a set instanceId
        """
        module = self._get_module_from_widget_id(widget_id)
        widget = module.get_widget(widget_id)
        return widget

    def _get_module_id_from_name(self,module_name):
        """
        returns the module id of the given module_name
        """
        module_name = str(module_name)
        db = self._core.get_db()
        stmnt = "SELECT MOD_ID FROM MODULES WHERE MOD_NAME = ? ;"
        cur = db.query(self._core,stmnt,(module_name,))
        row = cur.fetchonemap()
        if row is not None:
            return int(row["MOD_ID"])
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(6))

    def _get_module_from_widget_id(self,widget_id):
        """
        returns the module that belongs to a widget with the given id
        """
        db = self._core.get_db()
        stmnt = "SELECT WGT_MOD_ID FROM WIDGETS WHERE WGT_ID = ? ;"
        cur = db.query(self._core,stmnt,(widget_id,))
        row = cur.fetchonemap()
        if row is not None:
            return self.get_module(row["WGT_MOD_ID"])
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(7))            


    def install_module(self,module_meta):
        """
        actually installs the module
        """
        configuration = self._core.get_configuration()
        libpath = configuration.get_entry("global.libpath")

        modulepath = libpath+"/"+module_meta["name"]+"/v"+\
                              str(module_meta["version_major"])+"_"+ \
                              str(module_meta["version_minor"])+"_"+ \
                              str(module_meta["revision"])

        if os.path.exists(libpath+"/"+module_meta["name"]):
            if not os.path.exists(modulepath):
                os.mkdir(modulepath)
        else:
            os.mkdir(libpath+"/"+module_meta["name"])
            open(libpath+"/"+module_meta["name"]+"/__init__.py","w").close()
            os.mkdir(modulepath)
        
        repo = self.get_repository()
        datapath = repo.download_module(module_meta)
        tar = tarfile.open(datapath, "r:gz")

        tar.extractall(modulepath)
        manifest_file = open(modulepath+"/manifest.json","r")
        manifest = JSONDecoder().decode(manifest_file.read())
        manifest_file.close()

        nr = self._register_module(manifest)
        module = self.get_module(nr)

        permissionmanager = self._core.get_permission_manager()
        db = self._core.get_db()

        permissionmanager.create_permissions_for_module(module)
        db.create_tables_for_module(module)
        
        os.remove(datapath)

    def update_module(self,module):
        """
        updates the given module
        """
        # - neueste versionsnummer holen
        # - pruefen ob bereits auf fs vorhanden
        #   - wenn nein, holen
        # - neues modul laden
        # - tabellen aendern
        # - permissions aendern
        # - datenbank-versionseintraege updaten
        if module.__class__.__name__ != "Module":
            nr = self._get_module_id_from_name(module_meta["name"])
            module = self.get_module(nr)

        configuration = self._core.get_configuration()
        libpath = configuration.get_entry('global.libpath')

        repo = self.get_repository()
        latest_version = repo.get_latest_version(module)

        latest_path = libpath+"/"+latest_version["name"]+"/v"+\
                              latest_version["version_major"]+"_"+ \
                              latest_version["version_minor"]+"_"+ \
                              latest_version["revision"]

        if self.compare_versions(latest_version, module) == 1:
            if not os.path.exists(latest_path):
                datapath = repo.download_module(latest_version)
                os.mkdir(latest_path)
                tar = tarfile.open(datapath, "r:gz")
                tar.extractall(latest_path)
            nr = self._get_module_id_from_name(latest_version["name"])

            db = self._core.get_db()
            stmnt = "UPDATE MODULES SET MOD_VERSIONMAJOR = ?, \
                                        MOD_VERSIONMINOR = ?, \
                                        MOD_VERSIONREV = ? \
                        WHERE MOD_ID = ? ;"
            db.query(self._core,stmnt,(latest_version["version_major"],
                                       latest_version["version_minor"],
                                       latest_version["revision"], 
                                       nr),commit=True)
            updated_module = self.get_module(nr)
            db.update_tables_for_module(updated_module)
            permissionmanager = self._core.get_permission_manager()
            permissionmanager.update_permissions_for_module(updated_module)


    def uninstall_module(self,module, hard=False):
        """
        uninstall a module
        the flag "hard" actually deletes the files of this module in libpath
        module can be module or module meta
        """
        if module.__class__.__name__ != "Module":
            nr = self._get_module_id_from_name(module_meta["name"])
            module = self.get_module(nr)

        db = self._core.get_db()
        permissionmanager = self._core.get_permission_manager()
        db.remove_tables_for_module(module)
        permissionmanager.remove_permissions_for_module(module)

        if hard:
            configuration = self._core.get_configuration()
            libpath = configuration.get_entry('global.libpath')
            version = module.get_version()
            shutil.rmtree(libpath+"/"+module.get_name()+"/v"+version[0]+"_"+version[1]+"_"+version[2])

        self._unregister_module(module)

    def _register_module(self,manifest):
        """
        registers a module into the database
        """
        db = self._core.get_db()
        nr = db.get_seq_next("MOD_GEN")
        stmnt = "INSERT INTO MODULES (MOD_ID, MOD_NAME, MOD_DISPLAYNAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV) \
                      VALUES (?,?,?,?,?,?) ;"
        db.query(self._core,stmnt,(nr,manifest["name"],manifest["hrname"],
                                   manifest["version_major"],manifest["version_minor"],manifest["revision"]),commit=True)
        return nr

    def _unregister_module(self,module):
        db = self._core.get_db()
        stmnt = "DELETE FROM MODULES WHERE MOD_NAME = ? ;" 
        db.query(self._core,stmnt,(module.get_name(),),commit=True)

    def get_meta_from_module(self,module):
        d = {
            "name":module.get_name(),
            "hrname":module.get_hrname(),
            "version_major":module.get_version("major"),
            "version_minor":module.get_version("minor"),
            "revision":module.get_version("revision")
        }
        return d

    def get_repository(self):
        """
        returns this instance's repository
        """
        db = self._core.get_db()
        stmnt = "select rep_id, rep_name, rep_ip, rep_port, rep_lastupdate from repositories where rep_id = 1;"
        cur = db.query(self._core,stmnt)
        row = cur.fetchonemap()
        return Repository(self._core,row["REP_ID"],row["REP_NAME"],row["REP_IP"],row["REP_PORT"],row["REP_LASTUPDATE"])

    def set_repository(self, ip, port, name):
        """
        changes this instance's repository
        """
        repository = Repository(self._core, None, name, ip, port, None)
        repository.store()
        return repository

    def compare_versions(self,module1,module2):
        """
        compares the versions of module1 and module2
        if module 1 is newer, returns 1
        if module 2 is newer, returns -1
        if equal, returns 0
        """
        if type(module1) != dict:
            module1 = module1.get_meta_from_module()
        if type(module2) != dict:
            module2 = module2.get_meta_from_module()
        if module1["version_major"] > module2["version_major"]:
            return 1
        elif module1["version_major"] == module2["version_major"]:
            if module1["version_minor"] > module2["version_minor"]:
                return 1
            elif module1["version_minor"] == module2["version_minor"]:
                if module1["revision"] > module2["revision"]:
                    return 1
                elif module1["revision"] == module2["revision"]:
                    return 0
                else:
                    return -1
            else:
                return -1
        else:
            return -1

    def invoke_install(self, module_meta):
        """
        registers an operation, that installs a module
        """
        operationmanager = self._core.get_operation_manager()
        op = ModuleInstallOperation(self._core)
        op.set_values(module_meta)
        op.store()

    def invoke_update(self, module_meta):
        """
        registers an operation, that updates a module
        """
        operationmanager = self._core.get_operation_manager()
        op = ModuleUpdateOperation(self._core)
        op.set_values(module_meta)
        op.store()

    def invoke_uninstall(self, module_meta):
        """
        registers an operation, that uninstalls a module
        """
        operationmanager = self._core.get_operation_manager()
        op = ModuleUninstallOperation(self._core)
        op.set_values(module_meta)
        op.store()

    def update_modules(self):
        """
        update all modules of this instance
        """
        modules = self.get_modules()
        for module in modules:
            self.invoke_update(self.get_meta_from_module(module))

    def get_modules(self):
        db = self._core.get_db()
        stmnt = "SELECT MOD_ID FROM MODULES ;"
        cur = db.query(self._core,stmnt)
        ids = cur.fetchallmap()
        return [self.get_module(i["MOD_ID"]) for i in ids]

    def get_module_info(self, only_installed=False):
        """
        get metalist of all installed modules with additional information
         - is there a possible update
        """
        meta_records = []
        for module in self.get_modules():
            meta_record = self.get_meta_from_module(module)
            meta_record.update({'installed':True,'serverModuleId':module.get_id()})
            meta_records.append(meta_record)

        operation_manager = self._core.get_operation_manager() # To initialize cls._core of operations

        repository_joblocks = ModuleOperation.get_currently_processed_modules()

        if not only_installed:
            repo = self.get_repository()
            repomodules = repo.get_all_modules()
            for repomodule in repomodules:
                module_on_system = False
                for meta_record in meta_records:
                    if repomodule["name"] == meta_record["name"]:
                        self._core.log("REPO>"+repomodule['name']+" META>"+meta_record["name"])
                        if self.compare_versions(repomodule, meta_record) == 1:
                            meta_record["toUpdate"] == True
                        for repository_joblock in repository_joblocks:
                            if repository_joblock["name"] == meta_record["name"]:
                                meta_record["processing"] = 'Uninstalling'
                        module_on_system = True
                if module_on_system:
                    continue
                for repository_joblock in repository_joblocks:
                    if repository_joblock["name"] == repomodule["name"]:
                        repomodule["processing"] = 'Installing'
                meta_records.append(repomodule)

        return meta_records

class Repository(object):
    def __init__(self, core, nr=None, name=None, ip=None, port=80, lastupdate=None):
        self._core = core

        self._id = nr
        self._name = name
        self._ip = ip
        self._port = port
        self._lastupdate = lastupdate
        self._public_key = None

        self._jsonencoder = None
        self._jsondecoder = None

    def get_ip(self):
        """
        trivial
        """
        return self._ip

    def get_id(self):
        """
        trivial
        """
        return self._id

    def get_name(self):
        """
        trivial
        """
        return self._name

    def get_port(self):
        """
        trivial
        """
        return self._port

    def get_public_key(self):
        """
        trivial
        """
        if self._public_key is None:
            self._public_key = self.load_public_key()
        return self._public_key

    def get_host(self):
        """
        trivial
        """
        if self._port == 80:
            return "http://"+self._ip+"/"
        else:
            return "http://"+self._ip+":"+str(self._port)+"/"

    def _http_call(self,msg):
        if self._jsondecoder is None:
            self._jsondecoder = JSONDecoder()
        if self._jsonencoder is None:
            self._jsonencoder = JSONEncoder()
        url = self.get_host()+"?j="+quote(self._jsonencoder.encode(msg).encode('utf-8'))
        http = urlopen(url)
        return self._jsondecoder.decode(http.read())


    def get_all_modules(self):
        result = self._http_call({'c':1})
        return result["r"]

    def load_public_key(self):
        result = self._http_call({'c':6})
        return result["r"]

    def get_all_versions(self, module):
        if type(module) != dict:
            modulemanager = self._core.get_module_manager()
            module = modulemanager.get_meta_from_module(module)
        result = self._http_call({'c':2,'m':module})
        return result["r"]

    def get_latest_version(self, module):
        if type(module) != dict:
            modulemanager = self._core.get_module_manager()
            module = modulemanager.get_meta_from_module(module)
        result = self._http_call({'c':7,'m':module})
        return result["r"]

    def get_dependencies(self, module):
        if type(module) != dict:
            modulemanager = self._core.get_module_manager()
            module = modulemanager.get_meta_from_module(module)
        result = self._http_call({'c':3,'m':module})
        return result["r"]

    def get_descending_dependencies(self, module):
        if type(module) != dict:
            modulemanager = self._core.get_module_manager()
            module = modulemanager.get_meta_from_module(module)
        result = self._http_call({'c':4,'m':module})
        return result["r"]

    def verify_module(self,data,signature):
        """
        verifies if the data has been signed by this repository
        """
        import Crypto.Hash.SHA256 as SHA256
        import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
        k = RSA.importKey(self.get_public_key())
        verifier = PKCS1_v1_5.new(k)
        h = SHA256.new(data)
        signature = base64.decodestring(signature)
        return verifier.verify(h,signature)

    def download_module(self,module):
        """
        downloads a module and
        returns the data directly!
        """
        if type(module) != dict:
            modulemanager = self._core.get_module_manager()
            module = modulemanager.get_meta_from_module(module)
        result = self._http_call({'c':5,'m':module})
        if result is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(2))
        data = base64.decodestring(result["data"])
        if not self.verify_module(data, result["r"]["signature"]):
            raise ModuleCoreException(ModuleCoreException.get_msg(3))

        datapath = "/tmp/"+result["r"]["name"]+"_v"+ \
                                str(result["r"]["version_major"])+"_"+ \
                                str(result["r"]["version_minor"])+"_"+ \
                                str(result["r"]["revision"])+".tar.gz"
        datafile = open(datapath,"w")
        datafile.write(data)
        datafile.close()
        return datapath

    def store(self):
        """
        currently only one repository can be owned by one scoville instance
        """
        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO REPOSITORIES (REP_ID, REP_NAME, REP_IP, REP_PORT, REP_LASTUPDATE, REP_PUBLICKEY) VALUES (?,?,?,?,?,?) MATCHING (REP_ID) ;"
        db.query(self._core,stmnt,(self._id, self._name, self._ip, self._port, self._lastupdate, self.get_public_key()),commit=True)


    def delete(self):
        """
        deletes this repo from database
        """
        if self._id is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(4))
        db = self._core.get_db()

        stmnt = "DELETE FROM REPOSITORIES WHERE REP_ID = ? ;"
        db.query(self._core,stmnt,(self._id,),commit=True)