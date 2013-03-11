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

import pygtk
pygtk.require("2.0")
import gtk
import os
import gui.IconStock
from ObjectCombo import ObjectCombo
from DefaultEntry import DefaultEntry
from data.Server import Server
from data.Generic import GenericObjectStoreException

class NewScoville(gtk.Window):
    def __init__(self,par,server=None):
        self.par = par
        self.serverId =None
        self.installerId = None
        if server is not None:
            self.serverId = server.getLocalId()
        gtk.Window.__init__(self)
        self.targetsRendered = False


        self.vbox = gtk.VBox()
        self.set_title("Scoville Admin :: Create Instance")
        self.set_border_width(10)
        self.toplabel = gtk.Label("Please configure the new Installation")

        self.frm_srv = gtk.Frame("Server")
        self.frm_repo = gtk.Frame("Repository")
        self.frm_db = gtk.Frame("Database")
        self.frm_target = gtk.Frame("Target-OS")
        self.frm_apache = gtk.Frame("Apache2")

        self.frm_srv_tbl = gtk.Table(2,2,False)
        self.frm_repo_tbl = gtk.Table(2,1,False)
        self.frm_db_tbl = gtk.Table(2,2,False)
        self.frm_target_tbl = gtk.Table(3,1,False)
        self.frm_root_tbl = gtk.Table(2,2,False)
        self.frm_apache_tbl = gtk.Table(2,4,False)

        self.srv_combobox = ObjectCombo(self,"Server", server)

        self.srv_label = gtk.Label("Server:")
        self.srv_name_label = gtk.Label("New Instance Name:")
        self.srv_name_entry = DefaultEntry()
        self.srv_name_entry.set_default_message("Instance-Name")

        self.frm_srv_tbl.attach(self.srv_label,0,1,0,1)
        self.frm_srv_tbl.attach(self.srv_combobox,1,2,0,1)
        self.frm_srv_tbl.attach(self.srv_name_label,0,1,1,2)
        self.frm_srv_tbl.attach(self.srv_name_entry,1,2,1,2)
        self.frm_srv.add(self.frm_srv_tbl)

        self.repo_combobox = ObjectCombo(self,"Scoville_repo", selectFirst=True)
        self.repo_label = gtk.Label("Repository")

        self.frm_repo_tbl.attach(self.repo_label,0,1,0,1)
        self.frm_repo_tbl.attach(self.repo_combobox,1,2,0,1)
        self.frm_repo.add(self.frm_repo_tbl)

        self.db_radio_new = gtk.RadioButton(None,"Create new on Database:")
        self.db_radio_use = gtk.RadioButton(self.db_radio_new,"Use existing Schema:")
        self.db_db_combo = ObjectCombo(self,"Database", selectFirst=True)
        self.db_schema_combo = ObjectCombo(self,"Schema", selectFirst=True)
        self.db_schema_combo.set_sensitive(False)

        self.db_radio_new.connect("toggled", self.cb_ToggledDb,1)
        self.db_radio_use.connect("toggled", self.cb_ToggledDb,2)
        
        self.frm_db_tbl.attach(self.db_radio_new,0,1,0,1)
        self.frm_db_tbl.attach(self.db_db_combo,1,2,0,1)
        self.frm_db_tbl.attach(self.db_radio_use,0,1,1,2)
        self.frm_db_tbl.attach(self.db_schema_combo,1,2,1,2)
        self.frm_db.add(self.frm_db_tbl)        

        self.target_label = gtk.Label("Target-OS:")
        self.target_combobox_model = gtk.ListStore(str)
        self.target_combobox_renderer = gtk.CellRendererText()
        self.target_combobox = gtk.ComboBox(self.target_combobox_model)
        self.target_combobox.pack_start(self.target_combobox_renderer,True)
        self.target_combobox.add_attribute(self.target_combobox_renderer,'text',0)
        self.target_custombutton = gtk.Button("Customize")

        self.frm_target_tbl.attach(self.target_label,0,1,0,1)
        self.frm_target_tbl.attach(self.target_combobox,1,2,0,1)
        self.frm_target_tbl.attach(self.target_custombutton,2,3,0,1)
        self.frm_target.add(self.frm_target_tbl)

        self.apache_ip_label = gtk.Label("Listen-IP:")
        self.apache_ip_entry = DefaultEntry()
        self.apache_ip_entry.set_default_message("255.255.255.255 or *")
        self.apache_port_label = gtk.Label("Listen-Port:")
        self.apache_port_entry = DefaultEntry()
        self.apache_port_entry.set_default_message("80")
        self.apache_domain_label = gtk.Label("ServerName:")
        self.apache_domain_entry = DefaultEntry()
        self.apache_domain_entry.set_default_message("[subdomain.]domain.tld or leave empty")
        self.apache_subdomain_label = gtk.Label("ServerAlias:")
        self.apache_subdomain_entry = DefaultEntry()
        self.apache_subdomain_entry.set_default_message("[subdomain.]domain.tld or leave empty")

        self.frm_apache_tbl.attach(self.apache_ip_label,0,1,0,1)
        self.frm_apache_tbl.attach(self.apache_ip_entry,1,2,0,1)
        self.frm_apache_tbl.attach(self.apache_port_label,0,1,1,2)
        self.frm_apache_tbl.attach(self.apache_port_entry,1,2,1,2)
        self.frm_apache_tbl.attach(self.apache_domain_label,0,1,2,3)
        self.frm_apache_tbl.attach(self.apache_domain_entry,1,2,2,3)
        self.frm_apache_tbl.attach(self.apache_subdomain_label,0,1,3,4)
        self.frm_apache_tbl.attach(self.apache_subdomain_entry,1,2,3,4)
        self.frm_apache.add(self.frm_apache_tbl)

        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        self.cancel = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.progress = gtk.ProgressBar()
        self.buttonhbox = gtk.HBox()
        self.buttonhbox.pack_start(self.progress,True)
        self.buttonhbox.pack_start(self.cancel,False)
        self.buttonhbox.pack_start(self.ok,False)

        
        self.vboxdummy = gtk.Label("")
        self.vbox.pack_start(self.toplabel)
        self.vbox.pack_start(self.frm_srv)
        self.vbox.pack_start(self.frm_repo)
        self.vbox.pack_start(self.frm_db)
        self.vbox.pack_start(self.frm_target)
        self.vbox.pack_start(self.frm_apache)
        self.vbox.pack_start(self.vboxdummy)
        self.vbox.pack_start(self.buttonhbox)
        self.add(self.vbox)

        self.ok.connect("clicked", self.cb_Ok)
        self.cancel.connect("clicked", self.cb_Cancel)
        self.connect("delete-event",self.cb_Cancel)

        self.set_icon_from_file("../data/icon/mp_logo.png")

        self.show_all()
        self.getApplication().getObjectStore().addCallback(self.render)
        self.render()

    def cb_Ok(self,widget=None,data=None):
        server = self.srv_combobox.getSelected()
        if self.db_radio_new.get_active():
            db = self.db_db_combo.getSelected()
            repo = self.repo_combobox.getSelected()
            newSchemaName = self.srv_name_entry.get_text()
            newSchemaName = newSchemaName.translate(None, "!\"§$%&/()=?`´#+~'><|^¹²³¼½¬{[]}\\ *-.,:;")
            schemaInfo = db.createSchema(newSchemaName,repo)
            schemaInfo['ip'] = db.getServer().getIp()
        elif self.db_radio_use.get_active():
            schema = self.db_schema_combo.getSelected()
            schemaInfo = {'name':schema.db_name,
                          'user':schema.db_user,
                          'pass':schema.db_password,
                          'ip':schema.getDatabase().getServer().getIp()}
 
        instanceData = {
          "core.name":self.srv_name_entry.get_text(),
          "db.ip":schemaInfo['ip'],
          "db.name":schemaInfo['name'],
          "db.user":schemaInfo['user'],
          "db.password":schemaInfo['pass'],
          "apache.ip":self.apache_ip_entry.get_text(),
          "apache.port":self.apache_port_entry.get_text(),
          "apache.domain":self.apache_domain_entry.get_text(),
          "apache.subdomain":self.apache_subdomain_entry.get_text(),
        }

        target = self.target_combobox.get_active_text()
        installer = server.installNewInstance(instanceData, target)
        self.installerId = installer.getLocalId()


    def cb_Cancel(self,widget=None,data=None):
        self.srv_combobox.destroy()
        self.repo_combobox.destroy()
        self.db_db_combo.destroy()
        self.db_schema_combo.destroy()
        self.destroy()

    def cb_ToggledDb(self, widget=None, data=None):
        if data==1:
            self.db_db_combo.set_sensitive(True)
            self.db_schema_combo.set_sensitive(False)
            self.repo_combobox.set_sensitive(True)
        elif data==2:
            self.db_db_combo.set_sensitive(False)
            self.db_schema_combo.set_sensitive(True)
            self.repo_combobox.set_sensitive(False)

    def render(self):
        self.srv_combobox.render()
        self.db_schema_combo.render()
        self.db_db_combo.render()

        if not self.targetsRendered:
            targets = Server.INSTALLATION_TARGETS
            for target in targets:
                self.target_combobox_model.append((target,))
            self.target_combobox.set_active_iter(self.target_combobox_model.get_iter_first())
            self.targetsRendered=True

        if self.installerId is not None:
            try:
                installer = self.getApplication().getLocalObjectById(self.installerId)
                self.progress.set_fraction(installer.getStatus()/100)
                self.progress.set_text("Installing ... %d %%"%(installer.getStatus(),))
                
                sensitive = installer.status == 100
            except GenericObjectStoreException, e:
                sensitive = True

            self.srv_combobox.set_sensitive(sensitive)
            self.repo_combobox.set_sensitive(sensitive)
            self.srv_name_entry.set_sensitive(sensitive)
            self.db_db_combo.set_sensitive(sensitive)
            self.db_schema_combo.set_sensitive(sensitive)
            self.db_radio_new.set_sensitive(sensitive)
            self.db_radio_use.set_sensitive(sensitive)
            self.target_combobox.set_sensitive(sensitive)
            self.apache_ip_entry.set_sensitive(sensitive)
            self.apache_port_entry.set_sensitive(sensitive)
            self.apache_domain_entry.set_sensitive(sensitive)
            self.apache_subdomain_entry.set_sensitive(sensitive)
            self.ok.set_sensitive(sensitive)
            self.cancel.set_sensitive(sensitive)

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()