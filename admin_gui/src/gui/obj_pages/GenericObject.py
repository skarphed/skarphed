#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

class GenericObjectPage(gtk.VBox):
    def __init__(self,parent,object,iconstock=None):
        gtk.VBox.__init__(self,spacing = 10)
        self.par = parent
        
    def render(self):
        pass
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class PageFrame(gtk.Frame):
    def __init__(self,parent, text, icon=None):
        gtk.Frame.__init__(self)
        self.set_border_width(10)
        self.set_label_widget(FrameLabel(self,text,icon))
        
        

class FrameLabel(gtk.HBox):
    def __init__(self,parent, text, icon=None):
        self.par = parent
        gtk.HBox.__init__(self)
        assert type(text) == str, "text must be string"
        
        self.icon = gtk.Image()
        if icon is not None:
            self.icon.set_from_pixbuf(icon)
        self.label = gtk.Label()
        self.label.set_text(text)
        
        self.pack_start(self.icon,False)
        self.pack_start(self.label,True)
        self.show_all()
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

        
    
    
    