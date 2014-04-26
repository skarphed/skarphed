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
from glue.paths import COREFILES

import logging

TARGETNAME = "Debian 7 / nginx"
EXTRA_PARAMS = {
    'nginx.domain':(_('Domain'),_('example.org or leave empty')),
    'nginx.subdomain':(_('Subdomain'),_('sub.example.org or leave empty')),
    'nginx.port':(_('Port'),_('80'))
}

class Installer(AbstractInstaller):
    def execute_installation(self):
        os.mkdir(self.BUILDPATH)

        p = os.path.dirname(os.path.realpath(__file__))

        nginx_template = open(os.path.join(p,"nginx.conf"),"r").read()
        nginx_domain = ""
        domainlineterm = ""
        if self.data['nginx.port'] == "":
            self.data['nginx.port'] = "80"
        if self.data['nginx.domain'] != "":
            nginx_domain = "server_name "+self.data['nginx.domain']
            self.domain = self.data['nginx.domain']
            domainlineterm = ";"
        nginx_subdomain = ""
        if self.data['nginx.subdomain'] != "":
            nginx_subdomain = "alias "+self.data['nginx.subdomain']
            domainlineterm = ";"
        nginxconf = nginx_template%{'port':self.data['nginx.port'],
                                    'domain':nginx_domain,
                                    'subdomain':nginx_subdomain,
                                    'domainlineterm':domainlineterm}
        nginxconfresult = open(os.path.join(self.BUILDPATH,"nginx.conf"),"w")
        nginxconfresult.write(nginxconf)
        nginxconfresult.close()

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
        config_json = open(os.path.join(self.BUILDPATH,"config.json"),"w")
        config_json.write(jenc.encode(scv_config))
        config_json.close()

        shutil.copyfile(os.path.join(p,"skarphed.conf"), os.path.join(self.BUILDPATH,"skarphed.conf"))
        shutil.copyfile(os.path.join(p,"install.sh"), os.path.join(self.BUILDPATH,"install.sh"))
        shutil.copyfile(os.path.join(p,"uwsgi.conf"), os.path.join(self.BUILDPATH,"uwsgi.conf"))

        self.status = 30
        gobject.idle_add(self.updated)

        shutil.copytree(os.path.join(COREFILES,"web"), os.path.join(self.BUILDPATH, "web"))
        shutil.copytree(os.path.join(COREFILES,"lib"), os.path.join(self.BUILDPATH,"lib"))

        tar = tarfile.open(os.path.join(self.BUILDPATH,"scv_install.tar.gz"),"w:gz")
        tar.add(os.path.join(self.BUILDPATH,"nginx.conf"))
        tar.add(os.path.join(self.BUILDPATH,"uwsgi.conf"))
        tar.add(os.path.join(self.BUILDPATH,"config.json"))
        tar.add(os.path.join(self.BUILDPATH,"skarphed.conf"))
        tar.add(os.path.join(self.BUILDPATH,"install.sh"))
        tar.add(os.path.join(self.BUILDPATH,"web"))
        tar.add(os.path.join(self.BUILDPATH,"lib"))
        tar.close()

        self.status = 45
        gobject.idle_add(self.updated)

        con = self.server.getSSH()
        con_stdin, con_stdout, con_stderr = con.exec_command("mkdir /tmp/scvinst"+str(self.installationId))

        self.status = 50
        gobject.idle_add(self.updated)


        con = self.server.getSSH()
        ftp = con.open_sftp()
        ftp.put(os.path.join(self.BUILDPATH,"scv_install.tar.gz"),"/tmp/scvinst"+str(self.installationId)+"/scv_install.tar.gz")
        ftp.close()

        self.status = 65
        gobject.idle_add(self.updated)


        con = self.server.getSSH()
        con_stdin, con_stdout, con_stderr = con.exec_command("cd /tmp/scvinst"+str(self.installationId)+"; tar xvfz scv_install.tar.gz -C / ; chmod 755 install.sh ; ./install.sh ")

        output = con_stdout.read()
        logging.debug("SSH-outputlength: %d"%len(output))
        logging.debug(output)
        
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
        ftp.put(os.path.join(p,"teardown.sh"),"/tmp/teardown.sh")
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
