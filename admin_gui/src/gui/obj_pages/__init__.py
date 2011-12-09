#!/usr/bin/python
#-*- coding:utf-8 -*-

from GenericObject import GenericObject

class PageException(Exception):pass

def generatePageForObject(parent,object):
   if object.__class__.__name__ == "GenericScovilleObject":
       return  GenericObject(parent,object)
   elif object.__class__.__name__ == "Server":
       return  GenericObject(parent,object)
   else:
       raise PageException("There is no Page for the Classtype"+object.__class__.__name__)