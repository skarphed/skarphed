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

import json

class AJAXHandler(object):
    """
    This shit handles all shit that is AJAX and shit
    """
    def __init__(self, core, callstring):
        """
        Initialize
        """
        self._core = core

        call = json.loads(callstring)

        self._widget_id = call["w"]
        self._params = {}
        if call.has_key("p") and type(call["p"]) == dict:
            self._params.update(call["p"])

    def get_answer(self):
        """
        Handles an AJAX call
        """
        module_manager = self._core.get_module_manager()
        widget = module_manager.get_widget(self._widget_id)
        html = widget.render_html(self._params)
        js   = widget.render_javascript(self._params)
        answer = {'h':html, 'j':js}
        answer = json.dumps(answer)
        return answer

AJAXScript = """
(function() {
  var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  this.SkdAJAX = {
    execute_action: function(actionlist) {
      var action, _i, _len;
      for (_i = 0, _len = actionlist.length; _i < _len; _i++) {
        action = actionlist[_i];
        this.single_action(action);
      }
      return void 0;
    },
    single_action: function(action) {
      var req, url;
      if (typeof this.XMLHttpRequest === "undefined") {
        console.log('XMLHttpRequest is undefined');
        this.XMLHttpRequest = function() {
          var error;
          try {
            return new ActiveXObject("Msxml2.XMLHTTP.6.0");
          } catch (_error) {
            error = _error;
          }
          try {
            return new ActiveXObject("Msxml2.XMLHTTP.3.0");
          } catch (_error) {
            error = _error;
          }
          try {
            return new ActiveXObject("Microsoft.XMLHTTP");
          } catch (_error) {
            error = _error;
          }
          throw new Error("This browser does not support XMLHttpRequest.");
        };
      }
      req = new XMLHttpRequest();
      req.targetSpace = action.s;
      req.widgetId = action.w;
      req.addEventListener('readystatechange', function() {
        var response, space, success_resultcodes, widget_script, _ref;
        if (req.readyState === 4) {
          success_resultcodes = [200, 304];
          if (_ref = req.status, __indexOf.call(success_resultcodes, _ref) >= 0) {
            space = document.getElementById("space_" + req.targetSpace);
            widget_script = document.getElementById(req.widgetId + "_scr");
            response = JSON.parse(req.responseText);
            space.innerHTML = response.h;
            return widget_script.innerHTML = response.j;
          } else {
            return console.log("Error Loading Content");
          }
        }
      });
      delete action.s;
      url = '/ajax/' + JSON.stringify(action);
      req.open('GET', url, true);
      return req.send(null);
    }
  };

}).call(this);
"""