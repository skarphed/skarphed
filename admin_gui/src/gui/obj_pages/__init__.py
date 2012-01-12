#!/usr/bin/python
#-*- coding:utf-8 -*-

from GenericObject import GenericObjectPage
from User import UserPage

class PageException(Exception):pass

def generatePageForObject(parent,object,IconStock):
   if object.__class__.__name__ == "GenericScovilleObject":
       return  GenericObjectPage(parent,object)
   elif object.__class__.__name__ == "Server":
       return  GenericObjectPage(parent,object,IconStock)
   elif object.__class__.__name__ == "User":
       return  UserPage(parent,object,IconStock)
   elif object.__class__.__name__ == "Module":
       return  GenericObjectPage(parent,object,IconStock)
   elif object.__class__.__name__ == "Role":
       return  GenericObjectPage(parent,object,IconStock)
   elif object.__class__.__name__ == "Site":
       return  GenericObjectPage(parent,object,IconStock)
   elif object.__class__.__name__ == "Repository":
       return  GenericObjectPage(parent,object,IconStock)
   elif object.__class__.__name__ == "Template":
       return  GenericObjectPage(parent,object,IconStock)
   else:
       raise PageException("There is no Page for the Classtype "+object.__class__.__name__)
   