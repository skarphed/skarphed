#!/usr/bin/python
#-*- coding: utf-8 -*-

import paramiko

class SSHConnection(paramiko.SSHClient):
    def __init__(self,server):
        paramiko.SSHClient.__init__(self)
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect(server.getIp(), 22, server.getSSHUser(), server.getSSHPass())
        