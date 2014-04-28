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


import skarphedadmin.data
from skarphedadmin.data.Profile import Profile
from skarphedadmin.glue.threads import Tracker
from skarphedadmin.net.SSH import SSHConnector
import os
import logging
from skarphedcommon.errors import getAppropriateException

from skarphedadmin.glue.autosave import AutoSaveThread

class ApplicationException(Exception): pass

class Application(object):
    STATE_LOGGEDIN = 1
    STATE_LOGGEDOUT = 0
 
    _borg_mind = {}
   
    def __init__(self):
        self.__dict__ = Application._borg_mind
        print self.__dict__
        if self.__dict__ == {}:
            # register instance-types
            self.instanceTypes = []
            from skarphedadmin.data.skarphed_repo import register as skarphed_repo_register
            skarphed_repo_register(self)
            from skarphedadmin.data.database import register as database_register
            database_register(self)
            from skarphedadmin.data.skarphed import register as skarphed_register
            skarphed_register(self)
            
            # set application reference
            os.environ['PYGTK_FATAL_EXCEPTIONS'] = '1'
            import skarphedadmin.data.Generic
            skarphedadmin.data.Generic.setApplicationReference(self)

            # register official repository
            from skarphedadmin.data.skarphed_repo.Skarphed_repo import OfficialRepo
            OfficialRepo()

            # start up gui
            from skarphedadmin.gui import MainWindow
            self.mainwin = MainWindow(self)
            self.quitrequest = False

            # start up process tracker
            self.tracker = Tracker(self)
            self.tracker.start()
            self.state = self.STATE_LOGGEDOUT
            self.activeProfile=None
            
            if not os.path.exists(os.path.expanduser('~/.skarphedadmin/')):
                os.mkdir(os.path.expanduser('~/.skarphedadmin/'))

            logging.basicConfig(filename=os.path.expanduser('~/.skarphedadmin/generic.log'),level=logging.DEBUG)
            AutoSaveThread(self).start()

            
            from data import skarphed
    
    def run(self):
        try:
            from skarphedadmin.gui import run as guirun
            guirun()
        except KeyboardInterrupt, e:
            self.mainwin.cb_Close()
        
    def logout(self):
        if self.state == self.STATE_LOGGEDIN:
            self.activeProfile.updateProfile()
            self.activeProfile.save()
            from skarphedadmin.data.Generic import Generic
            Generic.ObjectStore().clear()
            del(self.activeProfile)
            self.state = self.STATE_LOGGEDOUT
        else:
            raise ApplicationException("Already logged out")
    
    def doLoginTry(self,username,password):
        if self.state == self.STATE_LOGGEDOUT:
            profile = Profile(username,password)
            profile.load()
            self.state = self.STATE_LOGGEDIN
            self.activeProfile = profile
            
    def createProfile(self,username,password):
        if self.state == self.STATE_LOGGEDOUT:
            profile = Profile(username,password)
            profile.create()
            self.state = self.STATE_LOGGEDIN
            self.activeProfile = profile
    
    def setQuitRequest(self,val):
        self.quitrequest = val
    
    def raiseRPCException(self, exception):
        raise exception

    def getSSHConnection(self,server):
        SSHConnector(server).start()
    
    def getObjectStore(self):
        return skarphedadmin.data.getObjectStore()
    
    def getData(self):
        return skarphedadmin.data

    def getMainWindow(self):
        return self.mainwin
    
    def getLocalObjectById(self,obj_id):
        return self.getObjectStore().getLocalObjectById(obj_id)
    
    def registerInstanceType(self, instancetype):
        self.instanceTypes.append(instancetype)
        
    def getInstanceTypes(self):
        return self.instanceTypes
    
    def createServerFromInstanceUrl(self, instanceurl):
        return skarphedadmin.data.createServerFromInstanceUrl(instanceurl)

if __name__=="__main__":
    application = Application()
    application.run()

        
