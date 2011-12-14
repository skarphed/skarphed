#!/usr/bin/python
#-*- coding: utf-8 -*-

import pycurl
import StringIO
import time
import json

class ScovilleRPC(object):
    HEADERS = ['Accept-Language: en-us,en;q=0.5',
                    #'Accept-Encoding: gzip,deflate', 
                    'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7', 
                    'Content-Type: application/json; charset=UTF-8',
                    'Keep-Alive: 300', 
                    'Pragma: no-cache, no-cache',
                    'Cache-Control: no-cache, no-cache',
                    'Connection: Keep-Alive']
    USER_AGENT = 'ScovilleAdmin'    
    def __init__(self,server):
        self.server = server
        #TODO: Server Muss online sein! Check!
        
        self.curl = pycurlConnect = pycurl.Curl()
        
        LOGIN_URL = 'http://'+server.getIp()+'/rpc/?nocache='+ str(int (time.time()*1000))
        
        pycurlConnect = pycurl.Curl()
        pycurlConnect.setopt(pycurl.URL, LOGIN_URL)
        pycurlConnect.setopt(pycurl.HTTPHEADER, HEADERS)
        pycurlConnect.setopt(pycurl.COOKIEFILE, 'cookies.txt')
        
    def call(self, method, params=[], callback=None):
        assert method is not None and method!="", "method is not valid" 
        
        answer = StringIO.StringIO()
        
        POST_DATA = '{"service":"scoville_admin.scvRpc","method":"'+method+'","id":1,"params":'+json.JSONEncoder.encode(params)+'}'
        pycurlConnect.setopt(pycurl.POSTFIELDS, POST_DATA)
        pycurlConnect.setopt(pycurl.WRITEFUNCTION, dev_null.write)
        pycurlConnect.setopt(pycurl.POST, 1)
        pycurlConnect.perform()
        
        # Close connections
        print dev_null.getvalue()
        dev_null.close()
        pycurlConnect.close()
        
        
        