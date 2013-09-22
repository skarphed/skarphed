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

from GenericObject import ObjectPageAbstract
from GenericObject import PageFrame
from OperationDaemonControl import OperationDaemonControl
from gui.DefaultEntry import DefaultEntry
import gui.IconStock

from glue.lng import _

class SkarphedPage(ObjectPageAbstract):
    RENDER_PURE = 0
    RENDER_AJAX = 1
    def __init__(self,par,skarphed):
        ObjectPageAbstract.__init__(self,par,skarphed)

        self.headline = gtk.Label(_("Skarphed Instance"))
        self.pack_start(self.headline,False)
        
        self.repo = PageFrame(self,_("Repository"), gui.IconStock.REPO)
        self.repoDummy = gtk.Label("")
        self.repoHBox = gtk.HBox()
        self.repotable = gtk.Table(2,3)
        self.repoLabel = gtk.Label(_("Repository"))
        self.repoEntry = DefaultEntry(default_message=_("example_repo.org:80"))
        self.repoInfoLabel = gtk.Label(_("Please enter Repository URL here:"))
        self.repoOkButton = gtk.Button(stock=gtk.STOCK_OK)
        self.repoOkButton.connect("clicked", self.cb_changeRepo)
        
        self.repotable.attach(self.repoInfoLabel,0,2,0,1)
        self.repotable.attach(self.repoLabel,0,1,1,2)
        self.repotable.attach(self.repoEntry,1,2,1,2)
        self.repotable.attach(self.repoOkButton,1,2,2,3)
        self.repoHBox.pack_start(self.repotable,False)
        self.repoHBox.pack_start(self.repoDummy,True)
        self.repo.add(self.repoHBox)

        self.pack_start(self.repo,False)

        self.opd = OperationDaemonControl(self,skarphed.getOperationDaemon())
        self.pack_start(self.opd,False)
        
        self.pki = PageFrame(self, _("Public Key"), gui.IconStock.CREDENTIAL)
        self.pki_label = gtk.Label(_("Instance Public Key:"))
        self.pki_textview = gtk.TextView()
        self.pki_textbuffer = gtk.TextBuffer()
        self.pki_textview.set_buffer(self.pki_textbuffer)
        self.pki_vbox = gtk.VBox()
        self.pki_vbox.pack_start(self.pki_label,False)
        self.pki_vbox.pack_start(self.pki_textview,True)
        self.pki.add(self.pki_vbox)
        self.pack_start(self.pki, False)

        self.settings = PageFrame(self, _("Server Settings"), gui.IconStock.SKARPHED)
        self.settings_vbox = gtk.VBox()
        self.settings_maintenance_toggle_lock = False
        self.settings_maintenance_hbox = gtk.HBox()
        self.settings_maintenance_checkbox = gtk.CheckButton(label=_("Maintenancemode active"))
        self.settings_maintenance_dummy = gtk.Label()
        self.settings_maintenance_hbox.pack_start(self.settings_maintenance_checkbox,False)
        self.settings_maintenance_hbox.pack_start(self.settings_maintenance_dummy,True)
        self.settings_maintenance_checkbox.connect("toggled", self.cb_maintenance)
        self.settings_vbox.pack_start(self.settings_maintenance_hbox,False)

        self.settings_rendermode_toggle_lock = False
        self.settings_rendermode_table = gtk.Table(2,2,False)
        self.settings_rendermode_pure = gtk.RadioButton(label=_("Pure (only static HTML)"))
        self.settings_rendermode_ajax = gtk.RadioButton(group=self.settings_rendermode_pure,label=_("AJAX (requires JS)"))
        self.settings_rendermode_dummy = gtk.Label("")
        self.settings_rendermode_pure.connect("toggled", self.cb_rendermode, SkarphedPage.RENDER_PURE)
        self.settings_rendermode_ajax.connect("toggled", self.cb_rendermode, SkarphedPage.RENDER_AJAX)
        self.settings_rendermode_table.attach(self.settings_rendermode_pure,0,1,0,1,gtk.FILL|gtk.SHRINK,gtk.FILL|gtk.SHRINK)
        self.settings_rendermode_table.attach(self.settings_rendermode_ajax,0,1,1,2,gtk.FILL|gtk.SHRINK,gtk.FILL|gtk.SHRINK)
        self.settings_rendermode_table.attach(self.settings_rendermode_dummy,1,2,0,2,gtk.FILL|gtk.EXPAND,gtk.FILL|gtk.EXPAND)
        self.settings_vbox.pack_start(self.settings_rendermode_table,False)

        self.settings.add(self.settings_vbox)
        self.pack_start(self.settings,False)

        self.show_all()
        
        self.render()
    
    def render(self):
        skarphed = self.getMyObject()
        if not skarphed:
            return


        self.repoEntry.set_text(skarphed.getRepoURL())
        public_key = skarphed.getPublickey()
        if public_key is not None:
            self.pki_textbuffer.set_text(public_key)
        else:
            self.pki_textbuffer.set_text("")

        self.settings_maintenance_toggle_lock = True
        self.settings_maintenance_checkbox.set_active(skarphed.isMaintenanceMode())
        self.settings_maintenance_toggle_lock = False
        
        rendermode = skarphed.getRendermode()
        if rendermode is not None:
            self.settings_rendermode_toggle_lock = True
            self.settings_rendermode_pure.set_active(rendermode == "pure")
            self.settings_rendermode_toggle_lock = True
            self.settings_rendermode_ajax.set_active(rendermode == "ajax")

    def cb_maintenance(self,widget=None,data=None):
        if self.settings_maintenance_toggle_lock:
            self.settings_maintenance_toggle_lock = False
            return

        skarphed = self.getMyObject()
        if not skarphed:
            self.destroy()
            return

        state = self.settings_maintenance_checkbox.get_active()
        skarphed.setMaintenanceMode(state)

    def cb_rendermode(self,widget=None,data=None):
        if self.settings_rendermode_toggle_lock:
            self.settings_rendermode_toggle_lock = False
            return

        skarphed = self.getMyObject()
        if not skarphed:
            self.destroy()
            return

        rendermode = skarphed.getRendermode()
        if data == SkarphedPage.RENDER_PURE and rendermode != "pure":
            skarphed.setRendermode("pure")

        if data == SkarphedPage.RENDER_AJAX and rendermode != "ajax":
            skarphed.setRendermode("ajax")

    def cb_changeRepo(self, widget=None, data=None):
        skarphed = self.getMyObject()
        if not skarphed:
            return

        repostring = self.repoEntry.get_text()
        skarphed.setRepository(repostring)



