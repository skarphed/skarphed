#!/usr/bin/python
#-*- coding: utf-8 -*-

#from grindhold_news import Module as News

class Module(object):
    def __init__(self):
        self.m = 1338

class Core(object):
    def __init__(self):
        self.c = "Core"

if __name__ == "__main__":
        from grindhold_news import Module as News

	core = Core()
	a = News(core)
	print a.get_tables()
	print a.render_html()
