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

class NewScoville(gtk.Window):
    def __init__(self,par,server=None):
        self.par = par
        self.serverId =None
        if server is not None:
            self.serverId = server.getLocalId()
        gtk.Window.__init__(self)
        self.targetsRendered = False


        self.vbox = gtk.VBox()
        self.set_title("Scoville Admin :: Create Instance")
        self.set_border_width(10)
        self.toplabel = gtk.Label("Please configure the new Installation")

        self.frm_srv = gtk.Frame("Server")
        self.frm_db = gtk.Frame("Database")
        self.frm_target = gtk.Frame("Target-OS")
        self.frm_apache = gtk.Frame("Apache2")

        self.frm_srv_tbl = gtk.Table(2,2,False)
        self.frm_db_tbl = gtk.Table(2,4,False)
        self.frm_target_tbl = gtk.Table(3,1,False)
        self.frm_root_tbl = gtk.Table(2,2,False)
        self.frm_apache_tbl = gtk.Table(2,4,False)

        self.srv_combobox = gtk.ComboBox()
        self.srv_combobox_model = gtk.ListStore(gtk.gdk.Pixbuf,str,int)
        self.srv_combobox.set_model(self.srv_combobox_model)
        self.srv_cell_icon = gtk.CellRendererPixbuf()
        self.srv_combobox.pack_start(self.srv_cell_icon, True)
        self.srv_combobox.add_attribute(self.srv_cell_icon, "pixbuf", 0)
        self.srv_cell_name = gtk.CellRendererText()
        self.srv_combobox.pack_start(self.srv_cell_name, False)
        self.srv_combobox.add_attribute(self.srv_cell_name, "text", 1)
        self.srv_label = gtk.Label("Server:")
        self.srv_name_label = gtk.Label("New Instance Name:")
        self.srv_name_entry = gtk.Entry()
        self.srv_name_entry.set_text("New Scoville Instance")

        self.frm_srv_tbl.attach(self.srv_label,0,1,0,1)
        self.frm_srv_tbl.attach(self.srv_combobox,1,2,0,1)
        self.frm_srv_tbl.attach(self.srv_name_label,0,1,1,2)
        self.frm_srv_tbl.attach(self.srv_name_entry,1,2,1,2)
        self.frm_srv.add(self.frm_srv_tbl)

        self.db_ip_entry = gtk.Entry()
        self.db_name_entry = gtk.Entry()
        self.db_user_entry = gtk.Entry()
        self.db_pass_entry = gtk.Entry()
        self.db_ip_label = gtk.Label("IP:")
        self.db_name_label = gtk.Label("DB-Name:")
        self.db_user_label = gtk.Label("User:")
        self.db_pass_label = gtk.Label("Password:")

        self.frm_db_tbl.attach(self.db_ip_label,0,1,0,1)
        self.frm_db_tbl.attach(self.db_ip_entry,1,2,0,1)
        self.frm_db_tbl.attach(self.db_name_label,0,1,1,2)
        self.frm_db_tbl.attach(self.db_name_entry,1,2,1,2)
        self.frm_db_tbl.attach(self.db_user_label,0,1,2,3)
        self.frm_db_tbl.attach(self.db_user_entry,1,2,2,3)
        self.frm_db_tbl.attach(self.db_pass_label,0,1,3,4)
        self.frm_db_tbl.attach(self.db_pass_entry,1,2,3,4)
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
        self.apache_ip_entry = gtk.Entry()
        self.apache_port_label = gtk.Label("Listen-Port:")
        self.apache_port_entry = gtk.Entry()
        self.apache_domain_label = gtk.Label("ServerName:")
        self.apache_domain_entry = gtk.Entry()
        self.apache_subdomain_label = gtk.Label("ServerAlias:")
        self.apache_subdomain_entry = gtk.Entry()

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
        self.cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.buttonboxdummy = gtk.Label("")
        self.buttonhbox = gtk.HBox()
        self.buttonhbox.pack_start(self.buttonboxdummy,True)
        self.buttonhbox.pack_start(self.cancel,False)
        self.buttonhbox.pack_start(self.ok,False)

        
        self.vboxdummy = gtk.Label("")
        self.vbox.pack_start(self.toplabel)
        self.vbox.pack_start(self.frm_srv)
        self.vbox.pack_start(self.frm_db)
        self.vbox.pack_start(self.frm_target)
        self.vbox.pack_start(self.frm_apache)
        self.vbox.pack_start(self.vboxdummy)
        self.vbox.pack_start(self.buttonhbox)
        self.add(self.vbox)

        self.ok.connect("clicked", self.cb_Ok)
        self.cancel.connect("clicked", self.cb_Cancel)

        self.show_all()
        self.getApplication().getObjectStore().addCallback(self.render)
        self.render()


    def cb_Ok(self,widget=None,data=None):
        if self.serverId is not None:
            server = self.getApplication().getLocalObjectById(self.serverId)
            instanceData = {
              "core.name":self.srv_name_entry.get_text(),
              "db.ip":self.db_ip_entry.get_text(),
              "db.name":self.db_name_entry.get_text(),
              "db.user":self.db_user_entry.get_text(),
              "db.password":self.db_pass_entry.get_text(),
              "apache.ip":self.apache_ip_entry.get_text(),
              "apache.port":self.apache_port_entry.get_text(),
              "apache.domain":self.apache_domain_entry.get_text(),
              "apache.subdomain":self.apache_subdomain_entry.get_text(),
            }
            target = self.target_combobox.get_active_text()
            server.installNewInstance(instanceData, target)


    def cb_Cancel(self,widget=None,data=None):
        print "ABBRECHEN GELECKT"

    def getModuleIterById(self, serverlist, serverId):
        def search(model, path, rowiter, serverId):
            val = model.get_value(rowiter,2)
            if val == serverId:
                model.tempiter = rowiter
        
        serverlist.tempiter = None
        serverlist.foreach(search, serverId)
        rowiter=serverlist.tempiter
        if rowiter is not None:
            return rowiter
        else:
            return None

    def render(self):
        def search(model, path, rowiter, processed):
            val = model.get_value(rowiter,2)
            if val not in processed:
                model.itersToRemove.append(rowiter)
        self.servers = self.getApplication().getObjectStore().getServers()
        processedServerIds = []
        for server in self.servers:
            rowiter = self.getModuleIterById(self.srv_combobox_model, server.getLocalId()) 
            if rowiter is None:
                self.srv_combobox_model.append((gui.IconStock.getServerIcon(server),server.getName(),server.getLocalId()))
            else:
                self.srv_combobox_model.set_value(rowiter,0,gui.IconStock.getServerIcon(server))
                self.srv_combobox_model.set_value(rowiter,1,server.getName())
            processedServerIds.append(server.getLocalId())


        if self.serverId is not None:
            activeiter = self.getModuleIterById(self.srv_combobox_model, self.serverId) 
            self.srv_combobox.set_active_iter(activeiter)
        self.srv_combobox_model.itersToRemove = []
        self.srv_combobox_model.foreach(search, processedServerIds)
        for rowiter in self.srv_combobox_model.itersToRemove:
            self.srv_combobox_model.remove(rowiter)

        if not self.targetsRendered:
            targets = self.servers[0].INSTALLATION_TARGETS
            for target in targets:
                self.target_combobox_model.append((target,))
            self.target_combobox.set_active_iter(self.target_combobox_model.get_iter_first())
            self.targetsRendered=True

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()