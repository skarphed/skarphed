#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from ViewPasswordButton import ViewPasswordButton


class ServerPropertyWindow(gtk.Window):
    addWindowOpen=False
    def __init__(self,parent, server=None):
        gtk.Window.__init__(self)
        self.par = parent
        
        if server is None:
            if ServerPropertyWindow.addWindowOpen:
                self.destroy()
                return
            self.set_title("Scoville Admin Pro :: New Server")
        else:
            self.set_title("Scoville Admin Pro :: Server Properties of "+server.getIp())
            
        self.vbox = gtk.VBox()
        
        self.instructionlabel = gtk.Label("Please enter the Server credentials")
        self.vbox.pack_start(self.instructionlabel,False)
        
        self.ipFrame = gtk.Frame("IP")
        self.ipFrameT = gtk.Table(2,1,False)
        self.ipFrame_IPLabel = gtk.Label("IP:")
        self.ipFrame_IPEntry = gtk.Entry()
        self.ipFrameT.attach(self.ipFrame_IPLabel, 0,1,0,1)
        self.ipFrameT.attach(self.ipFrame_IPEntry, 1,2,0,1)
        self.ipFrame.add(self.ipFrameT)
        self.vbox.pack_start(self.ipFrame,False)
        
        self.scvFrame = gtk.Frame("Scoville")
        self.scvFrameT = gtk.Table(2,2,False)
        self.scvFrame_NameLabel = gtk.Label("Username:")
        self.scvFrame_NameEntry = gtk.Entry()
        self.scvFrame_PassLabel = gtk.Label("Password:")
        self.scvFrame_PassEntry = gtk.Entry()
        self.scvFrame_PassEntry.set_visibility(False)
        self.scvFrame_PassEntry.set_invisible_char("●")
        self.scvFrameT.attach(self.scvFrame_NameLabel, 0,1,0,1)
        self.scvFrameT.attach(self.scvFrame_NameEntry, 1,2,0,1)
        self.scvFrameT.attach(self.scvFrame_PassLabel, 0,1,1,2)
        self.scvFrameT.attach(self.scvFrame_PassEntry, 1,2,1,2)
        self.scvFrame.add(self.scvFrameT)
        self.vbox.pack_start(self.scvFrame,False)
        
        self.sshFrame = gtk.Frame("SSH")
        self.sshFrameT = gtk.Table(2,2,False)
        self.sshFrame_NameLabel = gtk.Label("Username:")
        self.sshFrame_NameEntry = gtk.Entry()
        self.sshFrame_PassLabel = gtk.Label("Password:")
        self.sshFrame_PassEntry = gtk.Entry()
        self.sshFrame_PassEntry.set_visibility(False)
        self.sshFrame_PassEntry.set_invisible_char("●")
        self.sshFrameT.attach(self.sshFrame_NameLabel, 0,1,0,1)
        self.sshFrameT.attach(self.sshFrame_NameEntry, 1,2,0,1)
        self.sshFrameT.attach(self.sshFrame_PassLabel, 0,1,1,2)
        self.sshFrameT.attach(self.sshFrame_PassEntry, 1,2,1,2)
        self.sshFrame.add(self.sshFrameT)
        self.vbox.pack_start(self.sshFrame,False)
        
        self.fill = gtk.Label("")
        self.vbox.pack_start(self.fill,True)
        
        self.buttons = gtk.HBox()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        self.cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.viewpass = ViewPasswordButton()
        self.viewpass.addEntry(self.scvFrame_PassEntry)
        self.viewpass.addEntry(self.sshFrame_PassEntry)
        self.ok.connect("clicked", self.cb_OK)
        self.cancel.connect("clicked", self.cb_Cancel)
        self.buttons.pack_end(self.ok,False)
        self.buttons.pack_end(self.cancel,False)
        self.buttons.pack_end(self.viewpass,False)
        self.vbox.pack_start(self.buttons,False)
        
        self.add(self.vbox)
        
        self.set_transient_for(self.getPar())
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_border_width(10)
        self.set_size_request(500,600)
        
        if server is not None:
            self.ipFrame_IPEntry.set_text(server.getIp())
            self.scvFrame_NameEntry.set_text("SCVUSER")
            self.scvFrame_PassEntry.set_text("SCVPASS")
            self.sshFrame_NameEntry.set_text("SSHUSER")
            self.sshFrame_PassEntry.set_text("SSHPASS")
        
        self.show_all()
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
    def cb_OK(self,widget=None,data=None):
        pass
    
    def cb_Cancel(self,widget=None,data=None):
        pass
        