import os

from module import AbstractModule
#from moduleexpansion import ModuleExpansion

class ModuleException(Exception): 
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "DB_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class Module(AbstractModule):
    def __init__(self, core):
        AbstractModule.__init__(self,core)

        path = os.path.realpath(__file__)
        path = path.replace("__init__.pyc","")
        self._path = path.replace("__init__.py","")

        self._load_manifest()

    """
    BEGIN IMPLEMENTING YOUR MODULE HERE
    """

    def render_pure_html(self,widget_id,args={}):
        return "<h3>news! %s %s</h3>"%(ModuleExpansion().a,self._core.c)

    def render_html(self,widget_id,args={}):
        return "<h3>news! %s %s</h3>"%(ModuleExpansion().a,self._core.c)

    def render_javascript(self,widget_id,args={}):
        return """<script type="text/javascript"> alert('LOL');</script>"""

    def get_news(self,widget_id):
        db = self._core.get_db()
        stmnt = "SELECT NWS_ID, NWS_BLUB_ID"

    def get_news_entry(self,widget_id, entry_id):
        pass

    def save_news_entry(self, widget_id, entry_data):
        pass

    def create_news_entry(self, widget_id):
        pass