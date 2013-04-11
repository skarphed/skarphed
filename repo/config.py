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

import json

class Config(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __getitem__(self, key):
        return self.config[key]

    def load_from_file(self, path = 'config.json'):
        f = open(path, 'r')
        data = f.read()
        f.close()
        self.config = json.loads(data)


Config().load_from_file('/etc/scvrepo/config.json')
