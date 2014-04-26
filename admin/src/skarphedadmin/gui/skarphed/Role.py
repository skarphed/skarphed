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
from skarphedadmin.gui import IconStock

from skarphedadmin.glue.lng import _

class RolePage(ObjectPageAbstract):
    def __init__(self,parent,role):
        ObjectPageAbstract.__init__(self,parent,role)
        self.roleId = role.getLocalId()
        role.fetchPermissions()
        
        self.headline = gtk.Label()
        self.pack_start(self.headline,False)
        
        self.info = PageFrame(self,_("Information"), IconStock.ROLE)
        self.infobox = gtk.VBox()
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.perm = PageFrame(self,_("Permissions"), IconStock.PERMISSION)
        self.permbox = gtk.Table(1,2,False)
        self.permbox.set_row_spacings(10)
        self.permbox.set_col_spacings(10)
        self.permbox.set_border_width(10)
        
        self.perm_permlabel = FrameLabel(self,_("Please choose the Permissions you want to assign to the user here:"), IconStock.PERMISSION)
        
        self.perm_permlistview = gtk.TreeView()
        self.perm_permlist = gtk.ListStore(int, str,str)
        self.perm_permlistview.set_model(self.perm_permlist)
        self.perm_permlist_col_checkbox = gtk.TreeViewColumn('')
        self.perm_permlist_col_identifier = gtk.TreeViewColumn(_('Permission Identifier'))
        self.perm_permlist_col_name = gtk.TreeViewColumn(_('Permission Name'))
        self.perm_permlistview.append_column(self.perm_permlist_col_checkbox)
        self.perm_permlistview.append_column(self.perm_permlist_col_identifier)
        self.perm_permlistview.append_column(self.perm_permlist_col_name)
        self.perm_permlist_renderer_checkbox= gtk.CellRendererToggle()
        self.perm_permlist_renderer_identifier = gtk.CellRendererText()
        self.perm_permlist_renderer_name = gtk.CellRendererText()
        
        self.perm_permlist_col_checkbox.pack_start(self.perm_permlist_renderer_checkbox)
        self.perm_permlist_col_identifier.pack_start(self.perm_permlist_renderer_identifier)
        self.perm_permlist_col_name.pack_start(self.perm_permlist_renderer_name)
        self.perm_permlist_col_checkbox.add_attribute(self.perm_permlist_renderer_checkbox,'active',0)
        self.perm_permlist_col_identifier.add_attribute(self.perm_permlist_renderer_identifier,'text',1)
        self.perm_permlist_col_name.add_attribute(self.perm_permlist_renderer_name,'text',2)
        self.perm_permlist_renderer_checkbox.set_activatable(True)
        self.perm_permlist_renderer_checkbox.connect("toggled",self.toggledRight)
        
        self.permbox.attach(self.perm_permlabel,0,1,0,1)
        self.permbox.attach(self.perm_permlistview,0,1,1,2)
        
        self.perm.add(self.permbox)
        self.pack_start(self.perm,False)
        
        self.show_all()
        
        self.render()
    
    def render(self):
        role = self.getMyObject()
        if not role:
            return

        self.headline.set_markup(_("<b>Edit Role: "+role.getName()+"</b>"))
        
        if role.permissiondata is not None:
            self.perm_permlist.clear()
            for permission in role.permissiondata:
                self.perm_permlist.append((int(permission['granted']),str(permission['right']),''))
        
    
    def toggledRight(self,renderer = None, path = None):
        rowiter = self.perm_permlist.get_iter(path)
        perm = self.perm_permlist.get_value(rowiter,1)
        val = 1-self.perm_permlist.get_value(rowiter,0)
        role = self.getApplication().getLocalObjectById(self.roleId)
        if val == 1:
            role.assignPermission(perm)
        else:
            role.removePermission(perm)  
