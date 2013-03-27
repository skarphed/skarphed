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

from urlparse import parse_qs

from beaker.middleware import SessionMiddleware

from protocolhandler import ProtocolHandler
from repository import Repository


def application(environ, start_response):
    response_body = []
    response_headers = []
    
    args = parse_qs(environ['QUERY_STRING']) # TODO: exception handling

    try:
        jsonstr = args['j']
        try:
            repository = Repository(environ)
            handler = ProtocolHandler(repository, jsonstr[0])
            response_body = [handler.execute()]
        except Exception, e:
            response_body = ['{error:%s}' % str(e)]

        response_headers.append(('Content-Type', 'application/json'))
    except KeyError, e:
        try:
            with open("template.html") as f:
                template = f.read()
                repository = Repository(environ)
                template = template.replace('{{publickey}}', repository.get_public_key())
                response_body = [template]
            response_headers.append(('Content-Type', 'text/html'))
        except IOError, ie:
            response_body = ['Error reading template'] # TODO: improve error message
            response_headers.append(('Content-Type', 'text/plain'))
            

    status = '200 OK'
    start_response(status, response_headers)
    return response_body


wsgi_app = SessionMiddleware(application, type='dbm', data_dir='./.sessions')
