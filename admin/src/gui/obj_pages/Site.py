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
import gui.IconStock

class WidgetContainer(gtk.HBox):
    def __init__(self, par, site, spaceId, widget=None):
        self.par = par
        gtk.HBox.__init__(self)
        self.view = gtk.TreeView()
        self.store = gtk.ListStore(gtk.gdk.Pixbuf, str, int)
        self.spaceId = spaceId
        self.site = site
        self.widget = widget
        
        self.view.set_model(self.store)
        self.col_wdg = gtk.TreeViewColumn("")
        self.ren_icon = gtk.CellRendererPixbuf()
        self.ren_name = gtk.CellRendererText()
        self.view.append_column(self.col_wdg)
        self.col_wdg.pack_start(self.ren_icon,False)
        self.col_wdg.pack_start(self.ren_name,True)
        self.col_wdg.add_attribute(self.ren_icon,'pixbuf',0)
        self.col_wdg.add_attribute(self.ren_name,'text',1)
        
        self.view.set_name("siteWidget_"+str(self.site.getLocalId())+"_"+str(self.spaceId))
        self.view.enable_model_drag_dest([('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        self.view.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        self.view.connect("drag-data-received", self.dragReceiveWidget)
        self.view.connect("drag-data-get", self.dragGetWidget)
        
        self.pack_start(self.view,True)
        self.set_size_request(300,45)
        self.show_all()
        
        self.site.addCallback(self.render)
        if self.widget is not None:
            self.widget.addCallback(self.render)
        self.render()
        
    def render(self):
        self.widget = self.site.getWidgetInSpace(self.spaceId)
        if len(self.store) > 0:
            if self.widget is None:
                self.store.clear()
                self.col_wdg.set_title("Space "+str(self.spaceId)+": Free")
            else:
                self.store[0][1] = self.widget.getName()
                self.store[0][2] = self.widget.getLocalId()
        else:
            self.col_wdg.set_title("Space "+str(self.spaceId)+": Free")
            if self.widget is not None:
                self.store.append((IconStock.WIDGET, self.widget.getName(), self.widget.getLocalId()))
                self.col_wdg.set_title("Space "+str(self.spaceId)+": Occupied")
        
    def dragReceiveWidget(self, view, context, x, y, selection, info, timestamp):
        validDrop=False
        move = False
        sourceName = context.get_source_widget().get_name()
        if sourceName  == "siteWidgetList"+str(self.site.getLocalId()):
            validDrop = True
        if sourceName.startswith("siteWidget_"+str(self.site.getLocalId())) and sourceName[-1:] != str(self.spaceId):
            validDrop = True
            move = True
        if not validDrop:
            return
        
        if move:
            self.site.removeWidgetFromSpace(sourceName[-1:])
        widget = self.getApplication().getLocalObjectById(int(selection.data))
        self.site.addWidgetToSpace(self.spaceId, widget)
        
    def dragGetWidget(self, view, context, selection, info, timestamp):
        treeselection = view.get_selection()
        model, rowiter = treeselection.get_selected()
        value = model.get_value(rowiter,2)
        selection.set('text/plain',8,str(value))
        
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()


class SitePage(GenericObjectPage):
    def __init__(self, par, site):
        GenericObjectPage.__init__(self,par,site)
        self.par = par
        self.site = site
        
        self.info = PageFrame(self,"Information", gui.IconStock.SITE)
        self.infobox = gtk.VBox()
        self.info_table = gtk.Table(3,3,False)
        self.info_labelName = gtk.Label("Name:")
        self.info_labelDescription = gtk.Label("Description:")
        self.info_labelSpaces = gtk.Label("Spaces:")
        self.info_displayName = gtk.Label("")
        self.info_displayDescription = gtk.Label("")
        self.info_displaySpaces = gtk.Label("")
        self.info_minimapLabel = gtk.Label("Miniview:")
        self.info_minimap = gtk.Image()
        self.info_table.attach(self.info_labelName,0,1,0,1)
        self.info_table.attach(self.info_displayName,1,2,0,1)
        self.info_table.attach(self.info_labelDescription,0,1,1,2)
        self.info_table.attach(self.info_displayDescription,1,2,1,2)
        self.info_table.attach(self.info_labelSpaces,0,1,2,3)
        self.info_table.attach(self.info_displaySpaces,1,2,2,3)
        self.info_table.attach(self.info_minimapLabel,2,3,0,1)
        self.info_table.attach(self.info_minimap,2,3,1,3)
        self.infobox.add(self.info_table)
        self.info.add(self.infobox)
        self.pack_start(self.info,False)
        
        self.wdg = PageFrame(self,"Widgets", gui.IconStock.WIDGET)
        self.wdgbox = gtk.HBox()
        self.wdg_view = gtk.TreeView()
        self.wdg_store = gtk.ListStore(gtk.gdk.Pixbuf,str,int)
        self.wdg_view.set_model(self.wdg_store)
        self.wdg_col = gtk.TreeViewColumn("Widget")
        self.wdg_ren_icon = gtk.CellRendererPixbuf()
        self.wdg_ren_name = gtk.CellRendererText()
        self.wdg_col.pack_start(self.wdg_ren_icon,False)
        self.wdg_col.pack_start(self.wdg_ren_name,True)
        self.wdg_col.add_attribute(self.wdg_ren_icon,'pixbuf',0)
        self.wdg_col.add_attribute(self.wdg_ren_name,'text',1)
        self.wdg_view.append_column(self.wdg_col)
        self.wdg_view.set_name("siteWidgetList"+str(self.site.getLocalId()))
        self.wdg_view.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        self.wdg_view.enable_model_drag_dest([('text/plain',0,0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
        self.wdg_view.connect("drag-data-get", self.getDragDataCallback)
        
        self.wdg_spacescroll = gtk.ScrolledWindow()
        self.wdg_spacescroll.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
        self.wdg_spacescroll.set_size_request(300,200)
        self.wdg_spaces = gtk.VBox()
        self.wdg_spacescroll.add_with_viewport(self.wdg_spaces)
        self.wdg_spacewidgets = []
        
        for i in range(self.site.getSpaceCount()):
            widget = self.site.getWidgetInSpace(i+1)
            if widget is None:
                self.wdg_spacewidgets.append(WidgetContainer(self,self.site,i+1))
            else:
                self.wdg_spacewidgets.append(WidgetContainer(self,self.site,i+1,widget))
            #self.wdg_spacewidgets[i].set_border_width(10)
            self.wdg_spaces.add(self.wdg_spacewidgets[i])
        
        #self.wdg_spaces.set_size_request(300, 45*len(self.wdg_spacewidgets))
            
        self.wdgbox.add(self.wdg_spacescroll)
        self.wdgbox.add(self.wdg_view)
        self.wdg.add(self.wdgbox)
        self.pack_start(self.wdg,False)
        
        
        self.site.addCallback(self.render)
        self.render()
        
    def render(self):
        self.info_displayName.set_text(self.site.getName())
        self.info_displayDescription.set_text(self.site.getDescription())
        self.info_displaySpaces.set_text(str(self.site.getSpaceCount()))
        
        self.info_minimap.set_from_file(self.site.getMinimap())
        
        usedWidgetIds = self.site.getUsedWidgetIds()
        self.wdg_store.clear()
        widgets = self.site.getScoville().modules.getAllWidgets()
        for widget in widgets:
            if widget.getId() not in usedWidgetIds:
                self.wdg_store.append((IconStock.WIDGET,widget.getName(),widget.getLocalId()))
    
    def getDragDataCallback(self, view, context, selection, info, timestamp):
        treeselection = view.get_selection()
        model, rowiter = treeselection.get_selected()
        value = model.get_value(rowiter,2)
        selection.set('text/plain',8,str(value))
    
    def dragReceiveWidget(self, view, context, x, y, selection, info, timestamp):
        if not context.get_source_widget().get_name().startswith("siteWidget_"+str(self.site.getLocalId())):
            return
        spaceId = int(context.get_source_widget().get_name()[-1:])
        self.site.removeWidgetFromSpace(spaceId)
    
    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
