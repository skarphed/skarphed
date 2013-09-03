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

"""
This files accumulates all kind of enumerations throughout skarphed
"""

class Enum(object):
    """
    @classmethod
    def get_as_dict(cls):
        ret = {}
        for key, val in cls.__dict__:
            if type(val) == int:
                ret[key] = val
        return ret
    """

    @classmethod
    def is_valid_value(cls, valc):
        for key, val in cls.__dict__:
            if val == valc:
                return True
        return False


class JSMandatory(Enum):
    NO=0
    SUPPORTED=1
    MANDATORY=2

class BoxOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class ActivityType(Enum):
    TEMPLATE = 0
    MODULE = 1
    WIDGET = 2
