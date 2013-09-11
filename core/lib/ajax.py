#!/usr/bin/python
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

from json import JSONDecoder, JSONEncoder

class AJAXHandler(object):
    """
    This shit handles all shit that is AJAX and shit
    """
    def __init__(self, core, callstring):
        """
        Initialize
        """
        self._core = core

        decoder = JSONDecoder()
        call = decoder.loads(callstring)

        self._widget_id = call["w"]
        self._params = {}
        if call.has_key("p") and type(call["p"]) == dict:
            self._params.update(call["p"])

    def get_answer(self):
        """
        Handles an AJAX call
        """
        module_manager = self._core.get_module_manager()
        module = module_manager.get_module_from_widget_id(self._widget_id)
        html = module.render_html(self._widget_id, self._params)
        js   = module.render_javascript(self._widget_id, self._params)
        answer = {'h':html, 'j':js}
        encoder = JSONEncoder()
        answer = encoder.dumps(answer)
        return answer

