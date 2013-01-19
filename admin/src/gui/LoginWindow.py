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

class NewProfile(gtk.Fixed):
    def __init__(self,parent):
        gtk.Fixed.__init__(self)
        self.par=parent
        
        self.l_user = gtk.Label("user")
        self.e_user = gtk.Entry()
        self.l_password = gtk.Label("password")
        self.e_password = gtk.Entry()
        self.l_password_r = gtk.Label ("repeat password")
        self.e_password_r = gtk.Entry()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        
        self.e_password.set_invisible_char("●")
        self.e_password_r.set_invisible_char("●")
        self.e_password.set_visibility(False)
        self.e_password_r.set_visibility(False)
        
        
        self.put(self.l_user,10,10)
        self.put(self.e_user,110,10)
        self.put(self.l_password,10,35)
        self.put(self.e_password,110,35)
        self.put(self.l_password_r,10,60)
        self.put(self.e_password_r,110,60)
        self.put(self.ok,110,85)
        
        self.ok.connect("clicked", self.cb_OK)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
    def cb_OK(self,widget=None,data=None):
        pw1 = self.e_password.get_text()
        pw2 = self.e_password_r.get_text()
        if (pw1==pw2):
            username = self.e_user.get_text()
            try:
                hash = hashlib.md5()
                hash.update(pw1)
                self.getApplication().createProfile(username,hash.hexdigest())
            except Exception,e :
                raise e
            else:
                self.getPar().destroy()
            

class UseProfile(gtk.Fixed):
    def __init__(self,parent):
        gtk.Fixed.__init__(self)
        self.par=parent
        
        self.l_user = gtk.Label(u"user")
        self.e_user = gtk.Entry()
        self.l_password = gtk.Label(u"password")
        self.e_password = gtk.Entry()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        
        self.e_password.set_invisible_char("●")
        self.e_password.set_visibility(False)
        
        self.put(self.l_user,10,10)
        self.put(self.e_user,110,10)
        self.put(self.l_password,10,35)
        self.put(self.e_password,110,35)
        self.put(self.ok,110,60)
        
        self.ok.connect("clicked", self.cb_OK)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
    def cb_OK(self,widget=None,date=None):
        username=self.e_user.get_text()
        password=self.e_password.get_text()
        try:
            hash = hashlib.md5()
            hash.update(password)
            self.getApplication().doLoginTry(username,hash.hexdigest())
        except Exception,e :
            raise e
        else:
            self.getPar().destroy()

class LoginWindow(gtk.Window):
    def __init__(self,parent):
        gtk.Window.__init__(self)
        self.par = parent
        self.set_title("Scoville Admin Pro :: Login")
        self.set_icon_from_file("../data/icon/mp_logo.png")
        
        self.vbox = gtk.VBox()
        self.image = gtk.image_new_from_file("../data/login.png")
        self.notebook = gtk.Notebook()
        self.useprofile = UseProfile(self)
        self.newprofile = NewProfile(self)
        self.notebook.append_page(self.useprofile,gtk.Label("load profile"))
        self.notebook.append_page(self.newprofile,gtk.Label("create profile"))
        self.vbox.add(self.image)
        self.vbox.add(self.notebook)
        self.add(self.vbox)
        self.set_transient_for(self.getPar())
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        
        self.show_all()

        self.useprofile.e_user.grab_focus()
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
        