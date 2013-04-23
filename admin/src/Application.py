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


import gui
import data.Generic
import data.Profile
import net.HTTPRpc
import net.Tracker
import net.SSH
import os

class ApplicationException(Exception): pass

class Application(object):
    STATE_LOGGEDIN = 1
    STATE_LOGGEDOUT = 0
    
    def __init__(self):
        os.environ['PYGTK_FATAL_EXCEPTIONS'] = '1'
        data.Generic.setApplicationReference(self)
        self.mainwin = gui.MainWindow(self)
        self.quitrequest = False
        self.tracker = net.Tracker.Tracker(self)
        self.tracker.start()
        self.state = self.STATE_LOGGEDOUT
        self.activeProfile=None
        self.instanceTypes = []
        
        from data import scoville
    
    def run(self):
        try:
            gui.run()
        except KeyboardInterrupt, e:
            self.mainwin.cb_Close()
        
    def logout(self):
        if self.state == self.STATE_LOGGEDIN:
            self.activeProfile.updateProfile()
            self.activeProfile.save()
            data.Generic.ObjectStore().clear()
            del(self.activeProfile)
            self.state = self.STATE_LOGGEDOUT
        else:
            raise ApplicationException("Already logged out")
    
    def doLoginTry(self,username,password):
        if self.state == self.STATE_LOGGEDOUT:
            profile = data.Profile.Profile(username,password)
            profile.load()
            self.state = self.STATE_LOGGEDIN
            self.activeProfile = profile
            
    def createProfile(self,username,password):
        if self.state == self.STATE_LOGGEDOUT:
            profile = data.Profile.Profile(username,password)
            profile.create()
            self.state = self.STATE_LOGGEDIN
            self.activeProfile = profile
    
    def setQuitRequest(self,val):
        self.quitrequest = val
    
    def doRPCCall(self, server, callback, method, params=[]):
        call = net.HTTPRpc.ScovilleRPC(server,callback, method, params)
        call.start()
    
    def getSSHConnection(self,server):
        net.SSH.SSHConnector(server).start()
    
    def getObjectStore(self):
        return data.getObjectStore()
    
    def getData(self):
        return data

    def getMainWindow(self):
        return self.mainwin
    
    def getLocalObjectById(self,obj_id):
        return self.getObjectStore().getLocalObjectById(obj_id)
    
    def registerInstanceType(self, instancetype):
        self.instanceTypes.append(instancetype)
        
    def getInstanceTypes(self):
        return self.instanceTypes
    
    def createServerFromInstanceUrl(self, instanceurl):
        return data.createServerFromInstanceUrl(instanceurl)
    
application = Application()
application.run()

        
