#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import pygtk
pygtk.require("2.0")
import gtk

import IconStock

from data.Generic import GenericObjectStoreException

from glue.lng import _

class GenericPage(gtk.ScrolledWindow):
    """
    This Class defines a Page in the Skarphed Tab-Display
    """
    def __init__(self,par):
        gtk.ScrolledWindow.__init__(self)
        self.par = par
        self.vbox = gtk.VBox()
        
        self.add_with_viewport(self.vbox)

        #map the add-methods of vbox on this genericpage
        self.add = self.vbox.add
        self.pack_start = self.vbox.pack_start
        self.pack_end = self.vbox.pack_end

        #the page only scrolls if it outgrows the space that is there
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

    def __del__(self):
        self.getApplication().getObjectStore().removeCallback(self.render)

    def render(self):
        pass #to be overridden by descendants

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class ObjectPageAbstract(GenericPage):
    """
    This is a baseClass for displaying Pages that render objects
    """
    def __init__(self,par, obj):
        GenericPage.__init__(self, par)
        self.objId = obj.getLocalId()
        obj.addCallback(self.render)

    def getMyObject(self):
        try:
            obj = self.getApplication().getLocalObjectById(self.objId)
            return obj
        except GenericObjectStoreException:
            self.destroy()
            return False
        

class ObjectPage(ObjectPageAbstract):
    """
    This Class defines a Page in the Skarphed Tab-Display
    That simply displays an Object and its name

    Normally used as placeholder
    """
    def __init__(self,par, obj):
        ObjectPageAbstract.__init__(self, par, obj)
        self.labeltop = gtk.Label()

        self.labelbottom = gtk.Label(_("No further details"))
        self.add(self.labeltop)
        self.add(self.labelbottom)

        self.show_all()
        self.render()

    def render(self):
        obj = self.getMyObject()
        if not obj:
            self.destroy()
            return
        self.labeltop.set_text(obj.getName())

class FrameLabel(gtk.HBox):
    def __init__(self,parent, text, icon=None):
        self.par = parent
        gtk.HBox.__init__(self)
        self.set_spacing(10)

        assert type(text) in (str, unicode), "Text must be string"
        
        self.icon = gtk.Image()
        if icon is not None:
            self.icon.set_from_pixbuf(icon)
        self.label = gtk.Label()
        self.label.set_text(text)
        
        self.pack_start(self.icon,False)
        self.pack_start(self.label,True)
        self.show_all()
    
    def setText(self,text):
        self.label.set_text(text)

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()


class PageFrame(gtk.Frame):
    def __init__(self,parent, text, icon=None):
        gtk.Frame.__init__(self)
        self.set_border_width(10)
        self.set_label_widget(FrameLabel(self,text,icon))


class PageGenerator(object):
    def __init__(self,par,obj):
        self.obj = obj
        self.par = par
        
    def getInstanceOfObject(self,obj):
        try:
            while True:
                if hasattr(obj,'getInstanceType'):
                    return obj.getInstanceType()
                else:
                    obj = obj.getPar()
        except Exception,e:
            print type(e)
            return None
    
    def createPage(self):
        instanceType = self.getInstanceOfObject(self.obj)
        page = ObjectPage(self.par,self.obj)
        if instanceType is not None:
            try:
                exec "from "+instanceType.instanceTypeName+"."+self.obj.__class__.__name__+\
                 " import "+self.obj.__class__.__name__+"Page"
                exec "page = "+self.obj.__class__.__name__+"Page(self.par, self.obj)"            
            except ImportError:
                pass
        return page

class Tabs(gtk.Notebook):
    def __init__(self,parent):
        gtk.Notebook.__init__(self)
        self.par = parent
        self.pagestore = {}
        self.set_scrollable(True)
        self.connect("switch-page", self.pageSwitched)
        self.lastPageNum = None
        
    def openPage(self,obj,force=True):
        """
        opens a page that represents obj
        if force is True, there will be a page
        created if it does not exist
        """
        if not self.pagestore.has_key(obj.getLocalId()):
            if force:
                self.pagestore[obj.getLocalId()] = TabPage(self,obj)
                self.append_page(self.pagestore[obj.getLocalId()],TabLabel(self,obj))
                self.set_tab_reorderable(self.pagestore[obj.getLocalId()],True)
            else:
                return
        self.set_current_page(self.page_num(self.pagestore[obj.getLocalId()]))
        
        
    def closePage(self,objId):
        if self.pagestore.has_key(objId):
            self.remove_page(self.page_num(self.pagestore[objId]))
            del(self.pagestore[objId])

    def pageSwitched(self, note, page, page_num):
        if page_num != self.lastPageNum:
            page = self.get_nth_page(page_num)
            scvPage = page.get_children()[1]
            self.lastPageNum = page_num
            if hasattr(scvPage, "getMyObject"):
                obj = scvPage.getMyObject()
                self.getPar().getTree().setActiveObject(obj)

            
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
        try:
            obj = self.getApplication().getLocalObjectById(self.objId)
        except GenericObjectStoreException:
            self.getPar().closePage(self.objId)
            return
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
        self.body = PageGenerator(self,obj).createPage()
        self.brotkasten.pack_start(self.breadcrumbs,False)
        self.pack_start(self.brotkasten,False)
        self.pack_start(self.body,True)
        self.show_all()
        self.render()
        obj.addCallback(self.render)
        
    def render(self):
        try:
            self.getApplication().getObjectStore().getLocalObjectById(self.objId)
        except GenericObjectStoreException:
            #self.breadcrumbs.destroy()
            #self.body.destroy()
            #self.destroy()
            self.getPar().closePage(self.objId)
        else:
            self.breadcrumbs.render()
            self.body.render()
        #TODO: Implement
        
    def getObject(self):
        try:
            obj = self.getApplication().getLocalObjectById(self.objId)
            return obj
        except GenericObjectStoreException:
            self.getPar().closePage(self.objId)
            return None
    
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
        if obj is None:
            return
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
                sep = gtk.Label(" → ")
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
                crumbstring= obj.getName()+ " → "+crumbstring
            except Exception,e:
                crumbstring = "# "+crumbstring
                break
        self.set_text(crumbstring)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    