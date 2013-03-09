#!/usr/bin/env python

#from wsgiref.simple_server import make_server

import sys
import os

cfgfile = open("/etc/scoville/scoville.conf","r").read().split("\n")
cfg = {}
for line in cfgfile:
    if line.startswith("#") or line.find("=") == -1:
        continue
    key, value = line.split("=")
    cfg[key]=value

del(cfgfile)

p = os.path.realpath(__file__)
p = p.replace("scoville.pyc","")
p = p.replace("scoville.py","")
sys.path.append(p)

from instanceconf import SCV_INSTANCE_SCOPE_ID
cfg["SCV_INSTANCE_SCOPE_ID"] = SCV_INSTANCE_SCOPE_ID

sys.path.append(cfg["SCV_LIBPATH"])

from scv import Core

def application(environ, start_response):
    response_body = []
    response_headers = []

    session_id = ""

    core = Core(cfg)

    if environ['PATH_INFO'].startswith("/static/"):
        path = environ['PATH_INFO'].replace("/static/","",1)

        binary_manager = core.get_binary_manager()
        binary = binary_manager.get_by_filename(path)
        data = binary.get_data()
        
        response_body=[data]
        response_headers.append(('Content-Type', binary.get_mime()))

    elif environ['PATH_INFO'].startswith("/rpc/"):
        ret = core.rpc_call(environ)
        response_body.extend(ret["body"])
        response_headers.extend(ret["header"])
        response_headers.append(('Content-Type', 'application/json'))

    elif environ['PATH_INFO'].startswith("/web/"):
        ret = core.web_call(environ)
        response_body.extend(ret["body"])
        response_headers.extend(ret["header"])
        response_headers.append(('Content-Type', 'text/html'))

    elif environ['PATH_INFO'].startswith("/debug/"):
        response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
        response_body = ['\n'.join(response_body)]
        response_headers.append(('Content-Type', 'text/plain'))

    else: #call default view
        ret = core.web_call(environ)
        response_body.extend(ret["body"])
        response_headers.extend(ret["header"])
        response_headers.append(('Content-Type', 'text/html; charset=utf-8'))


    # So the content-lenght is the sum of all string's lengths
    content_length = 0
    for s in response_body:
        content_length += len(s)

    response_headers.append(('Content-Length', str(content_length)))

    status = '200 OK'

    start_response(status, response_headers)

    return response_body
