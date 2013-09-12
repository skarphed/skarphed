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

SkdAjax = 
    constructor: ->
        if (typeof @XMLHttpRequest == "undefined")
            console.log 'XMLHttpRequest is undefined'
            @XMLHttpRequest = ->
                try
                    return new ActiveXObject("Msxml2.XMLHTTP.6.0")
                catch error
                try
                    return new ActiveXObject("Msxml2.XMLHTTP.3.0")
                catch error
                try
                    return new ActiveXObject("Microsoft.XMLHTTP")
                catch error
                throw new Error("This browser does not support XMLHttpRequest.")


    execute_action: (jsonstring) ->
        actionlist = JSON.parse jsonstring
        this.single_action action for action in actionlist

    single_action: (action) ->
        req = new XMLHttpRequest()
        req.targetSpace = action.s
        req.addEventListener 'readystatechange', ->
            if req.readyState is 4
                success_resultcodes = [200,304]
                if req.state in success_resultcodes
                    space = document.getElementById "space_"+req.targetSpace 
                    space.innerHTML = req.responseText
                else
                    console.log "Error Loading File"
        delete(action.s)
        req.open 'GET', '/ajax/'+JSON.toString(action)
        req.send()

SkdAJAX = new SkdAjax()

