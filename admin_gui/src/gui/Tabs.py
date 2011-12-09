#!/usr/bin/python
#-*- coding: utf-8 -*-

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
        
    def openPage(self,object):
        if self.pagestore.has_key(object.getLocalId()):
            self.set_current_page(self.page_num(self.pagestore[object.getLocalId()]))
        else:
            self.pagestore[object.getLocalId()] = TabPage(self,object)
            self.append_page(self.pagestore[object.getLocalId()],TabLabel(self,object))
            self.set_tab_reorderable(self.pagestore[object.getLocalId()],True)
    
    def closePage(self,object):
        if self.pagestore.has_key(object.getLocalId()):
            self.remove_page(self.page_num(self.pagestore[object.getLocalId()]))
            
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class TabLabel(gtk.HBox):
    def __init__(self,parent, object):
        gtk.HBox.__init__(self)
        self.par = parent
        self.object = object
        self.icon = gtk.Image()
        self.label = gtk.Label()
        self.close = gtk.Button("X")
        self.close.connect("clicked", self.cb_Close)
        self.pack_start(self.icon,False)
        self.pack_start(self.label,True)
        self.pack_end(self.close,False)
        self.show_all()
        self.render()
        self.object.addCallback(self.render)
        
    def render(self):
        self.icon.set_from_pixbuf(IconStock.getAppropriateIcon(self.object))
        self.label.set_text(self.object.getName())
        
    def cb_Close(self,widget=None,data=None):
        self.getPar().closePage(self.object)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
class TabPage(gtk.VBox):
    def __init__(self,parent, object):
        gtk.VBox.__init__(self)
        self.par = parent
        self.object = object
        self.brotkasten = gtk.HBox()
        self.breadcrumbs = BreadCrumbs(self)
        self.body = obj_pages.generatePageForObject(self,object)
        self.brotkasten.pack_start(self.breadcrumbs,False)
        self.pack_start(self.brotkasten,False)
        self.pack_start(self.body,True)
        self.show_all()
        self.render()
        self.object.addCallback(self.render)
        
    def render(self):
        self.breadcrumbs.render()
        self.body.render()
        #TODO: Implement
        
    def getObject(self):
        return self.object
    
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
        object = self.par.getObject()
        crumbstring = object.getName()
        while True:
            try:
                object = object.getPar()
                object.addCallback(self.render)
                crumbstring= object.getName()+ " > "+crumbstring
            except Exception,e:
                crumbstring = "# "+crumbstring
                break
        self.set_text(crumbstring)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    