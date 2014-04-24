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

import urllib2
import time
import json
import gobject
from net import HTTPCookies, HTTPCall
from glue.threads import Tracker, KillableThread
from skarphedcommon.errors import getAppropriateException, UnknownCoreException
import logging

class SkarphedRPC(KillableThread, HTTPCall):    
    def __init__(self,skarphed,callback, method, handled_object, params=[], errorcallback = None):
        KillableThread.__init__(self)
        self.skarphed = skarphed
        self.callback = callback
        self.errorcallback = errorcallback
        self.handled_object = handled_object
        #TODO: skarphed Muss online sein! Check!
        
        json_enc = json.JSONEncoder()
        
        url = str(skarphed.getUrl()+'/rpc/?nocache='+ str(int (time.time()*1000)))
        post = '{"service":"skarphed_admin.scvRpc","method":"'+method+'","id":1,"params":'+json_enc.encode(params)+'}'
        
        self.request = urllib2.Request(url,post,self.HEADERS)

        Tracker().addThread(self)

    def rerun(self):
        """
        rerun workload of this thread after session refresh
        """
        self.skarphed.unsetRefreshSessionFlag()
        Tracker().addThread(self)
        self.run()
        
    def run(self):
        while self.skarphed.isRefreshingSession():
            time.sleep(0.01)

        try:
            answer = urllib2.urlopen(self.request)
            plaintext = answer.read() #Line is obviously unnescessary, but a good debugging point :)
            result = json.loads(plaintext)
        except urllib2.URLError:
            result = {'error':'HTTP-ERROR'}
    
        Tracker().removeThread(self)

        if result.has_key('error'):
            # Catch necessity for establishing a new session
            if result['error'].has_key('message') and result['error']['message'].startswith('SE_0'):
                self.skarphed.setRefreshSessionFlag()
                ses = SessionRefreshCall(self.skarphed, self.rerun)
                ses.start()
                return

            if self.errorcallback is None:
                logging.debug(result['error']['traceback'])
                exctyp = getAppropriateException(result['error']['class'])
                if exctyp is None:
                   exctyp = UnknownCoreException
                exc = exctyp(result['error']['message'])
                exc.set_tracebackstring(result['error']['traceback'])

                gobject.idle_add(self.skarphed.getApplication().raiseRPCException, exc) 
            else:
                gobject.idle_add(self.errorcallback,result)
        else:
            logging.debug(result)
            gobject.idle_add(self._callbackWrapper, self.callback, self.handled_object, result['result'])

    def _callbackWrapper(self, callback, handled_object, result):
        """
        Wraps the callback, so there will be no concurrent write-operatons
        on the COOKIEFILE
        """
        HTTPCookies.save()
        callback(handled_object, result)

class SessionRefreshCall(KillableThread, HTTPCall):
    """
    This thread is called to refresh a session with a skarphed instance,
    this occurs when said session expired
    """

    def __init__(self, skarphed, callback):
        KillableThread.__init__(self)
        self.skarphed = skarphed
        self.callback = callback

        params = [skarphed.getScvName(), skarphed.getScvPass()]

        url = str(skarphed.getUrl()+'/rpc/?nocache='+ str(int (time.time()*1000)))
        post = '{"service":"skarphed_admin.scvRpc","method":"authenticateUser","id":1,"params":'+json.dumps(params)+'}'
        
        self.request = urllib2.Request(url,post,self.HEADERS)

    def run(self):
        """
        refresh the coookie
        """
        HTTPCookies.clear(self.skarphed.getUrl(without_proto=True))

        try:
            answer = urllib2.urlopen(self.request)
            plaintext = answer.read() #Line is obviously unnescessary, but a good debugging point :)
            result = json.loads(plaintext)
        except urllib2.URLError:
            result = {'error':'HTTP-ERROR'}

        if result.has_key('error'):
            logging.debug('Could not reestablish session')
        else:
            gobject.idle_add(self._callbackWrapper, self.callback)

    def _callbackWrapper(self, callback):
        """
        Wraps the callback, so there will be no concurrent write-operatons
        on the COOKIEFILE
        """
        HTTPCookies.save()
        callback()
