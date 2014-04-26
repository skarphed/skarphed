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

from threading import Thread
from ctypes import c_long, py_object, pythonapi
from inspect import isclass
import gobject
import time

class UserKillThreadException(Exception):pass

class KillableThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    @classmethod
    def _kill_thread(cls, tid, exctype):
        '''Raises an exception in the threads with id tid'''
        if not isclass(exctype):
            raise TypeError("Need an Exception Class")
        res = pythonapi.PyThreadState_SetAsyncExc(c_long(tid),
                                                      py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # "if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"
            pythonapi.PyThreadState_SetAsyncExc(c_long(tid), None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def kill(self, exctype):
        Tracker().removeThread(self)
        KillableThread._kill_thread( self.ident, exctype )




class Tracker(Thread):
    activeThreads = []
    app = None
    def __init__(self,app=None):
        if app is not None:
            Tracker.app = app
        Thread.__init__(self)
        
    def run(self):
        while True:
            gobject.idle_add(Tracker.app.mainwin.pulseProgress,self)
            time.sleep(0.02)
            if Tracker.app.quitrequest:
                break

    def getThreads(self):
        return Tracker.activeThreads

    def addThread(self, thread):
        if thread not in Tracker.activeThreads:
            Tracker.activeThreads.append(thread)

    def removeThread(self, thread):
        if thread in Tracker.activeThreads:
            Tracker.activeThreads.remove(thread)

    def getThreadcount(self):
        return len(Tracker.activeThreads)
            