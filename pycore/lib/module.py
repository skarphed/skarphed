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

###########################################################
#
#    document process by commenting out overtaken PHP-
#    functions. Too much stuff is going to change here.
#
###########################################################

from json import JSONDecoder, JSONEncoder
from urllib2 import urlopen
import base64
import Crypto.PublicKey.RSA as RSA
import os
import tarfile


class ModuleCoreException(Exception):
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used""",
        1:"""This Widgets needs a module, to be saved into database""",
        2:"""Module could not be downloaded""",
        3:"""Module signature is not valid! Packet may be compromised""",
        4:"""Can't delete Repo with null-id! """,
        5:"""Module already exists!"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "DB_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class AbstractModule(object):
    def __init__(self,core):
        self._core=core

        self._name = None
        self._hrname = None
        self._version_major = None
        self._version_minor = None
        self._revision = None
        self._permissions = [] 
        self._tables = []


    def _load_manifest(self):
        """
        loads metadata into the module from the modules manifest.json-file
        """
        manifest_file = open(self._path+"manifest.json")
        manifest_data = manifest_file.read()
        manifest_file.close()
        manifest = JSONDecoder().decode(manifest_data)
        self._name = manifest["name"]
        self._hrname = manifest["name"]
        self._version_major = manifest["version_major"]
        self._version_minor = manifest["version_minor"]
        self._revision = manifest["revision"]
        self._permissions = manifest["rights"]
        self._tables = manifest["tables"]

    def get_tables(self):
        """
        returns this module's table-definitions
        """
        return self._tables

    def get_permssions(self):
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
        self._space = int(space):

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
        db.query(self._core,stmnt,(self._id,self._name, self._site_id,self._module.get_id(), self._space ))

    def delete(self):
        db = self._core.get_db()

        if self._id is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(2))

        stmnt = "DELETE FROM WIDGETS WHERE WGT_ID = ? ;"
        db.query(self._core,stmnt,(self._id,))


class ModuleManager(object):
    def __init__(self,core):
        self._core = core

    def get_module(self,module_id):
        """
        returns an instance of the requested module
        """
        pass

    def get_widget(self,widget_id):
        """
        returns an instance of thre requested module with a set instanceId
        """
        widget = Widget(self._core, self._get_module_from_widget(widget_id), widget_id)
        return widget

    def _get_module_id_from_name(self,module_name):
        """
        returns the module id of the given module_name
        """
        pass

    def _get_module_from_widget_id(self,widget_id):
        """
        returns the module that belongs to a widget with the given id
        """
        pass

    def install_module(self,module_meta):
        configuration = self._core.get_configuration()
        libpath = configuration.get_entry("global.libpath")

        datafile = open("/tmp/"+module_meta["name"]+"_v"+ \
                                module_meta["version_major"]+"_"+ \
                                module_meta["version_minor"]+"_"+ \
                                module_meta["revision"]+".tar.gz")

        modulepath = libpath+"/"+module_meta["name"]+"/v"+\
                              module_meta["version_major"]+"_"+ \
                              module_meta["version_minor"]+"_"+ \
                              module_meta["revision"]

        if os.path.exists(libpath+"/"+module_meta["name"]):
            if os.path.exists(modulepath)
                raise ModuleCoreException(ModuleCoreException.get_msg(5))
            else:
                os.mkdir(modulepath)
        else:
            os.mkdir(libpath+"/"+module_meta["name"])
            open(libpath+"/"+module_name["meta"]+"/__init__.py","w").close()
            os.mkdir(modulepath)

        tar = tarfile.open("/tmp/"+result["r"]["name"]+"_v"+ \
                                result["r"]["version_major"]+"_"+ \
                                result["r"]["version_minor"]+"_"+ \
                                result["r"]["revision"]+".tar.gz", "r:gz")
        

        #$version = v+$version_major+_+version_minor+_+revision
        #install folder will be LIBPATH/module_name/$version/*


    def update_module(self,module_meta):
        pass

    def uninstall_module(self,module_meta):
        pass

    def get_meta_from_module(self,module):
        d = {
            "name":module.get_name(),
            "hrname":module.get_hrname(),
            "version_major".module.get_version("major"),
            "version_minor".module.get_version("minor"),
            "revision".module.get_version("revision"),
        }
        return d

class Repository(object):
    def __init__(self, core, nr=None, name=None, ip=None, port=80, lastupdate=None):
        self._core = core

        self._id = nr
        self._name = name
        self._ip = ip
        self._port = port
        self._lastupdate = lastupdate
        self._public_key = None

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
        url = self.get_host()+"?j="+self._jsonencoder.encode(msg)
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
        k = RSA.importKey(self.get_public_key())
        h = SHA256.new(data).hexdigest()
        return k.verify(h,signature)

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
        datafile = open("/tmp/"+result["r"]["name"]+"_v"+ \
                                result["r"]["version_major"]+"_"+ \
                                result["r"]["version_minor"]+"_"+ \
                                result["r"]["revision"]+".tar.gz")
        datafile.write(data)
        datafile.close()

    def store(self):
        """
        currently only one repository can be owned by one scoville instance
        """
        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO REPOSITORIES (REP_ID, REP_NAME, REP_IP, REP_PORT, REP_LASTUPDATE, REP_PUBLICKEY) VALUES (?,?,?,?,?,?) MATCHING (REP_ID) ;"
        db.query(self._core,stmnt,(self._id, self._name, self._ip, self._port, self._lastupdate, self.get_public_key()))


    def delete(self):
        """
        deletes this repo from database
        """
        if self._id is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(4))
        db = self._core.get_db()

        stmnt = "DELETE FROM REPOSITORIES WHERE REP_ID = ? ;"
        db.query(self._core,stmnt,(self._id,))