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

from GenericObject import GenericObjectPage
from GenericObject import PageFrame
from GenericObject import FrameLabel

import gui.IconStock

class TemplatePage(GenericObjectPage):
    def __init__(self,parent,template):
        self.par = parent
        GenericObjectPage.__init__(self,parent,template)
        self.templateId = template.getLocalId()
        
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
        
        template.addCallback(self.render)
        self.show_all()
        self.render()
    
    def fileChosen(self, widget=None, data=None):
        self.fileToUpload = widget.get_filename()
    
    def uploadTemplate(self, widget=None, data=None):
        template = self.getApplication().getLocalObjectById(self.templateId)
        if self.fileToUpload is not None and self.fileToUpload != "":
            template.getScoville().uploadTemplate(self.fileToUpload)
        else:
            raise Exception("No File specified")
    
    def render(self):
        template = self.getApplication().getLocalObjectById(self.templateId)
        self.info_displayName.set_text(template.data['name'])
        self.info_displayDescription.set_text(template.data['description'])
        self.info_displayAuthor.set_text(template.data['author'])
        