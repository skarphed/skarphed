

from json import JSONDecoder
import os

from moduleexpansion import ModuleExpansion

class Module(object):
    def __init__(self, core):
        self._core = core

        path = os.path.realpath(__file__)
        path = path.replace("__init__.pyc","")
        self._path = path.replace("__init__.py","")

        self._name = None
        self._hrname = None
        self._version_major = None
        self._version_minor = None
        self._revision = None
        self._permissions = [] 
        self._tables = []
        self._load_manifest()

    def _load_manifest(self):
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
        return self._tables

    def get_permssions(self):
        return self._permissions

    """
    BEGIN IMPLEMENTING YOUR MODULE HERE
    """

    def render_pure_html(self,args={}):
        return "<h3>news! %s %s</h3>"%(ModuleExpansion().a,self._core.c)

    def render_html(self,args={}):
        return "<h3>news! %s %s</h3>"%(ModuleExpansion().a,self._core.c)

    def render_javascript(self,args={}):
        return """<script type="text/javascript"> alert('LOL');</script>"""
