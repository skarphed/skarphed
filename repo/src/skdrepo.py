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
sys.path.append('/var/www/skdrepo/')

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from config import Config
import wsgi


class RepositoryHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request(self.command)

    def do_POST(self):
        self.handle_request(self.command)

    def handle_request(self, method):
        def start_response(status, headers, exc_info=None):
            status = int(status.split(' ')[0])
            self.send_response(status)
            for (key, value) in headers:
                self.send_header(key, value)
            self.end_headers()

        environ = self.create_wsgi_environ()
        response_body = wsgi.application(environ, start_response)
        self.wfile.write(response_body[0])

    def create_wsgi_environ(self):

        print(self.path)
        print(self.command)
        print(self.headers)

        environ = {} 
        query_string = self.path.split('?', 1)
        if len(query_string) == 2:
            query_string = query_string[1]
        else:
            query_string = ''
        environ['QUERY_STRING'] = query_string
        environ['REQUEST_METHOD'] = self.command
        environ['PATH_INFO'] = self.path
        return environ


def main():
    """
    Executes a skprepo as standalone application. 
    """
    config = Config()
    listen_address = (config['server.ip'], config['server.port'])

    httpd = HTTPServer(listen_address, RepositoryHTTPRequestHandler)
    httpd.serve_forever()
    
    
if __name__ == '__main__':
    main()
