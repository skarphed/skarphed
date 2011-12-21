#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
gtk.gdk.threads_init()

import MainWindow as MainWindow_

MainWindow = MainWindow_.MainWindow


def run():
    gtk.main()

class Gui(object):
    def __init__(self,app):
        self.app = app
    def doLoginTry(self,username,password):
        self.app.doLoginTry(username,password)