#!/usr/bin/python
#-*- coding: utf-8 -*-

import paramiko

class SSHConnection(paramiko.SSHClient):
    def __init__(self,server):
        paramiko.SSHClient.__init__(self)
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.connect(server.getIp(), 22, server.getSSHName(), server.getSSHPass())
        except paramiko.AuthenticationException:
            server.setSSHState(server.SSH_LOCKED)
            server.ssh_connection = self
        else:
            server.setSSHState(server.SSH_UNLOCKED)
            server.ssh_connection = None