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
from gui import IconStock
pygtk.require("2.0")
import gtk

from GenericObject import GenericObjectPage
from GenericObject import PageFrame
from data.Generic import GenericObjectStoreException

class Scoville_repoPage (GenericObjectPage):
    def __init__(self,par,repo):
        self.par = par
        GenericObjectPage.__init__(self,par,repo)
        self.repoId = repo.getLocalId()
        
        self.table = gtk.Table(2,4,False)
        
        self.moduleFrame=PageFrame(self, "Modules", IconStock.MODULE)
        self.moduleList = ModuleList(self,repo)
        self.moduleFrame.add(self.moduleList)
        self.pack_start(self.moduleFrame,False)
        
        self.uploadFrame=PageFrame(self, "Upload", IconStock.MODULE)
        self.uploadbox = gtk.HBox()
        self.uploadbox.set_border_width(10)
        self.upload_label = gtk.Label("Please choose the module and click OK")
        self.upload_filechoose = gtk.FileChooserButton("Select Template", None)
        self.upload_filechoose.connect("file-set", self.fileChosen)
        self.upload_filechoose.set_size_request(200,30)
        self.upload_enter = gtk.Button(stock=gtk.STOCK_OK)
        self.upload_enter.connect("clicked", self.uploadModule)
        self.upload_dummy = gtk.Label("")
        self.uploadbox.pack_start(self.upload_label,False)
        self.uploadbox.pack_start(self.upload_filechoose,False)
        self.uploadbox.pack_start(self.upload_enter,False)
        self.uploadbox.pack_start(self.upload_dummy,True)
        self.uploadFrame.add(self.uploadbox)
        self.pack_start(self.uploadFrame,False)
        
        self.adminFrame= PageFrame(self, "Change Password", IconStock.CREDENTIAL)
        self.adminHBox = gtk.HBox()
        self.adminHBoxDummy = gtk.Label("")
        self.adminTable= gtk.Table(2,4,False)
        self.adminLabel = gtk.Label("Change admin-password here:")
        self.adminPasswordLabel = gtk.Label("New password")
        self.adminRepeatLabel = gtk.Label("New password (repeat)")
        self.adminPasswordEntry = gtk.Entry()
        self.adminPasswordEntry.set_visibility(False)
        self.adminPasswordEntry.set_invisible_char("●")
        self.adminRepeatEntry = gtk.Entry()
        self.adminRepeatEntry.set_visibility(False)
        self.adminRepeatEntry.set_invisible_char("●")
        self.adminButtonDummy = gtk.Label()
        self.adminButtonHBox = gtk.HBox()
        self.adminButtonChange = gtk.Button(stock=gtk.STOCK_OK)
        self.adminButtonHBox.pack_start(self.adminButtonDummy,True)
        self.adminButtonHBox.pack_start(self.adminButtonChange,False)
        self.adminTable.attach(self.adminLabel,0,2,0,1)
        self.adminTable.attach(self.adminPasswordLabel,0,1,1,2)
        self.adminTable.attach(self.adminPasswordEntry,1,2,1,2)
        self.adminTable.attach(self.adminRepeatLabel,0,1,2,3)
        self.adminTable.attach(self.adminRepeatEntry,1,2,2,3)
        self.adminTable.attach(self.adminButtonHBox,0,2,3,4)
        self.adminHBox.pack_start(self.adminTable,False)
        self.adminHBox.pack_start(self.adminHBoxDummy,True)
        self.adminFrame.add(self.adminHBox)
        self.adminButtonChange.connect("clicked", self.cb_ChangePassword)
        self.pack_start(self.adminFrame,False)
        
        
        self.developerFrame = PageFrame(self, "Developers", IconStock.USER)
        self.developerHBox= gtk.HBox()
        self.developerList= DeveloperList(self,repo)
        self.developerHBox.pack_start(self.developerList,True)
        self.developerTable = gtk.Table(2,5,False)
        self.developerButtonHBox = gtk.HBox()
        self.developerButtonHBoxDummy = gtk.Label()
        self.developerLabel = gtk.Label("Please enter the information for a new Developer here:")
        self.developerNameLabel = gtk.Label("Nickname:")
        self.developerFullnameLabel = gtk.Label("Full Name:")
        self.developerPublicKeyLabel = gtk.Label("Public Key:")
        self.developerNameEntry = gtk.Entry()
        self.developerFullnameEntry = gtk.Entry()
        self.developerPublicKeyEntry = gtk.TextView()
        self.developerAddButton = gtk.Button(stock=gtk.STOCK_ADD)
        self.developerAddButton.connect("clicked", self.cb_Add)
        self.developerButtonHBox.pack_start(self.developerButtonHBoxDummy,True)
        self.developerButtonHBox.pack_start(self.developerAddButton,False)
        self.developerTable.attach(self.developerLabel,0,2,0,1)
        self.developerTable.attach(self.developerNameLabel,0,1,1,2)
        self.developerTable.attach(self.developerNameEntry,1,2,1,2)
        self.developerTable.attach(self.developerFullnameLabel,0,1,2,3)
        self.developerTable.attach(self.developerFullnameEntry,1,2,2,3)
        self.developerTable.attach(self.developerPublicKeyLabel,0,1,3,4)
        self.developerTable.attach(self.developerPublicKeyEntry,1,2,3,4)
        self.developerTable.attach(self.developerButtonHBox,0,2,4,5)
        self.developerHBox.pack_start(self.developerTable,False)
        self.developerFrame.add(self.developerHBox)
        self.pack_start(self.developerFrame,False)
        
        self.show_all()
        
        repo.addCallback(self.render)
    
    def render(self):
        try:
            repo = self.getApplication().getLocalObjectById(self.repoId)
        except GenericObjectStoreException:
            self.destroy()

        auth = repo.isAuthenticated()

        self.adminFrame.set_visible(auth)
        self.developerFrame.set_visible(auth)
        self.moduleList.render()
        self.developerList.render()
    
    def cb_ChangePassword(self, widget=None, data=None):
        pw1 = self.adminPasswordEntry.get_text()
        pw2 = self.adminRepeatEntry.get_text()
        if pw1 == pw2:
            repo = self.getApplication().getLocalObjectById(self.repoId)
            repo.changePassword(pw1)
        else:
            pass #TODO: Implement error behaviour


    def cb_Add(self,widget=None,data=None):
        name = self.developerNameEntry.get_text()
        fullName = self.developerFullnameEntry.get_text()
        textBuffer = self.developerPublicKeyEntry.get_buffer()
        publicKey = textBuffer.get_text(textBuffer.get_start_iter(),textBuffer.get_end_iter())
        
        repo = self.getApplication().getLocalObjectById(self.repoId)
        repo.registerDeveloper(name,fullName,publicKey)
        
    
    def fileChosen(self, widget=None, data=None):
        self.fileToUpload = widget.get_filename()
    
    
    def uploadModule(self,widget=None,data=None):
        repo = self.getApplication().getLocalObjectById(self.repoId)
        repo.uploadModule(self.fileToUpload)
    
    def getPar(self):
        return self.par
    
    def getApplication(self):
        return self.getPar().getApplication()

