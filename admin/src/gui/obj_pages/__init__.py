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


from GenericObject import GenericObjectPage
from User import UserPage
from Role import RolePage
from Template import TemplatePage
from Repository import RepositoryPage
from Site import SitePage
from Menu import MenuPage

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
        return  SitePage(parent,obj)
    elif obj.__class__.__name__ == "Repository":
        return  RepositoryPage(parent,obj)
    elif obj.__class__.__name__ == "Template":
        return  TemplatePage(parent,obj)
    elif obj.__class__.__name__ == "Widget":
        return  GenericObjectPage(parent,obj)
    elif obj.__class__.__name__ == "Menu":
        return MenuPage(parent,obj)
    else:
        raise PageException("There is no Page for the Classtype "+obj.__class__.__name__)
   