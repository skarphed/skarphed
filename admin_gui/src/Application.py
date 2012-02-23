#!/usr/bin/python

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
        self.mainwin= gui.MainWindow(self)
        self.quitrequest = False
        self.tracker = net.Tracker.Tracker(self)
        self.tracker.start()
        self.state = self.STATE_LOGGEDOUT
        self.activeProfile=None
        self.instanceTypes = []
        
        from data import scoville
    
    def run(self):
        gui.run()
        
    def logout(self):
        if self.state == self.STATE_LOGGEDIN:
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

        