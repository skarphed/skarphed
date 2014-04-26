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

from sys import platform, path
from os.path import join, exists, expanduser

P = path[0]

# Handle different filepaths for most common OS (others may follow)

if exists(join(P,"DEVMODE")):
    ###
    ### Program runs in devmode. Use paths as they are in gitrepo
    ###
    if platform == 'linux2':
        DATA = join(P,"..","data")
        ICON = join(DATA,"icon")
        INSTALLER = join(P,"..","installer")
        LOCALE = join(P,"..","locale")
        COREFILES = join(P,"..","..","core")
        MODULEGUI = expanduser(join("~",".skarphedadmin","modulegui"))
        COOKIEPATH = expanduser(join("~",".skarphedadmin","cookies.txt"))
    elif platform == 'win32':
        DATA = join(P,"..","data")
        ICON = join(DATA,"icon")
        INSTALLER = join(P,"..","installer")
        LOCALE = join(P,"..","locale")
        COREFILES = join(P,"..","..","core")
        MODULEGUI = expanduser(join("~",".skarphedadmin","modulegui"))
        COOKIEPATH = expanduser(join("~",".skarphedadmin","cookies.txt"))
    elif platform == 'darwin':
        DATA = join(P,"..","data")
        ICON = join(DATA,"icon")
        INSTALLER = join(P,"..","installer")
        LOCALE = join(P,"..","locale")
        COREFILES = join(P,"..","..","core")
        MODULEGUI = expanduser(join("~",".skarphedadmin","modulegui"))
        COOKIEPATH = expanduser(join("~",".skarphedadmin","cookies.txt"))

else:
    ###
    ### Program runs in retailmode. Use packaged-paths
    ###
    if platform == 'linux2':
        DATA = join("/","usr","share","skarphed")
        ICON = join(DATA,"icon")
        INSTALLER = join("/","var","lib","skarphed","installer")
        LOCALE = join("/","usr","share","locale")
        COREFILES = join("/","usr","share","skarphed","corefiles")
        MODULEGUI = join("/","var","lib","skarphed","modulegui")
    elif platform == 'win32': #TODO: Get paths for Windows
        DATA = join(P,"..","..","data")
        ICON = join(DATA,"icon")
        INSTALLER = join(P,"..","..","installer")
        LOCALE = join(P,"..","..","locale")
        COREFILES = join(P,"..","..","core")
        MODULEGUI = join(P,"..","..","modulegui")
    elif platform == 'darwin': #TODO: Get paths for MacOS
        DATA = join(P,"..","data")
        ICON = join(DATA,"icon")
        INSTALLER = join(P,"..","installer")
        LOCALE = join(P,"..","locale")
        COREFILES = join(P,"..","..","core")
        MODULEGUI = expanduser(join("~",".skarphedadmin","modulegui"))