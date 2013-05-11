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

from GenericObject import ObjectPageAbstract
from GenericObject import PageFrame
from GenericObject import FrameLabel
from data.Generic import GenericObjectStoreException

from gui.IconStock import WIDGET, SITE, VIEW, SPACE
from gui.ObjectCombo import ObjectCombo
from gui.DefaultEntry import DefaultEntry


class ViewPage(ObjectPageAbstract):
    def __init__(self, par, view):
        ObjectPageAbstract.__init__(self, par, view)

        self.view = PageFrame(self, "View", VIEW)
        self.view_hbox = gtk.HBox(spacing=10)
        self.view_label = gtk.Label("Name of this View: ")
        self.view_entry = DefaultEntry()
        self.view_entry.set_default_message("name_of_view")
        self.view_hbox.pack_start(self.view_label,False)
        self.view_hbox.pack_start(self.view_entry,True)
        self.view.add(self.view_hbox)
        self.pack_start(self.view, False)

        self.page = PageFrame(self, "Site", SITE)
        self.page_hbox = gtk.HBox(spacing=10)
        self.page_label = gtk.Label("Site to Render: ")
        self.page_combobox = ObjectCombo(self, "Site", virtualRootObject=view.getViews().getScoville().getSites())
        self.page_hbox.pack_start(self.page_label,False)
        self.page_hbox.pack_start(self.page_combobox,False)
        self.page.add(self.page_hbox)
        self.pack_start(self.page,False)

        self.compose = PageFrame(self, "Compositing", WIDGET)
        self.compose_dummy = gtk.Label()
        self.compose_scroll = gtk.ScrolledWindow()
        self.compose_scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.compose_vbox = gtk.VBox(spacing=10)
        self.compose_vbox.set_border_width(10)
        self.compose_spacewidgets = {}
        self.compose_vbox.pack_end(self.compose_dummy,True)
        self.compose_scroll.add(self.compose_vbox)
        self.compose.add(self.compose_scroll)
        self.pack_start(self.compose, True)

        self.saveframe = gtk.HBox()
        self.savedummy = gtk.Label()
        self.savebutton = gtk.Button(stock=gtk.STOCK_SAVE)
        self.saveframe.pack_start(self.savedummy,True)
        self.saveframe.pack_start(self.savebutton,False)
        self.pack_start(self.saveframe, False)

        self.savebutton.connect("clicked", self.saveCallback)
        self.page_combobox.connect("changed", self.changedPageCallback)

        if not view.isFullyLoaded():
            view.loadFull()
        else:
            self.render()

    def render(self):
        view = self.getMyObject()
        if not view:
            return
            
        self.view_entry.set_text(view.data['name'])
        if view.data['default']:
            self.view_entry.set_sensitive(False)
        site = view.getPage()
        if site is not None:
            self.page_combobox.setSelected(site)
            spaces = site.getSpaces()
            processed_spaces = []
            for spaceId, spaceName in spaces.items():
                if self.compose_spacewidgets.has_key(spaceId):
                    self.compose_spacewidgets[spaceId].render()
                else:
                    self.compose_spacewidgets[spaceId] = SpaceWidget(self,spaceId,view)
                    self.compose_vbox.pack_start(self.compose_spacewidgets[spaceId],False)
                processed_spaces.append(spaceId)
            for spaceId in self.compose_spacewidgets.keys():
                if spaceId not in processed_spaces:
                    self.compose_spacewidgets[spaceId].destroy()

    def saveCallback(self, widget=None, data=None):
        try:
            view = self.getMyObject()
        except GenericObjectStoreException:
            return

        for spacewidget in self.compose_spacewidgets.values():
            widget = spacewidget.getWidgetCombo().getSelected()
            if (widget is None and spacewidget.getWidgetId() is None) or (widget is not None and widget.getId() == spacewidget.getWidgetId()):
                return
            if widget is not None:
                view.setWidgetIntoSpace(spacewidget.getSpaceId(), widget)
            else:
                view.removeWidgetFromSpace(spacewidget.getSpaceId())

    def changedPageCallback(self, widget=None, data=None):
        pass

