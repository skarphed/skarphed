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
            