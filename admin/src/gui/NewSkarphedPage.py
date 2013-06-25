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

import pygtk
pygtk.require("2.0")
import gtk
import os
import gui.IconStock
from ObjectCombo import ObjectCombo
from DefaultEntry import DefaultEntry
from data.Server import Server
from data.Generic import GenericObjectStoreException

from glue.lng import _

class NewSkarphedPage(gtk.Frame):
    def __init__(self,par,server=None):
        self.par = par
        self.serverId =None
        self.installerId = None
        if server is not None:
            self.serverId = server.getLocalId()
        gtk.Frame.__init__(self, _("Skarphed Admin :: Create Instance"))
        self.targetsRendered = False

        self.extradata_widgets = {}
        self.extradata_table = None
        self.no_installer_label = None

        self.alignment = gtk.Alignment(0.5,0.5,0.1,0.2)
        self.vbox = gtk.VBox()
        self.set_border_width(10)
        self.toplabel = gtk.Label(_("Please configure the new Installation"))

        self.frm_srv = gtk.Frame(_("Server"))
        self.frm_repo = gtk.Frame(_("Repository"))
        self.frm_db = gtk.Frame(_("Database"))
        self.frm_target = gtk.Frame(_("Target-OS"))
        self.frm_extradata = gtk.Frame()

        self.frm_srv_tbl = gtk.Table(2,2,False)
        self.frm_repo_tbl = gtk.Table(2,1,False)
        self.frm_db_tbl = gtk.Table(2,2,False)
        self.frm_target_tbl = gtk.Table(3,1,False)
        self.frm_root_tbl = gtk.Table(2,2,False)

        self.srv_combobox = ObjectCombo(self,"Server", server)

        self.srv_label = gtk.Label(_("Server:"))
        self.srv_name_label = gtk.Label(_("New Instance Name:"))
        self.srv_name_entry = DefaultEntry(default_message=_("Instance-Name"))

        self.frm_srv_tbl.attach(self.srv_label,0,1,0,1)
        self.frm_srv_tbl.attach(self.srv_combobox,1,2,0,1)
        self.frm_srv_tbl.attach(self.srv_name_label,0,1,1,2)
        self.frm_srv_tbl.attach(self.srv_name_entry,1,2,1,2)
        self.frm_srv.add(self.frm_srv_tbl)

        self.repo_combobox = ObjectCombo(self,"Skarphed_repo", selectFirst=True)
        self.repo_label = gtk.Label(_("Repository"))

        self.frm_repo_tbl.attach(self.repo_label,0,1,0,1)
        self.frm_repo_tbl.attach(self.repo_combobox,1,2,0,1)
        self.frm_repo.add(self.frm_repo_tbl)

        self.db_radio_new = gtk.RadioButton(None,_("Create new on Database:"))
        self.db_radio_use = gtk.RadioButton(self.db_radio_new,_("Use existing Schema:"))
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

        self.target_label = gtk.Label(_("Target-OS:"))
        self.target_display = gtk.Label("")

        self.frm_target_tbl.attach(self.target_label,0,1,0,1)
        self.frm_target_tbl.attach(self.target_display,1,2,0,1)
        self.frm_target.add(self.frm_target_tbl)

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
        self.vbox.pack_start(self.frm_extradata)
        self.vbox.pack_start(self.vboxdummy)
        self.vbox.pack_start(self.buttonhbox)
        self.alignment.add(self.vbox)
        self.add(self.alignment)

        self.ok.connect("clicked", self.cb_Ok)
        self.cancel.connect("clicked", self.cb_Cancel)
        self.connect("delete-event",self.cb_Cancel)
        self.srv_combobox.connect("changed", self.render)

        #self.set_icon_from_file("../data/icon/mp_logo.png")

        self.getApplication().getMainWindow().openDialogPane(self)
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
          "db.password":schemaInfo['pass']
        }

        for key, widget in self.extradata_widgets.items():
            instanceData[key] = widget.get_text()

        installer = server.installNewInstance(instanceData)
        self.installerId = installer.getLocalId()


    def cb_Cancel(self,widget=None,data=None):
        self.srv_combobox.destroy()
        self.repo_combobox.destroy()
        self.db_db_combo.destroy()
        self.db_schema_combo.destroy()
        self.getApplication().getMainWindow().closeDialogPane()

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

        """if not self.targetsRendered:
            targets = Server.INSTALLATION_TARGETS
            for target in targets:
                self.target_combobox_model.append((target,))
            self.target_combobox.set_active_iter(self.target_combobox_model.get_iter_first())
            self.targetsRendered=True"""

        if self.extradata_table is not None:
            self.extradata_table.destroy()
            self.extradata_table = None
        if self.no_installer_label is not None:
            self.no_installer_label.destroy()
            self.no_installer_label = None

        server = self.srv_combobox.getSelected()

        if server is not None:
            target = server.getTarget()
            if server.isTargetUsable():
                self.target_display.set_text(target.getName())
                self.frm_extradata.set_label_widget(gtk.Label(target.getName()))
                extradata = target.getExtraParams()
                extradata_table = gtk.Table(2,len(extradata),False)
                i = 0
                for key, value in extradata.items():
                    label = gtk.Label(value[0])
                    entry = DefaultEntry(default_message=value[1])
                    self.extradata_widgets[key] = entry
                    extradata_table.attach(label,0,1,i,i+1)
                    extradata_table.attach(entry,1,2,i,i+1)
                    i += 1
                self.extradata_table = extradata_table
                self.frm_extradata.add(extradata_table)
                extradata_table.show_all()
                self.ok.set_sensitive(True)
            else:
                self.no_installer_label = gtk.Label(_("No appropriate installer available"))
                self.frm_extradata.add(self.no_installer_label)
                self.no_installer_label.show()
                self.target_display.set_text(target)
                self.ok.set_sensitive(False)


        if self.installerId is not None:
            try:
                installer = self.getApplication().getLocalObjectById(self.installerId)
                self.progress.set_fraction(installer.getStatus()/100)
                self.progress.set_text(_("Installing ... %d %%")%(installer.getStatus(),))
                
                sensitive = installer.status == 100
            except GenericObjectStoreException:
                sensitive = True

            self.srv_combobox.set_sensitive(sensitive)
            self.repo_combobox.set_sensitive(sensitive)
            self.srv_name_entry.set_sensitive(sensitive)
            self.db_db_combo.set_sensitive(sensitive)
            self.db_schema_combo.set_sensitive(sensitive)
            self.db_radio_new.set_sensitive(sensitive)
            self.db_radio_use.set_sensitive(sensitive)
            for widget in self.extradata_widgets.values():
                widget.set_sensitive(sensitive)   
            self.ok.set_sensitive(sensitive)
            self.cancel.set_sensitive(sensitive)

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
