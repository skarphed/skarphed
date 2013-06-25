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

from glue.paths import ICON

#LOGO                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/mp_logo.png",16,16)

ACTION                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/action.png",16,16)
ACTIONLIST              = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/actionlist.png",16,16)
ADD                     = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/add.png",16,16)
CREDENTIAL              = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/credential.png",16,16)
CSS                     = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/css.png",16,16)
DATABASE                = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/database.png",16,16)
DELETE                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/delete.png",16,16)
ERROR                   = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/error.png",16,16)
JS_NO                   = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/js_no.png",16,16)
JS_SUPPORTED            = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/js_supported.png",16,16)
JS_MANDATORY            = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/js_mandatory.png",16,16)
MENU                    = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/menu.png",16,16)
MENUITEM                = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/menuitem.png",16,16)
MODULE_UPDATEABLE       = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/module_updateable.png",16,16)
MODULE                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/module.png",16,16)
OPERATION               = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/operation.png",16,16)
PERMISSION              = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/permission.png",16,16)
RELOAD                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/reload.png",16,16)
REPO                    = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/repo.png",16,16)
RETRY                   = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/retry.png",16,16)
ROLE                    = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/role.png",16,16)
SCHEMA                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/schema.png",16,16)
SKARPHED                = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/mp_logo.png",16,16)
SERVER_INVALID          = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/server_invalid.png",16,16) #DEPRECATED
SERVER_LOCKED           = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/server_locked.png",16,16) #DEPRECATED
SERVER                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/server.png",16,16)
SERVER_ONLINE           = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/server_online.png",16,16)
SERVER_ONLINE_SSH       = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/server_online_ssh.png",16,16)
SERVER_ONLINE_SCV       = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/server_online_scv.png",16,16)
SERVER_ONLINE_SSH_SCV   = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/server_online_ssh_scv.png",16,16)
SITE                    = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/site.png",16,16)
SPACE                   = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/space.png",16,16)
TEMPLATE                = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/template.png",16,16)
UPDATE                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/update.png",16,16)
USER                    = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/user.png",16,16)
USER_CURRENT            = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/user_current.png",16,16)
USER_ROOT               = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/user_root.png",16,16)
VIEW                    = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/view.png",16,16)
WEB                     = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/web.png",16,16)
WIDGET                  = gtk.gdk.pixbuf_new_from_file_at_size(ICON+"/widget.png",16,16)


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
                   "Skarphed_repo"    : REPO,
                   "Template"         : TEMPLATE,
                   "Widget"           : WIDGET,
                   "Action"           : ACTION,
                   "ActionList"       : ACTIONLIST,
                   "Menu"             : MENU,
                   "MenuItem"         : MENUITEM,
                   "Database"         : DATABASE,
                   "Schema"           : SCHEMA,
                   "View"             : VIEW,
                   "Views"            : VIEW  
                   }

def getServerIcon(server):
    if server.getSSHState() == server.SSH_UNLOCKED:
        return SERVER_ONLINE
    return SERVER

def getModuleIcon(module):
    if module.isUpdateable():
        return MODULE_UPDATEABLE
    else:
        return MODULE

def getUserIcon(user):
    if user.getName() == user.getUsers().getSkarphed().getUsername():
        return USER_CURRENT
    if user.getName() == 'root':
        return USER_ROOT
    return USER

def getAppropriateIcon(obj):
    if obj.__class__.__name__ == "Server":
        return getServerIcon(obj)
    if obj.__class__.__name__ == "Module":
        return getModuleIcon(obj)
    if obj.__class__.__name__ == "User":
        return getUserIcon(obj)
    if icon_object_map.has_key(obj.__class__.__name__):
        return icon_object_map[obj.__class__.__name__]
    else:
        return SKARPHED