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

MAINTENANCE_HTML = """
<!DOCTYPE html>
<html>
    <head>
        <title> Maintenance Mode </title>
        <style>
            body {
                background-color:#0F0F0F;
                padding-top:200px;
            }

            .box {
                margin-left:auto;
                margin-right:auto;
                width:400px;
                padding:50px;
                font-family: sans;
                text-align:center;
            }

            .content {
                font-size:18px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                background-color:#AAAAAA;
                color:#FFFFFF;
            }

            .footer {
                font-size:10px;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
                background-color:#222222;
                color:#FFFFFF;
            }
        </style>
    </head>
    <body>
        <div class="box content">
            This page is currently in maintenance mode.
        </div>
        <div class="box footer">
            This page is build and maintained using skarphed.
        </div>
    </body>
</html>
"""