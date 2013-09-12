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
        menu_id = content['menuId']
        action_manager = self._core.get_action_manager()
        menu = action_manager.get_menu_by_id(menu_id)
        menu_items = menu.get_menu_items()

        sub_menu_items = []

        render = StringIO()
        render.write("<div>")
        heights = []
        for menu_item in menu_items:
            lines = 1
            render.write('<div style="float:left; margin-right:30px;">')
            link = menu_item.get_action_list().render_link()
            name = menu_item.get_name()
            render.write('<p><a class="mainitem" href="%s">%s</a></p>'%(link, name))
            for sub_menu_item in menu_item.get_menu_items():
                lines += 1
                link = sub_menu_item.get_action_list().render_link()
                name = sub_menu_item.get_name()
                render.write('<p><a class="subitem" href="%s">%s</a></p>'%(link, name))
            heights.append(lines)
            render.write('</div>')
        for i in range(max(heights)):
            render.write("<p>&nbsp;</p>")
        render.write("</div>")
        return render.getvalue()

    def render_html(self,widget_id,args={}):
        return self.render_pure_html(widget_id, args)

    def render_javascript(self,widget_id,args={}):
        return ""

    def set_content(self, widget_id, menu_id):
        menu_id = int(menu_id)
        
        action_manager = self._core.get_action_manager()
        page_id = action_manager.get_menu_by_id(menu_id).get_page_id()
        
        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO ${footermenu} (MOD_INSTANCE_ID, FMN_SIT_ID, FMN_MNU_ID) \
                   VALUES (?,?,?) MATCHING (MOD_INSTANCE_ID) ;"
        db.query(self, stmnt, (widget_id, page_id, menu_id), commit=True)


    def get_content(self, widget_id):
        db = self._core.get_db()
        stmnt = "SELECT FMN_SIT_ID, FMN_MNU_ID FROM ${footermenu} WHERE MOD_INSTANCE_ID = ? ;"
        cur = db.query(self, stmnt, (widget_id,))
        row = cur.fetchonemap()
        if row is not None:
            return {'menuId':row["FMN_MNU_ID"]}
        else:
            return {"menuId":None}


