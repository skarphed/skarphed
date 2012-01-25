#!/usr/bin/python
#-*- coding:utf-8 -*-

from GenericObject import GenericObjectPage
from User import UserPage
from Role import RolePage

class PageException(Exception):pass

def generatePageForObject(parent,obj):
    if obj.__class__.__name__ == "GenericScovilleObject":
        return  GenericObjectPage(parent,obj)
    elif obj.__class__.__name__ == "Server":
        return  GenericObjectPage(parent,obj)
    elif obj.__class__.__name__ == "User":
        return  UserPage(parent,obj)
    elif obj.__class__.__name__ == "Module":
        return  GenericObjectPage(parent,obj)
    elif obj.__class__.__name__ == "Role":
        return  RolePage(parent,obj)
    elif obj.__class__.__name__ == "Site":
        return  GenericObjectPage(parent,obj)
    elif obj.__class__.__name__ == "Repository":
        return  GenericObjectPage(parent,obj)
    elif obj.__class__.__name__ == "Template":
        return  GenericObjectPage(parent,obj)
    elif obj.__class__.__name__ == "Widget":
        return  GenericObjectPage(parent,obj)
    else:
        raise PageException("There is no Page for the Classtype "+obj.__class__.__name__)
   