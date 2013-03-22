#!/usr/bin/env python

from urlparse import parse_qs

import protocolhandler

def application(environ, start_response):
    response_body = []
    response_headers = []
    
    args = parse_qs(environ['QUERY_STRING']) # TODO: exception handling

    try:
        jsonstr = args['j']
        try:
            handler = ProtocolHandler(jsonstr)
            response_body = [handler.execute()]
        except Exception, e:
            response_body = ['{error:%s}' % str(e)]

        response_headers.append(('Content-Type', 'application/json'))
    except KeyError, e:
        try:
            with open("template.html") as f:
                template = f.read()
                template = template.replace('{{publickey}}', 'THIS SHOULD BE A PUBLIC KEY') #get public key from repo
                response_body = [template]
            response_headers.append(('Content-Type', 'text/html'))
        except IOError, ie:
            response_body = ['Error reading template'] # TODO: improve error message
            response_headers.append(('Content-Type', 'text/plain'))
            

    status = '200 OK'
    start_response(status, response_headers)
    return response_body
