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
from urlparse import parse_qs
from traceback import print_exc
from StringIO import StringIO
import json

import os
import sys

sys.path.append(os.path.dirname(__file__))

from database import *
from protocolhandler import ProtocolHandler
from repository import *
from session import SessionMiddleware
from shareddatamiddleware import SharedDataMiddleware

def default_template(environ, response_headers):
    """
    Loads the default repositories template and returns it.
    """
    try:
        f = open('/usr/share/scvrepo/template.html')
        template = f.read()
        f.close()
        repository = Repository()
        template = template.replace('{{publickey}}', repository.get_public_key(environ))
        response_body = [template]
        response_headers.append(('Content-Type', 'text/html'))
        response_headers.append(('Content-Length', str(len(template))))
        status = '200 OK'
    except IOError, ie:
        response_body = ['404 Not Found'] # TODO: improve error message
        response_headers.append(('Content-Type', 'text/plain'))
        status = '404 Not Found'
    except RepositoryException, e:
        # TODO what to return if there is no public key
        response_body = ['404 Not Found'] # TODO: improve error message
        response_headers.append(('Content-Type', 'text/plain'))
        status = '404 Not Found'
    return (status, response_body)


def repo_application(environ, start_response):
    """
    The repositories WSGI application. If the incoming request's type is POST then it
    will be delegated to a protocol handler, otherwise the default template will be returned.
    """
    response_body = []
    response_headers = []

    try:
        status = '200 OK'
        if environ['REQUEST_METHOD'] == 'POST':
            try:
                size = int(environ.get('CONTENT_LENGTH', 0))
            except ValueError, e:
                size = 0
            args = FieldStorage(fp=environ['wsgi.input'], environ=environ)
            jsonstr = args.getvalue('j')
        else:
            args = parse_qs(environ['QUERY_STRING'])
            jsonstr = args['j'][0]
        print ("JSON: " + str(jsonstr))
        try:
            repository = Repository()
            handler = ProtocolHandler(repository, jsonstr)
            response_body = [handler.execute(environ)]
        except DatabaseException, e:
            response_body = ['{"error":{"c":%d,"args":[]}}' % RepositoryErrorCode.DATABASE_ERROR]
        except RepositoryException, e:
            response_body = ['{"error":%s}' % json.dumps(e.get_error_json())] 
        except Exception, e:
            errorstream  = StringIO()
            print_exc(None, errorstream)
            response_body = ['{error:%s}' % errorstream.getvalue()]

        response_headers.append(('Content-Type', 'application/json'))
    except KeyError, e:
        (status, response_body) = default_template(environ, response_headers) 
    
    start_response(status, response_headers)
    print ("RESPONSE: " + str(response_body))
    return response_body


"""
Wraps the repository application in a
0) SharedDataMiddleware, to provide some static content
1) DatabaseMiddleware, to provide a database connection via environ['db']
2) SessionMiddleware, to provide session handling
"""
application = SharedDataMiddleware(
        DatabaseMiddleware(SessionMiddleware(repo_application)),
        'static')
