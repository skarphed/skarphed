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


from skarphedadmin.gui import IconStock
from ViewPasswordButton import ViewPasswordButton
from InstancePage import InstancePage
from skarphedadmin.data.Generic import GenericObjectStoreException
from skarphedadmin.data.Server import Server

from skarphedadmin.gui.DefaultEntry import DefaultEntry

from skarphedadmin.glue.lng import _

class ServerPropertyPage(gtk.Frame):
    addWindowOpen=False
    MODE_EDIT = 0
    MODE_NEW = 1

    def __init__(self, parent, server=None):
        gtk.Frame.__init__(self)
        self.par = parent
        self.serverId = None
        if server is None:
            self.set_label(_("Skarphed Admin Pro :: New Server"))
            self.mode = ServerPropertyPage.MODE_NEW
        else:
            self.serverId = server.getLocalId()
            self.set_label(_("Skarphed Admin Pro :: Server Properties of ")+server.getIp())
            self.mode = ServerPropertyPage.MODE_EDIT
            
        self.vbox = gtk.VBox()
        
        self.instructionlabel = gtk.Label(_("Please enter the Server credentials"))
        self.vbox.pack_start(self.instructionlabel,False)
        
        self.ipFrame = gtk.Frame(_("Common"))
        self.ipFrameT = gtk.Table(2,3,False)
        self.ipFrame_IPLabel = gtk.Label(_("IP:"))
        self.ipFrame_IPEntry = DefaultEntry(default_message="172.16.13.37")
        self.ipFrameT.attach(self.ipFrame_IPLabel, 0,1,0,1)
        self.ipFrameT.attach(self.ipFrame_IPEntry, 1,2,0,1)
        self.ipFrame_NameLabel = gtk.Label(_("Name:"))
        self.ipFrame_NameEntry = DefaultEntry(default_message="Server1")
        self.ipFrameT.attach(self.ipFrame_NameLabel, 0,1,1,2)
        self.ipFrameT.attach(self.ipFrame_NameEntry, 1,2,1,2)
        self.ipFrame_Target_Label = gtk.Label("Target system:")
        self.ipFrame_Target_model = gtk.ListStore(str)
        for target in Server.INSTALLATION_TARGETS:
            self.ipFrame_Target_model.append((target.getName(),))
        self.ipFrame_Target_renderer = gtk.CellRendererText()
        self.ipFrame_Target = gtk.ComboBox(self.ipFrame_Target_model)
        self.ipFrame_Target.pack_start(self.ipFrame_Target_renderer,True)
        self.ipFrame_Target.add_attribute(self.ipFrame_Target_renderer,'text',0)
        self.ipFrameT.attach(self.ipFrame_Target_Label,0,1,2,3)
        self.ipFrameT.attach(self.ipFrame_Target,1,2,2,3)
        self.ipFrame.add(self.ipFrameT)

        self.vbox.pack_start(self.ipFrame,False)
                
        self.sshFrame = gtk.Frame(_("SSH"))
        self.sshFrameT = gtk.Table(2,2,False)
        self.sshFrame_NameLabel = gtk.Label(_("Username:"))
        self.sshFrame_NameEntry = DefaultEntry(default_message="root")
        self.sshFrame_PassLabel = gtk.Label(_("Password:"))
        self.sshFrame_PassEntry = gtk.Entry()
        self.sshFrame_PassEntry.set_visibility(False)
        self.sshFrame_PassEntry.set_invisible_char("●")
        self.sshFrameT.attach(self.sshFrame_NameLabel, 0,1,0,1)
        self.sshFrameT.attach(self.sshFrame_NameEntry, 1,2,0,1)
        self.sshFrameT.attach(self.sshFrame_PassLabel, 0,1,1,2)
        self.sshFrameT.attach(self.sshFrame_PassEntry, 1,2,1,2)
        self.sshFrame.add(self.sshFrameT)
        self.vbox.pack_start(self.sshFrame,False)
        
        self.instFrame = gtk.Frame(_("Instances"))
        self.instFrameT = gtk.Table(2,4,False)
        self.instList = gtk.TreeView()
        self.instStore = gtk.ListStore(gtk.gdk.Pixbuf,str,int)
        self.instList.set_model(self.instStore)
        self.instCol_Icon = gtk.TreeViewColumn()
        self.instCol_Name = gtk.TreeViewColumn(_('Instance'))
        self.instRen_Icon = gtk.CellRendererPixbuf()
        self.instRen_Name = gtk.CellRendererText()
        self.instCol_Icon.pack_start(self.instRen_Icon,False)
        self.instCol_Name.pack_start(self.instRen_Name,True)            
        self.instCol_Icon.add_attribute(self.instRen_Icon,'pixbuf',0)
        self.instCol_Name.add_attribute(self.instRen_Name,'text',1)
        self.instList.append_column(self.instCol_Icon)
        self.instList.append_column(self.instCol_Name)
        self.instAdd = gtk.Button(stock=gtk.STOCK_ADD)
        self.instRemove = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.instEdit = gtk.Button(stock=gtk.STOCK_EDIT)
        self.instFrameT.attach(self.instList,0,1,0,4)
        self.instFrameT.attach(self.instAdd,1,2,0,1)
        self.instFrameT.attach(self.instRemove,1,2,1,2)
        self.instFrameT.attach(self.instEdit,1,2,2,3)
        self.instAdd.connect("clicked",self.cb_Add)
        self.instRemove.connect("clicked",self.cb_Remove)
        self.instEdit.connect("clicked",self.cb_Edit)
        self.instList.connect("cursor-changed", self.cb_cursorChanged)
        self.instFrame.add(self.instFrameT)
        self.vbox.pack_start(self.instFrame,False)
        
        self.fill = gtk.Label("")
        self.vbox.pack_start(self.fill,True)
        
        self.buttons = gtk.HBox()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        self.cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.viewpass = ViewPasswordButton()
        self.viewpass.addEntry(self.sshFrame_PassEntry)
        self.ok.connect("clicked", self.cb_OK)
        self.cancel.connect("clicked", self.cb_Cancel)
        self.buttons.pack_end(self.ok,False)
        self.buttons.pack_end(self.cancel,False)
        self.buttons.pack_end(self.viewpass,False)
        self.vbox.pack_start(self.buttons,False)
        
        self.add(self.vbox)
        
        if server is not None:
            self.ipFrame_IPEntry.set_text(server.getIp())
            self.ipFrame_NameEntry.set_text(server.getRawName())
            self.sshFrame_NameEntry.set_text(server.getSSHName())
            self.sshFrame_PassEntry.set_text(server.getSSHPass())
            server.addCallback(self.render)
        self.getApplication().getMainWindow().openDialogPane(self)
        self.render()
    
    def render(self):
        def search(model, path, rowiter, target):
            text = model.get_value(rowiter,0)
            if text == target.getName():
                self.ipFrame_Target.set_active_iter(rowiter)

        server = None
        try:
            server = self.getApplication().getLocalObjectById(self.serverId)
        except GenericObjectStoreException:
            if self.mode == ServerPropertyPage.MODE_EDIT:
                self.getApplication().getMainWindow().closeDialogPane()
                return
        
        self.instFrame.set_visible(self.mode == ServerPropertyPage.MODE_EDIT)

        if server is not None and server.isTargetUsable():
            self.ipFrame_Target_model.foreach(search, server.getTarget())

        self.instStore.clear()
        if server is not None:
            for instance in server.getInstances():
                icon = IconStock.SKARPHED #TODO: Implement Icon
                self.instStore.append((icon,instance.getName(),instance.getLocalId()))
        self.cb_cursorChanged()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
    def cb_Add(self,widget=None,data=None):
        server = self.getApplication().getLocalObjectById(self.serverId)
        InstancePage(self,server)
    
    def cb_Remove(self,widget=None,data=None):
        instance = self.getCurrentInstance()
        if instance is None:
            return
        try:
            server = self.getApplication().getLocalObjectById(self.serverId)
        except GenericObjectStoreException:
            server = None
        server.removeInstance(instance)
        selection = self.instList.get_selection()
        rowiter = selection.get_selected()[1]
        self.instStore.remove(rowiter)
        self.render()
    
    def cb_Edit(self,widget=None,data=None):
        instance = self.getCurrentInstance()
        try:
            server = self.getApplication().getLocalObjectById(self.serverId)
        except GenericObjectStoreException:
            server = None
        if instance is None or server is None:
            return
        InstancePage(self,server,instance)

    def cb_cursorChanged(self, tree=None, path=None, data=None):
        selection = self.instList.get_selection()
        if selection is None:
            state = False
        else:
            rowiter = selection.get_selected()[1]
            state = rowiter is not None
        self.instEdit.set_sensitive(state)
        self.instRemove.set_sensitive(state)
    
    def getCurrentInstance(self, onlyId=True):
        try:
            server = self.getApplication().getLocalObjectById(self.serverId)
        except GenericObjectStoreException:
            server = None
        if server is None:
            return None
        selection = self.instList.get_selection()
        rowiter = selection.get_selected()[1]
        return self.getApplication().getLocalObjectById(self.instStore.get_value(rowiter,2))
         
    
    def cb_OK(self,widget=None,data=None):
        try:
            concernedServer = self.getApplication().getLocalObjectById(self.serverId)
        except GenericObjectStoreException:
            concernedServer = None
        if self.serverId is None:
            server = self.getApplication().getData().createServer()
            self.mode = ServerPropertyPage.MODE_EDIT
        else:
            server = concernedServer
        server.setIp(self.ipFrame_IPEntry.get_text())
        server.setName(self.ipFrame_NameEntry.get_text())
        server.setSSHName(self.sshFrame_NameEntry.get_text())
        server.setSSHPass(self.sshFrame_PassEntry.get_text())
        server.setTarget(self.ipFrame_Target.get_active_text())
        server.load = server.LOADED_PROFILE
        server.establishConnections()
        
        self.getApplication().getMainWindow().closeDialogPane()
    
    def cb_Cancel(self,widget=None,data=None):
        self.getApplication().getMainWindow().closeDialogPane()
        
