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

from mimetypes import guess_type

class SharedDataMiddleware(object):
    def __init__(self, wrap_app, location):
        self._location = location
        self._wrap_app = wrap_app

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/%s/' % self._location):
            prefix = "/usr/share/scvrepo/"
            path = prefix + environ['PATH_INFO'][1:]
            try:
                f = open(path, 'r')
                data = f.read()
                f.close()
                (mime, encoding) = guess_type(path)
                status = '200 OK'  
                response_headers = [('Content-Type', mime)]
                response_body = [data]
            except IOError, e:
                status = '404 Not Found'
                response_headers = [('Content-Type', 'text/plain')]
                response_body = ['404 Not Found - \'%s\'' % path]

            start_response(status, response_headers)
            return response_body

        else:
            return self._wrap_app(environ, start_response)

