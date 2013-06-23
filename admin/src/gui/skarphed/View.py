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

from GenericObject import ObjectPageAbstract
from GenericObject import PageFrame
from GenericObject import FrameLabel
from data.Generic import GenericObjectStoreException

from gui.IconStock import WIDGET, SITE, VIEW, SPACE
from gui.ObjectCombo import ObjectCombo
from gui.DefaultEntry import DefaultEntry

from glue.lng import _

from common.errors import ViewException
from common.enums import BoxOrientation

class ViewPage(ObjectPageAbstract):
    def __init__(self, par, view):
        ObjectPageAbstract.__init__(self, par, view)

        self.view = PageFrame(self, _("View"), VIEW)
        self.view_hbox = gtk.HBox(spacing=10)
        self.view_label = gtk.Label(_("Name of this View: "))
        self.view_entry = DefaultEntry()
        self.view_entry.set_default_message(_("name_of_view"))
        self.view_hbox.pack_start(self.view_label,False)
        self.view_hbox.pack_start(self.view_entry,True)
        self.view.add(self.view_hbox)
        self.pack_start(self.view, False)

        self.page = PageFrame(self, _("Site"), SITE)
        self.page_hbox = gtk.HBox(spacing=10)
        self.page_label = gtk.Label(_("Site to Render: "))
        self.page_combobox = ObjectCombo(self, "Site", virtualRootObject=view.getViews().getSkarphed().getSites())
        self.page_hbox.pack_start(self.page_label,False)
        self.page_hbox.pack_start(self.page_combobox,False)
        self.page.add(self.page_hbox)
        self.pack_start(self.page,False)

        self.compose = PageFrame(self, _("Compositing"), WIDGET)
        self.compose_dummy = gtk.Label()
        self.compose_scroll = gtk.ScrolledWindow()
        self.compose_scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.compose_vbox = gtk.VBox(spacing=10)
        self.compose_vbox.set_border_width(10)
        self.compose_spacewidgets = {}
        self.compose_boxwidgets = {}
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
            
            boxes = site.getBoxes()
            processed_boxes =  []

            for spaceId, spaceName in spaces.items():
                if self.compose_spacewidgets.has_key(spaceId):
                    self.compose_spacewidgets[spaceId].render()
                else:
                    self.compose_spacewidgets[spaceId] = SpaceWidget(self,view,spaceId=spaceId)
                    self.compose_vbox.pack_start(self.compose_spacewidgets[spaceId],False)
                processed_spaces.append(spaceId)
            for spaceId in self.compose_spacewidgets.keys():
                if spaceId not in processed_spaces:
                    self.compose_spacewidgets[spaceId].destroy()

            for boxId, boxInfo in boxes.items():
                if self.compose_boxwidgets.has_key(boxId):
                    self.compose_boxwidgets[boxId].render()
                else:
                    self.compose_boxwidgets[boxId] = BoxWidget(self, boxId, view)
                    self.compose_vbox.pack_start(self.compose_boxwidgets[boxId],False)
                processed_boxes.append(boxId)
            for boxId in self.compose_boxwidgets.keys():
                if boxId not in processed_boxes:
                    self.compose_boxwidgets[boxId].destroy()

    def saveCallback(self, widget=None, data=None):
        try:
            view = self.getMyObject()
        except GenericObjectStoreException:
            return
        mapping = {}
        used_widgetIds = []
        for spacewidget in self.compose_spacewidgets.values():
            wgt = spacewidget.getWidget()
            if wgt is not None:
                widgetId = wgt.getId()
                if widgetId in used_widgetIds:
                    raise ViewException(ViewException.get_msg(8,wgt.getName()))
                mapping[spacewidget.getSpaceId()]= widgetId
                used_widgetIds.append(widgetId)
        view.setSpaceWidgetMapping(mapping)
        
        boxmapping = {}
        for boxwidget in self.compose_boxwidgets.values():
            widgets = boxwidget.getWidgets()
            for wgt in widgets:
                widgetId = wgt.getId()
                if widgetId in used_widgetIds:
                    raise ViewException(ViewException.get_msg(8,wgt.getName()))
                if not boxmapping.has_key(boxwidget.getBoxId()):
                    boxmapping[boxwidget.getBoxId()] = []
                boxmapping[boxwidget.getBoxId()].append(widgetId)
                used_widgetIds.append(widgetId)
        view.setBoxMapping(boxmapping)
            
    def changedPageCallback(self, widget=None, data=None):
        pass