class ModuleList(gtk.ScrolledWindow):
    def __init__(self, par, repo):
        self.par = par
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        
        self.treeview = gtk.TreeView()
        self.store= gtk.ListStore(gtk.gdk.Pixbuf, str)
        self.treeview.set_model(self.store)
        self.repoId = repo.getLocalId()
        
        self.col = gtk.TreeViewColumn("Module")
        self.ren_icon = gtk.CellRendererPixbuf()
        self.ren_text = gtk.CellRendererText()
        self.col.pack_start(self.ren_icon,False)
        self.col.pack_start(self.ren_text,True)
        self.col.add_attribute(self.ren_icon, 'pixbuf',0)
        self.col.add_attribute(self.ren_text, 'text', 1)
        self.treeview.append_column(self.col)
        self.add(self.treeview)
        
        repo.addCallback(self.render)
        self.show_all()
        self.render()
        
    def render(self):
        repo = self.getApplication().getLocalObjectById(self.repoId)
        modules = repo.getModules()
        
        self.store.clear()
        for module in modules:
            self.store.append((IconStock.MODULE,module['hrname']))

    def getPar(self):
        return self.par
    
    def getApplication(self):
        return self.getPar().getApplication()
        

class DeveloperList(gtk.ScrolledWindow):
    def __init__(self, par, repo):
        self.par = par
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        
        self.treeview = gtk.TreeView()
        self.store= gtk.ListStore(gtk.gdk.Pixbuf, str)
        self.treeview.set_model(self.store)
        self.repoId = repo.getLocalId()
        
        self.col = gtk.TreeViewColumn("Developer")
        self.ren_icon = gtk.CellRendererPixbuf()
        self.ren_text = gtk.CellRendererText()
        self.col.pack_start(self.ren_icon,False)
        self.col.pack_start(self.ren_text,True)
        self.col.add_attribute(self.ren_icon, 'pixbuf',0)
        self.col.add_attribute(self.ren_text, 'text', 1)
        self.treeview.append_column(self.col)
        self.add(self.treeview)
        
        repo.addCallback(self.render)
        self.show_all()
        self.render()
        
    def render(self):
        repo = self.getApplication().getLocalObjectById(self.repoId)
        developers = repo.getDevelopers()
        
        self.store.clear()
        for developer in developers:
            self.store.append((IconStock.USER,developer['fullName']))
        
        
    def getPar(self):
        return self.par
    
    def getApplication(self):
        return self.getPar().getApplication()
        
