#!/usr/bin/python
#-*- coding: utf-8 -*-

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
            server.ssh_connection = self
        else:
            server.setSSHState(server.SSH_UNLOCKED)
            server.ssh_connection = None
        Tracker().removeProcess()
        gobject.idle_add(server.updated)
