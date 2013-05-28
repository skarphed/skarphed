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

from data.Generic import GenericObjectStoreException

from gui.ObjectCombo import ObjectCombo
from gui.Scoville.Menu import SpaceCombo

class ViewGenerationWidget(gtk.Frame):
    def __init__(self, par, widget):
        self.par = par
        gtk.Frame.__init__(self)
        self.widgetId = widget.getLocalId()
        self._change_for_render = False

        self.toggle = gtk.CheckButton("Automatically generate Views")
        self.set_label(self.toggle)

        self.table = gtk.Table(3,3,False)
        self.label_view = gtk.Label("Baseview:")
        self.label_space = gtk.Label("Targetspace:")
        self.combo_view = ObjectCombo(self, 
                                     "View",
                                     selectFirst=True,
                                     virtualRootObject=widget.getModule().getModules().getScoville())
        self.combo_space = SpaceCombo()
        self.savebutton = gtk.Button(stock=gtk.STOCK_SAVE)
        self.dummy = gtk.Label("")

        self.table.attach(self.label_view,0,1,0,1,gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK)
        self.table.attach(self.combo_view,1,2,0,1,gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK)
        self.table.attach(self.label_space,0,1,1,2,gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK)
        self.table.attach(self.combo_space,1,2,1,2,gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK)
        self.table.attach(self.savebutton,1,2,2,3,gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK)
        self.table.attach(self.dummy,2,3,0,3,gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND)

        self.combo_view.connect("changed", self.viewChangedCallback)
        self.savebutton.connect("clicked", self.saveCallback)
        self.toggle.connect("toggled", self.toggleCallback)

        self.add(self.table)

        widget.addCallback(self.render)

        self.render()

    def render(self):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
            return

        active = widget.isGeneratingViews()
        self._change_for_render = True
        self.toggle.set_active(active)
        self.combo_view.set_sensitive(active)
        self.combo_space.set_sensitive(active)
        self.savebutton.set_sensitive(active)

        if active:
            self.combo_view.setSelected(widget.getBaseview())
            self.combo_space.setSelected(widget.getBaseSpaceId())
        else:
            self.combo_view.setSelected(None)
            self.combo_space.setSelected(None)

    def toggleCallback(self, widget=None, data=None):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
            return

        if self._change_for_render:
            self._change_for_render = False
            return

        if not self.toggle.get_active():
            widget.deactivateGeneratingViews()

    def saveCallback(self, widget=None, data=None):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
            return

        widget.activateGeneratingViews(self.combo_view.getSelected(), self.combo_space.getSpaceId())

    def viewChangedCallback(self, widget=None, data=None):
        self.combo_space.destroy()
        view = self.cobo_view.getSelected()
        if view is None:
            return
        page = view.getPage()
        self.combo_space = SpaceCombo(page)
        self.table.attach(self.combo_space,1,2,1,2,gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK)


    def getApplication(self):
        return self.getPar().getApplication()

    def getPar(self):
        return self.par