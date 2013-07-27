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

import json

class Config(object):
    """
    Provides a global accessibly configuration.
    """
    # shared state for borg pattern
    __shared_state = {} 

    def __init__(self):
        """
        Initializes a configuration object with the shared state.
        """
        self.__dict__ = self.__shared_state

    def __getitem__(self, key):
        """
        Returns the value of the configuration entry with the given key.
        """
        return self.config[key]

    def load_from_file(self, path):
        """
        Loads the configuration from a json file.
        """
        f = open(path, 'r')
        data = f.read()
        f.close()
        self.config = json.loads(data)


# loads the default repository configuration
Config().load_from_file('/etc/skdrepo/config.json')
