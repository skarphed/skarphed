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

import urllib2, cookielib
import os

from skarphedadmin.glue.paths import COOKIEPATH

class HTTPCall(object):
    HEADERS = { 'Accept-Language':'en-us,en;q=0.5',        
                'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7', 
                'Content-Type':'application/json; charset=UTF-8',
                'Keep-Alive':'300', 
                'Pragma':'no-cache, no-cache',
                'Cache-Control':'no-cache, no-cache',
                'Connection':'Keep-Alive',
                'User-agent' : 'SkarphedAdmin'}

class HTTPCookies(object):
    @classmethod
    def initialize(cls):
        cls.cookiejar = cookielib.LWPCookieJar()

        if os.path.exists(COOKIEPATH):
            cls.cookiejar.load(COOKIEPATH)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cls.cookiejar))
        urllib2.install_opener(opener)

    @classmethod
    def save(cls):
        cls.cookiejar.save(COOKIEPATH, ignore_discard=True, ignore_expires=True)

    @classmethod
    def clear(cls, *args, **kwargs):
        cls.cookiejar.clear(*args, **kwargs)
        

HTTPCookies.initialize()
