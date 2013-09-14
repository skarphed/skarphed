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

from json import JSONDecoder, JSONEncoder
from urllib2 import unquote, quote
from cgi import FieldStorage
import StringIO
import re
from copy import deepcopy

from ajax import AJAXScript

from common.enums import ActivityType, BoxOrientation
from common.errors import ViewException, PageException

class View(object):
    CURRENTLY_RENDERING = None
    @classmethod
    def set_core(cls, core):
        """
        trivial
        """
        cls._core = core

    @classmethod
    def get_currently_rendering_view(cls):
        return cls.CURRENTLY_RENDERING

    @classmethod
    def set_currently_rendering_view(cls, view):
        cls.CURRENTLY_RENDERING = view

    @classmethod
    def get_viewlist(cls):
        """
        returns a list of available views for the GUI
        in a heavily used skarphed environment there 
        will be a huge amount of views so it makes
        more sense to load them on demand than to load
        them on every skarphed start
        """
        db = cls._core.get_db()
        stmnt = "SELECT VIE_ID, VIE_NAME, VIE_DEFAULT FROM VIEWS ;"
        cur = db.query(cls._core, stmnt)
        res = cur.fetchallmap()
        ret = []
        for row in res:
            ret.append({
                  'id': row["VIE_ID"],
                  'name': row["VIE_NAME"],
                  'default': bool(row["VIE_DEFAULT"])
                })
        return ret

    @classmethod
    def get_from_id(cls, nr):
        """
        returns the view that is given by this id
        """
        db = cls._core.get_db()
        stmnt = "SELECT VIE_NAME, VIE_SIT_ID, VIE_DEFAULT FROM VIEWS WHERE VIE_ID = ? ;"
        cur = db.query(cls._core, stmnt, (int(nr),))
        row = cur.fetchonemap()
        if row is None:
            raise ViewException(ViewException.get_msg(0))
        else:
            configuration = cls._core.get_configuration()
            rendermode = configuration.get_entry("core.rendermode")
            if rendermode == "pure":
                view = PureView(cls._core)
            elif rendermode == "ajax":
                view = AJAXView(cls._core)
            view.set_name(row["VIE_NAME"])
            view.set_default(row["VIE_DEFAULT"])
            view.set_page(row["VIE_SIT_ID"])
            view.set_id(nr)

        stmnt = "SELECT VIW_SPA_ID, VIW_WGT_ID FROM VIEWWIDGETS WHERE VIW_VIE_ID = ? ;"
        cur = db.query(cls._core, stmnt, (view.get_id(),))
        rows = cur.fetchallmap()
        space_widget_mapping = {}
        for row in rows:
            space_widget_mapping[row["VIW_SPA_ID"]] = row["VIW_WGT_ID"]
        view.set_space_widget_mapping(space_widget_mapping)

        stmnt = "SELECT BOX_ID, BWT_WGT_ID \
                 FROM BOXES LEFT JOIN BOXWIDGETS ON (BOX_ID = BWT_BOX_ID) \
                 WHERE BWT_VIE_ID = ? OR (BWT_VIE_ID IS NULL AND BOX_SIT_ID = ?) \
                 ORDER BY BWT_BOX_ID, BWT_ORDER ;"
        cur = db.query(cls._core, stmnt, (view.get_id(), view.get_page()))
        rows = cur.fetchallmap()
        box_mapping = {}
        for row in rows:
            box_id = int(row["BOX_ID"])
            if not box_mapping.has_key(box_id):
                box_mapping[box_id] = []
            if row["BWT_WGT_ID"] is not None:
                box_mapping[box_id].append(row["BWT_WGT_ID"])
        view.set_box_mapping(box_mapping)

        stmnt = "SELECT VWP_KEY, VWP_VALUE, VWP_WGT_ID FROM VIEWWIDGETPARAMS WHERE VWP_VIE_ID = ? ORDER BY VWP_WGT_ID;"
        cur = db.query(cls._core, stmnt, (view.get_id(),))
        rows = cur.fetchallmap()
        widget_param_mapping = {}
        for row in rows:
            if not widget_param_mapping.has_key(row["VWP_WGT_ID"]):
                widget_param_mapping[row["VWP_WGT_ID"]] = {}
            widget_param_mapping[row["VWP_WGT_ID"]][row["VWP_KEY"]]= row["VWP_VALUE"]
        view.set_widget_param_mapping(widget_param_mapping)

        return view


    @classmethod
    def get_default_view(cls):
        db = cls._core.get_db()
        stmnt = "SELECT VIE_ID FROM VIEWS WHERE VIE_DEFAULT = 1 ;"
        cur = db.query(cls._core, stmnt)
        row = cur.fetchonemap()
        if row is not None:
            return cls.get_from_id(row["VIE_ID"])
        else:
            raise ViewException(ViewException.get_msg(3))

    @classmethod
    def get_from_name(cls, name):
        """
        Searches in the database if there is a View
        with the given name. If there is, creates it
        with the data that can be retrieved from the database
        """
        if len(name) > 128:
            return None # Prevents DB-Error. Change VIE_NAME in scvdb.sql too if changing here
        db = cls._core.get_db()
        stmnt = "SELECT VIE_ID FROM VIEWS WHERE VIE_NAME = ? ;"
        cur = db.query(cls._core, stmnt, (str(name),))
        row = cur.fetchonemap()
        if row is None:
            raise ViewException(ViewException.get_msg(0))
        else:
            return cls.get_from_id(row["VIE_ID"])
        
    @classmethod
    def get_from_json(cls, json):
        """
        creates a view from a json that looks like this:

        {'s':<page_id>,
         'v':{'<space_id>':<widget_id>,'<space_id>':<widget_id>,[...]},
         'b':{'<box_id>':[<widget_id>, <widget_id>, [...]]},
         'c':{'<wgt_id>': {<widget_args>},'wgt_id':{<widget_args>},[...]},
         'p':<wgt_id>
        }

        's' is the page that this view is going to be rendered on 
        'v' is a dictionary that maps space_ids to widget_ids
        'b' represents box-packed widgets
        'c' maps parameters to widgets
        'p' is an OPTIONAL parameter. if a html-form is submitted, this 
            contains a widget_id to 
        """

        json = unquote(json)
        jd = JSONDecoder()
        try:
            json = jd.decode(json)
        except ValueError:
            raise ViewException(ViewException.get_msg(7))

        configuration = cls._core.get_configuration()
        rendermode = configuration.get_entry("core.rendermode")
        if rendermode == "pure":
            view = PureView(cls._core)
        elif rendermode == "ajax":
            view = AJAXView(cls._core)

        if json.has_key('s'):
            view.set_page(json['s'])
        else:
            raise ViewException(ViewException.get_msg(6))

        if json.has_key('v'):
            for key, value in json['v'].items(): #transform indices back to int
                json['v'][int(key)] = value
                del(json['v'][key])
            view.set_space_widget_mapping(json['v'])
        else:
            view.set_space_widget_mapping({})

        if json.has_key('b'):
            for key, value in json['b'].items(): #transform indices back to int
                json['b'][int(key)] = value
                del(json['b'][key])
            view.set_box_mapping(json['b'])
        else:
            view.set_box_mapping({})

        if json.has_key('c'):
            for key, value in json['c'].items(): #transform indices back to int
                json['c'][int(key)] = value
                del(json['c'][key])
            view.set_widget_param_mapping(json['c'])
        else:
            view.set_widget_param_mapping({})
        if json.has_key('p'):
            view.set_post_widget_id(json['p'])

        return view

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
                       VALUES (?,1,'default',1) ;"
            db.query(cls._core, stmnt, (view_id,), commit=True)

    @classmethod
    def delete_mappings_with_module(cls, module):
        """
        Delete all mappings that concern the given widget
        Usually called when a whole module is uninstalled 
        """
        db = cls._core.get_db()
        stmnt = "DELETE FROM VIEWWIDGETS WHERE VIW_WGT_ID IN (SELECT WGT_ID FROM WIDGETS WHERE WGT_MOD_ID = ? ) ;"
        db.query(cls._core, stmnt, (module.get_id(),),commit=True)
        stmnt = "DELETE FROM BOXWIDGETS WHERE BWT_WGT_ID IN (SELECT WGT_ID FROM WIDGETS WHERE WGT_MOD_ID = ? ) ;"
        db.query(cls._core, stmnt, (module.get_id(),),commit=True)
        stmnt = "DELETE FROM VIEWWIDGETPARAMS WHERE VWP_WGT_ID IN (SELECT WGT_ID FROM WIDGETS WHERE WGT_MOD_ID = ? ) ;"
        db.query(cls._core, stmnt, (module.get_id(),),commit=True)
        return

    @classmethod
    def delete_mappings_with_widget(cls, widget):
        """
        Delete all mappings that concern the given widget
        Usually called when a widget is deleted 
        """
        db = cls._core.get_db()
        stmnt = "DELETE FROM VIEWWIDGETS WHERE VIW_WGT_ID = ? ;"
        db.query(cls._core, stmnt, (widget.get_id(),),commit=True)
        stmnt = "DELETE FROM BOXWIDGETS WHERE BWT_WGT_ID = ? ;"
        db.query(cls._core, stmnt, (widget.get_id(),),commit=True)
        stmnt = "DELETE FROM VIEWWIDGETPARAMS WHERE VWP_WGT_ID = ? ;"
        db.query(cls._core, stmnt, (widget.get_id(),),commit=True)
        return

    def __init__(self,core):
        """
        initializes View for rendering
        """
        self._core = core

        self._id = None

        self._space_widget_mapping = {}
        self._box_mapping = {}
        self._widget_param_mapping = {}
        self._page = None
        self._name = None
        self._post_widget_id = None
        self._default = False

    def clone(self):
        view = View(self._core)
        view.set_space_widget_mapping(deepcopy(self.get_space_widget_mapping()))
        view.set_box_mapping(deepcopy(self.get_box_mapping()))
        view.set_widget_param_mapping(deepcopy(self.get_widget_param_mapping()))
        view.set_page(self.get_page())
        postwidget_id = self.get_post_widget_id()
        if postwidget_id is not None:
            view.set_post_widget_id(postwidget_id)
        return view

    def set_name(self, name):
        """
        trivial
        """
        self._name = str(name)

    def get_name(self):
        return self._name

    def set_id(self, nr):
        self._id = nr

    def get_id(self):
        return self._id

    def set_post_widget_id(self, nr):
        self._post_widget_id = int(nr)

    def set_page(self, page):
        """
        trivial
        """
        if type(page) == int:
            #TODO: get page
            page = page
        self._page = page

    def get_page(self):
        return self._page

    def set_default(self, default):
        self._default = bool(default)

    def get_post_widget_id(self):
        return self._post_widget_id

    def get_default(self):
        return self._default

    def set_widget_param_mapping(self, mapping):
        self._widget_param_mapping = mapping

    def set_space_widget_mapping(self, mapping):
        self._space_widget_mapping = mapping

    def set_box_mapping(self, mapping):
        self._box_mapping = mapping

    def get_box_mapping(self):
        return self._box_mapping

    def get_space_widget_mapping(self):
        return self._space_widget_mapping

    def get_widget_param_mapping(self):
        return self._widget_param_mapping

    def get_box_info(self, box_id):
        stmnt = "SELECT BOX_ORIENTATION, BOX_NAME FROM BOXES WHERE BOX_ID = ? ;"
        db = self._core.get_db()
        cur = db.query(self._core, stmnt, (int(box_id),))
        row = cur.fetchonemap()
        if row is None:
            raise ViewException(ViewException.get_msg(9))
        else:
            return row["BOX_ORIENTATION"], row["BOX_NAME"]

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

    def remove_widget_from_space(self, space):
        if type(space) == int:
            pass
        elif type(space) == str:
            space = self._page.get_space_id_by_name(space)
        else:
            raise ViewException(ViewException.get_msg(1))
            
        if self._space_widget_mapping.has_key(space):
            del(self._space_widget_mapping[space])

    def set_params_for_widget(self, widget, params):
        if type(widget) != int:
            widget = widget.get_id()
        
        if type(params) != dict:
            raise ViewException(ViewException.get_msg(2))

        if widget not in self._space_widget_mapping.values():
            raise ViewException(ViewException.get_msg(4))

        self._widget_param_mapping[widget] = params

    def check_has_name(self):
        """
        Checks if this view has already a name in Database
        A name is present if 
        there is a View that has the complete SpaceWidget-Mapping in DB 
        AND the complete WidgetParam-Mapping and the same page Id 
        Returns the name if there is one
        Returns False if there is no corresponding view
        """
        #TODO: Rewrite. Doesn't work anyways and needs code for boxes
        db = self._core.get_db()
        stmnt_params = []
        stmnt = "SELECT COUNT(VIW_VIE_ID) AS CNT, VIW_VIE_ID FROM VIEWWIDGETS INNER JOIN VIEWS ON VIW_VIE_ID = VIE_ID WHERE 1=0"
        for space_id , widget_id in self._space_widget_mapping.items():
            stmnt += " OR VIW_SPA_ID = ? AND VIW_WGT_ID = ? AND VIE_SIT_ID = ? "
            stmnt_params.extend((int(space_id), int(widget_id), self._page))
        stmnt += " GROUP BY VIW_VIE_ID ;"

        stmnt2_params = []
        stmnt2 = "SELECT COUNT(VWP_VIE_ID) AS CNT, VWP_VIE_ID FROM VIEWWIDGETPARAMS INNER JOIN VIEWS ON VWP_VIE_ID = VIE_ID WHERE 1=0"
        for wgt_id, params in self._widget_param_mapping.items():
            for key, value in params.items():
                stmnt2 += " OR VWP_WGT_ID = ? AND VWP_KEY = ? AND VWP_VALUE = ? AND VIE_SIT_ID = ? "
                stmnt2_params.extend((int(wgt_id), str(key), str(value), self._page))
        stmnt2 += " GROUP BY VWP_VIE_ID ;"

        db_param_mappingcounts = {}

        cur = db.query(self._core, stmnt2, stmnt2_params)
        res2 = cur.fetchallmap()

        for row in res2:
            db_param_mappingcounts[row["VWP_VIE_ID"]] = row["CNT"]

        cur = db.query(self._core, stmnt, stmnt_params)
        res1 = cur.fetchallmap()

        possible_views = []
        for row in res1:
            if row["CNT"] == len(self._space_widget_mapping):
                view_paramcount = 0
                for wgt_id , params in self._widget_param_mapping.items():
                    view_paramcount += len(params)
                if db_param_mappingcounts.has_key(row["VIW_VIE_ID"]) and view_paramcount == 0:
                    continue
                if (db_param_mappingcounts.has_key(row["VIW_VIE_ID"]) and db_param_mappingcounts[row["VIW_VIE_ID"]] == view_paramcount) \
                        or view_paramcount == 0:
                    possible_views.append(row["VIW_VIE_ID"])

        if len(possible_views) > 0:
            stmnt= "SELECT VIE_NAME FROM VIEWS WHERE VIE_ID = ? ;"
            cur = db.query(self._core, stmnt, (possible_views[0],))
            row = cur.fetchonemap()
            return row["VIE_NAME"]
        else:
            return False


    def generate_link_from_action(self,action):
        """
        returns a link that describes a call to a view that result of the action 
        """
        pass

    def generate_link_from_dict(self, dct):
        """
        Creates a link by analyzing a view-dictionary and merging it to this view
        The incoming dictionary can be thought of as a diff that is added to the 
        existing view.
        Does not affect the View itself.
        """
        target = {}
        target['s'] = self.get_page()
        target['v'] = deepcopy(self.get_space_widget_mapping())
        target['b'] = deepcopy(self.get_box_mapping())
        target['c'] = deepcopy(self.get_widget_param_mapping())
        
        if dct.has_key('s'):
            target['s'] = dct['s']
        if dct.has_key('v'):
            target['v'].update(dct['v'])
        if dct.has_key('b'):
            target['b'].update(dct['b'])
        if dct.has_key('c'):
            for widget_id in dct['c'].keys():
                target['c'][widget_id] = dct['c'][widget_id]
        if dct.has_key('p'):
            target['p'] = dct['p']

        encoder = JSONEncoder()
        viewjsonstring = quote(encoder.encode(target))
        view_manager = self._core.get_view_manager()
        checkview = view_manager.get_from_json(viewjsonstring)
        existing_name = checkview.check_has_name()
        if existing_name == False:
            return "/web/?"+viewjsonstring
        else:
            return "/web/"+existing_name
            

    def store(self):
        """
        stores this view in the database
        """
        db = self._core.get_db()
        if self._id is None:
            self._id = db.get_seq_next("VIE_GEN")
        
        # Get current space-widgetmapping to determine, which mappings to delete
        stmnt = "SELECT VIW_SPA_ID, VIW_WGT_ID FROM VIEWWIDGETS WHERE VIW_VIE_ID = ? ;"
        cur = db.query(self._core, stmnt, (self.get_id(),))
        dbSpaceWidgetMap = {}
        for row in cur.fetchallmap():
            dbSpaceWidgetMap[row["VIW_SPA_ID"]] = row["VIW_WGT_ID"]

        # update widgets
        stmnt = "UPDATE OR INSERT INTO VIEWWIDGETS (VIW_VIE_ID, VIW_SPA_ID, VIW_WGT_ID) \
                  VALUES (?,?,?) MATCHING (VIW_VIE_ID, VIW_SPA_ID) ;"
        for space_id, widget_id in self._space_widget_mapping.items():
            db.query(self._core,stmnt,(self._id, int(space_id), int(widget_id)),commit=True)
            try:
                del(dbSpaceWidgetMap[int(space_id)])
            except KeyError: pass

        # delete Removed Widgets
        stmnt = "DELETE FROM VIEWWIDGETS WHERE VIW_VIE_ID = ? AND VIW_SPA_ID = ? ;"
        for space_id in dbSpaceWidgetMap.keys():
            db.query(self._core, stmnt, (self.get_id(), space_id), commit=True)

        # get current box_widget_mapping to determine which mappings to delete
        stmnt = "SELECT BWT_BOX_ID, BWT_WGT_ID FROM BOXWIDGETS WHERE BWT_VIE_ID = ? ;"
        cur = db.query(self._core, stmnt, (self.get_id(),))
        dbBoxMapping = {}
        for row in cur.fetchallmap():
            dbBoxMapping[(row["BWT_BOX_ID"],row["BWT_WGT_ID"])] = 1

        # insert new box-related entries and change existing ones
        stmnt = "UPDATE OR INSERT INTO BOXWIDGETS (BWT_BOX_ID, BWT_WGT_ID, BWT_ORDER, BWT_VIE_ID) \
                  VALUES (?,?,?,?) MATCHING (BWT_BOX_ID, BWT_VIE_ID, BWT_WGT_ID) ;"
        for box_id, boxcontent in self._box_mapping.items():
            order = 0
            for widget_id in boxcontent:
                db.query(self._core, stmnt, (box_id, widget_id, order, self.get_id()), commit=True)
                try:
                    del(dbBoxMapping[(int(box_id),int(widget_id))])
                except KeyError: pass
                order +=1

        # delete boxwidgets that are not used anymore
        stmnt = "DELETE FROM BOXWIDGETS WHERE BWT_BOX_ID = ? AND BWT_VIE_ID = ? AND BWT_VIE_ID = ? ;"
        for box_id, widget_id in dbBoxMapping.keys():
            db.query(self._core, stmnt, (box_id, widget_id, self.get_id()), commit=True)

        # get all widget-param-mappings to determine which have to been deleted
        stmnt = "SELECT VWP_WGT_ID, VWP_KEY FROM VIEWWIDGETPARAMS WHERE VWP_VIE_ID = ? ;"
        cur = db.query(self._core, stmnt, (self.get_id(),))
        dbWidgetParamMap = {}
        for row in cur.fetchallmap():
            dbWidgetParamMap[(row["VWP_WGT_ID"],row["VWP_KEY"])] = 1

        # insert new widget params and update existing ones
        stmnt = "UPDATE OR INSERT INTO VIEWWIDGETPARAMS (VWP_VIE_ID, VWP_WGT_ID, VWP_KEY, VWP_VALUE) \
                  VALUES (?,?,?,?) MATCHING (VWP_VIE_ID, VWP_WGT_ID) ;"
        for widget_id, propdict in self._widget_param_mapping.items():
            for key, value in propdict.items():
                db.query(self._core,stmnt,(self._id, int(widget_id), str(key), str(value)),commit=True)
                try:
                    del(dbWidgetParamMap[(widget_id,key)])
                except KeyError: pass

        # delete widget params that dont exist anymore
        stmnt = "DELETE FROM VIEWWIDGETPARAMS WHERE VPW_VIE_ID = ? AND VWP_WGT_ID = ? AND VWP_KEY = ? ;"
        for widget_id, key in dbWidgetParamMap.keys():
            db.query(self._core, stmnt, (self.get_id(), widget_id, key), commit=True)

        # update the view itself
        stmnt = "UPDATE OR INSERT INTO VIEWS (VIE_ID, VIE_SIT_ID, VIE_NAME, VIE_DEFAULT) \
                  VALUES (?,?,?,?) MATCHING (VIE_ID) ;"
        db.query(self._core, stmnt, (self._id, self._page, self._name, int(self._default)),commit=True)
        self._core.get_poke_manager().add_activity(ActivityType.VIEW)

    def delete(self):
        """
        deletes this view from the database
        """

        db = self._core.get_db()
        stmnt = "DELETE FROM VIEWWIDGETPARAMS WHERE VWP_VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)
        stmnt = "DELETE FROM VIEWWIDGETS WHERE VIW_VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)
        stmnt = "DELETE FROM BOXWIDGETS WHERE BWT_VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)
        stmnt = "UPDATE WIDGETS SET WGT_VIE_BASEVIEW = NULL, WGT_SPA_BASESPACE = NULL WHERE WGT_VIE_BASEVIEW = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)
        stmnt = "DELETE FROM VIEWS WHERE VIE_ID = ? ;"
        db.query(self._core, stmnt, (self._id,),commit=True)
        self._core.get_poke_manager().add_activity(ActivityType.VIEW)

