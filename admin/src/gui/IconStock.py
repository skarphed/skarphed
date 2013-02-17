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

import sys

PATH = sys.path[0]
print PATH

#LOGO                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/mp_logo.png",16,16)

ACTION                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/action.png",16,16)
ACTIONLIST              = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/actionlist.png",16,16)
ADD                     = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/add.png",16,16)
CREDENTIAL              = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/credential.png",16,16)
CSS                     = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/css.png",16,16)
DATABASE                = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/database.png",16,16)
DELETE                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/delete.png",16,16)
ERROR                   = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/error.png",16,16)
MENU                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/menu.png",16,16)
MENUITEM                = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/menuitem.png",16,16)
MODULE_UPDATEABLE       = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/module_updateable.png",16,16)
MODULE                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/module.png",16,16)
OPERATION               = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/operation.png",16,16)
PERMISSION              = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/permission.png",16,16)
RELOAD                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/reload.png",16,16)
REPO                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/repo.png",16,16)
RETRY                   = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/retry.png",16,16)
ROLE                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/role.png",16,16)
SCHEMA                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/schema.png",16,16)
SCOVILLE                = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/mp_logo.png",16,16)
SERVER_INVALID          = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/server_invalid.png",16,16) #DEPRECATED
SERVER_LOCKED           = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/server_locked.png",16,16) #DEPRECATED
SERVER                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/server.png",16,16)
SERVER_ONLINE           = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/server_online.png",16,16)
SERVER_ONLINE_SSH       = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/server_online_ssh.png",16,16)
SERVER_ONLINE_SCV       = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/server_online_scv.png",16,16)
SERVER_ONLINE_SSH_SCV   = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/server_online_ssh_scv.png",16,16)
SITE                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/site.png",16,16)
TEMPLATE                = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/template.png",16,16)
USER                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/user.png",16,16)
WEB                     = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/web.png",16,16)
WIDGET                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/widget.png",16,16)


icon_object_map = {
                   "Server"           : SERVER,
                   "Users"            : USER,
                   "User"             : USER,
                   "Modules"          : MODULE,
                   "Module"           : MODULE,
                   "Roles"            : ROLE,
                   "Role"             : ROLE,
                   "Sites"            : SITE,
                   "Site"             : SITE,
                   "Repository"       : REPO,
                   "Scoville_repo"    : REPO,
                   "Template"         : TEMPLATE,
                   "Widget"           : WIDGET,
                   "Action"           : ACTION,
                   "ActionList"       : ACTIONLIST,
                   "Menu"             : MENU,
                   "MenuItem"         : MENUITEM,
                   "Database"         : DATABASE,
                   "Schema"           : SCHEMA   
                   }

def getServerIcon(server):
    
    if server.getSSHState() == server.SSH_UNLOCKED:
        return SERVER_ONLINE
    return SERVER

def getAppropriateIcon(object):
    if object.__class__.__name__ == "Server":
        return getServerIcon(object)
    if icon_object_map.has_key(object.__class__.__name__):
        return icon_object_map[object.__class__.__name__]
    else:
        return SCOVILLE