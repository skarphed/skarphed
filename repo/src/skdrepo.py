#!/usr/bin/env python
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


import sys
sys.path.append('/usr/share/skdrepo/')

from wsgiref.simple_server import make_server

from config import Config
import wsgi


def main():
    """
    Executes a skprepo as standalone application. 
    """
    config = Config()

    httpd = make_server(config['server.ip'], config['server.port'], wsgi.application)
    httpd.serve_forever()
    
    
if __name__ == '__main__':
    main()
