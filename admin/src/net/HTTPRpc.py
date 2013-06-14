#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import os
import urllib2, cookielib
import time
import json
import gobject
from glue.threads import Tracker, KillableThread
from common.errors import getAppropriateException, UnknownCoreException
import logging

COOKIEPATH = os.path.expanduser('~/.skarphedadmin/cookies.txt')
cookiejar = cookielib.LWPCookieJar()

if os.path.exists(COOKIEPATH):
    cookiejar.load(COOKIEPATH)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
urllib2.install_opener(opener)

class SkarphedRPC(KillableThread):
    HEADERS = { 'Accept-Language':'en-us,en;q=0.5',        
                'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7', 
                'Content-Type':'application/json; charset=UTF-8',
                'Keep-Alive':'300', 
                'Pragma':'no-cache, no-cache',
                'Cache-Control':'no-cache, no-cache',
                'Connection':'Keep-Alive',
                'User-agent' : 'SkarphedAdmin'}
    
    def __init__(self,server,callback, method, params=[], errorcallback = None):
        KillableThread.__init__(self)
        self.server = server
        self.callback = callback
        self.errorcallback = errorcallback
        global cookiejar
        self.cookiejar = cookiejar
        #TODO: Server Muss online sein! Check!
        
        json_enc = json.JSONEncoder()
        
        url = str(server.getUrl()+'/rpc/?nocache='+ str(int (time.time()*1000)))
        post = '{"service":"skarphed_admin.scvRpc","method":"'+method+'","id":1,"params":'+json_enc.encode(params)+'}'
        
        self.request = urllib2.Request(url,post,self.HEADERS)

        Tracker().addThread(self)
        
    def run(self):        
        json_dec = json.JSONDecoder()
        
        try:
            answer = urllib2.urlopen(self.request)
            plaintext = answer.read() #Line is obviously unnescessary, but a good debugging point :)
            result = json_dec.decode(plaintext)
        except urllib2.URLError:
            result = {'error':'HTTP-ERROR'}
    
        Tracker().removeThread(self)

        if result.has_key('error'):
            if self.errorcallback is None:
                logging.debug(result['error']['traceback'])
                exctyp = getAppropriateException(result['error']['class'])
                if exctyp is None:
                   exctyp = UnknownCoreException
                exc = exctyp(result['error']['message'])
                exc.set_tracebackstring(result['error']['traceback'])
                gobject.idle_add(self.server.getApplication().raiseRPCException, exc) 
            else:
                gobject.idle_add(self.errorcallback,result)
        else:
            logging.debug(result)
            gobject.idle_add(self._callbackWrapper, self.callback,result['result'])

    def _callbackWrapper(self, callback, result):
        """
        Wraps the callback, so there will be no concurrent write-operatons
        on the COOKIEFILE
        """
        self.cookiejar.save(COOKIEPATH, ignore_discard=True, ignore_expires=True)
        callback(result)
