<?php
  header('Content-type: text/javascript');
?>

var scripttags = new Array();

function scvrendermodules(obj) {
  var jsfunclist = new Array();
  for (var i in obj.modules) {
    document.getElementById("s" + obj.modules[i].s).innerHTML = obj.modules[i].c;
    if(typeof(obj.modules[i].j) != "undefined") {
      if(typeof(scripttags[obj.modules[i].s]) == "object") {
          eval("s" + obj.modules[i].s + "w" + scripttags[obj.modules[i].s][1].id + ".destroy()");
          document.body.removeChild(scripttags[obj.modules[i].s][0]);
      }
      var script = document.createElement("script");
      var type = document.createAttribute("type");
      type.nodeValue = "text/javascript";
      script.setAttributeNode(type);
      document.body.appendChild(script);
      script.innerHTML = obj.modules[i].j;
      jsfunclist.push("s" + obj.modules[i].s + "w" + obj.modules[i].id + ".init()");
      scripttags[obj.modules[i].s] = new Array(script,obj.modules[i]);
    }
  }
  return jsfunclist;
}

function scvajax() {
  this.request;
  
  this.init = function() {
    try {
      this.request = new XMLHttpRequest();
    } catch (msxml2failure) {
      try {
        this.request = new ActiveXObject("Msxml2.XMLHTTP");
      } catch (msfailure) {
        try {
          this.request = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (failure) {
          this.request = false;
        }
      }
    }
    if(!this.request) {
      alert("Your browser doesn't support XMLHttpRequest! Please update your browser.");
    }
  }
  
  this.send = function(json) {
    if(this.request != false) {
      if(typeof(json) == "object") { 
        this.request.open("POST","request.php",true);
        this.request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        this.request.setRequestHeader("Content-length", JSON.stringify(json, null).length);
        this.request.setRequestHeader("Connection", "close");
        this.request.onreadystatechange = this.get(this);
        this.request.send("data=" + JSON.stringify(json, null));
      }
    }
  }
  
  this.get = function(me) {
    return function(){
      if(me.request.readyState == 4) {
        var obj = JSON.parse(me.request.responseText);
        switch(obj.t) {
          case "m":
            var jsfunclist = scvrendermodules(obj);
            for (var i in jsfunclist) {
              window.setTimeout(jsfunclist[i], 0);
            }
        }
      }
    }
  }

}

function action(actionlistid) {
  var ajax = new scvajax();
  ajax.init();
  ajax.send({"t":"a","id":actionlistid});
}


var request = new scvajax();
request.init();
request.send({"t":"i","part":"site","id":sitid});

