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


import paramiko
import threading
import gobject
from Tracker import Tracker

class SSHConnection(paramiko.SSHClient):
    def __init__(self,server):
        paramiko.SSHClient.__init__(self)
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.server = server
        
    def getServer(self):
        return self.server
    
class SSHConnector(threading.Thread):
    def __init__(self,server):
        threading.Thread.__init__(self)
        self.connection = SSHConnection(server)
        
    def run(self):
        Tracker().addProcess()
        server = self.connection.getServer()
        try:
            self.connection.connect(server.getIp(), 22, server.getSSHName(), server.getSSHPass())
        except paramiko.AuthenticationException:
            server.setSSHState(server.SSH_LOCKED)
            server.ssh_connection = None
        else:
            server.setSSHState(server.SSH_UNLOCKED)
            server.ssh_connection = self.connection
        Tracker().removeProcess()
        gobject.idle_add(server.updated)