class BoxWidget(gtk.VBox):
    def __init__(self, parent, boxId, view):
        gtk.VBox.__init__(self)

        self.par = parent
        self.boxId = int(boxId)
        self.viewId = view.getLocalId()

        self.label = gtk.Label()
        self.addButton = gtk.Button(stock=gtk.STOCK_ADD)
        self.scrolledWindow = gtk.ScrolledWindow()
        self.scrolledWindow.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.spaceList = gtk.VBox()
        self.boxSpaces = []

        self.addButton.connect("clicked", self.cb_Add)

        self.pack_start(self.label, False)
        self.pack_start(self.addButton, False)
        self.scrolledWindow.add_with_viewport(self.spaceList)
        self.pack_start(self.scrolledWindow,False)

        self.show_all()

    def render(self):
        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return

        box_name, box_orientation = view.getPage().getBox(self.boxId)
        if box_orientation == BoxOrientation.HORIZONTAL:
            self.label.set_text(_("Horizontal Box:")+" "+box_name)
        else:
            self.label.set_text(_("Vertical Box:")+" "+box_name)

        for boxSpaceWidget in self.boxSpaces:
            boxSpaceWidget.destroy()

        order = 0
        boxcontent = view.getBoxContent(self.boxId)
        for widgetId in boxcontent:
            self.boxSpaces.append(BoxSpace(self, view, self.boxId, order))
            self.spaceList.pack_start(self.boxSpaces[order],False)
            self.boxSpaces[order].show()
            self.boxSpaces[order].render()
            order += 1

    def cb_Add(self, widget=None, data=None):
        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return
        order = len(self.boxSpaces)
        boxcontent = view.getBoxContent(self.boxId)
        boxcontent.append(None)
        self.boxSpaces.append(BoxSpace(self, view, self.boxId, order))
        self.spaceList.pack_start(self.boxSpaces[order],False)
        self.boxSpaces[order].show()
        self.boxSpaces[order].render()


    def getWidgets(self):
        widgets = []
        for boxspace in self.boxSpaces:
            widget = boxspace.getWidget()
            if widget is not None:
                widgets.append(widget)
        return widgets

    def getBoxId(self):
        return self.boxId


    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class BoxSpace(gtk.HBox):
    def __init__(self, parent, view, boxId, orderNumber):
        gtk.HBox.__init__(self)

        self.par = parent
        self.viewId = view.getLocalId()
        self.boxId = boxId
        self.orderNumber = orderNumber

        self.spaceWidget = SpaceWidget(self, view, boxId=boxId, orderNumber=orderNumber)
        self.buttonhbox = gtk.VBox()
        self.raiseOrderButton = gtk.Button(stock=gtk.STOCK_GO_UP)
        self.removeButton = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.lowerOrderButton = gtk.Button(stock=gtk.STOCK_GO_DOWN)

        self.raiseOrderButton.connect("clicked", self.cb_raiseOrder)
        self.removeButton.connect("clicked", self.cb_remove)
        self.lowerOrderButton.connect("clicked", self.cb_lowerOrder)

        self.pack_start(self.spaceWidget,True)
        self.buttonhbox.pack_start(self.raiseOrderButton,True)
        self.buttonhbox.pack_start(self.removeButton,True)
        self.buttonhbox.pack_start(self.lowerOrderButton,True)
        self.pack_start(self.buttonhbox,False)
        self.show_all()


    def render(self):
        self.spaceWidget.render()

    def cb_remove(self, widget=None, data=None):
        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return

        boxcontent = view.getBoxContent(self.boxId)
        del(boxcontent[self.orderNumber])

        self.spaceWidget.destroy()
        self.destroy()

    def cb_raiseOrder(self, widget=None, data=None):
        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return

        boxcontent = view.getBoxContent(self.boxId)
        if self.orderNumber == 0:
            return
        widgetId = boxcontent[self.orderNumber]
        boxcontent.remove(widgetId)
        boxcontent.insert(self.orderNumber-1,widget_id)

        self.getPar().render()

    def cb_lowerOrder(self, widget=None, data=None):
        try:
            view = self.getApplication().getLocalObjectById(self.viewId)
        except GenericObjectStoreException:
            self.destroy()
            return

        boxcontent = view.getBoxContent(self.boxId)
        if self.orderNumber == len(boxcontent)-1:
            return
        widgetId = boxcontent[self.orderNumber]
        boxcontent.remove(widgetId)
        boxcontent.insert(self.orderNumber+1,widget_id)

        self.getPar().render()

    def getWidget(self):
        return self.spaceWidget.getWidget()

    def getWidgetId(self):
        return self.spaceWidget.getWidgetId()

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class SpaceWidget(gtk.Frame):
    def __init__(self, parent,  view, spaceId=None, boxId=None, orderNumber=None):
        gtk.Frame.__init__(self)

        self.par = parent
        self.viewId = view.getLocalId()
        self.spaceId = spaceId
        self.boxId = boxId
        self.orderNumber = orderNumber
        self.widgetId = None

        self.vbox = gtk.VBox()
        self.hbox = gtk.HBox(spacing=10)
        self.framelabel = FrameLabel(self,_("Space: "), SPACE)
        self.set_label_widget(self.framelabel)
        self.spacelabel = gtk.Label(_("Widget in this Space:"))

        self.widget_combo = ObjectCombo(self, "Widget", virtualRootObject=view.getViews().getSkarphed().getModules(), noneElement=True)
        self.expander = gtk.Expander()
        self.expander.set_label_widget(gtk.Label(_("Edit Widget Parameters")))
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
        if self.spaceId is not None: # In case, this space is a real space
            spaceName = site.getNameOfSpace(self.spaceId)
            self.framelabel.setText(_("Space: ")+spaceName)
            spaceWidgetMapping = view.getSpaceWidgetMapping()
            try:
                widgetId = spaceWidgetMapping[str(self.spaceId)]
            except KeyError:
                widget = None
                widgetId = None
            else:
                widget = view.getViews().getSkarphed().getModules().getWidgetById(widgetId)
        else: #In case this space is only part of a box
            self.framelabel.setText(_("BoxSpace"))
            boxmapping = view.getBoxContent(self.boxId)
            try:
                widgetId = boxmapping[self.orderNumber]
            except KeyError:
                widget = None
                widgetId = None
            else:
                widget = view.getViews().getSkarphed().getModules().getWidgetById(widgetId)

        self.widgetId = widgetId
        self.widget_combo.setSelected(widget)
        self.param_widget.setWidget(widget)
        self.param_widget.render()
    
    def getWidgetId(self):
        widget = self.widget_combo.getSelected()
        if widget is None:
            return None
        else:
            return widget.getId()

    def getWidget(self):
        widget = self.widget_combo.getSelected()
        if widget is None:
            return None
        else:
            return widget

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
        self.col_param = gtk.TreeViewColumn(_('Parameter'))
        self.col_value = gtk.TreeViewColumn(_('Value'))
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
