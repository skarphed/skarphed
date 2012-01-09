#!/usr/bin/python
#-*- coding: utf-8 -*-

import data.Generic
import data.Server

createServer = data.Server.createServer

def getObjectStore():
    return data.Generic.ObjectStore()