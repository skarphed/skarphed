#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from GenericObject import GenericObjectPage
from GenericObject import PageFrame
from GenericObject import FrameLabel

from gui.OperationTool import OperationTool
import gui.IconStock

class RepositoryPage(GenericObjectPage):
    def __init__(self,parent,obj):
        self.par = parent
        GenericObjectPage.__init__(self,parent,obj)
        self.repo = obj
        
        self.headline = gtk.Label()
        self.pack_start(self.headline,False)
        
        self.info = PageFrame(self,"Information", gui.IconStock.REPO)
        self.infobox = gtk.VBox()
        self.info_table = gtk.Table(2,2,False)
        self.info_labelName = gtk.Label("name:")
        self.info_labelHost = gtk.Label("host:")
        self.info_displayName = gtk.Label()
        self.info_displayHost = gtk.Label()
        self.info_table.attach(self.info_labelName,0,1,0,1)
        self.info_table.attach(self.info_displayName,1,2,0,1)
        self.info_table.attach(self.info_labelHost,0,1,1,2)
        self.info_table.attach(self.info_displayHost,1,2,1,2)
        self.infobox.pack_start(self.info_table,False)
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.mod = PageFrame(self,"available and installed modules", gui.IconStock.MODULE)
        self.modbox = gtk.Table(5,2,False)
        self.modbox.set_row_spacings(10)
        self.modbox.set_col_spacings(10)
        self.modbox.set_border_width(10)
        
        self.mod_label = gtk.Label("please drag a module into the opposing list to install/uninstall it:\n")
        self.mod_labelInstalled = gtk.Label("installed modules")
        self.mod_labelAvailable = gtk.Label("available modules")
        self.mod_labelProcessed = gtk.Label("currently processed modules")
        
        self.mod_IListScroll = gtk.ScrolledWindow()
        self.mod_IListScroll.set_size_request(200,250)
        self.mod_IListScroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.mod_IList = gtk.TreeView()
        self.mod_IListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        self.mod_IList.set_model(self.mod_IListStore)
        self.mod_IList_col_module = gtk.TreeViewColumn('module name')
        self.mod_IList_ren_icon = gtk.CellRendererPixbuf()
        self.mod_IList_ren_name = gtk.CellRendererText()
        self.mod_IList.append_column(self.mod_IList_col_module)
        self.mod_IList_col_module.pack_start(self.mod_IList_ren_icon,False)
        self.mod_IList_col_module.pack_start(self.mod_IList_ren_name,True)
        self.mod_IList_col_module.add_attribute(self.mod_IList_ren_icon,'pixbuf',0)
        self.mod_IList_col_module.add_attribute(self.mod_IList_ren_name,'text',1)
        self.mod_IList_col_module.set_sort_column_id(1)
        self.mod_IListScroll.add(self.mod_IList)
        
        self.mod_AListScroll = gtk.ScrolledWindow()
        self.mod_AListScroll.set_size_request(200,250)
        self.mod_AListScroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)       
        self.mod_AList = gtk.TreeView()
        self.mod_AListStore = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        self.mod_AList.set_model(self.mod_AListStore)
        self.mod_AList_col_module = gtk.TreeViewColumn('module name')
        self.mod_AList_ren_icon = gtk.CellRendererPixbuf()
        self.mod_AList_ren_name = gtk.CellRendererText()
        self.mod_AList.append_column(self.mod_AList_col_module)
        self.mod_AList_col_module.pack_start(self.mod_AList_ren_icon,False)
        self.mod_AList_col_module.pack_start(self.mod_AList_ren_name,True)
        self.mod_AList_col_module.add_attribute(self.mod_AList_ren_icon,'pixbuf',0)
        self.mod_AList_col_module.add_attribute(self.mod_AList_ren_name,'text',1)
        self.mod_AList_col_module.set_sort_column_id(1)
        self.mod_AListScroll.add(self.mod_AList)
        
        self.mod_CList = OperationTool(self,self.repo.getServer())
        
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
        obj.addCallback(self.render)
        self.repo.getServer().getOperationManager().addCallback(self.render)
        self.getApplication().getObjectStore().addCallback(self.render)
    
    def iListGetDataCallback(self, treeview, context, selection, info, timestamp):
        treeselection = treeview.get_selection()
        model, rowiter = treeselection.get_selected()
        text = model.get_value(rowiter, 2)
        selection.set('text/plain', 8, str(text))
    
    def aListGetDataCallback(self, treeview, context, selection, info, timestamp):
        treeselection = treeview.get_selection()
        model, rowiter = treeselection.get_selected()
        text = model.get_value(rowiter, 2)
        selection.set('text/plain', 8, str(text))
    
    def iListReceiveCallback(self, treeview, context, x, y, selection, info , timestamp):
        if context.get_source_widget().get_name() != "AList":
            return
        module = self.getApplication().getLocalObjectById(int(selection.data))
        self.repo.getServer().getModules().installModule(module)
    
    def aListReceiveCallback(self, treeview, context, x, y, selection, info , timestamp):
        if context.get_source_widget().get_name() != "IList":
            return
        module = self.getApplication().getLocalObjectById(int(selection.data))
        self.repo.getServer().getModules().uninstallModule(module)    
    
    def getModuleIterById(self, moduleList, moduleId):
        def search(model, path, rowiter, moduleId):
            val = model.get_value(rowiter,2)
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
            val = model.get_value(rowiter,2)
            if val not in processed:
                model.itersToRemove.append(rowiter)
            
        self.headline.set_markup("<b>Repository: "+self.repo.getName()+"</b>")
        
        self.processedIListIds = []
        self.processedAListIds = []
        
        for module in self.repo.getServer().getModules().getAllModules():
            if module.data.has_key('installed') and module.data['installed'] == True:
                rowiter = self.getModuleIterById(self.mod_IListStore,module.getLocalId())
                if rowiter is None:
                    if module.data.has_key('toUpdate') and module.data['toUpdate'] == True:
                        self.mod_IListStore.append((gui.IconStock.MODULE_UPDATEABLE, module.getName(), module.getLocalId() ))
                    else:
                        self.mod_IListStore.append((gui.IconStock.MODULE, module.getName(), module.getLocalId() ))
                else:
                    print "GEFUNDEN"
                    if module.data.has_key('toUpdate') and module.data['toUpdate'] == True:
                        self.mod_IListStore.set_value(rowiter,0,gui.IconStock.MODULE_UPDATEABLE)
                    else:
                        self.mod_IListStore.set_value(rowiter,0,gui.IconStock.MODULE)
                self.processedIListIds.append(module.getLocalId())
            else:
                rowiter = self.getModuleIterById(self.mod_AListStore,module.getLocalId())
                if rowiter is None:
                    self.mod_AListStore.append((gui.IconStock.MODULE, module.data['hrname'], module.getLocalId() ))
                self.processedAListIds.append(module.getLocalId())
        
        self.mod_IListStore.itersToRemove = []
        self.mod_AListStore.itersToRemove = []
        self.mod_IListStore.foreach(search, self.processedIListIds)
        self.mod_AListStore.foreach(search, self.processedAListIds)
        
        for rowiter in self.mod_IListStore.itersToRemove:
            self.mod_IListStore.remove(rowiter)
        for rowiter in self.mod_AListStore.itersToRemove:
            self.mod_AListStore.remove(rowiter)
        
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
    
    