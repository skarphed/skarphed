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

class UserPage(GenericObjectPage):
    def __init__(self,parent,obj):
        GenericObjectPage.__init__(self,parent,object)
        self.user = obj
        self.user.fetchRightsData()
        self.user.fetchRoleData()
        
        self.headline = gtk.Label()
        self.pack_start(self.headline,False)
        
        self.info = PageFrame(self,"Information", gui.IconStock.USER)
        self.infobox = gtk.VBox()
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.perm = PageFrame(self,"Permissions / Roles", gui.IconStock.ROLE)
        self.permbox = gtk.Table(2,2,False)
        self.permbox.set_row_spacings(10)
        self.permbox.set_col_spacings(10)
        self.permbox.set_border_width(10)
        
        self.perm_permlabel = FrameLabel(self,"Please choose the Permissions you want to assign to the user here:",gui.IconStock.PERMISSION)
        self.perm_rolelabel = FrameLabel(self,"Please choose the Rights you want to assign to the user here:",gui.IconStock.ROLE)
        
        self.perm_permlistview = gtk.TreeView()
        self.perm_permlist = gtk.ListStore(int, str,str)
        self.perm_permlistview.set_model(self.perm_permlist)
        self.perm_permlist_col_checkbox = gtk.TreeViewColumn('')
        self.perm_permlist_col_identifier = gtk.TreeViewColumn('Permission Identifier')
        self.perm_permlist_col_name = gtk.TreeViewColumn('Permission Name')
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
        
        self.perm_rolelistview = gtk.TreeView()
        self.perm_rolelist = gtk.ListStore(int, str,str,int)
        self.perm_rolelistview.set_model(self.perm_rolelist)
        self.perm_rolelist_col_checkbox = gtk.TreeViewColumn('')
        self.perm_rolelist_col_identifier = gtk.TreeViewColumn('Permission Identifier')
        self.perm_rolelist_col_name = gtk.TreeViewColumn('Permission Name')
        self.perm_rolelistview.append_column(self.perm_rolelist_col_checkbox)
        self.perm_rolelistview.append_column(self.perm_rolelist_col_identifier)
        self.perm_rolelistview.append_column(self.perm_rolelist_col_name)
        self.perm_rolelist_renderer_checkbox= gtk.CellRendererToggle()
        self.perm_rolelist_renderer_identifier = gtk.CellRendererText()
        self.perm_rolelist_renderer_name = gtk.CellRendererText()
        
        self.perm_rolelist_col_checkbox.pack_start(self.perm_rolelist_renderer_checkbox)
        self.perm_rolelist_col_identifier.pack_start(self.perm_rolelist_renderer_identifier)
        self.perm_rolelist_col_name.pack_start(self.perm_rolelist_renderer_name)
        self.perm_rolelist_col_checkbox.add_attribute(self.perm_rolelist_renderer_checkbox,'active',0)
        self.perm_rolelist_col_identifier.add_attribute(self.perm_rolelist_renderer_identifier,'text',1)
        self.perm_rolelist_col_name.add_attribute(self.perm_rolelist_renderer_name,'text',2)
        self.perm_rolelist_renderer_checkbox.set_activatable(True)
        self.perm_rolelist_renderer_checkbox.connect("toggled",self.toggledRole)
        
        self.permbox.attach(self.perm_permlabel,0,1,0,1)
        self.permbox.attach(self.perm_permlistview,0,1,1,2)
        self.permbox.attach(self.perm_rolelabel,1,2,0,1)
        self.permbox.attach(self.perm_rolelistview,1,2,1,2)
        
        self.perm.add(self.permbox)
        self.pack_start(self.perm,False)
        
        self.show_all()
        
        self.render()
        obj.addCallback(self.render)
        
    def render(self):
        self.headline.set_markup("<b>Settings for User: "+self.user.getName()+"</b>")
        
        if self.user.permissiondata is not None:
            self.perm_permlist.clear()
            for permission in self.user.permissiondata:
                self.perm_permlist.append((int(permission['granted']),str(permission['right']),''))
        
        if self.user.roledata is not None:
            self.perm_rolelist.clear()
            for role in self.user.roledata:
                self.perm_rolelist.append((int(role['granted']), str(role['name']), '', role['id']))
    
    def toggledRole(self,render=None,path=None):
        iter = self.perm_rolelist.get_iter(path)
        id = self.perm_rolelist.get_value(iter,3)
        val = 1-self.perm_rolelist.get_value(iter,0)
        print val
        if val == 1:
            self.user.assignRole(id)
        else:
            self.user.removeRole(id)
    
    def toggledRight(self,render=None,path=None):
        iter = self.perm_permlist.get_iter(path)
        perm = self.perm_permlist.get_value(iter,1)
        val = 1-self.perm_permlist.get_value(iter,0)
        print val
        if val == 1:
            self.user.assignPermission(perm)
        else:
            self.user.removePermission(perm)  
