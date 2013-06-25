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

import os
import gobject
import json
import shutil
import tarfile

from glue.paths import INSTALLER
from data.skarphed.Skarphed import AbstractInstaller, AbstractDestroyer

from glue.lng import _

import logging

TARGETNAME = "Debian 6 / Apache2"
EXTRA_PARAMS = {
    'apache.domain':(_('Domain'),_('example.org or leave empty')),
    'apache.subdomain':(_('Subdomain'),_('sub.example.org or leave empty')),
    'apache.ip':(_('IP'),_('255.255.255.255 or *')),
    'apache.port':(_('Port'),_('80'))
}

class Installer(AbstractInstaller):
    def execute_installation(self):
        os.mkdir(self.BUILDPATH)

        p = os.path.dirname(os.path.realpath(__file__))

        apache_template = open(p+"/apache2.conf","r").read()
        apache_domain = ""
        if self.data['apache.domain'] != "":
            apache_domain = "ServerName "+self.data['apache.domain']
            self.domain = self.data['apache.domain']
        apache_subdomain = ""
        if self.data['apache.subdomain'] != "":
            apache_subdomain = "ServerAlias "+self.data['apache.subdomain']
        apacheconf = apache_template%(self.data['apache.ip'],
                                      self.data['apache.port'],
                                      apache_domain,
                                      apache_subdomain)
        apacheconfresult = open(self.BUILDPATH+"apache2.conf","w")
        apacheconfresult.write(apacheconf)
        apacheconfresult.close()

        self.status = 10
        gobject.idle_add(self.updated)


        scv_config = {}
        for key,val in self.data.items():
            if key.startswith("core.") or key.startswith("db."):
                if key == "db.name":
                    scv_config[key] = val+".fdb"
                    continue
                scv_config[key] = val

        scv_config_defaults = {
            "core.session_duration":2,
            "core.session_extend":1,
            "core.cookielaw":1,
            "core.debug":True
        }

        scv_config.update(scv_config_defaults)

        jenc = json.JSONEncoder()
        config_json = open(self.BUILDPATH+"config.json","w")
        config_json.write(jenc.encode(scv_config))
        config_json.close()

        shutil.copyfile(p+"/skarphed.conf",self.BUILDPATH+"skarphed.conf")
        shutil.copyfile(p+"/install.sh", self.BUILDPATH+"install.sh")

        self.status = 30
        gobject.idle_add(self.updated)

        shutil.copytree("../../core/web",self.BUILDPATH+"web")
        shutil.copytree("../../core/lib",self.BUILDPATH+"lib")
        #shutil.copytree("../../python-jsonrpc",self.BUILDPATH+"python-jsonrpc")

        tar = tarfile.open(self.BUILDPATH+"scv_install.tar.gz","w:gz")
        tar.add(self.BUILDPATH+"apache2.conf")
        tar.add(self.BUILDPATH+"config.json")
        tar.add(self.BUILDPATH+"skarphed.conf")
        tar.add(self.BUILDPATH+"install.sh")
        tar.add(self.BUILDPATH+"web")
        tar.add(self.BUILDPATH+"lib")
        #tar.add(self.BUILDPATH+"python-jsonrpc")
        tar.close()

        self.status = 45
        gobject.idle_add(self.updated)

        con = self.server.getSSH()
        con_stdin, con_stdout, con_stderr = con.exec_command("mkdir /tmp/scvinst"+str(self.installationId))

        self.status = 50
        gobject.idle_add(self.updated)


        con = self.server.getSSH()
        ftp = con.open_sftp()
        ftp.put(self.BUILDPATH+"scv_install.tar.gz","/tmp/scvinst"+str(self.installationId)+"/scv_install.tar.gz")
        ftp.close()

        self.status = 65
        gobject.idle_add(self.updated)


        con = self.server.getSSH()
        con_stdin, con_stdout, con_stderr = con.exec_command("cd /tmp/scvinst"+str(self.installationId)+"; tar xvfz scv_install.tar.gz -C / ; chmod 755 install.sh ; ./install.sh ")

        logging.debug(con_stdout.read())
        
        shutil.rmtree(self.BUILDPATH)
        self.status = 100
        gobject.idle_add(self.updated)
        gobject.idle_add(self.addInstanceToServer)

class Destroyer(AbstractDestroyer):
    def execute_destruction(self):
        p = os.path.dirname(os.path.realpath(__file__))

        server = self.instance.getServer()
        self.status = 10
        gobject.idle_add(self.updated)

        con = server.getSSH()
        ftp = con.open_sftp()
        ftp.put(p+"/teardown.sh","/tmp/teardown.sh")
        ftp.close()
        self.status = 30
        gobject.idle_add(self.updated)

        con = server.getSSH()
        con_stdin, con_stdout, con_stderr = con.exec_command("cd /tmp/ ; chmod 755 teardown.sh ; ./teardown.sh %d "%self.instanceid)
        logging.debug(con_stdout.read())
        self.status = 100
        gobject.idle_add(self.updated)

        gobject.idle_add(self.updated)
        gobject.idle_add(self.removeInstanceFromServer)
