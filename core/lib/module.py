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

from json import JSONDecoder, JSONEncoder
from urllib2 import urlopen, quote, URLError
import base64
import Crypto.PublicKey.RSA as RSA
import os
import tarfile
import shutil
import math

from skarphedcore.operation import ModuleInstallOperation, ModuleUninstallOperation, ModuleUpdateOperation, ModuleOperation
from skarphedcore.configuration import Configuration
from skarphedcore.database import Database, DatabaseException
from skarpehdcore.core import Core
from skarphedcore.permissions import Permission, PermissionException
from skarphedcore.view import View, ViewException
from skarphedcore.action import Action
from skarphedcore.css import CSSManager

from helper import sluggify

from common.enums import ActivityType, JSMandatory
from common.errors import ModuleCoreException, ConfigurationException

class AbstractModule(object):
    def __init__(self):
        self._id = None
        self._name = None
        self._hrname = None
        self._version_major = None
        self._version_minor = None
        self._revision = None
        self._js_mandatory = None
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
        manifest_file = open(self._path+"/manifest.json")
        manifest_data = manifest_file.read()
        manifest_file.close()
        manifest = JSONDecoder().decode(manifest_data)
        self._name = manifest["name"]
        self._hrname = manifest["hrname"]
        self._version_major = manifest["version_major"]
        self._version_minor = manifest["version_minor"]
        self._revision = manifest["revision"]
        self._js_mandatory = manifest["js_mandatory"]
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

    def set_js_mandatory(self, js_mandatory):
        if js_mandatory not in (JSMandatory.NO, JSMandatory.SUPPORTED, JSMandatory.MANDATORY):
            return False
        else:
            self._js_mandatory = js_mandatory

    def get_js_mandatory(self):
        return self._js_mandatory

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
        if name=="":
            raise ModuleCoreException(ModuleCoreException.get_msg(10))
        w = Widget(self)
        w.set_name(name)
        w.store()

    def get_widget(self,widget_id):
        """
        returns an instance of thre requested module with a set instanceId
        """
        db = Database()
        stmnt = "SELECT WGT_ID, WGT_NAME, WGT_VIE_BASEVIEW, WGT_SPA_BASESPACE FROM WIDGETS WHERE WGT_MOD_ID = ? AND WGT_ID = ? ;"
        cur = db.query(stmnt, (self._id,widget_id))

        row = cur.fetchonemap()
        if row is not None:
            widget = Widget(self, row["WGT_ID"])
            widget.set_name(row["WGT_NAME"])
            widget.set_baseview_id(row["WGT_VIE_BASEVIEW"])
            widget.set_baseview_space_id(row["WGT_SPA_BASESPACE"])
            return widget
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(7))

    def get_widgets(self):
        """
        returns an instance of thre requested module with a set instanceId
        """
        db = Database()
        stmnt = "SELECT WGT_ID, WGT_NAME, WGT_VIE_BASEVIEW, WGT_SPA_BASESPACE FROM WIDGETS WHERE WGT_MOD_ID = ? ;"
        cur = db.query(stmnt, (self._id,))

        widgets = []
        for row in cur.fetchallmap():
            widget = Widget(self, row["WGT_ID"])
            widget.set_name(row["WGT_NAME"])
            widget.set_baseview_id(row["WGT_VIE_BASEVIEW"])
            widget.set_baseview_space_id(row["WGT_SPA_BASESPACE"])
            widgets.append(widget)        
        return widgets

    def get_guidata(self):
        configuration = Configuration()
        modpath = configuration.get_entry("global.modpath")

        modulepath = modpath+"/"+self._name+"/v"+\
                              str(self._version_major)+"_"+ \
                              str(self._version_minor)+"_"+ \
                              str(self._revision)
        tar = tarfile.open(modulepath+"/gui.tar.gz","w:gz")
        tar.add(modulepath+"/gui")
        tar.close()

        f = open(modulepath+"/gui.tar.gz","r")
        data = f.read()
        f.close()

        os.unlink(modulepath+"/gui.tar.gz")
        return data

    def set_config_entry(self, entry, value, widget_id=None):
        """
        Sets a configuration entry for this module.
        If there is a widget id given, it changes the same
        configuration value of this widget.
        """
        configuration = Configuration()
        if widget_id is not None:
            widget = Module.get_widget(widget_id)
            configuration.set_entry(entry,value,widget=widget)
        else:    
            configuration.set_entry(entry,value,module=self)

    def get_config_entry(self, entry, widget_id=None):
        """
        Yields a configuration entry for this module.
        If there is a widget id given, it returns the
        configuration value of this widget. (MUST EXIST)
        """
        configuration = Configuration()
        if widget_id is not None:
            widget = Module.get_widget(widget_id)
            return configuration.get_entry(entry,widget=widget)
        else:    
            return configuration.get_entry(entry,module=self)

    def generate_view(self, widget_id, viewname, commands):
        """
        Acutally generates a named view according to the configuration of the widget
        """
        widget = Module.get_widget(widget_id)
        widget.generate_view(viewname, commands)