class SpaceWidget(gtk.Frame):
    def __init__(self, parent, spaceid, view):
        gtk.Frame.__init__(self)

        self.par = parent
        self.viewId = view.getLocalId()
        self.spaceId = spaceid
        self.widgetId = None

        self.vbox = gtk.VBox()
        self.hbox = gtk.HBox(spacing=10)
        self.framelabel = FrameLabel(self,"Space: ", SPACE)
        self.set_label_widget(self.framelabel)
        self.spacelabel = gtk.Label("Widget in this Space:")

        self.widget_combo = ObjectCombo(self, "Widget", virtualRootObject=view.getViews().getScoville().getModules(), noneElement=True)
        self.expander = gtk.Expander()
        self.expander.set_label_widget(gtk.Label("Edit Widget Parameters"))
        self.param_widget = ParamWidget(self, view)
        self.expander.add(self.param_widget)
        self.hbox.pack_start(self.spacelabel,False)
        self.hbox.pack_start(self.widget_combo,False)
        self.vbox.pack_start(self.hbox,False)
        self.vbox.pack_start(self.expander,False)
        self.add(self.vbox)

        self.show_all()
        self.render()

    def render(self):
        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return
        site = view.getPage()
        spaceName = site.getNameOfSpace(self.spaceId)
        self.framelabel.setText("Space: "+spaceName)
        spaceWidgetMapping = view.getSpaceWidgetMapping()
        try:
            widgetId = spaceWidgetMapping[str(self.spaceId)]
        except KeyError:
            widget = None
            widgetId = None
        else:
            widget = view.getViews().getScoville().getModules().getWidgetById(widgetId)
        self.widgetId = widgetId
        self.widget_combo.setSelected(widget)
        self.param_widget.setWidget(widget)
        self.param_widget.render()
    
    def getWidgetId(self):
        return self.widgetId

    def getSpaceId(self):
        return self.spaceId

    def getWidgetCombo(self):
        return self.widget_combo

    def getSpaceId(self):
        return self.spaceId

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class ParamWidget(gtk.VBox):
    def __init__(self, parent, view, widget=None):
        gtk.VBox.__init__(self)
        self.par = parent
        self.viewId = view.getLocalId()
        self._firstRendered = False
        self.setWidget(widget)

        self.buttonHBox = gtk.HBox()
        self.addbutton = gtk.Button(stock=gtk.STOCK_ADD)
        self.rembutton = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.savebutton = gtk.Button(stock=gtk.STOCK_SAVE)

        self.liststore = gtk.ListStore(str,str,str)
        self.treeview = gtk.TreeView()
        self.treeview.set_model(self.liststore)
        self.col_param = gtk.TreeViewColumn('Parameter')
        self.col_value = gtk.TreeViewColumn('Value')
        self.treeview.append_column(self.col_param)
        self.treeview.append_column(self.col_value)
        self.ren_param = gtk.CellRendererText()
        self.ren_value = gtk.CellRendererText()
        self.col_param.pack_start(self.ren_param,False)
        self.col_value.pack_start(self.ren_value,False)
        self.col_param.add_attribute(self.ren_param,'text',0)
        self.col_value.add_attribute(self.ren_value,'text',1)
        self.ren_value.set_property('editable',True)
        self.ren_value.connect("edited", self.editedValueCallback)

        self.addbutton.set_sensitive(False)
        self.rembutton.set_sensitive(False)
        self.addbutton.connect("clicked", self.addParamCallback)
        self.rembutton.connect("clicked", self.removeParamCallback)
        self.savebutton.connect("clicked", self.saveCallback)
        self.buttonHBox.pack_start(self.addbutton,False)
        self.buttonHBox.pack_start(self.rembutton,False)
        self.buttonHBox.pack_start(self.savebutton,False)

        self.add(self.buttonHBox)
        self.add(self.treeview)

        self.render()

    def editedValueCallback(self, widget=None, path=None, newtext=None):
        rowiter = self.liststore.get_iter(path)
        typ = self.liststore.get_value(rowiter, 2)
        try:
            if typ == 'bool':
                newtext = bool(newtext)
            elif typ == 'int':
                newtext = int(newtext)
            elif typ == 'str':
                newtext = str(newtext)
            elif typ == 'float':
                newtext = float(newtext)
            else:
                raise ValueError()
        except ValueError:
            return
        else:
            self.liststore.set_value(rowiter,1,newtext)

    def removeParamCallback(self, widget=None, data=None):
        pass #TODO Implement when it's clear whether there can be userdefined params or not

    def addParamCallback(self, widget=None, data=None):
        pass #TODO Implement when it's clear whether there can be userdefined params or not

    def saveCallback(self, widget=None, data=None):
        def readValue(model, path, rowiter):
            par = model.get_value(rowiter,0)
            val = model.get_value(rowiter,1)
            typ = model.get_value(rowiter,2)
            if typ == 'bool':
                self.liststore.newWidgetParamMapping[par] = bool(val)
            elif typ == 'int':
                self.liststore.newWidgetParamMapping[par] = int(val)
            elif typ == 'str':
                self.liststore.newWidgetParamMapping[par] = str(val)
            elif typ == 'float':
                self.liststore.newWidgetParamMapping[par] = str(val)

            
        self.liststore.newWidgetParamMapping={}
        self.liststore.foreach(readValue)

        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return

        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
            return

        view.setWidgetParamMapping(widget, self.liststore.newWidgetParamMapping)


    def setWidget(self, widget):
        self.widgetId = None
        if widget is not None:
            self.widgetId = widget.getLocalId()
        if self._firstRendered:
            self.render()

    def render(self):
        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return

        self.liststore.clear()

        if self.widgetId is not None:
            try:
                widget = self.getApplication().getLocalObjectById(self.widgetId)
            except GenericObjectStoreException:
                return

            widgetParamMapping = view.getWidgetParamMapping(widget)
            
            for key, value in widgetParamMapping.items():
                self.liststore.append((key, str(value), str(type(value))))

        self._firstRendered = True

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
