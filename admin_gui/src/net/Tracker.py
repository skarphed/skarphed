#!/usr/bin/python
#-*- coding: utf-8 -*-

import threading
import gobject
import time

class Tracker(threading.Thread):
    activeProcesses = 0
    app = None
    def __init__(self,app=None):
        if app is not None:
            Tracker.app = app
        threading.Thread.__init__(self)
        
    def run(self):
        #lastState = None
        while True:
            #if Tracker.activeProcesses!=lastState:
            gobject.idle_add(Tracker.app.mainwin.pulseProgress,Tracker.activeProcesses)
            #lastState=Tracker.activeProcesses
            time.sleep(0.02)
            if Tracker.app.quitrequest:
                break
    def addProcess(self):
        Tracker.activeProcesses+=1
    
    def removeProcess(self):
        if Tracker.activeProcesses>=0:
            Tracker.activeProcesses-=1
            