class PureView(View):
    """
    Delivers some methods for Pure rendering
    """
    def generate_link_from_actionlist(self, actionlist):
        """
        returns a link that describes a call to a view that results of the actionlist
        """
        target = {}
        target['s'] = self.get_page()
        target['v'] = deepcopy(self.get_space_widget_mapping())
        target['b'] = deepcopy(self.get_box_mapping())
        target['c'] = deepcopy(self.get_widget_param_mapping())
        
        for action in actionlist.get_actions():
            if action.get_url() is not None:
                return action.get_url()
            elif action.get_view_id() is not None:
                view = actionlist._core.get_view_manager().get_from_id(action.get_view_id())
                name = view.get_name()
                return "/web/"+quote(name)
            elif action.get_space() is not None and action.get_widget_id() is not None:
                target['v'][action.get_space()] = action.get_widget_id()
                #delete any parameters of this widget. otherwise link will only
                #load current state of that widget again
                if target['c'].has_key(action.get_widget_id()):
                    del(target['c'][action.get_widget_id()])

        #AJAX-rendermode regarded here: ↓
        encoder = JSONEncoder()
        viewjsonstring = quote(encoder.encode(target))
        view_manager = self._core.get_view_manager()
        checkview = view_manager.get_from_json(viewjsonstring)
        existing_name = checkview.check_has_name()
        if existing_name == False:
            return "/web/?"+viewjsonstring
        else:
            return "/web/"+existing_name

    def render(self, environ):
        """
        renders this view with pure http-abilities. no script needed
        """
        View.set_currently_rendering_view(self)
        frame = """
        <!DOCTYPE html>
        <html>
          <head>
            <title>%(title)s</title>
            <link href="/static/%(page_css)s" rel="stylesheet" type="text/css">
            <link href="%(scv_css)s" rel="stylesheet" type="text/css">
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
        for space, widget_id in self._space_widget_mapping.items():
            space_name = space_name_map[space]
            widget = module_manager.get_widget(widget_id)

            args = {} 
            if self._widget_param_mapping.has_key(widget_id):
                args.update(self._widget_param_mapping[widget_id])
            elif self._widget_param_mapping.has_key(str(widget_id)):
                args.update(self._widget_param_mapping[str(widget_id)])
            
            if self._post_widget_id == widget_id:
                # Check whether the viewjson-string is included here, too:
                # if so, eliminate it.
                post_args = FieldStorage(fp=environ['wsgi.input'],environ=environ)
                for key in post_args.keys():
                    args[key] = post_args[key].value

            widget_html = widget.render_pure_html(args)
            body = re.sub(r"<%%\s?space:%s\s?%%>"%space_name,widget_html,body)

        for box, boxcontent in self._box_mapping.items():
            box_orientation, box_name = self.get_box_info(box)
            box_html = StringIO.StringIO()
            for widget_id in boxcontent:
                widget = module_manager.get_widget(widget_id)

                args = {} 
                if self._widget_param_mapping.has_key(widget_id):
                    args.update(self._widget_param_mapping[widget_id])
                elif self._widget_param_mapping.has_key(str(widget_id)):
                    args.update(self._widget_param_mapping[str(widget_id)])

                if self._post_widget_id == widget_id:
                    # Check whether the viewjson-string is included here, too:
                    # if so, eliminate it.
                    post_args = FieldStorage(fp=environ['wsgi.input'],environ=environ)
                    for key in post_args.keys():
                        args[key] = post_args[key].value
            
                widget_html = widget.render_pure_html(args)
                box_html.write(widget_html)
                if box_orientation == BoxOrientation.VERTICAL:
                    box_html.write("<br>")

            if box_orientation == BoxOrientation.HORIZONTAL:
                body = re.sub(r"<%%\s?hbox:%s\s?%%>"%box_name,box_html.getvalue(),body)
            elif box_orientation == BoxOrientation.VERTICAL:
                body = re.sub(r"<%%\s?vbox:%s\s?%%>"%box_name,box_html.getvalue(),body)

        body = re.sub(r"<%[^%>]+%>","",body) #Replace all unused spaces with emptystring

        css_manager = self._core.get_css_manager()
        css_url = css_manager.get_css_url()

        configuration = self._core.get_configuration()
        title = configuration.get_entry("core.name")

        page_css = page.get_css_filename()
        View.set_currently_rendering_view(None)
        return frame%{'title':title,
                      'scv_css':css_url,
                      'page_css':page_css,
                      'head':head,
                      'body':body}


class AJAXView(View):
    """
    Delivers some methods for AJAX rendering
    """
    def generate_link_from_actionlist(self, actionlist):
        """
        Generates an ajaxlink from an actionlist.
        ajaxlinks look like:
        javascript:SkdAjax.load_link([{'w':<widget_id>,'p':{params}}, ... ])

        the corresponding js on clientside should generate something like:
        /ajax/{'w':<widget_id>,'p':{params}}
        """
        link = "javascript:window.SkdAJAX.execute_action(%s);"
        linkjson = []
        for action in actionlist.get_actions():
            if action.get_url() is not None:
                return action.get_url()
            elif action.get_view_id() is not None:
                view = actionlist._core.get_view_manager().get_from_id(action.get_view_id())
                name = view.get_name()
                return "/web/"+quote(name)
            elif action.get_space() is not None and action.get_widget_id() is not None:
                page_manager = self._core.get_page_manager()
                page = page_manager.get_page(self.get_page())
                space_names = page.get_space_names()
                space_name = space_names[action.get_space()]
                linkjson.append({"w":action.get_widget_id(), "s":space_name, "p":{}})
        encoder = JSONEncoder()
        ajaxdata = encoder.encode(linkjson)
        ajaxdata = ajaxdata.replace('"',"'")
        return link%ajaxdata

    def render(self, environ):
        View.set_currently_rendering_view(self)
        frame = """
        <!DOCTYPE html>
        <html>
          <head>
            <title>%(title)s</title>
            <link href="/static/%(page_css)s" rel="stylesheet" type="text/css">
            <link href="%(scv_css)s" rel="stylesheet" type="text/css">
            %(head)s
            <script type="text/javascript">%(ajax_script)s</script>
          </head>
          <body>
            %(body)s
          </body>
        </html>
        """
        js_frame = """<script type="text/javascript" id="%d_scr">%s</script>"""
        page_manager = self._core.get_page_manager()
        page = page_manager.get_page(self._page) 

        head = page.get_html_head()
        body = page.get_html_body()

        module_manager = self._core.get_module_manager()
        # Find placeholders to substitute
        
        space_name_map = page.get_space_names()
        for space, widget_id in self._space_widget_mapping.items():
            space_name = space_name_map[space]
            widget = module_manager.get_widget(widget_id)

            args = {} 
            if self._widget_param_mapping.has_key(widget_id):
                args.update(self._widget_param_mapping[widget_id])
            elif self._widget_param_mapping.has_key(str(widget_id)):
                args.update(self._widget_param_mapping[str(widget_id)])
            
            if self._post_widget_id == widget_id:
                # Check whether the viewjson-string is included here, too:
                # if so, eliminate it.
                post_args = FieldStorage(fp=environ['wsgi.input'],environ=environ)
                for key in post_args.keys():
                    args[key] = post_args[key].value

            widget_html = widget.render_html(args)
            widget_js = widget.render_javascript(args)
            widget_html += js_frame%(widget.get_id(), widget_js)
            body = re.sub(r"<%%\s?space:%s\s?%%>"%space_name,widget_html,body)

        for box, boxcontent in self._box_mapping.items():
            box_orientation, box_name = self.get_box_info(box)
            box_html = StringIO.StringIO()
            for widget_id in boxcontent:
                widget = module_manager.get_widget(widget_id)

                args = {} 
                if self._widget_param_mapping.has_key(widget_id):
                    args.update(self._widget_param_mapping[widget_id])
                elif self._widget_param_mapping.has_key(str(widget_id)):
                    args.update(self._widget_param_mapping[str(widget_id)])

                if self._post_widget_id == widget_id:
                    # Check whether the viewjson-string is included here, too:
                    # if so, eliminate it.
                    post_args = FieldStorage(fp=environ['wsgi.input'],environ=environ)
                    for key in post_args.keys():
                        args[key] = post_args[key].value
            
                widget_html = widget.render_html(args)
                widget_js = widget.render_javascript(args)
                widget_html += js_frame%(widget.get_id(), widget_js)
                box_html.write(widget_html)
                if box_orientation == BoxOrientation.VERTICAL:
                    box_html.write("<br>")

            if box_orientation == BoxOrientation.HORIZONTAL:
                body = re.sub(r"<%%\s?hbox:%s\s?%%>"%box_name,box_html.getvalue(),body)
            elif box_orientation == BoxOrientation.VERTICAL:
                body = re.sub(r"<%%\s?vbox:%s\s?%%>"%box_name,box_html.getvalue(),body)

        body = re.sub(r"<%[^%>]+%>","",body) #Replace all unused spaces with emptystring

        css_manager = self._core.get_css_manager()
        css_url = css_manager.get_css_url()

        configuration = self._core.get_configuration()
        title = configuration.get_entry("core.name")

        page_css = page.get_css_filename()
        View.set_currently_rendering_view(None)
        return frame%{'title':title,
                      'scv_css':css_url,
                      'page_css':page_css,
                      'ajax_script':AJAXScript,
                      'head':head,
                      'body':body}

class ViewManager(object):
    def __init__(self, core):
        self._core = core

        View.set_core(core)
        self.get_viewlist = View.get_viewlist
        self.get_from_id = View.get_from_id
        self.get_from_name = View.get_from_name
        self.get_from_json = View.get_from_json
        self.get_default_view = View.get_default_view
        self.create_default_view = View.create_default_view
        self.get_currently_rendering_view = View.get_currently_rendering_view
        self.create = View.create
        self.delete_mappings_with_widget = View.delete_mappings_with_widget
        self.delete_mappings_with_module = View.delete_mappings_with_module


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
    def get_pages(cls):
        db = cls._core.get_db()
        stmnt = "SELECT SIT_ID FROM SITES ;"
        cur = db.query(cls._core, stmnt)
        res = cur.fetchallmap()
        ret = []
        for row in res:
            ret.append(cls.get_page(row["SIT_ID"]))
        return ret

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

        stmnt_space= "INSERT INTO SPACES (SPA_ID, SPA_SIT_ID, SPA_NAME ) VALUES (?,?,?) ; "
        stmnt_box = "INSERT INTO BOXES (BOX_ID, BOX_SIT_ID, BOX_NAME, BOX_ORIENTATION) VALUES (?,?,?,?) ;"

        for placeholder in placeholders:
            splitted = placeholder.split(":")
            typ = splitted[0]
            name = splitted[1]
            if typ == "space":
                new_space_id = db.get_seq_next("SPA_GEN")
                db.query(cls._core, stmnt_space, (new_space_id, new_sit_id, name), commit=True )
            elif typ == "vbox" or typ == "hbox":
                new_box_id = db.get_seq_next("BOX_GEN")
                orientation = int(typ == "vbox")
                db.query(cls._core, stmnt_box, (new_box_id, new_sit_id, name, orientation), commit=True)
        # only changes when template changes, so no activity


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

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_html_head(self):
        return self._html_head

    def get_html_body(self):
        return self._html_body

    def get_menus(self):
        """
        gets the menus that belong to this page from action_manager
        and returns them
        """
        action_manager = self._core.get_action_manager()
        return action_manager.get_menus_of_page(self)

    def get_space_names(self):
        db = self._core.get_db()
        stmnt = "SELECT SPA_ID, SPA_NAME FROM SPACES WHERE SPA_SIT_ID = ? ;"
        cur = db.query(self._core,stmnt,(self.get_id(),))
        ret = {}
        rows = cur.fetchallmap()
        for row in rows:
            ret[row["SPA_ID"]] = row["SPA_NAME"]
        return ret

    def get_box_info(self):
        db = self._core.get_db()
        stmnt = "SELECT BOX_ID, BOX_NAME, BOX_ORIENTATION FROM BOXES WHERE BOX_SIT_ID = ? ;"
        cur = db.query(self._core, stmnt, (self.get_id(),))
        ret = {}
        rows = cur.fetchallmap()
        for row in rows:
            ret[int(row["BOX_ID"])] = (row["BOX_NAME"], row["BOX_ORIENTATION"])
        return ret
    
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
        # only changes when template changes, so no activity
        
class PageManager(object):
    def __init__(self, core):
        self._core = core

        Page.set_core(core)
        self.get_page = Page.get_page
        self.get_pages = Page.get_pages
        self.create = Page.create
        self.delete_all_pages = Page.delete_all_pages
