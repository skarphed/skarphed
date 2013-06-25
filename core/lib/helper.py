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

import re

def datetime2fdbTimestamp(datetime):
    y = str(datetime.year)
    if datetime.month < 10:
        m = "0"+str(datetime.month)
    else:
        m = str(datetime.month)
    if datetime.day < 10:
        d = "0"+str(datetime.day)
    else:
        d = str(datetime.day)
    if datetime.hour < 10:
        h = "0"+str(datetime.hour)
    else:
        h = str(datetime.hour)
    if datetime.minute < 10:
        mi = "0"+str(datetime.minute)
    else:
        mi = str(datetime.minute)
    if datetime.second < 10:
        s = "0"+str(datetime.second)
    else:
        s = str(datetime.second)

    return "%s-%s-%s %s:%s:%s"%(y,m,d,h,mi,s)

def fdbTimestamp2datetime(fdb_timestamp):
    pass

STRIP_SPACES = re.compile(r"\s+")
STRIP_THREE_LETTER_WORDS = re.compile(r"\w{3}\s")
def sluggify(s):
    """
    This method creates a slog from e.g. the title of a blogpost
    """
    s = s.strip()
    s = s.lower()

    #strip whitespace
    s = re.sub(STRIP_SPACES, " ", s)
    s = s.replace(" ","_")

    return s[:128]

