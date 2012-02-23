#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk


from IconStock import SCOVILLE
from ViewPasswordButton import ViewPasswordButton
from  data.Server import DNSError

class InstanceWindow(gtk.Window):
    addWindowOpen=False
    def __init__(self,parent, server=None, instance = None):
        gtk.Window.__init__(self)
        self.par = parent
        self.server = server
        self.instance = instance
        self.instanceTypes = self.getApplication().getInstanceTypes()
        
        self.set_title("Scoville Admin PRO :: Configure Instance")
        self.vbox = gtk.VBox()
        self.label = gtk.Label("Please configure the Instance")
        self.vspace = gtk.Label("")
        self.vbox.pack_start(self.label,False)
        self.vbox.pack_start(self.vspace,True)
        
        self.table = gtk.Table(2,4,False)
        self.typeLabel = gtk.Label("InstanceType:")
        
        
        self.typeStore = gtk.ListStore(str)
        self.typeCombo = gtk.ComboBox(self.typeStore)
        self.typeRenderer = gtk.CellRendererText()
        self.typeCombo.pack_start(self.typeRenderer, True)
        self.typeCombo.add_attribute(self.typeRenderer, 'text', 0)  
        for instanceType in self.instanceTypes:
            self.typeStore.append((instanceType.displayName,))
        self.urlLabel = gtk.Label("URL:")
        self.urlEntry = gtk.Entry()
        self.userLabel = gtk.Label("Username:")
        self.userEntry = gtk.Entry()
        self.passLabel = gtk.Label("Password:")
        self.passEntry = gtk.Entry()
        self.passEntry.set_visibility(False)
        self.passEntry.set_invisible_char("●")
        self.table.attach(self.typeLabel,0,1,0,1)
        self.table.attach(self.typeCombo,1,2,0,1)
        self.table.attach(self.urlLabel,0,1,1,2)
        self.table.attach(self.urlEntry,1,2,1,2)
        self.table.attach(self.userLabel,0,1,2,3)
        self.table.attach(self.userEntry,1,2,2,3)
        self.table.attach(self.passLabel,0,1,3,4)
        self.table.attach(self.passEntry,1,2,3,4)
        self.vbox.pack_start(self.table,False)
        
        self.buttonBox = gtk.HBox()
        self.ok = gtk.Button(stock=gtk.STOCK_OK)
        self.cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.viewpass = ViewPasswordButton()
        self.viewpass.addEntry(self.passEntry)
        self.space = gtk.Label("")
        self.buttonBox.pack_start(self.space,True)
        self.buttonBox.pack_start(self.viewpass,False)
        self.buttonBox.pack_start(self.cancel,False)
        self.buttonBox.pack_start(self.ok,False)
        self.ok.connect("clicked",self.cb_Ok)
        self.cancel.connect("clicked",self.cb_Cancel)
        self.vbox.pack_start(self.buttonBox,False)
        
        self.add(self.vbox)
        self.show_all()
    
    def getInstanceType(self,text):
        for instanceType in self.instanceTypes:
            if instanceType.displayName == text:
                return instanceType
        return None
    
    def cb_Cancel(self, widget=None, data=None):
        self.destroy()    
    
    def cb_Ok (self, widget=None, data=None):
        def errorMessage(msgId):
            msgs = ("This URL cannot be resolved",
                    "VAGINA"
                    )
            dia = gtk.MessageDialog(parent=self.getPar().getPar(), flags=0, type=gtk.MESSAGE_WARNING, \
                                  buttons=gtk.BUTTONS_OK, message_format=msgs[msgId])
            dia.run()
            dia.destroy()
        
        url = self.urlEntry.get_text()
        if self.server is None:
            try:
                self.server = self.getApplication().createServerFromInstanceUrl(url)
            except DNSError:
                errorMessage(0)
                return
        
        selection = self.typeStore[self.typeCombo.get_active()][0]  
        instanceType = self.getInstanceType(selection)
        
        username = self.userEntry.get_text()
        password = self.passEntry.get_text()
        try:
            self.server.createInstance(instanceType, url, username, password)
        except None:
            return
        self.destroy()

        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    