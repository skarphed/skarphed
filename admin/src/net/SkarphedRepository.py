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

import os

import urllib2, cookielib
import json
import gobject
from glue.threads import Tracker, KillableThread
from MultiPartForm import MultiPartForm
import logging

COOKIEPATH = os.path.expanduser('~/.skarphedadmin/cookies.txt')
cookiejar = cookielib.LWPCookieJar()

if os.path.exists(COOKIEPATH):
    cookiejar.load(COOKIEPATH)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
urllib2.install_opener(opener)

class SkarphedRepositoryException(Exception):
    SIMPLE_ERRORS = {
        2: "Authentication Failed. You are no Administrator",
        3: "Could not upload Module: manifest.json is broken",
        4: "Could not add Developer: Not a valid Public Key",
        5: "Could not add Developer: Developer already exists (nickname must be unique)",
        6: "Could not upload Module: Developername must be modulename-prefix (e.g. developer_module)",
        7: "Request Error: Erroneous Request-JSON received",
        8: "Database Error: A SQL-Statement failed in Execution"
    }
    def __init__(self, error):
        Exception.__init__(self)

        errorcode = error["c"]

        if SkarphedRepositoryException.SIMPLE_ERRORS.has_key(errorcode):
            self.message = SkarphedRepositoryException.SIMPLE_ERRORS[errorcode]
        elif errorcode == 9: #DEPENDENCY OF MODULE COULDNT BE RESOLVED
            dependencystring = ""
            for dependency in error['args']:
                dependencystring = "<br>%s (%s.%s)"%(dependency["name"], 
                                                     dependency["version_major"], 
                                                     dependency["version_minor"])
            self.message = "The following dependencies are given by the Module but couldn't be found on the server:<br>%s"%dependencystring
        elif errorcode == 1: # UNEXCPECTED EXCEPTION
            pass # TODO : raise generic exception with traceback here
        elif errorcode == 0:
            self.message = "OK"
        else:
            self.message = "Unknown RepositoryError: %d"%errorcode


class SkarphedRepository(KillableThread):
    TYPE_TEMPLATE = 0
    RESULT_OK    = 0
    RESULT_ERROR = 1
    
    COMMANDS = {1 : 'getAllModules',
                2 : 'getVersionsOfModule',
                3 : 'resolveDependenciesDownwards',
                4 : 'resolveDependenciesUpwards',
                5 : 'downloadModule',
                6 : 'getPublicKey',
                7 : 'getLatestVersion',
                8 : 'getAllTemplates',
                9 : 'downloadTemplate',
                100 : 'authenticate',
                101 : 'logout',
                102 : 'changePassword',
                103 : 'registerDeveloper',
                104 : 'unregisterDeveloper',
                105 : 'uploadModule',
                106 : 'deleteModule',
                107 : 'getDevelopers',
                108 : 'uploadTemplate',
                109 : 'deleteTemplate'}

    HEADERS = { 'Accept-Language':'en-us,en;q=0.5',
                'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Content-Type':'application/json; charset=UTF-8',
                'Keep-Alive':'300',
                'Pragma':'no-cache, no-cache',
                'Cache-Control':'no-cache, no-cache',
                'Connection':'Keep-Alive',
                'User-agent' : 'SkarphedAdmin'}
    
    def __init__(self,repo, command, callback=None):
        KillableThread.__init__(self)
        self.repo = repo
        self.callback=callback
        global cookiejar
        self.cookiejar = cookiejar
        
        assert SkarphedRepository.COMMANDS.has_key(command['c'])
        
        url = str(repo.getUrl())
        
        json_enc = json.JSONEncoder()
        
        form = MultiPartForm()
        form.add_field('j',json_enc.encode(command))
        
        post = str(form)
        
        self.request = urllib2.Request(url)
        self.request.add_header('User-agent','SkarphedAdmin')
        self.request.add_header('Content-type',form.get_content_type())
        self.request.add_header('Body-length',len(post))
        self.request.add_data(post)
        
        Tracker().addThread(self)

    def run(self):
        json_dec = json.JSONDecoder()
        
        answer = urllib2.urlopen(self.request)
        plaintext = answer.read()
        logging.debug(plaintext)
        result = json_dec.decode(plaintext)
    
        Tracker().removeThread(self)
        if result.has_key('error'):
            raise SkarphedRepositoryException(result['error'])
        

        if self.callback is not None:
            gobject.idle_add(self._callbackWrapper, self.callback,result)

    def _callbackWrapper(self, callback, result):
        """
        Wraps the callback, so there will be no concurrent write-operatons
        on the COOKIEFILE
        """
        self.cookiejar.save(COOKIEPATH, ignore_discard=True, ignore_expires=True)
        callback(result)