class Widget(object):
    def __init__(self, module, nr=None):
        self._id = nr
        self._module= module
        self._name = None
        self._site_id = None
        self._baseview_id = None
        self._baseview_space_id = None

    def set_id(self,nr):
        self._id = int(nr)

    def set_name(self,name):
        self._name = unicode(name)

    #TODO: Check if Widgets really still net Site-reference
    def set_site(self,site):
        if type(site)==int:
            self._site_id = site
        elif site.__class__.__name__ == "Site":
            self._site_id = site.get_id()

    def set_baseview_id(self, baseview_id):
        if type(baseview_id) == int or baseview_id is None:
            self._baseview_id = baseview_id

    def set_baseview_space_id(self, baseview_space_id):
        if type(baseview_space_id) == int or baseview_space_id is None:
            self._baseview_space_id = baseview_space_id

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    #TODO: Check if Widgets really still net Site-reference
    def get_site_id(self): 
        return self._site_id

    def get_baseview_id(self):
        return self._baseview_id

    def get_baseview_space_id(self):
        return self._baseview_space_id

    def render_pure_html(self,args={}):
        rendered = self._module.render_pure_html(self._id,args)
        return '<div class="%s w%d">%s</div>'%(self._module.get_name(), self._id, rendered)

    def render_html(self,args={}):
        rendered =  self._module.render_html(self._id,args)
        return '<div class="%s w%d">%s</div>'%(self._module.get_name(), self._id, rendered)

    def render_javascript(self,args={}):
        return self._module.render_javascript(self._id,args)

    def store(self):
        db = Database()

        if self._id is None:
            self._id = db.get_seq_next('WGT_GEN')

        if self._module is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(1))

        stmnt = "UPDATE OR INSERT INTO WIDGETS (WGT_ID, WGT_NAME, WGT_SIT_ID, WGT_MOD_ID, WGT_VIE_BASEVIEW, WGT_SPA_BASESPACE) \
                    VALUES (?,?,?,?,?,?) MATCHING (WGT_ID) ;"
        db.query(stmnt,(self._id,self._name, self._site_id,self._module.get_id(), self._baseview_id, self._baseview_space_id ),commit=True)
        PokeManager.add_activity(ActivityType.WIDGET)

    def get_module(self):
        """
        Returns the module of this widget
        """
        return Module.get_module_from_widget_id(self.get_id())

    def delete(self):
        db = Database()

        if self._id is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(2))

        Action.delete_actions_with_widget(self)

        View.delete_mappings_with_widget(self)

        css_manager = CSSManager()
        css_manager.delete_definitions_with_widget(self)

        stmnt = "DELETE FROM WIDGETS WHERE WGT_ID = ? ;"
        db.query(stmnt,(self._id,),commit=True)
        PokeManager.add_activity(ActivityType.WIDGET)

    def activate_viewgeneration(self, baseview, space_id):
        """
        Initializes the viewgeneration-feature.
        This feature allows the method generate_view to be used
        from within the module implementation-code

        It inherits from a baseview (most of the time this will
        typically be the defaultview)

        The space_id indicates in which space the widget of 
        this module should be rendered in the resulting
        named view.
        """
        self.set_baseview_id(baseview.get_id())
        self.set_baseview_space_id(space_id)
        self.store()

        module = self.get_module()
        module.set_config_entry("generate_views", "True", self.get_id())


    def generate_view(self, viewname, commands):
        """
        Actually generates a named view of the viewname,
        The baseview for this Widget, the space that has been set
        to be the target in the baseview and the set of
        commands provided in the dictionary commands
        """
        module = self.get_module()
        try:
            setting = module.get_config_entry("generate_views", self.get_id())
        except ConfigurationException:
            setting = "False"
        if setting == "True":
            newview = View.get_from_id(self.get_baseview_id()).derive()
            viewname = sluggify(viewname)
            extcount = 0
            while True:
                try:
                    viewmanager.get_from_name(viewname)
                except ViewException:
                    break
                else:
                    extcount +=1
                    viewname = viewname[:-int(1+(math.ceil(math.log(extcount,10))))]+str(extcount)
            newview.set_name(viewname)
            newview.get_space_widget_mapping()[self.get_baseview_space_id()] = self.get_id()
            newview.get_widget_param_mapping()[self.get_id()] = commands
            newview.store()

    def deactivate_viewgeneration(self):
        """
        Deactivate Generating views
        """
        self.set_baseview_id(None)
        self.set_baseview_space_id(None)
        self.store()

        module = self.get_module()
        module.set_config_entry("generate_views", "False", self.get_id())

    def is_generating_views(self):
        """
        Returns True if this widget is generating named views of its entries.
        Returns False if not.
        """
        module = self.get_module()
        try:
            return module.get_config_entry("generate_views", self.get_id()) == "True"
        except:
            return False


