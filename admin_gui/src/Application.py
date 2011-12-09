#!/usr/bin/python

import gui
import data.Profile
import data.Server

class ApplicationException(Exception): pass

class Application:
    STATE_LOGGEDIN = 1
    STATE_LOGGEDOUT = 0
    
    def __init__(self):
        self.mainwin= gui.MainWindow(self)
        self.state = self.STATE_LOGGEDOUT
        self.activeProfile=None
    
    def run(self):
        gui.run()
    
    def logout(self):
        if self.state == self.STATE_LOGGEDIN:
            self.activeProfile.save()
            del(self.activeProfile)
            self.state = self.STATE_LOGGEDOUT
        else:
            raise ApplicationException("Already loggedout")
    
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
            
    ########################################
    #        EXPERIMENTELLER KREMPEL!
    ########################################
    def createTestserver(self):
        server = data.Server.Server()
        server.ip = "192.168.0.110"
        return server
        
application = Application()
application.run()

        