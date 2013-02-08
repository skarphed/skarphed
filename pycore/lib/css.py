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
        1:"""Only the Configuration-class is authorized to access this variable"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "CSS_"+str(nr)+": "+cls.ERRORS[nr]+" "+info
