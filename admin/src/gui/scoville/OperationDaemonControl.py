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

from GenericObject import GenericObjectPage
from GenericObject import PageFrame
from GenericObject import FrameLabel
import gui.IconStock

class OperationDaemonControl(PageFrame):
    def __init__(self, par, opdaemon):
        PageFrame.__init__(self, par,"Operation Daemon",gui.IconStock.OPERATION)
        self.par = par

        self.operationdaemonId = opdaemon.getLocalId()

        self.opdLabel = gtk.Label("Control the status of the OperationDaemon here:")
        self.opdStatusLabel = gtk.Label("Current status:")
        self.opdStatusDisplay = gtk.Label("")
        self.opdStartButton = gtk.Button("Start")
        self.opdStopButton = gtk.Button("Stop")
        self.opdRestartButton = gtk.Button("Restart")
        self.opdRefreshButton = gtk.Button("Refresh")

        self.opdVBox = gtk.VBox()
        self.opdLabelBox = gtk.HBox()
        self.opdStatusBox = gtk.HBox()
        self.opdButtonBox = gtk.HBox()
        self.opdLabelBox.pack_start(self.opdLabel,False)
        self.opdStatusBox.pack_start(self.opdStatusLabel,False)
        self.opdStatusBox.pack_start(self.opdStatusDisplay,False)
        self.opdButtonBox.pack_start(self.opdStartButton,False)
        self.opdButtonBox.pack_start(self.opdStopButton,False)
        self.opdButtonBox.pack_start(self.opdRestartButton,False)
        self.opdButtonBox.pack_start(self.opdRefreshButton,False)
        self.opdVBox.pack_start(self.opdLabelBox,False)
        self.opdVBox.pack_start(self.opdStatusBox,False)
        self.opdVBox.pack_start(self.opdButtonBox,False)
        self.add(self.opdVBox)

        self.opdStartButton.connect("clicked",self.cb_op, "start")
        self.opdStopButton.connect("clicked",self.cb_op, "stop")
        self.opdRestartButton.connect("clicked",self.cb_op, "restart")
        self.opdRefreshButton.connect("clicked",self.cb_op, "refresh")


        self.render()
        opdaemon.addCallback(self.render)

    def cb_op(self, widget=None, data=None):
        opdaemon = self.getApplication().getLocalObjectById(self.operationdaemonId)
        if data == "start":
            opdaemon.start()
        elif data == "stop":
            opdaemon.stop()
        elif data == "restart":
            opdaemon.restart()
        elif data == "refresh":
            opdaemon.refresh()

    def render(self):
        opdaemon = self.getApplication().getLocalObjectById(self.operationdaemonId)
        status = opdaemon.getStatus()
        if status:
            self.opdStatusDisplay.set_markup('<span color="#00ff00">Active</span>')
        else:
            self.opdStatusDisplay.set_markup('<span color="#ff0000">Inactive</span>')

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
