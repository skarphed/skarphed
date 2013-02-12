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
# class CSSException
# class CSSManager
# - public createCssPropertySetFromSerial
# - public getCssPropertySet()
# - public render()
# - public getCssFile()
# - public cleanUpCssSessionTable()
# class CSSPropertySet
# - public setModuleId()
# - public setWidgetId()
# - public setSessionId()
# - public setTypeGeneral()
# - public getType()
# - public getModuleId()
# - public getWidgetId()
# - public getSessionId()
# - public editValue()
# - public setAllInherited()
# - public getNonInherited()
# - public store()
# - public delete()
# - public render()
# - public serializeSet()
# - public buildSerialized()
# - public setFromParser()
# class CSSParser
# - public __construct()
# - public parseData()
# - private parse()
# - public getValue()
###########################################################

import re

class CSSException(Exception):
    ERRORS = {
        0:"""Get CSSPropertySet: This Widget does not exist"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "CSS_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class CSSManager(object):
    pass

class CSSPropertySet(object):
    ALL = -1
    @classmethod
    def create_csspropertyset_from_serial(cls, serial):
        """
        creates a propertyset from a serialized dataformat
        """
        css_property_set = CSSPropertySet()
        css_property_set.build_serialized(serial)
        return css_property_set

    @classmethod
    def get_csspropertyset(cls, module_id=None,widget_id=None,session_id=None,with_inherited=True):
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
    def render(filename):
        pass



class CSSParser(iter): #TODO find proper iter handling method in python (yield and stuff)
    pass