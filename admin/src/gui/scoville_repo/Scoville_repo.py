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

from GenericObject import ObjectPageAbstract
from GenericObject import PageFrame
from data.Generic import GenericObjectStoreException
from gui.YesNoPage import YesNoPage
from gui.DefaultEntry import DefaultEntry

class Scoville_repoPage (ObjectPageAbstract):
    def __init__(self,par,repo):
        ObjectPageAbstract.__init__(self,par,repo)
        
        self.table = gtk.Table(2,4,False)
        
        self.moduleFrame=PageFrame(self, "Modules", IconStock.MODULE)
        self.moduleList = ModuleList(self,repo)
        self.moduleFrame.add(self.moduleList)
        self.pack_start(self.moduleFrame,False)
        
        self.mUploadFrame=PageFrame(self, "Upload Module", IconStock.MODULE)
        self.mUploadbox = gtk.HBox()
        self.mUploadbox.set_border_width(10)
        self.mUpload_label = gtk.Label("Please choose the Module and click OK")
        self.mUpload_filechoose = gtk.FileChooserButton("Select Module", None)
        self.mUpload_filechoose.connect("file-set", self.moduleFileChosen)
        self.mUpload_filechoose.set_size_request(200,30)
        self.mUpload_enter = gtk.Button(stock=gtk.STOCK_OK)
        self.mUpload_enter.connect("clicked", self.uploadModule)
        self.mUpload_dummy = gtk.Label("")
        self.mUploadbox.pack_start(self.mUpload_label,False)
        self.mUploadbox.pack_start(self.mUpload_filechoose,False)
        self.mUploadbox.pack_start(self.mUpload_enter,False)
        self.mUploadbox.pack_start(self.mUpload_dummy,True)
        self.mUploadFrame.add(self.mUploadbox)
        self.pack_start(self.mUploadFrame,False)
        
        self.templateFrame=PageFrame(self, "Templates", IconStock.TEMPLATE)
        self.templateVBox = gtk.VBox()
        self.templateButtonBox = gtk.HBox()
        self.templateDeleteButton = gtk.Button(stock=gtk.STOCK_DELETE)
        self.templateDummy = gtk.Label("")
        self.templateList = TemplateList(self,repo)
        self.templateVBox.pack_start(self.templateList,True)
        self.templateVBox.pack_start(self.templateButtonBox,False)
        self.templateButtonBox.pack_start(self.templateDummy,True)
        self.templateButtonBox.pack_start(self.templateDeleteButton,False)
        self.templateDeleteButton.connect("clicked",self.cb_DeleteTemplate)
        self.templateFrame.add(self.templateVBox)
        self.pack_start(self.templateFrame,False)
        
        self.tUploadFrame=PageFrame(self, "Upload Template", IconStock.TEMPLATE)
        self.tUploadbox = gtk.HBox()
        self.tUploadbox.set_border_width(10)
        self.tUpload_label = gtk.Label("Please choose the Template and click OK")
        self.tUpload_filechoose = gtk.FileChooserButton("Select Template", None)
        self.tUpload_filechoose.connect("file-set", self.templateFileChosen)
        self.tUpload_filechoose.set_size_request(200,30)
        self.tUpload_enter = gtk.Button(stock=gtk.STOCK_OK)
        self.tUpload_enter.connect("clicked", self.uploadTemplate)
        self.tUpload_dummy = gtk.Label("")
        self.tUploadbox.pack_start(self.tUpload_label,False)
        self.tUploadbox.pack_start(self.tUpload_filechoose,False)
        self.tUploadbox.pack_start(self.tUpload_enter,False)
        self.tUploadbox.pack_start(self.tUpload_dummy,True)
        self.tUploadFrame.add(self.tUploadbox)
        self.pack_start(self.tUploadFrame,False)

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
        self.developerNameEntry = DefaultEntry(default_message="nickname")
        self.developerFullnameEntry = DefaultEntry(default_message="Firstname Lastname")
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
    
    def render(self):
        repo = self.getMyObject()
        if not repo:
            return

        auth = repo.isAuthenticated()

        self.adminFrame.set_visible(auth)
        self.developerFrame.set_visible(auth)
        self.templateDeleteButton.set_visible(auth)
        self.moduleList.render()
        self.developerList.render()
    
    def cb_ChangePassword(self, widget=None, data=None):
        pw1 = self.adminPasswordEntry.get_text()
        pw2 = self.adminRepeatEntry.get_text()
        if pw1 == pw2:
            repo = self.getMyObject()
            repo.changePassword(pw1)
        else:
            pass #TODO: Implement error behaviour

    def cb_DeleteTemplate(self,widget=None,data=None): 
        def execute():
            repo = self.getMyObject()
            repo.deleteTemplate(self.templateToDelete)
            self.templateToDelete = None
        
        selection = self.templateList.treeview.get_selection()
        rowiter = selection.get_selected()[1]
        nr = self.templateList.store.get_value(rowiter,4)
        self.templateToDelete = nr
        YesNoPage(self.getApplication().getMainWindow(), "Do you really want to delete this Template from the Repository?", execute)



    def cb_Add(self,widget=None,data=None):
        name = self.developerNameEntry.get_text()
        fullName = self.developerFullnameEntry.get_text()
        textBuffer = self.developerPublicKeyEntry.get_buffer()
        publicKey = textBuffer.get_text(textBuffer.get_start_iter(),textBuffer.get_end_iter())
        
        repo = self.getMyObject()
        if not repo:
            return
        repo.registerDeveloper(name,fullName,publicKey)
        
    
    def moduleFileChosen(self, widget=None, data=None):
        self.moduleFileToUpload = widget.get_filename()
    
    def templateFileChosen(self, widget=None, data=None):
        self.templateFileToUpload = widget.get_filename()
    
    def uploadModule(self,widget=None,data=None):
        repo = self.getMyObject()
        if not repo:
            return
        repo.uploadModule(self.moduleFileToUpload)
    
    def uploadTemplate(self,widget=None,data=None):
        repo = self.getMyObject()
        if not repo:
            return
        repo.uploadTemplate(self.templateFileToUpload)

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
        try:
            repo = self.getApplication().getLocalObjectById(self.repoId)
        except GenericObjectStoreException:
            self.destroy()
            return
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
        try:
            repo = self.getApplication().getLocalObjectById(self.repoId)
        except GenericObjectStoreException:
            self.destroy()
            return
        developers = repo.getDevelopers()
        
        self.store.clear()
        for developer in developers:
            self.store.append((IconStock.USER,developer['fullName']))
        
        
    def getPar(self):
        return self.par
    
    def getApplication(self):
        return self.getPar().getApplication()
        
