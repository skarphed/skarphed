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

import obj_pages
import IconStock
    
class Tabs(gtk.Notebook):
    def __init__(self,parent):
        gtk.Notebook.__init__(self)
        self.par = parent
        self.pagestore = {}
        self.set_scrollable(True)
        
    def openPage(self,obj):
        if not self.pagestore.has_key(obj.getLocalId()):
            self.pagestore[obj.getLocalId()] = TabPage(self,obj)
            self.append_page(self.pagestore[obj.getLocalId()],TabLabel(self,obj))
            self.set_tab_reorderable(self.pagestore[obj.getLocalId()],True)
        self.set_current_page(self.page_num(self.pagestore[obj.getLocalId()]))
        
    def closePage(self,objId):
        if self.pagestore.has_key(objId):
            self.remove_page(self.page_num(self.pagestore[objId]))
            del(self.pagestore[objId])
            
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class TabLabel(gtk.HBox):
    def __init__(self,parent, obj):
        gtk.HBox.__init__(self)
        self.par = parent
        self.objId = obj.getLocalId()
        self.icon = gtk.Image()
        self.label = gtk.Label()
        self.close = gtk.Button("X")
        self.close.connect("clicked", self.cb_Close)
        self.pack_start(self.icon,False)
        self.pack_start(self.label,True)
        self.pack_end(self.close,False)
        self.show_all()
        self.render()
        obj.addCallback(self.render)
        
    def render(self):
        obj = self.getApplication().getLocalObjectById(self.objId)
        self.icon.set_from_pixbuf(IconStock.getAppropriateIcon(obj))
        self.label.set_text(obj.getName())
        
    def cb_Close(self,widget=None,data=None):
        self.getPar().closePage(self.objId)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
class TabPage(gtk.VBox):
    def __init__(self,parent, obj):
        gtk.VBox.__init__(self)
        self.par = parent
        self.objId = obj.getLocalId()
        self.brotkasten = gtk.HBox()
        self.breadcrumbs = ButtonBreadCrumbs(self)
        self.body = obj_pages.generatePageForObject(self,obj)
        self.brotkasten.pack_start(self.breadcrumbs,False)
        self.pack_start(self.brotkasten,False)
        self.pack_start(self.body,True)
        self.show_all()
        self.render()
        obj.addCallback(self.render)
        
    def render(self):
        try:
            self.getApplication().getObjectStore().getLocalObjectById(self.objId)
        except:
            self.breadcrumbs.destroy()
            self.body.destroy()
            self.destroy()
        else:
            self.breadcrumbs.render()
            self.body.render()
        #TODO: Implement
        
    def getObject(self):
        return self.getApplication().getLocalObjectById(self.objId)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class ButtonBreadCrumb(gtk.Button):
    def __init__(self,parent,obj):
        self.objId = obj.getLocalId()
        gtk.Button.__init__(self,obj.getName())
        self.par = parent
        self.image = gtk.Image()
        self.image.set_from_pixbuf(IconStock.getAppropriateIcon(obj))
        self.set_image(self.image)
        self.connect("clicked",self.cb_Click)
        
    def cb_Click(self,widget=None,data=None):
        obj = self.getApplication().getLocalObjectById(self.objId)
        self.getApplication().mainwin.tabs.openPage(obj)

    def getPar(self):
        return self.par

    def getApplication(self):
        
        return self.par.getApplication()

class ButtonBreadCrumbs(gtk.HBox):
    def __init__(self,parent):
        gtk.HBox.__init__(self)
        self.par = parent
        self.crumbs = []
        self.par.getObject().addCallback(self.render)
        
    def render(self):
        while len(self.crumbs) != 0:
            widget =self.crumbs.pop()
            self.remove(widget) 
            widget.destroy()
        obj = self.par.getObject()
        self.crumbs.append(gtk.Label(obj.getName()))
        while True:
            try:
                obj = obj.getPar()
                obj.addCallback(self.render)
                button = ButtonBreadCrumb(self,obj)
                self.crumbs.insert(0,button)
            except Exception,e:
                print e
                break
        separators = []
        for index,crumb in enumerate(self.crumbs,1):
            self.pack_start(crumb,True)
            if index != len(self.crumbs):
                sep = gtk.Label(" > ")
                separators.append(sep)
                self.pack_start(sep,False)
        self.crumbs.extend(separators)
        self.show_all()
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()


class BreadCrumbs(gtk.Label):
    def __init__(self,parent):
        gtk.Label.__init__(self)
        self.par = parent
        self.render()
        self.par.getObject().addCallback(self.render)
    
    def render(self):
        obj = self.par.getObject()
        crumbstring = obj.getName()
        while True:
            try:
                obj = object.getPar()
                obj.addCallback(self.render)
                crumbstring= obj.getName()+ " > "+crumbstring
            except Exception,e:
                crumbstring = "# "+crumbstring
                break
        self.set_text(crumbstring)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    