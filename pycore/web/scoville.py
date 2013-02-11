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

   response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
   response_body = '\n'.join(response_body)

   # Response_body has now more than one string
   response_body = ['The Beggining\n',
                    '*' * 30 + '\n',
                    response_body,
                    '\n' + '*' * 30 ,
                    '\nThe End']


   if environ['PATH_INFO'].startswith("/static_"):
      response_body.append("\nMust return static stuff!\n")
   elif environ['PATH_INFO'].startswith("/rpc_"):
      response_body.append("\nDo RPC Request")
   elif environ['PATH_INFO'].startswith("/v_"):
      response_body.append("\nRender View")
      core = Core(cfg)

   # So the content-lenght is the sum of all string's lengths
   content_length = 0
   for s in response_body:
      content_length += len(s)

   status = '200 OK'
   response_headers = [('Content-Type', 'text/plain'),
                  ('Content-Length', str(content_length))]
   start_response(status, response_headers)

   return response_body
