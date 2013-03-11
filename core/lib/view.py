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
import StringIO
import re

class ViewException(Exception):
    ERRORS = {
        0:"""Get By Name: No such view""",
        1:"""Invalid input type to specify Space""",
        2:"""Invalid input type to specify Widget""",
        3:"""There is no default view"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "VIE_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class PageException(Exception):
    ERRORS = {
        0:"""Create: This Page has no spaces. As useless as you.""",
        1:"""Space: There is no space with that name."""
        
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
    def get_default_view(cls):
        db = cls._core.get_db()
        stmnt = "SELECT VIE_NAME FROM VIEWS WHERE VIE_DEFAULT = 1 ;"
        cur = db.query(cls._core, stmnt)
        row = cur.fetchonemap()
        if row is not None:
            return cls.get_from_name(row["VIE_NAME"])
        else:
            raise ViewException(ViewException.get_msg(3))

    @classmethod
    def get_from_name(cls, name):
        """
        Searches in the database if there is a View
        with the given name. If there is, creates it
        with the data that can be retrieved from the database
        """
        db = cls._core.get_db()
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

        stmnt = "SELECT VWP_KEY, VWP_VALUE, VWP_WGT_ID FROM VIEWWIDGETPARAMS WHERE VWP_VIE_ID = ? ORDER BY VWP_WGT_ID;"
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
        view = View(cls._core)

    @classmethod
    def create_default_view(cls):
        db = cls._core.get_db()
        stmnt = "SELECT VIE_ID FROM VIEWS WHERE VIE_DEFAULT = 1 ;"
        cur = db.query(cls._core, stmnt)
        row = cur.fetchonemap()
        if row is None:
            view_id = db.get_seq_next("VIE_GEN")
            stmnt = "INSERT INTO VIEWS (VIE_ID, VIE_SIT_ID, VIE_NAME, VIE_DEFAULT) \
                       VALUES (?,2,'default',1) ;"
            db.query(cls._core, stmnt, (view_id,), commit=True)

    def __init__(self,core):
        """
        initializes View for rendering
        """
        self._core = core

        self._id = None

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

    def get_id(self):
        return self._id

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

    def place_widget_in_space(self, space, widget):
        if type(space) == int:
            pass
        elif type(space) == str:
            space = self._page.get_space_id_by_name(space)
        else:
            raise ViewException(ViewException.get_msg(1))

        if type(widget) != int:
            widget = widget.get_id()

        self._space_widget_mapping[space] = widget

    def set_params_for_widget(self, widget, params):
        if type(widget) != int:
            widget = widget.get_id()
        
        if type(params) != dict:
            raise ViewException(ViewException.get_msg(2))

        self._widget_param_mapping[widget] = params


    def generate_link_from_action(self,action):
        """
        returns a link that describes a call to a view that result of the action 
        """
        pass

    def generate_link_from_actionlist(self,actionlist):
        """
        returns a link that describes a call to a view that results of the actionlist
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
            <link href="static/%(page_css)s" rel="stylesheet" type="text/css">
            %(head)s
          </head>
          <body>
            %(body)s
          </body>
        </html>
        """
        
        page_manager = self._core.get_page_manager()
        page = page_manager.get_page(self._page) 

        head = page.get_html_head()
        body = page.get_html_body()

        module_manager = self._core.get_module_manager()

        # Find placeholders to substitute
        
        space_name_map = page.get_space_names()
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
        #css_url = css_manager.get_css_url()

        configuration = self._core.get_configuration()
        title = configuration.get_entry("core.name")

        page_css = page.get_css_filename()

        return frame%{'title':title,
                      'scv_css':"css_url",
                      'page_css':page_css,
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
        rendermode = configuration.get_entry("core.rendermode")
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
            db.query(self._core,stmnt,(self._id, int(space_id), int(widget_id)),commit=True)

        stmnt = "UPDATE OR INSERT INTO VIEWWIDGETPARAMS (VWP_VIE_ID, VWP_WGT_ID, VWP_KEY, VWP_VALUE) \
                  VALUES (?,?,?,?) MATCHING (VWP_VIE_ID, VWP_WGT_ID) ;"
        for widget_id, propdict in self._space_widget_mapping['c'].items():
            for key, value in propdict.items():
                db.query(self._core,stmnt,(self._id, int(widget_id), str(key), str(value)),commit=True)

        stmnt = "UPDATE OR INSERT INTO VIEWS (VIE_ID, VIE_SIT_ID, VIE_NAME, VIE_DEFAULT) \
                  VALUES (?,?,?,?) MATCHING (VIE_ID) ;"
        db.query(self._core, stmnt, (self._id, self._page.get_id(), self._name, int(self._default)),commit=True)

    def delete(self):
        """
        deletes this view from the database
        """

        db = self._core.get_db()
        stmnt = "DELETE FROM VIEWWIDGETPARAMS WHERE VWP_VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)
        stmnt = "DELETE FROM VIEWWIDGETS WHERE VIW_VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)
        stmnt = "DELETE FROM VIEWS WHERE VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)


class ViewManager(object):
    def __init__(self, core):
        self._core = core

        View.set_core(core)
        self.get_from_name = View.get_from_name
        self.get_from_json = View.get_from_json
        self.get_default_view = View.get_default_view
        self.create_default_view = View.create_default_view
        self.create = View.create


class Page(object):
    """
    The Page represents one HTML-Document that contains
    Placeholders to be filled with Widgets.
    Those placeholders are called Spaces. One Page has n
    Spaces
    """
    @classmethod
    def set_core(cls, core):
        cls._core = core

    @classmethod
    def get_page(cls, nr):
        """
        Returns a Page in the Database that has the given id
        """
        db = cls._core.get_db()
        stmnt = "SELECT SIT_NAME, SIT_DESCRIPTION, SIT_HTML, SIT_HTML_HEAD, SIT_BIN_MINIMAP, SIT_BIN_CSS \
                 FROM SITES WHERE SIT_ID = ? ;"
        cur = db.query(cls._core, stmnt, (int(nr),))
        res = cur.fetchonemap()
        if res:
            page = Page(cls._core)
            page._name = res["SIT_NAME"]
            page._description = res["SIT_DESCRIPTION"]
            page._id = int(nr)
            page._html_body = res["SIT_HTML"]
            page._html_head = res["SIT_HTML_HEAD"]
            page._minimap_id = res["SIT_BIN_MINIMAP"]
            page._css_id = res["SIT_BIN_CSS"]
            return page
        else:
            raise Exception("No such Page %d"%(nr,))

    @classmethod
    def delete_all_pages(cls):
        """
        Deletes all Pages

        Pages are not something, that are to be edited one by one. 
        Pages are delivered as a package by templates. And They are all
        to be removed at Template uninstallation
        """
        db = cls._core.get_db()
        stmnt = "DELETE FROM SITES ;"
        db.query(cls._core, stmnt, commit=True)
        stmnt = "DELETE FROM SPACES ;"
        db.query(cls._core, stmnt, commit=True)

    @classmethod
    def create(cls, name, internal_name, description, html_body, html_head, css, minimap=None):
        """
        Creates A Page (normally as a part of the installation process of a Template)
        in Database
        """

        placeholders = re.findall(r"<%[^%>]+%>",html_body)
        placeholders = [p.replace("<%","",1) for p in placeholders]
        placeholders = [p.replace("%>","",1) for p in placeholders]
        placeholders = [p.strip() for p in placeholders]

        if len(placeholders) < 1:
            pass # Eventually we need to check for Pages with no spaces. Not an error yet

        html_head_io = StringIO.StringIO(html_head)
        html_body_io = StringIO.StringIO(html_body)

        binary_manager = cls._core.get_binary_manager()
        
        minimap_id = None
        if minimap is not None:
            minimap_binary = binary_manager.create("image/png", minimap)
            minimap_binary.set_filename(internal_name+"_minimap.png")
            minimap_binary.store()
            minimap_id = minimap_binary.get_id()

        css_binary = binary_manager.create("text/css", css)
        css_binary.set_filename(internal_name+".css")
        css_binary.store()
        css_id = css_binary.get_id()

        stmnt = "INSERT INTO SITES (SIT_ID, SIT_HTML, SIT_HTML_HEAD, SIT_DESCRIPTION, SIT_NAME, SIT_BIN_MINIMAP, SIT_BIN_CSS) \
                 VALUES (?,?,?,?,?,?,?) ;"

        db = cls._core.get_db()
        new_sit_id = db.get_seq_next("SIT_GEN")

        db.query(cls._core, stmnt , (new_sit_id, html_body_io, html_head_io, description, name, minimap_id, css_id), commit=True)

        stmnt= "INSERT INTO SPACES (SPA_ID, SPA_SIT_ID, SPA_NAME ) VALUES (?,?,?) ; "

        for placeholder in placeholders:
            new_space_id = db.get_seq_next("SPA_GEN")
            db.query(cls._core, stmnt, (new_space_id, new_sit_id, placeholder ), commit=True )


    def __init__(self,core):
        self._core = core

        self._id = None
        self._name = None
        self._description = None
        self._minimap_id = None
        self._css_id = None

        self._html_head = None
        self._html_body = None

    def get_id(self):
        return self._id

    def get_html_head(self):
        return self._html_head

    def get_html_body(self):
        return self._html_body

    def get_space_names(self):
        db = self._core.get_db()
        stmnt = "SELECT SPA_ID, SPA_NAME FROM SPACES WHERE SPA_SIT_ID = ? ;"
        cur = db.query(self._core,stmnt,(self.get_id(),))
        ret = {}
        rows = cur.fetchallmap()
        for row in rows:
            ret[row["SPA_ID"]] = row["SPA_NAME"]
    
    def get_space_id_by_name(self, name):
        sn = self.get_space_names()
        for key, value in sn.items():
            if value == name:
                return key
        raise PageException(PageException.get_msg(1))  

    def get_css_filename(self):
        binary_manager = self._core.get_binary_manager()
        binary_css = binary_manager.get_by_id(self._css_id)
        return binary_css.get_filename()

    def delete(self):
        binary_manager = self._core.get_binary_manager()
        minimap_bin = binary_manager.get_by_id(self._minimap_id)
        minimap_bin.delete()

        css_bin = binary_manager.get_by_id(self._css_id)
        css_bin.delete()

        db = self._core.get_db()
        stmnt = "DELETE FROM SPACES WHERE SPA_SIT_ID = ? ;"
        db.query(self._core, stmnt, (self.get_id(),), commit=True)

        stmnt = "DELETE FROM SITES WHERE SIT_ID = ? ;"
        db.query(self._core, stmnt, (self.get_id(),), commit=True)
        
class PageManager(object):
    def __init__(self, core):
        self._core = core

        Page.set_core(core)
        self.get_page = Page.get_page
        self.create = Page.create
        self.delete_all_pages = Page.delete_all_pages