class TemplateList(gtk.ScrolledWindow):
    def __init__(self, par, repo):
        self.par = par
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        
        self.treeview = gtk.TreeView()
        self.store= gtk.ListStore(gtk.gdk.Pixbuf, str, str, str, int)
        self.treeview.set_model(self.store)
        self.repoId = repo.getLocalId()
        
        self.col_name = gtk.TreeViewColumn("Template")
        self.col_description = gtk.TreeViewColumn("Description")
        self.col_author = gtk.TreeViewColumn("Author")
        self.ren_icon = gtk.CellRendererPixbuf()
        self.ren_name = gtk.CellRendererText()
        self.ren_description = gtk.CellRendererText()
        self.ren_author = gtk.CellRendererText()
        self.col_name.pack_start(self.ren_icon,False)
        self.col_name.pack_start(self.ren_name,False)
        self.col_description.pack_start(self.ren_description,True)
        self.col_author.pack_start(self.ren_author,False)
        self.col_name.add_attribute(self.ren_icon, 'pixbuf',0)
        self.col_name.add_attribute(self.ren_name, 'text', 1)
        self.col_description.add_attribute(self.ren_description, 'text', 2)
        self.col_author.add_attribute(self.ren_author, 'text', 3)
        self.treeview.append_column(self.col_name)
        self.treeview.append_column(self.col_description)
        self.treeview.append_column(self.col_author)
        self.add(self.treeview)
        
        repo.addCallback(self.render)
        self.show_all()
        self.render()
        
    def render(self):
        try:
            repo = self.getApplication().getLocalObjectById(self.repoId)
        except GenericObjectStoreException:
            self.destroy()
            return
        templates = repo.getTemplates()
        
        self.store.clear()
        for template in templates:
            self.store.append((IconStock.TEMPLATE,template['name'],template['description'],template['author'],template['id']))
            
    def getPar(self):
        return self.par
    
    def getApplication(self):
        return self.getPar().getApplication()
