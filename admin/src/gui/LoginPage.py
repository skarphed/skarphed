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
import hashlib

from gui.DefaultEntry import DefaultEntry

from glue.lng import _

class LoginPage(gtk.Frame):
    def __init__(self, parent):
        gtk.Frame.__init__(self, _("Scoville Admin Pro :: Login"))
        self.par = parent

        self.image = gtk.image_new_from_file("../data/loginbanner.png")
        self.alignment = gtk.Alignment(0.5,0.2,0.1,0.1)
        self.vbox = gtk.VBox()
        self.hbox = gtk.HBox(True)
        self.newprofile = NewProfile(self)
        self.useprofile = UseProfile(self)

        self.hbox.pack_start(self.useprofile)
        self.hbox.pack_start(self.newprofile)

        self.vbox.pack_start(self.image, False, False)
        self.vbox.pack_start(self.hbox)

        self.alignment.add(self.vbox)
        self.add(self.alignment)

        self.getPar().openDialogPane(self)

        self.useprofile.e_user.grab_focus()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()


class NewProfile(gtk.Frame):
    def __init__(self, parent):
        gtk.Frame.__init__(self, _("Create a new profile"))
        self.par=parent

        self.fixed = gtk.Fixed()
        
        self.l_user = gtk.Label(_("User"))
        self.e_user = DefaultEntry(default_message=_("username"))
        self.l_password = gtk.Label(_("Password"))
        self.e_password = gtk.Entry()
        self.l_password_r = gtk.Label (_("Repeat password"))
        self.e_password_r = gtk.Entry()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        
        self.e_password.set_invisible_char("●")
        self.e_password_r.set_invisible_char("●")
        self.e_password.set_visibility(False)
        self.e_password_r.set_visibility(False)
        
        self.fixed.put(self.l_user,10,10)
        self.fixed.put(self.e_user,110,10)
        self.fixed.put(self.l_password,10,35)
        self.fixed.put(self.e_password,110,35)
        self.fixed.put(self.l_password_r,10,60)
        self.fixed.put(self.e_password_r,110,60)
        self.fixed.put(self.ok,110,85)

        self.add(self.fixed)
        
        self.ok.connect("clicked", self.cb_OK)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
    def cb_OK(self,widget=None,data=None):
        pw1 = self.e_password.get_text()
        pw2 = self.e_password_r.get_text()
        username = self.e_user.get_text()
        if username and pw1 == pw2:
            try:
                hash = hashlib.md5()
                hash.update(pw1)
                self.getApplication().createProfile(username,hash.hexdigest())
                self.getApplication().getMainWindow().closeDialogPane()
            except Exception,e :
                raise e
            

class UseProfile(gtk.Frame):
    def __init__(self,parent):
        gtk.Frame.__init__(self, _("Login to profile"))
        self.par=parent
        
        self.fixed = gtk.Fixed()
        self.l_user = gtk.Label(_("User"))
        self.e_user = DefaultEntry(default_message=_("username"))
        self.l_password = gtk.Label(_("Password"))
        self.e_password = gtk.Entry()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        
        self.e_password.set_invisible_char("●")
        self.e_password.set_visibility(False)
        
        self.fixed.put(self.l_user,10,10)
        self.fixed.put(self.e_user,110,10)
        self.fixed.put(self.l_password,10,35)
        self.fixed.put(self.e_password,110,35)
        self.fixed.put(self.ok,110,60)

        self.add(self.fixed)
        
        self.ok.connect("clicked", self.cb_OK)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

    def cb_OK(self,widget=None,date=None):
        username=self.e_user.get_text()
        password=self.e_password.get_text()
        if username and password:
            try:
                hash = hashlib.md5()
                hash.update(password)
                self.getApplication().doLoginTry(username,hash.hexdigest())
            except Exception,e :
                raise e
            else:
                self.getPar().destroy()
            self.getApplication().getMainWindow().closeDialogPane()
