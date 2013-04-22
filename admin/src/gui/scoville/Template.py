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

from GenericObject import ObjectPageAbstract
from GenericObject import PageFrame
from GenericObject import FrameLabel

import gui.IconStock

class TemplatePageException(Exception): pass

class TemplatePage(ObjectPageAbstract):
    def __init__(self,parent,template):
        ObjectPageAbstract.__init__(self,parent,template)
        
        self.headline = gtk.Label()
        self.pack_start(self.headline,False)
        
        self.info = PageFrame(self,"Currently Installed", gui.IconStock.TEMPLATE)
        self.infobox = gtk.VBox()
        self.info_table = gtk.Table(2,3,False)
        self.info_labelName = gtk.Label("name:")
        self.info_labelDescription = gtk.Label("description:")
        self.info_labelAuthor = gtk.Label("author:")
        self.info_displayName = gtk.Label()
        self.info_displayDescription = gtk.Label()
        self.info_displayAuthor = gtk.Label()
        self.info_table.attach(self.info_labelName,0,1,0,1)
        self.info_table.attach(self.info_displayName,1,2,0,1)
        self.info_table.attach(self.info_labelDescription,0,1,1,2)
        self.info_table.attach(self.info_displayDescription,1,2,1,2)
        self.info_table.attach(self.info_labelAuthor,0,1,2,3)
        self.info_table.attach(self.info_displayAuthor,1,2,2,3)
        self.infobox.pack_start(self.info_table,False)
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.upload = PageFrame(self,"Upload new Template", gui.IconStock.TEMPLATE)
        self.uploadbox = gtk.HBox()
        self.uploadbox.set_border_width(10)
        self.upload_label = gtk.Label("Please choose the template and click OK")
        self.upload_filechoose = gtk.FileChooserButton("Select Template", None)
        self.upload_filechoose.connect("file-set", self.fileChosen)
        self.upload_filechoose.set_size_request(200,30)
        self.upload_enter = gtk.Button(stock=gtk.STOCK_OK)
        self.upload_enter.connect("clicked", self.uploadTemplate)
        self.upload_dummy = gtk.Label("")
        self.uploadbox.pack_start(self.upload_label,False)
        self.uploadbox.pack_start(self.upload_filechoose,False)
        self.uploadbox.pack_start(self.upload_enter,False)
        self.uploadbox.pack_start(self.upload_dummy,True)
        self.upload.add(self.uploadbox)
        self.pack_start(self.upload,False)
        
        self.repo = PageFrame(self,"Install Template from Repository", gui.IconStock.TEMPLATE)
        self.repoVBox = gtk.VBox()
        self.repoButtonbox = gtk.HBox()
        self.repoDummy = gtk.Label("")
        self.repoInstallButton = gtk.Button("Install")
        self.repoRefreshButton = gtk.Button(stock=gtk.STOCK_REFRESH)
        self.repostore = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str, int)
        self.repotree = gtk.TreeView()
        self.repotree.set_model(self.repostore)
        self.reposcroll = gtk.ScrolledWindow()
        self.reposcroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.repocol_name = gtk.TreeViewColumn("Template")
        self.repocol_description = gtk.TreeViewColumn("Description")
        self.repocol_author = gtk.TreeViewColumn("Author")
        self.reporen_icon = gtk.CellRendererPixbuf()
        self.reporen_name = gtk.CellRendererText()
        self.reporen_description = gtk.CellRendererText()
        self.reporen_author = gtk.CellRendererText()
        self.repocol_name.pack_start(self.reporen_icon,False)
        self.repocol_name.pack_start(self.reporen_name,False)
        self.repocol_description.pack_start(self.reporen_description,True)
        self.repocol_author.pack_start(self.reporen_author,False)
        self.repocol_name.add_attribute(self.reporen_icon,'pixbuf',0)
        self.repocol_name.add_attribute(self.reporen_name,'text',1)
        self.repocol_description.add_attribute(self.reporen_description,'text',2)
        self.repocol_author.add_attribute(self.reporen_author,'text',3)
        self.repotree.append_column(self.repocol_name)
        self.repotree.append_column(self.repocol_description)
        self.repotree.append_column(self.repocol_author)
        self.repotree.connect("row-activated",self.installRowCallback)
        self.reposcroll.add(self.repotree)
        self.repoButtonbox.pack_start(self.repoDummy,True)
        self.repoButtonbox.pack_start(self.repoRefreshButton,False)
        self.repoButtonbox.pack_start(self.repoInstallButton,False)
        self.repoVBox.pack_start(self.reposcroll,True)
        self.repoVBox.pack_start(self.repoButtonbox,False)
        self.repoRefreshButton.connect("clicked",self.refreshAvailableTemplates)
        self.repoInstallButton.connect("clicked",self.installButtonCallback)
        self.repo.add(self.repoVBox)
        self.pack_start(self.repo)

        self.show_all()
        self.render()
    
    def render(self):
        template = self.getMyObject()
        if not template:
            return

        self.info_displayName.set_text(template.data['name'])
        self.info_displayDescription.set_text(template.data['description'])
        self.info_displayAuthor.set_text(template.data['author'])

        self.repostore.clear()
        for available_template in template.getAvailableTemplates():
            self.repostore.append((gui.IconStock.TEMPLATE,
                                   available_template['name'],
                                   available_template['description'],
                                   available_template['author'],
                                   available_template['id']))
        
    def fileChosen(self, widget=None, data=None):
        self.fileToUpload = widget.get_filename()
    
    def uploadTemplate(self, widget=None, data=None):
        template = self.getMyObject()
        if not template:
            return

        if self.fileToUpload is not None and self.fileToUpload != "":
            template.getScoville().uploadTemplate(self.fileToUpload)
        else:
            raise Exception("No File specified")

    def installRowCallback(self,treeview=None,iter=None,path=None,data=None):
        template = self.getMyObject()
        if not template:
            return

        selection = self.repotree.get_selection()
        rowiter = selection.get_selected()[1]
        if rowiter is None:
            raise TemplatePageException("You must select a Template to install it")
        nr = self.repostore.get_value(rowiter,4)
        template.installFromRepo(nr)

    def installButtonCallback(self,widget=None,data=None):
        self.installRowCallback()

    def refreshAvailableTemplates(self,widget=None,data=None):
        template = self.getMyObject()
        if not template:
            return
        template.getRepoTemplates()