class ModuleManager(object):
    @staticmethod
    def get_module(module_id):
        """
        returns an instance of the requested module
        """
        module_id = int(module_id)
        db = Database()
        stmnt = "SELECT MOD_NAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV FROM MODULES WHERE MOD_ID = ? ;"
        cur = db.query(stmnt,(module_id,))
        row = cur.fetchonemap()
        if row is not None:
            exec "from skarphedcore.modules.%s.v%d_%d_%d import Module as ModuleImplementation"%(row["MOD_NAME"], row["MOD_VERSIONMAJOR"], row["MOD_VERSIONMINOR"], row["MOD_VERSIONREV"])
            module = ModuleImplementation() 
            module.set_id(module_id)
            return module
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(6))

    @classmethod
    def get_module_by_name(cls,name):
        nr = cls._get_module_id_from_name(name)
        return cls.get_module(nr)
    
    @classmethod
    def get_widget(cls,widget_id):
        """
        returns an instance of thre requested module with a set instanceId
        """
        module = cls._get_module_from_widget_id(widget_id)
        widget = module.get_widget(widget_id)
        return widget

    @staticmethod
    def _get_module_id_from_name(module_name):
        """
        returns the module id of the given module_name
        """
        module_name = str(module_name)
        db = Database()
        stmnt = "SELECT MOD_ID FROM MODULES WHERE MOD_NAME = ? ;"
        cur = db.query(stmnt,(module_name,))
        row = cur.fetchonemap()
        if row is not None:
            return int(row["MOD_ID"])
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(6))
    
    @classmethod
    def get_module_from_widget_id(cls,widget_id):
        return cls._get_module_from_widget_id(widget_id)

    @classmethod
    def _get_module_from_widget_id(cls, widget_id):
        """
        returns the module that belongs to a widget with the given id
        """
        db = Database()
        stmnt = "SELECT WGT_MOD_ID FROM WIDGETS WHERE WGT_ID = ? ;"
        cur = db.query(stmnt,(widget_id,))
        row = cur.fetchonemap()
        if row is not None:
            return cls.get_module(row["WGT_MOD_ID"])
        else:
            raise ModuleCoreException(ModuleCoreException.get_msg(7))

    @classmethod
    def check_integrity(cls):
        """
        Verifies, that all modules that are entered in the database
        for this instance, are in fact installed on the server that
        this instance runs on
        """
        db = Database()
        stmnt = "SELECT MOD_NAME, MOD_DISPLAYNAME,MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV FROM MODULES ;"
        cur = db.query(stmnt)
        rows = cur.fetchallmap()
        for row in rows:
            modpath = Configuration().get_entry("global.modpath")

            modulepath = modpath+"/"+row["MOD_NAME"]+"/v"+\
                                  str(row["MOD_VERSIONMAJOR"])+"_"+ \
                                  str(row["MOD_VERSIONMINOR"])+"_"+ \
                                  str(row["MOD_VERSIONREV"])
            if not os.path.exists(modulepath):
                module_meta = {"name":row["MOD_NAME"],
                               "hrname":row["MOD_DISPLAYNAME"],
                               "version_major":row["MOD_VERSIONMAJOR"],
                               "version_minor":row["MOD_VERSIONMINOR"],
                               "revision":row["MOD_VERSIONREV"]}
                cls.install_module(module_meta)

    @classmethod
    def install_module(cls, module_meta):
        """
        prepares the module installation by invoking the download
        """
        modpath = Configuration().get_entry("global.modpath")

        modulepath = modpath+"/"+module_meta["name"]+"/v"+\
                              str(module_meta["version_major"])+"_"+ \
                              str(module_meta["version_minor"])+"_"+ \
                              str(module_meta["revision"])

        if os.path.exists(modpath+"/"+module_meta["name"]):
            if not os.path.exists(modulepath):
                os.mkdir(modulepath)
        else:
            os.mkdir(modpath+"/"+module_meta["name"])
            open(modpath+"/"+module_meta["name"]+"/__init__.py","w").close()
            os.mkdir(modulepath)

        repo = cls.get_repository()
        return cls.install_module_write_changes(repo.download_module(module_meta), modulepath)

    @classmethod
    def install_module_write_changes(cls, datapath, modulepath):
        """
        actually write changes to local installation
        """

        tar = tarfile.open(datapath, "r:gz")

        tar.extractall(modulepath)
        manifest_file = open(modulepath+"/manifest.json","r")
        manifest = JSONDecoder().decode(manifest_file.read())
        manifest_file.close()

        # REGISTER THE MODULE IN DB
        try:
            nr = cls._register_module(manifest)
        except DatabaseException, e: #revert stuff on error
            Core().log(e)
            shutil.rmtree(modulepath)
            os.remove(datapath)
            raise e

        module = cls.get_module(nr)

        db = Database()

        # CREATE PERMISSIONS FOR MOUDLE
        try:
            Permission.create_permissions_for_module(module)
        except PermissionException, e: #revert on error
            cls._unregister_module(module)
            shutil.rmtree(modulepath)
            os.remove(datapath)
            raise e

        # CREATE DATBASE TABLES FOR MODULE
        try:
            db.create_tables_for_module(module)
        except DatabaseException, e:
            cls._unregister_module(module)
            shutil.rmtree(modulepath)
            Permission.remove_permissions_for_module(module)
            os.remove(datapath)
            raise e
        
        os.remove(datapath)
        PokeManager.add_activity(ActivityType.MODULE)

    @classmethod
    def update_module(cls,module):
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
            nr = cls._get_module_id_from_name(module_meta["name"])
            module = cls.get_module(nr)

        modpath = Configuration().get_entry('global.modpath')

        repo = cls.get_repository()
        latest_version = repo.get_latest_version(module)

        latest_path = modpath+"/"+latest_version["name"]+"/v"+\
                              str(latest_version["version_major"])+"_"+ \
                              str(latest_version["version_minor"])+"_"+ \
                              str(latest_version["revision"])

        if cls.compare_versions(latest_version, module) == 1:
            if not os.path.exists(latest_path):
                datapath = repo.download_module(latest_version)
                os.mkdir(latest_path)
                tar = tarfile.open(datapath, "r:gz")
                tar.extractall(latest_path)
            nr = cls._get_module_id_from_name(latest_version["name"])

            db = Database()
            stmnt = "UPDATE MODULES SET MOD_VERSIONMAJOR = ?, \
                                        MOD_VERSIONMINOR = ?, \
                                        MOD_VERSIONREV = ? \
                        WHERE MOD_ID = ? ;"
            db.query(stmnt,(latest_version["version_major"],
                                       latest_version["version_minor"],
                                       latest_version["revision"], 
                                       nr),commit=True)
            updated_module = cls.get_module(nr)
            db.update_tables_for_module(updated_module)
            Permission.update_permissions_for_module(updated_module)

        PokeManager.add_activity(ActivityType.MODULE)

    @classmethod
    def uninstall_module(cls,module, hard=False):
        """
        uninstall a module
        the flag "hard" actually deletes the files of this module in modpath
        module can be module or module meta
        """
        if module.__class__.__name__ != "Module":
            nr = cls._get_module_id_from_name(module_meta["name"])
            module = cls.get_module(nr)

        Action.delete_actions_with_module(module)
        View.delete_mappings_with_module(module)
        CSSManager().delete_definitions_with_module(module)

        db = Database()
        db.remove_tables_for_module(module)
        Permission.remove_permissions_for_module(module)

        if hard:
            modpath = Configuration().get_entry('global.modpath')
            version = module.get_version()
            shutil.rmtree(modpath+"/"+module.get_name()+"/v"+version[0]+"_"+version[1]+"_"+version[2])

        cls._unregister_module(module)
        PokeManager.add_activity(ActivityType.MODULE)

    @staticmethod
    def _register_module(manifest):
        """
        registers a module into the database
        """
        db = Database()
        nr = db.get_seq_next("MOD_GEN")
        stmnt = "INSERT INTO MODULES (MOD_ID, MOD_NAME, MOD_DISPLAYNAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_JSMANDATORY) \
                      VALUES (?,?,?,?,?,?,?) ;"
        db.query(stmnt,(nr,manifest["name"],manifest["hrname"],
                                   manifest["version_major"],manifest["version_minor"],
                                   manifest["revision"],manifest["js_mandatory"]),commit=True)
        return nr

    @staticmethod
    def _unregister_module(module):
        db = Database()
        stmnt = "DELETE FROM MODULES WHERE MOD_NAME = ? ;" 
        db.query(stmnt,(module.get_name(),),commit=True)

    @staticmethod
    def get_meta_from_module(module):
        d = {
            "name":module.get_name(),
            "hrname":module.get_hrname(),
            "version_major":module.get_version("major"),
            "version_minor":module.get_version("minor"),
            "revision":module.get_version("revision"),
            "js_mandatory":module.get_js_mandatory()
        }
        return d

    @staticmethod
    def get_repository():
        """
        returns this instance's repository
        """
        db = Database()
        stmnt = "select rep_id, rep_name, rep_ip, rep_port, rep_lastupdate from repositories where rep_id = 1;"
        cur = db.query(stmnt)
        row = cur.fetchonemap()
        return Repository(row["REP_ID"],row["REP_NAME"],row["REP_IP"],row["REP_PORT"],row["REP_LASTUPDATE"])

    @staticmethod
    def set_repository(ip, port, name):
        """
        changes this instance's repository
        """
        repository = Repository(None, name, ip, port, None)
        repository.store()
        return repository

    @classmethod
    def compare_versions(cls, module1, module2):
        """
        compares the versions of module1 and module2
        if module 1 is newer, returns 1
        if module 2 is newer, returns -1
        if equal, returns 0
        """

        if type(module1) != dict:
            module1 = cls.get_meta_from_module(module1)
        if type(module2) != dict:
            module2 = cls.get_meta_from_module(module2)
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

    @staticmethod
    def invoke_install(module_meta):
        """
        registers an operation, that installs a module
        """
        op = ModuleInstallOperation()
        op.set_values(module_meta)
        op.store()

    @staticmethod
    def invoke_update(module_meta):
        """
        registers an operation, that updates a module
        """
        op = ModuleUpdateOperation()
        op.set_values(module_meta)
        op.store()

    @staticmethod
    def invoke_uninstall(module_meta):
        """
        registers an operation, that uninstalls a module
        """
        op = ModuleUninstallOperation()
        op.set_values(module_meta)
        op.store()

    @classmethod
    def update_modules(cls):
        """
        update all modules of this instance
        """
        modules = cls.get_modules()
        for module in modules:
            cls.invoke_update(cls.get_meta_from_module(module))

    @classmethod
    def get_modules(cls):
        db = Database()
        stmnt = "SELECT MOD_ID FROM MODULES ;"
        cur = db.query(stmnt)
        ids = cur.fetchallmap()
        return [cls.get_module(i["MOD_ID"]) for i in ids]

    @classmethod
    def get_module_info(cls, only_installed=False):
        """
        get metalist of all installed modules with additional information
         - is there a possible update
        """
        meta_records = []
        for module in cls.get_modules():
            meta_record = cls.get_meta_from_module(module)
            meta_record.update({'installed':True,'serverModuleId':module.get_id()})
            meta_records.append(meta_record)

        repository_joblocks = ModuleOperation.get_currently_processed_modules()

        if not only_installed:
            repo = cls.get_repository()
            repomodules = repo.get_all_modules()
            for repomodule in repomodules:
                module_on_system = False
                for meta_record in meta_records:
                    if repomodule["name"] == meta_record["name"]:
                        if cls.compare_versions(repomodule, meta_record) == 1:
                            meta_record["toUpdate"] = True
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
    def __init__(self, nr=None, name=None, ip=None, port=80, lastupdate=None):
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

    def ping(self):
        try:
            self.load_public_key()
        except ModuleCoreException:
            return False
        else:
            return True

    def _http_call(self,msg, timeout=5):
        if self._jsondecoder is None:
            self._jsondecoder = JSONDecoder()
        if self._jsonencoder is None:
            self._jsonencoder = JSONEncoder()
        url = self.get_host()
        try:
            http = urlopen(url,timeout=timeout, data="j="+quote(self._jsonencoder.encode(msg).encode('utf-8')))
        except URLError:
            raise ModuleCoreException(ModuleCoreException.get_msg(9))
        return self._jsondecoder.decode(http.read())


    def get_all_modules(self):
        result = self._http_call({'c':1})
        return result["r"]

    def load_public_key(self):
        result = self._http_call({'c':6})
        return result["r"]

    def get_all_versions(self, module):
        if type(module) != dict:
            module = ModuleManager.get_meta_from_module(module)
        result = self._http_call({'c':2,'m':module})
        return result["r"]

    def get_latest_version(self, module):
        if type(module) != dict:
            module = ModuleManager.get_meta_from_module(module)
        result = self._http_call({'c':7,'m':module})
        return result["r"]

    def get_dependencies(self, module):
        if type(module) != dict:
            module = ModuleManager.get_meta_from_module(module)
        result = self._http_call({'c':3,'m':module})
        return result["r"]

    def get_descending_dependencies(self, module):
        if type(module) != dict:
            module = ModuleManager.get_meta_from_module(module)
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
        signature = base64.b64decode(signature)
        return verifier.verify(h,signature)

    def download_module(self,module):
        """
        downloads a module and
        returns the data directly!
        """
        if type(module) != dict:
            module = ModuleManager.get_meta_from_module(module)
        result = self._http_call({'c':5,'m':module},timeout=1800)
        if result is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(2))
        data = base64.b64decode(result["data"])
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

    def download_template(self, nr):
        """
        downloads a template, verifies its signature and returns its data
        """
        result = self._http_call({'c':9,'id':int(nr)})
        data = base64.b64decode(result['r'])
        if not self.verify_module(data, result['signature']):
            raise ModuleCoreException(ModuleCoreException.get_msg(3))
        else:
            return data

    def get_all_templates(self):
        result = self._http_call({'c':8})
        return result['r']

    def store(self):
        """
        currently only one repository can be owned by one skarphed instance
        """
        db = Database()
        stmnt = "UPDATE OR INSERT INTO REPOSITORIES (REP_ID, REP_NAME, REP_IP, REP_PORT, REP_LASTUPDATE, REP_PUBLICKEY) VALUES (1,?,?,?,?,?) MATCHING (REP_ID) ;"
        db.query(stmnt,(self._name, self._ip, self._port, self._lastupdate, self.get_public_key()),commit=True)
        PokeManager.add_activity(ActivityType.REPOSITORY)


    def delete(self):
        """
        deletes this repo from database
        """
        if self._id is None:
            raise ModuleCoreException(ModuleCoreException.get_msg(4))
        db = Database()

        stmnt = "DELETE FROM REPOSITORIES WHERE REP_ID = ? ;"
        db.query(stmnt,(self._id,),commit=True)
        PokeManager.add_activity(ActivityType.REPOSITORY)
