#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################


import pygtk
pygtk.require("2.0")
import gtk

from GenericObject import ObjectPageAbstract
from GenericObject import PageFrame

from gui.OperationTool import OperationTool
import gui.IconStock

from glue.lng import _
from common.enums import JSMandatory

class ModulesPage(ObjectPageAbstract):
    def __init__(self,parent,modules):
        ObjectPageAbstract.__init__(self,parent,modules)
        
        self.info = PageFrame(self,_("Information"), gui.IconStock.REPO)
        self.infobox = gtk.VBox()
        self.info_table = gtk.Table(2,2,False)
        self.info_labelName = gtk.Label(_("Name:"))
        self.info_labelHost = gtk.Label(_("Host:"))
        self.info_displayName = gtk.Label()
        self.info_displayHost = gtk.Label()
        self.info_table.attach(self.info_labelName,0,1,0,1)
        self.info_table.attach(self.info_displayName,1,2,0,1)
        self.info_table.attach(self.info_labelHost,0,1,1,2)
        self.info_table.attach(self.info_displayHost,1,2,1,2)
        self.infobox.pack_start(self.info_table,False)
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.mod = PageFrame(self,_("Available and installed modules"), gui.IconStock.MODULE)
        self.modbox = gtk.Table(5,2,False)
        self.modbox.set_row_spacings(10)
        self.modbox.set_col_spacings(10)
        self.modbox.set_border_width(10)
        
        self.mod_label = gtk.Label(_("Please drag a module into the opposing list to install/uninstall it:\n"))
        self.mod_norepo_label = gtk.Label(_("Repository not reachable"))
        self.mod_labelInstalled = gtk.Label(_("Installed modules"))
        self.mod_labelAvailable = gtk.Label(_("Available modules"))
        self.mod_labelProcessed = gtk.Label(_("Currently processed modules"))
        
        self.mod_IListScroll = gtk.ScrolledWindow()
        self.mod_IListScroll.set_size_request(200,250)
        self.mod_IListScroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.mod_IList = gtk.TreeView()
        self.mod_IListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, gtk.gdk.Pixbuf, int)
        self.mod_IList.set_model(self.mod_IListStore)
        self.mod_IList_col_module = gtk.TreeViewColumn(_('Modulename'))
        self.mod_IList_col_js = gtk.TreeViewColumn(_('JS'))
        self.mod_IList_ren_icon = gtk.CellRendererPixbuf()
        self.mod_IList_ren_name = gtk.CellRendererText()
        self.mod_IList_ren_js = gtk.CellRendererPixbuf()
        self.mod_IList.append_column(self.mod_IList_col_module)
        self.mod_IList.append_column(self.mod_IList_col_js)
        self.mod_IList_col_module.pack_start(self.mod_IList_ren_icon,False)
        self.mod_IList_col_module.pack_start(self.mod_IList_ren_name,True)
        self.mod_IList_col_js.pack_start(self.mod_IList_ren_js,False)
        self.mod_IList_col_module.add_attribute(self.mod_IList_ren_icon,'pixbuf',0)
        self.mod_IList_col_module.add_attribute(self.mod_IList_ren_name,'text',1)
        self.mod_IList_col_js.add_attribute(self.mod_IList_ren_js,'pixbuf',2)
        self.mod_IList_col_module.set_sort_column_id(1)
        self.mod_IListScroll.add(self.mod_IList)
        
        self.mod_AListScroll = gtk.ScrolledWindow()
        self.mod_AListScroll.set_size_request(200,250)
        self.mod_AListScroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)       
        self.mod_AList = gtk.TreeView()
        self.mod_AListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, gtk.gdk.Pixbuf, int)
        self.mod_AList.set_model(self.mod_AListStore)
        self.mod_AList_col_module = gtk.TreeViewColumn(_('Modulename'))
        self.mod_AList_col_js = gtk.TreeViewColumn(_('JS'))
        self.mod_AList_ren_icon = gtk.CellRendererPixbuf()
        self.mod_AList_ren_name = gtk.CellRendererText()
        self.mod_AList_ren_js = gtk.CellRendererPixbuf()
        self.mod_AList.append_column(self.mod_AList_col_module)
        self.mod_AList.append_column(self.mod_AList_col_js)
        self.mod_AList_col_module.pack_start(self.mod_AList_ren_icon,False)
        self.mod_AList_col_module.pack_start(self.mod_AList_ren_name,True)
        self.mod_AList_col_js.pack_start(self.mod_AList_ren_js,False)
        self.mod_AList_col_module.add_attribute(self.mod_AList_ren_icon,'pixbuf',0)
        self.mod_AList_col_module.add_attribute(self.mod_AList_ren_name,'text',1)
        self.mod_AList_col_js.add_attribute(self.mod_AList_ren_js,'pixbuf',2)
        self.mod_AList_col_module.set_sort_column_id(1)
        self.mod_AListScroll.add(self.mod_AList)
        
        self.mod_CList = OperationTool(self,modules.getSkarphed())
        
        self.modbox.attach(self.mod_label,0,2,0,1)
        self.modbox.attach(self.mod_labelInstalled,0,1,1,2)
        self.modbox.attach(self.mod_labelAvailable,1,2,1,2)
        self.modbox.attach(self.mod_IListScroll,0,1,2,3)
        self.modbox.attach(self.mod_AListScroll,1,2,2,3)
        self.modbox.attach(self.mod_labelProcessed,0,2,3,4)
        self.modbox.attach(self.mod_CList,0,2,4,5)
        
        self.mod_AList.enable_model_drag_dest([('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        self.mod_IList.enable_model_drag_dest([('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        self.mod_AList.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        self.mod_IList.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        
        self.mod_AList.connect("drag-data-received", self.aListReceiveCallback)
        self.mod_IList.connect("drag-data-received", self.iListReceiveCallback)
        self.mod_AList.connect("drag-data-get", self.aListGetDataCallback)
        self.mod_IList.connect("drag-data-get", self.iListGetDataCallback)
        self.mod_AList.set_name("AList")
        self.mod_IList.set_name("IList")
        
        self.mod.add(self.modbox)
        self.pack_start(self.mod,False)
        
        self.show_all()
        
        self.render()
        modules.getSkarphed().getOperationManager().addCallback(self.render)
        self.getApplication().getObjectStore().addCallback(self.render)
    
    def iListGetDataCallback(self, treeview, context, selection, info, timestamp):
        treeselection = treeview.get_selection()
        model, rowiter = treeselection.get_selected()
        text = model.get_value(rowiter, 3)
        selection.set('text/plain', 8, str(text))
    
    def aListGetDataCallback(self, treeview, context, selection, info, timestamp):
        treeselection = treeview.get_selection()
        model, rowiter = treeselection.get_selected()
        text = model.get_value(rowiter, 3)
        selection.set('text/plain', 8, str(text))
    
    def iListReceiveCallback(self, treeview, context, x, y, selection, info , timestamp):
        if context.get_source_widget().get_name() != "AList":
            return
        module = self.getApplication().getLocalObjectById(int(selection.data))
        modules = self.getMyObject()
        if not modules:
            return
        modules.invokeInstallModule(module)
    
    def aListReceiveCallback(self, treeview, context, x, y, selection, info , timestamp):
        if context.get_source_widget().get_name() != "IList":
            return
        module = self.getApplication().getLocalObjectById(int(selection.data))
        modules = self.getMyObject()
        if not modules:
            return
        modules.invokeUninstallModule(module)
    
    def getModuleIterById(self, moduleList, moduleId):
        def search(model, path, rowiter, moduleId):
            val = model.get_value(rowiter,3)
            if val == moduleId:
                model.tempiter = rowiter
        
        moduleList.tempiter = None
        moduleList.foreach(search, moduleId)
        rowiter=moduleList.tempiter
        if rowiter is not None:
            return rowiter
        else:
            return None
    
    def render(self):
        def search(model, path, rowiter, processed):
            val = model.get_value(rowiter,3)
            if val not in processed:
                model.itersToRemove.append(rowiter)
        
        js_iconmap = {
            JSMandatory.NO : gui.IconStock.JS_NO,
            JSMandatory.SUPPORTED : gui.IconStock.JS_SUPPORTED,
            JSMandatory.MANDATORY : gui.IconStock.JS_MANDATORY
        }

        modules = self.getMyObject()
        if not modules:
            self.destroy()
            return

        if modules.getRepoState():
            self.modbox.remove(self.mod_norepo_label)
            self.modbox.attach(self.mod_AListScroll,1,2,2,3)
        else:
            self.modbox.remove(self.mod_AListScroll)
            self.modbox.attach(self.mod_norepo_label,1,2,2,3)

        self.processedIListIds = []
        self.processedAListIds = []
        
        for module in modules.getAllModules():
            if module.data.has_key('installed') and module.data['installed'] == True:
                rowiter = self.getModuleIterById(self.mod_IListStore,module.getLocalId())
                if rowiter is None:
                    self.mod_IListStore.append((gui.IconStock.getAppropriateIcon(module), module.getName(), js_iconmap[module.getJSMandatory()], module.getLocalId() ))
                else:
                    self.mod_IListStore.set_value(rowiter,0,gui.IconStock.getAppropriateIcon(module))
                    self.mod_IListStore.set_value(rowiter,1,module.getName())
                    self.mod_IListStore.set_value(rowiter,2,js_iconmap[module.getJSMandatory()])
                self.processedIListIds.append(module.getLocalId())
            else:
                rowiter = self.getModuleIterById(self.mod_AListStore,module.getLocalId())
                if rowiter is None:
                    self.mod_AListStore.append((gui.IconStock.MODULE, module.getName(), js_iconmap[module.getJSMandatory()], module.getLocalId() ))
                else:
                    self.mod_AListStore.set_value(rowiter,0,gui.IconStock.getAppropriateIcon(module))
                    self.mod_IListStore.set_value(rowiter,1,module.getName())
                    self.mod_IListStore.set_value(rowiter,2,js_iconmap[module.getJSMandatory()])
                self.processedAListIds.append(module.getLocalId())
        
        self.mod_IListStore.itersToRemove = []
        self.mod_AListStore.itersToRemove = []
        self.mod_IListStore.foreach(search, self.processedIListIds)
        self.mod_AListStore.foreach(search, self.processedAListIds)
        
        for rowiter in self.mod_IListStore.itersToRemove:
            self.mod_IListStore.remove(rowiter)
        for rowiter in self.mod_AListStore.itersToRemove:
            self.mod_AListStore.remove(rowiter)
