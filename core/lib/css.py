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

from tinycss.css21 import CSS21Parser

class CSSException(Exception):
    ERRORS = {
        0:"""Get CSSPropertySet: This Widget does not exist""",
        1:"""Edit Value: The general propertyset does not have inherited values""",
        2:"""Invalid Propertyset: GENERAL type set must not have any Ids""",
        3:"""Invalid Propertyset: MODULE type set must not have any Ids but must have ModuleId""",
        4:"""Invalid Propertyset: WIDGET type set must not have any Ids but must have WidgetId""",
        5:"""Invalid Propertyset: SESSION type set must not have any Ids but must have Session""",
        6:"""Invalid Propertyset: Invalid type:"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "CSS_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class CSSManager(object):
    """
    Manages CssPropertySets
    """
    def __init__(self, core):
        self._core = core
        CSSPropertySet.set_core(core)

        self.create_csspropertyset_from_serial = CSSPropertySet.create_csspropertyset_from_serial
        self.create_csspropertyset_from_css = CSSPropertySet.create_csspropertyset_from_css
        self.create_csspropertyset_from_file = CSSPropertySet.create_csspropertyset_from_file
        self.get_csspropertyset = CSSPropertySet.get_csspropertyset
        self.render = CSSPropertySet.render
        self.get_css_file = CSSPropertySet.get_css_file
        self.get_css_url = CSSPropertySet.get_css_url
        self.cleanup_css_sessiontable = CSSPropertySet.cleanup_css_sessiontable


class CSSPropertySet(object):
    ALL = -1

    GENERAL = 0
    MODULE = 1
    WIDGET = 2
    SESSION = 3

    SPLIT="?"

    @classmethod
    def set_core(cls,core):
        """
        trivial
        """
        cls._core=core

    @classmethod
    def create_csspropertyset_from_serial(cls, serial):
        """
        creates a propertyset from a serialized dataformat
        """
        css_property_set = CSSPropertySet(cls._core)
        css_property_set.build_serialized(serial)
        return css_property_set

    @classmethod
    def create_csspropertyset_from_css(cls, css):
        """
        creates a csspropertyset from css-code
        """
        parser = CSS21Parser()
        stylesheet = None
        try:
            stylesheet = parser.parse_stylesheet_bytes(css)
        except Exception,e :
            raise e # implement correct error handling
        propertyset = CSSPropertySet(cls._core)
        for rule in stylesheet.rules:
            selector = ",".join([s.as_css() for s in rule.selector])
            for declaration in rule.declarations:
                values = [val.value for val in declaration.value]
                propertyset.edit_value(selector, declaration.name, ",".join(values))
        return propertyset


    @classmethod
    def create_csspropertyset_from_file(cls, filename):
        """
        creates a CSSPropertySet off the css contained in the file
        """
        f = open(filename)
        data = f.read()
        f.close()
        return self.create_csspropertyset_from_css(data)

    @classmethod
    def get_csspropertyset(cls, module_id=None,widget_id=None,session_id=None,with_inherited=True):
        """
        loads a csspropertyset from the database
        """
        db = cls._core.get_db()
        if module_id is not None:
            if module_id != CSSPropertySet.ALL:
                ret = {}
                stmnt = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME, MOD_ID \
                                 FROM CSS \
                                   INNER JOIN MODULES ON (CSS_MOD_ID = MOD_ID) \
                                 WHERE CSS_MOD_ID IS NOT NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL ;"
                cur = db.query(cls._core,stmnt)
                rows = cur.fetchmapall()
                for row in rows:
                    if not ret.has_key(row["MOD_ID"]):
                        ret[row["MOD_ID"]] = CSSPropertySet()
                        ret[row["MOD_ID"]].set_module_id(row["MOD_ID"])
                    ret[row["MOD_ID"]].edit_value(row["CSS_SELECTOR"], row["CSS_TAG"], row["CSS_VALUE"])
                return ret
            else:
                if with_inherited:
                    propertyset = cls.get_csspropertyset()
                    propertyset.set_all_inherited()
                else:
                    propertyset = CSSPropertySet()
                propertyset.set_module_id(module_id)
                stmnt = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME \
                             FROM CSS \
                               INNER JOIN MODULES ON (CSS_MOD_ID = MOD_ID) \
                             WHERE CSS_MOD_ID IS NOT NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL AND CSS_MOD_ID = ? ;";
                cur = db.query(cls._core,stmnt,(module_id,))
                rows = cur.fetchmapall()
                for row in rows:
                    propertyset.edit_value(row["CSS_SELECTOR"],row["CSS_TAG"], row["CSS_VALUE"])
                return propertyset
        if widget_id is not None:
            if widget_id == CSSPropertySet.ALL:
                ret = {}
                stmnt = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME, MOD_ID, WGT_NAME, WGT_ID \
                         FROM CSS \
                           INNER JOIN WIDGETS ON (CSS_WGT_ID = WGT_ID) \
                           INNER JOIN MODULES ON (WGT_MOD_ID = MOD_ID) \
                         WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NOT NULL AND CSS_SESSION IS NULL ;"
                cur = db.query(cls._core,stmnt)
                rows = cur.fetchmapall()
                for row in rows:
                    if not ret.has_key(row["WGT_ID"]):
                        ret[row["WGT_ID"]] = CSSPropertySet()
                        ret[row["WGT_ID"]].set_widget_id(row["WGT_ID"])
                    ret[row["WGT_ID"]].edit_value(row["CSS_SELECTOR"],row["CSS_TAG"],row["CSS_VALUE"])
                return ret
            else:
                if with_inherited:
                    stmnt = "SELECT WGT_MOD_ID FROM WIDGETS WHERE WGT_ID = ? ; "
                    cur = db.query(cls._core,stmnt,(widget_id,))
                    row = cur.fetchone()
                    if row:
                        propertyset = cls.get_csspropertyset(module_id = row[0])
                        propertyset.set_all_inherited()
                    else:
                        raise CSSException(CSSException.get_msg(0))
                else:
                    propertyset = CSSPropertySet()
                propertyset.set_widget_id(widget_id)
                stmnt = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME, WGT_NAME \
                             FROM CSS \
                               INNER JOIN WIDGETS ON (CSS_WGT_ID = WGT_ID) \
                               INNER JOIN MODULES ON (WGT_MOD_ID = MOD_ID) \
                             WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NOT NULL AND CSS_SESSION IS NULL AND CSS_WGT_ID = ? ;"
                cur = db.query(cls._core,stmnt,(widget_id,))
                rows = cur.fetchmapall()
                for row in rows:
                    propertyset.edit_value(row["CSS_SELECTOR"], row["CSS_TAG"], row["CSS_VALUE"])
                return propertyset
        if session_id is not None:
            return None
            #TODO: Implement

        #Standard CSS Propertyset
        propertyset = CSSPropertySet()
        propertyset.set_type_general()
        stmnt = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL ;"
        cur = db.query(cls._core,stmnt)
        rows = cur.fetchmapall()
        for row in rows:
            propertyset.edit_value(row["CSS_SELECTOR"], row["CSS_TAG"], row["CSS_VALUE"])
        return propertyset

    @classmethod
    def render(cls, filename):
        """
        renders a css file
        """
        css = ""
        session_id = None
        current_session = cls._core.get_session_manager().get_current_session()
        if current_session is None:
            generic_set = cls.get_csspropertyset()
            module_sets = cls.get_csspropertyset(cls.ALL,None,None)
            widget_sets = cls.get_csspropertyset(None,cls.ALL,None)

            css+= generic_set.render()
            for module_set in module_sets:
                css+= module_set.render()
            for widget_set in widget_sets:
                css+= widget_set.render()

            cssfile = open(filename,"w")
            cssfile.write(css)
            cssfile.close()

        else:
            #TODO: Implement behaviour with session
            generic_set = cls.get_csspropertyset()
            module_sets = cls.get_csspropertyset(cls.ALL,None,None)
            widget_sets = cls.get_csspropertyset(None,cls.ALL,None)

            css+= generic_set.render()
            for module_set in module_sets:
                css+= module_set.render()
            for widget_set in widget_sets:
                css+= widget_set.render()

            cssfile = open(filename,"w")
            cssfile.write(css)
            cssfile.close()

    @classmethod
    def get_css_file(cls):
        """
        Gets the name of the cssFile for the current user
        """
        configuration = cls._core.get_configuration()
        css_folder = "%s%s%s/"%(configuration.get_entry("global.webpath"),
                                configuration.get_entry("core.instance_id"),
                                configuration.get_entry("core.css_folder"))
        
        db = cls._core.get_db()
        current_session = cls._core.get_session_manager().get_current_session()
        if current_session is not None:
            stmnt = "SELECT CSE_FILE FROM CSSSESSION WHERE CSE_SES_ID = ? AND CSE_OUTDATED = 0 ;"
            cur = db.query(cls._core,stmnt,(current_session.get_id(),))
            row = cur.fetchonemap()
            if row is not None:
                filename= row["CSE_FILE"]
            else:
                filename= css_folder+current_session.get_id()+".css"
                stmnt = "INSERT INTO CSSSESSION (CSE_SES_ID,CSE_FILE,CSE_OUTDATED) VALUES (?,?,0) ;"
                db.query(cls._core,stmnt,(current_session.get_id(),filename),commit=True)
        else:
            stmnt = "SELECT CSE_FILE FROM CSSSESSION WHERE CSE_SES_ID = 'GENERAL' AND CSE_OUTDATED = 0 ;"
            cur = db.query(cls._core,stmnt,(current_session.get_id(),))
            row = cur.fetchonemap()
            if row is not None:
                filename= row["CSE_FILE"]
            else:
                filename= css_folder+"general.css"
                stmnt = "INSERT INTO CSSSESSION (CSE_SES_ID,CSE_FILE,CSE_OUTDATED) VALUES ('GENERAL',?,0) ;"
                db.query(cls._core,stmnt,(filename,),commit=True)

        if not os.path.exists(filename):
            cls.render(filename)

        cls.cleanup_css_sessiontable()
        return filename

    @classmethod
    def get_css_url(cls):
        """
        Gets the cssFile as URL for the current user
        """
        configuration = cls._core.get_configuration()
        filename = filename.replace(configuration.get_entry("global.webpath"),"",1)
        filename = filename.replace(configuration.get_entry("core.instance_id"),"",1)
        filename = filename.replace(configuration.get_entry("/"),"",1)
        return filename

    @classmethod
    def cleanup_css_sessiontable(cls):
        """
        Cleans up old css filenames
        """
        db = cls._core.get_db()
        stmnt = "DELETE FROM CSSSESSION WHERE CSE_OUTDATED = 1 ;"
        db.query(cls._core,stmnt,commit=True)
        return


    def __init__(self, core):
        """
        initializes a css propertyset
        """
        self._core = core

        self._properties = {}

        self._typ = None
        self._module_id = None
        self._widget_id = None
        self._session = None

    def set_module_id(self,module_id):
        """
        sets this propertyset's type to "module" and sets the module_id
        """
        self._module_id = int(module_id)
        self._session = None
        self._widget_id = None
        self._typ = CSSPropertySet.MODULE

    def set_widget_id(self,widget_id):
        """
        sets this propertyset's type to "widget" and sets the widget_id
        """
        self._module_id = None
        self._session = None
        self._widget_id = int(widget_id)
        self._typ = CSSPropertySet.WIDGET

    def set_session_id(self,session_id):
        """
        sets this propertyset's type to "session" and sets the session_id
        """
        self._module_id = None
        self._session = str(session_id)
        self._widget_id = None
        self._typ = CSSPropertySet.SESSION        

    def set_type_general(self):
        """
        sets this css propertyset as GENERAL
        """
        self._module_id = None
        self._session = None
        self._widget_id = None
        self._typ = CSSPropertySet.GENERAL

    def get_type(self):
        """
        returns this cssPropertySet's type
        """        
        return self._typ

    def get_module_id(self):
        """
        returns this cssPropertySet's module_id
        """
        return self._module_id

    def get_widget_id(self):
        """
        returns this cssPropertySet's widget_id
        """
        return self._widget_id

    def get_session_id(self):
        """
        returns this cssPropertySet's session_id
        """
        return self._session

    def edit_value(self, selector, tag, value, inherited=False):
        """
        edits a value determined by selector and tag in this csspropertyset
        """
        if self.get_type() == CSSPropertySet.GENERAL and inherited:
            raise CSSException(CSSException.get_msg(1))
        self._properties[selector+CSSPropertySet.SPLIT+tag] = {'v':value,'i':False}

    def get_value(self,selector,tag):
        """
        Returns a value determined by selector and tag
        """
        if self._properties.has_key(selector+CSSPropertySet.SPLIT+tag):
            return self._properties[selector+CSSPropertySet.SPLIT+tag]
        else:
            return None

    def set_all_inherited(self):
        """
        Sets all 'inherited' flags in this csspropertySet to "True"
        """
        for key in self._properties.keys():
            self._properties[key]['i'] = True

    def get_non_inherited(self):
        """
        gets all properties that are not inherited from another cssPropertySet
        """
        ret = {}
        for key, value in self._properties.items():
            if value['i']:
                ret[key] = value
        return ret

    def store(self):
        """
        stores this cssPropertySet into the database
        """
        db = self._core.get_db()
        current_session = self._core.get_session_manager().get_current_session()


        self.delete()

        values_to_store = self.get_non_inherited()
        stmnt = "UPDATE OR INSERT INTO CSS (CSS_SELECTOR, CSS_TAG, CSS_VALUE, CSS_MOD_ID, CSS_WGT_ID, CSS_SESSION) \
                   VALUES ( ?,?,?,?,?,?) MATCHING (CSS_SELECTOR,CSS_TAG,CSS_MOD_ID,CSS_WGT_ID, CSS_SESSION) ;"
        for key, value in values_to_store.items():
            selector, tag = key.split(CSSPropertySet.SPLIT)
            db.query(self._core,stmnt,(selector,tag,value['v'],self.get_module_id(),self.get_widget_id(),self.get_session_id()),commit=True)

        if self._typ == CSSPropertySet.SESSION and current_session is not None:
            stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1 WHERE CSE_SES_ID = ? ;"
            db.query(self._core,stmnt,(current_session.get_id()),commit=True)
        else:
            stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1;"
            db.query(self._core,stmnt,commit=True)

    def delete(self):
        """
        deletes this csspropertyset from the database
        """
        db = self._core.get_db()
        current_session = self._core.get_session_manager().get_current_session()

        if self._typ == CSSPropertySet.GENERAL:
            stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SES_ID IS NULL;";
            db.query(self._core,stmnt,commit=True)
        elif self._typ == CSSPropertySet.MODULE:
            stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID = ? AND CSS_WGT_ID IS NULL AND CSS_SES_ID IS NULL;";
            db.query(self._core,stmnt,(self.get_module_id(),),commit=True)
        elif self._typ == CSSPropertySet.WIDGET:
            stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID = ? AND CSS_SES_ID IS NULL;";
            db.query(self._core,stmnt,(self.get_widget_id(),),commit=True)
        elif self._typ == CSSPropertySet.SESSION:
            stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SES_ID = ? ;"
            db.query(self._core,stmnt,(self.get_session_id(),),commit=True)

        if self._typ == CSSPropertySet.SESSION:
            if current_session is not None:
                stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1 WHERE CSE_SES_ID = ? ;";
                db.query(self._core,stmnt,(current_session.get_id(),),commit=True)
        else:
            stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1 ;"
            db.query(self._core,stmnt,commit=True)

    def render(self):
        """
        renders a CSS propertyset
        """
        module_manager = self._core.get_module_manager()
        css = ""
        if self._typ == CSSPropertySet.GENERAL:
            selectorlist = {}
            for key, value in self.get_non_inherited().items():
                splitselector = key.split(CSSPropertySet.SPLIT)
                if len(splitselector) == 1:
                    splitselector.insert(0,"")
                selector, tag = splitselector
                if not selectorlist.has_key(selector):
                    selectorlist[selector] = []
                selectorlist[selector].append({'t':tag,'v':value['v']})

            for selector, values in selectorlist.items():
                css += selector+"{\n"
                for value in values:
                    css += value['t']+":"+value['v']+";\n"
                css += "}\n\n"
        
        elif self.typ == CSSPropertySet.MODULE:
            selectorlist = {}
            module_name = module_manager.get_module(self._module_id).get_name()
            # TODO: Assert That modulenames do not contain dots
            for key, value in self.get_non_inherited().items():
                splitselector = key.split(CSSPropertySet.SPLT)
                if len(splitselector) == 1:
                    splitselector.insert(0,"")
                selector, tag = splitselector
                if not selectorlist.has_key(selector):
                    selectorlist[selector] = []
                selectorlist[selector].append({'t':tag,'v':value['v']})

            for selector, values in selectorlist.items():
                css += "."+module_name+" "+selector+" {\n"
                for value in values:
                    css += value['t']+":"+value['v']+";\n"
                css += "}\n\n";

        elif self.typ == CSSPropertySet.WIDGET:
            selectorlist = {}

            for key, value in self.get_non_inherited().items():
                splitselector = key.split(CSSPropertySet.SPLT)
                if len(splitselector) == 1:
                    splitselector.insert(0,"")
                selector, tag = splitselector
                if not selectorlist.has_key(selector):
                    selectorlist[selector] = []
                selectorlist[selector].append({'t':tag,'v':value['v']})

            for selector, values in selectorlist.items():
                css += ".w"+self.get_widget_id()+" "+selector+" {\n"
                for value in values:
                    css += value['t']+":"+value['v']+";\n"
                css += "}\n\n";

        elif self.typ == CSSPropertySet.SESSION:
            pass #TODO Implement sessiondependent behaviour

    def serialize_set(self):
        """
        returns a serialized version of this set
        """
        ret = {}
        ret['type'] = self._typ
        ret['moduleId'] = self._module_id
        ret['widgetId'] = self._widget_id
        ret['session'] = self._session
        propcopy = {}
        for key, value in self._properties.items():
            propcopy[key] = value
        ret['properties'] = propcopy
        return ret

    def build_serialized(self,buildset):
        """
        Checks whether the serialized data is valid. If yes, builds this CssPropertySet from the data
        """

        if buildset['type'] == CSSPropertySet.GENERAL:
            if buildset['moduleId'] is not None or buildset['widgetId'] is not None or buildset['session'] is not None:
                raise CSSException(CSSException.get_msg(2))
        elif buildset['type'] == CSSPropertySet.MODULE:
            if buildset['moduleId'] is None or buildset['widgetId'] is not None or buildset['session'] is not None:
                raise CSSException(CSSException.get_msg(3))
        elif buildset['type'] == CSSPropertySet.WIDGET:
            if buildset['moduleId'] is not None or buildset['widgetId'] is None or buildset['session'] is not None:
                raise CSSException(CSSException.get_msg(4))
        elif buildset['type'] == CSSPropertySet.SESSION:
            if buildset['moduleId'] is not None or buildset['widgetId'] is not None or buildset['session'] is None:
                raise CSSException(CSSException.get_msg(5))
        else:
            raise CSSException(CSSException.get_msg(6,buildset['type']))

        self._module_id = buildset['moduleId']
        self._widget_id = buildset['widgetId']
        self._session = buildset['session']
        self._typ = buildset['type']
        self._properties = {}
        self._properties.update(buildset['properties'])

    
