#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib2, cookielib
import threading
import time
import json
import gobject
from Tracker import Tracker

cookiejar = cookielib.LWPCookieJar()
cookiejar.load('cookies.txt')

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
urllib2.install_opener(opener)

class ScovilleRPC(threading.Thread):
    HEADERS = { 'Accept-Language':'en-us,en;q=0.5',        
                'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7', 
                'Content-Type':'application/json; charset=UTF-8',
                'Keep-Alive':'300', 
                'Pragma':'no-cache, no-cache',
                'Cache-Control':'no-cache, no-cache',
                'Connection':'Keep-Alive',
                'User-agent' : 'ScovilleAdmin'}
    
    def __init__(self,server,callback, method, params=[], errorcallback = None):
        threading.Thread.__init__(self)
        self.server = server
        self.callback = callback
        self.errorcallback = errorcallback
        #TODO: Server Muss online sein! Check!
        
        
        json_enc = json.JSONEncoder()
        
        url = str('http://'+server.getIp()+'/rpc/?nocache='+ str(int (time.time()*1000)))
        post = '{"service":"scoville_admin.scvRpc","method":"'+method+'","id":1,"params":'+json_enc.encode(params)+'}'
        
        self.request = urllib2.Request(url,post,self.HEADERS)

        Tracker().addProcess()
        
    def run(self):        
        json_dec = json.JSONDecoder()
        
        
        try:
            answer = urllib2.urlopen(self.request)
            plaintext = answer.read() #Line is obviously unnescessary, but a good debugging point :)
            result = json_dec.decode(plaintext)
        except urllib2.URLError:
            result = {'error':'HTTP-ERROR'}
    
        Tracker().removeProcess()
        if result.has_key('error'):
            if self.errorcallback is None:
                print result['error']
            else:
                gobject.idle_add(self.errorcallback,result)
        else:
            print result
            gobject.idle_add(self.callback,result['result'])
        
        
        
        
        