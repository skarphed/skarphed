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

import os

from data.Generic import GenericObjectStoreException

from gui.skarphed.ViewGenerationControl import ViewGenerationControl
from gui.InputBox import InputBox

class WidgetPage(gtk.VBox):
    def __init__(self, parent, widget):
        self.par = parent
        gtk.VBox.__init__(self)
        self.widgetId = widget.getLocalId()

        self._news = {}
        self._current_entry = {}

        path = os.path.realpath(__file__)
        path = path.replace("widget.pyc","")
        self._path = path.replace("widget.py","")

        self.builder = gtk.Builder()
        self.builder.add_from_file(self._path+"widget.glade")
        self.handlers = {
            "save_cb"       : self.saveCallback,
            "new_cb"        : self.newCallback,
            "choose_news_cb": self.chooseNewsCallback
        }
        self.builder.connect_signals(self.handlers)

        self.widget = self.builder.get_object("widget")

        self._newsstore = self.builder.get_object("newsstore")
        self._commentstore = self.builder.get_object("commentstore")

        self.widget.pack_start(ViewGenerationControl(self, widget))

        self.add(self.widget)
        self.loadNews()

    def render(self):
        def search_news(model,path,rowiter):
            nr = model.get_value(rowiter,4)
            if str(nr) not in self._news.keys():
                self._itersToRemove.append(rowiter)
            else:
                model.set_value(rowiter,0,self._news[str(nr)]["show"])
                model.set_value(rowiter,1,self._news[str(nr)]["title"])
                model.set_value(rowiter,2,self._news[str(nr)]["author"])
                model.set_value(rowiter,3,self._news[str(nr)]["date"])
            self._news_handled.append(nr)
        
        def search_comments(model,path,rowiter):
            comments = self._current_entry["comments"]
            nr = model.get_value(rowiter,4)
            if str(nr) not in self._news.keys():
                self._itersToRemove.append(rowiter)
            else:
                model.set_value(rowiter,0,comments[str(nr)]["del"])
                model.set_value(rowiter,1,comments[str(nr)]["date"])
                model.set_value(rowiter,2,comments[str(nr)]["author"])
                model.set_value(rowiter,3,comments[str(nr)]["content"])
            self._news_handled.append(nr)
        

        self._news_handled = []
        self._itersToRemove = []
        self._newsstore.foreach(search_news)

        for rowiter in self._itersToRemove:
            self._newsstore.remove(rowiter)

        for nr in self._news.keys():
            if int(nr) not in self._news_handled:
                self._newsstore.append((self._news[nr]["show"],
                                        self._news[nr]["title"],
                                        self._news[nr]["author"],
                                        self._news[nr]["date"],
                                        int(nr)))

        del(self._news_handled)

        if self._current_entry != {}:
            self._itersToRemove = []
            self._comments_handled = []

            self._commentstore.foreach(search_comments)

            for rowiter in self._itersToRemove:
                self._commentstore.remove(rowiter)

            for nr in self._current_entry["comments"].keys():
                if int(nr) not in self._comments_handled:
                    self._commentstore.append((self._current_entry["comments"][nr]["del"],
                                               self._current_entry["comments"][nr]["date"],
                                               self._current_entry["comments"][nr]["author"],
                                               self._current_entry["comments"][nr]["content"],
                                               int(nr)))
            del(self._comments_handled)
            self.builder.get_object("title").set_text(self._current_entry["title"])
            self.builder.get_object("content").get_buffer().set_text(self._current_entry["content"])

        del(self._itersToRemove)

    def loadNewsCallback(self,data):
        self._news = data
        self.render()

    def loadNews(self):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getSkarphed()
        scv.doRPCCall(self.loadNewsCallback, "executeModuleMethod", [module.getId(), "get_news", [widget.getId()]])


    def loadNewsEntryCallback(self,data):
        self._current_entry = data
        for comment in self._current_entry["comments"].values():
            comment["del"] = False

        self.render()


    def loadNewsEntry(self, entry_id):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getSkarphed()
        scv.doRPCCall(self.loadNewsEntryCallback, "executeModuleMethod", [module.getId(), "get_news_entry", [widget.getId(), entry_id]])

    def chooseNewsCallback(self, tree=None, path=None, data=None):
        selection = self.builder.get_object("newsview").get_selection()
        rowiter = selection.get_selected()[1]
        nr = self._newsstore.get_value(rowiter,4)
        self.loadNewsEntry(nr)

    def savedEntryCallback(self, data):
        self.loadNewsEntry(self._current_entry["id"])

    def saveCallback(self, widget=None, data=None):
        self._saving_entry = self._current_entry

        self._saving_entry["title"] = self.builder.get_object("title").get_text()
        textbuffer = self.builder.get_object("content").get_buffer()
        self._saving_entry["content"] = textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter())

        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getSkarphed()
        scv.doRPCCall(self.createNewEntryCallback, "executeModuleMethod", [module.getId(), "save_news_entry", [widget.getId(), self._saving_entry]])

    def createNewEntryCallback(self, data):
        self.loadNews()

    def newCallback(self, widget=None, data=None):
        InputBox(self, "Please enter the title of the new news-entry", self.executeNew, notEmpty=True)

    def executeNew(self, title):
        try:
            widget = self.getApplication().getLocalObjectById(self.widgetId)
        except GenericObjectStoreException:
            self.destroy()
        module = widget.getModule()

        scv = module.getModules().getSkarphed()
        scv.doRPCCall(self.createNewEntryCallback, "executeModuleMethod", [module.getId(), "create_news_entry", [widget.getId(), title]])

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
