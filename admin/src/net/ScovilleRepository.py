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

import urllib2, cookielib
import threading
import json
import gobject
from Tracker import Tracker
from MultiPartForm import MultiPartForm

cookiejar = cookielib.LWPCookieJar()
cookiejar.load('cookies.txt')

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
urllib2.install_opener(opener)

class ScovilleRepositoryException(Exception):pass

class ScovilleRepository(threading.Thread):
    TYPE_TEMPLATE = 0
    RESULT_OK    = 0
    RESULT_ERROR = 1
    
    COMMANDS = {1 : 'getAllModules',
                2 : 'getVersionsOfModule',
                3 : 'resolveDependenciesDownwards',
                4 : 'resolveDependenciesUpwards',
                5 : 'downloadModule',
                100 : 'authenticate',
                101 : 'logout',
                102 : 'changePassword',
                103 : 'registerDeveloper',
                104 : 'unregisterDeveloper',
                105 : 'uploadModule',
                106 : 'deleteModule',
                107 : 'getDevelopers'}
    
    HEADERS = { 'Accept-Language':'en-us,en;q=0.5',        
                'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7', 
                'Content-Type':'application/json; charset=UTF-8',
                'Keep-Alive':'300', 
                'Pragma':'no-cache, no-cache',
                'Cache-Control':'no-cache, no-cache',
                'Connection':'Keep-Alive',
                'User-agent' : 'ScovilleAdmin'}
    
    def __init__(self,repo, command, callback=None):
        threading.Thread.__init__(self)
        self.repo = repo
        self.callback=callback
        
        assert ScovilleRepository.COMMANDS.has_key(command['c'])
        
        url = str(repo.getUrl())
        
        json_enc = json.JSONEncoder()
        
        form = MultiPartForm()
        form.add_field('j',json_enc.encode(command))
        
        post = str(form)
        
        self.request = urllib2.Request(url)
        self.request.add_header('User-agent','ScovilleAdmin')
        self.request.add_header('Content-type',form.get_content_type())
        self.request.add_header('Body-length',len(post))
        self.request.add_data(post)
        
        Tracker().addProcess()
        
    def run(self):
        json_dec = json.JSONDecoder()
        
        answer = urllib2.urlopen(self.request)
        plaintext = answer.read()
        print plaintext
        result = json_dec.decode(plaintext)
    
        Tracker().removeProcess()
        if result.has_key('error'):
            raise ScovilleRepositoryException(result['error'])
        
        if self.callback is not None:
            gobject.idle_add(self.callback,result)