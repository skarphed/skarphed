#!/usr/bin/env python

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

from cgi import FieldStorage
from mimetypes import guess_type
from urlparse import parse_qs
from traceback import print_exc
from StringIO import StringIO
import json

import sys
sys.path.append('/var/www_py/')

from database import DatabaseMiddleware
from protocolhandler import ProtocolHandler
from repository import Repository


def default_template(environ, response_headers):
    try:
        f = open('/usr/share/scvrepo/template.html')
        template = f.read()
        f.close()
        repository = Repository()
        template = template.replace('{{publickey}}', repository.get_public_key(environ))
        response_body = [template]
        response_headers.append(('Content-Type', 'text/html'))
    except IOError, ie:
        response_body = ['Error reading template'] # TODO: improve error message
        response_headers.append(('Content-Type', 'text/plain'))
    return response_body


def repo_application(environ, start_response):
    response_body = []
    response_headers = []

    if environ['PATH_INFO'].startswith('/static/'):
        prefix = "/usr/share/scvrepo/"
        path = environ['PATH_INFO'][1:]
        status = '200 OK'  
        (mime, encoding) = guess_type(prefix+path)
        f = open(prefix+path, 'r')
        data = f.read()
        f.close()
        response_body = [data]
        response_headers.append(('Content-Type', mime))
    else:
        try:
            if environ['REQUEST_METHOD'] == 'POST':
                try:
                    size = int(environ.get('CONTENT_LENGTH', 0))
                except ValueError, e:
                    size = 0
                args = FieldStorage(fp=environ['wsgi.input'], environ=environ)
                jsonstr = args.getvalue('j')
            else:
                args = parse_qs(environ['QUERY_STRING'])
                jsonstr = args['j']
            print ("JSON: " + str(jsonstr))
            try:
                repository = Repository()
                handler = ProtocolHandler(repository, jsonstr[0], response_headers)
                response_body = [handler.execute(environ)]
            except Exception, e:
                errorstream  = StringIO()
                print_exc(None,errorstream)
                response_body = ['{error:%s}' % errorstream.getvalue()]

            response_headers.append(('Content-Type', 'application/json'))
        except KeyError, e:
            response_body = default_template(environ, response_headers) 
        status = '200 OK'
    
    start_response(status, response_headers)
    return response_body


application = DatabaseMiddleware(repo_application)
