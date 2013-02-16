#!/usr/bin/python
#-*- coding: utf-8 -*-

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

from json import JSONDecoder, JSONEncoder

class Rpc(object):
    def __init__(self, core):
        self._core = core

    def __call__(self, instructions):
        jd = JSONDecoder()
        je = JSONEncoder()
        answer = {}
        try:
            instructions = jd.decode(instructions)
        except ValueError, e:
            answer['error'] = "could not decode instructions"
            self._core.response_body.append(je.encode(answer))
            return

        method = instructions['method']
        params = instructions['params']
        try:
            exec "res = self.%s(params)"%method
        except AttributeError,e :
            answer['error'] = "The Rpc-backed does not support this method %s"%method
            self._core.response_body.append(je.encode(answer))
            return
        except Exception, e:
            answer['error'] = "Exception: %s"%repr(e)
            self._core.response_body.append(je.encode(answer))
            return
        else:
            answer['result'] = res
            self._core.response_body.append(je.encode(answer))
    
    # RPC - Method-Implementations____________________________

    def getServerInfo(self,params):
        return self._core.get_configuration().get_entry("core.name")

    def authenticateUser(self,params):
        username = params[0]
        password = params[1]

        user_manager = self._core.get_user_manager()
        user = user_manager.get_user_by_name(username)

        if user.authenticate(password):
            pass

