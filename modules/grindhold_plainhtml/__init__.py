#!/usr/bin/python
#-*- coding: utf-8 -*-

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

import os
from StringIO import StringIO

from module import AbstractModule

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
        self._path = os.path.dirname(__file__)
        self._load_manifest()

    """
    BEGIN IMPLEMENTING YOUR MODULE HERE
    """

    def render_pure_html(self,widget_id,args={}):
        content = self.get_content(widget_id)
        return"<h2>%s</h2>%s"%(content['title'],content['html'])

    def render_html(self,widget_id,args={}):
        return self.render_pure_html(widget_id, args)

    def render_javascript(self,widget_id,args={}):
        return ""

    def set_content(self, widget_id, content="", title=""):
        title = unicode(title)
        content = unicode(content)
        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO ${html} (MOD_INSTANCE_ID, HTM_TITLE, HTM_HTML) \
                   VALUES (?,?,?) MATCHING (MOD_INSTANCE_ID) ;"
        db.query(self, stmnt, (widget_id, title, content), commit=True)


    def get_content(self, widget_id):
        db = self._core.get_db()
        stmnt = "SELECT HTM_TITLE, HTM_HTML FROM ${html} WHERE MOD_INSTANCE_ID = ? ;"
        cur = db.query(self, stmnt, (widget_id,))
        row = cur.fetchonemap()
        if row is not None:
            return {'title':row["HTM_TITLE"],
                    'html':row["HTM_HTML"]}
        else:
            return {"title":"Widget not found",
                    "html":"<p>This widget does apparently not exist</p>"}


