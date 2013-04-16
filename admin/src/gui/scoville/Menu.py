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
from gui import IconStock
pygtk.require("2.0")
import gtk

from GenericObject import GenericObjectPage
from GenericObject import PageFrame
from data.Generic import GenericObjectStoreException
from gui.ObjectCombo import ObjectCombo

class MenuPage(GenericObjectPage):
    def __init__(self, par, menu):
        GenericObjectPage.__init__(self,par,menu)
        self.par = par
        self.menuId = menu.getLocalId()
        
        self.info = PageFrame(self, "Name", IconStock.SITE)
        self.infobox = gtk.HBox()
        self.info_labelName = gtk.Label("Name:")
        self.info_entryName = gtk.Entry()
        self.info_saveName = gtk.Button(stock=gtk.STOCK_SAVE)
        self.infobox.pack_start(self.info_labelName,False)
        self.infobox.pack_start(self.info_entryName,True)
        self.infobox.pack_start(self.info_saveName,False)
        self.info_saveName.connect("clicked",self.renameCallback)
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.edit = PageFrame(self, "Edit Items", IconStock.MENU)
        self.editbox = gtk.HPaned()
        self.edit_left_box = gtk.VBox()
        self.edit_toolbar = gtk.Toolbar()
        
        self.addbutton=gtk.ToolButton()
        self.addbutton.set_stock_id(gtk.STOCK_ADD)
        self.addbutton.connect("clicked", self.cb_Add)
        self.removebutton=gtk.ToolButton()
        self.removebutton.set_stock_id(gtk.STOCK_REMOVE)
        self.removebutton.connect("clicked", self.cb_Remove)
        self.increasebutton=gtk.ToolButton()
        self.increasebutton.set_stock_id(gtk.STOCK_GO_UP)
        self.increasebutton.connect("clicked", self.cb_Increase)
        self.decreasebutton=gtk.ToolButton()
        self.decreasebutton.set_stock_id(gtk.STOCK_GO_DOWN)
        self.decreasebutton.connect("clicked", self.cb_Decrease)
        self.topbutton=gtk.ToolButton()
        self.topbutton.set_stock_id(gtk.STOCK_GOTO_TOP)
        self.topbutton.connect("clicked", self.cb_Top)
        self.bottombutton=gtk.ToolButton()
        self.bottombutton.set_stock_id(gtk.STOCK_GOTO_BOTTOM)
        self.bottombutton.connect("clicked", self.cb_Bottom)
        self.edit_toolbar.add(self.addbutton)
        self.edit_toolbar.add(self.removebutton)
        self.edit_toolbar.add(self.increasebutton)
        self.edit_toolbar.add(self.decreasebutton)
        self.edit_toolbar.add(self.topbutton)
        self.edit_toolbar.add(self.bottombutton)
        
        self.edit_menutree = MenuItemTree(self,menu)
        self.edit_right_box = gtk.Frame("ACTIONS")
        self.actionListItem = None
        self.edit_left_box.pack_start(self.edit_toolbar,False)
        self.edit_left_box.pack_start(self.edit_menutree,True)
        self.editbox.add(self.edit_left_box)
        self.editbox.add(self.edit_right_box)
        self.edit.add(self.editbox)
        self.pack_start(self.edit)
        
        self.edit_menutree.connect("cursor-changed",self.menuItemChangeCallback)
        
        menu.addCallback(self.render)
        self.show_all()
        
    
    def render(self):
        try:
            menu = self.getApplication().getLocalObjectById(self.menuId)
        except GenericObjectStoreException:
            self.destroy()
            return
        self.info_labelName.set_text(menu.getName())
    
    def renameCallback(self,widget=None,data=None):
        try:
            menu = self.getApplication().getLocalObjectById(self.menuId)
        except GenericObjectStoreException:
            self.destroy()
        else:
            menu.rename(self.info_entryName.get_text())
    
    def menuItemChangeCallback(self,*args,**kwargs):
        self.addbutton.set_sensitive(False)
        self.removebutton.set_sensitive(False)
        self.increasebutton.set_sensitive(False)
        self.decreasebutton.set_sensitive(False)
        self.topbutton.set_sensitive(False)
        self.bottombutton.set_sensitive(False)
        try:
            obj = self.edit_menutree.getSelectedMenuItem()
        except TypeError:
            return
        if obj.__class__.__name__ == 'MenuItem':
            self.addbutton.set_sensitive(True)
            self.removebutton.set_sensitive(True)
            self.increasebutton.set_sensitive(True)
            self.decreasebutton.set_sensitive(True)
            self.topbutton.set_sensitive(True)
            self.bottombutton.set_sensitive(True)
            self.showActionList(obj.getActionList())
        elif obj.__class__.__name__ == 'Menu':
            self.addbutton.set_sensitive(True)
        
    def cb_Add(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().createMenuItem()
    
    def cb_Remove(self,widget=None,data=None):
        item = self.edit_menutree.getSelectedMenuItem()
        item.getPar().deleteMenuItem(item)
    
    def cb_Increase(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().increaseOrder()
        
    def cb_Decrease(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().decreaseOrder()
    
    def cb_Top(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().moveToTop()
        
    def cb_Bottom(self,widget=None,data=None):
        self.edit_menutree.getSelectedMenuItem().moveToBottom()
    
    def showActionList(self,actionList):
        if self.actionListItem is not None:
            self.actionListItem.destroy()
        self.actionListItem = ActionListWidget(self,actionList)
        self.edit_right_box.add(self.actionListItem)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class ActionListWidget(gtk.ScrolledWindow):
    def __init__(self, par, actionList):
        self.par = par
        gtk.ScrolledWindow.__init__(self)
        self.actionListId = actionList.getLocalId()
        self.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
        
        self.container= None
        self.buttoncontainer = None
        
        actionList.addCallback(self.render)
        self.render()
    
    def render(self):
        def widgetSorter(x,y):
            x = self.getApplication().getLocalObjectById(x.actionId).getOrder()
            y = self.getApplication().getLocalObjectById(y.actionId).getOrder()
            if x>y:
                return 1
            else:
                return -1
        
        if self.container:
            self.container.destroy()
        if self.buttoncontainer:
            self.buttoncontainer.destroy()
        
        self.addbutton = gtk.Button(stock=gtk.STOCK_ADD)
        self.addbutton.connect("clicked", self.addCallback)
        self.container = gtk.VBox()
        self.buttoncontainer = gtk.VBox() 
        self.add_with_viewport(self.buttoncontainer)
        self.actionWidgets = []
        actionList = self.getApplication().getLocalObjectById(self.actionListId)
        for action in actionList.getActions():
            self.actionWidgets.append(ActionWidget(self,action))
        self.actionWidgets.sort(widgetSorter)
        for actionWidget in self.actionWidgets:
            self.container.pack_start(actionWidget,False)
        self.container.pack_start(gtk.Label(""),True)
        
        self.buttoncontainer.pack_start(self.container,True)
        self.buttoncontainer.pack_start(self.addbutton,False)
        self.show_all()
    
    def addCallback(self,widget=None,data=None):
        actionList = self.getApplication().getLocalObjectById(self.actionListId)
        actionList.addAction()
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()   
    
class ActionWidget(gtk.Expander):
    def __init__(self, par, action):
        gtk.Expander.__init__(self)
        self.par = par
        self.actionId = action.getLocalId()
        
        self.label = ActionWidgetLabel(self,action)
        self.set_label_widget(self.label)
        
        self.config = ActionWidgetConfig(self,action)
        self.add(self.config)
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()    
    
class ActionWidgetLabel(gtk.HBox):
    def __init__(self,par, action):
        gtk.HBox.__init__(self)
        self.par = par
        self.actionId = action.getLocalId()
        
        self.actionDisplay = gtk.Entry()
        self.pack_start(self.actionDisplay,True)
        action.addCallback(self.render)
        self.render()

    def render(self):
        try:
            action = self.getApplication().getLocalObjectById(self.actionId)
        except GenericObjectStoreException:
            self.getPar().destroy()
            return
        if action.data['type'] == 'url':
            self.actionDisplay.set_text('Goto URL: '+str(action.data['url']))
        elif action.data['type'] == 'widgetSpaceConstellation':
            self.actionDisplay.set_text('Move Widget '+str(action.data['widgetId'])+' into Space '+str(action.data['space']))
        elif action.data['type'] == 'site':
            self.actionDisplay.set_text('Goto Site '+str(action.data['siteId']))

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
class ActionWidgetConfig(gtk.Table):
    def __init__(self, par, action):
        self.par = par
        gtk.Table.__init__(self,4,4,False)
        self.actionId = action.getLocalId()
        
        self.radio_url = gtk.RadioButton(None, "URL:")
        self.radio_widgetSpaceConstellation = gtk.RadioButton(self.radio_url, "Widget into Space:")
        self.radio_site = gtk.RadioButton(self.radio_url, "Other Site:")
        
        spaceCount = action.getActionList().getMenuItem().getMenu().getSite().getSpaceCount()
        
        self.entry_url = gtk.Entry()
        self.entry_widget = ObjectCombo(self, 
                                     "Widget",
                                     selectFirst=True,
                                     virtualRootObject=action.getActionList().getMenuItem().getMenu().getSite().getScoville())
        self.entry_space = SpaceCombo(self,action.getActionList().getMenuItem().getMenu().getSite())
        self.entry_site = ObjectCombo(self, 
                                   "Site",
                                   selectFirst=True,
                                   virtualRootObject=action.getActionList().getMenuItem().getMenu().getSite().getScoville())
        self.entry_url.connect("focus-in-event",self.focusCallback)
        self.entry_widget.connect("popup",self.focusCallback)
        self.entry_widget.connect("changed",self.focusCallback)
        self.entry_space.connect("focus-in-event",self.focusCallback)
        self.entry_site.connect("popup",self.focusCallback)
        self.entry_widget.connect("changed",self.focusCallback)
        
        self.deleteButton = gtk.Button(stock=gtk.STOCK_DELETE)
        self.increaseOrderButton = gtk.Button(stock=gtk.STOCK_GO_UP)
        self.decreaseOrderButton = gtk.Button(stock=gtk.STOCK_GO_DOWN)
        self.saveButton = gtk.Button(stock=gtk.STOCK_SAVE)
        self.deleteButton.connect("clicked", self.deleteCallback)
        self.increaseOrderButton.connect("clicked", self.increaseOrderCallback)
        self.decreaseOrderButton.connect("clicked", self.decreaseOrderCallback)
        self.saveButton.connect("clicked", self.saveCallback)
        
        self.attach(self.radio_url,0,1,0,1)
        self.attach(self.entry_url,1,3,0,1)
        self.attach(self.radio_widgetSpaceConstellation,0,1,1,2)
        self.attach(self.entry_widget,1,2,1,2)
        self.attach(self.entry_space,2,3,1,2)
        self.attach(self.radio_site,0,1,2,3)
        self.attach(self.entry_site,1,3,2,3)
        self.attach(self.deleteButton,0,1,3,4)
        self.attach(self.increaseOrderButton,1,2,3,4)
        self.attach(self.decreaseOrderButton,2,3,3,4)
        self.attach(self.saveButton,3,4,3,4)
        action.addCallback(self.render)
        self.show_all()
        
        self.render()
        
    def render(self):
        try:
            action = self.getApplication().getLocalObjectById(self.actionId)
        except GenericObjectStoreException:
            self.getPar().destroy()
            return
        if action.data['type'] == 'url':
            self.radio_url.set_active(True)
            self.entry_url.set_text(action.data['url'])
        elif action.data['type'] == 'widgetSpaceConstellation':
            self.radio_widgetSpaceConstellation.set_active(True)
            widget=action.getWidget()
            space=action.getSpaceId()
            self.entry_space.setSpaceId(space)
            self.entry_widget.setSelected(widget)
        elif action.data['type'] == 'site':
            self.radio_site.set_active(True)
            site=action.getSite()
            self.entry_site.setSelected(site)
    
    def focusCallback(self,widget=None,event=None):
        if widget == self.entry_url:
            self.radio_url.activate()
        elif widget == self.entry_space or widget == self.entry_widget:
            self.radio_widgetSpaceConstellation.activate()
        elif widget == self.entry_site:
            self.radio_site.activate()
        
    
    def deleteCallback(self, widget=None, data=None):
        action = self.getApplication().getLocalObjectById(self.actionId)
        action.getPar().deleteAction(action)
    
    def increaseOrderCallback(self, widget=None, data=None):
        action = self.getApplication().getLocalObjectById(self.actionId)
        action.increaseOrder()
        
    def decreaseOrderCallback(self, widget=None, data=None):
        action = self.getApplication().getLocalObjectById(self.actionId)
        action.decreaseOrder()
        
    def saveCallback(self, widget=None,data=None):
        action = self.getApplication().getLocalObjectById(self.actionId)
        if self.radio_url.get_active():
            action.setUrl(self.entry_url.get_text())
        elif self.radio_widgetSpaceConstellation.get_active():
            widget = self.entry_widget.getSelected()
            action.setWidgetSpaceConstellation(widget.getLocalId(),self.entry_space.getSpaceId())
        elif self.radio_site.get_active():
            action.setSite(self.entry_site.getSelected().getId())
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()

class SpaceCombo(gtk.ComboBox):
    def __init__(self, par,page):
        self.par = par
        gtk.ComboBox.__init__(self)
        
        self.pageId = page.getLocalId()

        self.store = gtk.ListStore(gtk.gdk.Pixbuf,str,int)
        self.set_model(self.store)
        
        self.renderer_icon = gtk.CellRendererPixbuf()
        self.renderer_text = gtk.CellRendererText()
        self.pack_start(self.renderer_icon,False)
        self.pack_start(self.renderer_text,True)
        self.add_attribute(self.renderer_icon,'pixbuf',0)
        self.add_attribute(self.renderer_text,'text',1)
        
        self.firstrender = True
        page.addCallback(self.render)
        self.render()
    
    def render(self):
        def search(model,path,rowiter):
            space_id = model.get_value(rowiter,2)
            if space_id >=0:
                if space_id in model.objectsToAllocate.keys():
                    model.set_value(rowiter,0,IconStock.WIDGET)
                    model.set_value(rowiter,1,model.objectsToAllocate[space_id])
                    del(model.objectsToAllocate[space_id])
                else:
                    model.itersToRemove.append(rowiter)
        
        page = self.getApplication().getLocalObjectById(self.pageId)
        self.store.objectsToAllocate = page.getSpaces()
        self.store.itersToRemove = []
        self.store.foreach(search,)
        
        for rowiter in self.store.itersToRemove:
            self.store.remove(rowiter)
        
        for key, value in self.store.objectsToAllocate.items():
            self.store.append((IconStock.SPACE,value,int(key)))
            
        if self.firstrender:
            self.set_active(0)
            self.firstrender = False
    
    def getSpaceId(self):
        return self.store.get_value(self.get_active_iter(),2)

    def setSpaceId(self, nr):
        def search(model, path, rowiter, to_select_id):
            space_id = model.get_value(rowiter,2)
            if space_id == int(to_select_id):
                model.iterToSelect = rowiter
        self.store.iterToSelect = None
        self.store.foreach(search,nr)
        if self.store.iterToSelect is not None:
            self.set_active_iter(self.store.iterToSelect)
        return

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
class MenuItemTree(gtk.TreeView):
    def __init__(self, par, menu=None):
        gtk.TreeView.__init__(self)
        self.par = par
        self.menuId = menu.getLocalId()
        
        self.store = MenuItemStore(gtk.gdk.Pixbuf,str,int,int,parent=self.par, objectStore = self.getApplication().getObjectStore(),menu=menu)
        
        self.set_model(self.store)
        self.col_name = gtk.TreeViewColumn("MenuItem")
        self.col_order = gtk.TreeViewColumn("order")
        self.append_column(self.col_name)
        self.append_column(self.col_order)
        self.renderer_icon = gtk.CellRendererPixbuf()
        self.renderer_name = gtk.CellRendererText()
        self.renderer_order = gtk.CellRendererText()
        self.renderer_name.set_property('editable',True)
        self.col_name.pack_start(self.renderer_icon,False)
        self.col_name.pack_start(self.renderer_name,True)
        self.col_order.pack_start(self.renderer_order,True)
        self.col_name.add_attribute(self.renderer_icon,'pixbuf',0)
        self.col_name.add_attribute(self.renderer_name,'text',1)
        self.col_order.add_attribute(self.renderer_order,'text',3)
        self.renderer_name.connect('edited', self.renamedCallback)
        self.set_reorderable(True)
        
        self.col_order.set_sort_column_id(2)
        self.col_order.set_sort_order(gtk.SORT_DESCENDING)
        self.store.emit("sort_column_changed")
        
        self.set_search_column(1)
        
    def getSelectedMenuItem(self):
        selection = self.get_selection()
        rowiter = selection.get_selected()[1]
        obj_id = self.store.get_value(rowiter,2)
        obj = self.getApplication().getLocalObjectById(obj_id)
        return obj
    
    def renamedCallback(self, cell, path, name):
        obj_id = self.store[path][2]
        obj = self.getApplication().getLocalObjectById(obj_id)
        if obj.__class__.__name__ == 'MenuItem':
            obj.rename(name)    
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
class MenuItemStore(gtk.TreeStore):
    WHITELISTED_CLASSES = ("Menu","MenuItem")
    def __init__(self,*args,**kwargs):
        assert kwargs['objectStore'] is not None, "need objectStore!"
        gtk.TreeStore.__init__(self,*args)
        self.par = kwargs['parent']
        self.objectStore = kwargs['objectStore']
        self.menuId = kwargs['menu'].getLocalId()
        
        kwargs['menu'].addCallback(self.render)
        self.busy = False # Prevent threadcollisions 
        self.root = self.append(None,(IconStock.MENU,kwargs['menu'].getName(),self.menuId,0))
        self.render()

    def getIterById(self, obj_id):
        def search(model, path, rowiter, obj_id):
                val = model.get_value(rowiter,2)
                if val == obj_id:
                    model.tempiter = rowiter
            
        if not self.busy:
            self.busy = True
                    
            self.tempiter = None
            self.foreach(search, obj_id)
            
            rowiter=self.tempiter
            self.busy = False
            if rowiter is not None:
                return rowiter
            else:
                return None
        else:
            pass
            #raise StoreException("store is busy")
    
    def addObject(self,obj,addToRootIfNoParent=True):
        if obj.__class__.__name__ not in self.WHITELISTED_CLASSES:
            return True
        try:
            parent = obj.getPar()
            if parent.__class__.__name__ == "MenuItem" or parent.__class__.__name__ == "Menu":
                parentIter = self.getIterById(parent.getLocalId())
                self.append(parentIter,(IconStock.MENUITEM, obj.getName(), obj.getLocalId(),obj.getOrder()))
                return True
            else:
                raise Exception()
        except:
            if addToRootIfNoParent : 
                root = self.getIterById(-2)
                self.append(root,(IconStock.MENUITEM, obj.getName(), obj.getLocalId(),obj.getOrder()))
                return True
            return False
    

    def render(self):
        def search(model, path, rowiter):
            obj_id = model.get_value(rowiter,2)
            if obj_id >= 0:
                try:
                    obj = self.objectStore.getLocalObjectById(obj_id)
                except GenericObjectStoreException:
                    model.itersToRemove.append(rowiter)
                else:
                    if obj.__class__.__name__=="MenuItem":
                        model.set_value(rowiter,0,IconStock.MENUITEM)
                        model.set_value(rowiter,1,obj.getName())
                        model.set_value(rowiter,3,obj.getOrder())
                        try:
                            self.objectsToAllocate.remove(obj)
                        except ValueError,e:
                            print obj, self.objectsToAllocate
                    else:
                        model.set_value(rowiter,0,IconStock.MENU)
                        model.set_value(rowiter,1,obj.getName())
                        self.objectsToAllocate.remove(obj)
                                
        objectsAllocated = 1
        try:
            menu = self.getApplication().getLocalObjectById(self.menuId)
        except GenericObjectStoreException:
            self.getPar().destroy()
            return
        self.objectsToAllocate = [self.objectStore.getLocalObjectById(c) for c in menu.getMenuItemsRecursive()]
        self.objectsToAllocate.append(menu)
        self.itersToRemove= []
        self.foreach(search)
        
        self.itersToRemove.reverse() # objects must be deleted from treeview from child to parent
        pass                         # but come in in exactly the other direction from getMenuItemsRecursive()
        
        for rowiter in self.itersToRemove:
            self.remove(rowiter)

        while objectsAllocated > 0:
            objectsAllocated = 0
            for obj in self.objectsToAllocate:
                if self.addObject(obj, False):
                    self.objectsToAllocate.remove(obj)
                    objectsAllocated+=1
        
        for obj in self.objectsToAllocate:
            self.addObject(obj, True)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
        
        
    