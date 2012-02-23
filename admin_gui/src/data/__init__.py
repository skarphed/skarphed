#!/usr/bin/python
#-*- coding: utf-8 -*-

import Generic
import Server 

createServer = Server.createServer
createServerFromInstanceUrl = Server.createServerFromInstanceUrl

def getObjectStore():
    return Generic.ObjectStore()