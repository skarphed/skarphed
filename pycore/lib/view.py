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
import re

class ViewException(Exception):
    ERRORS = {
        0:"""Get By Name: No such view"""
        
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "VIE_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class View(object):
    @classmethod
    def set_core(cls, core):
        """
        trivial
        """
        cls._core = core

    @classmethod
    def get_from_name(cls, name):
        """
        Searches in the database if there is a View
        with the given name. If there is, creates it
        with the data that can be retrieved from the database
        """
        db = self._core.get_db()
        stmnt = "SELECT VIE_ID, VIE_SIT_ID, VIE_DEFAULT FROM VIEWS WHERE VIE_NAME = ? ;"
        cur = db.query(cls._core, stmnt, (str(name),))
        row = cur.fetchonemap()
        if row is None:
            raise ViewException(ViewException.get_msg(0))
        else:
            view = View(cls._core)
            view.set_name(str(name))
            view.set_default(row["VIE_DEFAULT"])
            view.set_page(row["VIE_SIT_ID"])
            view.set_id = (row["VIE_ID"])

        stmnt = "SELECT VIW_SPA_ID, VIW_WGT_ID FROM VIEWWIDGETS WHERE VIW_VIE_ID = ? ;"
        cur = db.query(cls._core, stmnt, (view.get_id(),))
        rows = cur.fetchallmap()
        space_widget_mapping = {}
        for row in rows:
            space_widget_mapping[row["VIW_SPA_ID"]] = row["VIW_WGT_ID"]
        view.set_space_widget_mapping(space_widget_mapping)

        stmnt = "SELECT VWP_KEY, VWP_VALUE, VWP_WGT_ID FROM VIEWWIDGETPARAMS WHERE VIW_VIE_ID = ? ORDER BY VIW_WGT_ID;"
        cur = db.query(cls._core, stmnt, (view.get_id(),))
        rows = cur.fetchallmap()
        widget_param_mapping = {}
        for row in rows:
            if not widget_param_mapping.has_key(row["VWP_WGT_ID"]):
                widget_param_mapping[row["VWP_WGT_ID"]] = {}
            widget_param_mapping["VWP_WGT_ID"][row["VWP_KEY"]]= row["VWP_VALUE"]
        view.set_widget_param_mapping(widget_param_mapping)

        return view
        
    @classmethod
    def get_from_json(cls, json):
        """
        creates a view from a json that looks like this:

        {'s':<page_id>,
         'v':{'<space_id>':<widget_id>,'<space_id>':<widget_id>,[...]},
         'c':{'wgt_id>': {<widget_args},'wgt_id':{<widget_args>}}
         'p':<wgt_id>
        }

        's' is the page that this view is going to be rendered on 
        'v' is a dictionary that maps space_ids to widget_ids
        'c' maps parameters to widgets
        'p' is an OPTIONAL parameter. if a html-form is submitted, this 
            contains a widget_id to 
        """
        pass

    @classmethod
    def create(cls, page, name, json):
        view = View(self._core)

    def __init__(self,core):
        """
        initializes View for rendering
        """
        self._core = core

        self._space_widget_mapping = {}
        self._widget_param_mapping = {}
        self._page = None
        self._name = None
        self._post_widget_id = None
        self._default = False

    def set_name(self, name):
        """
        trivial
        """
        self._name = str(name)

    def set_page(self, page):
        """
        trivial
        """
        if type(page) == int:
            #TODO: get page
            page = page
        self._page = page

    def set_default(self, default):
        self._default = bool(default)

    def set_widget_param_mapping(self, mapping):
        self._widget_param_mapping = mapping

    def set_space_widget_mapping(self, mapping):
        self._space_widget_mapping = mapping


    def generate_link_from_action(self,action):
        """
        returns a link that describes a call to a view that result of the action 
        """
        pass

    def render_pure(self):
        """
        renders this view with pure http-abilities. no script needed
        """
        frame = """
        <!DOCTYPE html>
        <html>
          <head>
            <title>%(title)s</title>
            <link href="%(scv_css)s" rel="stylesheet" type="text/css">
            %(head)s
          </head>
          <body>
            %(body)s
          </body>
        </html>
        """

        head = self._page.get_html_head()
        body = self._page.get_html_body()

        module_manager = self._core.get_module_manager()

        # Find placeholders to substitute
        placeholders = re.findall(r"<%[^%>]+%>",a)
        space_name_map = self._page.get_space_names()
        for space, widget_id in self._space_widget_mapping:
            space_name = space_name_map[space]
            widget = module_manager.get_widget(widget_id)

            args = {} 
            if self._widget_param_mapping.has_key(str(widget_id)):
                args.update(self._widget_param_mapping[str(widget_id)])
            if self._post_widget_id == widget_id:
                # TODO: Implement arguments getting prepared from POSTDATA
                pass

            widget_html = widget.render_pure_html(args)
            body = re.sub(r"<%%\s?%s\s?%%>"%space_name,widget_html,body)

        body = re.sub(r"<%[^%>]+%>","",body) #Replace all unused spaces with emptystring

        css_manager = self._core.get_css_manager()
        css_url = css_manager.get_css_url()

        configuration = self._core.get_css_manager()
        title = configuration.get_entry("core.name")

        return frame%{'title':title,
                      'scv_css':css_url,
                      'head':head,
                      'body':body}


    def render_ajax(self):
        #TODO: Implement
        pass

    def render(self):
        """
        render this view
        """
        configuration = self._core.get_configuration()
        render_mode = configuration.get_entry("core.rendermode")
        if rendermode == "pure":
            return self.render_pure()
        elif rendermode == "ajax":
            return self.render_ajax()

    def store(self):
        """
        stores this view in the database
        """
        db = self._core.get_db()
        if self._id is None:
            self._id = db.get_seq_next("VIE_GEN")

        stmnt = "UPDATE OR INSERT INTO VIEWWIDGETS (VIW_VIE_ID, VIW_SPA_ID, VIW_WGT_ID) \
                  VALUES (?,?,?) MATCHING (VIW_VIE_ID, VIW_SPA_ID) ;"
        for space_id, widget_id in self._space_widget_mapping['v'].items():
            db.query(self._core,stmnt,(self._id, int(space_id), int(widget_id)))

        stmnt = "UPDATE OR INSERT INTO VIEWWIDGETPARAMS (VWP_VIE_ID, VWP_WGT_ID, VWP_KEY, VWP_VALUE) \
                  VALUES (?,?,?,?) MATCHING (VWP_VIE_ID, VWP_WGT_ID) ;"
        for widget_id, propdict in self._space_widget_mapping['c'].items():
            for key, value in propdict.items():
                db.query(self._core,stmnt,(self._id, int(widget_id), str(key), str(value)))

        stmnt = "UPDATE OR INSERT INTO VIEWS (VIE_ID, VIE_SIT_ID, VIE_NAME, VIE_DEFAULT) \
                  VALUES (?,?,?,?) MATCHING (VIE_ID) ;"
        db.query(self._core, stmnt, (self._id, self._page.get_id(), self._name, int(self._default)))

    def delete(self):
        """
        deletes this view from the database
        """

        db = self._core.get_db()
        stmnt = "DELETE FROM VIEWWIDGETPARAMS WHERE VWP_VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,))
        stmnt = "DELETE FROM VIEWWIDGETS WHERE VIW_VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,))
        stmnt = "DELETE FROM VIEWS WHERE VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,))


class Page(object):
    def __init__(self,core):
        self._core = core

        self._id = None

        self._html_head = None
        self._html_body = None

    def get_id(self):
        return self._id

    def get_html_head(self):
        return self._html_head

    def get_html_body(self):
        return self._html_head

    def get_space_names(self):
        db = self._core.get_db()
        stmnt = "SELECT SPA_ID, SPA_NAME FROM SPACES WHERE SPA_SIT_ID = ? ;"
        cur = db.query(self._core,stmnt,(self.get_id(),))
        ret = {}
        rows = cur.fetchallmap()
        for row in rows:
            ret[row["SPA_ID"]] = row["SPA_NAME"]


