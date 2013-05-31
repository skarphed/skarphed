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

from glue.lng import _

class UserPage(ObjectPageAbstract):
    def __init__(self,par,user):
        ObjectPageAbstract.__init__(self,par,user)

        user.fetchRightsData()
        user.fetchRoleData()
        
        self.headline = gtk.Label()
        self.pack_start(self.headline,False)
        
        self.info = PageFrame(self,_("Information"), gui.IconStock.USER)
        self.infobox = gtk.VBox()
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.perm = PageFrame(self,_("Permissions / Roles"), gui.IconStock.ROLE)
        self.permbox = gtk.Table(2,2,False)
        self.permbox.set_row_spacings(10)
        self.permbox.set_col_spacings(10)
        self.permbox.set_border_width(10)
        
        self.perm_permlabel = FrameLabel(self,_("Please choose the Permissions you want to assign to the user here:"),gui.IconStock.PERMISSION)
        self.perm_rolelabel = FrameLabel(self,_("Please choose the Rights you want to assign to the user here:"),gui.IconStock.ROLE)
        
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
        
        self.perm_rolelistview = gtk.TreeView()
        self.perm_rolelist = gtk.ListStore(int, str,str,int)
        self.perm_rolelistview.set_model(self.perm_rolelist)
        self.perm_rolelist_col_checkbox = gtk.TreeViewColumn('')
        self.perm_rolelist_col_identifier = gtk.TreeViewColumn(_('Role Identifier'))
        self.perm_rolelist_col_name = gtk.TreeViewColumn(_('RoleName'))
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

        self.alterpw = PageFrame(self, _("Alter Password"), gui.IconStock.CREDENTIAL)
        self.alterpwhbox = gtk.HBox()
        self.alterpwdummy = gtk.Label("")
        self.alterpwbox = gtk.Table(2,4,False)
        self.alterpwbox.set_row_spacings(10)
        self.alterpwbox.set_col_spacings(10)
        self.alterpwbox.set_border_width(10)
        self.alterpw_oldpw_label = gtk.Label(_("Old Password:"))
        self.alterpw_newpw1_label = gtk.Label(_("New Password:"))
        self.alterpw_newpw2_label = gtk.Label(_("Repeat Password:"))
        self.alterpw_oldpw_entry = gtk.Entry()
        self.alterpw_oldpw_entry.set_invisible_char("●")
        self.alterpw_oldpw_entry.set_visibility(False)
        self.alterpw_newpw1_entry = gtk.Entry()
        self.alterpw_newpw1_entry.set_invisible_char("●")
        self.alterpw_newpw1_entry.set_visibility(False)
        self.alterpw_newpw2_entry = gtk.Entry()
        self.alterpw_newpw2_entry.set_invisible_char("●")
        self.alterpw_newpw2_entry.set_visibility(False)
        self.alterpw_ok = gtk.Button(_("Alter Password"))
        self.alterpwbox.attach(self.alterpw_oldpw_label,0,1,0,1)
        self.alterpwbox.attach(self.alterpw_oldpw_entry,1,2,0,1)
        self.alterpwbox.attach(self.alterpw_newpw1_label,0,1,1,2)
        self.alterpwbox.attach(self.alterpw_newpw1_entry,1,2,1,2)
        self.alterpwbox.attach(self.alterpw_newpw2_label,0,1,2,3)
        self.alterpwbox.attach(self.alterpw_newpw2_entry,1,2,2,3)
        self.alterpwbox.attach(self.alterpw_ok,1,2,3,4)
        self.alterpwhbox.pack_start(self.alterpwbox,False)
        self.alterpwhbox.pack_start(self.alterpwdummy,True)
        self.alterpw.add(self.alterpwhbox)
        self.alterpw_ok.connect("clicked", self.alterPassword)
        self.pack_start(self.alterpw,False)


        self.show_all()
        
        self.render()
        
    def render(self):
        user = self.getMyObject()
        if not user:
            return 

        self.headline.set_markup(_("<b>Settings for User: ")+user.getName()+"</b>")
        
        if user.permissiondata is not None:
            self.perm_permlist.clear()
            for permission in user.permissiondata:
                self.perm_permlist.append((int(permission['granted']),str(permission['right']),''))
        
        if user.roledata is not None:
            self.perm_rolelist.clear()
            for role in user.roledata:
                self.perm_rolelist.append((int(role['granted']), str(role['name']), '', role['id']))

        alter_pw_permitted = user.getUsers().getScoville().checkPermission("scoville.users.alter_password")
        is_active_user = user.getUsers().getScoville().getUsername() == user.getName()
        if alter_pw_permitted or is_active_user:
            self.alterpw.set_visible(True)
            self.alterpw_oldpw_entry.set_visible(is_active_user)
            self.alterpw_oldpw_label.set_visible(is_active_user)
        else:
            self.alterpw.set_visible(False)

    def alterPassword(self, widget=None, data=None):
        user = self.getMyObject()
        if not user:
            return 

        alter_pw_permitted = user.getUsers().getScoville().checkPermission("scoville.users.alter_password")
        is_active_user = user.getUsers().getScoville().getUsername() == user.getName()
        if alter_pw_permitted or is_active_user:
            if is_active_user:
                oldpw = self.alterpw_oldpw_entry.get_text()
            newpw1 = self.alterpw_newpw1_entry.get_text()
            newpw2 = self.alterpw_newpw2_entry.get_text()
            if newpw2 != newpw1:
                return False # Password repeat not successful
            if newpw1 == "":
                return False # New password is empty
            if is_active_user:
                user.alterPassword(newpw1,oldpw)
            else:
                user.alterPassword(newpw1)
    
    def toggledRole(self,render=None,path=None):
        rowiter = self.perm_rolelist.get_iter(path)
        roleId = self.perm_rolelist.get_value(rowiter,3)
        val = 1-self.perm_rolelist.get_value(rowiter,0)
        
        user = self.getMyObject()
        if not user:
            return 
        
        if val == 1:
            user.assignRole(roleId)
        else:
            user.removeRole(roleId)
    
    def toggledRight(self,render=None,path=None):
        rowiter = self.perm_permlist.get_iter(path)
        perm = self.perm_permlist.get_value(rowiter,1)
        val = 1-self.perm_permlist.get_value(rowiter,0)
        
        user = self.getMyObject()
        if not user:
            return 
        
        if val == 1:
            user.assignPermission(perm)
        else:
            user.removePermission(perm)  
