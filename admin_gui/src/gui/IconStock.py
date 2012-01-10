#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

import sys

PATH = sys.path[0]
print PATH
ADD                     = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/add.png",16,16)
CREDENTIAL              = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/credential.png",16,16)
CSS                     = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/css.png",16,16)
DELETE                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/delete.png",16,16)
ERROR                   = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/error.png",16,16)
MODULE_UPDATEABLE       = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/module_updateable.png",16,16)
MODULE                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/module.png",16,16)
OPERATION               = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/operation.png",16,16)
PERMISSION              = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/permission.png",16,16)
RELOAD                  = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/reload.png",16,16)
REPO                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/repo.png",16,16)
RETRY                   = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/retry.png",16,16)
ROLE                    = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/role.png",16,16)
SCOVILLE                = gtk.gdk.pixbuf_new_from_file_at_size(PATH+"/../data/icon/scoville.png",16,16)
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
                   "Server" : SERVER,
                   "Users"  : USER,
                   "User"   : USER
                   }

def getServerIcon(server):
    if server.isOnline():
        if server.getSSHState() == server.SSH_UNLOCKED and server.getSCVState() == server.SCV_UNLOCKED:
            return SERVER_ONLINE_SSH_SCV
        elif server.getSSHState() == server.SSH_UNLOCKED:
            return SERVER_ONLINE_SSH
        elif server.getSCVState() == server.SCV_UNLOCKED:
            return SERVER_ONLINE_SCV
        else:
            return SERVER_ONLINE
    return SERVER

def getAppropriateIcon(object):
    if object.__class__.__name__ == "Server":
        return getServerIcon(object)
    if icon_object_map.has_key(object.__class__.__name__):
        return icon_object_map[object.__class__.__name__]
    else:
        return SCOVILLE