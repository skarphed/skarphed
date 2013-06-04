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

from glue.lng import _
from glue.threads import UserKillThreadException

class ThreadControl(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self,gtk.WINDOW_POPUP)

        self.width = 300
        self.height = 200

        self.closebutton = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.decoframe = gtk.Frame()
        self.dummy = gtk.Label("")
        self.hbox = gtk.HBox()
        self.vbox = gtk.VBox()
        self.vbox.set_border_width(3)
        self.vbox.set_spacing(5)
        self.threadvbox = gtk.VBox()
        self.threads = {}
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_NEVER,gtk.POLICY_ALWAYS)
        self.scroll.add_with_viewport(self.threadvbox)
        self.hbox.pack_start(self.dummy,True)
        self.hbox.pack_start(self.closebutton,False)
        self.vbox.pack_start(self.hbox,False)
        self.vbox.pack_start(self.scroll,True)
        self.decoframe.add(self.vbox)
        self.add(self.decoframe)
        self.set_visible(False)
        self.closebutton.connect("clicked", self.close)

        self.set_size_request(self.width,self.height)

        self.show_all()

    def render(self, threads):
        for thread in threads:
            if thread.ident not in self.threads.keys():
                threadwidget = ThreadLine()
                self.threads[thread.ident] = threadwidget
                self.threadvbox.pack_start(threadwidget,False)
                threadwidget.render(thread)
                threadwidget.show()

        for threadkey in self.threads.keys():
            if threadkey not in [thread.ident for thread in threads]:
                self.threads[threadkey].destroy()
                del(self.threads[threadkey])

    def popup(self,x,y):
        self.move(x-(self.width/2),y-(self.height))
        self.set_visible(True)

    def close(self, widget=None, data=None):
        self.set_visible(False)

    def isOpen(self):
        return self.get_visible()

class ThreadLine(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)

        self.label = gtk.Label()
        self.killswitch = gtk.Button(_("Kill"))
        self.pack_start(self.label,True)
        self.pack_start(self.killswitch,False)
        self.set_border_width(2)

        self.threadId = None
        self.show_all()
        self.killswitch.set_visible(False)

    def render(self, thread):
        self.threadId = thread.ident
        if hasattr(thread,"kill"):
            self.killswitch.connect("clicked", self.cb_kill, thread)
            self.killswitch.set_visible(True)
        if hasattr(thread,"getName"):
            self.label.set_text(thread.getName())
        else:
            self.label.set_text("Unspecified Process")

    def cb_kill(self, widget=None, data=None):
        data.kill(UserKillThreadException)
