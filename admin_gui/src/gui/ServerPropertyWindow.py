#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk


from IconStock import SCOVILLE
from ViewPasswordButton import ViewPasswordButton
from InstanceWindow import InstanceWindow

class ServerPropertyWindow(gtk.Window):
    addWindowOpen=False
    def __init__(self,parent, server=None):
        gtk.Window.__init__(self)
        self.par = parent
        self.server = None
        if server is None:
            if ServerPropertyWindow.addWindowOpen:
                self.destroy()
                return
            self.set_title("Scoville Admin Pro :: New Server")
            ServerPropertyWindow.addWindowOpen = True
        else:
            self.server = server
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
        
        if server is not None:
            self.instFrame = gtk.Frame("Instances")
            self.instFrameT = gtk.Table(2,4,False)
            self.instList = gtk.TreeView()
            self.instStore = gtk.ListStore(gtk.gdk.Pixbuf,str,int)
            self.instList.set_model(self.instStore)
            self.instAdd = gtk.Button(stock=gtk.STOCK_ADD)
            self.instRemove = gtk.Button(stock=gtk.STOCK_REMOVE)
            self.instEdit = gtk.Button(stock=gtk.STOCK_EDIT)
            self.instFrameT.attach(self.instList,0,1,0,4)
            self.instFrameT.attach(self.instAdd,1,2,0,1)
            self.instFrameT.attach(self.instRemove,1,2,1,2)
            self.instFrameT.attach(self.instEdit,1,2,2,3)
            self.instAdd.connect("clicked",self.cb_Add)
            self.instRemove.connect("clicked",self.cb_Remove)
            self.instEdit.connect("clicked",self.cb_Edit)
            self.instFrame.add(self.instFrameT)
            self.vbox.pack_start(self.instFrame,False)
        
        self.fill = gtk.Label("")
        self.vbox.pack_start(self.fill,True)
        
        self.buttons = gtk.HBox()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        self.cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.viewpass = ViewPasswordButton()
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
            self.sshFrame_NameEntry.set_text(server.getSSHName())
            self.sshFrame_PassEntry.set_text(server.getSSHPass())
            server.addCallback(self.render)
        self.show_all()
        
    
    def render(self):
        self.instStore.clear()
        for instance in self.server.getInstances():
            icon = SCOVILLE #TODO: Implement Icon
            self.instStore.append((icon,instance.getName(),instance.getLocalId()))
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
    def cb_Add(self,widget=None,data=None):
        InstanceWindow(self)
    
    def cb_Remove(self,widget=None,data=None):
        instance = self.getCurrentInstance()
        if instance is None:
            return
        self.server.removeInstance(instance)
    
    def cb_Edit(self,widget=None,data=None):
        instance = self.getCurrentInstance()
        if instance is None:
            return
        InstanceWindow(self,instance)
    
    def getCurrentInstance(self, onlyId):
        if self.server is None:
            return None
        selection = self.instList.get_selection()
        rowiter = selection.get_selected()[1]
        return self.getApplication().getLocalObjectById(self.instStore.get_value(rowiter,2))
         
    
    def cb_OK(self,widget=None,data=None):
        if self.server is None:
            server = self.getApplication().getData().createServer()
        else:
            server = self.server
        server.setIp(self.ipFrame_IPEntry.get_text())
        server.setSSHName(self.sshFrame_NameEntry.get_text())
        server.setSSHPass(self.sshFrame_PassEntry.get_text())
        server.load = server.LOADED_PROFILE
        server.establishConnections()
        
        if self.server is None:
            ServerPropertyWindow.addWindowOpen = False
        
        self.destroy()
    
    def cb_Cancel(self,widget=None,data=None):
        if self.server is None:
            ServerPropertyWindow.addWindowOpen = False
        self.destroy()
        