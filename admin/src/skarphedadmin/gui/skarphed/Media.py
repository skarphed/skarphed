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
from GenericObject import FrameLabel
from skarphedadmin.data.Generic import GenericObjectStoreException

from skarphedadmin.gui import IconStock

from skarphedadmin.glue.lng import _

from skarphedcommon.errors import BinaryException

class MediaPage(ObjectPageAbstract):
    def __init__(self, par, media):
        ObjectPageAbstract.__init__(self, par, media)

        self.media = PageFrame(self, _("Media"), IconStock.MEDIA)
        self.store = gtk.ListStore(bool, gtk.gdk.Pixbuf, str, str, str, int)
        self.view = gtk.TreeView()
        self.view.set_model(self.store)
        self.buttonbox = gtk.HBox()
        self.hidden_check = gtk.CheckButton(_("show hidden media"))
        self.upload_button = gtk.Button(_("upload media"))
        self.delete_button = gtk.Button(stock=gtk.STOCK_DELETE)
        self.view_scroll = gtk.ScrolledWindow()
        self.view_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    
        self.col_del = gtk.TreeViewColumn(_("Del"))
        self.col_name = gtk.TreeViewColumn(_("Name"))
        self.col_mime = gtk.TreeViewColumn(_("MIME-Type"))
        self.col_size = gtk.TreeViewColumn(_("Size"))
        self.ren_del = gtk.CellRendererToggle()
        self.ren_icon = gtk.CellRendererPixbuf()
        self.ren_name = gtk.CellRendererText()
        self.ren_mime = gtk.CellRendererText()
        self.ren_size = gtk.CellRendererText()
        
        self.col_del.pack_start(self.ren_del,False)
        self.col_name.pack_start(self.ren_icon,False)
        self.col_name.pack_start(self.ren_name,True)
        self.col_mime.pack_start(self.ren_mime,False)
        self.col_size.pack_start(self.ren_size,False)
        self.col_del.add_attribute(self.ren_del, 'toggle', 0)
        self.col_name.add_attribute(self.ren_icon, 'pixbuf', 1)
        self.col_name.add_attribute(self.ren_name, 'text', 2)
        self.col_mime.add_attribute(self.ren_mime, 'text', 3)
        self.col_size.add_attribute(self.ren_size, 'text', 4)
        
        self.view.append_column(self.col_del)
        self.view.append_column(self.col_name)
        self.view.append_column(self.col_mime)
        self.view.append_column(self.col_size)
        self.view_scroll.add(self.view)
        self.pack_start(self.view_scroll, True)

        self.upload_button.connect("clicked", self.upload_cb)
        self.delete_button.connect("clicked", self.delete_cb)
        
        self.buttonbox.pack_start(gtk.Label(),True)
        self.buttonbox.pack_start(self.upload_button, False)
        self.buttonbox.pack_start(self.delete_button, False)        
        self.pack_start(self.buttonbox,False)

        self.show_all()
        self.render()
        
    def render(self):
        def add(binary):
            print "adding"
            self.store.append((
                False,
                IconStock.BINARY,
                binary.getFilename(),
                binary.getMime(),
                binary.getSize(),
                binary.getId()))

        def search(model, path, rowiter):
            nr = model.get_value(rowiter, 4)
            binaryIds = [b.getId() for b in self.objectsToAllocate]
            if nr not in binaryIds:
                self.itersToRemove.append(rowiter)
            else:
                binary = None
                for obj in self.objectsToAllocate:
                    if obj.getId() == nr:
                        binary = obj
                model.set_value(rowiter,2, binary.getFilename())
                model.set_value(rowiter,3, binary.getMime())
                model.set_value(rowiter,4, binary.getSize())
                self.objectsToAllocate.remove(binary)

        media = self.getMyObject()

        self.objectsToAllocate = media.getBinaries()
        self.itersToRemove = []
        self.store.foreach(search)
        for binary in self.objectsToAllocate:
            add(binary)
        for rowiter in self.itersToRemove:
            self.store.remove(rowiter)
            

    def upload_cb(self, widget=None, data=None):
        pass

    def delete_cb(self, widget=None, data=None):
        pass
