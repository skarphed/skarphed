(function(){

if (!window.qx) window.qx = {};

qx.$$start = new Date();
  
if (!qx.$$environment) qx.$$environment = {};
var envinfo = {"qx.application":"scoville_admin.Application","qx.debug":false,"qx.optimization.basecalls":true,"qx.optimization.comments":true,"qx.optimization.privates":true,"qx.optimization.strings":true,"qx.optimization.variables":true,"qx.optimization.variants":true,"qx.revision":"381","qx.theme":"scoville_admin.theme.Theme","qx.version":"1.5"};
for (var k in envinfo) qx.$$environment[k] = envinfo[k];

if (!qx.$$libraries) qx.$$libraries = {};
var libinfo = {"__out__":{"sourceUri":"script"},"qx":{"resourceUri":"resource","sourceUri":"script","version":"1.5"},"scoville_admin":{"resourceUri":"resource","sourceUri":"script","version":"trunk"}};
for (var k in libinfo) qx.$$libraries[k] = libinfo[k];

qx.$$resources = {};
qx.$$translations = {};
qx.$$locales = {};
qx.$$packageData = {};

qx.$$loader = {
  parts : {"boot":[0]},
  packages : {"0":{"uris":["__out__:scoville_admin.dd3bba85ee91.js"]}},
  urisBefore : [],
  cssBefore : [],
  boot : "boot",
  closureParts : {},
  bootIsInline : true,
  addNoCacheParam : false,
  
  decodeUris : function(compressedUris)
  {
    var libs = qx.$$libraries;
    var uris = [];
    for (var i=0; i<compressedUris.length; i++)
    {
      var uri = compressedUris[i].split(":");
      var euri;
      if (uri.length==2 && uri[0] in libs) {
        var prefix = libs[uri[0]].sourceUri;
        euri = prefix + "/" + uri[1];
      } else {
        euri = compressedUris[i];
      }
      if (qx.$$loader.addNoCacheParam) {
        euri += "?nocache=" + Math.random();
      }
      
      uris.push(euri);
    }
    return uris;      
  }
};  

function loadScript(uri, callback) {
  var elem = document.createElement("script");
  elem.charset = "utf-8";
  elem.src = uri;
  elem.onreadystatechange = elem.onload = function() {
    if (!this.readyState || this.readyState == "loaded" || this.readyState == "complete") {
      elem.onreadystatechange = elem.onload = null;
      callback();
    }
  };
  var head = document.getElementsByTagName("head")[0];
  head.appendChild(elem);
}

function loadCss(uri) {
  var elem = document.createElement("link");
  elem.rel = "stylesheet";
  elem.type= "text/css";
  elem.href= uri;
  var head = document.getElementsByTagName("head")[0];
  head.appendChild(elem);
}

var isWebkit = /AppleWebKit\/([^ ]+)/.test(navigator.userAgent);

function loadScriptList(list, callback) {
  if (list.length == 0) {
    callback();
    return;
  }
  var item = list.shift();
  loadScript(item,  function() {
    if (isWebkit) {
      // force async, else Safari fails with a "maximum recursion depth exceeded"
      window.setTimeout(function() {
        loadScriptList(list, callback);
      }, 0);
    } else {
      loadScriptList(list, callback);
    }
  });
}

var fireContentLoadedEvent = function() {
  qx.$$domReady = true;
  document.removeEventListener('DOMContentLoaded', fireContentLoadedEvent, false);
};
if (document.addEventListener) {
  document.addEventListener('DOMContentLoaded', fireContentLoadedEvent, false);
}

qx.$$loader.importPackageData = function (dataMap, callback) {
  if (dataMap["resources"]){
    var resMap = dataMap["resources"];
    for (var k in resMap) qx.$$resources[k] = resMap[k];
  }
  if (dataMap["locales"]){
    var locMap = dataMap["locales"];
    var qxlocs = qx.$$locales;
    for (var lang in locMap){
      if (!qxlocs[lang]) qxlocs[lang] = locMap[lang];
      else 
        for (var k in locMap[lang]) qxlocs[lang][k] = locMap[lang][k];
    }
  }
  if (dataMap["translations"]){
    var trMap   = dataMap["translations"];
    var qxtrans = qx.$$translations;
    for (var lang in trMap){
      if (!qxtrans[lang]) qxtrans[lang] = trMap[lang];
      else 
        for (var k in trMap[lang]) qxtrans[lang][k] = trMap[lang][k];
    }
  }
  if (callback){
    callback(dataMap);
  }
}

qx.$$loader.signalStartup = function () 
{
  qx.$$loader.scriptLoaded = true;
  if (window.qx && qx.event && qx.event.handler && qx.event.handler.Application) {
    qx.event.handler.Application.onScriptLoaded();
    qx.$$loader.applicationHandlerReady = true; 
  } else {
    qx.$$loader.applicationHandlerReady = false;
  }
}

// Load all stuff
qx.$$loader.init = function(){
  var l=qx.$$loader;
  if (l.cssBefore.length>0) {
    for (var i=0, m=l.cssBefore.length; i<m; i++) {
      loadCss(l.cssBefore[i]);
    }
  }
  if (l.urisBefore.length>0){
    loadScriptList(l.urisBefore, function(){
      l.initUris();
    });
  } else {
    l.initUris();
  }
}

// Load qooxdoo boot stuff
qx.$$loader.initUris = function(){
  var l=qx.$$loader;
  var bootPackageHash=l.parts[l.boot][0];
  if (l.bootIsInline){
    l.importPackageData(qx.$$packageData[bootPackageHash]);
    l.signalStartup();
  } else {
    loadScriptList(l.decodeUris(l.packages[l.parts[l.boot][0]].uris), function(){
      // Opera needs this extra time to parse the scripts
      window.setTimeout(function(){
        l.importPackageData(qx.$$packageData[bootPackageHash] || {});
        l.signalStartup();
      }, 0);
    });
  }
}
})();

qx.$$packageData['0']={"locales":{"C":{"alternateQuotationEnd":"’","alternateQuotationStart":"‘","cldr_am":"AM","cldr_date_format_full":"EEEE, MMMM d, y","cldr_date_format_long":"MMMM d, y","cldr_date_format_medium":"MMM d, y","cldr_date_format_short":"M/d/yy","cldr_date_time_format_EEEd":"d EEE","cldr_date_time_format_Hm":"HH:mm","cldr_date_time_format_Hms":"HH:mm:ss","cldr_date_time_format_M":"L","cldr_date_time_format_MEd":"E, M/d","cldr_date_time_format_MMM":"LLL","cldr_date_time_format_MMMEd":"E, MMM d","cldr_date_time_format_MMMd":"MMM d","cldr_date_time_format_Md":"M/d","cldr_date_time_format_d":"d","cldr_date_time_format_hm":"h:mm a","cldr_date_time_format_hms":"h:mm:ss a","cldr_date_time_format_ms":"mm:ss","cldr_date_time_format_y":"y","cldr_date_time_format_yM":"M/y","cldr_date_time_format_yMEd":"EEE, M/d/y","cldr_date_time_format_yMMM":"MMM y","cldr_date_time_format_yMMMEd":"EEE, MMM d, y","cldr_date_time_format_yMMMd":"MMM d, y","cldr_date_time_format_yMd":"M/d/y","cldr_date_time_format_yQ":"Q y","cldr_date_time_format_yQQQ":"QQQ y","cldr_day_format_abbreviated_fri":"Fri","cldr_day_format_abbreviated_mon":"Mon","cldr_day_format_abbreviated_sat":"Sat","cldr_day_format_abbreviated_sun":"Sun","cldr_day_format_abbreviated_thu":"Thu","cldr_day_format_abbreviated_tue":"Tue","cldr_day_format_abbreviated_wed":"Wed","cldr_day_format_wide_fri":"Friday","cldr_day_format_wide_mon":"Monday","cldr_day_format_wide_sat":"Saturday","cldr_day_format_wide_sun":"Sunday","cldr_day_format_wide_thu":"Thursday","cldr_day_format_wide_tue":"Tuesday","cldr_day_format_wide_wed":"Wednesday","cldr_day_stand-alone_narrow_fri":"F","cldr_day_stand-alone_narrow_mon":"M","cldr_day_stand-alone_narrow_sat":"S","cldr_day_stand-alone_narrow_sun":"S","cldr_day_stand-alone_narrow_thu":"T","cldr_day_stand-alone_narrow_tue":"T","cldr_day_stand-alone_narrow_wed":"W","cldr_month_format_abbreviated_1":"Jan","cldr_month_format_abbreviated_10":"Oct","cldr_month_format_abbreviated_11":"Nov","cldr_month_format_abbreviated_12":"Dec","cldr_month_format_abbreviated_2":"Feb","cldr_month_format_abbreviated_3":"Mar","cldr_month_format_abbreviated_4":"Apr","cldr_month_format_abbreviated_5":"May","cldr_month_format_abbreviated_6":"Jun","cldr_month_format_abbreviated_7":"Jul","cldr_month_format_abbreviated_8":"Aug","cldr_month_format_abbreviated_9":"Sep","cldr_month_format_wide_1":"January","cldr_month_format_wide_10":"October","cldr_month_format_wide_11":"November","cldr_month_format_wide_12":"December","cldr_month_format_wide_2":"February","cldr_month_format_wide_3":"March","cldr_month_format_wide_4":"April","cldr_month_format_wide_5":"May","cldr_month_format_wide_6":"June","cldr_month_format_wide_7":"July","cldr_month_format_wide_8":"August","cldr_month_format_wide_9":"September","cldr_month_stand-alone_narrow_1":"J","cldr_month_stand-alone_narrow_10":"O","cldr_month_stand-alone_narrow_11":"N","cldr_month_stand-alone_narrow_12":"D","cldr_month_stand-alone_narrow_2":"F","cldr_month_stand-alone_narrow_3":"M","cldr_month_stand-alone_narrow_4":"A","cldr_month_stand-alone_narrow_5":"M","cldr_month_stand-alone_narrow_6":"J","cldr_month_stand-alone_narrow_7":"J","cldr_month_stand-alone_narrow_8":"A","cldr_month_stand-alone_narrow_9":"S","cldr_number_decimal_separator":".","cldr_number_group_separator":",","cldr_number_percent_format":"#,##0%","cldr_pm":"PM","cldr_time_format_full":"h:mm:ss a zzzz","cldr_time_format_long":"h:mm:ss a z","cldr_time_format_medium":"h:mm:ss a","cldr_time_format_short":"h:mm a","day":"Day","dayperiod":"AM/PM","era":"Era","hour":"Hour","minute":"Minute","month":"Month","quotationEnd":"”","quotationStart":"“","second":"Second","week":"Week","weekday":"Day of the Week","year":"Year","zone":"Time Zone"},"en":{"alternateQuotationEnd":"’","alternateQuotationStart":"‘","cldr_am":"AM","cldr_date_format_full":"EEEE, MMMM d, y","cldr_date_format_long":"MMMM d, y","cldr_date_format_medium":"MMM d, y","cldr_date_format_short":"M/d/yy","cldr_date_time_format_EEEd":"d EEE","cldr_date_time_format_Hm":"HH:mm","cldr_date_time_format_Hms":"HH:mm:ss","cldr_date_time_format_M":"L","cldr_date_time_format_MEd":"E, M/d","cldr_date_time_format_MMM":"LLL","cldr_date_time_format_MMMEd":"E, MMM d","cldr_date_time_format_MMMd":"MMM d","cldr_date_time_format_Md":"M/d","cldr_date_time_format_d":"d","cldr_date_time_format_hm":"h:mm a","cldr_date_time_format_hms":"h:mm:ss a","cldr_date_time_format_ms":"mm:ss","cldr_date_time_format_y":"y","cldr_date_time_format_yM":"M/y","cldr_date_time_format_yMEd":"EEE, M/d/y","cldr_date_time_format_yMMM":"MMM y","cldr_date_time_format_yMMMEd":"EEE, MMM d, y","cldr_date_time_format_yMMMd":"MMM d, y","cldr_date_time_format_yMd":"M/d/y","cldr_date_time_format_yQ":"Q y","cldr_date_time_format_yQQQ":"QQQ y","cldr_day_format_abbreviated_fri":"Fri","cldr_day_format_abbreviated_mon":"Mon","cldr_day_format_abbreviated_sat":"Sat","cldr_day_format_abbreviated_sun":"Sun","cldr_day_format_abbreviated_thu":"Thu","cldr_day_format_abbreviated_tue":"Tue","cldr_day_format_abbreviated_wed":"Wed","cldr_day_format_wide_fri":"Friday","cldr_day_format_wide_mon":"Monday","cldr_day_format_wide_sat":"Saturday","cldr_day_format_wide_sun":"Sunday","cldr_day_format_wide_thu":"Thursday","cldr_day_format_wide_tue":"Tuesday","cldr_day_format_wide_wed":"Wednesday","cldr_day_stand-alone_narrow_fri":"F","cldr_day_stand-alone_narrow_mon":"M","cldr_day_stand-alone_narrow_sat":"S","cldr_day_stand-alone_narrow_sun":"S","cldr_day_stand-alone_narrow_thu":"T","cldr_day_stand-alone_narrow_tue":"T","cldr_day_stand-alone_narrow_wed":"W","cldr_month_format_abbreviated_1":"Jan","cldr_month_format_abbreviated_10":"Oct","cldr_month_format_abbreviated_11":"Nov","cldr_month_format_abbreviated_12":"Dec","cldr_month_format_abbreviated_2":"Feb","cldr_month_format_abbreviated_3":"Mar","cldr_month_format_abbreviated_4":"Apr","cldr_month_format_abbreviated_5":"May","cldr_month_format_abbreviated_6":"Jun","cldr_month_format_abbreviated_7":"Jul","cldr_month_format_abbreviated_8":"Aug","cldr_month_format_abbreviated_9":"Sep","cldr_month_format_wide_1":"January","cldr_month_format_wide_10":"October","cldr_month_format_wide_11":"November","cldr_month_format_wide_12":"December","cldr_month_format_wide_2":"February","cldr_month_format_wide_3":"March","cldr_month_format_wide_4":"April","cldr_month_format_wide_5":"May","cldr_month_format_wide_6":"June","cldr_month_format_wide_7":"July","cldr_month_format_wide_8":"August","cldr_month_format_wide_9":"September","cldr_month_stand-alone_narrow_1":"J","cldr_month_stand-alone_narrow_10":"O","cldr_month_stand-alone_narrow_11":"N","cldr_month_stand-alone_narrow_12":"D","cldr_month_stand-alone_narrow_2":"F","cldr_month_stand-alone_narrow_3":"M","cldr_month_stand-alone_narrow_4":"A","cldr_month_stand-alone_narrow_5":"M","cldr_month_stand-alone_narrow_6":"J","cldr_month_stand-alone_narrow_7":"J","cldr_month_stand-alone_narrow_8":"A","cldr_month_stand-alone_narrow_9":"S","cldr_number_decimal_separator":".","cldr_number_group_separator":",","cldr_number_percent_format":"#,##0%","cldr_pm":"PM","cldr_time_format_full":"h:mm:ss a zzzz","cldr_time_format_long":"h:mm:ss a z","cldr_time_format_medium":"h:mm:ss a","cldr_time_format_short":"h:mm a","day":"Day","dayperiod":"AM/PM","era":"Era","hour":"Hour","minute":"Minute","month":"Month","quotationEnd":"”","quotationStart":"“","second":"Second","week":"Week","weekday":"Day of the Week","year":"Year","zone":"Time Zone"}},"resources":{"qx/decoration/Modern/app-header.png":[110,20,"png","qx"],"qx/decoration/Modern/arrows-combined.png":[87,8,"png","qx"],"qx/decoration/Modern/arrows/down-invert.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-74,0],"qx/decoration/Modern/arrows/down-small-invert.png":[5,3,"png","qx","qx/decoration/Modern/arrows-combined.png",-69,0],"qx/decoration/Modern/arrows/down-small.png":[5,3,"png","qx","qx/decoration/Modern/arrows-combined.png",-49,0],"qx/decoration/Modern/arrows/down.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-20,0],"qx/decoration/Modern/arrows/forward.png":[10,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-59,0],"qx/decoration/Modern/arrows/left-invert.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",0,0],"qx/decoration/Modern/arrows/left.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-44,0],"qx/decoration/Modern/arrows/rewind.png":[10,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-10,0],"qx/decoration/Modern/arrows/right-invert.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-5,0],"qx/decoration/Modern/arrows/right.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-54,0],"qx/decoration/Modern/arrows/up-invert.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-28,0],"qx/decoration/Modern/arrows/up-small.png":[5,3,"png","qx","qx/decoration/Modern/arrows-combined.png",-82,0],"qx/decoration/Modern/arrows/up.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-36,0],"qx/decoration/Modern/button-lr-combined.png":[72,52,"png","qx"],"qx/decoration/Modern/button-tb-combined.png":[4,216,"png","qx"],"qx/decoration/Modern/checkradio-combined.png":[504,14,"png","qx"],"qx/decoration/Modern/colorselector-combined.gif":[46,11,"gif","qx"],"qx/decoration/Modern/colorselector/brightness-field.png":[19,256,"png","qx"],"qx/decoration/Modern/colorselector/brightness-handle.gif":[35,11,"gif","qx","qx/decoration/Modern/colorselector-combined.gif",0,0],"qx/decoration/Modern/colorselector/huesaturation-field.jpg":[256,256,"jpeg","qx"],"qx/decoration/Modern/colorselector/huesaturation-handle.gif":[11,11,"gif","qx","qx/decoration/Modern/colorselector-combined.gif",-35,0],"qx/decoration/Modern/cursors-combined.gif":[71,20,"gif","qx"],"qx/decoration/Modern/cursors/alias.gif":[19,15,"gif","qx","qx/decoration/Modern/cursors-combined.gif",-52,0],"qx/decoration/Modern/cursors/copy.gif":[19,15,"gif","qx","qx/decoration/Modern/cursors-combined.gif",-33,0],"qx/decoration/Modern/cursors/move.gif":[13,9,"gif","qx","qx/decoration/Modern/cursors-combined.gif",-20,0],"qx/decoration/Modern/cursors/nodrop.gif":[20,20,"gif","qx","qx/decoration/Modern/cursors-combined.gif",0,0],"qx/decoration/Modern/form/button-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-72],"qx/decoration/Modern/form/button-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-204],"qx/decoration/Modern/form/button-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-188],"qx/decoration/Modern/form/button-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-checked-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-36],"qx/decoration/Modern/form/button-checked-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-84],"qx/decoration/Modern/form/button-checked-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-184],"qx/decoration/Modern/form/button-checked-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-checked-focused-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-156],"qx/decoration/Modern/form/button-checked-focused-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-208],"qx/decoration/Modern/form/button-checked-focused-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-160],"qx/decoration/Modern/form/button-checked-focused-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-checked-focused-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-40,0],"qx/decoration/Modern/form/button-checked-focused-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-32,0],"qx/decoration/Modern/form/button-checked-focused-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-28],"qx/decoration/Modern/form/button-checked-focused-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-24],"qx/decoration/Modern/form/button-checked-focused-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-48],"qx/decoration/Modern/form/button-checked-focused.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-checked-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-16,0],"qx/decoration/Modern/form/button-checked-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-60,0],"qx/decoration/Modern/form/button-checked-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-140],"qx/decoration/Modern/form/button-checked-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-56],"qx/decoration/Modern/form/button-checked-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-112],"qx/decoration/Modern/form/button-checked.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-disabled-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-40],"qx/decoration/Modern/form/button-disabled-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-136],"qx/decoration/Modern/form/button-disabled-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-16],"qx/decoration/Modern/form/button-disabled-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-disabled-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-68,0],"qx/decoration/Modern/form/button-disabled-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-4,0],"qx/decoration/Modern/form/button-disabled-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-116],"qx/decoration/Modern/form/button-disabled-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-168],"qx/decoration/Modern/form/button-disabled-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-60],"qx/decoration/Modern/form/button-disabled.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-focused-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-68],"qx/decoration/Modern/form/button-focused-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-144],"qx/decoration/Modern/form/button-focused-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-8],"qx/decoration/Modern/form/button-focused-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-focused-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-24,0],"qx/decoration/Modern/form/button-focused-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-44,0],"qx/decoration/Modern/form/button-focused-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-192],"qx/decoration/Modern/form/button-focused-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-148],"qx/decoration/Modern/form/button-focused-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-104],"qx/decoration/Modern/form/button-focused.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-hovered-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-108],"qx/decoration/Modern/form/button-hovered-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-32],"qx/decoration/Modern/form/button-hovered-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-128],"qx/decoration/Modern/form/button-hovered-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-hovered-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-20,0],"qx/decoration/Modern/form/button-hovered-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-48,0],"qx/decoration/Modern/form/button-hovered-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-44],"qx/decoration/Modern/form/button-hovered-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-76],"qx/decoration/Modern/form/button-hovered-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-88],"qx/decoration/Modern/form/button-hovered.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-56,0],"qx/decoration/Modern/form/button-preselected-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-124],"qx/decoration/Modern/form/button-preselected-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-176],"qx/decoration/Modern/form/button-preselected-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-200],"qx/decoration/Modern/form/button-preselected-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-preselected-focused-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,0],"qx/decoration/Modern/form/button-preselected-focused-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-4],"qx/decoration/Modern/form/button-preselected-focused-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-152],"qx/decoration/Modern/form/button-preselected-focused-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-preselected-focused-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-28,0],"qx/decoration/Modern/form/button-preselected-focused-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-36,0],"qx/decoration/Modern/form/button-preselected-focused-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-196],"qx/decoration/Modern/form/button-preselected-focused-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-164],"qx/decoration/Modern/form/button-preselected-focused-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-212],"qx/decoration/Modern/form/button-preselected-focused.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-preselected-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-8,0],"qx/decoration/Modern/form/button-preselected-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-64,0],"qx/decoration/Modern/form/button-preselected-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-96],"qx/decoration/Modern/form/button-preselected-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-80],"qx/decoration/Modern/form/button-preselected-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-132],"qx/decoration/Modern/form/button-preselected.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-pressed-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-12],"qx/decoration/Modern/form/button-pressed-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-52],"qx/decoration/Modern/form/button-pressed-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-20],"qx/decoration/Modern/form/button-pressed-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-pressed-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-52,0],"qx/decoration/Modern/form/button-pressed-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-12,0],"qx/decoration/Modern/form/button-pressed-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-100],"qx/decoration/Modern/form/button-pressed-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-172],"qx/decoration/Modern/form/button-pressed-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-64],"qx/decoration/Modern/form/button-pressed.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",0,0],"qx/decoration/Modern/form/button-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-92],"qx/decoration/Modern/form/button-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-120],"qx/decoration/Modern/form/button-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-180],"qx/decoration/Modern/form/button.png":[80,60,"png","qx"],"qx/decoration/Modern/form/checkbox-checked-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-126,0],"qx/decoration/Modern/form/checkbox-checked-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-322,0],"qx/decoration/Modern/form/checkbox-checked-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-294,0],"qx/decoration/Modern/form/checkbox-checked-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-364,0],"qx/decoration/Modern/form/checkbox-checked-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-490,0],"qx/decoration/Modern/form/checkbox-checked-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-224,0],"qx/decoration/Modern/form/checkbox-checked-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-378,0],"qx/decoration/Modern/form/checkbox-checked-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-84,0],"qx/decoration/Modern/form/checkbox-checked.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-182,0],"qx/decoration/Modern/form/checkbox-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-42,0],"qx/decoration/Modern/form/checkbox-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-392,0],"qx/decoration/Modern/form/checkbox-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-210,0],"qx/decoration/Modern/form/checkbox-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-14,0],"qx/decoration/Modern/form/checkbox-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-238,0],"qx/decoration/Modern/form/checkbox-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-462,0],"qx/decoration/Modern/form/checkbox-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-112,0],"qx/decoration/Modern/form/checkbox-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-448,0],"qx/decoration/Modern/form/checkbox-undetermined-disabled.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-focused-invalid.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-focused.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-hovered-invalid.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-hovered.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-invalid.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-140,0],"qx/decoration/Modern/form/checked-disabled.png":[6,6,"png","qx"],"qx/decoration/Modern/form/checked.png":[6,6,"png","qx"],"qx/decoration/Modern/form/input-focused.png":[40,12,"png","qx"],"qx/decoration/Modern/form/input.png":[84,12,"png","qx"],"qx/decoration/Modern/form/radiobutton-checked-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-196,0],"qx/decoration/Modern/form/radiobutton-checked-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-168,0],"qx/decoration/Modern/form/radiobutton-checked-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-98,0],"qx/decoration/Modern/form/radiobutton-checked-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-308,0],"qx/decoration/Modern/form/radiobutton-checked-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-406,0],"qx/decoration/Modern/form/radiobutton-checked-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-28,0],"qx/decoration/Modern/form/radiobutton-checked-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-350,0],"qx/decoration/Modern/form/radiobutton-checked-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-266,0],"qx/decoration/Modern/form/radiobutton-checked.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-252,0],"qx/decoration/Modern/form/radiobutton-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-336,0],"qx/decoration/Modern/form/radiobutton-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-476,0],"qx/decoration/Modern/form/radiobutton-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-420,0],"qx/decoration/Modern/form/radiobutton-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-56,0],"qx/decoration/Modern/form/radiobutton-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",0,0],"qx/decoration/Modern/form/radiobutton-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-154,0],"qx/decoration/Modern/form/radiobutton-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-434,0],"qx/decoration/Modern/form/radiobutton-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-280,0],"qx/decoration/Modern/form/radiobutton.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-70,0],"qx/decoration/Modern/form/tooltip-error-arrow.png":[11,14,"png","qx"],"qx/decoration/Modern/form/tooltip-error-b.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-30],"qx/decoration/Modern/form/tooltip-error-bl.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-24],"qx/decoration/Modern/form/tooltip-error-br.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,0],"qx/decoration/Modern/form/tooltip-error-c.png":[40,18,"png","qx"],"qx/decoration/Modern/form/tooltip-error-l.png":[6,18,"png","qx","qx/decoration/Modern/tooltip-error-lr-combined.png",-6,0],"qx/decoration/Modern/form/tooltip-error-r.png":[6,18,"png","qx","qx/decoration/Modern/tooltip-error-lr-combined.png",0,0],"qx/decoration/Modern/form/tooltip-error-t.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-6],"qx/decoration/Modern/form/tooltip-error-tl.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-18],"qx/decoration/Modern/form/tooltip-error-tr.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-12],"qx/decoration/Modern/form/tooltip-error.png":[127,30,"png","qx"],"qx/decoration/Modern/form/undetermined-disabled.png":[6,2,"png","qx"],"qx/decoration/Modern/form/undetermined.png":[6,2,"png","qx"],"qx/decoration/Modern/group-item.png":[110,20,"png","qx"],"qx/decoration/Modern/groupbox-lr-combined.png":[8,51,"png","qx"],"qx/decoration/Modern/groupbox-tb-combined.png":[4,24,"png","qx"],"qx/decoration/Modern/groupbox/groupbox-b.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-12],"qx/decoration/Modern/groupbox/groupbox-bl.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-16],"qx/decoration/Modern/groupbox/groupbox-br.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-8],"qx/decoration/Modern/groupbox/groupbox-c.png":[40,51,"png","qx"],"qx/decoration/Modern/groupbox/groupbox-l.png":[4,51,"png","qx","qx/decoration/Modern/groupbox-lr-combined.png",-4,0],"qx/decoration/Modern/groupbox/groupbox-r.png":[4,51,"png","qx","qx/decoration/Modern/groupbox-lr-combined.png",0,0],"qx/decoration/Modern/groupbox/groupbox-t.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-4],"qx/decoration/Modern/groupbox/groupbox-tl.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,0],"qx/decoration/Modern/groupbox/groupbox-tr.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-20],"qx/decoration/Modern/groupbox/groupbox.png":[255,59,"png","qx"],"qx/decoration/Modern/menu-background-combined.png":[80,49,"png","qx"],"qx/decoration/Modern/menu-checkradio-combined.gif":[64,7,"gif","qx"],"qx/decoration/Modern/menu/background.png":[40,49,"png","qx","qx/decoration/Modern/menu-background-combined.png",-40,0],"qx/decoration/Modern/menu/bar-background.png":[40,20,"png","qx","qx/decoration/Modern/menu-background-combined.png",0,0],"qx/decoration/Modern/menu/checkbox-invert.gif":[16,7,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",-16,0],"qx/decoration/Modern/menu/checkbox.gif":[16,7,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",-48,0],"qx/decoration/Modern/menu/radiobutton-invert.gif":[16,5,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",-32,0],"qx/decoration/Modern/menu/radiobutton.gif":[16,5,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",0,0],"qx/decoration/Modern/pane-lr-combined.png":[12,238,"png","qx"],"qx/decoration/Modern/pane-tb-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/pane/pane-b.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-30],"qx/decoration/Modern/pane/pane-bl.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-18],"qx/decoration/Modern/pane/pane-br.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-12],"qx/decoration/Modern/pane/pane-c.png":[40,238,"png","qx"],"qx/decoration/Modern/pane/pane-l.png":[6,238,"png","qx","qx/decoration/Modern/pane-lr-combined.png",0,0],"qx/decoration/Modern/pane/pane-r.png":[6,238,"png","qx","qx/decoration/Modern/pane-lr-combined.png",-6,0],"qx/decoration/Modern/pane/pane-t.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,0],"qx/decoration/Modern/pane/pane-tl.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-24],"qx/decoration/Modern/pane/pane-tr.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-6],"qx/decoration/Modern/pane/pane.png":[185,250,"png","qx"],"qx/decoration/Modern/scrollbar-combined.png":[54,12,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-horizontal.png":[76,15,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-pressed-horizontal.png":[19,10,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-pressed-vertical.png":[10,19,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-vertical.png":[15,76,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-button-bg-horizontal.png":[12,10,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-34,0],"qx/decoration/Modern/scrollbar/scrollbar-button-bg-vertical.png":[10,12,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-6,0],"qx/decoration/Modern/scrollbar/scrollbar-down.png":[6,4,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-28,0],"qx/decoration/Modern/scrollbar/scrollbar-left.png":[4,6,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-50,0],"qx/decoration/Modern/scrollbar/scrollbar-right.png":[4,6,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-46,0],"qx/decoration/Modern/scrollbar/scrollbar-up.png":[6,4,"png","qx","qx/decoration/Modern/scrollbar-combined.png",0,0],"qx/decoration/Modern/scrollbar/slider-knob-background.png":[12,10,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-16,0],"qx/decoration/Modern/selection.png":[110,20,"png","qx"],"qx/decoration/Modern/shadow-lr-combined.png":[30,382,"png","qx"],"qx/decoration/Modern/shadow-small-lr-combined.png":[10,136,"png","qx"],"qx/decoration/Modern/shadow-small-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/shadow-tb-combined.png":[15,90,"png","qx"],"qx/decoration/Modern/shadow/shadow-b.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-30],"qx/decoration/Modern/shadow/shadow-bl.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-15],"qx/decoration/Modern/shadow/shadow-br.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-45],"qx/decoration/Modern/shadow/shadow-c.png":[40,382,"png","qx"],"qx/decoration/Modern/shadow/shadow-l.png":[15,382,"png","qx","qx/decoration/Modern/shadow-lr-combined.png",0,0],"qx/decoration/Modern/shadow/shadow-r.png":[15,382,"png","qx","qx/decoration/Modern/shadow-lr-combined.png",-15,0],"qx/decoration/Modern/shadow/shadow-small-b.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-20],"qx/decoration/Modern/shadow/shadow-small-bl.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-15],"qx/decoration/Modern/shadow/shadow-small-br.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-10],"qx/decoration/Modern/shadow/shadow-small-c.png":[40,136,"png","qx"],"qx/decoration/Modern/shadow/shadow-small-l.png":[5,136,"png","qx","qx/decoration/Modern/shadow-small-lr-combined.png",0,0],"qx/decoration/Modern/shadow/shadow-small-r.png":[5,136,"png","qx","qx/decoration/Modern/shadow-small-lr-combined.png",-5,0],"qx/decoration/Modern/shadow/shadow-small-t.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-5],"qx/decoration/Modern/shadow/shadow-small-tl.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,0],"qx/decoration/Modern/shadow/shadow-small-tr.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-25],"qx/decoration/Modern/shadow/shadow-small.png":[114,146,"png","qx"],"qx/decoration/Modern/shadow/shadow-t.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-60],"qx/decoration/Modern/shadow/shadow-tl.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-75],"qx/decoration/Modern/shadow/shadow-tr.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,0],"qx/decoration/Modern/shadow/shadow.png":[381,412,"png","qx"],"qx/decoration/Modern/splitpane-knobs-combined.png":[8,9,"png","qx"],"qx/decoration/Modern/splitpane/knob-horizontal.png":[1,8,"png","qx","qx/decoration/Modern/splitpane-knobs-combined.png",0,-1],"qx/decoration/Modern/splitpane/knob-vertical.png":[8,1,"png","qx","qx/decoration/Modern/splitpane-knobs-combined.png",0,0],"qx/decoration/Modern/table-combined.png":[94,18,"png","qx"],"qx/decoration/Modern/table/ascending.png":[8,5,"png","qx","qx/decoration/Modern/table-combined.png",0,0],"qx/decoration/Modern/table/boolean-false.png":[14,14,"png","qx","qx/decoration/Modern/table-combined.png",-80,0],"qx/decoration/Modern/table/boolean-true.png":[14,14,"png","qx","qx/decoration/Modern/table-combined.png",-26,0],"qx/decoration/Modern/table/descending.png":[8,5,"png","qx","qx/decoration/Modern/table-combined.png",-18,0],"qx/decoration/Modern/table/header-cell.png":[40,18,"png","qx","qx/decoration/Modern/table-combined.png",-40,0],"qx/decoration/Modern/table/select-column-order.png":[10,9,"png","qx","qx/decoration/Modern/table-combined.png",-8,0],"qx/decoration/Modern/tabview-button-bottom-active-lr-combined.png":[10,14,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-inactive-lr-combined.png":[6,15,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-left-active-lr-combined.png":[10,37,"png","qx"],"qx/decoration/Modern/tabview-button-left-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-left-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-left-inactive-lr-combined.png":[6,39,"png","qx"],"qx/decoration/Modern/tabview-button-left-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-right-active-lr-combined.png":[10,37,"png","qx"],"qx/decoration/Modern/tabview-button-right-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-right-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-right-inactive-lr-combined.png":[6,39,"png","qx"],"qx/decoration/Modern/tabview-button-right-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-top-active-lr-combined.png":[10,12,"png","qx"],"qx/decoration/Modern/tabview-button-top-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-top-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-top-inactive-lr-combined.png":[6,15,"png","qx"],"qx/decoration/Modern/tabview-button-top-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-pane-lr-combined.png":[60,2,"png","qx"],"qx/decoration/Modern/tabview-pane-tb-combined.png":[30,180,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-bottom-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-bottom-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-bottom-active-c.png":[40,14,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-active-l.png":[5,14,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-active-r.png":[5,14,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-bottom-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-bottom-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-bottom-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-active.png":[49,24,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-c.png":[40,15,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-l.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-r.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-bottom-inactive.png":[45,21,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-left-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-left-active-c.png":[40,37,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-active-l.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-left-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-active-r.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-left-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-left-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-left-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-left-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-left-active.png":[22,47,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-left-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-left-inactive-c.png":[40,39,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-inactive-l.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-r.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-left-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-left-inactive.png":[20,45,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-right-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-right-active-c.png":[40,37,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-active-l.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-right-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-active-r.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-right-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-right-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-right-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-right-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-right-active.png":[22,47,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-right-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-right-inactive-c.png":[40,39,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-inactive-l.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-r.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-right-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-right-inactive.png":[20,45,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-top-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-top-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-top-active-c.png":[40,14,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-active-l.png":[5,12,"png","qx","qx/decoration/Modern/tabview-button-top-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-active-r.png":[5,12,"png","qx","qx/decoration/Modern/tabview-button-top-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-top-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-top-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-top-active.png":[48,22,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-top-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-top-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-c.png":[40,15,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-inactive-l.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-r.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-top-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-top-inactive.png":[45,21,"png","qx"],"qx/decoration/Modern/tabview/tabview-pane-b.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-60],"qx/decoration/Modern/tabview/tabview-pane-bl.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tabview-pane-br.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-120],"qx/decoration/Modern/tabview/tabview-pane-c.png":[40,120,"png","qx"],"qx/decoration/Modern/tabview/tabview-pane-l.png":[30,2,"png","qx","qx/decoration/Modern/tabview-pane-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tabview-pane-r.png":[30,2,"png","qx","qx/decoration/Modern/tabview-pane-lr-combined.png",-30,0],"qx/decoration/Modern/tabview/tabview-pane-t.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-150],"qx/decoration/Modern/tabview/tabview-pane-tl.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-30],"qx/decoration/Modern/tabview/tabview-pane-tr.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-90],"qx/decoration/Modern/tabview/tabview-pane.png":[185,250,"png","qx"],"qx/decoration/Modern/toolbar-combined.png":[80,130,"png","qx"],"qx/decoration/Modern/toolbar/toolbar-gradient-blue.png":[40,130,"png","qx","qx/decoration/Modern/toolbar-combined.png",-40,0],"qx/decoration/Modern/toolbar/toolbar-gradient.png":[40,130,"png","qx","qx/decoration/Modern/toolbar-combined.png",0,0],"qx/decoration/Modern/toolbar/toolbar-handle-knob.gif":[1,8,"gif","qx"],"qx/decoration/Modern/toolbar/toolbar-part.gif":[7,1,"gif","qx"],"qx/decoration/Modern/tooltip-error-lr-combined.png":[12,18,"png","qx"],"qx/decoration/Modern/tooltip-error-tb-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/tree-combined.png":[32,8,"png","qx"],"qx/decoration/Modern/tree/closed-selected.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",-24,0],"qx/decoration/Modern/tree/closed.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",-16,0],"qx/decoration/Modern/tree/open-selected.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",-8,0],"qx/decoration/Modern/tree/open.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",0,0],"qx/decoration/Modern/window-captionbar-buttons-combined.png":[108,9,"png","qx"],"qx/decoration/Modern/window-captionbar-lr-active-combined.png":[12,9,"png","qx"],"qx/decoration/Modern/window-captionbar-lr-inactive-combined.png":[12,9,"png","qx"],"qx/decoration/Modern/window-captionbar-tb-active-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/window-captionbar-tb-inactive-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/window-statusbar-lr-combined.png":[8,7,"png","qx"],"qx/decoration/Modern/window-statusbar-tb-combined.png":[4,24,"png","qx"],"qx/decoration/Modern/window/captionbar-active-b.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-18],"qx/decoration/Modern/window/captionbar-active-bl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-24],"qx/decoration/Modern/window/captionbar-active-br.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-12],"qx/decoration/Modern/window/captionbar-active-c.png":[40,9,"png","qx"],"qx/decoration/Modern/window/captionbar-active-l.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-active-combined.png",-6,0],"qx/decoration/Modern/window/captionbar-active-r.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-active-combined.png",0,0],"qx/decoration/Modern/window/captionbar-active-t.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-6],"qx/decoration/Modern/window/captionbar-active-tl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,0],"qx/decoration/Modern/window/captionbar-active-tr.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-30],"qx/decoration/Modern/window/captionbar-active.png":[69,21,"png","qx"],"qx/decoration/Modern/window/captionbar-inactive-b.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-24],"qx/decoration/Modern/window/captionbar-inactive-bl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-6],"qx/decoration/Modern/window/captionbar-inactive-br.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-30],"qx/decoration/Modern/window/captionbar-inactive-c.png":[40,9,"png","qx"],"qx/decoration/Modern/window/captionbar-inactive-l.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-inactive-combined.png",0,0],"qx/decoration/Modern/window/captionbar-inactive-r.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-inactive-combined.png",-6,0],"qx/decoration/Modern/window/captionbar-inactive-t.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,0],"qx/decoration/Modern/window/captionbar-inactive-tl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-12],"qx/decoration/Modern/window/captionbar-inactive-tr.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-18],"qx/decoration/Modern/window/captionbar-inactive.png":[69,21,"png","qx"],"qx/decoration/Modern/window/close-active-hovered.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-27,0],"qx/decoration/Modern/window/close-active.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-9,0],"qx/decoration/Modern/window/close-inactive.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-90,0],"qx/decoration/Modern/window/maximize-active-hovered.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-18,0],"qx/decoration/Modern/window/maximize-active.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-81,0],"qx/decoration/Modern/window/maximize-inactive.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-54,0],"qx/decoration/Modern/window/minimize-active-hovered.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-63,0],"qx/decoration/Modern/window/minimize-active.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-72,0],"qx/decoration/Modern/window/minimize-inactive.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-36,0],"qx/decoration/Modern/window/restore-active-hovered.png":[9,8,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",0,0],"qx/decoration/Modern/window/restore-active.png":[9,8,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-99,0],"qx/decoration/Modern/window/restore-inactive.png":[9,8,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-45,0],"qx/decoration/Modern/window/statusbar-b.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-16],"qx/decoration/Modern/window/statusbar-bl.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-20],"qx/decoration/Modern/window/statusbar-br.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-4],"qx/decoration/Modern/window/statusbar-c.png":[40,7,"png","qx"],"qx/decoration/Modern/window/statusbar-l.png":[4,7,"png","qx","qx/decoration/Modern/window-statusbar-lr-combined.png",-4,0],"qx/decoration/Modern/window/statusbar-r.png":[4,7,"png","qx","qx/decoration/Modern/window-statusbar-lr-combined.png",0,0],"qx/decoration/Modern/window/statusbar-t.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,0],"qx/decoration/Modern/window/statusbar-tl.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-8],"qx/decoration/Modern/window/statusbar-tr.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-12],"qx/decoration/Modern/window/statusbar.png":[369,15,"png","qx"],"qx/icon/Tango/16/actions/dialog-cancel.png":[16,16,"png","qx"],"qx/icon/Tango/16/actions/dialog-ok.png":[16,16,"png","qx"],"qx/icon/Tango/16/actions/view-refresh.png":[16,16,"png","qx"],"qx/icon/Tango/16/actions/window-close.png":[16,16,"png","qx"],"qx/icon/Tango/16/apps/office-calendar.png":[16,16,"png","qx"],"qx/icon/Tango/16/apps/utilities-color-chooser.png":[16,16,"png","qx"],"qx/icon/Tango/16/mimetypes/office-document.png":[16,16,"png","qx"],"qx/icon/Tango/16/places/folder-open.png":[16,16,"png","qx"],"qx/icon/Tango/16/places/folder.png":[16,16,"png","qx"],"qx/icon/Tango/22/mimetypes/office-document.png":[22,22,"png","qx"],"qx/icon/Tango/22/places/folder-open.png":[22,22,"png","qx"],"qx/icon/Tango/22/places/folder.png":[22,22,"png","qx"],"qx/icon/Tango/32/mimetypes/office-document.png":[32,32,"png","qx"],"qx/icon/Tango/32/places/folder-open.png":[32,32,"png","qx"],"qx/icon/Tango/32/places/folder.png":[32,32,"png","qx"],"qx/static/blank.gif":[1,1,"gif","qx"],"scoville_admin/config_header.png":[640,100,"png","scoville_admin"],"scoville_admin/loading.gif":[16,16,"gif","scoville_admin"],"scoville_admin/module.png":[16,16,"png","scoville_admin"],"scoville_admin/permission.png":[16,16,"png","scoville_admin"],"scoville_admin/role.png":[16,16,"png","scoville_admin"],"scoville_admin/server.png":[16,16,"png","scoville_admin"],"scoville_admin/server_invalid.png":[16,16,"png","scoville_admin"],"scoville_admin/server_locked.png":[16,16,"png","scoville_admin"],"scoville_admin/site.png":[16,16,"png","scoville_admin"],"scoville_admin/test.png":[32,32,"png","scoville_admin"],"scoville_admin/user.png":[16,16,"png","scoville_admin"],"scoville_admin/web.png":[16,16,"png","scoville_admin"]},"translations":{}};
(function(){var m="toString",k=".",j="default",h="Object",g='"',f="Array",e="()",d="String",c="Function",b=".prototype",L="function",K="Boolean",J="Error",I="constructor",H="warn",G="hasOwnProperty",F="string",E="toLocaleString",D="RegExp",C='\", "',t="info",u="BROKEN_IE",r="isPrototypeOf",s="Date",p="",q="qx.Bootstrap",n="]",o="Class",v="error",w="[Class ",y="valueOf",x="Number",A="count",z="debug",B="ES5";
if(!window.qx){window.qx={};
}qx.Bootstrap={genericToString:function(){return w+this.classname+n;
},createNamespace:function(name,M){var O=name.split(k);
var parent=window;
var N=O[0];

for(var i=0,P=O.length-1;i<P;i++,N=O[i]){if(!parent[N]){parent=parent[N]={};
}else{parent=parent[N];
}}parent[N]=M;
return N;
},setDisplayName:function(Q,R,name){Q.displayName=R+k+name+e;
},setDisplayNames:function(S,T){for(var name in S){var U=S[name];

if(U instanceof Function){U.displayName=T+k+name+e;
}}},define:function(name,V){if(!V){var V={statics:{}};
}var bb;
var Y=null;
qx.Bootstrap.setDisplayNames(V.statics,name);

if(V.members||V.extend){qx.Bootstrap.setDisplayNames(V.members,name+b);
bb=V.construct||new Function;

if(V.extend){this.extendClass(bb,bb,V.extend,name,ba);
}var W=V.statics||{};
for(var i=0,bc=qx.Bootstrap.getKeys(W),l=bc.length;i<l;i++){var bd=bc[i];
bb[bd]=W[bd];
}Y=bb.prototype;
var X=V.members||{};
for(var i=0,bc=qx.Bootstrap.getKeys(X),l=bc.length;i<l;i++){var bd=bc[i];
Y[bd]=X[bd];
}}else{bb=V.statics||{};
}var ba=this.createNamespace(name,bb);
bb.name=bb.classname=name;
bb.basename=ba;
bb.$$type=o;
if(!bb.hasOwnProperty(m)){bb.toString=this.genericToString;
}if(V.defer){V.defer(bb,Y);
}qx.Bootstrap.$$registry[name]=V.statics;
return bb;
}};
qx.Bootstrap.define(q,{statics:{LOADSTART:qx.$$start||new Date(),DEBUG:(function(){var be=true;

if(qx.$$environment&&qx.$$environment["qx.debug"]===false){be=false;
}return be;
})(),getEnvironmentSetting:function(bf){if(qx.$$environment){return qx.$$environment[bf];
}},setEnvironmentSetting:function(bg,bh){if(!qx.$$environment){qx.$$environment={};
}
if(qx.$$environment[bg]===undefined){qx.$$environment[bg]=bh;
}},createNamespace:qx.Bootstrap.createNamespace,define:qx.Bootstrap.define,setDisplayName:qx.Bootstrap.setDisplayName,setDisplayNames:qx.Bootstrap.setDisplayNames,genericToString:qx.Bootstrap.genericToString,extendClass:function(bi,bj,bk,name,bl){var bo=bk.prototype;
var bn=new Function;
bn.prototype=bo;
var bm=new bn;
bi.prototype=bm;
bm.name=bm.classname=name;
bm.basename=bl;
bj.base=bi.superclass=bk;
bj.self=bi.constructor=bm.constructor=bi;
},getByName:function(name){return qx.Bootstrap.$$registry[name];
},$$registry:{},objectGetLength:({"count":function(bp){return bp.__count__;
},"default":function(bq){var length=0;

for(var br in bq){length++;
}return length;
}})[(({}).__count__==0)?A:j],objectMergeWith:function(bs,bt,bu){if(bu===undefined){bu=true;
}
for(var bv in bt){if(bu||bs[bv]===undefined){bs[bv]=bt[bv];
}}return bs;
},__a:[r,G,E,m,y,I],getKeys:({"ES5":Object.keys,"BROKEN_IE":function(bw){var bx=[];
var bz=Object.prototype.hasOwnProperty;

for(var bA in bw){if(bz.call(bw,bA)){bx.push(bA);
}}var by=qx.Bootstrap.__a;

for(var i=0,a=by,l=a.length;i<l;i++){if(bz.call(bw,a[i])){bx.push(a[i]);
}}return bx;
},"default":function(bB){var bC=[];
var bD=Object.prototype.hasOwnProperty;

for(var bE in bB){if(bD.call(bB,bE)){bC.push(bE);
}}return bC;
}})[typeof (Object.keys)==L?B:(function(){for(var bF in {toString:1}){return bF;
}})()!==m?u:j],getKeysAsString:function(bG){var bH=qx.Bootstrap.getKeys(bG);

if(bH.length==0){return p;
}return g+bH.join(C)+g;
},__b:{"[object String]":d,"[object Array]":f,"[object Object]":h,"[object RegExp]":D,"[object Number]":x,"[object Boolean]":K,"[object Date]":s,"[object Function]":c,"[object Error]":J},bind:function(bI,self,bJ){var bK=Array.prototype.slice.call(arguments,2,arguments.length);
return function(){var bL=Array.prototype.slice.call(arguments,0,arguments.length);
return bI.apply(self,bK.concat(bL));
};
},firstUp:function(bM){return bM.charAt(0).toUpperCase()+bM.substr(1);
},firstLow:function(bN){return bN.charAt(0).toLowerCase()+bN.substr(1);
},getClass:function(bO){var bP=Object.prototype.toString.call(bO);
return (qx.Bootstrap.__b[bP]||bP.slice(8,-1));
},isString:function(bQ){return (bQ!==null&&(typeof bQ===F||qx.Bootstrap.getClass(bQ)==d||bQ instanceof String||(!!bQ&&!!bQ.$$isString)));
},isArray:function(bR){return (bR!==null&&(bR instanceof Array||(bR&&qx.data&&qx.data.IListData&&qx.Bootstrap.hasInterface(bR.constructor,qx.data.IListData))||qx.Bootstrap.getClass(bR)==f||(!!bR&&!!bR.$$isArray)));
},isObject:function(bS){return (bS!==undefined&&bS!==null&&qx.Bootstrap.getClass(bS)==h);
},isFunction:function(bT){return qx.Bootstrap.getClass(bT)==c;
},classIsDefined:function(name){return qx.Bootstrap.getByName(name)!==undefined;
},getPropertyDefinition:function(bU,name){while(bU){if(bU.$$properties&&bU.$$properties[name]){return bU.$$properties[name];
}bU=bU.superclass;
}return null;
},hasProperty:function(bV,name){return !!qx.Bootstrap.getPropertyDefinition(bV,name);
},getEventType:function(bW,name){var bW=bW.constructor;

while(bW.superclass){if(bW.$$events&&bW.$$events[name]!==undefined){return bW.$$events[name];
}bW=bW.superclass;
}return null;
},supportsEvent:function(bX,name){return !!qx.Bootstrap.getEventType(bX,name);
},getByInterface:function(bY,ca){var cb,i,l;

while(bY){if(bY.$$implements){cb=bY.$$flatImplements;

for(i=0,l=cb.length;i<l;i++){if(cb[i]===ca){return bY;
}}}bY=bY.superclass;
}return null;
},hasInterface:function(cc,cd){return !!qx.Bootstrap.getByInterface(cc,cd);
},getMixins:function(ce){var cf=[];

while(ce){if(ce.$$includes){cf.push.apply(cf,ce.$$flatIncludes);
}ce=ce.superclass;
}return cf;
},$$logs:[],debug:function(cg,ch){qx.Bootstrap.$$logs.push([z,arguments]);
},info:function(ci,cj){qx.Bootstrap.$$logs.push([t,arguments]);
},warn:function(ck,cl){qx.Bootstrap.$$logs.push([H,arguments]);
},error:function(cm,cn){qx.Bootstrap.$$logs.push([v,arguments]);
},trace:function(co){}}});
})();
(function(){var r=".",q="function",p="",o="gecko",n="[object Opera]",m="mshtml",l="8.0",k="AppleWebKit/",j="9.0",i="[^\\.0-9]",c="Gecko",h="webkit",f="4.0",b="1.9.0.0",a="opera",e="Version/",d="5.0",g="qx.bom.client.Engine";
qx.Bootstrap.define(g,{statics:{getVersion:function(){var v=window.navigator.userAgent;
var t=p;

if(qx.bom.client.Engine.__c()){if(/Opera[\s\/]([0-9]+)\.([0-9])([0-9]*)/.test(v)){if(v.indexOf(e)!=-1){var u=v.match(/Version\/(\d+)\.(\d+)/);
t=u[1]+r+u[2].charAt(0)+r+u[2].substring(1,u[2].length);
}else{t=RegExp.$1+r+RegExp.$2;

if(RegExp.$3!=p){t+=r+RegExp.$3;
}}}}else if(qx.bom.client.Engine.__d()){if(/AppleWebKit\/([^ ]+)/.test(v)){t=RegExp.$1;
var w=RegExp(i).exec(t);

if(w){t=t.slice(0,w.index);
}}}else if(qx.bom.client.Engine.__e()){if(/rv\:([^\);]+)(\)|;)/.test(v)){t=RegExp.$1;
}}else if(qx.bom.client.Engine.__f()){if(/MSIE\s+([^\);]+)(\)|;)/.test(v)){t=RegExp.$1;
if(t<8&&/Trident\/([^\);]+)(\)|;)/.test(v)){if(RegExp.$1==f){t=l;
}else if(RegExp.$1==d){t=j;
}}}}else{var s=window.qxFail;

if(s&&typeof s===q){t=s().FULLVERSION;
}else{t=b;
qx.Bootstrap.warn("Unsupported client: "+v+"! Assumed gecko version 1.9.0.0 (Firefox 3.0).");
}}return t;
},getName:function(){var name;

if(qx.bom.client.Engine.__c()){name=a;
}else if(qx.bom.client.Engine.__d()){name=h;
}else if(qx.bom.client.Engine.__e()){name=o;
}else if(qx.bom.client.Engine.__f()){name=m;
}else{var x=window.qxFail;

if(x&&typeof x===q){name=x().NAME;
}else{name=o;
qx.Bootstrap.warn("Unsupported client: "+window.navigator.userAgent+"! Assumed gecko version 1.9.0.0 (Firefox 3.0).");
}}return name;
},__c:function(){return window.opera&&Object.prototype.toString.call(window.opera)==n;
},__d:function(){return window.navigator.userAgent.indexOf(k)!=-1;
},__e:function(){return window.controllers&&window.navigator.product===c;
},__f:function(){return window.navigator.cpuClass&&/MSIE\s+([^\);]+)(\)|;)/.test(window.navigator.userAgent);
}}});
})();
(function(){var k="xhr",j="Microsoft.XMLHTTP",i="",h="file:",g="https:",f="webkit",e="gecko",d="activex",c="opera",b=".",a="qx.bom.client.Transport";
qx.Bootstrap.define(a,{statics:{getMaxConcurrentRequestCount:function(){var l;
var o=qx.bom.client.Engine.getVersion().split(b);
var m=0;
var p=0;
var n=0;
if(o[0]){m=o[0];
}if(o[1]){p=o[1];
}if(o[2]){n=o[2];
}if(window.maxConnectionsPerServer){l=window.maxConnectionsPerServer;
}else if(qx.bom.client.Engine.getName()==c){l=8;
}else if(qx.bom.client.Engine.getName()==f){l=4;
}else if(qx.bom.client.Engine.getName()==e&&((m>1)||((m==1)&&(p>9))||((m==1)&&(p==9)&&(n>=1)))){l=6;
}else{l=2;
}return l;
},getSsl:function(){return window.location.protocol===g;
},getXmlHttpRequest:function(){var q=window.ActiveXObject?(function(){if(window.location.protocol!==h){try{new window.XMLHttpRequest();
return k;
}catch(r){}}
try{new window.ActiveXObject(j);
return d;
}catch(s){}})():(function(){try{new window.XMLHttpRequest();
return k;
}catch(t){}})();
return q||i;
}}});
})();
(function(){var j="",i="10.1",h="10.3",g="10.7",f="10.5",e="95",d="10.2",c="98",b="2000",a="10.6",bb="10.0",ba="10.4",Y="rim_tabletos",X="Darwin",W="2003",V=")",U="iPhone",T="android",S="unix",R="ce",q="7",r="SymbianOS",o="|",p="MacPPC",m="iPod",n="\.",k="Win64",l="linux",u="me",v="Macintosh",D="Android",B="Windows",J="ios",F="vista",N="blackberry",L="(",x="win",Q="Linux",P="BSD",O="iPad",w="X11",z="xp",A="symbian",C="qx.bom.client.OperatingSystem",E="g",G="Win32",K="osx",M="webOS",s="RIM Tablet OS",t="BlackBerry",y="nt4",I="MacIntel",H="webos";
qx.Bootstrap.define(C,{statics:{getName:function(){if(!navigator){return j;
}var bc=navigator.platform||j;
var bd=navigator.userAgent||j;

if(bc.indexOf(B)!=-1||bc.indexOf(G)!=-1||bc.indexOf(k)!=-1){return x;
}else if(bc.indexOf(v)!=-1||bc.indexOf(p)!=-1||bc.indexOf(I)!=-1){return K;
}else if(bd.indexOf(s)!=-1){return Y;
}else if(bd.indexOf(M)!=-1){return H;
}else if(bc.indexOf(m)!=-1||bc.indexOf(U)!=-1||bc.indexOf(O)!=-1){return J;
}else if(bc.indexOf(Q)!=-1){return l;
}else if(bc.indexOf(w)!=-1||bc.indexOf(P)!=-1||bc.indexOf(X)!=-1){return S;
}else if(bc.indexOf(D)!=-1){return T;
}else if(bc.indexOf(r)!=-1){return A;
}else if(bc.indexOf(t)!=-1){return N;
}return j;
},__g:{"Windows NT 6.1":q,"Windows NT 6.0":F,"Windows NT 5.2":W,"Windows NT 5.1":z,"Windows NT 5.0":b,"Windows 2000":b,"Windows NT 4.0":y,"Win 9x 4.90":u,"Windows CE":R,"Windows 98":c,"Win98":c,"Windows 95":e,"Win95":e,"Mac OS X 10_7":g,"Mac OS X 10.7":g,"Mac OS X 10_6":a,"Mac OS X 10.6":a,"Mac OS X 10_5":f,"Mac OS X 10.5":f,"Mac OS X 10_4":ba,"Mac OS X 10.4":ba,"Mac OS X 10_3":h,"Mac OS X 10.3":h,"Mac OS X 10_2":d,"Mac OS X 10.2":d,"Mac OS X 10_1":i,"Mac OS X 10.1":i,"Mac OS X 10_0":bb,"Mac OS X 10.0":bb},getVersion:function(){var bg=[];

for(var bf in qx.bom.client.OperatingSystem.__g){bg.push(bf);
}var bh=new RegExp(L+bg.join(o).replace(/\./g,n)+V,E);
var be=bh.exec(navigator.userAgent);

if(be&&be[1]){return qx.bom.client.OperatingSystem.__g[be[1]];
}return j;
}}});
})();
(function(){var k="background",j="div",h="color",g="linear-gradient(0deg, white 0%, red 100%)",f="placeholder",e="content",d="OTextOverflow",c="MozBorderRadius",b="qx.bom.client.Css",a='m11',C="input",B="-ms-linear-gradient(0deg, white 0%, red 100%)",A="-moz-linear-gradient(0deg, white 0%, red 100%)",z="gradient",y="-webkit-linear-gradient(left, white, black)",x="MozBoxShadow",w="rgba(1, 2, 3, 0.5)",v="rgba",u="-o-linear-gradient(0deg, white 0%, red 100%)",t="borderRadius",r='WebKitCSSMatrix',s="WebkitBorderRadius",p="-webkit-gradient(linear,0% 0%,100% 100%,from(white), to(red))",q="mshtml",n="WebkitBoxShadow",o="textOverflow",l="boxShadow",m="border";
qx.Bootstrap.define(b,{statics:{getBoxModel:function(){var content=qx.bom.client.Engine.getName()!==q||!qx.bom.client.Browser.getQuirksMode();
return content?e:m;
},getTextOverflow:function(){return o in document.documentElement.style||d in document.documentElement.style;
},getPlaceholder:function(){var i=document.createElement(C);
return f in i;
},getBorderRadius:function(){return t in document.documentElement.style||c in document.documentElement.style||s in document.documentElement.style;
},getBoxShadow:function(){return l in document.documentElement.style||x in document.documentElement.style||n in document.documentElement.style;
},getTranslate3d:function(){return r in window&&a in new WebKitCSSMatrix();
},getGradients:function(){var D;

try{D=document.createElement(j);
}catch(F){D=document.createElement();
}var E=[p,y,A,u,B,g];

for(var i=0;i<E.length;i++){try{D.style[k]=E[i];

if(D.style[k].indexOf(z)!=-1){return true;
}}catch(G){}}return false;
},getRgba:function(){var H;

try{H=document.createElement(j);
}catch(I){H=document.createElement();
}try{H.style[h]=w;

if(H.style[h].indexOf(v)!=-1){return true;
}}catch(J){}return false;
}}});
})();
(function(){var j="mshtml",i="msie",h=")(/| )([0-9]+\.[0-9])",g="",f="(",e="ce",d="CSS1Compat",c="android",b="operamini",a="mobile chrome",z="iemobile",y="prism|Fennec|Camino|Kmeleon|Galeon|Netscape|SeaMonkey|Namoroka|Firefox",x="opera mobi",w="Mobile Safari",v="operamobile",u="ie",t="mobile safari",s="IEMobile|Maxthon|MSIE",r="qx.bom.client.Browser",q="opera mini",o="opera",p="Opera Mini|Opera Mobi|Opera",m="AdobeAIR|Titanium|Fluid|Chrome|Android|Epiphany|Konqueror|iCab|OmniWeb|Maxthon|Pre|Mobile Safari|Safari",n="webkit",k="5.0",l="Mobile/";
qx.Bootstrap.define(r,{statics:{getName:function(){var D=navigator.userAgent;
var C=new RegExp(f+qx.bom.client.Browser.__h+h);
var B=D.match(C);

if(!B){return g;
}var name=B[1].toLowerCase();
var A=qx.bom.client.Engine.getName();

if(A===n){if(name===c){name=a;
}else if(D.indexOf(w)!==-1||D.indexOf(l)!==-1){name=t;
}}else if(A===j){if(name===i){name=u;
if(qx.bom.client.OperatingSystem.getVersion()===e){name=z;
}}}else if(A===o){if(name===x){name=v;
}else if(name===q){name=b;
}}return name;
},getVersion:function(){var H=navigator.userAgent;
var G=new RegExp(f+qx.bom.client.Browser.__h+h);
var F=H.match(G);

if(!F){return g;
}var name=F[1].toLowerCase();
var E=F[3];
if(H.match(/Version(\/| )([0-9]+\.[0-9])/)){E=RegExp.$2;
}
if(qx.bom.client.Engine.getName()==j){E=qx.bom.client.Engine.getVersion();

if(name===i&&qx.bom.client.OperatingSystem.getVersion()==e){E=k;
}}return E;
},getDocumentMode:function(){if(document.documentMode){return document.documentMode;
}return 0;
},getQuirksMode:function(){if(qx.bom.client.Engine.getName()==j&&parseFloat(qx.bom.client.Engine.getVersion())>=8){return qx.bom.client.Engine.DOCUMENT_MODE===5;
}else{return document.compatMode!==d;
}},__h:{"webkit":m,"gecko":y,"mshtml":s,"opera":p}[qx.bom.client.Engine.getName()]}});
})();
(function(){var d="-",c="",b="qx.bom.client.Locale",a="android";
qx.Bootstrap.define(b,{statics:{getLocale:function(){var e=qx.bom.client.Locale.__i();
var f=e.indexOf(d);

if(f!=-1){e=e.substr(0,f);
}return e;
},getVariant:function(){var g=qx.bom.client.Locale.__i();
var i=c;
var h=g.indexOf(d);

if(h!=-1){i=g.substr(h+1);
}return i;
},__i:function(){var j=(navigator.userLanguage||navigator.language||c);
if(qx.bom.client.OperatingSystem.getName()==a){var k=/(\w{2})-(\w{2})/i.exec(navigator.userAgent);

if(k){j=k[0];
}}return j.toLowerCase();
}}});
})();
(function(){var l="",k="audio",j="video",i='video/ogg; codecs="theora, vorbis"',h="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul",g="http://www.w3.org/TR/SVG11/feature#BasicStructure",f='audio',d='video/mp4; codecs="avc1.42E01E, mp4a.40.2"',c="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==",b="audio/mpeg",z="org.w3c.dom.svg",y="DOMTokenList",x="1.1",w="audio/x-wav",u="audio/ogg",t="audio/x-aiff",s="qx.bom.client.Html",r='video',q="mshtml",p="label",n='video/webm; codecs="vp8, vorbis"',o="1.0",m="audio/basic";
qx.Bootstrap.define(s,{statics:{getWebWorker:function(){return window.Worker!=null;
},getFileReader:function(){return window.FileReader!=null;
},getGeoLocation:function(){return navigator.geolocation!=null;
},getAudio:function(){return !!document.createElement(f).canPlayType;
},getAudioOgg:function(){if(!qx.bom.client.Html.getAudio()){return l;
}var a=document.createElement(k);
return a.canPlayType(u);
},getAudioMp3:function(){if(!qx.bom.client.Html.getAudio()){return l;
}var a=document.createElement(k);
return a.canPlayType(b);
},getAudioWav:function(){if(!qx.bom.client.Html.getAudio()){return l;
}var a=document.createElement(k);
return a.canPlayType(w);
},getAudioAu:function(){if(!qx.bom.client.Html.getAudio()){return l;
}var a=document.createElement(k);
return a.canPlayType(m);
},getAudioAif:function(){if(!qx.bom.client.Html.getAudio()){return l;
}var a=document.createElement(k);
return a.canPlayType(t);
},getVideo:function(){return !!document.createElement(r).canPlayType;
},getVideoOgg:function(){if(!qx.bom.client.Html.getVideo()){return l;
}var v=document.createElement(j);
return v.canPlayType(i);
},getVideoH264:function(){if(!qx.bom.client.Html.getVideo()){return l;
}var v=document.createElement(j);
return v.canPlayType(d);
},getVideoWebm:function(){if(!qx.bom.client.Html.getVideo()){return l;
}var v=document.createElement(j);
return v.canPlayType(n);
},getLocalStorage:function(){try{return window.localStorage!=null;
}catch(A){return false;
}},getSessionStorage:function(){try{return window.sessionStorage!=null;
}catch(B){return false;
}},getClassList:function(){return !!(document.documentElement.classList&&qx.Bootstrap.getClass(document.documentElement.classList)===y);
},getXPath:function(){return !!document.evaluate;
},getXul:function(){try{document.createElementNS(h,p);
return true;
}catch(e){return false;
}},getSvg:function(){return document.implementation&&document.implementation.hasFeature&&(document.implementation.hasFeature(z,o)||document.implementation.hasFeature(g,x));
},getVml:function(){return qx.bom.client.Engine.getName()==q;
},getCanvas:function(){return !!window.CanvasRenderingContext2D;
},getDataUrl:function(C){var D=new Image();
D.onload=D.onerror=function(){window.setTimeout(function(){C.call(null,(D.width==1&&D.height==1));
},0);
};
D.src=c;
},getDataset:function(){return !!document.documentElement.dataset;
}}});
})();
(function(){var e="qx.bom.client.Event",d="ontouchstart",c="mshtml",b="opera",a="pointerEvents";
qx.Bootstrap.define(e,{statics:{getTouch:function(){return (d in window);
},getPointer:function(){if(a in document.documentElement.style){var f=qx.bom.client.Engine.getName();
return f!=b&&f!=c;
}return false;
}}});
})();
(function(){var a="qx.bom.client.EcmaScript";
qx.Bootstrap.define(a,{statics:{getObjectCount:function(){return (({}).__count__==0);
}}});
})();
(function(){var k="os.name",j="os.version",h="css.borderradius",g="default",f="browser.quirksmode",e="browser.name",d="qx.allowUrlSettings",c="event.pointer",b="io.ssl",a="locale.variant",W="css.textoverflow",V="html.xul",U="css.boxshadow",T="event.touch",S="io.maxrequests",R="css.gradients",Q="browser.documentmode",P="ecmascript.objectcount",O="locale",N="engine.version",r="engine.name",s="css.rgba",p="css.boxmodel",q="css.placeholder",n="|",o="browser.version",l="qx.core.Environment",m="qx.debug.databinding",t="qx.optimization.basecalls",u="qx.debug.dispose",B="qx.optimization.variables",z="true",F="qx.optimization.privates",D="qx.aspects",J="qx.debug",H="qx.dynamicmousewheel",w=":",M="qxenv",L="qx.optimization.strings",K="qx.optimization.comments",v="qx.optimization.variants",x="qx.mobile.emulatetouch",y="qx.dynlocale",A="false",C="&",E="qx.mobile.nativescroll",G="qx.allowUrlVariants",I="qx.propertyDebugLevel";
qx.Bootstrap.define(l,{statics:{_checks:{},_asyncChecks:{},__j:{},get:function(X){if(this.__j[X]!=undefined){return this.__j[X];
}var Y=this._checks[X];

if(Y){var ba=Y();
this.__j[X]=ba;
return ba;
}if(qx.Bootstrap.DEBUG){qx.Bootstrap.warn(X+" is not a valid key. Please see the API-doc of "+"qx.core.Environment for a list of predefined keys.");
qx.Bootstrap.trace(this);
}},getAsync:function(bb,bc,self){var be=this;

if(this.__j[bb]!=undefined){window.setTimeout(function(){bc.call(self,be.__j[bb]);
},0);
return;
}var bd=this._asyncChecks[bb];

if(bd){bd(function(bf){be.__j[bb]=bf;
bc.call(self,bf);
});
return;
}if(qx.Bootstrap.DEBUG){qx.Bootstrap.warn(bb+" is not a valid key. Please see the API-doc of "+"qx.core.Environment for a list of predefined keys.");
qx.Bootstrap.trace(this);
}},select:function(bg,bh){return this.__k(this.get(bg),bh);
},selectAsync:function(bi,bj,self){this.getAsync(bi,function(bk){var bl=this.__k(bi,bj);
bl.call(self,bk);
},this);
},__k:function(bm,bn){var bp=bn[bm];

if(bn.hasOwnProperty(bm)){return bp;
}for(var bo in bn){if(bo.indexOf(n)!=-1){var bq=bo.split(n);

for(var i=0;i<bq.length;i++){if(bq[i]==bm){return bn[bo];
}}}}
if(bn[g]!==undefined){return bn[g];
}
if(qx.Bootstrap.DEBUG){throw new Error('No match for variant "'+bm+'" ('+(typeof bm)+' type)'+' in variants ['+qx.Bootstrap.getKeysAsString(bn)+'] found, and no default ("default") given');
}},invalidateCacheKey:function(br){delete this.__j[br];
},add:function(bs,bt){if(this._checks[bs]==undefined){if(bt instanceof Function){this._checks[bs]=bt;
}else{this._checks[bs]=this.__n(bt);
}}},addAsync:function(bu,bv){if(this._checks[bu]==undefined){this._asyncChecks[bu]=bv;
}},_initDefaultQxValues:function(){this.add(d,function(){return false;
});
this.add(G,function(){return false;
});
this.add(I,function(){return 0;
});
this.add(J,function(){return true;
});
this.add(D,function(){return false;
});
this.add(y,function(){return true;
});
this.add(x,function(){return false;
});
this.add(E,function(){return false;
});
this.add(H,function(){return true;
});
this.add(m,function(){return false;
});
this.add(u,function(){return false;
});
this.add(t,function(){return false;
});
this.add(K,function(){return false;
});
this.add(F,function(){return false;
});
this.add(L,function(){return false;
});
this.add(B,function(){return false;
});
this.add(v,function(){return false;
});
},__l:function(){if(qx&&qx.$$environment){for(var bx in qx.$$environment){var bw=qx.$$environment[bx];
this._checks[bx]=this.__n(bw);
}}},__m:function(){if(window.document&&window.document.location){var by=window.document.location.search.slice(1).split(C);

for(var i=0;i<by.length;i++){var bA=by[i].split(w);

if(bA.length!=3||bA[0]!=M){continue;
}var bB=bA[1];
var bz=decodeURIComponent(bA[2]);
if(bz==z){bz=true;
}else if(bz==A){bz=false;
}else if(/^(\d|\.)+$/.test(bz)){bz=parseFloat(bz);
}this._checks[bB]=this.__n(bz);
}}},__n:function(bC){return qx.Bootstrap.bind(function(bD){return bD;
},null,bC);
},useCheck:function(bE){return true;
},_initChecksMap:function(){if(this.useCheck(N)){this._checks[N]=qx.bom.client.Engine.getVersion;
}
if(this.useCheck(r)){this._checks[r]=qx.bom.client.Engine.getName;
}if(this.useCheck(e)){this._checks[e]=qx.bom.client.Browser.getName;
}
if(this.useCheck(o)){this._checks[o]=qx.bom.client.Browser.getVersion;
}
if(this.useCheck(Q)){this._checks[Q]=qx.bom.client.Browser.getDocumentMode;
}
if(this.useCheck(f)){this._checks[f]=qx.bom.client.Browser.getQuirksMode;
}if(this.useCheck(O)){this._checks[O]=qx.bom.client.Locale.getLocale;
}
if(this.useCheck(a)){this._checks[a]=qx.bom.client.Locale.getVariant;
}if(this.useCheck(k)){this._checks[k]=qx.bom.client.OperatingSystem.getName;
}
if(this.useCheck(j)){this._checks[j]=qx.bom.client.OperatingSystem.getVersion;
}if(this.useCheck(S)){this._checks[S]=qx.bom.client.Transport.getMaxConcurrentRequestCount;
}
if(this.useCheck(b)){this._checks[b]=qx.bom.client.Transport.getSsl;
}if(this.useCheck(T)){this._checks[T]=qx.bom.client.Event.getTouch;
}
if(this.useCheck(c)){this._checks[c]=qx.bom.client.Event.getPointer;
}if(this.useCheck(P)){this._checks[P]=qx.bom.client.EcmaScript.getObjectCount;
}
if(this.useCheck(V)){this._checks[V]=qx.bom.client.Html.getXul;
}if(this.useCheck(W)){this._checks[W]=qx.bom.client.Css.getTextOverflow;
}
if(this.useCheck(q)){this._checks[q]=qx.bom.client.Css.getPlaceholder;
}
if(this.useCheck(h)){this._checks[h]=qx.bom.client.Css.getBorderRadius;
}
if(this.useCheck(U)){this._checks[U]=qx.bom.client.Css.getBoxShadow;
}
if(this.useCheck(R)){this._checks[R]=qx.bom.client.Css.getGradients;
}
if(this.useCheck(p)){this._checks[p]=qx.bom.client.Css.getBoxModel;
}
if(this.useCheck(s)){this._checks[s]=qx.bom.client.Css.getRgba;
}}},defer:function(bF){bF._initDefaultQxValues();
bF._initChecksMap();
bF.__l();
if(bF.get(d)===true){bF.__m();
}}});
})();
(function(){var h="qx.Mixin",g=".prototype",f="constructor",e="Array",d="[Mixin ",c="]",b="destruct",a="Mixin";
qx.Bootstrap.define(h,{statics:{define:function(name,j){if(j){if(j.include&&!(qx.Bootstrap.getClass(j.include)===e)){j.include=[j.include];
}var m=j.statics?j.statics:{};
qx.Bootstrap.setDisplayNames(m,name);

for(var k in m){if(m[k] instanceof Function){m[k].$$mixin=m;
}}if(j.construct){m.$$constructor=j.construct;
qx.Bootstrap.setDisplayName(j.construct,name,f);
}
if(j.include){m.$$includes=j.include;
}
if(j.properties){m.$$properties=j.properties;
}
if(j.members){m.$$members=j.members;
qx.Bootstrap.setDisplayNames(j.members,name+g);
}
for(var k in m.$$members){if(m.$$members[k] instanceof Function){m.$$members[k].$$mixin=m;
}}
if(j.events){m.$$events=j.events;
}
if(j.destruct){m.$$destructor=j.destruct;
qx.Bootstrap.setDisplayName(j.destruct,name,b);
}}else{var m={};
}m.$$type=a;
m.name=name;
m.toString=this.genericToString;
m.basename=qx.Bootstrap.createNamespace(name,m);
this.$$registry[name]=m;
return m;
},checkCompatibility:function(n){var q=this.flatten(n);
var r=q.length;

if(r<2){return true;
}var u={};
var t={};
var s={};
var p;

for(var i=0;i<r;i++){p=q[i];

for(var o in p.events){if(s[o]){throw new Error('Conflict between mixin "'+p.name+'" and "'+s[o]+'" in member "'+o+'"!');
}s[o]=p.name;
}
for(var o in p.properties){if(u[o]){throw new Error('Conflict between mixin "'+p.name+'" and "'+u[o]+'" in property "'+o+'"!');
}u[o]=p.name;
}
for(var o in p.members){if(t[o]){throw new Error('Conflict between mixin "'+p.name+'" and "'+t[o]+'" in member "'+o+'"!');
}t[o]=p.name;
}}return true;
},isCompatible:function(v,w){var x=qx.Bootstrap.getMixins(w);
x.push(v);
return qx.Mixin.checkCompatibility(x);
},getByName:function(name){return this.$$registry[name];
},isDefined:function(name){return this.getByName(name)!==undefined;
},getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},flatten:function(y){if(!y){return [];
}var z=y.concat();

for(var i=0,l=y.length;i<l;i++){if(y[i].$$includes){z.push.apply(z,this.flatten(y[i].$$includes));
}}return z;
},genericToString:function(){return d+this.name+c;
},$$registry:{},__o:null,__p:function(){}}});
})();
(function(){var j="function",h="Boolean",g="qx.Interface",f="Array",e="]",d="toggle",c="Interface",b="is",a="[Interface ";
qx.Bootstrap.define(g,{statics:{define:function(name,k){if(k){if(k.extend&&!(qx.Bootstrap.getClass(k.extend)===f)){k.extend=[k.extend];
}var m=k.statics?k.statics:{};
if(k.extend){m.$$extends=k.extend;
}
if(k.properties){m.$$properties=k.properties;
}
if(k.members){m.$$members=k.members;
}
if(k.events){m.$$events=k.events;
}}else{var m={};
}m.$$type=c;
m.name=name;
m.toString=this.genericToString;
m.basename=qx.Bootstrap.createNamespace(name,m);
qx.Interface.$$registry[name]=m;
return m;
},getByName:function(name){return this.$$registry[name];
},isDefined:function(name){return this.getByName(name)!==undefined;
},getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},flatten:function(n){if(!n){return [];
}var o=n.concat();

for(var i=0,l=n.length;i<l;i++){if(n[i].$$extends){o.push.apply(o,this.flatten(n[i].$$extends));
}}return o;
},__q:function(p,q,r,s){var w=r.$$members;

if(w){for(var v in w){if(qx.Bootstrap.isFunction(w[v])){var u=this.__r(q,v);
var t=u||qx.Bootstrap.isFunction(p[v]);

if(!t){throw new Error('Implementation of method "'+v+'" is missing in class "'+q.classname+'" required by interface "'+r.name+'"');
}var x=s===true&&!u&&!qx.Bootstrap.hasInterface(q,r);

if(x){p[v]=this.__u(r,p[v],v,w[v]);
}}else{if(typeof p[v]===undefined){if(typeof p[v]!==j){throw new Error('Implementation of member "'+v+'" is missing in class "'+q.classname+'" required by interface "'+r.name+'"');
}}}}}},__r:function(y,z){var D=z.match(/^(is|toggle|get|set|reset)(.*)$/);

if(!D){return false;
}var A=qx.Bootstrap.firstLow(D[2]);
var B=qx.Bootstrap.getPropertyDefinition(y,A);

if(!B){return false;
}var C=D[0]==b||D[0]==d;

if(C){return qx.Bootstrap.getPropertyDefinition(y,A).check==h;
}return true;
},__s:function(E,F){if(F.$$properties){for(var G in F.$$properties){if(!qx.Bootstrap.getPropertyDefinition(E,G)){throw new Error('The property "'+G+'" is not supported by Class "'+E.classname+'"!');
}}}},__t:function(H,I){if(I.$$events){for(var J in I.$$events){if(!qx.Bootstrap.supportsEvent(H,J)){throw new Error('The event "'+J+'" is not supported by Class "'+H.classname+'"!');
}}}},assertObject:function(K,L){var N=K.constructor;
this.__q(K,N,L,false);
this.__s(N,L);
this.__t(N,L);
var M=L.$$extends;

if(M){for(var i=0,l=M.length;i<l;i++){this.assertObject(K,M[i]);
}}},assert:function(O,P,Q){this.__q(O.prototype,O,P,Q);
this.__s(O,P);
this.__t(O,P);
var R=P.$$extends;

if(R){for(var i=0,l=R.length;i<l;i++){this.assert(O,R[i],Q);
}}},genericToString:function(){return a+this.name+e;
},$$registry:{},__u:function(){},__o:null,__p:function(){}}});
})();
(function(){var d="qx.core.Aspect",c="before",b="*",a="static";
qx.Bootstrap.define(d,{statics:{__v:[],wrap:function(e,f,g){var m=[];
var h=[];
var l=this.__v;
var k;

for(var i=0;i<l.length;i++){k=l[i];

if((k.type==null||g==k.type||k.type==b)&&(k.name==null||e.match(k.name))){k.pos==-1?m.push(k.fcn):h.push(k.fcn);
}}
if(m.length===0&&h.length===0){return f;
}var j=function(){for(var i=0;i<m.length;i++){m[i].call(this,e,f,g,arguments);
}var n=f.apply(this,arguments);

for(var i=0;i<h.length;i++){h[i].call(this,e,f,g,arguments,n);
}return n;
};

if(g!==a){j.self=f.self;
j.base=f.base;
}f.wrapper=j;
j.original=f;
return j;
},addAdvice:function(o,p,q,name){this.__v.push({fcn:o,pos:p===c?-1:1,type:q,name:name});
}}});
})();
(function(){var g="emulated",f="native",e='"',d="qx.lang.Core",c="\\\\",b="\\\"",a="[object Error]";
qx.Bootstrap.define(d,{statics:{errorToString:{"native":Error.prototype.toString,"emulated":function(){return this.message;
}}[(!Error.prototype.toString||Error.prototype.toString()==a)?g:f],arrayIndexOf:{"native":Array.prototype.indexOf,"emulated":function(h,j){if(j==null){j=0;
}else if(j<0){j=Math.max(0,this.length+j);
}
for(var i=j;i<this.length;i++){if(this[i]===h){return i;
}}return -1;
}}[Array.prototype.indexOf?f:g],arrayLastIndexOf:{"native":Array.prototype.lastIndexOf,"emulated":function(k,m){if(m==null){m=this.length-1;
}else if(m<0){m=Math.max(0,this.length+m);
}
for(var i=m;i>=0;i--){if(this[i]===k){return i;
}}return -1;
}}[Array.prototype.lastIndexOf?f:g],arrayForEach:{"native":Array.prototype.forEach,"emulated":function(n,o){var l=this.length;

for(var i=0;i<l;i++){var p=this[i];

if(p!==undefined){n.call(o||window,p,i,this);
}}}}[Array.prototype.forEach?f:g],arrayFilter:{"native":Array.prototype.filter,"emulated":function(q,r){var s=[];
var l=this.length;

for(var i=0;i<l;i++){var t=this[i];

if(t!==undefined){if(q.call(r||window,t,i,this)){s.push(this[i]);
}}}return s;
}}[Array.prototype.filter?f:g],arrayMap:{"native":Array.prototype.map,"emulated":function(u,v){var w=[];
var l=this.length;

for(var i=0;i<l;i++){var x=this[i];

if(x!==undefined){w[i]=u.call(v||window,x,i,this);
}}return w;
}}[Array.prototype.map?f:g],arraySome:{"native":Array.prototype.some,"emulated":function(y,z){var l=this.length;

for(var i=0;i<l;i++){var A=this[i];

if(A!==undefined){if(y.call(z||window,A,i,this)){return true;
}}}return false;
}}[Array.prototype.some?f:g],arrayEvery:{"native":Array.prototype.every,"emulated":function(B,C){var l=this.length;

for(var i=0;i<l;i++){var D=this[i];

if(D!==undefined){if(!B.call(C||window,D,i,this)){return false;
}}}return true;
}}[Array.prototype.every?f:g],stringQuote:{"native":String.prototype.quote,"emulated":function(){return e+this.replace(/\\/g,c).replace(/\"/g,b)+e;
}}[String.prototype.quote?f:g]}});
Error.prototype.toString=qx.lang.Core.errorToString;
Array.prototype.indexOf=qx.lang.Core.arrayIndexOf;
Array.prototype.lastIndexOf=qx.lang.Core.arrayLastIndexOf;
Array.prototype.forEach=qx.lang.Core.arrayForEach;
Array.prototype.filter=qx.lang.Core.arrayFilter;
Array.prototype.map=qx.lang.Core.arrayMap;
Array.prototype.some=qx.lang.Core.arraySome;
Array.prototype.every=qx.lang.Core.arrayEvery;
String.prototype.quote=qx.lang.Core.stringQuote;
})();
(function(){var m=';',k='return this.',j="boolean",h="string",g='!==undefined)',f='else if(this.',e='if(this.',d='else ',c=' of an instance of ',b=' is not (yet) ready!");',bi="init",bh='qx.lang.Type.isString(value) && qx.util.ColorUtil.isValidPropertyValue(value)',bg='value !== null && qx.theme.manager.Font.getInstance().isDynamic(value)',bf=" of class ",be='qx.core.Assert.assertInstance(value, Date, msg) || true',bd='value !== null && value.nodeType !== undefined',bc='var inherit=prop.$$inherit;',bb='value !== null && value.nodeType === 9 && value.documentElement',ba='return init;',Y='value !== null && value.$$type === "Mixin"',t='qx.core.Assert.assertMap(value, msg) || true',u='var init=this.',r='return value;',s='qx.core.Assert.assertNumber(value, msg) || true',p='qx.core.Assert.assertPositiveInteger(value, msg) || true',q="': ",n="Error in property ",o='if(init==qx.core.Property.$$inherit)init=null;',x='qx.core.Assert.assertInteger(value, msg) || true',y="rv:1.8.1",G='value !== null && value.$$type === "Interface"',E="set",O='value !== null && value.$$type === "Theme"',J='qx.core.Assert.assertInstance(value, RegExp, msg) || true',U='value !== null && value.type !== undefined',S='value !== null && value.document',A=" in method ",X='qx.core.Assert.assertInstance(value, Error, msg) || true',W='throw new Error("Property ',V='qx.core.Assert.assertBoolean(value, msg) || true',z='return null;',C='qx.core.Assert.assertObject(value, msg) || true',D="setRuntime",F='value !== null && value.nodeType === 1 && value.attributes',H=" with incoming value '",K="setThemed",P='qx.core.Assert.assertString(value, msg) || true',T="inherit",v='value !== null && value.$$type === "Class"',w='qx.core.Assert.assertFunction(value, msg) || true',B='value !== null && qx.theme.manager.Decoration.getInstance().isValidPropertyValue(value)',N='qx.core.Assert.assertArray(value, msg) || true',M='qx.core.Assert.assertPositiveNumber(value, msg) || true',L="object",R="MSIE 6.0",Q='if(init==qx.core.Property.$$inherit)throw new Error("Inheritable property ',I="qx.core.Property";
qx.Bootstrap.define(I,{statics:{__w:{"Boolean":V,"String":P,"Number":s,"Integer":x,"PositiveNumber":M,"PositiveInteger":p,"Error":X,"RegExp":J,"Object":C,"Array":N,"Map":t,"Function":w,"Date":be,"Node":bd,"Element":F,"Document":bb,"Window":S,"Event":U,"Class":v,"Mixin":Y,"Interface":G,"Theme":O,"Color":bh,"Decorator":B,"Font":bg},__x:{"Node":true,"Element":true,"Document":true,"Window":true,"Event":true},$$inherit:T,$$store:{runtime:{},user:{},theme:{},inherit:{},init:{},useinit:{}},$$method:{get:{},set:{},reset:{},init:{},refresh:{},setRuntime:{},resetRuntime:{},setThemed:{},resetThemed:{}},$$allowedKeys:{name:h,dereference:j,inheritable:j,nullable:j,themeable:j,refine:j,init:null,apply:h,event:h,check:null,transform:h,deferredInit:j,validate:null},$$allowedGroupKeys:{name:h,group:L,mode:h,themeable:j},$$inheritable:{},__y:function(bj){var bk=this.__z(bj);

if(!bk.length){var bl=function(){};
}else{bl=this.__A(bk);
}bj.prototype.$$refreshInheritables=bl;
},__z:function(bm){var bo=[];

while(bm){var bn=bm.$$properties;

if(bn){for(var name in this.$$inheritable){if(bn[name]&&bn[name].inheritable){bo.push(name);
}}}bm=bm.superclass;
}return bo;
},__A:function(bp){var bt=this.$$store.inherit;
var bs=this.$$store.init;
var br=this.$$method.refresh;
var bq=["var parent = this.getLayoutParent();","if (!parent) return;"];

for(var i=0,l=bp.length;i<l;i++){var name=bp[i];
bq.push("var value = parent.",bt[name],";","if (value===undefined) value = parent.",bs[name],";","this.",br[name],"(value);");
}return new Function(bq.join(""));
},attachRefreshInheritables:function(bu){bu.prototype.$$refreshInheritables=function(){qx.core.Property.__y(bu);
return this.$$refreshInheritables();
};
},attachMethods:function(bv,name,bw){bw.group?this.__B(bv,bw,name):this.__C(bv,bw,name);
},__B:function(bx,by,name){var bF=qx.Bootstrap.firstUp(name);
var bE=bx.prototype;
var bG=by.themeable===true;
var bH=[];
var bB=[];

if(bG){var bz=[];
var bD=[];
}var bC="var a=arguments[0] instanceof Array?arguments[0]:arguments;";
bH.push(bC);

if(bG){bz.push(bC);
}
if(by.mode=="shorthand"){var bA="a=qx.lang.Array.fromShortHand(qx.lang.Array.fromArguments(a));";
bH.push(bA);

if(bG){bz.push(bA);
}}
for(var i=0,a=by.group,l=a.length;i<l;i++){bH.push("this.",this.$$method.set[a[i]],"(a[",i,"]);");
bB.push("this.",this.$$method.reset[a[i]],"();");

if(bG){bz.push("this.",this.$$method.setThemed[a[i]],"(a[",i,"]);");
bD.push("this.",this.$$method.resetThemed[a[i]],"();");
}}this.$$method.set[name]="set"+bF;
bE[this.$$method.set[name]]=new Function(bH.join(""));
this.$$method.reset[name]="reset"+bF;
bE[this.$$method.reset[name]]=new Function(bB.join(""));

if(bG){this.$$method.setThemed[name]="setThemed"+bF;
bE[this.$$method.setThemed[name]]=new Function(bz.join(""));
this.$$method.resetThemed[name]="resetThemed"+bF;
bE[this.$$method.resetThemed[name]]=new Function(bD.join(""));
}},__C:function(bI,bJ,name){var bL=qx.Bootstrap.firstUp(name);
var bN=bI.prototype;
if(bJ.dereference===undefined&&typeof bJ.check==="string"){bJ.dereference=this.__D(bJ.check);
}var bM=this.$$method;
var bK=this.$$store;
bK.runtime[name]="$$runtime_"+name;
bK.user[name]="$$user_"+name;
bK.theme[name]="$$theme_"+name;
bK.init[name]="$$init_"+name;
bK.inherit[name]="$$inherit_"+name;
bK.useinit[name]="$$useinit_"+name;
bM.get[name]="get"+bL;
bN[bM.get[name]]=function(){return qx.core.Property.executeOptimizedGetter(this,bI,name,"get");
};
bM.set[name]="set"+bL;
bN[bM.set[name]]=function(bO){return qx.core.Property.executeOptimizedSetter(this,bI,name,"set",arguments);
};
bM.reset[name]="reset"+bL;
bN[bM.reset[name]]=function(){return qx.core.Property.executeOptimizedSetter(this,bI,name,"reset");
};

if(bJ.inheritable||bJ.apply||bJ.event||bJ.deferredInit){bM.init[name]="init"+bL;
bN[bM.init[name]]=function(bP){return qx.core.Property.executeOptimizedSetter(this,bI,name,"init",arguments);
};
}
if(bJ.inheritable){bM.refresh[name]="refresh"+bL;
bN[bM.refresh[name]]=function(bQ){return qx.core.Property.executeOptimizedSetter(this,bI,name,"refresh",arguments);
};
}bM.setRuntime[name]="setRuntime"+bL;
bN[bM.setRuntime[name]]=function(bR){return qx.core.Property.executeOptimizedSetter(this,bI,name,"setRuntime",arguments);
};
bM.resetRuntime[name]="resetRuntime"+bL;
bN[bM.resetRuntime[name]]=function(){return qx.core.Property.executeOptimizedSetter(this,bI,name,"resetRuntime");
};

if(bJ.themeable){bM.setThemed[name]="setThemed"+bL;
bN[bM.setThemed[name]]=function(bS){return qx.core.Property.executeOptimizedSetter(this,bI,name,"setThemed",arguments);
};
bM.resetThemed[name]="resetThemed"+bL;
bN[bM.resetThemed[name]]=function(){return qx.core.Property.executeOptimizedSetter(this,bI,name,"resetThemed");
};
}
if(bJ.check==="Boolean"){bN["toggle"+bL]=new Function("return this."+bM.set[name]+"(!this."+bM.get[name]+"())");
bN["is"+bL]=new Function("return this."+bM.get[name]+"()");
}},__D:function(bT){return !!this.__x[bT];
},__E:function(bU){return this.__x[bU]||qx.Bootstrap.classIsDefined(bU)||(qx.Interface&&qx.Interface.isDefined(bU));
},__F:{0:'Could not change or apply init value after constructing phase!',1:'Requires exactly one argument!',2:'Undefined value is not allowed!',3:'Does not allow any arguments!',4:'Null value is not allowed!',5:'Is invalid!'},error:function(bV,bW,bX,bY,ca){var cb=bV.constructor.classname;
var cc=n+bX+bf+cb+A+this.$$method[bY][bX]+H+ca+q;
throw new Error(cc+(this.__F[bW]||"Unknown reason: "+bW));
},__G:function(cd,ce,name,cf,cg,ch){var ci=this.$$method[cf][name];
{ce[ci]=new Function("value",cg.join(""));
};
if(qx.core.Environment.get("qx.aspects")){ce[ci]=qx.core.Aspect.wrap(cd.classname+"."+ci,ce[ci],"property");
}qx.Bootstrap.setDisplayName(ce[ci],cd.classname+".prototype",ci);
if(ch===undefined){return cd[ci]();
}else{return cd[ci](ch[0]);
}},executeOptimizedGetter:function(cj,ck,name,cl){var cn=ck.$$properties[name];
var cp=ck.prototype;
var cm=[];
var co=this.$$store;
cm.push(e,co.runtime[name],g);
cm.push(k,co.runtime[name],m);

if(cn.inheritable){cm.push(f,co.inherit[name],g);
cm.push(k,co.inherit[name],m);
cm.push(d);
}cm.push(e,co.user[name],g);
cm.push(k,co.user[name],m);

if(cn.themeable){cm.push(f,co.theme[name],g);
cm.push(k,co.theme[name],m);
}
if(cn.deferredInit&&cn.init===undefined){cm.push(f,co.init[name],g);
cm.push(k,co.init[name],m);
}cm.push(d);

if(cn.init!==undefined){if(cn.inheritable){cm.push(u,co.init[name],m);

if(cn.nullable){cm.push(o);
}else if(cn.init!==undefined){cm.push(k,co.init[name],m);
}else{cm.push(Q,name,c,ck.classname,b);
}cm.push(ba);
}else{cm.push(k,co.init[name],m);
}}else if(cn.inheritable||cn.nullable){cm.push(z);
}else{cm.push(W,name,c,ck.classname,b);
}return this.__G(cj,cp,name,cl,cm);
},executeOptimizedSetter:function(cq,cr,name,cs,ct){var cy=cr.$$properties[name];
var cx=cr.prototype;
var cv=[];
var cu=cs===E||cs===K||cs===D||(cs===bi&&cy.init===undefined);
var cw=cy.apply||cy.event||cy.inheritable;
var cz=this.__H(cs,name);
this.__I(cv,cy,name,cs,cu);

if(cu){this.__J(cv,cr,cy,name);
}
if(cw){this.__K(cv,cu,cz,cs);
}
if(cy.inheritable){cv.push(bc);
}
if(!cw){this.__M(cv,name,cs,cu);
}else{this.__N(cv,cy,name,cs,cu);
}
if(cy.inheritable){this.__O(cv,cy,name,cs);
}else if(cw){this.__P(cv,cy,name,cs);
}
if(cw){this.__Q(cv,cy,name);
if(cy.inheritable&&cx._getChildren){this.__R(cv,name);
}}if(cu){cv.push(r);
}return this.__G(cq,cx,name,cs,cv,ct);
},__H:function(cA,name){if(cA==="setRuntime"||cA==="resetRuntime"){var cB=this.$$store.runtime[name];
}else if(cA==="setThemed"||cA==="resetThemed"){cB=this.$$store.theme[name];
}else if(cA==="init"){cB=this.$$store.init[name];
}else{cB=this.$$store.user[name];
}return cB;
},__I:function(cC,cD,name,cE,cF){{if(!cD.nullable||cD.check||cD.inheritable){cC.push('var prop=qx.core.Property;');
}if(cE==="set"){cC.push('if(value===undefined)prop.error(this,2,"',name,'","',cE,'",value);');
}};
},__J:function(cG,cH,cI,name){if(cI.transform){cG.push('value=this.',cI.transform,'(value);');
}if(cI.validate){if(typeof cI.validate==="string"){cG.push('this.',cI.validate,'(value);');
}else if(cI.validate instanceof Function){cG.push(cH.classname,'.$$properties.',name);
cG.push('.validate.call(this, value);');
}}},__K:function(cJ,cK,cL,cM){var cN=(cM==="reset"||cM==="resetThemed"||cM==="resetRuntime");

if(cK){cJ.push('if(this.',cL,'===value)return value;');
}else if(cN){cJ.push('if(this.',cL,'===undefined)return;');
}},__L:undefined,__M:function(cO,name,cP,cQ){if(cP==="setRuntime"){cO.push('this.',this.$$store.runtime[name],'=value;');
}else if(cP==="resetRuntime"){cO.push('if(this.',this.$$store.runtime[name],'!==undefined)');
cO.push('delete this.',this.$$store.runtime[name],';');
}else if(cP==="set"){cO.push('this.',this.$$store.user[name],'=value;');
}else if(cP==="reset"){cO.push('if(this.',this.$$store.user[name],'!==undefined)');
cO.push('delete this.',this.$$store.user[name],';');
}else if(cP==="setThemed"){cO.push('this.',this.$$store.theme[name],'=value;');
}else if(cP==="resetThemed"){cO.push('if(this.',this.$$store.theme[name],'!==undefined)');
cO.push('delete this.',this.$$store.theme[name],';');
}else if(cP==="init"&&cQ){cO.push('this.',this.$$store.init[name],'=value;');
}},__N:function(cR,cS,name,cT,cU){if(cS.inheritable){cR.push('var computed, old=this.',this.$$store.inherit[name],';');
}else{cR.push('var computed, old;');
}cR.push('if(this.',this.$$store.runtime[name],'!==undefined){');

if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="resetRuntime"){cR.push('delete this.',this.$$store.runtime[name],';');
cR.push('if(this.',this.$$store.user[name],'!==undefined)');
cR.push('computed=this.',this.$$store.user[name],';');
cR.push('else if(this.',this.$$store.theme[name],'!==undefined)');
cR.push('computed=this.',this.$$store.theme[name],';');
cR.push('else if(this.',this.$$store.init[name],'!==undefined){');
cR.push('computed=this.',this.$$store.init[name],';');
cR.push('this.',this.$$store.useinit[name],'=true;');
cR.push('}');
}else{cR.push('old=computed=this.',this.$$store.runtime[name],';');
if(cT==="set"){cR.push('this.',this.$$store.user[name],'=value;');
}else if(cT==="reset"){cR.push('delete this.',this.$$store.user[name],';');
}else if(cT==="setThemed"){cR.push('this.',this.$$store.theme[name],'=value;');
}else if(cT==="resetThemed"){cR.push('delete this.',this.$$store.theme[name],';');
}else if(cT==="init"&&cU){cR.push('this.',this.$$store.init[name],'=value;');
}}cR.push('}');
cR.push('else if(this.',this.$$store.user[name],'!==undefined){');

if(cT==="set"){if(!cS.inheritable){cR.push('old=this.',this.$$store.user[name],';');
}cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="reset"){if(!cS.inheritable){cR.push('old=this.',this.$$store.user[name],';');
}cR.push('delete this.',this.$$store.user[name],';');
cR.push('if(this.',this.$$store.runtime[name],'!==undefined)');
cR.push('computed=this.',this.$$store.runtime[name],';');
cR.push('if(this.',this.$$store.theme[name],'!==undefined)');
cR.push('computed=this.',this.$$store.theme[name],';');
cR.push('else if(this.',this.$$store.init[name],'!==undefined){');
cR.push('computed=this.',this.$$store.init[name],';');
cR.push('this.',this.$$store.useinit[name],'=true;');
cR.push('}');
}else{if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cS.inheritable){cR.push('computed=this.',this.$$store.user[name],';');
}else{cR.push('old=computed=this.',this.$$store.user[name],';');
}if(cT==="setThemed"){cR.push('this.',this.$$store.theme[name],'=value;');
}else if(cT==="resetThemed"){cR.push('delete this.',this.$$store.theme[name],';');
}else if(cT==="init"&&cU){cR.push('this.',this.$$store.init[name],'=value;');
}}cR.push('}');
if(cS.themeable){cR.push('else if(this.',this.$$store.theme[name],'!==undefined){');

if(!cS.inheritable){cR.push('old=this.',this.$$store.theme[name],';');
}
if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="set"){cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="setThemed"){cR.push('computed=this.',this.$$store.theme[name],'=value;');
}else if(cT==="resetThemed"){cR.push('delete this.',this.$$store.theme[name],';');
cR.push('if(this.',this.$$store.init[name],'!==undefined){');
cR.push('computed=this.',this.$$store.init[name],';');
cR.push('this.',this.$$store.useinit[name],'=true;');
cR.push('}');
}else if(cT==="init"){if(cU){cR.push('this.',this.$$store.init[name],'=value;');
}cR.push('computed=this.',this.$$store.theme[name],';');
}else if(cT==="refresh"){cR.push('computed=this.',this.$$store.theme[name],';');
}cR.push('}');
}cR.push('else if(this.',this.$$store.useinit[name],'){');

if(!cS.inheritable){cR.push('old=this.',this.$$store.init[name],';');
}
if(cT==="init"){if(cU){cR.push('computed=this.',this.$$store.init[name],'=value;');
}else{cR.push('computed=this.',this.$$store.init[name],';');
}}else if(cT==="set"||cT==="setRuntime"||cT==="setThemed"||cT==="refresh"){cR.push('delete this.',this.$$store.useinit[name],';');

if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="set"){cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="setThemed"){cR.push('computed=this.',this.$$store.theme[name],'=value;');
}else if(cT==="refresh"){cR.push('computed=this.',this.$$store.init[name],';');
}}cR.push('}');
if(cT==="set"||cT==="setRuntime"||cT==="setThemed"||cT==="init"){cR.push('else{');

if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="set"){cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="setThemed"){cR.push('computed=this.',this.$$store.theme[name],'=value;');
}else if(cT==="init"){if(cU){cR.push('computed=this.',this.$$store.init[name],'=value;');
}else{cR.push('computed=this.',this.$$store.init[name],';');
}cR.push('this.',this.$$store.useinit[name],'=true;');
}cR.push('}');
}},__O:function(cV,cW,name,cX){cV.push('if(computed===undefined||computed===inherit){');

if(cX==="refresh"){cV.push('computed=value;');
}else{cV.push('var pa=this.getLayoutParent();if(pa)computed=pa.',this.$$store.inherit[name],';');
}cV.push('if((computed===undefined||computed===inherit)&&');
cV.push('this.',this.$$store.init[name],'!==undefined&&');
cV.push('this.',this.$$store.init[name],'!==inherit){');
cV.push('computed=this.',this.$$store.init[name],';');
cV.push('this.',this.$$store.useinit[name],'=true;');
cV.push('}else{');
cV.push('delete this.',this.$$store.useinit[name],';}');
cV.push('}');
cV.push('if(old===computed)return value;');
cV.push('if(computed===inherit){');
cV.push('computed=undefined;delete this.',this.$$store.inherit[name],';');
cV.push('}');
cV.push('else if(computed===undefined)');
cV.push('delete this.',this.$$store.inherit[name],';');
cV.push('else this.',this.$$store.inherit[name],'=computed;');
cV.push('var backup=computed;');
if(cW.init!==undefined&&cX!=="init"){cV.push('if(old===undefined)old=this.',this.$$store.init[name],";");
}else{cV.push('if(old===undefined)old=null;');
}cV.push('if(computed===undefined||computed==inherit)computed=null;');
},__P:function(cY,da,name,db){if(db!=="set"&&db!=="setRuntime"&&db!=="setThemed"){cY.push('if(computed===undefined)computed=null;');
}cY.push('if(old===computed)return value;');
if(da.init!==undefined&&db!=="init"){cY.push('if(old===undefined)old=this.',this.$$store.init[name],";");
}else{cY.push('if(old===undefined)old=null;');
}},__Q:function(dc,dd,name){if(dd.apply){dc.push('this.',dd.apply,'(computed, old, "',name,'");');
}if(dd.event){dc.push("var reg=qx.event.Registration;","if(reg.hasListener(this, '",dd.event,"')){","reg.fireEvent(this, '",dd.event,"', qx.event.type.Data, [computed, old]",")}");
}},__R:function(de,name){de.push('var a=this._getChildren();if(a)for(var i=0,l=a.length;i<l;i++){');
de.push('if(a[i].',this.$$method.refresh[name],')a[i].',this.$$method.refresh[name],'(backup);');
de.push('}');
}},defer:function(df){var dh=navigator.userAgent.indexOf(R)!=-1;
var dg=navigator.userAgent.indexOf(y)!=-1;
if(dh||dg){df.__D=df.__E;
}}});
})();
(function(){var k="qx.aspects",j="Array",h=".",g="static",f="[Class ",e="]",d="constructor",c="extend",b="qx.Class";
qx.Bootstrap.define(b,{statics:{define:function(name,m){if(!m){var m={};
}if(m.include&&!(qx.Bootstrap.getClass(m.include)===j)){m.include=[m.include];
}if(m.implement&&!(qx.Bootstrap.getClass(m.implement)===j)){m.implement=[m.implement];
}var n=false;

if(!m.hasOwnProperty(c)&&!m.type){m.type=g;
n=true;
}var o=this.__U(name,m.type,m.extend,m.statics,m.construct,m.destruct,m.include);
if(m.extend){if(m.properties){this.__W(o,m.properties,true);
}if(m.members){this.__Y(o,m.members,true,true,false);
}if(m.events){this.__V(o,m.events,true);
}if(m.include){for(var i=0,l=m.include.length;i<l;i++){this.__bd(o,m.include[i],false);
}}}if(m.environment){for(var p in m.environment){qx.core.Environment.add(p,m.environment[p]);
}}if(m.implement){for(var i=0,l=m.implement.length;i<l;i++){this.__bb(o,m.implement[i]);
}}if(m.defer){m.defer.self=o;
m.defer(o,o.prototype,{add:function(name,q){var r={};
r[name]=q;
qx.Class.__W(o,r,true);
}});
}return o;
},undefine:function(name){delete this.$$registry[name];
var s=name.split(h);
var u=[window];

for(var i=0;i<s.length;i++){u.push(u[i][s[i]]);
}for(var i=u.length-1;i>=1;i--){var t=u[i];
var parent=u[i-1];

if(qx.Bootstrap.isFunction(t)||qx.Bootstrap.objectGetLength(t)===0){delete parent[s[i-1]];
}else{break;
}}},isDefined:qx.Bootstrap.classIsDefined,getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},getByName:qx.Bootstrap.getByName,include:function(v,w){qx.Class.__bd(v,w,false);
},patch:function(x,y){qx.Class.__bd(x,y,true);
},isSubClassOf:function(z,A){if(!z){return false;
}
if(z==A){return true;
}
if(z.prototype instanceof A){return true;
}return false;
},getPropertyDefinition:qx.Bootstrap.getPropertyDefinition,getProperties:function(B){var C=[];

while(B){if(B.$$properties){C.push.apply(C,qx.Bootstrap.getKeys(B.$$properties));
}B=B.superclass;
}return C;
},getByProperty:function(D,name){while(D){if(D.$$properties&&D.$$properties[name]){return D;
}D=D.superclass;
}return null;
},hasProperty:qx.Bootstrap.hasProperty,getEventType:qx.Bootstrap.getEventType,supportsEvent:qx.Bootstrap.supportsEvent,hasOwnMixin:function(E,F){return E.$$includes&&E.$$includes.indexOf(F)!==-1;
},getByMixin:function(G,H){var I,i,l;

while(G){if(G.$$includes){I=G.$$flatIncludes;

for(i=0,l=I.length;i<l;i++){if(I[i]===H){return G;
}}}G=G.superclass;
}return null;
},getMixins:qx.Bootstrap.getMixins,hasMixin:function(J,K){return !!this.getByMixin(J,K);
},hasOwnInterface:function(L,M){return L.$$implements&&L.$$implements.indexOf(M)!==-1;
},getByInterface:qx.Bootstrap.getByInterface,getInterfaces:function(N){var O=[];

while(N){if(N.$$implements){O.push.apply(O,N.$$flatImplements);
}N=N.superclass;
}return O;
},hasInterface:qx.Bootstrap.hasInterface,implementsInterface:function(P,Q){var R=P.constructor;

if(this.hasInterface(R,Q)){return true;
}
try{qx.Interface.assertObject(P,Q);
return true;
}catch(S){}
try{qx.Interface.assert(R,Q,false);
return true;
}catch(T){}return false;
},getInstance:function(){if(!this.$$instance){this.$$allowconstruct=true;
this.$$instance=new this;
delete this.$$allowconstruct;
}return this.$$instance;
},genericToString:function(){return f+this.classname+e;
},$$registry:qx.Bootstrap.$$registry,__o:null,__S:null,__p:function(){},__T:function(){},__U:function(name,U,V,W,X,Y,ba){var bd;

if(!V&&qx.core.Environment.get("qx.aspects")==false){bd=W||{};
qx.Bootstrap.setDisplayNames(bd,name);
}else{var bd={};

if(V){if(!X){X=this.__be();
}
if(this.__bg(V,ba)){bd=this.__bh(X,name,U);
}else{bd=X;
}if(U==="singleton"){bd.getInstance=this.getInstance;
}qx.Bootstrap.setDisplayName(X,name,"constructor");
}if(W){qx.Bootstrap.setDisplayNames(W,name);
var be;

for(var i=0,a=qx.Bootstrap.getKeys(W),l=a.length;i<l;i++){be=a[i];
var bb=W[be];

if(qx.core.Environment.get("qx.aspects")){if(bb instanceof Function){bb=qx.core.Aspect.wrap(name+"."+be,bb,"static");
}bd[be]=bb;
}else{bd[be]=bb;
}}}}var bc=qx.Bootstrap.createNamespace(name,bd);
bd.name=bd.classname=name;
bd.basename=bc;
bd.$$type="Class";

if(U){bd.$$classtype=U;
}if(!bd.hasOwnProperty("toString")){bd.toString=this.genericToString;
}
if(V){qx.Bootstrap.extendClass(bd,X,V,name,bc);
if(Y){if(qx.core.Environment.get("qx.aspects")){Y=qx.core.Aspect.wrap(name,Y,"destructor");
}bd.$$destructor=Y;
qx.Bootstrap.setDisplayName(Y,name,"destruct");
}}this.$$registry[name]=bd;
return bd;
},__V:function(bf,bg,bh){var bi,bi;

if(bf.$$events){for(var bi in bg){bf.$$events[bi]=bg[bi];
}}else{bf.$$events=bg;
}},__W:function(bj,bk,bl){var bm;

if(bl===undefined){bl=false;
}var bn=bj.prototype;

for(var name in bk){bm=bk[name];
bm.name=name;
if(!bm.refine){if(bj.$$properties===undefined){bj.$$properties={};
}bj.$$properties[name]=bm;
}if(bm.init!==undefined){bj.prototype["$$init_"+name]=bm.init;
}if(bm.event!==undefined){var event={};
event[bm.event]="qx.event.type.Data";
this.__V(bj,event,bl);
}if(bm.inheritable){qx.core.Property.$$inheritable[name]=true;

if(!bn.$$refreshInheritables){qx.core.Property.attachRefreshInheritables(bj);
}}
if(!bm.refine){qx.core.Property.attachMethods(bj,name,bm);
}}},__X:null,__Y:function(bo,bp,bq,br,bs){var bt=bo.prototype;
var bv,bu;
qx.Bootstrap.setDisplayNames(bp,bo.classname+".prototype");

for(var i=0,a=qx.Bootstrap.getKeys(bp),l=a.length;i<l;i++){bv=a[i];
bu=bp[bv];
if(br!==false&&bu instanceof Function&&bu.$$type==null){if(bs==true){bu=this.__ba(bu,bt[bv]);
}else{if(bt[bv]){bu.base=bt[bv];
}bu.self=bo;
}
if(qx.core.Environment.get("qx.aspects")){bu=qx.core.Aspect.wrap(bo.classname+"."+bv,bu,"member");
}}bt[bv]=bu;
}},__ba:function(bw,bx){if(bx){return function(){var bz=bw.base;
bw.base=bx;
var by=bw.apply(this,arguments);
bw.base=bz;
return by;
};
}else{return bw;
}},__bb:function(bA,bB){var bC=qx.Interface.flatten([bB]);

if(bA.$$implements){bA.$$implements.push(bB);
bA.$$flatImplements.push.apply(bA.$$flatImplements,bC);
}else{bA.$$implements=[bB];
bA.$$flatImplements=bC;
}},__bc:function(bD){var name=bD.classname;
var bE=this.__bh(bD,name,bD.$$classtype);
for(var i=0,a=qx.Bootstrap.getKeys(bD),l=a.length;i<l;i++){bF=a[i];
bE[bF]=bD[bF];
}bE.prototype=bD.prototype;
var bH=bD.prototype;

for(var i=0,a=qx.Bootstrap.getKeys(bH),l=a.length;i<l;i++){bF=a[i];
var bI=bH[bF];
if(bI&&bI.self==bD){bI.self=bE;
}}for(var bF in this.$$registry){var bG=this.$$registry[bF];

if(!bG){continue;
}
if(bG.base==bD){bG.base=bE;
}
if(bG.superclass==bD){bG.superclass=bE;
}
if(bG.$$original){if(bG.$$original.base==bD){bG.$$original.base=bE;
}
if(bG.$$original.superclass==bD){bG.$$original.superclass=bE;
}}}qx.Bootstrap.createNamespace(name,bE);
this.$$registry[name]=bE;
return bE;
},__bd:function(bJ,bK,bL){if(this.hasMixin(bJ,bK)){return;
}var bO=bJ.$$original;

if(bK.$$constructor&&!bO){bJ=this.__bc(bJ);
}var bN=qx.Mixin.flatten([bK]);
var bM;

for(var i=0,l=bN.length;i<l;i++){bM=bN[i];
if(bM.$$events){this.__V(bJ,bM.$$events,bL);
}if(bM.$$properties){this.__W(bJ,bM.$$properties,bL);
}if(bM.$$members){this.__Y(bJ,bM.$$members,bL,bL,bL);
}}if(bJ.$$includes){bJ.$$includes.push(bK);
bJ.$$flatIncludes.push.apply(bJ.$$flatIncludes,bN);
}else{bJ.$$includes=[bK];
bJ.$$flatIncludes=bN;
}},__be:function(){function bP(){bP.base.apply(this,arguments);
}return bP;
},__bf:function(){return function(){};
},__bg:function(bQ,bR){if(bQ&&bQ.$$includes){var bS=bQ.$$flatIncludes;

for(var i=0,l=bS.length;i<l;i++){if(bS[i].$$constructor){return true;
}}}if(bR){var bT=qx.Mixin.flatten(bR);

for(var i=0,l=bT.length;i<l;i++){if(bT[i].$$constructor){return true;
}}}return false;
},__bh:function(bU,name,bV){var bX=function(){var cb=bX;
var ca=cb.$$original.apply(this,arguments);
if(cb.$$includes){var bY=cb.$$flatIncludes;

for(var i=0,l=bY.length;i<l;i++){if(bY[i].$$constructor){bY[i].$$constructor.apply(this,arguments);
}}}return ca;
};

if(qx.core.Environment.get(k)){var bW=qx.core.Aspect.wrap(name,bX,d);
bX.$$original=bU;
bX.constructor=bW;
bX=bW;
}bX.$$original=bU;
bU.wrapper=bX;
return bX;
}},defer:function(){if(qx.core.Environment.get(k)){for(var cc in qx.Bootstrap.$$registry){var cd=qx.Bootstrap.$$registry[cc];

for(var ce in cd){if(cd[ce] instanceof Function){cd[ce]=qx.core.Aspect.wrap(cc+h+ce,cd[ce],g);
}}}}}});
})();
(function(){var c="qx.event.type.Data",b="qx.event.type.Event",a="qx.data.IListData";
qx.Interface.define(a,{events:{"change":c,"changeLength":b},members:{getItem:function(d){},setItem:function(e,f){},splice:function(g,h,i){},contains:function(j){},getLength:function(){},toArray:function(){}}});
})();
(function(){var k="indexOf",j="lastIndexOf",h="slice",g="concat",f="join",e="toLocaleUpperCase",d="shift",c="substr",b="filter",a="unshift",I="match",H="quote",G="qx.lang.Generics",F="localeCompare",E="sort",D="some",C="charAt",B="split",A="substring",z="pop",t="toUpperCase",u="replace",q="push",r="charCodeAt",o="every",p="reverse",m="search",n="forEach",v="map",w="toLowerCase",y="splice",x="toLocaleLowerCase";
qx.Class.define(G,{statics:{__bi:{"Array":[f,p,E,q,z,d,a,y,g,h,k,j,n,v,b,D,o],"String":[H,A,w,t,C,r,k,j,x,e,F,I,m,u,B,c,g,h]},__bj:function(J,K){return function(s){return J.prototype[K].apply(s,Array.prototype.slice.call(arguments,1));
};
},__bk:function(){var L=qx.lang.Generics.__bi;

for(var P in L){var N=window[P];
var M=L[P];

for(var i=0,l=M.length;i<l;i++){var O=M[i];

if(!N[O]){N[O]=qx.lang.Generics.__bj(N,O);
}}}}},defer:function(Q){Q.__bk();
}});
})();
(function(){var a="qx.data.MBinding";
qx.Mixin.define(a,{members:{bind:function(b,c,d,e){return qx.data.SingleValueBinding.bind(this,b,c,d,e);
},removeBinding:function(f){qx.data.SingleValueBinding.removeBindingFromObject(this,f);
},removeAllBindings:function(){qx.data.SingleValueBinding.removeAllBindingsForObject(this);
},getBindings:function(){return qx.data.SingleValueBinding.getAllBindingsForObject(this);
}}});
})();
(function(){var m="get",l="",k="[",h="last",g="change",f="]",d=".",c="Number",b="String",a="qx.debug.databinding",F="set",E="deepBinding",D="item",C="reset",B="' (",A="Boolean",z=") to the object '",y="Integer",x=" of object ",w="qx.data.SingleValueBinding",u="Binding property ",v="Binding from '",s="PositiveNumber",t="PositiveInteger",q="Binding does not exist!",r=").",n="Date",p=" not possible: No event available. ";
qx.Class.define(w,{statics:{__bl:{},bind:function(G,H,I,J,K){var V=this.__bn(G,H,I,J,K);
var Q=H.split(d);
var M=this.__bt(Q);
var U=[];
var R=[];
var S=[];
var O=[];
var P=G;
try{for(var i=0;i<Q.length;i++){if(M[i]!==l){O.push(g);
}else{O.push(this.__bo(P,Q[i]));
}U[i]=P;
if(i==Q.length-1){if(M[i]!==l){var ba=M[i]===h?P.length-1:M[i];
var L=P.getItem(ba);
this.__bs(L,I,J,K,G);
S[i]=this.__bu(P,O[i],I,J,K,M[i]);
}else{if(Q[i]!=null&&P[m+qx.lang.String.firstUp(Q[i])]!=null){var L=P[m+qx.lang.String.firstUp(Q[i])]();
this.__bs(L,I,J,K,G);
}S[i]=this.__bu(P,O[i],I,J,K);
}}else{var W={index:i,propertyNames:Q,sources:U,listenerIds:S,arrayIndexValues:M,targetObject:I,targetPropertyChain:J,options:K,listeners:R};
var T=qx.lang.Function.bind(this.__bm,this,W);
R.push(T);
S[i]=P.addListener(O[i],T);
}if(P[m+qx.lang.String.firstUp(Q[i])]==null){P=null;
}else if(M[i]!==l){P=P[m+qx.lang.String.firstUp(Q[i])](M[i]);
}else{P=P[m+qx.lang.String.firstUp(Q[i])]();
}
if(!P){break;
}}}catch(bb){for(var i=0;i<U.length;i++){if(U[i]&&S[i]){U[i].removeListenerById(S[i]);
}}var Y=V.targets;
var N=V.listenerIds[i];
for(var i=0;i<Y.length;i++){if(Y[i]&&N[i]){Y[i].removeListenerById(N[i]);
}}throw bb;
}var X={type:E,listenerIds:S,sources:U,targetListenerIds:V.listenerIds,targets:V.targets};
this.__bv(X,G,H,I,J);
return X;
},__bm:function(bc){if(bc.options&&bc.options.onUpdate){bc.options.onUpdate(bc.sources[bc.index],bc.targetObject);
}for(var j=bc.index+1;j<bc.propertyNames.length;j++){var bg=bc.sources[j];
bc.sources[j]=null;

if(!bg){continue;
}bg.removeListenerById(bc.listenerIds[j]);
}var bg=bc.sources[bc.index];
for(var j=bc.index+1;j<bc.propertyNames.length;j++){if(bc.arrayIndexValues[j-1]!==l){bg=bg[m+qx.lang.String.firstUp(bc.propertyNames[j-1])](bc.arrayIndexValues[j-1]);
}else{bg=bg[m+qx.lang.String.firstUp(bc.propertyNames[j-1])]();
}bc.sources[j]=bg;
if(!bg){this.__bp(bc.targetObject,bc.targetPropertyChain);
break;
}if(j==bc.propertyNames.length-1){if(qx.Class.implementsInterface(bg,qx.data.IListData)){var bh=bc.arrayIndexValues[j]===h?bg.length-1:bc.arrayIndexValues[j];
var be=bg.getItem(bh);
this.__bs(be,bc.targetObject,bc.targetPropertyChain,bc.options,bc.sources[bc.index]);
bc.listenerIds[j]=this.__bu(bg,g,bc.targetObject,bc.targetPropertyChain,bc.options,bc.arrayIndexValues[j]);
}else{if(bc.propertyNames[j]!=null&&bg[m+qx.lang.String.firstUp(bc.propertyNames[j])]!=null){var be=bg[m+qx.lang.String.firstUp(bc.propertyNames[j])]();
this.__bs(be,bc.targetObject,bc.targetPropertyChain,bc.options,bc.sources[bc.index]);
}var bf=this.__bo(bg,bc.propertyNames[j]);
bc.listenerIds[j]=this.__bu(bg,bf,bc.targetObject,bc.targetPropertyChain,bc.options);
}}else{if(bc.listeners[j]==null){var bd=qx.lang.Function.bind(this.__bm,this,bc);
bc.listeners.push(bd);
}if(qx.Class.implementsInterface(bg,qx.data.IListData)){var bf=g;
}else{var bf=this.__bo(bg,bc.propertyNames[j]);
}bc.listenerIds[j]=bg.addListener(bf,bc.listeners[j]);
}}},__bn:function(bi,bj,bk,bl,bm){var bq=bl.split(d);
var bo=this.__bt(bq);
var bv=[];
var bu=[];
var bs=[];
var br=[];
var bp=bk;
for(var i=0;i<bq.length-1;i++){if(bo[i]!==l){br.push(g);
}else{try{br.push(this.__bo(bp,bq[i]));
}catch(e){break;
}}bv[i]=bp;
var bt=function(){for(var j=i+1;j<bq.length-1;j++){var by=bv[j];
bv[j]=null;

if(!by){continue;
}by.removeListenerById(bs[j]);
}var by=bv[i];
for(var j=i+1;j<bq.length-1;j++){var bw=qx.lang.String.firstUp(bq[j-1]);
if(bo[j-1]!==l){var bz=bo[j-1]===h?by.getLength()-1:bo[j-1];
by=by[m+bw](bz);
}else{by=by[m+bw]();
}bv[j]=by;
if(bu[j]==null){bu.push(bt);
}if(qx.Class.implementsInterface(by,qx.data.IListData)){var bx=g;
}else{try{var bx=qx.data.SingleValueBinding.__bo(by,bq[j]);
}catch(e){break;
}}bs[j]=by.addListener(bx,bu[j]);
}qx.data.SingleValueBinding.updateTarget(bi,bj,bk,bl,bm);
};
bu.push(bt);
bs[i]=bp.addListener(br[i],bt);
var bn=qx.lang.String.firstUp(bq[i]);
if(bp[m+bn]==null){bp=null;
}else if(bo[i]!==l){bp=bp[m+bn](bo[i]);
}else{bp=bp[m+bn]();
}
if(!bp){break;
}}return {listenerIds:bs,targets:bv};
},updateTarget:function(bA,bB,bC,bD,bE){var bF=this.getValueFromObject(bA,bB);
bF=qx.data.SingleValueBinding.__bw(bF,bC,bD,bE,bA);
this.__bq(bC,bD,bF);
},getValueFromObject:function(o,bG){var bK=this.__br(o,bG);
var bI;

if(bK!=null){var bM=bG.substring(bG.lastIndexOf(d)+1,bG.length);
if(bM.charAt(bM.length-1)==f){var bH=bM.substring(bM.lastIndexOf(k)+1,bM.length-1);
var bJ=bM.substring(0,bM.lastIndexOf(k));
var bL=bK[m+qx.lang.String.firstUp(bJ)]();

if(bH==h){bH=bL.length-1;
}
if(bL!=null){bI=bL.getItem(bH);
}}else{bI=bK[m+qx.lang.String.firstUp(bM)]();
}}return bI;
},__bo:function(bN,bO){var bP=this.__bx(bN,bO);
if(bP==null){if(qx.Class.supportsEvent(bN.constructor,bO)){bP=bO;
}else if(qx.Class.supportsEvent(bN.constructor,g+qx.lang.String.firstUp(bO))){bP=g+qx.lang.String.firstUp(bO);
}else{throw new qx.core.AssertionError(u+bO+x+bN+p);
}}return bP;
},__bp:function(bQ,bR){var bS=this.__br(bQ,bR);

if(bS!=null){var bT=bR.substring(bR.lastIndexOf(d)+1,bR.length);
if(bT.charAt(bT.length-1)==f){this.__bq(bQ,bR,null);
return;
}if(bS[C+qx.lang.String.firstUp(bT)]!=undefined){bS[C+qx.lang.String.firstUp(bT)]();
}else{bS[F+qx.lang.String.firstUp(bT)](null);
}}},__bq:function(bU,bV,bW){var cb=this.__br(bU,bV);

if(cb!=null){var cc=bV.substring(bV.lastIndexOf(d)+1,bV.length);
if(cc.charAt(cc.length-1)==f){var bX=cc.substring(cc.lastIndexOf(k)+1,cc.length-1);
var ca=cc.substring(0,cc.lastIndexOf(k));
var bY=bU;

if(!qx.Class.implementsInterface(bY,qx.data.IListData)){bY=cb[m+qx.lang.String.firstUp(ca)]();
}
if(bX==h){bX=bY.length-1;
}
if(bY!=null){bY.setItem(bX,bW);
}}else{cb[F+qx.lang.String.firstUp(cc)](bW);
}}},__br:function(cd,ce){var ch=ce.split(d);
var ci=cd;
for(var i=0;i<ch.length-1;i++){try{var cg=ch[i];
if(cg.indexOf(f)==cg.length-1){var cf=cg.substring(cg.indexOf(k)+1,cg.length-1);
cg=cg.substring(0,cg.indexOf(k));
}if(cg!=l){ci=ci[m+qx.lang.String.firstUp(cg)]();
}if(cf!=null){if(cf==h){cf=ci.length-1;
}ci=ci.getItem(cf);
cf=null;
}}catch(cj){return null;
}}return ci;
},__bs:function(ck,cl,cm,cn,co){ck=this.__bw(ck,cl,cm,cn,co);
if(ck===undefined){this.__bp(cl,cm);
}if(ck!==undefined){try{this.__bq(cl,cm,ck);
if(cn&&cn.onUpdate){cn.onUpdate(co,cl,ck);
}}catch(e){if(!(e instanceof qx.core.ValidationError)){throw e;
}
if(cn&&cn.onSetFail){cn.onSetFail(e);
}else{qx.log.Logger.warn("Failed so set value "+ck+" on "+cl+". Error message: "+e);
}}}},__bt:function(cp){var cq=[];
for(var i=0;i<cp.length;i++){var name=cp[i];
if(qx.lang.String.endsWith(name,f)){var cr=name.substring(name.indexOf(k)+1,name.indexOf(f));
if(name.indexOf(f)!=name.length-1){throw new Error("Please use only one array at a time: "+name+" does not work.");
}
if(cr!==h){if(cr==l||isNaN(parseInt(cr,10))){throw new Error("No number or 'last' value hast been given"+" in an array binding: "+name+" does not work.");
}}if(name.indexOf(k)!=0){cp[i]=name.substring(0,name.indexOf(k));
cq[i]=l;
cq[i+1]=cr;
cp.splice(i+1,0,D);
i++;
}else{cq[i]=cr;
cp.splice(i,1,D);
}}else{cq[i]=l;
}}return cq;
},__bu:function(cs,ct,cu,cv,cw,cx){var cy;
var cA=function(cB,e){if(cB!==l){if(cB===h){cB=cs.length-1;
}var cE=cs.getItem(cB);
if(cE===undefined){qx.data.SingleValueBinding.__bp(cu,cv);
}var cC=e.getData().start;
var cD=e.getData().end;

if(cB<cC||cB>cD){return;
}}else{var cE=e.getData();
}if(qx.core.Environment.get(a)){qx.log.Logger.debug("Binding executed from "+cs+" by "+ct+" to "+cu+" ("+cv+")");
qx.log.Logger.debug("Data before conversion: "+cE);
}cE=qx.data.SingleValueBinding.__bw(cE,cu,cv,cw,cs);
if(qx.core.Environment.get(a)){qx.log.Logger.debug("Data after conversion: "+cE);
}try{if(cE!==undefined){qx.data.SingleValueBinding.__bq(cu,cv,cE);
}else{qx.data.SingleValueBinding.__bp(cu,cv);
}if(cw&&cw.onUpdate){cw.onUpdate(cs,cu,cE);
}}catch(e){if(!(e instanceof qx.core.ValidationError)){throw e;
}
if(cw&&cw.onSetFail){cw.onSetFail(e);
}else{qx.log.Logger.warn("Failed so set value "+cE+" on "+cu+". Error message: "+e);
}}};
if(!cx){cx=l;
}cA=qx.lang.Function.bind(cA,cs,cx);
var cz=cs.addListener(ct,cA);
return cz;
},__bv:function(cF,cG,cH,cI,cJ){if(this.__bl[cG.toHashCode()]===undefined){this.__bl[cG.toHashCode()]=[];
}this.__bl[cG.toHashCode()].push([cF,cG,cH,cI,cJ]);
},__bw:function(cK,cL,cM,cN,cO){if(cN&&cN.converter){var cQ;

if(cL.getModel){cQ=cL.getModel();
}return cN.converter(cK,cQ,cO,cL);
}else{var cS=this.__br(cL,cM);
var cT=cM.substring(cM.lastIndexOf(d)+1,cM.length);
if(cS==null){return cK;
}var cR=qx.Class.getPropertyDefinition(cS.constructor,cT);
var cP=cR==null?l:cR.check;
return this.__by(cK,cP);
}},__bx:function(cU,cV){var cW=qx.Class.getPropertyDefinition(cU.constructor,cV);

if(cW==null){return null;
}return cW.event;
},__by:function(cX,cY){var da=qx.lang.Type.getClass(cX);
if((da==c||da==b)&&(cY==y||cY==t)){cX=parseInt(cX,10);
}if((da==A||da==c||da==n)&&cY==b){cX=cX+l;
}if((da==c||da==b)&&(cY==c||cY==s)){cX=parseFloat(cX);
}return cX;
},removeBindingFromObject:function(db,dc){if(dc.type==E){for(var i=0;i<dc.sources.length;i++){if(dc.sources[i]){dc.sources[i].removeListenerById(dc.listenerIds[i]);
}}for(var i=0;i<dc.targets.length;i++){if(dc.targets[i]){dc.targets[i].removeListenerById(dc.targetListenerIds[i]);
}}}else{db.removeListenerById(dc);
}var dd=this.__bl[db.toHashCode()];
if(dd!=undefined){for(var i=0;i<dd.length;i++){if(dd[i][0]==dc){qx.lang.Array.remove(dd,dd[i]);
return;
}}}throw new Error("Binding could not be found!");
},removeAllBindingsForObject:function(de){var df=this.__bl[de.toHashCode()];

if(df!=undefined){for(var i=df.length-1;i>=0;i--){this.removeBindingFromObject(de,df[i][0]);
}}},getAllBindingsForObject:function(dg){if(this.__bl[dg.toHashCode()]===undefined){this.__bl[dg.toHashCode()]=[];
}return this.__bl[dg.toHashCode()];
},removeAllBindings:function(){for(var di in this.__bl){var dh=qx.core.ObjectRegistry.fromHashCode(di);
if(dh==null){delete this.__bl[di];
continue;
}this.removeAllBindingsForObject(dh);
}this.__bl={};
},getAllBindings:function(){return this.__bl;
},showBindingInLog:function(dj,dk){var dm;
for(var i=0;i<this.__bl[dj.toHashCode()].length;i++){if(this.__bl[dj.toHashCode()][i][0]==dk){dm=this.__bl[dj.toHashCode()][i];
break;
}}
if(dm===undefined){var dl=q;
}else{var dl=v+dm[1]+B+dm[2]+z+dm[3]+B+dm[4]+r;
}qx.log.Logger.debug(dl);
},showAllBindingsInLog:function(){for(var dp in this.__bl){var dn=qx.core.ObjectRegistry.fromHashCode(dp);

for(var i=0;i<this.__bl[dp].length;i++){this.showBindingInLog(dn,this.__bl[dp][i][0]);
}}}}});
})();
(function(){var p="",o="g",n="]",m='\\u',l="undefined",k='\\$1',j="0041-005A0061-007A00AA00B500BA00C0-00D600D8-00F600F8-02C102C6-02D102E0-02E402EC02EE0370-037403760377037A-037D03860388-038A038C038E-03A103A3-03F503F7-0481048A-05250531-055605590561-058705D0-05EA05F0-05F20621-064A066E066F0671-06D306D506E506E606EE06EF06FA-06FC06FF07100712-072F074D-07A507B107CA-07EA07F407F507FA0800-0815081A082408280904-0939093D09500958-0961097109720979-097F0985-098C098F09900993-09A809AA-09B009B209B6-09B909BD09CE09DC09DD09DF-09E109F009F10A05-0A0A0A0F0A100A13-0A280A2A-0A300A320A330A350A360A380A390A59-0A5C0A5E0A72-0A740A85-0A8D0A8F-0A910A93-0AA80AAA-0AB00AB20AB30AB5-0AB90ABD0AD00AE00AE10B05-0B0C0B0F0B100B13-0B280B2A-0B300B320B330B35-0B390B3D0B5C0B5D0B5F-0B610B710B830B85-0B8A0B8E-0B900B92-0B950B990B9A0B9C0B9E0B9F0BA30BA40BA8-0BAA0BAE-0BB90BD00C05-0C0C0C0E-0C100C12-0C280C2A-0C330C35-0C390C3D0C580C590C600C610C85-0C8C0C8E-0C900C92-0CA80CAA-0CB30CB5-0CB90CBD0CDE0CE00CE10D05-0D0C0D0E-0D100D12-0D280D2A-0D390D3D0D600D610D7A-0D7F0D85-0D960D9A-0DB10DB3-0DBB0DBD0DC0-0DC60E01-0E300E320E330E40-0E460E810E820E840E870E880E8A0E8D0E94-0E970E99-0E9F0EA1-0EA30EA50EA70EAA0EAB0EAD-0EB00EB20EB30EBD0EC0-0EC40EC60EDC0EDD0F000F40-0F470F49-0F6C0F88-0F8B1000-102A103F1050-1055105A-105D106110651066106E-10701075-1081108E10A0-10C510D0-10FA10FC1100-1248124A-124D1250-12561258125A-125D1260-1288128A-128D1290-12B012B2-12B512B8-12BE12C012C2-12C512C8-12D612D8-13101312-13151318-135A1380-138F13A0-13F41401-166C166F-167F1681-169A16A0-16EA1700-170C170E-17111720-17311740-17511760-176C176E-17701780-17B317D717DC1820-18771880-18A818AA18B0-18F51900-191C1950-196D1970-19741980-19AB19C1-19C71A00-1A161A20-1A541AA71B05-1B331B45-1B4B1B83-1BA01BAE1BAF1C00-1C231C4D-1C4F1C5A-1C7D1CE9-1CEC1CEE-1CF11D00-1DBF1E00-1F151F18-1F1D1F20-1F451F48-1F4D1F50-1F571F591F5B1F5D1F5F-1F7D1F80-1FB41FB6-1FBC1FBE1FC2-1FC41FC6-1FCC1FD0-1FD31FD6-1FDB1FE0-1FEC1FF2-1FF41FF6-1FFC2071207F2090-209421022107210A-211321152119-211D212421262128212A-212D212F-2139213C-213F2145-2149214E218321842C00-2C2E2C30-2C5E2C60-2CE42CEB-2CEE2D00-2D252D30-2D652D6F2D80-2D962DA0-2DA62DA8-2DAE2DB0-2DB62DB8-2DBE2DC0-2DC62DC8-2DCE2DD0-2DD62DD8-2DDE2E2F300530063031-3035303B303C3041-3096309D-309F30A1-30FA30FC-30FF3105-312D3131-318E31A0-31B731F0-31FF3400-4DB54E00-9FCBA000-A48CA4D0-A4FDA500-A60CA610-A61FA62AA62BA640-A65FA662-A66EA67F-A697A6A0-A6E5A717-A71FA722-A788A78BA78CA7FB-A801A803-A805A807-A80AA80C-A822A840-A873A882-A8B3A8F2-A8F7A8FBA90A-A925A930-A946A960-A97CA984-A9B2A9CFAA00-AA28AA40-AA42AA44-AA4BAA60-AA76AA7AAA80-AAAFAAB1AAB5AAB6AAB9-AABDAAC0AAC2AADB-AADDABC0-ABE2AC00-D7A3D7B0-D7C6D7CB-D7FBF900-FA2DFA30-FA6DFA70-FAD9FB00-FB06FB13-FB17FB1DFB1F-FB28FB2A-FB36FB38-FB3CFB3EFB40FB41FB43FB44FB46-FBB1FBD3-FD3DFD50-FD8FFD92-FDC7FDF0-FDFBFE70-FE74FE76-FEFCFF21-FF3AFF41-FF5AFF66-FFBEFFC2-FFC7FFCA-FFCFFFD2-FFD7FFDA-FFDC",h='-',g="qx.lang.String",f="(^|[^",c="0",e="%",d=' ',b='\n',a="])[";
qx.Class.define(g,{statics:{__bz:j,__bA:null,__bB:{},camelCase:function(q){var r=this.__bB[q];

if(!r){r=q.replace(/\-([a-z])/g,function(s,t){return t.toUpperCase();
});
}return r;
},hyphenate:function(u){var v=this.__bB[u];

if(!v){v=u.replace(/[A-Z]/g,function(w){return (h+w.charAt(0).toLowerCase());
});
}return v;
},capitalize:function(x){if(this.__bA===null){var y=m;
this.__bA=new RegExp(f+this.__bz.replace(/[0-9A-F]{4}/g,function(z){return y+z;
})+a+this.__bz.replace(/[0-9A-F]{4}/g,function(A){return y+A;
})+n,o);
}return x.replace(this.__bA,function(B){return B.toUpperCase();
});
},clean:function(C){return this.trim(C.replace(/\s+/g,d));
},trimLeft:function(D){return D.replace(/^\s+/,p);
},trimRight:function(E){return E.replace(/\s+$/,p);
},trim:function(F){return F.replace(/^\s+|\s+$/g,p);
},startsWith:function(G,H){return G.indexOf(H)===0;
},endsWith:function(I,J){return I.substring(I.length-J.length,I.length)===J;
},repeat:function(K,L){return K.length>0?new Array(L+1).join(K):p;
},pad:function(M,length,N){var O=length-M.length;

if(O>0){if(typeof N===l){N=c;
}return this.repeat(N,O)+M;
}else{return M;
}},firstUp:qx.Bootstrap.firstUp,firstLow:qx.Bootstrap.firstLow,contains:function(P,Q){return P.indexOf(Q)!=-1;
},format:function(R,S){var T=R;
var i=S.length;

while(i--){T=T.replace(new RegExp(e+(i+1),o),S[i]+p);
}return T;
},escapeRegexpChars:function(U){return U.replace(/([.*+?^${}()|[\]\/\\])/g,k);
},toArray:function(V){return V.split(/\B|\b/g);
},stripTags:function(W){return W.replace(/<\/?[^>]+>/gi,p);
},stripScripts:function(X,Y){var bb=p;
var ba=X.replace(/<script[^>]*>([\s\S]*?)<\/script>/gi,function(){bb+=arguments[1]+b;
return p;
});

if(Y===true){qx.lang.Function.globalEval(bb);
}return ba;
}}});
})();
(function(){var g="mshtml",f="engine.name",e="[object Array]",d="qx.lang.Array",c="qx",b="number",a="string";
qx.Class.define(d,{statics:{toArray:function(h,j){return this.cast(h,Array,j);
},cast:function(k,m,n){if(k.constructor===m){return k;
}
if(qx.Class.hasInterface(k,qx.data.IListData)){var k=k.toArray();
}var o=new m;
if((qx.core.Environment.get(f)==g)){if(k.item){for(var i=n||0,l=k.length;i<l;i++){o.push(k[i]);
}return o;
}}if(Object.prototype.toString.call(k)===e&&n==null){o.push.apply(o,k);
}else{o.push.apply(o,Array.prototype.slice.call(k,n||0));
}return o;
},fromArguments:function(p,q){return Array.prototype.slice.call(p,q||0);
},fromCollection:function(r){if((qx.core.Environment.get(f)==g)){if(r.item){var s=[];

for(var i=0,l=r.length;i<l;i++){s[i]=r[i];
}return s;
}}return Array.prototype.slice.call(r,0);
},fromShortHand:function(t){var v=t.length;
var u=qx.lang.Array.clone(t);
switch(v){case 1:u[1]=u[2]=u[3]=u[0];
break;
case 2:u[2]=u[0];
case 3:u[3]=u[1];
}return u;
},clone:function(w){return w.concat();
},insertAt:function(x,y,i){x.splice(i,0,y);
return x;
},insertBefore:function(z,A,B){var i=z.indexOf(B);

if(i==-1){z.push(A);
}else{z.splice(i,0,A);
}return z;
},insertAfter:function(C,D,E){var i=C.indexOf(E);

if(i==-1||i==(C.length-1)){C.push(D);
}else{C.splice(i+1,0,D);
}return C;
},removeAt:function(F,i){return F.splice(i,1)[0];
},removeAll:function(G){G.length=0;
return this;
},append:function(H,I){Array.prototype.push.apply(H,I);
return H;
},exclude:function(J,K){for(var i=0,M=K.length,L;i<M;i++){L=J.indexOf(K[i]);

if(L!=-1){J.splice(L,1);
}}return J;
},remove:function(N,O){var i=N.indexOf(O);

if(i!=-1){N.splice(i,1);
return O;
}},contains:function(P,Q){return P.indexOf(Q)!==-1;
},equals:function(R,S){var length=R.length;

if(length!==S.length){return false;
}
for(var i=0;i<length;i++){if(R[i]!==S[i]){return false;
}}return true;
},sum:function(T){var U=0;

for(var i=0,l=T.length;i<l;i++){U+=T[i];
}return U;
},max:function(V){var i,X=V.length,W=V[0];

for(i=1;i<X;i++){if(V[i]>W){W=V[i];
}}return W===undefined?null:W;
},min:function(Y){var i,bb=Y.length,ba=Y[0];

for(i=1;i<bb;i++){if(Y[i]<ba){ba=Y[i];
}}return ba===undefined?null:ba;
},unique:function(bc){var bm=[],be={},bh={},bj={};
var bi,bd=0;
var bn=c+qx.lang.Date.now();
var bf=false,bl=false,bo=false;
for(var i=0,bk=bc.length;i<bk;i++){bi=bc[i];
if(bi===null){if(!bf){bf=true;
bm.push(bi);
}}else if(bi===undefined){}else if(bi===false){if(!bl){bl=true;
bm.push(bi);
}}else if(bi===true){if(!bo){bo=true;
bm.push(bi);
}}else if(typeof bi===a){if(!be[bi]){be[bi]=1;
bm.push(bi);
}}else if(typeof bi===b){if(!bh[bi]){bh[bi]=1;
bm.push(bi);
}}else{bg=bi[bn];

if(bg==null){bg=bi[bn]=bd++;
}
if(!bj[bg]){bj[bg]=bi;
bm.push(bi);
}}}for(var bg in bj){try{delete bj[bg][bn];
}catch(bp){try{bj[bg][bn]=null;
}catch(bq){throw new Error("Cannot clean-up map entry doneObjects["+bg+"]["+bn+"]");
}}}return bm;
}}});
})();
(function(){var a="qx.lang.Date";
qx.Class.define(a,{statics:{now:function(){return +new Date;
}}});
})();
(function(){var f="()",e=".",d=".prototype.",c='anonymous()',b="qx.lang.Function",a=".constructor()";
qx.Class.define(b,{statics:{getCaller:function(g){return g.caller?g.caller.callee:g.callee.caller;
},getName:function(h){if(h.displayName){return h.displayName;
}
if(h.$$original||h.wrapper||h.classname){return h.classname+a;
}
if(h.$$mixin){for(var j in h.$$mixin.$$members){if(h.$$mixin.$$members[j]==h){return h.$$mixin.name+d+j+f;
}}for(var j in h.$$mixin){if(h.$$mixin[j]==h){return h.$$mixin.name+e+j+f;
}}}
if(h.self){var k=h.self.constructor;

if(k){for(var j in k.prototype){if(k.prototype[j]==h){return k.classname+d+j+f;
}}for(var j in k){if(k[j]==h){return k.classname+e+j+f;
}}}}var i=h.toString().match(/function\s*(\w*)\s*\(.*/);

if(i&&i.length>=1&&i[1]){return i[1]+f;
}return c;
},globalEval:function(l){if(window.execScript){return window.execScript(l);
}else{return eval.call(window,l);
}},empty:function(){},returnTrue:function(){return true;
},returnFalse:function(){return false;
},returnNull:function(){return null;
},returnThis:function(){return this;
},returnZero:function(){return 0;
},create:function(m,n){if(!n){return m;
}if(!(n.self||n.args||n.delay!=null||n.periodical!=null||n.attempt)){return m;
}return function(event){var p=qx.lang.Array.fromArguments(arguments);
if(n.args){p=n.args.concat(p);
}
if(n.delay||n.periodical){var o=qx.event.GlobalError.observeMethod(function(){return m.apply(n.self||this,p);
});

if(n.delay){return window.setTimeout(o,n.delay);
}
if(n.periodical){return window.setInterval(o,n.periodical);
}}else if(n.attempt){var q=false;

try{q=m.apply(n.self||this,p);
}catch(r){}return q;
}else{return m.apply(n.self||this,p);
}};
},bind:function(s,self,t){return this.create(s,{self:self,args:arguments.length>2?qx.lang.Array.fromArguments(arguments,2):null});
},curry:function(u,v){return this.create(u,{args:arguments.length>1?qx.lang.Array.fromArguments(arguments,1):null});
},listener:function(w,self,x){if(arguments.length<3){return function(event){return w.call(self||this,event||window.event);
};
}else{var y=qx.lang.Array.fromArguments(arguments,2);
return function(event){var z=[event||window.event];
z.push.apply(z,y);
w.apply(self||this,z);
};
}},attempt:function(A,self,B){return this.create(A,{self:self,attempt:true,args:arguments.length>2?qx.lang.Array.fromArguments(arguments,2):null})();
},delay:function(C,D,self,E){return this.create(C,{delay:D,self:self,args:arguments.length>3?qx.lang.Array.fromArguments(arguments,3):null})();
},periodical:function(F,G,self,H){return this.create(F,{periodical:G,self:self,args:arguments.length>3?qx.lang.Array.fromArguments(arguments,3):null})();
}}});
})();
(function(){var b="qx.globalErrorHandling",a="qx.event.GlobalError";
qx.Bootstrap.define(a,{statics:{__bC:function(){if(qx.core&&qx.core.Environment){return qx.core.Environment.get(b);
}else{return !!qx.Bootstrap.getEnvironmentSetting(b);
}},setErrorHandler:function(c,d){this.__bD=c||null;
this.__bE=d||window;

if(this.__bC()){if(c&&window.onerror){var e=qx.Bootstrap.bind(this.__bG,this);

if(this.__bF==null){this.__bF=window.onerror;
}var self=this;
window.onerror=function(f,g,h){self.__bF(f,g,h);
e(f,g,h);
};
}
if(c&&!window.onerror){window.onerror=qx.Bootstrap.bind(this.__bG,this);
}if(this.__bD==null){if(this.__bF!=null){window.onerror=this.__bF;
this.__bF=null;
}else{window.onerror=null;
}}}},__bG:function(i,j,k){if(this.__bD){this.handleError(new qx.core.WindowError(i,j,k));
return true;
}},observeMethod:function(l){if(this.__bC()){var self=this;
return function(){if(!self.__bD){return l.apply(this,arguments);
}
try{return l.apply(this,arguments);
}catch(m){self.handleError(new qx.core.GlobalError(m,arguments));
}};
}else{return l;
}},handleError:function(n){if(this.__bD){this.__bD.call(this.__bE,n);
}}},defer:function(o){if(qx.core&&qx.core.Environment){qx.core.Environment.add(b,true);
}else{qx.Bootstrap.setEnvironmentSetting(b,true);
}o.setErrorHandler(null,null);
}});
})();
(function(){var b="",a="qx.core.WindowError";
qx.Bootstrap.define(a,{extend:Error,construct:function(c,d,e){Error.call(this,c);
this.__bH=c;
this.__bI=d||b;
this.__bJ=e===undefined?-1:e;
},members:{__bH:null,__bI:null,__bJ:null,toString:function(){return this.__bH;
},getUri:function(){return this.__bI;
},getLineNumber:function(){return this.__bJ;
}}});
})();
(function(){var b="GlobalError: ",a="qx.core.GlobalError";
qx.Bootstrap.define(a,{extend:Error,construct:function(c,d){if(qx.Bootstrap.DEBUG){qx.core.Assert.assertNotUndefined(c);
}this.__bH=b+(c&&c.message?c.message:c);
Error.call(this,this.__bH);
this.__bK=d;
this.__bL=c;
},members:{__bL:null,__bK:null,__bH:null,toString:function(){return this.__bH;
},getArguments:function(){return this.__bK;
},getSourceException:function(){return this.__bL;
}},destruct:function(){this.__bL=null;
this.__bK=null;
this.__bH=null;
}});
})();
(function(){var f="qx.lang.Type",e="Error",d="RegExp",c="Date",b="Number",a="Boolean";
qx.Class.define(f,{statics:{getClass:qx.Bootstrap.getClass,isString:qx.Bootstrap.isString,isArray:qx.Bootstrap.isArray,isObject:qx.Bootstrap.isObject,isFunction:qx.Bootstrap.isFunction,isRegExp:function(g){return this.getClass(g)==d;
},isNumber:function(h){return (h!==null&&(this.getClass(h)==b||h instanceof Number));
},isBoolean:function(i){return (i!==null&&(this.getClass(i)==a||i instanceof Boolean));
},isDate:function(j){return (j!==null&&(this.getClass(j)==c||j instanceof Date));
},isError:function(k){return (k!==null&&(this.getClass(k)==e||k instanceof Error));
}}});
})();
(function(){var p="",o="!",n="'!",m="'",k="Expected '",j="' (rgb(",h=",",g=")), but found value '",f="Event (",d="Expected value to be the CSS color '",bz="' but found ",by="]",bx=", ",bw="The value '",bv=" != ",bu="qx.core.Object",bt="Expected value to be an array but found ",bs=") was fired.",br="Expected value to be an integer >= 0 but found ",bq="' to be not equal with '",w="' to '",x="Expected object '",u="Called assertTrue with '",v="Expected value to be a map but found ",s="The function did not raise an exception!",t="Expected value to be undefined but found ",q="Expected value to be a DOM element but found  '",r="Expected value to be a regular expression but found ",E="' to implement the interface '",F="Expected value to be null but found ",S="Invalid argument 'type'",O="Called assert with 'false'",bb="Assertion error! ",V="null",bm="' but found '",bg="' must must be a key of the map '",J="The String '",bp="Expected value to be a string but found ",bo="Expected value not to be undefined but found undefined!",bn="qx.util.ColorUtil",I=": ",L="The raised exception does not have the expected type! ",N=") not fired.",Q="qx.core.Assert",T="Expected value to be typeof object but found ",W="' (identical) but found '",bd="' must have any of the values defined in the array '",bi="Expected value to be a number but found ",y="Called assertFalse with '",z="qx.ui.core.Widget",K="Expected value to be a qooxdoo object but found ",ba="' arguments.",Y="Expected value '%1' to be in the range '%2'..'%3'!",X="Array[",bf="' does not match the regular expression '",be="' to be not identical with '",U="Expected [",bc="' arguments but found '",a="', which cannot be converted to a CSS color!",bh="qx.core.AssertionError",A="Expected value to be a boolean but found ",B="Expected value not to be null but found null!",P="))!",b="Expected value to be a qooxdoo widget but found ",c="Expected value to be typeof '",H="Expected value to be typeof function but found ",C="Expected value to be an integer but found ",D="Called fail().",G="The parameter 're' must be a string or a regular expression.",R="Expected value to be a number >= 0 but found ",bk="Expected value to be instanceof '",bj="], but found [",M="Wrong number of arguments given. Expected '",bl="object";
qx.Class.define(Q,{statics:{__bM:true,__bN:function(bA,bB){var bF=p;

for(var i=1,l=arguments.length;i<l;i++){bF=bF+this.__bO(arguments[i]);
}var bE=p;

if(bF){bE=bA+I+bF;
}else{bE=bA;
}var bD=bb+bE;

if(this.__bM){qx.Bootstrap.error(bD);
}
if(qx.Class.isDefined(bh)){var bC=new qx.core.AssertionError(bA,bF);

if(this.__bM){qx.Bootstrap.error("Stack trace: \n"+bC.getStackTrace());
}throw bC;
}else{throw new Error(bD);
}},__bO:function(bG){var bH;

if(bG===null){bH=V;
}else if(qx.lang.Type.isArray(bG)&&bG.length>10){bH=X+bG.length+by;
}else if((bG instanceof Object)&&(bG.toString==null)){bH=qx.lang.Json.stringify(bG,null,2);
}else{try{bH=bG.toString();
}catch(e){bH=p;
}}return bH;
},assert:function(bI,bJ){bI==true||this.__bN(bJ||p,O);
},fail:function(bK,bL){var bM=bL?p:D;
this.__bN(bK||p,bM);
},assertTrue:function(bN,bO){(bN===true)||this.__bN(bO||p,u,bN,m);
},assertFalse:function(bP,bQ){(bP===false)||this.__bN(bQ||p,y,bP,m);
},assertEquals:function(bR,bS,bT){bR==bS||this.__bN(bT||p,k,bR,bm,bS,n);
},assertNotEquals:function(bU,bV,bW){bU!=bV||this.__bN(bW||p,k,bU,bq,bV,n);
},assertIdentical:function(bX,bY,ca){bX===bY||this.__bN(ca||p,k,bX,W,bY,n);
},assertNotIdentical:function(cb,cc,cd){cb!==cc||this.__bN(cd||p,k,cb,be,cc,n);
},assertNotUndefined:function(ce,cf){ce!==undefined||this.__bN(cf||p,bo);
},assertUndefined:function(cg,ch){cg===undefined||this.__bN(ch||p,t,cg,o);
},assertNotNull:function(ci,cj){ci!==null||this.__bN(cj||p,B);
},assertNull:function(ck,cl){ck===null||this.__bN(cl||p,F,ck,o);
},assertJsonEquals:function(cm,cn,co){this.assertEquals(qx.lang.Json.stringify(cm),qx.lang.Json.stringify(cn),co);
},assertMatch:function(cp,cq,cr){this.assertString(cp);
this.assert(qx.lang.Type.isRegExp(cq)||qx.lang.Type.isString(cq),G);
cp.search(cq)>=0||this.__bN(cr||p,J,cp,bf,cq.toString(),n);
},assertArgumentsCount:function(cs,ct,cu,cv){var cw=cs.length;
(cw>=ct&&cw<=cu)||this.__bN(cv||p,M,ct,w,cu,bc,arguments.length,ba);
},assertEventFired:function(cx,event,cy,cz,cA){var cC=false;
var cB=function(e){if(cz){cz.call(cx,e);
}cC=true;
};
var cD;

try{cD=cx.addListener(event,cB,cx);
cy.call();
}catch(cE){throw cE;
}finally{try{cx.removeListenerById(cD);
}catch(cF){}}cC===true||this.__bN(cA||p,f,event,N);
},assertEventNotFired:function(cG,event,cH,cI){var cK=false;
var cJ=function(e){cK=true;
};
var cL=cG.addListener(event,cJ,cG);
cH.call();
cK===false||this.__bN(cI||p,f,event,bs);
cG.removeListenerById(cL);
},assertException:function(cM,cN,cO,cP){var cN=cN||Error;
var cQ;

try{this.__bM=false;
cM();
}catch(cR){cQ=cR;
}finally{this.__bM=true;
}
if(cQ==null){this.__bN(cP||p,s);
}cQ instanceof cN||this.__bN(cP||p,L,cN,bv,cQ);

if(cO){this.assertMatch(cQ.toString(),cO,cP);
}},assertInArray:function(cS,cT,cU){cT.indexOf(cS)!==-1||this.__bN(cU||p,bw,cS,bd,cT,m);
},assertArrayEquals:function(cV,cW,cX){this.assertArray(cV,cX);
this.assertArray(cW,cX);
cX=cX||U+cV.join(bx)+bj+cW.join(bx)+by;

if(cV.length!==cW.length){this.fail(cX,true);
}
for(var i=0;i<cV.length;i++){if(cV[i]!==cW[i]){this.fail(cX,true);
}}},assertKeyInMap:function(cY,da,db){da[cY]!==undefined||this.__bN(db||p,bw,cY,bg,da,m);
},assertFunction:function(dc,dd){qx.lang.Type.isFunction(dc)||this.__bN(dd||p,H,dc,o);
},assertString:function(de,df){qx.lang.Type.isString(de)||this.__bN(df||p,bp,de,o);
},assertBoolean:function(dg,dh){qx.lang.Type.isBoolean(dg)||this.__bN(dh||p,A,dg,o);
},assertNumber:function(di,dj){(qx.lang.Type.isNumber(di)&&isFinite(di))||this.__bN(dj||p,bi,di,o);
},assertPositiveNumber:function(dk,dl){(qx.lang.Type.isNumber(dk)&&isFinite(dk)&&dk>=0)||this.__bN(dl||p,R,dk,o);
},assertInteger:function(dm,dn){(qx.lang.Type.isNumber(dm)&&isFinite(dm)&&dm%1===0)||this.__bN(dn||p,C,dm,o);
},assertPositiveInteger:function(dp,dq){var dr=(qx.lang.Type.isNumber(dp)&&isFinite(dp)&&dp%1===0&&dp>=0);
dr||this.__bN(dq||p,br,dp,o);
},assertInRange:function(ds,dt,du,dv){(ds>=dt&&ds<=du)||this.__bN(dv||p,qx.lang.String.format(Y,[ds,dt,du]));
},assertObject:function(dw,dx){var dy=dw!==null&&(qx.lang.Type.isObject(dw)||typeof dw===bl);
dy||this.__bN(dx||p,T,(dw),o);
},assertArray:function(dz,dA){qx.lang.Type.isArray(dz)||this.__bN(dA||p,bt,dz,o);
},assertMap:function(dB,dC){qx.lang.Type.isObject(dB)||this.__bN(dC||p,v,dB,o);
},assertRegExp:function(dD,dE){qx.lang.Type.isRegExp(dD)||this.__bN(dE||p,r,dD,o);
},assertType:function(dF,dG,dH){this.assertString(dG,S);
typeof (dF)===dG||this.__bN(dH||p,c,dG,bz,dF,o);
},assertInstance:function(dI,dJ,dK){var dL=dJ.classname||dJ+p;
dI instanceof dJ||this.__bN(dK||p,bk,dL,bz,dI,o);
},assertInterface:function(dM,dN,dO){qx.Class.implementsInterface(dM,dN)||this.__bN(dO||p,x,dM,E,dN,n);
},assertCssColor:function(dP,dQ,dR){var dS=qx.Class.getByName(bn);

if(!dS){throw new Error("qx.util.ColorUtil not available! Your code must have a dependency on 'qx.util.ColorUtil'");
}var dU=dS.stringToRgb(dP);

try{var dT=dS.stringToRgb(dQ);
}catch(dW){this.__bN(dR||p,d,dP,j,dU.join(h),g,dQ,a);
}var dV=dU[0]==dT[0]&&dU[1]==dT[1]&&dU[2]==dT[2];
dV||this.__bN(dR||p,d,dU,j,dU.join(h),g,dQ,j,dT.join(h),P);
},assertElement:function(dX,dY){!!(dX&&dX.nodeType===1)||this.__bN(dY||p,q,dX,n);
},assertQxObject:function(ea,eb){this.__bP(ea,bu)||this.__bN(eb||p,K,ea,o);
},assertQxWidget:function(ec,ed){this.__bP(ec,z)||this.__bN(ed||p,b,ec,o);
},__bP:function(ee,ef){if(!ee){return false;
}var eg=ee.constructor;

while(eg){if(eg.classname===ef){return true;
}eg=eg.superclass;
}return false;
}}});
})();
(function(){var c="",b=": ",a="qx.type.BaseError";
qx.Class.define(a,{extend:Error,construct:function(d,e){Error.call(this,e);
this.__bQ=d||c;
this.message=e||qx.type.BaseError.DEFAULTMESSAGE;
},statics:{DEFAULTMESSAGE:"error"},members:{__bQ:null,message:null,getComment:function(){return this.__bQ;
},toString:function(){return this.__bQ+(this.message?b+this.message:c);
}}});
})();
(function(){var a="qx.core.AssertionError";
qx.Class.define(a,{extend:qx.type.BaseError,construct:function(b,c){qx.type.BaseError.call(this,b,c);
this.__bR=qx.dev.StackTrace.getStackTrace();
},members:{__bR:null,getStackTrace:function(){return this.__bR;
}}});
})();
(function(){var m=":",l="engine.name",k="Error created at",j="...",h="qx.dev.StackTrace",g="",f="\n",e="?",d="/source/class/",c="anonymous",a="of linked script",b=".";
qx.Bootstrap.define(h,{statics:{getStackTrace:qx.core.Environment.select(l,{"gecko":function(){try{throw new Error();
}catch(A){var u=this.getStackTraceFromError(A);
qx.lang.Array.removeAt(u,0);
var s=this.getStackTraceFromCaller(arguments);
var q=s.length>u.length?s:u;

for(var i=0;i<Math.min(s.length,u.length);i++){var r=s[i];

if(r.indexOf(c)>=0){continue;
}var y=r.split(m);

if(y.length!=2){continue;
}var w=y[0];
var p=y[1];
var o=u[i];
var z=o.split(m);
var v=z[0];
var n=z[1];

if(qx.Class.getByName(v)){var t=v;
}else{t=w;
}var x=t+m;

if(p){x+=p+m;
}x+=n;
q[i]=x;
}return q;
}},"mshtml|webkit":function(){return this.getStackTraceFromCaller(arguments);
},"opera":function(){var B;

try{B.bar();
}catch(D){var C=this.getStackTraceFromError(D);
qx.lang.Array.removeAt(C,0);
return C;
}return [];
}}),getStackTraceFromCaller:qx.core.Environment.select(l,{"opera":function(E){return [];
},"default":function(F){var K=[];
var J=qx.lang.Function.getCaller(F);
var G={};

while(J){var H=qx.lang.Function.getName(J);
K.push(H);

try{J=J.caller;
}catch(L){break;
}
if(!J){break;
}var I=qx.core.ObjectRegistry.toHashCode(J);

if(G[I]){K.push(j);
break;
}G[I]=J;
}return K;
}}),getStackTraceFromError:qx.core.Environment.select(l,{"gecko":function(M){if(!M.stack){return [];
}var S=/@(.+):(\d+)$/gm;
var N;
var O=[];

while((N=S.exec(M.stack))!=null){var P=N[1];
var R=N[2];
var Q=this.__bS(P);
O.push(Q+m+R);
}return O;
},"webkit":function(T){if(T.stack){var bb=/at (.*)/gm;
var ba=/\((.*?)(:[^\/].*)\)/;
var X=/(.*?)(:[^\/].*)/;
var U;
var V=[];

while((U=bb.exec(T.stack))!=null){var W=ba.exec(U[1]);

if(!W){W=X.exec(U[1]);
}
if(W){var Y=this.__bS(W[1]);
V.push(Y+W[2]);
}else{V.push(U[1]);
}}return V;
}else if(T.sourceURL&&T.line){return [this.__bS(T.sourceURL)+m+T.line];
}else{return [];
}},"opera":function(bc){if(bc.stacktrace){var be=bc.stacktrace;

if(be.indexOf(k)>=0){be=be.split(k)[0];
}if(be.indexOf(a)>=0){var bo=/Line\ (\d+?)\ of\ linked\ script\ (.*?)$/gm;
var bf;
var bg=[];

while((bf=bo.exec(be))!=null){var bn=bf[1];
var bi=bf[2];
var bm=this.__bS(bi);
bg.push(bm+m+bn);
}}else{var bo=/line\ (\d+?),\ column\ (\d+?)\ in\ (?:.*?)\ in\ (.*?):[^\/]/gm;
var bf;
var bg=[];

while((bf=bo.exec(be))!=null){var bn=bf[1];
var bh=bf[2];
var bi=bf[3];
var bm=this.__bS(bi);
bg.push(bm+m+bn+m+bh);
}}return bg;
}else if(bc.message&&bc.message.indexOf("Backtrace:")>=0){var bg=[];
var bj=qx.lang.String.trim(bc.message.split("Backtrace:")[1]);
var bk=bj.split(f);

for(var i=0;i<bk.length;i++){var bd=bk[i].match(/\s*Line ([0-9]+) of.* (\S.*)/);

if(bd&&bd.length>=2){var bn=bd[1];
var bl=this.__bS(bd[2]);
bg.push(bl+m+bn);
}}return bg;
}else{return [];
}},"default":function(){return [];
}}),__bS:function(bp){var bt=d;
var bq=bp.indexOf(bt);
var bs=bp.indexOf(e);

if(bs>=0){bp=bp.substring(0,bs);
}var br=(bq==-1)?bp:bp.substring(bq+bt.length).replace(/\//g,b).replace(/\.js$/,g);
return br;
}}});
})();
(function(){var h="qx.debug.dispose",g="$$hash",f="-",e="",d="qx.core.ObjectRegistry",c="-0";
qx.Class.define(d,{statics:{inShutDown:false,__v:{},__bT:0,__bU:[],__bV:e,__bW:{},register:function(j){var n=this.__v;

if(!n){return;
}var m=j.$$hash;

if(m==null){var k=this.__bU;

if(k.length>0&&!qx.core.Environment.get(h)){m=k.pop();
}else{m=(this.__bT++)+this.__bV;
}j.$$hash=m;

if(qx.core.Environment.get(h)&&qx.dev&&qx.dev.Debug&&qx.dev.Debug.disposeProfilingActive){this.__bW[m]=qx.dev.StackTrace.getStackTrace();
}}n[m]=j;
},unregister:function(o){var p=o.$$hash;

if(p==null){return;
}var q=this.__v;

if(q&&q[p]){delete q[p];
this.__bU.push(p);
}try{delete o.$$hash;
}catch(r){if(o.removeAttribute){o.removeAttribute(g);
}}},toHashCode:function(s){var u=s.$$hash;

if(u!=null){return u;
}var t=this.__bU;

if(t.length>0){u=t.pop();
}else{u=(this.__bT++)+this.__bV;
}return s.$$hash=u;
},clearHashCode:function(v){var w=v.$$hash;

if(w!=null){this.__bU.push(w);
try{delete v.$$hash;
}catch(x){if(v.removeAttribute){v.removeAttribute(g);
}}}},fromHashCode:function(y){return this.__v[y]||null;
},shutdown:function(){this.inShutDown=true;
var A=this.__v;
var C=[];

for(var B in A){C.push(B);
}C.sort(function(a,b){return parseInt(b,10)-parseInt(a,10);
});
var z,i=0,l=C.length;

while(true){try{for(;i<l;i++){B=C[i];
z=A[B];

if(z&&z.dispose){z.dispose();
}}}catch(D){qx.Bootstrap.error(this,"Could not dispose object "+z.toString()+": "+D);

if(i!==l){i++;
continue;
}}break;
}qx.Bootstrap.debug(this,"Disposed "+l+" objects");
delete this.__v;
},getRegistry:function(){return this.__v;
},getNextHash:function(){return this.__bT;
},getPostId:function(){return this.__bV;
},getStackTraces:function(){return this.__bW;
}},defer:function(E){if(window&&window.top){var frames=window.top.frames;

for(var i=0;i<frames.length;i++){if(frames[i]===window){E.__bV=f+(i+1);
return;
}}}E.__bV=c;
}});
})();
(function(){var p='',o='"',m=':',l=']',h='null',g=': ',f='object',e='function',d=',',b='\n',ba='\\u',Y=',\n',X='0000',W='string',V="Cannot stringify a recursive object.",U='0',T='-',S='}',R='String',Q='Boolean',x='\\\\',y='\\f',u='\\t',w='{\n',s='[]',t="qx.lang.JsonImpl",q='Z',r='\\n',z='Object',A='{}',H='@',F='.',K='(',J='Array',M='T',L='\\r',C='{',P='JSON.parse',O=' ',N='[',B='Number',D=')',E='[\n',G='\\"',I='\\b';
qx.Class.define(t,{extend:Object,construct:function(){this.stringify=qx.lang.Function.bind(this.stringify,this);
this.parse=qx.lang.Function.bind(this.parse,this);
},members:{__bX:null,__bY:null,__ca:null,__cb:null,stringify:function(bb,bc,bd){this.__bX=p;
this.__bY=p;
this.__cb=[];

if(qx.lang.Type.isNumber(bd)){var bd=Math.min(10,Math.floor(bd));

for(var i=0;i<bd;i+=1){this.__bY+=O;
}}else if(qx.lang.Type.isString(bd)){if(bd.length>10){bd=bd.slice(0,10);
}this.__bY=bd;
}if(bc&&(qx.lang.Type.isFunction(bc)||qx.lang.Type.isArray(bc))){this.__ca=bc;
}else{this.__ca=null;
}return this.__cc(p,{'':bb});
},__cc:function(be,bf){var bi=this.__bX,bg,bj=bf[be];
if(bj&&qx.lang.Type.isFunction(bj.toJSON)){bj=bj.toJSON(be);
}else if(qx.lang.Type.isDate(bj)){bj=this.dateToJSON(bj);
}if(typeof this.__ca===e){bj=this.__ca.call(bf,be,bj);
}
if(bj===null){return h;
}
if(bj===undefined){return undefined;
}switch(qx.lang.Type.getClass(bj)){case R:return this.__cd(bj);
case B:return isFinite(bj)?String(bj):h;
case Q:return String(bj);
case J:this.__bX+=this.__bY;
bg=[];

if(this.__cb.indexOf(bj)!==-1){throw new TypeError(V);
}this.__cb.push(bj);
var length=bj.length;

for(var i=0;i<length;i+=1){bg[i]=this.__cc(i,bj)||h;
}this.__cb.pop();
if(bg.length===0){var bh=s;
}else if(this.__bX){bh=E+this.__bX+bg.join(Y+this.__bX)+b+bi+l;
}else{bh=N+bg.join(d)+l;
}this.__bX=bi;
return bh;
case z:this.__bX+=this.__bY;
bg=[];

if(this.__cb.indexOf(bj)!==-1){throw new TypeError(V);
}this.__cb.push(bj);
if(this.__ca&&typeof this.__ca===f){var length=this.__ca.length;

for(var i=0;i<length;i+=1){var k=this.__ca[i];

if(typeof k===W){var v=this.__cc(k,bj);

if(v){bg.push(this.__cd(k)+(this.__bX?g:m)+v);
}}}}else{for(var k in bj){if(Object.hasOwnProperty.call(bj,k)){var v=this.__cc(k,bj);

if(v){bg.push(this.__cd(k)+(this.__bX?g:m)+v);
}}}}this.__cb.pop();
if(bg.length===0){var bh=A;
}else if(this.__bX){bh=w+this.__bX+bg.join(Y+this.__bX)+b+bi+S;
}else{bh=C+bg.join(d)+S;
}this.__bX=bi;
return bh;
}},dateToJSON:function(bk){var bl=function(n){return n<10?U+n:n;
};
var bm=function(n){var bn=bl(n);
return n<100?U+bn:bn;
};
return isFinite(bk.valueOf())?bk.getUTCFullYear()+T+bl(bk.getUTCMonth()+1)+T+bl(bk.getUTCDate())+M+bl(bk.getUTCHours())+m+bl(bk.getUTCMinutes())+m+bl(bk.getUTCSeconds())+F+bm(bk.getUTCMilliseconds())+q:null;
},__cd:function(bo){var bp={'\b':I,'\t':u,'\n':r,'\f':y,'\r':L,'"':G,'\\':x};
var bq=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
bq.lastIndex=0;

if(bq.test(bo)){return o+bo.replace(bq,function(a){var c=bp[a];
return typeof c===W?c:ba+(X+a.charCodeAt(0).toString(16)).slice(-4);
})+o;
}else{return o+bo+o;
}},parse:function(br,bs){var bt=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
bt.lastIndex=0;
if(bt.test(br)){br=br.replace(bt,function(a){return ba+(X+a.charCodeAt(0).toString(16)).slice(-4);
});
}if(/^[\],:{}\s]*$/.test(br.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,H).replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,l).replace(/(?:^|:|,)(?:\s*\[)+/g,p))){var j=eval(K+br+D);
return typeof bs===e?this.__ce({'':j},p,bs):j;
}throw new SyntaxError(P);
},__ce:function(bu,bv,bw){var bx=bu[bv];

if(bx&&typeof bx===f){for(var k in bx){if(Object.hasOwnProperty.call(bx,k)){var v=this.__ce(bx,k,bw);

if(v!==undefined){bx[k]=v;
}else{delete bx[k];
}}}}return bw.call(bu,bv,bx);
}}});
})();
(function(){var d="qx.dom.Node",c="engine.name",b="";
qx.Class.define(d,{statics:{ELEMENT:1,ATTRIBUTE:2,TEXT:3,CDATA_SECTION:4,ENTITY_REFERENCE:5,ENTITY:6,PROCESSING_INSTRUCTION:7,COMMENT:8,DOCUMENT:9,DOCUMENT_TYPE:10,DOCUMENT_FRAGMENT:11,NOTATION:12,getDocument:function(e){return e.nodeType===this.DOCUMENT?e:e.ownerDocument||e.document;
},getWindow:qx.core.Environment.select(c,{"mshtml":function(f){if(f.nodeType==null){return f;
}if(f.nodeType!==this.DOCUMENT){f=f.ownerDocument;
}return f.parentWindow;
},"default":function(g){if(g.nodeType==null){return g;
}if(g.nodeType!==this.DOCUMENT){g=g.ownerDocument;
}return g.defaultView;
}}),getDocumentElement:function(h){return this.getDocument(h).documentElement;
},getBodyElement:function(j){return this.getDocument(j).body;
},isNode:function(k){return !!(k&&k.nodeType!=null);
},isElement:function(l){return !!(l&&l.nodeType===this.ELEMENT);
},isDocument:function(m){return !!(m&&m.nodeType===this.DOCUMENT);
},isText:function(n){return !!(n&&n.nodeType===this.TEXT);
},isWindow:function(o){return !!(o&&o.history&&o.location&&o.document);
},isNodeName:function(p,q){if(!q||!p||!p.nodeName){return false;
}return q.toLowerCase()==qx.dom.Node.getName(p);
},getName:function(r){if(!r||!r.nodeName){return null;
}return r.nodeName.toLowerCase();
},getText:function(s){if(!s||!s.nodeType){return null;
}
switch(s.nodeType){case 1:var i,a=[],t=s.childNodes,length=t.length;

for(i=0;i<length;i++){a[i]=this.getText(t[i]);
}return a.join(b);
case 2:case 3:case 4:return s.nodeValue;
}return null;
},isBlockNode:function(u){if(!qx.dom.Node.isElement(u)){return false;
}u=qx.dom.Node.getName(u);
return /^(body|form|textarea|fieldset|ul|ol|dl|dt|dd|li|div|hr|p|h[1-6]|quote|pre|table|thead|tbody|tfoot|tr|td|th|iframe|address|blockquote)$/.test(u);
}}});
})();
(function(){var l="on",k="engine.name",j="gecko",i="engine.version",h="function",g="undefined",f="mousedown",d="qx.bom.Event",c="return;",b="mouseover",a="HTMLEvents";
qx.Class.define(d,{statics:{addNativeListener:function(m,n,o,p){if(m.addEventListener){m.addEventListener(n,o,!!p);
}else if(m.attachEvent){m.attachEvent(l+n,o);
}else if(typeof m[l+n]!=g){m[l+n]=o;
}else{}},removeNativeListener:function(q,r,s,t){if(q.removeEventListener){q.removeEventListener(r,s,!!t);
}else if(q.detachEvent){try{q.detachEvent(l+r,s);
}catch(e){if(e.number!==-2146828218){throw e;
}}}else if(typeof q[l+r]!=g){q[l+r]=null;
}else{}},getTarget:function(e){return e.target||e.srcElement;
},getRelatedTarget:function(e){if(e.relatedTarget!==undefined){if((qx.core.Environment.get(k)==j)){try{e.relatedTarget&&e.relatedTarget.nodeType;
}catch(e){return null;
}}return e.relatedTarget;
}else if(e.fromElement!==undefined&&e.type===b){return e.fromElement;
}else if(e.toElement!==undefined){return e.toElement;
}else{return null;
}},preventDefault:function(e){if(e.preventDefault){if((qx.core.Environment.get(k)==j)&&parseFloat(qx.core.Environment.get(i))>=1.9&&e.type==f&&e.button==2){return;
}e.preventDefault();
if((qx.core.Environment.get(k)==j)&&parseFloat(qx.core.Environment.get(i))<1.9){try{e.keyCode=0;
}catch(u){}}}else{try{e.keyCode=0;
}catch(v){}e.returnValue=false;
}},stopPropagation:function(e){if(e.stopPropagation){e.stopPropagation();
}else{e.cancelBubble=true;
}},fire:function(w,x){if(document.createEvent){var y=document.createEvent(a);
y.initEvent(x,true,true);
return !w.dispatchEvent(y);
}else{var y=document.createEventObject();
return w.fireEvent(l+x,y);
}},supportsEvent:qx.core.Environment.select(k,{"webkit":function(z,A){return z.hasOwnProperty(l+A);
},"default":function(B,C){var D=l+C;
var E=(D in B);

if(!E){E=typeof B[D]==h;

if(!E&&B.setAttribute){B.setAttribute(D,c);
E=typeof B[D]==h;
B.removeAttribute(D);
}}return E;
}})}});
})();
(function(){var r="|bubble",q="|capture",p="|",o="",n="_",m="unload",k="UNKNOWN_",j="__ck",h="__cj",g="c",c="DOM_",f="WIN_",e="QX_",b="qx.event.Manager",a="capture",d="DOCUMENT_";
qx.Class.define(b,{extend:Object,construct:function(s,t){this.__cf=s;
this.__cg=qx.core.ObjectRegistry.toHashCode(s);
this.__ch=t;
if(s.qx!==qx){var self=this;
qx.bom.Event.addNativeListener(s,m,qx.event.GlobalError.observeMethod(function(){qx.bom.Event.removeNativeListener(s,m,arguments.callee);
self.dispose();
}));
}this.__ci={};
this.__cj={};
this.__ck={};
this.__cl={};
},statics:{__cm:0,getNextUniqueId:function(){return (this.__cm++)+o;
}},members:{__ch:null,__ci:null,__ck:null,__cn:null,__cj:null,__cl:null,__cf:null,__cg:null,getWindow:function(){return this.__cf;
},getWindowId:function(){return this.__cg;
},getHandler:function(u){var v=this.__cj[u.classname];

if(v){return v;
}return this.__cj[u.classname]=new u(this);
},getDispatcher:function(w){var x=this.__ck[w.classname];

if(x){return x;
}return this.__ck[w.classname]=new w(this,this.__ch);
},getListeners:function(y,z,A){var B=y.$$hash||qx.core.ObjectRegistry.toHashCode(y);
var D=this.__ci[B];

if(!D){return null;
}var E=z+(A?q:r);
var C=D[E];
return C?C.concat():null;
},getAllListeners:function(){return this.__ci;
},serializeListeners:function(F){var M=F.$$hash||qx.core.ObjectRegistry.toHashCode(F);
var O=this.__ci[M];
var K=[];

if(O){var I,N,G,J,L;

for(var H in O){I=H.indexOf(p);
N=H.substring(0,I);
G=H.charAt(I+1)==g;
J=O[H];

for(var i=0,l=J.length;i<l;i++){L=J[i];
K.push({self:L.context,handler:L.handler,type:N,capture:G});
}}}return K;
},toggleAttachedEvents:function(P,Q){var V=P.$$hash||qx.core.ObjectRegistry.toHashCode(P);
var X=this.__ci[V];

if(X){var S,W,R,T;

for(var U in X){S=U.indexOf(p);
W=U.substring(0,S);
R=U.charCodeAt(S+1)===99;
T=X[U];

if(Q){this.__co(P,W,R);
}else{this.__cp(P,W,R);
}}}},hasListener:function(Y,ba,bb){var bc=Y.$$hash||qx.core.ObjectRegistry.toHashCode(Y);
var be=this.__ci[bc];

if(!be){return false;
}var bf=ba+(bb?q:r);
var bd=be[bf];
return !!(bd&&bd.length>0);
},importListeners:function(bg,bh){var bn=bg.$$hash||qx.core.ObjectRegistry.toHashCode(bg);
var bo=this.__ci[bn]={};
var bk=qx.event.Manager;

for(var bi in bh){var bl=bh[bi];
var bm=bl.type+(bl.capture?q:r);
var bj=bo[bm];

if(!bj){bj=bo[bm]=[];
this.__co(bg,bl.type,bl.capture);
}bj.push({handler:bl.listener,context:bl.self,unique:bl.unique||(bk.__cm++)+o});
}},addListener:function(bp,bq,br,self,bs){var bw;
var bx=bp.$$hash||qx.core.ObjectRegistry.toHashCode(bp);
var bz=this.__ci[bx];

if(!bz){bz=this.__ci[bx]={};
}var bv=bq+(bs?q:r);
var bu=bz[bv];

if(!bu){bu=bz[bv]=[];
}if(bu.length===0){this.__co(bp,bq,bs);
}var by=(qx.event.Manager.__cm++)+o;
var bt={handler:br,context:self,unique:by};
bu.push(bt);
return bv+p+by;
},findHandler:function(bA,bB){var bN=false,bF=false,bO=false,bC=false;
var bL;

if(bA.nodeType===1){bN=true;
bL=c+bA.tagName.toLowerCase()+n+bB;
}else if(bA.nodeType===9){bC=true;
bL=d+bB;
}else if(bA==this.__cf){bF=true;
bL=f+bB;
}else if(bA.classname){bO=true;
bL=e+bA.classname+n+bB;
}else{bL=k+bA+n+bB;
}var bH=this.__cl;

if(bH[bL]){return bH[bL];
}var bK=this.__ch.getHandlers();
var bG=qx.event.IEventHandler;
var bI,bJ,bE,bD;

for(var i=0,l=bK.length;i<l;i++){bI=bK[i];
bE=bI.SUPPORTED_TYPES;

if(bE&&!bE[bB]){continue;
}bD=bI.TARGET_CHECK;

if(bD){var bM=false;

if(bN&&((bD&bG.TARGET_DOMNODE)!=0)){bM=true;
}else if(bF&&((bD&bG.TARGET_WINDOW)!=0)){bM=true;
}else if(bO&&((bD&bG.TARGET_OBJECT)!=0)){bM=true;
}else if(bC&&((bD&bG.TARGET_DOCUMENT)!=0)){bM=true;
}
if(!bM){continue;
}}bJ=this.getHandler(bK[i]);

if(bI.IGNORE_CAN_HANDLE||bJ.canHandleEvent(bA,bB)){bH[bL]=bJ;
return bJ;
}}return null;
},__co:function(bP,bQ,bR){var bS=this.findHandler(bP,bQ);

if(bS){bS.registerEvent(bP,bQ,bR);
return;
}},removeListener:function(bT,bU,bV,self,bW){var cb;
var cc=bT.$$hash||qx.core.ObjectRegistry.toHashCode(bT);
var cd=this.__ci[cc];

if(!cd){return false;
}var bX=bU+(bW?q:r);
var bY=cd[bX];

if(!bY){return false;
}var ca;

for(var i=0,l=bY.length;i<l;i++){ca=bY[i];

if(ca.handler===bV&&ca.context===self){qx.lang.Array.removeAt(bY,i);

if(bY.length==0){this.__cp(bT,bU,bW);
}return true;
}}return false;
},removeListenerById:function(ce,cf){var cl;
var cj=cf.split(p);
var co=cj[0];
var cg=cj[1].charCodeAt(0)==99;
var cn=cj[2];
var cm=ce.$$hash||qx.core.ObjectRegistry.toHashCode(ce);
var cp=this.__ci[cm];

if(!cp){return false;
}var ck=co+(cg?q:r);
var ci=cp[ck];

if(!ci){return false;
}var ch;

for(var i=0,l=ci.length;i<l;i++){ch=ci[i];

if(ch.unique===cn){qx.lang.Array.removeAt(ci,i);

if(ci.length==0){this.__cp(ce,co,cg);
}return true;
}}return false;
},removeAllListeners:function(cq){var cu=cq.$$hash||qx.core.ObjectRegistry.toHashCode(cq);
var cw=this.__ci[cu];

if(!cw){return false;
}var cs,cv,cr;

for(var ct in cw){if(cw[ct].length>0){cs=ct.split(p);
cv=cs[0];
cr=cs[1]===a;
this.__cp(cq,cv,cr);
}}delete this.__ci[cu];
return true;
},deleteAllListeners:function(cx){delete this.__ci[cx];
},__cp:function(cy,cz,cA){var cB=this.findHandler(cy,cz);

if(cB){cB.unregisterEvent(cy,cz,cA);
return;
}},dispatchEvent:function(cC,event){var cH;
var cI=event.getType();

if(!event.getBubbles()&&!this.hasListener(cC,cI)){qx.event.Pool.getInstance().poolObject(event);
return true;
}
if(!event.getTarget()){event.setTarget(cC);
}var cG=this.__ch.getDispatchers();
var cF;
var cE=false;

for(var i=0,l=cG.length;i<l;i++){cF=this.getDispatcher(cG[i]);
if(cF.canDispatchEvent(cC,event,cI)){cF.dispatchEvent(cC,event,cI);
cE=true;
break;
}}
if(!cE){return true;
}var cD=event.getDefaultPrevented();
qx.event.Pool.getInstance().poolObject(event);
return !cD;
},dispose:function(){this.__ch.removeManager(this);
qx.util.DisposeUtil.disposeMap(this,h);
qx.util.DisposeUtil.disposeMap(this,j);
this.__ci=this.__cf=this.__cn=null;
this.__ch=this.__cl=null;
}}});
})();
(function(){var a="qx.event.IEventHandler";
qx.Interface.define(a,{statics:{TARGET_DOMNODE:1,TARGET_WINDOW:2,TARGET_OBJECT:4,TARGET_DOCUMENT:8},members:{canHandleEvent:function(b,c){},registerEvent:function(d,e,f){},unregisterEvent:function(g,h,i){}}});
})();
(function(){var c="qx.event.Registration";
qx.Class.define(c,{statics:{__cq:{},getManager:function(d){if(d==null){d=window;
}else if(d.nodeType){d=qx.dom.Node.getWindow(d);
}else if(!qx.dom.Node.isWindow(d)){d=window;
}var f=d.$$hash||qx.core.ObjectRegistry.toHashCode(d);
var e=this.__cq[f];

if(!e){e=new qx.event.Manager(d,this);
this.__cq[f]=e;
}return e;
},removeManager:function(g){var h=g.getWindowId();
delete this.__cq[h];
},addListener:function(i,j,k,self,l){return this.getManager(i).addListener(i,j,k,self,l);
},removeListener:function(m,n,o,self,p){return this.getManager(m).removeListener(m,n,o,self,p);
},removeListenerById:function(q,r){return this.getManager(q).removeListenerById(q,r);
},removeAllListeners:function(s){return this.getManager(s).removeAllListeners(s);
},deleteAllListeners:function(t){var u=t.$$hash;

if(u){this.getManager(t).deleteAllListeners(u);
}},hasListener:function(v,w,x){return this.getManager(v).hasListener(v,w,x);
},serializeListeners:function(y){return this.getManager(y).serializeListeners(y);
},createEvent:function(z,A,B){if(A==null){A=qx.event.type.Event;
}var C=qx.event.Pool.getInstance().getObject(A);
B?C.init.apply(C,B):C.init();
if(z){C.setType(z);
}return C;
},dispatchEvent:function(D,event){return this.getManager(D).dispatchEvent(D,event);
},fireEvent:function(E,F,G,H){var I;
var J=this.createEvent(F,G||null,H);
return this.getManager(E).dispatchEvent(E,J);
},fireNonBubblingEvent:function(K,L,M,N){var O=this.getManager(K);

if(!O.hasListener(K,L,false)){return true;
}var P=this.createEvent(L,M||null,N);
return O.dispatchEvent(K,P);
},PRIORITY_FIRST:-32000,PRIORITY_NORMAL:0,PRIORITY_LAST:32000,__cj:[],addHandler:function(Q){this.__cj.push(Q);
this.__cj.sort(function(a,b){return a.PRIORITY-b.PRIORITY;
});
},getHandlers:function(){return this.__cj;
},__ck:[],addDispatcher:function(R,S){this.__ck.push(R);
this.__ck.sort(function(a,b){return a.PRIORITY-b.PRIORITY;
});
},getDispatchers:function(){return this.__ck;
}}});
})();
(function(){var a="qx.lang.RingBuffer";
qx.Class.define(a,{extend:Object,construct:function(b){this.setMaxEntries(b||50);
},members:{__cr:0,__cs:0,__ct:false,__cu:0,__cv:null,__cw:null,setMaxEntries:function(c){this.__cw=c;
this.clear();
},getMaxEntries:function(){return this.__cw;
},addEntry:function(d){this.__cv[this.__cr]=d;
this.__cr=this.__cx(this.__cr,1);
var e=this.getMaxEntries();

if(this.__cs<e){this.__cs++;
}if(this.__ct&&(this.__cu<e)){this.__cu++;
}},mark:function(){this.__ct=true;
this.__cu=0;
},clearMark:function(){this.__ct=false;
},getAllEntries:function(){return this.getEntries(this.getMaxEntries(),false);
},getEntries:function(f,g){if(f>this.__cs){f=this.__cs;
}if(g&&this.__ct&&(f>this.__cu)){f=this.__cu;
}
if(f>0){var i=this.__cx(this.__cr,-1);
var h=this.__cx(i,-f+1);
var j;

if(h<=i){j=this.__cv.slice(h,i+1);
}else{j=this.__cv.slice(h,this.__cs).concat(this.__cv.slice(0,i+1));
}}else{j=[];
}return j;
},clear:function(){this.__cv=new Array(this.getMaxEntries());
this.__cs=0;
this.__cu=0;
this.__cr=0;
},__cx:function(k,l){var m=this.getMaxEntries();
var n=(k+l)%m;
if(n<0){n+=m;
}return n;
}}});
})();
(function(){var a="qx.log.appender.RingBuffer";
qx.Class.define(a,{extend:qx.lang.RingBuffer,construct:function(b){this.setMaxMessages(b||50);
},members:{setMaxMessages:function(c){this.setMaxEntries(c);
},getMaxMessages:function(){return this.getMaxEntries();
},process:function(d){this.addEntry(d);
},getAllLogEvents:function(){return this.getAllEntries();
},retrieveLogEvents:function(e,f){return this.getEntries(e,f);
},clearHistory:function(){this.clear();
}}});
})();
(function(){var k="node",j="error",h="...(+",g="array",f=")",e="info",d="instance",c="string",b="null",a="class",H="number",G="stringify",F="]",E="date",D="unknown",C="function",B="boolean",A="debug",z="map",y="undefined",s="qx.log.Logger",t="[",q="#",r="warn",o="document",p="{...(",m="text[",n="[...(",u="\n",v=")}",x=")]",w="object";
qx.Class.define(s,{statics:{__cy:A,setLevel:function(I){this.__cy=I;
},getLevel:function(){return this.__cy;
},setTreshold:function(J){this.__cB.setMaxMessages(J);
},getTreshold:function(){return this.__cB.getMaxMessages();
},__cz:{},__cA:0,register:function(K){if(K.$$id){return;
}var M=this.__cA++;
this.__cz[M]=K;
K.$$id=M;
var L=this.__cC;
var N=this.__cB.getAllLogEvents();

for(var i=0,l=N.length;i<l;i++){if(L[N[i].level]>=L[this.__cy]){K.process(N[i]);
}}},unregister:function(O){var P=O.$$id;

if(P==null){return;
}delete this.__cz[P];
delete O.$$id;
},debug:function(Q,R){qx.log.Logger.__cD(A,arguments);
},info:function(S,T){qx.log.Logger.__cD(e,arguments);
},warn:function(U,V){qx.log.Logger.__cD(r,arguments);
},error:function(W,X){qx.log.Logger.__cD(j,arguments);
},trace:function(Y){qx.log.Logger.__cD(e,[Y,qx.dev.StackTrace.getStackTrace().join(u)]);
},deprecatedMethodWarning:function(ba,bb){var bc;
},deprecatedClassWarning:function(bd,be){var bf;
},deprecatedEventWarning:function(bg,event,bh){var bi;
},deprecatedMixinWarning:function(bj,bk){var bl;
},deprecatedConstantWarning:function(bm,bn,bo){var self,bp;
},deprecateMethodOverriding:function(bq,br,bs,bt){var bu;
},clear:function(){this.__cB.clearHistory();
},__cB:new qx.log.appender.RingBuffer(50),__cC:{debug:0,info:1,warn:2,error:3},__cD:function(bv,bw){var bB=this.__cC;

if(bB[bv]<bB[this.__cy]){return;
}var by=bw.length<2?null:bw[0];
var bA=by?1:0;
var bx=[];

for(var i=bA,l=bw.length;i<l;i++){bx.push(this.__cF(bw[i],true));
}var bC=new Date;
var bD={time:bC,offset:bC-qx.Bootstrap.LOADSTART,level:bv,items:bx,win:window};
if(by){if(by.$$hash!==undefined){bD.object=by.$$hash;
}else if(by.$$type){bD.clazz=by;
}}this.__cB.process(bD);
var bE=this.__cz;

for(var bz in bE){bE[bz].process(bD);
}},__cE:function(bF){if(bF===undefined){return y;
}else if(bF===null){return b;
}
if(bF.$$type){return a;
}var bG=typeof bF;

if(bG===C||bG==c||bG===H||bG===B){return bG;
}else if(bG===w){if(bF.nodeType){return k;
}else if(bF.classname){return d;
}else if(bF instanceof Array){return g;
}else if(bF instanceof Error){return j;
}else if(bF instanceof Date){return E;
}else{return z;
}}
if(bF.toString){return G;
}return D;
},__cF:function(bH,bI){var bP=this.__cE(bH);
var bL=D;
var bK=[];

switch(bP){case b:case y:bL=bP;
break;
case c:case H:case B:case E:bL=bH;
break;
case k:if(bH.nodeType===9){bL=o;
}else if(bH.nodeType===3){bL=m+bH.nodeValue+F;
}else if(bH.nodeType===1){bL=bH.nodeName.toLowerCase();

if(bH.id){bL+=q+bH.id;
}}else{bL=k;
}break;
case C:bL=qx.lang.Function.getName(bH)||bP;
break;
case d:bL=bH.basename+t+bH.$$hash+F;
break;
case a:case G:bL=bH.toString();
break;
case j:bK=qx.dev.StackTrace.getStackTraceFromError(bH);
bL=bH.toString();
break;
case g:if(bI){bL=[];

for(var i=0,l=bH.length;i<l;i++){if(bL.length>20){bL.push(h+(l-i)+f);
break;
}bL.push(this.__cF(bH[i],false));
}}else{bL=n+bH.length+x;
}break;
case z:if(bI){var bJ;
var bO=[];

for(var bN in bH){bO.push(bN);
}bO.sort();
bL=[];

for(var i=0,l=bO.length;i<l;i++){if(bL.length>20){bL.push(h+(l-i)+f);
break;
}bN=bO[i];
bJ=this.__cF(bH[bN],false);
bJ.key=bN;
bL.push(bJ);
}}else{var bM=0;

for(var bN in bH){bM++;
}bL=p+bM+v;
}break;
}return {type:bP,text:bL,trace:bK};
}},defer:function(bQ){var bR=qx.Bootstrap.$$logs;

for(var i=0;i<bR.length;i++){bQ.__cD(bR[i][0],bR[i][1]);
}qx.Bootstrap.debug=bQ.debug;
qx.Bootstrap.info=bQ.info;
qx.Bootstrap.warn=bQ.warn;
qx.Bootstrap.error=bQ.error;
qx.Bootstrap.trace=bQ.trace;
}});
})();
(function(){var q="set",p="get",o="reset",n="MSIE 6.0",m="info",k="qx.core.Object",j="error",h="warn",g="]",f="debug",b="[",d="$$user_",c="rv:1.8.1",a="Object";
qx.Class.define(k,{extend:Object,include:[qx.data.MBinding],construct:function(){qx.core.ObjectRegistry.register(this);
},statics:{$$type:a},members:{toHashCode:function(){return this.$$hash;
},toString:function(){return this.classname+b+this.$$hash+g;
},base:function(r,s){if(arguments.length===1){return r.callee.base.call(this);
}else{return r.callee.base.apply(this,Array.prototype.slice.call(arguments,1));
}},self:function(t){return t.callee.self;
},clone:function(){var v=this.constructor;
var u=new v;
var x=qx.Class.getProperties(v);
var w=qx.core.Property.$$store.user;
var y=qx.core.Property.$$method.set;
var name;
for(var i=0,l=x.length;i<l;i++){name=x[i];

if(this.hasOwnProperty(w[name])){u[y[name]](this[w[name]]);
}}return u;
},set:function(z,A){var C=qx.core.Property.$$method.set;

if(qx.Bootstrap.isString(z)){if(!this[C[z]]){if(this[q+qx.Bootstrap.firstUp(z)]!=undefined){this[q+qx.Bootstrap.firstUp(z)](A);
return this;
}}return this[C[z]](A);
}else{for(var B in z){if(!this[C[B]]){if(this[q+qx.Bootstrap.firstUp(B)]!=undefined){this[q+qx.Bootstrap.firstUp(B)](z[B]);
continue;
}}this[C[B]](z[B]);
}return this;
}},get:function(D){var E=qx.core.Property.$$method.get;

if(!this[E[D]]){if(this[p+qx.Bootstrap.firstUp(D)]!=undefined){return this[p+qx.Bootstrap.firstUp(D)]();
}}return this[E[D]]();
},reset:function(F){var G=qx.core.Property.$$method.reset;

if(!this[G[F]]){if(this[o+qx.Bootstrap.firstUp(F)]!=undefined){this[o+qx.Bootstrap.firstUp(F)]();
return;
}}this[G[F]]();
},__cG:qx.event.Registration,addListener:function(H,I,self,J){if(!this.$$disposed){return this.__cG.addListener(this,H,I,self,J);
}return null;
},addListenerOnce:function(K,L,self,M){var N=function(e){this.removeListener(K,N,this,M);
L.call(self||this,e);
};
return this.addListener(K,N,this,M);
},removeListener:function(O,P,self,Q){if(!this.$$disposed){return this.__cG.removeListener(this,O,P,self,Q);
}return false;
},removeListenerById:function(R){if(!this.$$disposed){return this.__cG.removeListenerById(this,R);
}return false;
},hasListener:function(S,T){return this.__cG.hasListener(this,S,T);
},dispatchEvent:function(U){if(!this.$$disposed){return this.__cG.dispatchEvent(this,U);
}return true;
},fireEvent:function(V,W,X){if(!this.$$disposed){return this.__cG.fireEvent(this,V,W,X);
}return true;
},fireNonBubblingEvent:function(Y,ba,bb){if(!this.$$disposed){return this.__cG.fireNonBubblingEvent(this,Y,ba,bb);
}return true;
},fireDataEvent:function(bc,bd,be,bf){if(!this.$$disposed){if(be===undefined){be=null;
}return this.__cG.fireNonBubblingEvent(this,bc,qx.event.type.Data,[bd,be,!!bf]);
}return true;
},__cH:null,setUserData:function(bg,bh){if(!this.__cH){this.__cH={};
}this.__cH[bg]=bh;
},getUserData:function(bi){if(!this.__cH){return null;
}var bj=this.__cH[bi];
return bj===undefined?null:bj;
},__cI:qx.log.Logger,debug:function(bk){this.__cJ(f,arguments);
},info:function(bl){this.__cJ(m,arguments);
},warn:function(bm){this.__cJ(h,arguments);
},error:function(bn){this.__cJ(j,arguments);
},trace:function(){this.__cI.trace(this);
},__cJ:function(bo,bp){var bq=qx.lang.Array.fromArguments(bp);
bq.unshift(this);
this.__cI[bo].apply(this.__cI,bq);
},isDisposed:function(){return this.$$disposed||false;
},dispose:function(){var bv,bt,bs,bw;
if(this.$$disposed){return;
}this.$$disposed=true;
this.$$instance=null;
this.$$allowconstruct=null;
var bu=this.constructor;
var br;

while(bu.superclass){if(bu.$$destructor){bu.$$destructor.call(this);
}if(bu.$$includes){br=bu.$$flatIncludes;

for(var i=0,l=br.length;i<l;i++){if(br[i].$$destructor){br[i].$$destructor.call(this);
}}}bu=bu.superclass;
}if(this.__cK){this.__cK();
}},__cK:null,__cL:function(){var bx=qx.Class.getProperties(this.constructor);

for(var i=0,l=bx.length;i<l;i++){delete this[d+bx[i]];
}},_disposeObjects:function(by){qx.util.DisposeUtil.disposeObjects(this,arguments);
},_disposeSingletonObjects:function(bz){qx.util.DisposeUtil.disposeObjects(this,arguments,true);
},_disposeArray:function(bA){qx.util.DisposeUtil.disposeArray(this,bA);
},_disposeMap:function(bB){qx.util.DisposeUtil.disposeMap(this,bB);
}},environment:{"qx.disposerDebugLevel":0},defer:function(bC,bD){var bF=navigator.userAgent.indexOf(n)!=-1;
var bE=navigator.userAgent.indexOf(c)!=-1;
if(bF||bE){bD.__cK=bD.__cL;
}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){qx.event.Registration.removeAllListeners(this);
}else{qx.event.Registration.deleteAllListeners(this);
}qx.core.ObjectRegistry.unregister(this);
this.__cH=null;
var bI=this.constructor;
var bM;
var bN=qx.core.Property.$$store;
var bK=bN.user;
var bL=bN.theme;
var bG=bN.inherit;
var bJ=bN.useinit;
var bH=bN.init;

while(bI){bM=bI.$$properties;

if(bM){for(var name in bM){if(bM[name].dereference){this[bK[name]]=this[bL[name]]=this[bG[name]]=this[bJ[name]]=this[bH[name]]=undefined;
}}}bI=bI.superclass;
}}});
})();
(function(){var a="qx.event.IEventDispatcher";
qx.Interface.define(a,{members:{canDispatchEvent:function(b,event,c){this.assertInstance(event,qx.event.type.Event);
this.assertString(c);
},dispatchEvent:function(d,event,e){this.assertInstance(event,qx.event.type.Event);
this.assertString(e);
}}});
})();
(function(){var a="qx.event.type.Event";
qx.Class.define(a,{extend:qx.core.Object,statics:{CAPTURING_PHASE:1,AT_TARGET:2,BUBBLING_PHASE:3},members:{init:function(b,c){this._type=null;
this._target=null;
this._currentTarget=null;
this._relatedTarget=null;
this._originalTarget=null;
this._stopPropagation=false;
this._preventDefault=false;
this._bubbles=!!b;
this._cancelable=!!c;
this._timeStamp=(new Date()).getTime();
this._eventPhase=null;
return this;
},clone:function(d){if(d){var e=d;
}else{var e=qx.event.Pool.getInstance().getObject(this.constructor);
}e._type=this._type;
e._target=this._target;
e._currentTarget=this._currentTarget;
e._relatedTarget=this._relatedTarget;
e._originalTarget=this._originalTarget;
e._stopPropagation=this._stopPropagation;
e._bubbles=this._bubbles;
e._preventDefault=this._preventDefault;
e._cancelable=this._cancelable;
return e;
},stop:function(){if(this._bubbles){this.stopPropagation();
}
if(this._cancelable){this.preventDefault();
}},stopPropagation:function(){this._stopPropagation=true;
},getPropagationStopped:function(){return !!this._stopPropagation;
},preventDefault:function(){this._preventDefault=true;
},getDefaultPrevented:function(){return !!this._preventDefault;
},getType:function(){return this._type;
},setType:function(f){this._type=f;
},getEventPhase:function(){return this._eventPhase;
},setEventPhase:function(g){this._eventPhase=g;
},getTimeStamp:function(){return this._timeStamp;
},getTarget:function(){return this._target;
},setTarget:function(h){this._target=h;
},getCurrentTarget:function(){return this._currentTarget||this._target;
},setCurrentTarget:function(i){this._currentTarget=i;
},getRelatedTarget:function(){return this._relatedTarget;
},setRelatedTarget:function(j){this._relatedTarget=j;
},getOriginalTarget:function(){return this._originalTarget;
},setOriginalTarget:function(k){this._originalTarget=k;
},getBubbles:function(){return this._bubbles;
},setBubbles:function(l){this._bubbles=l;
},isCancelable:function(){return this._cancelable;
},setCancelable:function(m){this._cancelable=m;
}},destruct:function(){this._target=this._currentTarget=this._relatedTarget=this._originalTarget=null;
}});
})();
(function(){var b="qx.util.ObjectPool",a="Integer";
qx.Class.define(b,{extend:qx.core.Object,construct:function(c){qx.core.Object.call(this);
this.__cM={};

if(c!=null){this.setSize(c);
}},properties:{size:{check:a,init:Infinity}},members:{__cM:null,getObject:function(d){if(this.$$disposed){return new d;
}
if(!d){throw new Error("Class needs to be defined!");
}var e=null;
var f=this.__cM[d.classname];

if(f){e=f.pop();
}
if(e){e.$$pooled=false;
}else{e=new d;
}return e;
},poolObject:function(g){if(!this.__cM){return;
}var h=g.classname;
var j=this.__cM[h];

if(g.$$pooled){throw new Error("Object is already pooled: "+g);
}
if(!j){this.__cM[h]=j=[];
}if(j.length>this.getSize()){if(g.destroy){g.destroy();
}else{g.dispose();
}return;
}g.$$pooled=true;
j.push(g);
}},destruct:function(){var n=this.__cM;
var k,m,i,l;

for(k in n){m=n[k];

for(i=0,l=m.length;i<l;i++){m[i].dispose();
}}delete this.__cM;
}});
})();
(function(){var b="singleton",a="qx.event.Pool";
qx.Class.define(a,{extend:qx.util.ObjectPool,type:b,construct:function(){qx.util.ObjectPool.call(this,30);
}});
})();
(function(){var a="qx.event.dispatch.Direct";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventDispatcher,construct:function(b){this._manager=b;
},statics:{PRIORITY:qx.event.Registration.PRIORITY_LAST},members:{canDispatchEvent:function(c,event,d){return !event.getBubbles();
},dispatchEvent:function(e,event,f){var j,g;
event.setEventPhase(qx.event.type.Event.AT_TARGET);
var k=this._manager.getListeners(e,f,false);

if(k){for(var i=0,l=k.length;i<l;i++){var h=k[i].context||e;
k[i].handler.call(h,event);
}}}},defer:function(m){qx.event.Registration.addDispatcher(m);
}});
})();
(function(){var a="qx.lang.Json";
qx.Class.define(a,{statics:{JSON:(qx.lang.Type.getClass(window.JSON)=="JSON"&&JSON.parse('{"x":1}').x===1&&JSON.stringify({"prop":"val"},function(k,v){return k==="prop"?"repl":v;
}).indexOf("repl")>0)?window.JSON:new qx.lang.JsonImpl(),stringify:null,parse:null},defer:function(b){b.stringify=b.JSON.stringify;
b.parse=b.JSON.parse;
}});
})();
(function(){var a="qx.event.handler.Object";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,statics:{PRIORITY:qx.event.Registration.PRIORITY_LAST,SUPPORTED_TYPES:null,TARGET_CHECK:qx.event.IEventHandler.TARGET_OBJECT,IGNORE_CAN_HANDLE:false},members:{canHandleEvent:function(b,c){return qx.Class.supportsEvent(b.constructor,c);
},registerEvent:function(d,e,f){},unregisterEvent:function(g,h,i){}},defer:function(j){qx.event.Registration.addHandler(j);
}});
})();
(function(){var a="qx.event.type.Data";
qx.Class.define(a,{extend:qx.event.type.Event,members:{__cN:null,__cO:null,init:function(b,c,d){qx.event.type.Event.prototype.init.call(this,false,d);
this.__cN=b;
this.__cO=c;
return this;
},clone:function(e){var f=qx.event.type.Event.prototype.clone.call(this,e);
f.__cN=this.__cN;
f.__cO=this.__cO;
return f;
},getData:function(){return this.__cN;
},getOldData:function(){return this.__cO;
}},destruct:function(){this.__cN=this.__cO=null;
}});
})();
(function(){var a="qx.util.DisposeUtil";
qx.Class.define(a,{statics:{disposeObjects:function(b,c,d){var name;

for(var i=0,l=c.length;i<l;i++){name=c[i];

if(b[name]==null||!b.hasOwnProperty(name)){continue;
}
if(!qx.core.ObjectRegistry.inShutDown){if(b[name].dispose){if(!d&&b[name].constructor.$$instance){throw new Error("The object stored in key "+name+" is a singleton! Please use disposeSingleton instead.");
}else{b[name].dispose();
}}else{throw new Error("Has no disposable object under key: "+name+"!");
}}b[name]=null;
}},disposeArray:function(e,f){var h=e[f];

if(!h){return;
}if(qx.core.ObjectRegistry.inShutDown){e[f]=null;
return;
}try{var g;

for(var i=h.length-1;i>=0;i--){g=h[i];

if(g){g.dispose();
}}}catch(j){throw new Error("The array field: "+f+" of object: "+e+" has non disposable entries: "+j);
}h.length=0;
e[f]=null;
},disposeMap:function(k,m){var o=k[m];

if(!o){return;
}if(qx.core.ObjectRegistry.inShutDown){k[m]=null;
return;
}try{var n;

for(var p in o){n=o[p];

if(o.hasOwnProperty(p)&&n){n.dispose();
}}}catch(q){throw new Error("The map field: "+m+" of object: "+k+" has non disposable entries: "+q);
}k[m]=null;
},disposeTriggeredBy:function(r,s){var t=s.dispose;
s.dispose=function(){t.call(s);
r.dispose();
};
}}});
})();
(function(){var a="qx.core.ValidationError";
qx.Class.define(a,{extend:qx.type.BaseError});
})();
(function(){var a="qx.application.IApplication";
qx.Interface.define(a,{members:{main:function(){},finalize:function(){},close:function(){},terminate:function(){}}});
})();
(function(){var a="qx.locale.MTranslation";
qx.Mixin.define(a,{members:{tr:function(b,c){var d=qx.locale.Manager;

if(d){return d.tr.apply(d,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
},trn:function(e,f,g,h){var i=qx.locale.Manager;

if(i){return i.trn.apply(i,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
},trc:function(j,k,l){var m=qx.locale.Manager;

if(m){return m.trc.apply(m,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
},marktr:function(n){var o=qx.locale.Manager;

if(o){return o.marktr.apply(o,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
}}});
})();
(function(){var g="",f="qx.core.BaseInit",d="engine.name",c="os.name",b="engine.version",a="scoville_admin.Application";
qx.Class.define(f,{statics:{getApplication:function(){return this.__cP||null;
},ready:function(){if(this.__cP){return;
}
if(qx.core.Environment.get(d)==g){qx.log.Logger.warn("Could not detect engine!");
}
if(qx.core.Environment.get(b)==g){qx.log.Logger.warn("Could not detect the version of the engine!");
}
if(qx.core.Environment.get(c)==g){qx.log.Logger.warn("Could not detect operating system!");
}qx.log.Logger.debug(this,"Load runtime: "+(new Date-qx.Bootstrap.LOADSTART)+"ms");
var i=a;
var j=qx.Class.getByName(i);

if(j){this.__cP=new j;
var h=new Date;
this.__cP.main();
qx.log.Logger.debug(this,"Main runtime: "+(new Date-h)+"ms");
var h=new Date;
this.__cP.finalize();
qx.log.Logger.debug(this,"Finalize runtime: "+(new Date-h)+"ms");
}else{qx.log.Logger.warn("Missing application class: "+i);
}},__cQ:function(e){var k=this.__cP;

if(k){k.close();
}},__cR:function(){var l=this.__cP;

if(l){l.terminate();
}qx.core.ObjectRegistry.shutdown();
}}});
})();
(function(){var a="qx.event.type.Native";
qx.Class.define(a,{extend:qx.event.type.Event,members:{init:function(b,c,d,e,f){qx.event.type.Event.prototype.init.call(this,e,f);
this._target=c||qx.bom.Event.getTarget(b);
this._relatedTarget=d||qx.bom.Event.getRelatedTarget(b);

if(b.timeStamp){this._timeStamp=b.timeStamp;
}this._native=b;
this._returnValue=null;
return this;
},clone:function(g){var h=qx.event.type.Event.prototype.clone.call(this,g);
var i={};
h._native=this._cloneNativeEvent(this._native,i);
h._returnValue=this._returnValue;
return h;
},_cloneNativeEvent:function(j,k){k.preventDefault=qx.lang.Function.empty;
return k;
},preventDefault:function(){qx.event.type.Event.prototype.preventDefault.call(this);
qx.bom.Event.preventDefault(this._native);
},getNativeEvent:function(){return this._native;
},setReturnValue:function(l){this._returnValue=l;
},getReturnValue:function(){return this._returnValue;
}},destruct:function(){this._native=this._returnValue=null;
}});
})();
(function(){var a="qx.event.handler.Window";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(b){qx.core.Object.call(this);
this._manager=b;
this._window=b.getWindow();
this._initWindowObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{error:1,load:1,beforeunload:1,unload:1,resize:1,scroll:1,beforeshutdown:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{canHandleEvent:function(c,d){},registerEvent:function(f,g,h){},unregisterEvent:function(i,j,k){},_initWindowObserver:function(){this._onNativeWrapper=qx.lang.Function.listener(this._onNative,this);
var m=qx.event.handler.Window.SUPPORTED_TYPES;

for(var l in m){qx.bom.Event.addNativeListener(this._window,l,this._onNativeWrapper);
}},_stopWindowObserver:function(){var o=qx.event.handler.Window.SUPPORTED_TYPES;

for(var n in o){qx.bom.Event.removeNativeListener(this._window,n,this._onNativeWrapper);
}},_onNative:qx.event.GlobalError.observeMethod(function(e){if(this.isDisposed()){return;
}var q=this._window;

try{var t=q.document;
}catch(e){return ;
}var r=t.documentElement;
var p=qx.bom.Event.getTarget(e);

if(p==null||p===q||p===t||p===r){var event=qx.event.Registration.createEvent(e.type,qx.event.type.Native,[e,q]);
qx.event.Registration.dispatchEvent(q,event);
var s=event.getReturnValue();

if(s!=null){e.returnValue=s;
return s;
}}})},destruct:function(){this._stopWindowObserver();
this._manager=this._window=null;
},defer:function(u){qx.event.Registration.addHandler(u);
}});
})();
(function(){var n="engine.name",m="ready",l="mshtml",k="load",j="unload",i="qx.event.handler.Application",h="complete",g="webkit",f="gecko",d="opera",a="left",c="DOMContentLoaded",b="shutdown";
qx.Class.define(i,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(o){qx.core.Object.call(this);
this._window=o.getWindow();
this.__cS=false;
this.__cT=false;
this.__cU=false;
this.__cV=false;
this._initObserver();
qx.event.handler.Application.$$instance=this;
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{ready:1,shutdown:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true,onScriptLoaded:function(){var p=qx.event.handler.Application.$$instance;

if(p){p.__cW();
}}},members:{canHandleEvent:function(q,r){},registerEvent:function(s,t,u){},unregisterEvent:function(v,w,x){},__cU:null,__cS:null,__cT:null,__cV:null,__cW:function(){if(!this.__cU&&this.__cS&&qx.$$loader.scriptLoaded){if((qx.core.Environment.get(n)==l)){if(qx.event.Registration.hasListener(this._window,m)){this.__cU=true;
qx.event.Registration.fireEvent(this._window,m);
}}else{this.__cU=true;
qx.event.Registration.fireEvent(this._window,m);
}}},isApplicationReady:function(){return this.__cU;
},_initObserver:function(){if(qx.$$domReady||document.readyState==h||document.readyState==m){this.__cS=true;
this.__cW();
}else{this._onNativeLoadWrapped=qx.lang.Function.bind(this._onNativeLoad,this);

if(qx.core.Environment.get(n)==f||qx.core.Environment.get(n)==d||qx.core.Environment.get(n)==g){qx.bom.Event.addNativeListener(this._window,c,this._onNativeLoadWrapped);
}else if((qx.core.Environment.get(n)==l)){var self=this;
var y=function(){try{document.documentElement.doScroll(a);

if(document.body){self._onNativeLoadWrapped();
}}catch(z){window.setTimeout(y,100);
}};
y();
}qx.bom.Event.addNativeListener(this._window,k,this._onNativeLoadWrapped);
}this._onNativeUnloadWrapped=qx.lang.Function.bind(this._onNativeUnload,this);
qx.bom.Event.addNativeListener(this._window,j,this._onNativeUnloadWrapped);
},_stopObserver:function(){if(this._onNativeLoadWrapped){qx.bom.Event.removeNativeListener(this._window,k,this._onNativeLoadWrapped);
}qx.bom.Event.removeNativeListener(this._window,j,this._onNativeUnloadWrapped);
this._onNativeLoadWrapped=null;
this._onNativeUnloadWrapped=null;
},_onNativeLoad:qx.event.GlobalError.observeMethod(function(){this.__cS=true;
this.__cW();
}),_onNativeUnload:qx.event.GlobalError.observeMethod(function(){if(!this.__cV){this.__cV=true;

try{qx.event.Registration.fireEvent(this._window,b);
}catch(e){throw e;
}finally{qx.core.ObjectRegistry.shutdown();
}}})},destruct:function(){this._stopObserver();
this._window=null;
},defer:function(A){qx.event.Registration.addHandler(A);
}});
})();
(function(){var d="ready",c="shutdown",b="beforeunload",a="qx.core.Init";
qx.Class.define(a,{statics:{getApplication:qx.core.BaseInit.getApplication,ready:qx.core.BaseInit.ready,__cQ:function(e){var f=this.__application;

if(f){e.setReturnValue(f.close());
}},__cR:function(){var g=this.__application;

if(g){g.terminate();
}}},defer:function(h){qx.event.Registration.addListener(window,d,h.ready,h);
qx.event.Registration.addListener(window,c,h.__cR,h);
qx.event.Registration.addListener(window,b,h.__cQ,h);
}});
})();
(function(){var b="abstract",a="qx.application.AbstractGui";
qx.Class.define(a,{type:b,extend:qx.core.Object,implement:[qx.application.IApplication],include:qx.locale.MTranslation,members:{__cX:null,_createRootWidget:function(){throw new Error("Abstract method call");
},getRoot:function(){return this.__cX;
},main:function(){qx.theme.manager.Meta.getInstance().initialize();
qx.ui.tooltip.Manager.getInstance();
this.__cX=this._createRootWidget();
},finalize:function(){this.render();
},render:function(){qx.ui.core.queue.Manager.flush();
},close:function(c){},terminate:function(){}},destruct:function(){this.__cX=null;
}});
})();
(function(){var f="_applyTheme",e="qx.theme",d="qx.theme.manager.Meta",c="qx.theme.Modern",b="Theme",a="singleton";
qx.Class.define(d,{type:a,extend:qx.core.Object,properties:{theme:{check:b,nullable:true,apply:f}},members:{_applyTheme:function(g,h){var k=null;
var n=null;
var q=null;
var r=null;
var m=null;

if(g){k=g.meta.color||null;
n=g.meta.decoration||null;
q=g.meta.font||null;
r=g.meta.icon||null;
m=g.meta.appearance||null;
}var o=qx.theme.manager.Color.getInstance();
var p=qx.theme.manager.Decoration.getInstance();
var i=qx.theme.manager.Font.getInstance();
var l=qx.theme.manager.Icon.getInstance();
var j=qx.theme.manager.Appearance.getInstance();
o.setTheme(k);
p.setTheme(n);
i.setTheme(q);
l.setTheme(r);
j.setTheme(m);
},initialize:function(){var u=qx.core.Environment;
var s,t;
s=u.get(e);

if(s){t=qx.Theme.getByName(s);

if(!t){throw new Error("The theme to use is not available: "+s);
}this.setTheme(t);
}}},environment:{"qx.theme":c}});
})();
(function(){var b="qx.util.ValueManager",a="abstract";
qx.Class.define(b,{type:a,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this._dynamic={};
},members:{_dynamic:null,resolveDynamic:function(c){return this._dynamic[c];
},isDynamic:function(d){return !!this._dynamic[d];
},resolve:function(e){if(e&&this._dynamic[e]){return this._dynamic[e];
}return e;
},_setDynamic:function(f){this._dynamic=f;
},_getDynamic:function(){return this._dynamic;
}},destruct:function(){this._dynamic=null;
}});
})();
(function(){var f="_applyTheme",e="qx.theme.manager.Color",d="Theme",c="changeTheme",b="string",a="singleton";
qx.Class.define(e,{type:a,extend:qx.util.ValueManager,properties:{theme:{check:d,nullable:true,apply:f,event:c}},members:{_applyTheme:function(g){var h={};

if(g){var i=g.colors;
var j=qx.util.ColorUtil;
var k;

for(var l in i){k=i[l];

if(typeof k===b){if(!j.isCssString(k)){throw new Error("Could not parse color: "+k);
}}else if(k instanceof Array){k=j.rgbToRgbString(k);
}else{throw new Error("Could not parse color: "+k);
}h[l]=k;
}}this._setDynamic(h);
},resolve:function(m){var p=this._dynamic;
var n=p[m];

if(n){return n;
}var o=this.getTheme();

if(o!==null&&o.colors[m]){return p[m]=o.colors[m];
}return m;
},isDynamic:function(q){var s=this._dynamic;

if(q&&(s[q]!==undefined)){return true;
}var r=this.getTheme();

if(r!==null&&q&&(r.colors[q]!==undefined)){s[q]=r.colors[q];
return true;
}return false;
}}});
})();
(function(){var h=",",e="rgb(",d=")",c="qx.theme.manager.Color",a="qx.util.ColorUtil";
qx.Class.define(a,{statics:{REGEXP:{hex3:/^#([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,hex6:/^#([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,rgb:/^rgb\(\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*\)$/,rgba:/^rgba\(\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*\)$/},SYSTEM:{activeborder:true,activecaption:true,appworkspace:true,background:true,buttonface:true,buttonhighlight:true,buttonshadow:true,buttontext:true,captiontext:true,graytext:true,highlight:true,highlighttext:true,inactiveborder:true,inactivecaption:true,inactivecaptiontext:true,infobackground:true,infotext:true,menu:true,menutext:true,scrollbar:true,threeddarkshadow:true,threedface:true,threedhighlight:true,threedlightshadow:true,threedshadow:true,window:true,windowframe:true,windowtext:true},NAMED:{black:[0,0,0],silver:[192,192,192],gray:[128,128,128],white:[255,255,255],maroon:[128,0,0],red:[255,0,0],purple:[128,0,128],fuchsia:[255,0,255],green:[0,128,0],lime:[0,255,0],olive:[128,128,0],yellow:[255,255,0],navy:[0,0,128],blue:[0,0,255],teal:[0,128,128],aqua:[0,255,255],transparent:[-1,-1,-1],magenta:[255,0,255],orange:[255,165,0],brown:[165,42,42]},isNamedColor:function(j){return this.NAMED[j]!==undefined;
},isSystemColor:function(k){return this.SYSTEM[k]!==undefined;
},supportsThemes:function(){return qx.Class.isDefined(c);
},isThemedColor:function(l){if(!this.supportsThemes()){return false;
}return qx.theme.manager.Color.getInstance().isDynamic(l);
},stringToRgb:function(m){if(this.supportsThemes()&&this.isThemedColor(m)){var m=qx.theme.manager.Color.getInstance().resolveDynamic(m);
}
if(this.isNamedColor(m)){return this.NAMED[m];
}else if(this.isSystemColor(m)){throw new Error("Could not convert system colors to RGB: "+m);
}else if(this.isRgbString(m)){return this.__cY();
}else if(this.isHex3String(m)){return this.__db();
}else if(this.isHex6String(m)){return this.__dc();
}throw new Error("Could not parse color: "+m);
},cssStringToRgb:function(n){if(this.isNamedColor(n)){return this.NAMED[n];
}else if(this.isSystemColor(n)){throw new Error("Could not convert system colors to RGB: "+n);
}else if(this.isRgbString(n)){return this.__cY();
}else if(this.isRgbaString(n)){return this.__da();
}else if(this.isHex3String(n)){return this.__db();
}else if(this.isHex6String(n)){return this.__dc();
}throw new Error("Could not parse color: "+n);
},stringToRgbString:function(o){return this.rgbToRgbString(this.stringToRgb(o));
},rgbToRgbString:function(s){return e+s[0]+h+s[1]+h+s[2]+d;
},rgbToHexString:function(u){return (qx.lang.String.pad(u[0].toString(16).toUpperCase(),2)+qx.lang.String.pad(u[1].toString(16).toUpperCase(),2)+qx.lang.String.pad(u[2].toString(16).toUpperCase(),2));
},isValidPropertyValue:function(v){return (this.isThemedColor(v)||this.isNamedColor(v)||this.isHex3String(v)||this.isHex6String(v)||this.isRgbString(v)||this.isRgbaString(v));
},isCssString:function(w){return (this.isSystemColor(w)||this.isNamedColor(w)||this.isHex3String(w)||this.isHex6String(w)||this.isRgbString(w)||this.isRgbaString(w));
},isHex3String:function(x){return this.REGEXP.hex3.test(x);
},isHex6String:function(y){return this.REGEXP.hex6.test(y);
},isRgbString:function(z){return this.REGEXP.rgb.test(z);
},isRgbaString:function(A){return this.REGEXP.rgba.test(A);
},__cY:function(){var D=parseInt(RegExp.$1,10);
var C=parseInt(RegExp.$2,10);
var B=parseInt(RegExp.$3,10);
return [D,C,B];
},__da:function(){var G=parseInt(RegExp.$1,10);
var F=parseInt(RegExp.$2,10);
var E=parseInt(RegExp.$3,10);
return [G,F,E];
},__db:function(){var J=parseInt(RegExp.$1,16)*17;
var I=parseInt(RegExp.$2,16)*17;
var H=parseInt(RegExp.$3,16)*17;
return [J,I,H];
},__dc:function(){var M=(parseInt(RegExp.$1,16)*16)+parseInt(RegExp.$2,16);
var L=(parseInt(RegExp.$3,16)*16)+parseInt(RegExp.$4,16);
var K=(parseInt(RegExp.$5,16)*16)+parseInt(RegExp.$6,16);
return [M,L,K];
},hex3StringToRgb:function(N){if(this.isHex3String(N)){return this.__db(N);
}throw new Error("Invalid hex3 value: "+N);
},hex6StringToRgb:function(O){if(this.isHex6String(O)){return this.__dc(O);
}throw new Error("Invalid hex6 value: "+O);
},hexStringToRgb:function(P){if(this.isHex3String(P)){return this.__db(P);
}
if(this.isHex6String(P)){return this.__dc(P);
}throw new Error("Invalid hex value: "+P);
},rgbToHsb:function(Q){var S,T,V;
var bc=Q[0];
var Y=Q[1];
var R=Q[2];
var bb=(bc>Y)?bc:Y;

if(R>bb){bb=R;
}var U=(bc<Y)?bc:Y;

if(R<U){U=R;
}V=bb/255.0;

if(bb!=0){T=(bb-U)/bb;
}else{T=0;
}
if(T==0){S=0;
}else{var X=(bb-bc)/(bb-U);
var ba=(bb-Y)/(bb-U);
var W=(bb-R)/(bb-U);

if(bc==bb){S=W-ba;
}else if(Y==bb){S=2.0+X-W;
}else{S=4.0+ba-X;
}S=S/6.0;

if(S<0){S=S+1.0;
}}return [Math.round(S*360),Math.round(T*100),Math.round(V*100)];
},hsbToRgb:function(bd){var i,f,p,q,t;
var be=bd[0]/360;
var bf=bd[1]/100;
var bg=bd[2]/100;

if(be>=1.0){be%=1.0;
}
if(bf>1.0){bf=1.0;
}
if(bg>1.0){bg=1.0;
}var bh=Math.floor(255*bg);
var bi={};

if(bf==0.0){bi.red=bi.green=bi.blue=bh;
}else{be*=6.0;
i=Math.floor(be);
f=be-i;
p=Math.floor(bh*(1.0-bf));
q=Math.floor(bh*(1.0-(bf*f)));
t=Math.floor(bh*(1.0-(bf*(1.0-f))));

switch(i){case 0:bi.red=bh;
bi.green=t;
bi.blue=p;
break;
case 1:bi.red=q;
bi.green=bh;
bi.blue=p;
break;
case 2:bi.red=p;
bi.green=bh;
bi.blue=t;
break;
case 3:bi.red=p;
bi.green=q;
bi.blue=bh;
break;
case 4:bi.red=t;
bi.green=p;
bi.blue=bh;
break;
case 5:bi.red=bh;
bi.green=p;
bi.blue=q;
break;
}}return [bi.red,bi.green,bi.blue];
},randomColor:function(){var r=Math.round(Math.random()*255);
var g=Math.round(Math.random()*255);
var b=Math.round(Math.random()*255);
return this.rgbToRgbString([r,g,b]);
}}});
})();
(function(){var m="object",l="__dd",k="_applyTheme",j="",h="_",g="qx.ui.decoration.",f="qx.theme.manager.Decoration",e=".",d="Theme",c="changeTheme",a="string",b="singleton";
qx.Class.define(f,{type:b,extend:qx.core.Object,properties:{theme:{check:d,nullable:true,apply:k,event:c}},members:{__dd:null,resolve:function(n){if(!n){return null;
}
if(typeof n===m){return n;
}var s=this.getTheme();

if(!s){return null;
}var p=this.__dd;

if(!p){p=this.__dd={};
}var o=p[n];

if(o){return o;
}var v=s.decorations[n];

if(!v){return null;
}if(!v.style){v.style={};
}var q=v;

while(q.include){q=s.decorations[q.include];
if(!v.decorator&&q.decorator){v.decorator=q.decorator;
}if(q.style){for(var u in q.style){if(v.style[u]==undefined){v.style[u]=q.style[u];
}}}}var r=v.decorator;

if(r==null){throw new Error("Missing definition of which decorator to use in entry: "+n+"!");
}if(r instanceof Array){var t=r.concat([]);

for(var i=0;i<t.length;i++){t[i]=t[i].basename.replace(e,j);
}var name=g+t.join(h);

if(!qx.Class.getByName(name)){qx.Class.define(name,{extend:qx.ui.decoration.DynamicDecorator,include:r});
}r=qx.Class.getByName(name);
}return p[n]=(new r).set(v.style);
},isValidPropertyValue:function(w){if(typeof w===a){return this.isDynamic(w);
}else if(typeof w===m){var x=w.constructor;
return qx.Class.hasInterface(x,qx.ui.decoration.IDecorator);
}return false;
},isDynamic:function(y){if(!y){return false;
}var z=this.getTheme();

if(!z){return false;
}return !!z.decorations[y];
},isCached:function(A){return qx.lang.Object.contains(this.__dd,A);
},_applyTheme:function(B,C){var E=qx.util.AliasManager.getInstance();

if(C){for(var D in C.aliases){E.remove(D);
}}
if(B){for(var D in B.aliases){E.add(D,B.aliases[D]);
}}
if(!B){this.__dd={};
}}},destruct:function(){this._disposeMap(l);
}});
})();
(function(){var a="qx.ui.decoration.IDecorator";
qx.Interface.define(a,{members:{getMarkup:function(){},resize:function(b,c,d){},tint:function(e,f){},getInsets:function(){}}});
})();
(function(){var i="Number",h="_applyInsets",g="abstract",f="insetRight",e="insetTop",d="insetBottom",c="qx.ui.decoration.Abstract",b="shorthand",a="insetLeft";
qx.Class.define(c,{extend:qx.core.Object,implement:[qx.ui.decoration.IDecorator],type:g,properties:{insetLeft:{check:i,nullable:true,apply:h},insetRight:{check:i,nullable:true,apply:h},insetBottom:{check:i,nullable:true,apply:h},insetTop:{check:i,nullable:true,apply:h},insets:{group:[e,f,d,a],mode:b}},members:{__de:null,_getDefaultInsets:function(){throw new Error("Abstract method called.");
},_isInitialized:function(){throw new Error("Abstract method called.");
},_resetInsets:function(){this.__de=null;
},getInsets:function(){if(this.__de){return this.__de;
}var j=this._getDefaultInsets();
return this.__de={left:this.getInsetLeft()==null?j.left:this.getInsetLeft(),right:this.getInsetRight()==null?j.right:this.getInsetRight(),bottom:this.getInsetBottom()==null?j.bottom:this.getInsetBottom(),top:this.getInsetTop()==null?j.top:this.getInsetTop()};
},_applyInsets:function(){this.__de=null;
}},destruct:function(){this.__de=null;
}});
})();
(function(){var o="px",n="top",m="_tint",l="abstract",k='<div style="',j="",h="_getDefaultInsetsFor",g="bottom",f="qx.ui.decoration.DynamicDecorator",e="left",b="right",d="_resize",c="_style",a='"></div>';
qx.Class.define(f,{extend:qx.ui.decoration.Abstract,type:l,members:{getMarkup:function(){if(this._markup){return this._markup;
}var p={};

for(var name in this){if(name.indexOf(c)==0&&this[name] instanceof Function){this[name](p);
}}if(!this._generateMarkup){var q=[k];
q.push(qx.bom.element.Style.compile(p));
q.push(a);
q=q.join(j);
}else{var q=this._generateMarkup(p);
}return this._markup=q;
},resize:function(r,s,t){var v={};

for(var name in this){if(name.indexOf(d)==0&&this[name] instanceof Function){var u=this[name](r,s,t);

if(v.left==undefined){v.left=u.left;
v.top=u.top;
}
if(v.width==undefined){v.width=u.width;
v.height=u.height;
}
if(u.elementToApplyDimensions){v.elementToApplyDimensions=u.elementToApplyDimensions;
}v.left=u.left<v.left?u.left:v.left;
v.top=u.top<v.top?u.top:v.top;
v.width=u.width>v.width?u.width:v.width;
v.height=u.height>v.height?u.height:v.height;
}}if(v.left!=undefined){r.style.left=v.left+o;
r.style.top=v.top+o;
}if(v.width!=undefined){if(v.width<0){v.width=0;
}
if(v.height<0){v.height=0;
}
if(v.elementToApplyDimensions){r=v.elementToApplyDimensions;
}r.style.width=v.width+o;
r.style.height=v.height+o;
}},tint:function(w,x){for(var name in this){if(name.indexOf(m)==0&&this[name] instanceof Function){this[name](w,x,w.style);
}}},_isInitialized:function(){return !!this._markup;
},_getDefaultInsets:function(){var B=[n,b,g,e];
var z={};

for(var name in this){if(name.indexOf(h)==0&&this[name] instanceof Function){var A=this[name]();

for(var i=0;i<B.length;i++){var y=B[i];
if(z[y]==undefined){z[y]=A[y];
}if(A[y]<z[y]){z[y]=A[y];
}}}}if(z[n]!=undefined){return z;
}return {top:0,right:0,bottom:0,left:0};
}}});
})();
(function(){var k="n-resize",j="e-resize",i="nw-resize",h="ne-resize",g="engine.name",f="",e="cursor:",d=";",c="qx.bom.element.Cursor",b="cursor",a="hand";
qx.Class.define(c,{statics:{__bi:qx.core.Environment.select(g,{"mshtml":{"cursor":a,"ew-resize":j,"ns-resize":k,"nesw-resize":h,"nwse-resize":i},"opera":{"col-resize":j,"row-resize":k,"ew-resize":j,"ns-resize":k,"nesw-resize":h,"nwse-resize":i},"default":{}}),compile:function(l){return e+(this.__bi[l]||l)+d;
},get:function(m,n){return qx.bom.element.Style.get(m,b,n,false);
},set:function(o,p){o.style.cursor=this.__bi[p]||p;
},reset:function(q){q.style.cursor=f;
}}});
})();
(function(){var k="engine.version",j="",i="engine.name",h="hidden",g="-moz-scrollbars-none",f="overflow",e=";",d="overflowY",b=":",a="overflowX",z="overflow:",y="none",x="scroll",w="borderLeftStyle",v="borderRightStyle",u="div",r="borderRightWidth",q="overflow-y",p="borderLeftWidth",o="-moz-scrollbars-vertical",m="100px",n="qx.bom.element.Overflow",l="overflow-x";
qx.Class.define(n,{statics:{__df:null,getScrollbarWidth:function(){if(this.__df!==null){return this.__df;
}var A=qx.bom.element.Style;
var C=function(G,H){return parseInt(A.get(G,H),10)||0;
};
var D=function(I){return (A.get(I,v)==y?0:C(I,r));
};
var B=function(J){return (A.get(J,w)==y?0:C(J,p));
};
var F=qx.core.Environment.select(i,{"mshtml":function(K){if(A.get(K,d)==h||K.clientWidth==0){return D(K);
}return Math.max(0,K.offsetWidth-K.clientLeft-K.clientWidth);
},"default":function(L){if(L.clientWidth==0){var M=A.get(L,f);
var N=(M==x||M==o?16:0);
return Math.max(0,D(L)+N);
}return Math.max(0,(L.offsetWidth-L.clientWidth-B(L)));
}});
var E=function(O){return F(O)-D(O);
};
var t=document.createElement(u);
var s=t.style;
s.height=s.width=m;
s.overflow=x;
document.body.appendChild(t);
var c=E(t);
this.__df=c?c:16;
document.body.removeChild(t);
return this.__df;
},_compile:qx.core.Environment.select(i,{"gecko":parseFloat(qx.core.Environment.get(k))<1.8?function(P,Q){if(Q==h){Q=g;
}return z+Q+e;
}:function(R,S){return R+b+S+e;
},"opera":parseFloat(qx.core.Environment.get(k))<9.5?function(T,U){return z+U+e;
}:function(V,W){return V+b+W+e;
},"default":function(X,Y){return X+b+Y+e;
}}),compileX:function(ba){return this._compile(l,ba);
},compileY:function(bb){return this._compile(q,bb);
},getX:qx.core.Environment.select(i,{"gecko":parseFloat(qx.core.Environment.get(k))<1.8?function(bc,bd){var be=qx.bom.element.Style.get(bc,f,bd,false);

if(be===g){be=h;
}return be;
}:function(bf,bg){return qx.bom.element.Style.get(bf,a,bg,false);
},"opera":parseFloat(qx.core.Environment.get(k))<9.5?function(bh,bi){return qx.bom.element.Style.get(bh,f,bi,false);
}:function(bj,bk){return qx.bom.element.Style.get(bj,a,bk,false);
},"default":function(bl,bm){return qx.bom.element.Style.get(bl,a,bm,false);
}}),setX:qx.core.Environment.select(i,{"gecko":parseFloat(qx.core.Environment.get(k))<1.8?function(bn,bo){if(bo==h){bo=g;
}bn.style.overflow=bo;
}:function(bp,bq){bp.style.overflowX=bq;
},"opera":parseFloat(qx.core.Environment.get(k))<9.5?function(br,bs){br.style.overflow=bs;
}:function(bt,bu){bt.style.overflowX=bu;
},"default":function(bv,bw){bv.style.overflowX=bw;
}}),resetX:qx.core.Environment.select(i,{"gecko":parseFloat(qx.core.Environment.get(k))<1.8?function(bx){bx.style.overflow=j;
}:function(by){by.style.overflowX=j;
},"opera":parseFloat(qx.core.Environment.get(k))<9.5?function(bz,bA){bz.style.overflow=j;
}:function(bB,bC){bB.style.overflowX=j;
},"default":function(bD){bD.style.overflowX=j;
}}),getY:qx.core.Environment.select(i,{"gecko":parseFloat(qx.core.Environment.get(k))<1.8?function(bE,bF){var bG=qx.bom.element.Style.get(bE,f,bF,false);

if(bG===g){bG=h;
}return bG;
}:function(bH,bI){return qx.bom.element.Style.get(bH,d,bI,false);
},"opera":parseFloat(qx.core.Environment.get(k))<9.5?function(bJ,bK){return qx.bom.element.Style.get(bJ,f,bK,false);
}:function(bL,bM){return qx.bom.element.Style.get(bL,d,bM,false);
},"default":function(bN,bO){return qx.bom.element.Style.get(bN,d,bO,false);
}}),setY:qx.core.Environment.select(i,{"gecko":parseFloat(qx.core.Environment.get(k))<1.8?function(bP,bQ){if(bQ===h){bQ=g;
}bP.style.overflow=bQ;
}:function(bR,bS){bR.style.overflowY=bS;
},"opera":parseFloat(qx.core.Environment.get(k))<9.5?function(bT,bU){bT.style.overflow=bU;
}:function(bV,bW){bV.style.overflowY=bW;
},"default":function(bX,bY){bX.style.overflowY=bY;
}}),resetY:qx.core.Environment.select(i,{"gecko":parseFloat(qx.core.Environment.get(k))<1.8?function(ca){ca.style.overflow=j;
}:function(cb){cb.style.overflowY=j;
},"opera":parseFloat(qx.core.Environment.get(k))<9.5?function(cc,cd){cc.style.overflow=j;
}:function(ce,cf){ce.style.overflowY=j;
},"default":function(cg){cg.style.overflowY=j;
}})}});
})();
(function(){var q="engine.name",p="",o="boxSizing",n="box-sizing",m="qx.bom.element.BoxSizing",k="KhtmlBoxSizing",j="border-box",h="-moz-box-sizing",g="WebkitBoxSizing",f=":",c=";",e="-khtml-box-sizing",d="content-box",b="-webkit-box-sizing",a="MozBoxSizing";
qx.Class.define(m,{statics:{__dg:qx.core.Environment.select(q,{"mshtml":null,"webkit":[o,k,g],"gecko":[a],"opera":[o]}),__dh:qx.core.Environment.select(q,{"mshtml":null,"webkit":[n,e,b],"gecko":[h],"opera":[n]}),__di:{tags:{button:true,select:true},types:{search:true,button:true,submit:true,reset:true,checkbox:true,radio:true}},__dj:function(r){var s=this.__di;
return s.tags[r.tagName.toLowerCase()]||s.types[r.type];
},compile:qx.core.Environment.select(q,{"mshtml":function(t){},"default":function(u){var w=this.__dh;
var v=p;

if(w){for(var i=0,l=w.length;i<l;i++){v+=w[i]+f+u+c;
}}return v;
}}),get:qx.core.Environment.select(q,{"mshtml":function(x){if(qx.bom.Document.isStandardMode(qx.dom.Node.getDocument(x))){if(!this.__dj(x)){return d;
}}return j;
},"default":function(y){var A=this.__dg;
var z;

if(A){for(var i=0,l=A.length;i<l;i++){z=qx.bom.element.Style.get(y,A[i],null,false);

if(z!=null&&z!==p){return z;
}}}return p;
}}),set:qx.core.Environment.select(q,{"mshtml":function(B,C){},"default":function(D,E){var F=this.__dg;

if(F){for(var i=0,l=F.length;i<l;i++){D.style[F[i]]=E;
}}}}),reset:function(G){this.set(G,p);
}}});
})();
(function(){var g="CSS1Compat",f="engine.name",e="position:absolute;width:0;height:0;width:1",d="engine.version",c="qx.bom.Document",b="1px",a="div";
qx.Class.define(c,{statics:{isQuirksMode:qx.core.Environment.select(f,{"mshtml":function(h){if(qx.core.Environment.get(d)>=8){return (h||window).document.documentMode===5;
}else{return (h||window).document.compatMode!==g;
}},"webkit":function(i){if(document.compatMode===undefined){var j=(i||window).document.createElement(a);
j.style.cssText=e;
return j.style.width===b?true:false;
}else{return (i||window).document.compatMode!==g;
}},"default":function(k){return (k||window).document.compatMode!==g;
}}),isStandardMode:function(l){return !this.isQuirksMode(l);
},getWidth:function(m){var n=(m||window).document;
var o=qx.bom.Viewport.getWidth(m);
var scroll=this.isStandardMode(m)?n.documentElement.scrollWidth:n.body.scrollWidth;
return Math.max(scroll,o);
},getHeight:function(p){var q=(p||window).document;
var r=qx.bom.Viewport.getHeight(p);
var scroll=this.isStandardMode(p)?q.documentElement.scrollHeight:q.body.scrollHeight;
return Math.max(scroll,r);
}}});
})();
(function(){var c="engine.version",b="engine.name",a="qx.bom.Viewport";
qx.Class.define(a,{statics:{getWidth:qx.core.Environment.select(b,{"opera":function(d){if(parseFloat(qx.core.Environment.get(c))<9.5){return (d||window).document.body.clientWidth;
}else{var e=(d||window).document;
return qx.bom.Document.isStandardMode(d)?e.documentElement.clientWidth:e.body.clientWidth;
}},"webkit":function(f){if(parseFloat(qx.core.Environment.get(c))<523.15){return (f||window).innerWidth;
}else{var g=(f||window).document;
return qx.bom.Document.isStandardMode(f)?g.documentElement.clientWidth:g.body.clientWidth;
}},"default":function(h){var i=(h||window).document;
return qx.bom.Document.isStandardMode(h)?i.documentElement.clientWidth:i.body.clientWidth;
}}),getHeight:qx.core.Environment.select(b,{"opera":function(j){if(parseFloat(qx.core.Environment.get(c))<9.5){return (j||window).document.body.clientHeight;
}else{var k=(j||window).document;
return qx.bom.Document.isStandardMode(j)?k.documentElement.clientHeight:k.body.clientHeight;
}},"webkit":function(l){if(parseFloat(qx.core.Environment.get(c))<523.15){return (l||window).innerHeight;
}else{var m=(l||window).document;
return qx.bom.Document.isStandardMode(l)?m.documentElement.clientHeight:m.body.clientHeight;
}},"default":function(n){var o=(n||window).document;
return qx.bom.Document.isStandardMode(n)?o.documentElement.clientHeight:o.body.clientHeight;
}}),getScrollLeft:qx.core.Environment.select(b,{"mshtml":function(p){var q=(p||window).document;
return q.documentElement.scrollLeft||q.body.scrollLeft;
},"default":function(r){return (r||window).pageXOffset;
}}),getScrollTop:qx.core.Environment.select(b,{"mshtml":function(s){var t=(s||window).document;
return t.documentElement.scrollTop||t.body.scrollTop;
},"default":function(u){return (u||window).pageYOffset;
}}),__dk:function(){var v=this.getWidth()>this.getHeight()?90:0;
var w=window.orientation;

if(w==null||Math.abs(w%180)==v){return {"-270":90,"-180":180,"-90":-90,"0":0,"90":90,"180":180,"270":-90};
}else{return {"-270":180,"-180":-90,"-90":0,"0":90,"90":180,"180":-90,"270":0};
}},__dl:null,getOrientation:function(x){var y=(x||window).orientation;

if(y==null){y=this.getWidth(x)>this.getHeight(x)?90:0;
}else{y=this.__dl[y];
}return y;
},isLandscape:function(z){return Math.abs(this.getOrientation(z))==90;
},isPortrait:function(A){return Math.abs(this.getOrientation(A))!==90;
}},defer:function(B){B.__dl=B.__dk();
}});
})();
(function(){var o="auto",n="px",m=",",l="clip:auto;",k="rect(",j=");",i="",h=")",g="qx.bom.element.Clip",f="string",c="clip:rect(",e=" ",d="clip",b="rect(auto,auto,auto,auto)",a="rect(auto, auto, auto, auto)";
qx.Class.define(g,{statics:{compile:function(p){if(!p){return l;
}var u=p.left;
var top=p.top;
var t=p.width;
var s=p.height;
var q,r;

if(u==null){q=(t==null?o:t+n);
u=o;
}else{q=(t==null?o:u+t+n);
u=u+n;
}
if(top==null){r=(s==null?o:s+n);
top=o;
}else{r=(s==null?o:top+s+n);
top=top+n;
}return c+top+m+q+m+r+m+u+j;
},get:function(v,w){var y=qx.bom.element.Style.get(v,d,w,false);
var E,top,C,B;
var x,z;

if(typeof y===f&&y!==o&&y!==i){y=qx.lang.String.trim(y);
if(/\((.*)\)/.test(y)){var D=RegExp.$1;
if(/,/.test(D)){var A=D.split(m);
}else{var A=D.split(e);
}top=qx.lang.String.trim(A[0]);
x=qx.lang.String.trim(A[1]);
z=qx.lang.String.trim(A[2]);
E=qx.lang.String.trim(A[3]);
if(E===o){E=null;
}
if(top===o){top=null;
}
if(x===o){x=null;
}
if(z===o){z=null;
}if(top!=null){top=parseInt(top,10);
}
if(x!=null){x=parseInt(x,10);
}
if(z!=null){z=parseInt(z,10);
}
if(E!=null){E=parseInt(E,10);
}if(x!=null&&E!=null){C=x-E;
}else if(x!=null){C=x;
}
if(z!=null&&top!=null){B=z-top;
}else if(z!=null){B=z;
}}else{throw new Error("Could not parse clip string: "+y);
}}return {left:E||null,top:top||null,width:C||null,height:B||null};
},set:function(F,G){if(!G){F.style.clip=b;
return;
}var L=G.left;
var top=G.top;
var K=G.width;
var J=G.height;
var H,I;

if(L==null){H=(K==null?o:K+n);
L=o;
}else{H=(K==null?o:L+K+n);
L=L+n;
}
if(top==null){I=(J==null?o:J+n);
top=o;
}else{I=(J==null?o:top+J+n);
top=top+n;
}F.style.clip=k+top+m+H+m+I+m+L+h;
},reset:function(M){M.style.clip=a;
}}});
})();
(function(){var m="",l="engine.name",k=";",j="opacity:",i="opacity",h="filter",g="MozOpacity",f=");",e=")",d="zoom:1;filter:alpha(opacity=",a="qx.bom.element.Opacity",c="alpha(opacity=",b="-moz-opacity:";
qx.Class.define(a,{statics:{SUPPORT_CSS3_OPACITY:false,compile:qx.core.Environment.select(l,{"mshtml":function(n){if(n>=1){n=1;
}
if(n<0.00001){n=0;
}
if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){return j+n+k;
}else{return d+(n*100)+f;
}},"gecko":function(o){if(o>=1){o=0.999999;
}
if(!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){return b+o+k;
}else{return j+o+k;
}},"default":function(p){if(p>=1){return m;
}return j+p+k;
}}),set:qx.core.Environment.select(l,{"mshtml":function(q,r){if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){if(r>=1){r=m;
}q.style.opacity=r;
}else{var s=qx.bom.element.Style.get(q,h,qx.bom.element.Style.COMPUTED_MODE,false);

if(r>=1){r=1;
}
if(r<0.00001){r=0;
}if(!q.currentStyle||!q.currentStyle.hasLayout){q.style.zoom=1;
}q.style.filter=s.replace(/alpha\([^\)]*\)/gi,m)+c+r*100+e;
}},"gecko":function(t,u){if(u>=1){u=0.999999;
}
if(!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){t.style.MozOpacity=u;
}else{t.style.opacity=u;
}},"default":function(v,w){if(w>=1){w=m;
}v.style.opacity=w;
}}),reset:qx.core.Environment.select(l,{"mshtml":function(x){if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){x.style.opacity=m;
}else{var y=qx.bom.element.Style.get(x,h,qx.bom.element.Style.COMPUTED_MODE,false);
x.style.filter=y.replace(/alpha\([^\)]*\)/gi,m);
}},"gecko":function(z){if(!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){z.style.MozOpacity=m;
}else{z.style.opacity=m;
}},"default":function(A){A.style.opacity=m;
}}),get:qx.core.Environment.select(l,{"mshtml":function(B,C){if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){var D=qx.bom.element.Style.get(B,i,C,false);

if(D!=null){return parseFloat(D);
}return 1.0;
}else{var E=qx.bom.element.Style.get(B,h,C,false);

if(E){var D=E.match(/alpha\(opacity=(.*)\)/);

if(D&&D[1]){return parseFloat(D[1])/100;
}}return 1.0;
}},"gecko":function(F,G){var H=qx.bom.element.Style.get(F,!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY?g:i,G,false);

if(H==0.999999){H=1.0;
}
if(H!=null){return parseFloat(H);
}return 1.0;
},"default":function(I,J){var K=qx.bom.element.Style.get(I,i,J,false);

if(K!=null){return parseFloat(K);
}return 1.0;
}})},defer:function(L){L.SUPPORT_CSS3_OPACITY=(typeof document.documentElement.style.opacity=="string");
}});
})();
(function(){var m="",k="engine.name",h="userSelect",g="style",f="MozUserModify",e="px",d="pixelBottom",c="float",b="borderImage",a="styleFloat",F="appearance",E="pixelHeight",D='Ms',C=":",B="cssFloat",A="pixelTop",z="pixelLeft",y='O',x="qx.bom.element.Style",w='Khtml',t='string',u="pixelRight",r='Moz',s="pixelWidth",p=";",q="textOverflow",n="userModify",o='Webkit',v="WebkitUserModify";
qx.Class.define(x,{statics:{__dm:function(){var G=[F,h,q,b];
var K={};
var H=document.documentElement.style;
var L=[r,o,w,y,D];

for(var i=0,l=G.length;i<l;i++){var M=G[i];
var I=M;

if(H[M]){K[I]=M;
continue;
}M=qx.lang.String.firstUp(M);

for(var j=0,N=L.length;j<N;j++){var J=L[j]+M;

if(typeof H[J]==t){K[I]=J;
break;
}}}this.__dn=K;
this.__dn[n]=qx.core.Environment.select(k,{"gecko":f,"webkit":v,"default":h});
this.__do={};

for(var I in K){this.__do[I]=qx.lang.String.hyphenate(K[I]);
}this.__dn[c]=qx.core.Environment.select(k,{"mshtml":a,"default":B});
},__dp:{width:s,height:E,left:z,right:u,top:A,bottom:d},__dq:{clip:qx.bom.element.Clip,cursor:qx.bom.element.Cursor,opacity:qx.bom.element.Opacity,boxSizing:qx.bom.element.BoxSizing,overflowX:{set:qx.lang.Function.bind(qx.bom.element.Overflow.setX,qx.bom.element.Overflow),get:qx.lang.Function.bind(qx.bom.element.Overflow.getX,qx.bom.element.Overflow),reset:qx.lang.Function.bind(qx.bom.element.Overflow.resetX,qx.bom.element.Overflow),compile:qx.lang.Function.bind(qx.bom.element.Overflow.compileX,qx.bom.element.Overflow)},overflowY:{set:qx.lang.Function.bind(qx.bom.element.Overflow.setY,qx.bom.element.Overflow),get:qx.lang.Function.bind(qx.bom.element.Overflow.getY,qx.bom.element.Overflow),reset:qx.lang.Function.bind(qx.bom.element.Overflow.resetY,qx.bom.element.Overflow),compile:qx.lang.Function.bind(qx.bom.element.Overflow.compileY,qx.bom.element.Overflow)}},compile:function(O){var Q=[];
var S=this.__dq;
var R=this.__do;
var name,P;

for(name in O){P=O[name];

if(P==null){continue;
}name=R[name]||name;
if(S[name]){Q.push(S[name].compile(P));
}else{Q.push(qx.lang.String.hyphenate(name),C,P,p);
}}return Q.join(m);
},setCss:qx.core.Environment.select(k,{"mshtml":function(T,U){T.style.cssText=U;
},"default":function(V,W){V.setAttribute(g,W);
}}),getCss:qx.core.Environment.select(k,{"mshtml":function(X){return X.style.cssText.toLowerCase();
},"default":function(Y){return Y.getAttribute(g);
}}),isPropertySupported:function(ba){return (this.__dq[ba]||this.__dn[ba]||ba in document.documentElement.style);
},COMPUTED_MODE:1,CASCADED_MODE:2,LOCAL_MODE:3,set:function(bb,name,bc,bd){name=this.__dn[name]||name;
if(bd!==false&&this.__dq[name]){return this.__dq[name].set(bb,bc);
}else{bb.style[name]=bc!==null?bc:m;
}},setStyles:function(be,bf,bg){var bj=this.__dn;
var bl=this.__dq;
var bh=be.style;

for(var bk in bf){var bi=bf[bk];
var name=bj[bk]||bk;

if(bi===undefined){if(bg!==false&&bl[name]){bl[name].reset(be);
}else{bh[name]=m;
}}else{if(bg!==false&&bl[name]){bl[name].set(be,bi);
}else{bh[name]=bi!==null?bi:m;
}}}},reset:function(bm,name,bn){name=this.__dn[name]||name;
if(bn!==false&&this.__dq[name]){return this.__dq[name].reset(bm);
}else{bm.style[name]=m;
}},get:qx.core.Environment.select(k,{"mshtml":function(bo,name,bp,bq){name=this.__dn[name]||name;
if(bq!==false&&this.__dq[name]){return this.__dq[name].get(bo,bp);
}if(!bo.currentStyle){return bo.style[name]||m;
}switch(bp){case this.LOCAL_MODE:return bo.style[name]||m;
case this.CASCADED_MODE:return bo.currentStyle[name]||m;
default:var bu=bo.currentStyle[name]||m;
if(/^-?[\.\d]+(px)?$/i.test(bu)){return bu;
}var bt=this.__dp[name];

if(bt){var br=bo.style[name];
bo.style[name]=bu||0;
var bs=bo.style[bt]+e;
bo.style[name]=br;
return bs;
}if(/^-?[\.\d]+(em|pt|%)?$/i.test(bu)){throw new Error("Untranslated computed property value: "+name+". Only pixel values work well across different clients.");
}return bu;
}},"default":function(bv,name,bw,bx){name=this.__dn[name]||name;
if(bx!==false&&this.__dq[name]){return this.__dq[name].get(bv,bw);
}switch(bw){case this.LOCAL_MODE:return bv.style[name]||m;
case this.CASCADED_MODE:if(bv.currentStyle){return bv.currentStyle[name]||m;
}throw new Error("Cascaded styles are not supported in this browser!");
default:var by=qx.dom.Node.getDocument(bv);
var bz=by.defaultView.getComputedStyle(bv,null);
return bz?bz[name]:m;
}}})},defer:function(bA){bA.__dm();
}});
})();
(function(){var e="=",d="ecmascript.objectcount",c="+",b="qx.lang.Object",a="&";
qx.Class.define(b,{statics:{empty:function(f){for(var g in f){if(f.hasOwnProperty(g)){delete f[g];
}}},isEmpty:(qx.core.Environment.get(d))?function(h){return h.__count__===0;
}:function(j){for(var k in j){return false;
}return true;
},hasMinLength:(qx.core.Environment.get(d))?function(m,n){return m.__count__>=n;
}:function(o,p){if(p<=0){return true;
}var length=0;

for(var q in o){if((++length)>=p){return true;
}}return false;
},getLength:qx.Bootstrap.objectGetLength,getKeys:qx.Bootstrap.getKeys,getKeysAsString:qx.Bootstrap.getKeysAsString,getValues:function(r){var t=[];
var s=this.getKeys(r);

for(var i=0,l=s.length;i<l;i++){t.push(r[s[i]]);
}return t;
},mergeWith:qx.Bootstrap.objectMergeWith,carefullyMergeWith:function(u,v){return qx.lang.Object.mergeWith(u,v,false);
},merge:function(w,x){var y=arguments.length;

for(var i=1;i<y;i++){qx.lang.Object.mergeWith(w,arguments[i]);
}return w;
},clone:function(z){var A={};

for(var B in z){A[B]=z[B];
}return A;
},invert:function(C){var D={};

for(var E in C){D[C[E].toString()]=E;
}return D;
},getKeyFromValue:function(F,G){for(var H in F){if(F.hasOwnProperty(H)&&F[H]===G){return H;
}}return null;
},contains:function(I,J){return this.getKeyFromValue(I,J)!==null;
},select:function(K,L){return L[K];
},fromArray:function(M){var N={};

for(var i=0,l=M.length;i<l;i++){N[M[i].toString()]=true;
}return N;
},toUriParameter:function(O,P){var S,R=[],Q=window.encodeURIComponent;

for(S in O){if(O.hasOwnProperty(S)){if(P){R.push(Q(S).replace(/%20/g,c)+e+Q(O[S]).replace(/%20/g,c));
}else{R.push(Q(S)+e+Q(O[S]));
}}}return R.join(a);
}}});
})();
(function(){var j="/",i="0",h="qx/static",g="http://",f="https://",e="file://",d="qx.util.AliasManager",c="singleton",b=".",a="static";
qx.Class.define(d,{type:c,extend:qx.util.ValueManager,construct:function(){qx.util.ValueManager.call(this);
this.__dr={};
this.add(a,h);
},members:{__dr:null,_preprocess:function(k){var n=this._getDynamic();

if(n[k]===false){return k;
}else if(n[k]===undefined){if(k.charAt(0)===j||k.charAt(0)===b||k.indexOf(g)===0||k.indexOf(f)===i||k.indexOf(e)===0){n[k]=false;
return k;
}
if(this.__dr[k]){return this.__dr[k];
}var m=k.substring(0,k.indexOf(j));
var l=this.__dr[m];

if(l!==undefined){n[k]=l+k.substring(m.length);
}}return k;
},add:function(o,p){this.__dr[o]=p;
var r=this._getDynamic();
for(var q in r){if(q.substring(0,q.indexOf(j))===o){r[q]=p+q.substring(o.length);
}}},remove:function(s){delete this.__dr[s];
},resolve:function(t){var u=this._getDynamic();

if(t!=null){t=this._preprocess(t);
}return u[t]||t;
},getAliases:function(){var v={};

for(var w in this.__dr){v[w]=this.__dr[w];
}return v;
}},destruct:function(){this.__dr=null;
}});
})();
(function(){var f="_applyTheme",e="qx.theme.manager.Font",d="_dynamic",c="Theme",b="changeTheme",a="singleton";
qx.Class.define(e,{type:a,extend:qx.util.ValueManager,properties:{theme:{check:c,nullable:true,apply:f,event:b}},members:{resolveDynamic:function(g){var h=this._dynamic;
return g instanceof qx.bom.Font?g:h[g];
},resolve:function(i){var l=this._dynamic;
var j=l[i];

if(j){return j;
}var k=this.getTheme();

if(k!==null&&k.fonts[i]){var m=this.__dt(k.fonts[i]);
return l[i]=(new m).set(k.fonts[i]);
}return i;
},isDynamic:function(n){var q=this._dynamic;

if(n&&(n instanceof qx.bom.Font||q[n]!==undefined)){return true;
}var p=this.getTheme();

if(p!==null&&n&&p.fonts[n]){var o=this.__dt(p.fonts[n]);
q[n]=(new o).set(p.fonts[n]);
return true;
}return false;
},__ds:function(r,s){if(r[s].include){var t=r[r[s].include];
r[s].include=null;
delete r[s].include;
r[s]=qx.lang.Object.mergeWith(r[s],t,false);
this.__ds(r,s);
}},_applyTheme:function(u){var v=this._getDynamic();

for(var y in v){if(v[y].themed){v[y].dispose();
delete v[y];
}}
if(u){var w=u.fonts;

for(var y in w){if(w[y].include&&w[w[y].include]){this.__ds(w,y);
}var x=this.__dt(w[y]);
v[y]=(new x).set(w[y]);
v[y].themed=true;
}}this._setDynamic(v);
},__dt:function(z){if(z.sources){return qx.bom.webfonts.WebFont;
}return qx.bom.Font;
}},destruct:function(){this._disposeMap(d);
}});
})();
(function(){var k="",j="underline",h="Boolean",g="px",f='"',e="italic",d="normal",c="bold",b="_applyItalic",a="_applyBold",z="Integer",y="_applyFamily",x="_applyLineHeight",w="Array",v="line-through",u="overline",t="Color",s="qx.bom.Font",r="Number",q="_applyDecoration",o=" ",p="_applySize",m=",",n="_applyColor";
qx.Class.define(s,{extend:qx.core.Object,construct:function(A,B){qx.core.Object.call(this);

if(A!==undefined){this.setSize(A);
}
if(B!==undefined){this.setFamily(B);
}},statics:{fromString:function(C){var G=new qx.bom.Font();
var E=C.split(/\s+/);
var name=[];
var F;

for(var i=0;i<E.length;i++){switch(F=E[i]){case c:G.setBold(true);
break;
case e:G.setItalic(true);
break;
case j:G.setDecoration(j);
break;
default:var D=parseInt(F,10);

if(D==F||qx.lang.String.contains(F,g)){G.setSize(D);
}else{name.push(F);
}break;
}}
if(name.length>0){G.setFamily(name);
}return G;
},fromConfig:function(H){var I=new qx.bom.Font;
I.set(H);
return I;
},__du:{fontFamily:k,fontSize:k,fontWeight:k,fontStyle:k,textDecoration:k,lineHeight:1.2,textColor:k},getDefaultStyles:function(){return this.__du;
}},properties:{size:{check:z,nullable:true,apply:p},lineHeight:{check:r,nullable:true,apply:x},family:{check:w,nullable:true,apply:y},bold:{check:h,nullable:true,apply:a},italic:{check:h,nullable:true,apply:b},decoration:{check:[j,v,u],nullable:true,apply:q},color:{check:t,nullable:true,apply:n}},members:{__dv:null,__dw:null,__dx:null,__dy:null,__dz:null,__dA:null,__dB:null,_applySize:function(J,K){this.__dv=J===null?null:J+g;
},_applyLineHeight:function(L,M){this.__dA=L===null?null:L;
},_applyFamily:function(N,O){var P=k;

for(var i=0,l=N.length;i<l;i++){if(N[i].indexOf(o)>0){P+=f+N[i]+f;
}else{P+=N[i];
}
if(i!==l-1){P+=m;
}}this.__dw=P;
},_applyBold:function(Q,R){this.__dx=Q===null?null:Q?c:d;
},_applyItalic:function(S,T){this.__dy=S===null?null:S?e:d;
},_applyDecoration:function(U,V){this.__dz=U===null?null:U;
},_applyColor:function(W,X){this.__dB=W===null?null:W;
},getStyles:function(){return {fontFamily:this.__dw,fontSize:this.__dv,fontWeight:this.__dx,fontStyle:this.__dy,textDecoration:this.__dz,lineHeight:this.__dA,textColor:this.__dB};
}}});
})();
(function(){var g="'",f="qx.bom.webfonts.WebFont",e="",d="changeStatus",c=" ",b="_applySources",a="qx.event.type.Data";
qx.Class.define(f,{extend:qx.bom.Font,events:{"changeStatus":a},properties:{sources:{nullable:true,apply:b}},members:{__dC:null,_applySources:function(h,j){var n=[];

for(var i=0,l=h.length;i<l;i++){var m=this._quoteFontFamily(h[i].family);
n.push(m);
var k=h[i].source;
qx.bom.webfonts.Manager.getInstance().require(m,k,this._onWebFontChangeStatus,this);
}this.setFamily(n.concat(this.getFamily()));
},_onWebFontChangeStatus:function(o){var p=o.getData();
this.fireDataEvent(d,p);
},_quoteFontFamily:function(q){q=q.replace(/["']/g,e);

if(q.indexOf(c)>0){q=g+q+g;
}return q;
}}});
})();
(function(){var n="",k="url('",h="ie",g="browser.name",f="changeStatus",e="svg",d="chrome",c="#",b="firefox",a="eot",T="ios",S="ttf",R="browser.version",Q="woff",P="m",O="os.name",N=")",M="qx.bom.webfonts.Manager",L="singleton",K=",\n",u="src: ",v="mobileSafari",s="'eot)",t="@font-face {",q="interval",r="}\n",o="font-family: ",p="mobile safari",w="safari",y="?#iefix') format('eot')",C=";\n",B="') format('woff')",E="opera",D="\.(",G="os.version",F="') format('svg')",A="'eot')",J="\nfont-style: normal;\nfont-weight: normal;",I="@font-face.*?",H=";",z="') format('truetype')";
qx.Class.define(M,{extend:qx.core.Object,type:L,construct:function(){qx.core.Object.call(this);
this.__dD=[];
this.__dE={};
this.__dF=[];
this.__dG=this.getPreferredFormats();
},statics:{FONT_FORMATS:["eot","woff","ttf","svg"],VALIDATION_TIMEOUT:5000},members:{__dD:null,__dH:null,__dE:null,__dG:null,__dF:null,__dI:null,require:function(U,V,W,X){var Y=[];

for(var i=0,l=V.length;i<l;i++){var bb=V[i].split(c);
var ba=qx.util.ResourceManager.getInstance().toUri(bb[0]);

if(bb.length>1){ba=ba+c+bb[1];
}Y.push(ba);
}if(!(qx.core.Environment.get(g)==h&&qx.bom.client.Browser.getVersion()<9)){this.__dJ(U,Y,W,X);
return;
}
if(!this.__dI){this.__dI=new qx.event.Timer(100);
this.__dI.addListener(q,this.__dK,this);
}
if(!this.__dI.isEnabled()){this.__dI.start();
}this.__dF.push([U,Y,W,X]);
},remove:function(bc){var bd=null;

for(var i=0,l=this.__dD.length;i<l;i++){if(this.__dD[i]==bc){bd=i;
this.__dQ(bc);
break;
}}
if(bd){qx.lang.Array.removeAt(this.__dD,bd);
}
if(bc in this.__dE){this.__dE[bc].dispose();
delete this.__dE[bc];
}},getPreferredFormats:function(){var be=[];
var bi=qx.core.Environment.get(g);
var bf=qx.core.Environment.get(R);
var bh=qx.core.Environment.get(O);
var bg=qx.core.Environment.get(G);

if((bi==h&&bf>=9)||(bi==b&&bf>=3.6)||(bi==d&&bf>=6)){be.push(Q);
}
if((bi==E&&bf>=10)||(bi==w&&bf>=3.1)||(bi==b&&bf>=3.5)||(bi==d&&bf>=4)||(bi==p&&bh==T&&bg>=4.2)){be.push(S);
}
if(bi==h&&bf>=4){be.push(a);
}
if(bi==v&&bh==T&&bg>=4.1){be.push(e);
}return be;
},removeStyleSheet:function(){this.__dD=[];

if(this.__dH){var bj=this.__dH.ownerNode?this.__dH.ownerNode:this.__dH.owningElement;
qx.dom.Element.removeChild(bj,bj.parentNode);
}this.__dH=null;
},__dJ:function(bk,bl,bm,bn){if(!qx.lang.Array.contains(this.__dD,bk)){var bq=this.__dM(bl);
var bp=this.__dN(bk,bq);

if(!bp){throw new Error("Couldn't create @font-face rule for WebFont "+bk+"!");
}
if(!this.__dH){this.__dH=qx.bom.Stylesheet.createElement();
}
try{this.__dP(bp);
}catch(br){}this.__dD.push(bk);
}
if(!this.__dE[bk]){this.__dE[bk]=new qx.bom.webfonts.Validator(bk);
this.__dE[bk].setTimeout(qx.bom.webfonts.Manager.VALIDATION_TIMEOUT);
this.__dE[bk].addListenerOnce(f,this.__dL,this);
}
if(bm){var bo=bn||window;
this.__dE[bk].addListenerOnce(f,bm,bo);
}this.__dE[bk].validate();
},__dK:function(){if(this.__dF.length==0){this.__dI.stop();
return;
}var bs=this.__dF.shift();
this.__dJ.apply(this,bs);
},__dL:function(bt){var bu=bt.getData();

if(bu.valid===false){qx.event.Timer.once(function(){this.remove(bu.family);
},this,250);
}},__dM:function(bv){var bx=qx.bom.webfonts.Manager.FONT_FORMATS;
var bA={};

for(var i=0,l=bv.length;i<l;i++){var by=null;

for(var x=0;x<bx.length;x++){var bz=new RegExp(D+bx[x]+N);
var bw=bz.exec(bv[i]);

if(bw){by=bw[1];
}}
if(by){bA[by]=bv[i];
}}return bA;
},__dN:function(bB,bC){var bF=[];
var bD=this.__dG.length>0?this.__dG:qx.bom.webfonts.Manager.FONT_FORMATS;

for(var i=0,l=bD.length;i<l;i++){var bE=bD[i];

if(bC[bE]){bF.push(this.__dO(bE,bC[bE]));
}}var bG=u+bF.join(K)+H;
bG=o+bB+C+bG;
bG=bG+J;
return bG;
},__dO:function(bH,bI){switch(bH){case a:return k+bI+y;
case Q:return k+bI+B;
case S:return k+bI+z;
case e:return k+bI+F;
default:return null;
}},__dP:function(bJ){var bL=t+bJ+r;

if(qx.core.Environment.get(g)==h&&qx.core.Environment.get(R)<9){var bK=this.__dR(this.__dH.cssText);
bK+=bL;
this.__dH.cssText=bK;
}else{this.__dH.insertRule(bL,this.__dH.cssRules.length);
}},__dQ:function(bM){var bP=new RegExp(I+bM,P);

for(var i=0,l=document.styleSheets.length;i<l;i++){var bN=document.styleSheets[i];

if(bN.cssText){var bO=bN.cssText.replace(/\n/g,n).replace(/\r/g,n);
bO=this.__dR(bO);

if(bP.exec(bO)){bO=bO.replace(bP,n);
}bN.cssText=bO;
}else if(bN.cssRules){for(var j=0,m=bN.cssRules.length;j<m;j++){var bO=bN.cssRules[j].cssText.replace(/\n/g,n).replace(/\r/g,n);

if(bP.exec(bO)){this.__dH.deleteRule(j);
return;
}}}}},__dR:function(bQ){return bQ.replace(s,A);
}},destruct:function(){delete this.__dD;
this.removeStyleSheet();

for(var bR in this.__dE){this.__dE[bR].dispose();
}qx.bom.webfonts.Validator.removeDefaultHelperElements();
}});
})();
(function(){var p="",o="/",n="mshtml",m="engine.name",l="io.ssl",k="string",j="//",i="?",h="data",g="type",c="data:image/",f=";",e="encoding",b="qx.util.ResourceManager",a="singleton",d=",";
qx.Class.define(b,{extend:qx.core.Object,type:a,construct:function(){qx.core.Object.call(this);
},statics:{__v:qx.$$resources||{},__dS:{}},members:{has:function(q){return !!this.self(arguments).__v[q];
},getData:function(r){return this.self(arguments).__v[r]||null;
},getImageWidth:function(s){var t=this.self(arguments).__v[s];
return t?t[0]:null;
},getImageHeight:function(u){var v=this.self(arguments).__v[u];
return v?v[1]:null;
},getImageFormat:function(w){var x=this.self(arguments).__v[w];
return x?x[2]:null;
},getCombinedFormat:function(y){var B=p;
var A=this.self(arguments).__v[y];
var z=A&&A.length>4&&typeof (A[4])==k&&this.constructor.__v[A[4]];

if(z){var D=A[4];
var C=this.constructor.__v[D];
B=C[2];
}return B;
},toUri:function(E){if(E==null){return E;
}var F=this.self(arguments).__v[E];

if(!F){return E;
}
if(typeof F===k){var H=F;
}else{var H=F[3];
if(!H){return E;
}}var G=p;

if((qx.core.Environment.get(m)==n)&&qx.core.Environment.get(l)){G=this.self(arguments).__dS[H];
}return G+qx.$$libraries[H].resourceUri+o+E;
},toDataUri:function(I){var K=this.constructor.__v[I];
var L=this.constructor.__v[K[4]];
var M;

if(L){var J=L[4][I];
M=c+J[g]+f+J[e]+d+J[h];
}else{M=this.toUri(I);
}return M;
}},defer:function(N){if((qx.core.Environment.get(m)==n)){if(qx.core.Environment.get(l)){for(var R in qx.$$libraries){var P;

if(qx.$$libraries[R].resourceUri){P=qx.$$libraries[R].resourceUri;
}else{N.__dS[R]=p;
continue;
}if(P.match(/^\/\//)!=null){N.__dS[R]=window.location.protocol;
}else if(P.match(/^\//)!=null){N.__dS[R]=window.location.protocol+j+window.location.host;
}else if(P.match(/^\.\//)!=null){var O=document.URL;
N.__dS[R]=O.substring(0,O.lastIndexOf(o)+1);
}else if(P.match(/^http/)!=null){N.__dS[R]=p;
}else{var S=window.location.href.indexOf(i);
var Q;

if(S==-1){Q=window.location.href;
}else{Q=window.location.href.substring(0,S);
}N.__dS[R]=Q.substring(0,Q.lastIndexOf(o)+1);
}}}}}});
})();
(function(){var h="interval",g="qx.event.Timer",f="_applyInterval",d="_applyEnabled",c="Boolean",b="qx.event.type.Event",a="Integer";
qx.Class.define(g,{extend:qx.core.Object,construct:function(i){qx.core.Object.call(this);
this.setEnabled(false);

if(i!=null){this.setInterval(i);
}var self=this;
this.__dT=function(){self._oninterval.call(self);
};
},events:{"interval":b},statics:{once:function(j,k,l){var m=new qx.event.Timer(l);
m.__dU=j;
m.addListener(h,function(e){m.stop();
j.call(k,e);
m.dispose();
k=null;
},k);
m.start();
return m;
}},properties:{enabled:{init:true,check:c,apply:d},interval:{check:a,init:1000,apply:f}},members:{__dV:null,__dT:null,_applyInterval:function(n,o){if(this.getEnabled()){this.restart();
}},_applyEnabled:function(p,q){if(q){window.clearInterval(this.__dV);
this.__dV=null;
}else if(p){this.__dV=window.setInterval(this.__dT,this.getInterval());
}},start:function(){this.setEnabled(true);
},startWith:function(r){this.setInterval(r);
this.start();
},stop:function(){this.setEnabled(false);
},restart:function(){this.stop();
this.start();
},restartWith:function(s){this.stop();
this.startWith(s);
},_oninterval:qx.event.GlobalError.observeMethod(function(){if(this.$$disposed){return;
}
if(this.getEnabled()){this.fireEvent(h);
}})},destruct:function(){if(this.__dV){window.clearInterval(this.__dV);
}this.__dV=this.__dT=null;
}});
})();
(function(){var a="qx.dom.Element";
qx.Class.define(a,{statics:{hasChild:function(parent,b){return b.parentNode===parent;
},hasChildren:function(c){return !!c.firstChild;
},hasChildElements:function(d){d=d.firstChild;

while(d){if(d.nodeType===1){return true;
}d=d.nextSibling;
}return false;
},getParentElement:function(e){return e.parentNode;
},isInDom:function(f,g){if(!g){g=window;
}var h=g.document.getElementsByTagName(f.nodeName);

for(var i=0,l=h.length;i<l;i++){if(h[i]===f){return true;
}}return false;
},insertAt:function(j,parent,k){var m=parent.childNodes[k];

if(m){parent.insertBefore(j,m);
}else{parent.appendChild(j);
}return true;
},insertBegin:function(n,parent){if(parent.firstChild){this.insertBefore(n,parent.firstChild);
}else{parent.appendChild(n);
}},insertEnd:function(o,parent){parent.appendChild(o);
},insertBefore:function(p,q){q.parentNode.insertBefore(p,q);
return true;
},insertAfter:function(r,s){var parent=s.parentNode;

if(s==parent.lastChild){parent.appendChild(r);
}else{return this.insertBefore(r,s.nextSibling);
}return true;
},remove:function(t){if(!t.parentNode){return false;
}t.parentNode.removeChild(t);
return true;
},removeChild:function(u,parent){if(u.parentNode!==parent){return false;
}parent.removeChild(u);
return true;
},removeChildAt:function(v,parent){var w=parent.childNodes[v];

if(!w){return false;
}parent.removeChild(w);
return true;
},replaceChild:function(x,y){if(!y.parentNode){return false;
}y.parentNode.replaceChild(x,y);
return true;
},replaceAt:function(z,A,parent){var B=parent.childNodes[A];

if(!B){return false;
}parent.replaceChild(z,B);
return true;
}}});
})();
(function(){var l="engine.name",k="head",j="text/css",h="stylesheet",g="}",f='@import "',e="{",d='";',c="qx.bom.Stylesheet",b="link",a="style";
qx.Class.define(c,{statics:{includeFile:function(m,n){if(!n){n=document;
}var o=n.createElement(b);
o.type=j;
o.rel=h;
o.href=qx.util.ResourceManager.getInstance().toUri(m);
var p=n.getElementsByTagName(k)[0];
p.appendChild(o);
},createElement:qx.core.Environment.select(l,{"mshtml":function(q){var r=document.createStyleSheet();

if(q){r.cssText=q;
}return r;
},"default":function(s){var t=document.createElement(a);
t.type=j;

if(s){t.appendChild(document.createTextNode(s));
}document.getElementsByTagName(k)[0].appendChild(t);
return t.sheet;
}}),addRule:qx.core.Environment.select(l,{"mshtml":function(u,v,w){u.addRule(v,w);
},"default":function(x,y,z){x.insertRule(y+e+z+g,x.cssRules.length);
}}),removeRule:qx.core.Environment.select(l,{"mshtml":function(A,B){var C=A.rules;
var D=C.length;

for(var i=D-1;i>=0;--i){if(C[i].selectorText==B){A.removeRule(i);
}}},"default":function(E,F){var G=E.cssRules;
var H=G.length;

for(var i=H-1;i>=0;--i){if(G[i].selectorText==F){E.deleteRule(i);
}}}}),removeAllRules:qx.core.Environment.select(l,{"mshtml":function(I){var J=I.rules;
var K=J.length;

for(var i=K-1;i>=0;i--){I.removeRule(i);
}},"default":function(L){var M=L.cssRules;
var N=M.length;

for(var i=N-1;i>=0;i--){L.deleteRule(i);
}}}),addImport:qx.core.Environment.select(l,{"mshtml":function(O,P){O.addImport(P);
},"default":function(Q,R){Q.insertRule(f+R+d,Q.cssRules.length);
}}),removeImport:qx.core.Environment.select(l,{"mshtml":function(S,T){var U=S.imports;
var V=U.length;

for(var i=V-1;i>=0;i--){if(U[i].href==T){S.removeImport(i);
}}},"default":function(W,X){var Y=W.cssRules;
var ba=Y.length;

for(var i=ba-1;i>=0;i--){if(Y[i].href==X){W.deleteRule(i);
}}}}),removeAllImports:qx.core.Environment.select(l,{"mshtml":function(bb){var bc=bb.imports;
var bd=bc.length;

for(var i=bd-1;i>=0;i--){bb.removeImport(i);
}},"default":function(be){var bf=be.cssRules;
var bg=bf.length;

for(var i=bg-1;i>=0;i--){if(bf[i].type==bf[i].IMPORT_RULE){be.deleteRule(i);
}}}})}});
})();
(function(){var h=",",g="interval",f="changeStatus",e="qx.event.type.Data",d="qx.bom.webfonts.Validator",c="_applyFontFamily",b="span",a="Integer";
qx.Class.define(d,{extend:qx.core.Object,construct:function(i){qx.core.Object.call(this);

if(i){this.setFontFamily(i);
}this.__dW=this._getRequestedHelpers();
},statics:{COMPARISON_FONTS:{sans:["Arial","Helvetica","sans-serif"],serif:["Times New Roman","Georgia","serif"]},HELPER_CSS:{position:"absolute",margin:"0",padding:"0",top:"-1000px",left:"-1000px",fontSize:"350px",width:"auto",height:"auto",lineHeight:"normal",fontVariant:"normal"},COMPARISON_STRING:"WEei",__dX:null,__dY:null,removeDefaultHelperElements:function(){var j=qx.bom.webfonts.Validator.__dY;

if(j){for(var k in j){document.body.removeChild(j[k]);
}}delete qx.bom.webfonts.Validator.__dY;
}},properties:{fontFamily:{nullable:true,init:null,apply:c},timeout:{check:a,init:5000}},events:{"changeStatus":e},members:{__dW:null,__ea:null,__eb:null,validate:function(){this.__eb=new Date().getTime();

if(this.__ea){this.__ea.restart();
}else{this.__ea=new qx.event.Timer(100);
this.__ea.addListener(g,this.__ec,this);
qx.event.Timer.once(function(){this.__ea.start();
},this,0);
}},_reset:function(){if(this.__dW){for(var m in this.__dW){var l=this.__dW[m];
document.body.removeChild(l);
}this.__dW=null;
}},_isFontValid:function(){if(!qx.bom.webfonts.Validator.__dX){this.__bk();
}
if(!this.__dW){this.__dW=this._getRequestedHelpers();
}var o=qx.bom.element.Dimension.getWidth(this.__dW.sans);
var n=qx.bom.element.Dimension.getWidth(this.__dW.serif);
var p=qx.bom.webfonts.Validator;

if(o!==p.__dX.sans&&n!==p.__dX.serif){return true;
}return false;
},_getRequestedHelpers:function(){var q=[this.getFontFamily()].concat(qx.bom.webfonts.Validator.COMPARISON_FONTS.sans);
var r=[this.getFontFamily()].concat(qx.bom.webfonts.Validator.COMPARISON_FONTS.serif);
return {sans:this._getHelperElement(q),serif:this._getHelperElement(r)};
},_getHelperElement:function(s){var t=qx.lang.Object.clone(qx.bom.webfonts.Validator.HELPER_CSS);

if(s){if(t.fontFamily){t.fontFamily+=h+s.join(h);
}else{t.fontFamily=s.join(h);
}}var u=document.createElement(b);
u.innerHTML=qx.bom.webfonts.Validator.COMPARISON_STRING;
qx.bom.element.Style.setStyles(u,t);
document.body.appendChild(u);
return u;
},_applyFontFamily:function(v,w){if(v!==w){this._reset();
}},__bk:function(){var x=qx.bom.webfonts.Validator;

if(!x.__dY){x.__dY={sans:this._getHelperElement(x.COMPARISON_FONTS.sans),serif:this._getHelperElement(x.COMPARISON_FONTS.serif)};
}x.__dX={sans:qx.bom.element.Dimension.getWidth(x.__dY.sans),serif:qx.bom.element.Dimension.getWidth(x.__dY.serif)};
},__ec:function(){if(this._isFontValid()){this.__ea.stop();
this._reset();
this.fireDataEvent(f,{family:this.getFontFamily(),valid:true});
}else{var y=new Date().getTime();

if(y-this.__eb>=this.getTimeout()){this.__ea.stop();
this._reset();
this.fireDataEvent(f,{family:this.getFontFamily(),valid:false});
}}}},destruct:function(){this._reset();
this.__ea.stop();
this.__ea.removeListener(g,this.__ec,this);
this._disposeObjects(this.__ea);
}});
})();
(function(){var j="engine.name",i="0px",h="mshtml",g="engine.version",f="qx.bom.element.Dimension",e="paddingRight",d="paddingLeft",c="opera",b="paddingBottom",a="paddingTop";
qx.Class.define(f,{statics:{getWidth:qx.core.Environment.select(j,{"gecko":function(k){if(k.getBoundingClientRect){var l=k.getBoundingClientRect();
return Math.round(l.right)-Math.round(l.left);
}else{return k.offsetWidth;
}},"default":function(m){return m.offsetWidth;
}}),getHeight:qx.core.Environment.select(j,{"gecko":function(n){if(n.getBoundingClientRect){var o=n.getBoundingClientRect();
return Math.round(o.bottom)-Math.round(o.top);
}else{return n.offsetHeight;
}},"default":function(p){return p.offsetHeight;
}}),getSize:function(q){return {width:this.getWidth(q),height:this.getHeight(q)};
},__ed:{visible:true,hidden:true},getContentWidth:function(r){var s=qx.bom.element.Style;
var t=qx.bom.element.Overflow.getX(r);
var u=parseInt(s.get(r,d)||i,10);
var x=parseInt(s.get(r,e)||i,10);

if(this.__ed[t]){var w=r.clientWidth;

if((qx.core.Environment.get(j)==c)){w=w-u-x;
}else{if(qx.dom.Node.isBlockNode(r)){w=w-u-x;
}}return w;
}else{if(r.clientWidth>=r.scrollWidth){return Math.max(r.clientWidth,r.scrollWidth)-u-x;
}else{var v=r.scrollWidth-u;
if(qx.core.Environment.get(j)==h&&qx.core.Environment.get(g)>=6){v-=x;
}return v;
}}},getContentHeight:function(y){var z=qx.bom.element.Style;
var C=qx.bom.element.Overflow.getY(y);
var B=parseInt(z.get(y,a)||i,10);
var A=parseInt(z.get(y,b)||i,10);

if(this.__ed[C]){return y.clientHeight-B-A;
}else{if(y.clientHeight>=y.scrollHeight){return Math.max(y.clientHeight,y.scrollHeight)-B-A;
}else{var D=y.scrollHeight-B;
if(qx.core.Environment.get(j)==h&&qx.core.Environment.get(g)==6){D-=A;
}return D;
}}},getContentSize:function(E){return {width:this.getContentWidth(E),height:this.getContentHeight(E)};
}}});
})();
(function(){var e="qx.theme.manager.Icon",d="Theme",c="changeTheme",b="_applyTheme",a="singleton";
qx.Class.define(e,{type:a,extend:qx.core.Object,properties:{theme:{check:d,nullable:true,apply:b,event:c}},members:{_applyTheme:function(f,g){var i=qx.util.AliasManager.getInstance();

if(g){for(var h in g.aliases){i.remove(h);
}}
if(f){for(var h in f.aliases){i.add(h,f.aliases[h]);
}}}}});
})();
(function(){var h="string",g="_applyTheme",f="qx.theme.manager.Appearance",e=":",d="Theme",c="changeTheme",b="/",a="singleton";
qx.Class.define(f,{type:a,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__ee={};
this.__ef={};
},properties:{theme:{check:d,nullable:true,event:c,apply:g}},members:{__eg:{},__ee:null,__ef:null,_applyTheme:function(j,k){this.__ef={};
this.__ee={};
},__eh:function(l,m,n){var s=m.appearances;
var v=s[l];

if(!v){var w=b;
var p=[];
var u=l.split(w);
var t;

while(!v&&u.length>0){p.unshift(u.pop());
var q=u.join(w);
v=s[q];

if(v){t=v.alias||v;

if(typeof t===h){var r=t+w+p.join(w);
return this.__eh(r,m,n);
}}}for(var i=0;i<p.length-1;i++){p.shift();
var q=p.join(w);
var o=this.__eh(q,m);

if(o){return o;
}}if(n!=null){return this.__eh(n,m);
}return null;
}else if(typeof v===h){return this.__eh(v,m,n);
}else if(v.include&&!v.style){return this.__eh(v.include,m,n);
}return l;
},styleFrom:function(x,y,z,A){if(!z){z=this.getTheme();
}var F=this.__ef;
var B=F[x];

if(!B){B=F[x]=this.__eh(x,z,A);
}var L=z.appearances[B];

if(!L){this.warn("Missing appearance: "+x);
return null;
}if(!L.style){return null;
}var M=B;

if(y){var N=L.$$bits;

if(!N){N=L.$$bits={};
L.$$length=0;
}var D=0;

for(var H in y){if(!y[H]){continue;
}
if(N[H]==null){N[H]=1<<L.$$length++;
}D+=N[H];
}if(D>0){M+=e+D;
}}var E=this.__ee;

if(E[M]!==undefined){return E[M];
}if(!y){y=this.__eg;
}var J;
if(L.include||L.base){var C;

if(L.include){C=this.styleFrom(L.include,y,z,A);
}var G=L.style(y,C);
J={};
if(L.base){var I=this.styleFrom(B,y,L.base,A);

if(L.include){for(var K in I){if(!C.hasOwnProperty(K)&&!G.hasOwnProperty(K)){J[K]=I[K];
}}}else{for(var K in I){if(!G.hasOwnProperty(K)){J[K]=I[K];
}}}}if(L.include){for(var K in C){if(!G.hasOwnProperty(K)){J[K]=C[K];
}}}for(var K in G){J[K]=G[K];
}}else{J=L.style(y);
}return E[M]=J||null;
}},destruct:function(){this.__ee=this.__ef=null;
}});
})();
(function(){var p="other",o="widgets",n="fonts",m="appearances",k="qx.Theme",j="]",h="[Theme ",g="colors",f="decorations",e="Theme",b="meta",d="borders",c="icons";
qx.Bootstrap.define(k,{statics:{define:function(name,q){if(!q){var q={};
}q.include=this.__ei(q.include);
q.patch=this.__ei(q.patch);
var r={$$type:e,name:name,title:q.title,toString:this.genericToString};
if(q.extend){r.supertheme=q.extend;
}r.basename=qx.Bootstrap.createNamespace(name,r);
this.__el(r,q);
this.__ej(r,q);
this.$$registry[name]=r;
for(var i=0,a=q.include,l=a.length;i<l;i++){this.include(r,a[i]);
}
for(var i=0,a=q.patch,l=a.length;i<l;i++){this.patch(r,a[i]);
}},__ei:function(s){if(!s){return [];
}
if(qx.Bootstrap.isArray(s)){return s;
}else{return [s];
}},__ej:function(t,u){var v=u.aliases||{};

if(u.extend&&u.extend.aliases){qx.Bootstrap.objectMergeWith(v,u.extend.aliases,false);
}t.aliases=v;
},getAll:function(){return this.$$registry;
},getByName:function(name){return this.$$registry[name];
},isDefined:function(name){return this.getByName(name)!==undefined;
},getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},genericToString:function(){return h+this.name+j;
},__ek:function(w){for(var i=0,x=this.__em,l=x.length;i<l;i++){if(w[x[i]]){return x[i];
}}},__el:function(y,z){var C=this.__ek(z);
if(z.extend&&!C){C=z.extend.type;
}y.type=C||p;
var E=function(){};
if(z.extend){E.prototype=new z.extend.$$clazz;
}var D=E.prototype;
var B=z[C];
for(var A in B){D[A]=B[A];
if(D[A].base){D[A].base=z.extend;
}}y.$$clazz=E;
y[C]=new E;
},$$registry:{},__em:[g,d,f,n,c,o,m,b],__o:null,__en:null,__p:function(){},patch:function(F,G){var I=this.__ek(G);

if(I!==this.__ek(F)){throw new Error("The mixins '"+F.name+"' are not compatible '"+G.name+"'!");
}var H=G[I];
var J=F.$$clazz.prototype;

for(var K in H){J[K]=H[K];
}},include:function(L,M){var O=M.type;

if(O!==L.type){throw new Error("The mixins '"+L.name+"' are not compatible '"+M.name+"'!");
}var N=M[O];
var P=L.$$clazz.prototype;

for(var Q in N){if(P[Q]!==undefined){continue;
}P[Q]=N[Q];
}}}});
})();
(function(){var p="Boolean",o="focusout",n="interval",m="mouseover",l="mouseout",k="mousemove",j="widget",i="qx.ui.tooltip.ToolTip",h="__eo",g="__er",c="_applyCurrent",f="qx.ui.tooltip.Manager",d="tooltip-error",b="singleton",a="__ep";
qx.Class.define(f,{type:b,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
qx.event.Registration.addListener(document.body,m,this.__ey,this,true);
this.__eo=new qx.event.Timer();
this.__eo.addListener(n,this.__ev,this);
this.__ep=new qx.event.Timer();
this.__ep.addListener(n,this.__ew,this);
this.__eq={left:0,top:0};
},properties:{current:{check:i,nullable:true,apply:c},showInvalidToolTips:{check:p,init:true},showToolTips:{check:p,init:true}},members:{__eq:null,__ep:null,__eo:null,__er:null,__es:null,__et:function(){if(!this.__er){this.__er=new qx.ui.tooltip.ToolTip().set({rich:true});
}return this.__er;
},__eu:function(){if(!this.__es){this.__es=new qx.ui.tooltip.ToolTip().set({appearance:d});
this.__es.syncAppearance();
}return this.__es;
},_applyCurrent:function(q,r){if(r&&qx.ui.core.Widget.contains(r,q)){return;
}if(r){if(!r.isDisposed()){r.exclude();
}this.__eo.stop();
this.__ep.stop();
}var t=qx.event.Registration;
var s=document.body;
if(q){this.__eo.startWith(q.getShowTimeout());
t.addListener(s,l,this.__ez,this,true);
t.addListener(s,o,this.__eA,this,true);
t.addListener(s,k,this.__ex,this,true);
}else{t.removeListener(s,l,this.__ez,this,true);
t.removeListener(s,o,this.__eA,this,true);
t.removeListener(s,k,this.__ex,this,true);
}},__ev:function(e){var u=this.getCurrent();

if(u&&!u.isDisposed()){this.__ep.startWith(u.getHideTimeout());

if(u.getPlaceMethod()==j){u.placeToWidget(u.getOpener());
}else{u.placeToPoint(this.__eq);
}u.show();
}this.__eo.stop();
},__ew:function(e){var v=this.getCurrent();

if(v&&!v.isDisposed()){v.exclude();
}this.__ep.stop();
this.resetCurrent();
},__ex:function(e){var w=this.__eq;
w.left=e.getDocumentLeft();
w.top=e.getDocumentTop();
},__ey:function(e){var z=qx.ui.core.Widget.getWidgetByElement(e.getTarget());

if(!z){return;
}var A,B,y,x;
while(z!=null){A=z.getToolTip();
B=z.getToolTipText()||null;
y=z.getToolTipIcon()||null;

if(qx.Class.hasInterface(z.constructor,qx.ui.form.IForm)&&!z.isValid()){x=z.getInvalidMessage();
}
if(A||B||y||x){break;
}z=z.getLayoutParent();
}if(!z||!z.getEnabled()||z.isBlockToolTip()||(!x&&!this.getShowToolTips())||(x&&!this.getShowInvalidToolTips())){return;
}
if(x){A=this.__eu().set({label:x});
}
if(!A){A=this.__et().set({label:B,icon:y});
}this.setCurrent(A);
A.setOpener(z);
},__ez:function(e){var C=qx.ui.core.Widget.getWidgetByElement(e.getTarget());

if(!C){return;
}var D=qx.ui.core.Widget.getWidgetByElement(e.getRelatedTarget());

if(!D){return;
}var E=this.getCurrent();
if(E&&(D==E||qx.ui.core.Widget.contains(E,D))){return;
}if(D&&C&&qx.ui.core.Widget.contains(C,D)){return;
}if(E&&!D){this.setCurrent(null);
}else{this.resetCurrent();
}},__eA:function(e){var F=qx.ui.core.Widget.getWidgetByElement(e.getTarget());

if(!F){return;
}var G=this.getCurrent();
if(G&&G==F.getToolTip()){this.setCurrent(null);
}}},destruct:function(){qx.event.Registration.removeListener(document.body,m,this.__ey,this,true);
this._disposeObjects(h,a,g);
this.__eq=null;
}});
})();
(function(){var a="qx.ui.core.MChildrenHandling";
qx.Mixin.define(a,{members:{getChildren:function(){return this._getChildren();
},hasChildren:function(){return this._hasChildren();
},indexOf:function(b){return this._indexOf(b);
},add:function(c,d){this._add(c,d);
},addAt:function(e,f,g){this._addAt(e,f,g);
},addBefore:function(h,i,j){this._addBefore(h,i,j);
},addAfter:function(k,l,m){this._addAfter(k,l,m);
},remove:function(n){this._remove(n);
},removeAt:function(o){return this._removeAt(o);
},removeAll:function(){return this._removeAll();
}},statics:{remap:function(p){p.getChildren=p._getChildren;
p.hasChildren=p._hasChildren;
p.indexOf=p._indexOf;
p.add=p._add;
p.addAt=p._addAt;
p.addBefore=p._addBefore;
p.addAfter=p._addAfter;
p.remove=p._remove;
p.removeAt=p._removeAt;
p.removeAll=p._removeAll;
}}});
})();
(function(){var a="qx.ui.core.MLayoutHandling";
qx.Mixin.define(a,{members:{setLayout:function(b){return this._setLayout(b);
},getLayout:function(){return this._getLayout();
}},statics:{remap:function(c){c.getLayout=c._getLayout;
c.setLayout=c._setLayout;
}}});
})();
(function(){var b="qx.ui.core.DecoratorFactory",a="$$nopool$$";
qx.Class.define(b,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__cM={};
},statics:{MAX_SIZE:15,__eB:a},members:{__cM:null,getDecoratorElement:function(c){var h=qx.ui.core.DecoratorFactory;

if(qx.lang.Type.isString(c)){var f=c;
var e=qx.theme.manager.Decoration.getInstance().resolve(c);
}else{var f=h.__eB;
e=c;
}var g=this.__cM;

if(g[f]&&g[f].length>0){var d=g[f].pop();
}else{var d=this._createDecoratorElement(e,f);
}d.$$pooled=false;
return d;
},poolDecorator:function(i){if(!i||i.$$pooled||i.isDisposed()){return;
}var l=qx.ui.core.DecoratorFactory;
var j=i.getId();

if(j==l.__eB){i.dispose();
return;
}var k=this.__cM;

if(!k[j]){k[j]=[];
}
if(k[j].length>l.MAX_SIZE){i.dispose();
}else{i.$$pooled=true;
k[j].push(i);
}},_createDecoratorElement:function(m,n){var o=new qx.html.Decorator(m,n);
return o;
},toString:function(){return qx.core.Object.prototype.toString.call(this);
}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){var q=this.__cM;

for(var p in q){qx.util.DisposeUtil.disposeArray(q,p);
}}this.__cM=null;
}});
})();
(function(){var b="qx.util.DeferredCallManager",a="singleton";
qx.Class.define(b,{extend:qx.core.Object,type:a,construct:function(){this.__eC={};
this.__eD=qx.lang.Function.bind(this.__eH,this);
this.__eE=false;
},members:{__eF:null,__eG:null,__eC:null,__eE:null,__eD:null,schedule:function(c){if(this.__eF==null){this.__eF=window.setTimeout(this.__eD,0);
}var d=c.toHashCode();
if(this.__eG&&this.__eG[d]){return;
}this.__eC[d]=c;
this.__eE=true;
},cancel:function(e){var f=e.toHashCode();
if(this.__eG&&this.__eG[f]){this.__eG[f]=null;
return;
}delete this.__eC[f];
if(qx.lang.Object.isEmpty(this.__eC)&&this.__eF!=null){window.clearTimeout(this.__eF);
this.__eF=null;
}},__eH:qx.event.GlobalError.observeMethod(function(){this.__eF=null;
while(this.__eE){this.__eG=qx.lang.Object.clone(this.__eC);
this.__eC={};
this.__eE=false;

for(var h in this.__eG){var g=this.__eG[h];

if(g){this.__eG[h]=null;
g.call();
}}}this.__eG=null;
})},destruct:function(){if(this.__eF!=null){window.clearTimeout(this.__eF);
}this.__eD=this.__eC=null;
}});
})();
(function(){var a="qx.util.DeferredCall";
qx.Class.define(a,{extend:qx.core.Object,construct:function(b,c){qx.core.Object.call(this);
this.__bD=b;
this.__bE=c||null;
this.__eI=qx.util.DeferredCallManager.getInstance();
},members:{__bD:null,__bE:null,__eI:null,cancel:function(){this.__eI.cancel(this);
},schedule:function(){this.__eI.schedule(this);
},call:function(){var d;
this.__bE?this.__bD.apply(this.__bE):this.__bD();
}},destruct:function(){this.cancel();
this.__bE=this.__bD=this.__eI=null;
}});
})();
(function(){var m="element",k="qxSelectable",j="off",h="engine.name",g="on",f="text",d="div",c="",b="mshtml",a="none",F="scroll",E="qx.html.Element",D="|capture|",C="activate",B="blur",A="deactivate",z="capture",w="userSelect",v="-moz-none",u="visible",s="releaseCapture",t="|bubble|",q="__ff",r="tabIndex",o="focus",p="MozUserSelect",n="hidden";
qx.Class.define(E,{extend:qx.core.Object,construct:function(G,H,I){qx.core.Object.call(this);
this.__eJ=G||d;
this.__eK=H||null;
this.__eL=I||null;
},statics:{DEBUG:false,_modified:{},_visibility:{},_scroll:{},_actions:[],__eM:{},_scheduleFlush:function(J){qx.html.Element.__fq.schedule();
},flush:function(){var U;
var M=this.__eN();
var L=M.getFocus();

if(L&&this.__eR(L)){M.blur(L);
}var bc=M.getActive();

if(bc&&this.__eR(bc)){qx.bom.Element.deactivate(bc);
}var P=this.__eP();

if(P&&this.__eR(P)){qx.bom.Element.releaseCapture(P);
}var V=[];
var W=this._modified;

for(var T in W){U=W[T];
if(U.__fj()){if(U.__eS&&qx.dom.Hierarchy.isRendered(U.__eS)){V.push(U);
}else{U.__fi();
}delete W[T];
}}
for(var i=0,l=V.length;i<l;i++){U=V[i];
U.__fi();
}var R=this._visibility;

for(var T in R){U=R[T];
var X=U.__eS;

if(!X){delete R[T];
continue;
}if(!U.$$disposed){X.style.display=U.__eU?c:a;
if((qx.core.Environment.get(h)==b)){if(!(document.documentMode>=8)){X.style.visibility=U.__eU?u:n;
}}}delete R[T];
}var scroll=this._scroll;

for(var T in scroll){U=scroll[T];
var bd=U.__eS;

if(bd&&bd.offsetWidth){var O=true;
if(U.__eX!=null){U.__eS.scrollLeft=U.__eX;
delete U.__eX;
}if(U.__eY!=null){U.__eS.scrollTop=U.__eY;
delete U.__eY;
}var Y=U.__eV;

if(Y!=null){var S=Y.element.getDomElement();

if(S&&S.offsetWidth){qx.bom.element.Scroll.intoViewX(S,bd,Y.align);
delete U.__eV;
}else{O=false;
}}var ba=U.__eW;

if(ba!=null){var S=ba.element.getDomElement();

if(S&&S.offsetWidth){qx.bom.element.Scroll.intoViewY(S,bd,ba.align);
delete U.__eW;
}else{O=false;
}}if(O){delete scroll[T];
}}}var N={"releaseCapture":1,"blur":1,"deactivate":1};
for(var i=0;i<this._actions.length;i++){var bb=this._actions[i];
var X=bb.element.__eS;

if(!X||!N[bb.type]&&!bb.element.__fj()){continue;
}var Q=bb.args;
Q.unshift(X);
qx.bom.Element[bb.type].apply(qx.bom.Element,Q);
}this._actions=[];
for(var T in this.__eM){var K=this.__eM[T];
var bd=K.element.__eS;

if(bd){qx.bom.Selection.set(bd,K.start,K.end);
delete this.__eM[T];
}}qx.event.handler.Appear.refresh();
},__eN:function(){if(!this.__eO){var be=qx.event.Registration.getManager(window);
this.__eO=be.getHandler(qx.event.handler.Focus);
}return this.__eO;
},__eP:function(){if(!this.__eQ){var bf=qx.event.Registration.getManager(window);
this.__eQ=bf.getDispatcher(qx.event.dispatch.MouseCapture);
}return this.__eQ.getCaptureElement();
},__eR:function(bg){var bh=qx.core.ObjectRegistry.fromHashCode(bg.$$element);
return bh&&!bh.__fj();
}},members:{__eJ:null,__eS:null,__cX:false,__eT:true,__eU:true,__eV:null,__eW:null,__eX:null,__eY:null,__fa:null,__fb:null,__fc:null,__eK:null,__eL:null,__fd:null,__fe:null,__ff:null,__fg:null,__fh:null,_scheduleChildrenUpdate:function(){if(this.__fg){return;
}this.__fg=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
},_createDomElement:function(){return qx.bom.Element.create(this.__eJ);
},__fi:function(){var length;
var bi=this.__ff;

if(bi){length=bi.length;
var bj;

for(var i=0;i<length;i++){bj=bi[i];

if(bj.__eU&&bj.__eT&&!bj.__eS){bj.__fi();
}}}
if(!this.__eS){this.__eS=this._createDomElement();
this.__eS.$$element=this.$$hash;
this._copyData(false);

if(bi&&length>0){this._insertChildren();
}}else{this._syncData();

if(this.__fg){this._syncChildren();
}}delete this.__fg;
},_insertChildren:function(){var bk=this.__ff;
var length=bk.length;
var bm;

if(length>2){var bl=document.createDocumentFragment();

for(var i=0;i<length;i++){bm=bk[i];

if(bm.__eS&&bm.__eT){bl.appendChild(bm.__eS);
}}this.__eS.appendChild(bl);
}else{var bl=this.__eS;

for(var i=0;i<length;i++){bm=bk[i];

if(bm.__eS&&bm.__eT){bl.appendChild(bm.__eS);
}}}},_syncChildren:function(){var br;
var bw=qx.core.ObjectRegistry;
var bn=this.__ff;
var bu=bn.length;
var bo;
var bs;
var bq=this.__eS;
var bt=bq.childNodes;
var bp=0;
var bv;
for(var i=bt.length-1;i>=0;i--){bv=bt[i];
bs=bw.fromHashCode(bv.$$element);

if(!bs||!bs.__eT||bs.__fh!==this){bq.removeChild(bv);
}}for(var i=0;i<bu;i++){bo=bn[i];
if(bo.__eT){bs=bo.__eS;
bv=bt[bp];

if(!bs){continue;
}if(bs!=bv){if(bv){bq.insertBefore(bs,bv);
}else{bq.appendChild(bs);
}}bp++;
}}},_copyData:function(bx){var bB=this.__eS;
var bA=this.__eL;

if(bA){var by=qx.bom.element.Attribute;

for(var bC in bA){by.set(bB,bC,bA[bC]);
}}var bA=this.__eK;

if(bA){var bz=qx.bom.element.Style;

if(bx){bz.setStyles(bB,bA);
}else{bz.setCss(bB,bz.compile(bA));
}}var bA=this.__fd;

if(bA){for(var bC in bA){this._applyProperty(bC,bA[bC]);
}}var bA=this.__fe;

if(bA){qx.event.Registration.getManager(bB).importListeners(bB,bA);
delete this.__fe;
}},_syncData:function(){var bH=this.__eS;
var bG=qx.bom.element.Attribute;
var bE=qx.bom.element.Style;
var bF=this.__fb;

if(bF){var bK=this.__eL;

if(bK){var bI;

for(var bJ in bF){bI=bK[bJ];

if(bI!==undefined){bG.set(bH,bJ,bI);
}else{bG.reset(bH,bJ);
}}}this.__fb=null;
}var bF=this.__fa;

if(bF){var bK=this.__eK;

if(bK){var bD={};

for(var bJ in bF){bD[bJ]=bK[bJ];
}bE.setStyles(bH,bD);
}this.__fa=null;
}var bF=this.__fc;

if(bF){var bK=this.__fd;

if(bK){var bI;

for(var bJ in bF){this._applyProperty(bJ,bK[bJ]);
}}this.__fc=null;
}},__fj:function(){var bL=this;
while(bL){if(bL.__cX){return true;
}
if(!bL.__eT||!bL.__eU){return false;
}bL=bL.__fh;
}return false;
},__fk:function(bM){if(bM.__fh===this){throw new Error("Child is already in: "+bM);
}
if(bM.__cX){throw new Error("Root elements could not be inserted into other ones.");
}if(bM.__fh){bM.__fh.remove(bM);
}bM.__fh=this;
if(!this.__ff){this.__ff=[];
}if(this.__eS){this._scheduleChildrenUpdate();
}},__fl:function(bN){if(bN.__fh!==this){throw new Error("Has no child: "+bN);
}if(this.__eS){this._scheduleChildrenUpdate();
}delete bN.__fh;
},__fm:function(bO){if(bO.__fh!==this){throw new Error("Has no child: "+bO);
}if(this.__eS){this._scheduleChildrenUpdate();
}},getChildren:function(){return this.__ff||null;
},getChild:function(bP){var bQ=this.__ff;
return bQ&&bQ[bP]||null;
},hasChildren:function(){var bR=this.__ff;
return bR&&bR[0]!==undefined;
},indexOf:function(bS){var bT=this.__ff;
return bT?bT.indexOf(bS):-1;
},hasChild:function(bU){var bV=this.__ff;
return bV&&bV.indexOf(bU)!==-1;
},add:function(bW){if(arguments[1]){for(var i=0,l=arguments.length;i<l;i++){this.__fk(arguments[i]);
}this.__ff.push.apply(this.__ff,arguments);
}else{this.__fk(bW);
this.__ff.push(bW);
}return this;
},addAt:function(bX,bY){this.__fk(bX);
qx.lang.Array.insertAt(this.__ff,bX,bY);
return this;
},remove:function(ca){var cb=this.__ff;

if(!cb){return;
}
if(arguments[1]){var cc;

for(var i=0,l=arguments.length;i<l;i++){cc=arguments[i];
this.__fl(cc);
qx.lang.Array.remove(cb,cc);
}}else{this.__fl(ca);
qx.lang.Array.remove(cb,ca);
}return this;
},removeAt:function(cd){var ce=this.__ff;

if(!ce){throw new Error("Has no children!");
}var cf=ce[cd];

if(!cf){throw new Error("Has no child at this position!");
}this.__fl(cf);
qx.lang.Array.removeAt(this.__ff,cd);
return this;
},removeAll:function(){var cg=this.__ff;

if(cg){for(var i=0,l=cg.length;i<l;i++){this.__fl(cg[i]);
}cg.length=0;
}return this;
},getParent:function(){return this.__fh||null;
},insertInto:function(parent,ch){parent.__fk(this);

if(ch==null){parent.__ff.push(this);
}else{qx.lang.Array.insertAt(this.__ff,this,ch);
}return this;
},insertBefore:function(ci){var parent=ci.__fh;
parent.__fk(this);
qx.lang.Array.insertBefore(parent.__ff,this,ci);
return this;
},insertAfter:function(cj){var parent=cj.__fh;
parent.__fk(this);
qx.lang.Array.insertAfter(parent.__ff,this,cj);
return this;
},moveTo:function(ck){var parent=this.__fh;
parent.__fm(this);
var cl=parent.__ff.indexOf(this);

if(cl===ck){throw new Error("Could not move to same index!");
}else if(cl<ck){ck--;
}qx.lang.Array.removeAt(parent.__ff,cl);
qx.lang.Array.insertAt(parent.__ff,this,ck);
return this;
},moveBefore:function(cm){var parent=this.__fh;
return this.moveTo(parent.__ff.indexOf(cm));
},moveAfter:function(cn){var parent=this.__fh;
return this.moveTo(parent.__ff.indexOf(cn)+1);
},free:function(){var parent=this.__fh;

if(!parent){throw new Error("Has no parent to remove from.");
}
if(!parent.__ff){return;
}parent.__fl(this);
qx.lang.Array.remove(parent.__ff,this);
return this;
},getDomElement:function(){return this.__eS||null;
},getNodeName:function(){return this.__eJ;
},setNodeName:function(name){this.__eJ=name;
},setRoot:function(co){this.__cX=co;
},useMarkup:function(cp){if(this.__eS){throw new Error("Could not overwrite existing element!");
}if((qx.core.Environment.get(h)==b)){var cq=document.createElement(d);
}else{var cq=qx.bom.Element.getHelperElement();
}cq.innerHTML=cp;
this.useElement(cq.firstChild);
return this.__eS;
},useElement:function(cr){if(this.__eS){throw new Error("Could not overwrite existing element!");
}this.__eS=cr;
this.__eS.$$element=this.$$hash;
this._copyData(true);
},isFocusable:function(){var ct=this.getAttribute(r);

if(ct>=1){return true;
}var cs=qx.event.handler.Focus.FOCUSABLE_ELEMENTS;

if(ct>=0&&cs[this.__eJ]){return true;
}return false;
},setSelectable:qx.core.Environment.select(h,{"webkit":function(cu){this.setAttribute(k,cu?g:j);
this.setStyle(w,cu?f:a);
},"gecko":function(cv){this.setAttribute(k,cv?g:j);
this.setStyle(p,cv?f:v);
},"default":function(cw){this.setAttribute(k,cw?g:j);
}}),isNativelyFocusable:function(){return !!qx.event.handler.Focus.FOCUSABLE_ELEMENTS[this.__eJ];
},include:function(){if(this.__eT){return;
}delete this.__eT;

if(this.__fh){this.__fh._scheduleChildrenUpdate();
}return this;
},exclude:function(){if(!this.__eT){return;
}this.__eT=false;

if(this.__fh){this.__fh._scheduleChildrenUpdate();
}return this;
},isIncluded:function(){return this.__eT===true;
},show:function(){if(this.__eU){return;
}
if(this.__eS){qx.html.Element._visibility[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}if(this.__fh){this.__fh._scheduleChildrenUpdate();
}delete this.__eU;
},hide:function(){if(!this.__eU){return;
}
if(this.__eS){qx.html.Element._visibility[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}this.__eU=false;
},isVisible:function(){return this.__eU===true;
},scrollChildIntoViewX:function(cx,cy,cz){var cA=this.__eS;
var cB=cx.getDomElement();

if(cz!==false&&cA&&cA.offsetWidth&&cB&&cB.offsetWidth){qx.bom.element.Scroll.intoViewX(cB,cA,cy);
}else{this.__eV={element:cx,align:cy};
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__eX;
},scrollChildIntoViewY:function(cC,cD,cE){var cF=this.__eS;
var cG=cC.getDomElement();

if(cE!==false&&cF&&cF.offsetWidth&&cG&&cG.offsetWidth){qx.bom.element.Scroll.intoViewY(cG,cF,cD);
}else{this.__eW={element:cC,align:cD};
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__eY;
},scrollToX:function(x,cH){var cI=this.__eS;

if(cH!==true&&cI&&cI.offsetWidth){cI.scrollLeft=x;
delete this.__eX;
}else{this.__eX=x;
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__eV;
},getScrollX:function(){var cJ=this.__eS;

if(cJ){return cJ.scrollLeft;
}return this.__eX||0;
},scrollToY:function(y,cK){var cL=this.__eS;

if(cK!==true&&cL&&cL.offsetWidth){cL.scrollTop=y;
delete this.__eY;
}else{this.__eY=y;
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__eW;
},getScrollY:function(){var cM=this.__eS;

if(cM){return cM.scrollTop;
}return this.__eY||0;
},disableScrolling:function(){this.enableScrolling();
this.scrollToX(0);
this.scrollToY(0);
this.addListener(F,this.__fo,this);
},enableScrolling:function(){this.removeListener(F,this.__fo,this);
},__fn:null,__fo:function(e){if(!this.__fn){this.__fn=true;
this.__eS.scrollTop=0;
this.__eS.scrollLeft=0;
delete this.__fn;
}},getTextSelection:function(){var cN=this.__eS;

if(cN){return qx.bom.Selection.get(cN);
}return null;
},getTextSelectionLength:function(){var cO=this.__eS;

if(cO){return qx.bom.Selection.getLength(cO);
}return null;
},getTextSelectionStart:function(){var cP=this.__eS;

if(cP){return qx.bom.Selection.getStart(cP);
}return null;
},getTextSelectionEnd:function(){var cQ=this.__eS;

if(cQ){return qx.bom.Selection.getEnd(cQ);
}return null;
},setTextSelection:function(cR,cS){var cT=this.__eS;

if(cT){qx.bom.Selection.set(cT,cR,cS);
return;
}qx.html.Element.__eM[this.toHashCode()]={element:this,start:cR,end:cS};
qx.html.Element._scheduleFlush(m);
},clearTextSelection:function(){var cU=this.__eS;

if(cU){qx.bom.Selection.clear(cU);
}delete qx.html.Element.__eM[this.toHashCode()];
},__fp:function(cV,cW){var cX=qx.html.Element._actions;
cX.push({type:cV,element:this,args:cW||[]});
qx.html.Element._scheduleFlush(m);
},focus:function(){this.__fp(o);
},blur:function(){this.__fp(B);
},activate:function(){this.__fp(C);
},deactivate:function(){this.__fp(A);
},capture:function(cY){this.__fp(z,[cY!==false]);
},releaseCapture:function(){this.__fp(s);
},setStyle:function(da,dc,dd){if(!this.__eK){this.__eK={};
}
if(this.__eK[da]==dc){return;
}
if(dc==null){delete this.__eK[da];
}else{this.__eK[da]=dc;
}if(this.__eS){if(dd){qx.bom.element.Style.set(this.__eS,da,dc);
return this;
}if(!this.__fa){this.__fa={};
}this.__fa[da]=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}return this;
},setStyles:function(de,df){var dg=qx.bom.element.Style;

if(!this.__eK){this.__eK={};
}
if(this.__eS){if(!this.__fa){this.__fa={};
}
for(var di in de){var dh=de[di];

if(this.__eK[di]==dh){continue;
}
if(dh==null){delete this.__eK[di];
}else{this.__eK[di]=dh;
}if(df){dg.set(this.__eS,di,dh);
continue;
}this.__fa[di]=true;
}qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}else{for(var di in de){var dh=de[di];

if(this.__eK[di]==dh){continue;
}
if(dh==null){delete this.__eK[di];
}else{this.__eK[di]=dh;
}}}return this;
},removeStyle:function(dj,dk){this.setStyle(dj,null,dk);
},getStyle:function(dl){return this.__eK?this.__eK[dl]:null;
},getAllStyles:function(){return this.__eK||null;
},setAttribute:function(dm,dn,dp){if(!this.__eL){this.__eL={};
}
if(this.__eL[dm]==dn){return;
}
if(dn==null){delete this.__eL[dm];
}else{this.__eL[dm]=dn;
}if(this.__eS){if(dp){qx.bom.element.Attribute.set(this.__eS,dm,dn);
return this;
}if(!this.__fb){this.__fb={};
}this.__fb[dm]=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}return this;
},setAttributes:function(dq,dr){for(var ds in dq){this.setAttribute(ds,dq[ds],dr);
}return this;
},removeAttribute:function(dt,du){this.setAttribute(dt,null,du);
},getAttribute:function(dv){return this.__eL?this.__eL[dv]:null;
},_applyProperty:function(name,dw){},_setProperty:function(dx,dy,dz){if(!this.__fd){this.__fd={};
}
if(this.__fd[dx]==dy){return;
}
if(dy==null){delete this.__fd[dx];
}else{this.__fd[dx]=dy;
}if(this.__eS){if(dz){this._applyProperty(dx,dy);
return this;
}if(!this.__fc){this.__fc={};
}this.__fc[dx]=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}return this;
},_removeProperty:function(dA,dB){this._setProperty(dA,null,dB);
},_getProperty:function(dC){var dD=this.__fd;

if(!dD){return null;
}var dE=dD[dC];
return dE==null?null:dE;
},addListener:function(dF,dG,self,dH){var dI;

if(this.$$disposed){return null;
}
if(this.__eS){return qx.event.Registration.addListener(this.__eS,dF,dG,self,dH);
}
if(!this.__fe){this.__fe={};
}
if(dH==null){dH=false;
}var dJ=qx.event.Manager.getNextUniqueId();
var dK=dF+(dH?D:t)+dJ;
this.__fe[dK]={type:dF,listener:dG,self:self,capture:dH,unique:dJ};
return dK;
},removeListener:function(dL,dM,self,dN){var dO;

if(this.$$disposed){return null;
}
if(this.__eS){qx.event.Registration.removeListener(this.__eS,dL,dM,self,dN);
}else{var dQ=this.__fe;
var dP;

if(dN==null){dN=false;
}
for(var dR in dQ){dP=dQ[dR];
if(dP.listener===dM&&dP.self===self&&dP.capture===dN&&dP.type===dL){delete dQ[dR];
break;
}}}return this;
},removeListenerById:function(dS){if(this.$$disposed){return null;
}
if(this.__eS){qx.event.Registration.removeListenerById(this.__eS,dS);
}else{delete this.__fe[dS];
}return this;
},hasListener:function(dT,dU){if(this.$$disposed){return false;
}
if(this.__eS){return qx.event.Registration.hasListener(this.__eS,dT,dU);
}var dW=this.__fe;
var dV;

if(dU==null){dU=false;
}
for(var dX in dW){dV=dW[dX];
if(dV.capture===dU&&dV.type===dT){return true;
}}return false;
}},defer:function(dY){dY.__fq=new qx.util.DeferredCall(dY.flush,dY);
},destruct:function(){var ea=this.__eS;

if(ea){qx.event.Registration.getManager(ea).removeAllListeners(ea);
ea.$$element=c;
}
if(!qx.core.ObjectRegistry.inShutDown){var parent=this.__fh;

if(parent&&!parent.$$disposed){parent.remove(this);
}}this._disposeArray(q);
this.__eL=this.__eK=this.__fe=this.__fd=this.__fb=this.__fa=this.__fc=this.__eS=this.__fh=this.__eV=this.__eW=null;
}});
})();
(function(){var e="orientationchange",d="resize",c="landscape",b="portrait",a="qx.event.handler.Orientation";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(f){qx.core.Object.call(this);
this.__eI=f;
this.__cf=f.getWindow();
this._initObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{orientationchange:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{__eI:null,__cf:null,__fr:null,__fs:null,__ft:null,canHandleEvent:function(g,h){},registerEvent:function(i,j,k){},unregisterEvent:function(l,m,n){},_initObserver:function(){this.__ft=qx.lang.Function.listener(this._onNative,this);
this.__fr=qx.bom.Event.supportsEvent(this.__cf,e)?e:d;
var Event=qx.bom.Event;
Event.addNativeListener(this.__cf,this.__fr,this.__ft);
},_stopObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__cf,this.__fr,this.__ft);
},_onNative:qx.event.GlobalError.observeMethod(function(o){var q=qx.bom.Viewport;
var p=q.getOrientation();

if(this.__fs!=p){this.__fs=p;
var r=q.isLandscape()?c:b;
qx.event.Registration.fireEvent(this.__cf,e,qx.event.type.Orientation,[p,r]);
}})},destruct:function(){this._stopObserver();
this.__eI=this.__cf=null;
},defer:function(s){qx.event.Registration.addHandler(s);
}});
})();
(function(){var c="landscape",b="qx.event.type.Orientation",a="portrait";
qx.Class.define(b,{extend:qx.event.type.Event,members:{__fu:null,__fv:null,init:function(d,e){qx.event.type.Event.prototype.init.call(this,false,false);
this.__fu=d;
this.__fv=e;
return this;
},clone:function(f){var g=qx.event.type.Event.prototype.clone.call(this,f);
g.__fu=this.__fu;
g.__fv=this.__fv;
return g;
},getOrientation:function(){return this.__fu;
},isLandscape:function(){return this.__fv==c;
},isPortrait:function(){return this.__fv==a;
}}});
})();
(function(){var a="qx.event.handler.UserAction";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(b){qx.core.Object.call(this);
this.__eI=b;
this.__cf=b.getWindow();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{useraction:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{__eI:null,__cf:null,canHandleEvent:function(c,d){},registerEvent:function(e,f,g){},unregisterEvent:function(h,i,j){}},destruct:function(){this.__eI=this.__cf=null;
},defer:function(k){qx.event.Registration.addHandler(k);
}});
})();
(function(){var t="qx.mobile.emulatetouch",s="touchend",r="touchstart",q="touchmove",p="event.touch",o="mousemove",n="engine.name",m="touchcancel",l="mouseup",k="mousedown",d="mshtml",j="qx.event.handler.Touch",h="useraction",c="swipe",b="qx.mobile.nativescroll",g="webkit",f="tap",i="x",a="y";
qx.Class.define(j,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(u){qx.core.Object.call(this);
this.__eI=u;
this.__cf=u.getWindow();
this.__cX=this.__cf.document;
this._initTouchObserver();
this._initMouseObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{touchstart:1,touchmove:1,touchend:1,touchcancel:1,tap:1,swipe:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE+qx.event.IEventHandler.TARGET_DOCUMENT,IGNORE_CAN_HANDLE:true,MOUSE_TO_TOUCH_MAPPING:{"mousedown":"touchstart","mousemove":"touchmove","mouseup":"touchend"},SWIPE_DIRECTION:{x:["left","right"],y:["up","down"]},TAP_MAX_DISTANCE:qx.core.Environment.get("os.name")!="android"?10:40,SWIPE_MIN_DISTANCE:qx.core.Environment.get("os.name")!="android"?11:41,SWIPE_MIN_VELOCITY:0},members:{__fw:null,__fx:null,__eI:null,__cf:null,__cX:null,__fy:null,__fz:null,__fA:null,__fB:null,__fC:false,__fD:null,canHandleEvent:function(v,w){},registerEvent:function(x,y,z){},unregisterEvent:function(A,B,C){},__fE:function(D){var E=qx.bom.Event.getTarget(D);
if((qx.core.Environment.get(n)==g)){if(E&&E.nodeType==3){E=E.parentNode;
}}return E;
},__fF:function(F,G,H,I){if(!H){H=this.__fE(F);
}var G=G||F.type;

if(H&&H.nodeType){qx.event.Registration.fireEvent(H,G,I||qx.event.type.Touch,[F,H,null,true,true]);
}qx.event.Registration.fireEvent(this.__cf,h,qx.event.type.Data,[G]);
},__fG:function(J,K,L){if(!L){L=this.__fE(J);
}var K=K||J.type;

if(K==r){this.__fH(J,L);
}else if(K==q){this.__fI(J,L);
}else if(K==s){this.__fJ(J,L);
}},__fH:function(M,N){var O=M.changedTouches[0];
this.__fy=O.screenX;
this.__fz=O.screenY;
this.__fA=new Date().getTime();
this.__fB=M.changedTouches.length===1;
},__fI:function(P,Q){if(this.__fB&&P.changedTouches.length>1){this.__fB=false;
}},__fJ:function(R,S){if(this.__fB){var T=R.changedTouches[0];
var V={x:T.screenX-this.__fy,y:T.screenY-this.__fz};
var W=qx.event.handler.Touch;

if(this.__fD==S&&Math.abs(V.x)<=W.TAP_MAX_DISTANCE&&Math.abs(V.y)<=W.TAP_MAX_DISTANCE){this.__fF(R,f,S,qx.event.type.Tap);
}else{var U=this.__fK(R,S,V);

if(U){R.swipe=U;
this.__fF(R,c,S,qx.event.type.Swipe);
}}}},__fK:function(X,Y,ba){var be=qx.event.handler.Touch;
var bf=new Date().getTime()-this.__fA;
var bh=(Math.abs(ba.x)>=Math.abs(ba.y))?i:a;
var bb=ba[bh];
var bc=be.SWIPE_DIRECTION[bh][bb<0?0:1];
var bg=(bf!==0)?bb/bf:0;
var bd=null;

if(Math.abs(bg)>=be.SWIPE_MIN_VELOCITY&&Math.abs(bb)>=be.SWIPE_MIN_DISTANCE){bd={startTime:this.__fA,duration:bf,axis:bh,direction:bc,distance:bb,velocity:bg};
}return bd;
},__fL:qx.core.Environment.select(t,{"true":function(bi){var bj=bi.type;
var bl=qx.event.handler.Touch.MOUSE_TO_TOUCH_MAPPING;

if(bl[bj]){bj=bl[bj];
if(bj==r&&this.__fM(bi)){this.__fC=true;
}else if(bj==s){this.__fC=false;
}var bm=this.__fN(bi);
var bk=(bj==s?[]:[bm]);
bi.touches=bk;
bi.targetTouches=bk;
bi.changedTouches=[bm];
}return bj;
},"default":qx.lang.Function.empty}),__fM:qx.core.Environment.select(t,{"true":function(bn){if((qx.core.Environment.get(n)==d)){var bo=1;
}else{var bo=0;
}return bn.button==bo;
},"default":qx.lang.Function.empty}),__fN:qx.core.Environment.select(t,{"true":function(bp){var bq=this.__fE(bp);
return {clientX:bp.clientX,clientY:bp.clientY,screenX:bp.screenX,screenY:bp.screenY,pageX:bp.pageX,pageY:bp.pageY,identifier:1,target:bq};
},"default":qx.lang.Function.empty}),_initTouchObserver:function(){this.__fw=qx.lang.Function.listener(this._onTouchEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__cX,r,this.__fw);
Event.addNativeListener(this.__cX,q,this.__fw);
Event.addNativeListener(this.__cX,s,this.__fw);
Event.addNativeListener(this.__cX,m,this.__fw);
},_initMouseObserver:qx.core.Environment.select(t,{"true":function(){if(!qx.core.Environment.get(p)){this.__fx=qx.lang.Function.listener(this._onMouseEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__cX,k,this.__fx);
Event.addNativeListener(this.__cX,o,this.__fx);
Event.addNativeListener(this.__cX,l,this.__fx);
}},"default":qx.lang.Function.empty}),_stopTouchObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__cX,r,this.__fw);
Event.removeNativeListener(this.__cX,q,this.__fw);
Event.removeNativeListener(this.__cX,s,this.__fw);
Event.removeNativeListener(this.__cX,m,this.__fw);
},_stopMouseObserver:qx.core.Environment.select(t,{"true":function(){if(!qx.core.Environment.get(p)){var Event=qx.bom.Event;
Event.removeNativeListener(this.__cX,k,this.__fx);
Event.removeNativeListener(this.__cX,o,this.__fx);
Event.removeNativeListener(this.__cX,l,this.__fx);
}},"default":qx.lang.Function.empty}),_onTouchEvent:qx.event.GlobalError.observeMethod(function(br){this._commonTouchEventHandler(br);
}),_onMouseEvent:qx.core.Environment.select(t,{"true":qx.event.GlobalError.observeMethod(function(bs){if(!qx.core.Environment.get(p)){if(bs.type==o&&!this.__fC){return;
}var bt=this.__fL(bs);
this._commonTouchEventHandler(bs,bt);
}}),"default":qx.lang.Function.empty}),_commonTouchEventHandler:function(bu,bv){var bv=bv||bu.type;

if(bv==r){this.__fD=this.__fE(bu);
}this.__fF(bu,bv);
this.__fG(bu,bv);
}},destruct:function(){this._stopTouchObserver();
this._stopMouseObserver();
this.__eI=this.__cf=this.__cX=this.__fD=null;
},defer:function(bw){qx.event.Registration.addHandler(bw);
if(qx.core.Environment.get(p)){if(qx.core.Environment.get(b)==false){document.addEventListener(q,function(e){e.preventDefault();
});
}qx.event.Registration.getManager(document).getHandler(bw);
}}});
})();
(function(){var c="os.name",b="qx.event.type.Dom",a="osx";
qx.Class.define(b,{extend:qx.event.type.Native,statics:{SHIFT_MASK:1,CTRL_MASK:2,ALT_MASK:4,META_MASK:8},members:{_cloneNativeEvent:function(d,e){var e=qx.event.type.Native.prototype._cloneNativeEvent.call(this,d,e);
e.shiftKey=d.shiftKey;
e.ctrlKey=d.ctrlKey;
e.altKey=d.altKey;
e.metaKey=d.metaKey;
return e;
},getModifiers:function(){var g=0;
var f=this._native;

if(f.shiftKey){g|=qx.event.type.Dom.SHIFT_MASK;
}
if(f.ctrlKey){g|=qx.event.type.Dom.CTRL_MASK;
}
if(f.altKey){g|=qx.event.type.Dom.ALT_MASK;
}
if(f.metaKey){g|=qx.event.type.Dom.META_MASK;
}return g;
},isCtrlPressed:function(){return this._native.ctrlKey;
},isShiftPressed:function(){return this._native.shiftKey;
},isAltPressed:function(){return this._native.altKey;
},isMetaPressed:function(){return this._native.metaKey;
},isCtrlOrCommandPressed:function(){if(qx.core.Environment.get(c)==a){return this._native.metaKey;
}else{return this._native.ctrlKey;
}}}});
})();
(function(){var c="touchcancel",b="qx.event.type.Touch",a="touchend";
qx.Class.define(b,{extend:qx.event.type.Dom,members:{_cloneNativeEvent:function(d,e){var e=qx.event.type.Dom.prototype._cloneNativeEvent.call(this,d,e);
e.pageX=d.pageX;
e.pageY=d.pageY;
e.layerX=d.layerX;
e.layerY=d.layerY;
e.scale=d.scale;
e.rotation=d.rotation;
e.srcElement=d.srcElement;
e.targetTouches=[];

for(var i=0;i<d.targetTouches.length;i++){e.targetTouches[i]=d.targetTouches[i];
}e.changedTouches=[];

for(var i=0;i<d.changedTouches.length;i++){e.changedTouches[i]=d.changedTouches[i];
}e.touches=[];

for(var i=0;i<d.touches.length;i++){e.touches[i]=d.touches[i];
}return e;
},stop:function(){this.stopPropagation();
},getAllTouches:function(){return this._native.touches;
},getTargetTouches:function(){return this._native.targetTouches;
},getChangedTargetTouches:function(){return this._native.changedTouches;
},isMultiTouch:function(){return this.__fP().length>1;
},getScale:function(){return this._native.scale;
},getRotation:function(){return this._native.rotation;
},getDocumentLeft:function(f){return this.__fO(f).pageX;
},getDocumentTop:function(g){return this.__fO(g).pageY;
},getScreenLeft:function(h){return this.__fO(h).screenX;
},getScreenTop:function(j){return this.__fO(j).screenY;
},getViewportLeft:function(k){return this.__fO(k).clientX;
},getViewportTop:function(l){return this.__fO(l).clientY;
},getIdentifier:function(m){return this.__fO(m).identifier;
},__fO:function(n){n=n==null?0:n;
return this.__fP()[n];
},__fP:function(){var o=(this._isTouchEnd()?this.getChangedTargetTouches():this.getTargetTouches());
return o;
},_isTouchEnd:function(){return (this.getType()==a||this.getType()==c);
}}});
})();
(function(){var a="qx.event.type.Tap";
qx.Class.define(a,{extend:qx.event.type.Touch,members:{_isTouchEnd:function(){return true;
}}});
})();
(function(){var a="qx.event.type.Swipe";
qx.Class.define(a,{extend:qx.event.type.Touch,members:{_cloneNativeEvent:function(b,c){var c=qx.event.type.Touch.prototype._cloneNativeEvent.call(this,b,c);
c.swipe=b.swipe;
return c;
},_isTouchEnd:function(){return true;
},getStartTime:function(){return this._native.swipe.startTime;
},getDuration:function(){return this._native.swipe.duration;
},getAxis:function(){return this._native.swipe.axis;
},getDirection:function(){return this._native.swipe.direction;
},getVelocity:function(){return this._native.swipe.velocity;
},getDistance:function(){return this._native.swipe.distance;
}}});
})();
(function(){var c="qx.event.handler.Appear",b="disappear",a="appear";
qx.Class.define(c,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(d){qx.core.Object.call(this);
this.__eI=d;
this.__fQ={};
qx.event.handler.Appear.__fR[this.$$hash]=this;
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{appear:true,disappear:true},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:true,__fR:{},refresh:function(){var e=this.__fR;

for(var f in e){e[f].refresh();
}}},members:{__eI:null,__fQ:null,canHandleEvent:function(g,h){},registerEvent:function(i,j,k){var l=qx.core.ObjectRegistry.toHashCode(i)+j;
var m=this.__fQ;

if(m&&!m[l]){m[l]=i;
i.$$displayed=i.offsetWidth>0;
}},unregisterEvent:function(n,o,p){var q=qx.core.ObjectRegistry.toHashCode(n)+o;
var r=this.__fQ;

if(!r){return;
}
if(r[q]){delete r[q];
}},refresh:function(){var v=this.__fQ;
var w;

for(var u in v){w=v[u];
var s=w.offsetWidth>0;

if((!!w.$$displayed)!==s){w.$$displayed=s;
var t=qx.event.Registration.createEvent(s?a:b);
this.__eI.dispatchEvent(w,t);
}}}},destruct:function(){this.__eI=this.__fQ=null;
delete qx.event.handler.Appear.__fR[this.$$hash];
},defer:function(x){qx.event.Registration.addHandler(x);
}});
})();
(function(){var b="abstract",a="qx.event.dispatch.AbstractBubbling";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventDispatcher,type:b,construct:function(c){this._manager=c;
},members:{_getParent:function(d){throw new Error("Missing implementation");
},canDispatchEvent:function(e,event,f){return event.getBubbles();
},dispatchEvent:function(g,event,h){var parent=g;
var s=this._manager;
var p,w;
var n;
var r,u;
var t;
var v=[];
p=s.getListeners(g,h,true);
w=s.getListeners(g,h,false);

if(p){v.push(p);
}
if(w){v.push(w);
}var parent=this._getParent(g);
var l=[];
var k=[];
var m=[];
var q=[];
while(parent!=null){p=s.getListeners(parent,h,true);

if(p){m.push(p);
q.push(parent);
}w=s.getListeners(parent,h,false);

if(w){l.push(w);
k.push(parent);
}parent=this._getParent(parent);
}event.setEventPhase(qx.event.type.Event.CAPTURING_PHASE);

for(var i=m.length-1;i>=0;i--){t=q[i];
event.setCurrentTarget(t);
n=m[i];

for(var j=0,o=n.length;j<o;j++){r=n[j];
u=r.context||t;
r.handler.call(u,event);
}
if(event.getPropagationStopped()){return;
}}event.setEventPhase(qx.event.type.Event.AT_TARGET);
event.setCurrentTarget(g);

for(var i=0,x=v.length;i<x;i++){n=v[i];

for(var j=0,o=n.length;j<o;j++){r=n[j];
u=r.context||g;
r.handler.call(u,event);
}
if(event.getPropagationStopped()){return;
}}event.setEventPhase(qx.event.type.Event.BUBBLING_PHASE);

for(var i=0,x=l.length;i<x;i++){t=k[i];
event.setCurrentTarget(t);
n=l[i];

for(var j=0,o=n.length;j<o;j++){r=n[j];
u=r.context||t;
r.handler.call(u,event);
}
if(event.getPropagationStopped()){return;
}}}}});
})();
(function(){var a="qx.event.dispatch.DomBubbling";
qx.Class.define(a,{extend:qx.event.dispatch.AbstractBubbling,statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL},members:{_getParent:function(b){return b.parentNode;
},canDispatchEvent:function(c,event,d){return c.nodeType!==undefined&&event.getBubbles();
}},defer:function(e){qx.event.Registration.addDispatcher(e);
}});
})();
(function(){var d="-",c="qx.event.handler.Element",b="load",a="iframe";
qx.Class.define(c,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(e){qx.core.Object.call(this);
this._manager=e;
this._registeredEvents={};
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{abort:true,load:true,scroll:true,select:true,reset:true,submit:true},CANCELABLE:{selectstart:true},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:false},members:{canHandleEvent:function(f,g){if(g===b){return f.tagName.toLowerCase()!==a;
}else{return true;
}},registerEvent:function(h,i,j){var m=qx.core.ObjectRegistry.toHashCode(h);
var k=m+d+i;
var l=qx.lang.Function.listener(this._onNative,this,k);
qx.bom.Event.addNativeListener(h,i,l);
this._registeredEvents[k]={element:h,type:i,listener:l};
},unregisterEvent:function(n,o,p){var s=this._registeredEvents;

if(!s){return;
}var t=qx.core.ObjectRegistry.toHashCode(n);
var q=t+d+o;
var r=this._registeredEvents[q];

if(r){qx.bom.Event.removeNativeListener(n,o,r.listener);
}delete this._registeredEvents[q];
},_onNative:qx.event.GlobalError.observeMethod(function(u,v){var x=this._registeredEvents;

if(!x){return;
}var w=x[v];
var y=this.constructor.CANCELABLE[w.type];
qx.event.Registration.fireNonBubblingEvent(w.element,w.type,qx.event.type.Native,[u,undefined,undefined,undefined,y]);
})},destruct:function(){var z;
var A=this._registeredEvents;

for(var B in A){z=A[B];
qx.bom.Event.removeNativeListener(z.element,z.type,z.listener);
}this._manager=this._registeredEvents=null;
},defer:function(C){qx.event.Registration.addHandler(C);
}});
})();
(function(){var t="mouseup",s="engine.name",r="click",q="mousedown",p="contextmenu",o="mousewheel",n="dblclick",m="os.name",l="mouseover",k="mouseout",d="ios",j="mousemove",g="on",c="engine.version",b="useraction",f="webkit",e="gecko",h="DOMMouseScroll",a="qx.event.handler.Mouse";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(u){qx.core.Object.call(this);
this.__eI=u;
this.__cf=u.getWindow();
this.__cX=this.__cf.document;
this._initButtonObserver();
this._initMoveObserver();
this._initWheelObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{mousemove:1,mouseover:1,mouseout:1,mousedown:1,mouseup:1,click:1,dblclick:1,contextmenu:1,mousewheel:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE+qx.event.IEventHandler.TARGET_DOCUMENT+qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{__fS:null,__fT:null,__fU:null,__fV:null,__fW:null,__eI:null,__cf:null,__cX:null,canHandleEvent:function(v,w){},registerEvent:qx.core.Environment.get(m)===d?function(x,y,z){x[g+y]=qx.lang.Function.returnNull;
}:qx.lang.Function.returnNull,unregisterEvent:qx.core.Environment.get(m)===d?function(A,B,C){A[g+B]=undefined;
}:qx.lang.Function.returnNull,__fF:function(D,E,F){if(!F){F=qx.bom.Event.getTarget(D);
}if(F&&F.nodeType){qx.event.Registration.fireEvent(F,E||D.type,E==o?qx.event.type.MouseWheel:qx.event.type.Mouse,[D,F,null,true,true]);
}qx.event.Registration.fireEvent(this.__cf,b,qx.event.type.Data,[E||D.type]);
},__fX:function(){var H=[this.__cf,this.__cX,this.__cX.body];
var I=this.__cf;
var G=h;

for(var i=0;i<H.length;i++){if(qx.bom.Event.supportsEvent(H[i],o)){G=o;
I=H[i];
break;
}}return {type:G,target:I};
},_initButtonObserver:function(){this.__fS=qx.lang.Function.listener(this._onButtonEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__cX,q,this.__fS);
Event.addNativeListener(this.__cX,t,this.__fS);
Event.addNativeListener(this.__cX,r,this.__fS);
Event.addNativeListener(this.__cX,n,this.__fS);
Event.addNativeListener(this.__cX,p,this.__fS);
},_initMoveObserver:function(){this.__fT=qx.lang.Function.listener(this._onMoveEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__cX,j,this.__fT);
Event.addNativeListener(this.__cX,l,this.__fT);
Event.addNativeListener(this.__cX,k,this.__fT);
},_initWheelObserver:function(){this.__fU=qx.lang.Function.listener(this._onWheelEvent,this);
var J=this.__fX();
qx.bom.Event.addNativeListener(J.target,J.type,this.__fU);
},_stopButtonObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__cX,q,this.__fS);
Event.removeNativeListener(this.__cX,t,this.__fS);
Event.removeNativeListener(this.__cX,r,this.__fS);
Event.removeNativeListener(this.__cX,n,this.__fS);
Event.removeNativeListener(this.__cX,p,this.__fS);
},_stopMoveObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__cX,j,this.__fT);
Event.removeNativeListener(this.__cX,l,this.__fT);
Event.removeNativeListener(this.__cX,k,this.__fT);
},_stopWheelObserver:function(){var K=this.__fX();
qx.bom.Event.removeNativeListener(K.target,K.type,this.__fU);
},_onMoveEvent:qx.event.GlobalError.observeMethod(function(L){this.__fF(L);
}),_onButtonEvent:qx.event.GlobalError.observeMethod(function(M){var N=M.type;
var O=qx.bom.Event.getTarget(M);
if(qx.core.Environment.get(s)==e||qx.core.Environment.get(s)==f){if(O&&O.nodeType==3){O=O.parentNode;
}}
if(this.__fY){this.__fY(M,N,O);
}
if(this.__gb){this.__gb(M,N,O);
}this.__fF(M,N,O);

if(this.__ga){this.__ga(M,N,O);
}
if(this.__gc){this.__gc(M,N,O);
}this.__fV=N;
}),_onWheelEvent:qx.event.GlobalError.observeMethod(function(P){this.__fF(P,o);
}),__fY:qx.core.Environment.select(s,{"webkit":function(Q,R,S){if(parseFloat(qx.core.Environment.get(c))<530){if(R==p){this.__fF(Q,t,S);
}}},"default":null}),__ga:qx.core.Environment.select(s,{"opera":function(T,U,V){if(U==t&&T.button==2){this.__fF(T,p,V);
}},"default":null}),__gb:qx.core.Environment.select(s,{"mshtml":function(W,X,Y){if(W.target!==undefined){return;
}
if(X==t&&this.__fV==r){this.__fF(W,q,Y);
}else if(X==n){this.__fF(W,r,Y);
}},"default":null}),__gc:qx.core.Environment.select(s,{"mshtml":null,"default":function(ba,bb,bc){switch(bb){case q:this.__fW=bc;
break;
case t:if(bc!==this.__fW){var bd=qx.dom.Hierarchy.getCommonParent(bc,this.__fW);
this.__fF(ba,r,bd);
}}}})},destruct:function(){this._stopButtonObserver();
this._stopMoveObserver();
this._stopWheelObserver();
this.__eI=this.__cf=this.__cX=this.__fW=null;
},defer:function(be){qx.event.Registration.addHandler(be);
}});
})();
(function(){var j="left",i="right",h="middle",g="none",f="click",e="contextmenu",d="qx.event.type.Mouse",c="browser.documentmode",b="browser.name",a="ie";
qx.Class.define(d,{extend:qx.event.type.Dom,members:{_cloneNativeEvent:function(k,l){var l=qx.event.type.Dom.prototype._cloneNativeEvent.call(this,k,l);
l.button=k.button;
l.clientX=k.clientX;
l.clientY=k.clientY;
l.pageX=k.pageX;
l.pageY=k.pageY;
l.screenX=k.screenX;
l.screenY=k.screenY;
l.wheelDelta=k.wheelDelta;
l.wheelDeltaX=k.wheelDeltaX;
l.wheelDeltaY=k.wheelDeltaY;
l.detail=k.detail;
l.axis=k.axis;
l.wheelX=k.wheelX;
l.wheelY=k.wheelY;
l.HORIZONTAL_AXIS=k.HORIZONTAL_AXIS;
l.srcElement=k.srcElement;
l.target=k.target;
return l;
},__gd:{0:j,2:i,1:h},__ge:{1:j,2:i,4:h},stop:function(){this.stopPropagation();
},getButton:function(){switch(this._type){case e:return i;
case f:if(qx.core.Environment.get(b)===a&&qx.core.Environment.get(c)<9){return j;
}default:if(this._native.target!==undefined){return this.__gd[this._native.button]||g;
}else{return this.__ge[this._native.button]||g;
}}},isLeftPressed:function(){return this.getButton()===j;
},isMiddlePressed:function(){return this.getButton()===h;
},isRightPressed:function(){return this.getButton()===i;
},getRelatedTarget:function(){return this._relatedTarget;
},getViewportLeft:function(){return this._native.clientX;
},getViewportTop:function(){return this._native.clientY;
},getDocumentLeft:function(){if(this._native.pageX!==undefined){return this._native.pageX;
}else{var m=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientX+qx.bom.Viewport.getScrollLeft(m);
}},getDocumentTop:function(){if(this._native.pageY!==undefined){return this._native.pageY;
}else{var n=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientY+qx.bom.Viewport.getScrollTop(n);
}},getScreenLeft:function(){return this._native.screenX;
},getScreenTop:function(){return this._native.screenY;
}}});
})();
(function(){var l="engine.version",k="os.name",j="engine.name",i="x",h="osx",g="win",f="qx.dynamicmousewheel",d="chrome",c="qx.event.type.MouseWheel",b="browser.name",a="y";
qx.Class.define(c,{extend:qx.event.type.Mouse,statics:{MAXSCROLL:null,MINSCROLL:null,FACTOR:1},members:{stop:function(){this.stopPropagation();
this.preventDefault();
},__gf:function(m){var n=Math.abs(m);
if(qx.event.type.MouseWheel.MINSCROLL==null||qx.event.type.MouseWheel.MINSCROLL>n){qx.event.type.MouseWheel.MINSCROLL=n;
this.__gg();
}if(qx.event.type.MouseWheel.MAXSCROLL==null||qx.event.type.MouseWheel.MAXSCROLL<n){qx.event.type.MouseWheel.MAXSCROLL=n;
this.__gg();
}if(qx.event.type.MouseWheel.MAXSCROLL===n&&qx.event.type.MouseWheel.MINSCROLL===n){return 2*(m/n);
}var o=qx.event.type.MouseWheel.MAXSCROLL-qx.event.type.MouseWheel.MINSCROLL;
var p=(m/o)*Math.log(o)*qx.event.type.MouseWheel.FACTOR;
return p<0?Math.min(p,-1):Math.max(p,1);
},__gg:function(){var q=qx.event.type.MouseWheel.MAXSCROLL||0;
var t=qx.event.type.MouseWheel.MINSCROLL||q;

if(q<=t){return;
}var r=q-t;
var s=(q/r)*Math.log(r);

if(s==0){s=1;
}qx.event.type.MouseWheel.FACTOR=6/s;
},getWheelDelta:function(u){var e=this._native;
if(u===undefined){if(v===undefined){var v=-e.wheelDelta;

if(e.wheelDelta===undefined){v=e.detail;
}}return this.__gh(v);
}if(u===i){var x=0;

if(e.wheelDelta!==undefined){if(e.wheelDeltaX!==undefined){x=e.wheelDeltaX?this.__gh(-e.wheelDeltaX):0;
}}else{if(e.axis&&e.axis==e.HORIZONTAL_AXIS){x=this.__gh(e.detail);
}}return x;
}if(u===a){var y=0;

if(e.wheelDelta!==undefined){if(e.wheelDeltaY!==undefined){y=e.wheelDeltaY?this.__gh(-e.wheelDeltaY):0;
}else{y=this.__gh(-e.wheelDelta);
}}else{if(!(e.axis&&e.axis==e.HORIZONTAL_AXIS)){y=this.__gh(e.detail);
}}return y;
}return 0;
},__gh:function(w){if(qx.core.Environment.get(f)){return this.__gf(w);
}else{var z=qx.core.Environment.select(j,{"default":function(){return w/40;
},"gecko":function(){return w;
},"webkit":function(){if(qx.core.Environment.get(b)==d){if(qx.core.Environment.get(k)==h){return w/60;
}else{return w/120;
}}else{if(qx.core.Environment.get(k)==g){var A=120;
if(parseFloat(qx.core.Environment.get(l))==533.16){A=1200;
}}else{A=40;
if(parseFloat(qx.core.Environment.get(l))==533.16||parseFloat(qx.core.Environment.get(l))==533.17||parseFloat(qx.core.Environment.get(l))==533.18){A=1200;
}}return w/A;
}}});
return z.call(this);
}}}});
})();
(function(){var f="engine.name",e="qx.dom.Hierarchy",d="previousSibling",c="*",b="nextSibling",a="parentNode";
qx.Class.define(e,{statics:{getNodeIndex:function(g){var h=0;

while(g&&(g=g.previousSibling)){h++;
}return h;
},getElementIndex:function(i){var j=0;
var k=qx.dom.Node.ELEMENT;

while(i&&(i=i.previousSibling)){if(i.nodeType==k){j++;
}}return j;
},getNextElementSibling:function(l){while(l&&(l=l.nextSibling)&&!qx.dom.Node.isElement(l)){continue;
}return l||null;
},getPreviousElementSibling:function(m){while(m&&(m=m.previousSibling)&&!qx.dom.Node.isElement(m)){continue;
}return m||null;
},contains:qx.core.Environment.select(f,{"webkit|mshtml|opera":function(n,o){if(qx.dom.Node.isDocument(n)){var p=qx.dom.Node.getDocument(o);
return n&&p==n;
}else if(qx.dom.Node.isDocument(o)){return false;
}else{return n.contains(o);
}},"gecko":function(q,r){return !!(q.compareDocumentPosition(r)&16);
},"default":function(s,t){while(t){if(s==t){return true;
}t=t.parentNode;
}return false;
}}),isRendered:qx.core.Environment.select(f,{"mshtml":function(u){if(!u.parentNode||!u.offsetParent){return false;
}var v=u.ownerDocument||u.document;
return v.body.contains(u);
},"gecko":function(w){var x=w.ownerDocument||w.document;
return !!(x.compareDocumentPosition(w)&16);
},"default":function(y){if(!y.parentNode||!y.offsetParent){return false;
}var z=y.ownerDocument||y.document;
return z.body.contains(y);
}}),isDescendantOf:function(A,B){return this.contains(B,A);
},getCommonParent:qx.core.Environment.select(f,{"mshtml|opera":function(C,D){if(C===D){return C;
}
while(C&&qx.dom.Node.isElement(C)){if(C.contains(D)){return C;
}C=C.parentNode;
}return null;
},"default":function(E,F){if(E===F){return E;
}var G={};
var J=qx.core.ObjectRegistry;
var I,H;

while(E||F){if(E){I=J.toHashCode(E);

if(G[I]){return G[I];
}G[I]=E;
E=E.parentNode;
}
if(F){H=J.toHashCode(F);

if(G[H]){return G[H];
}G[H]=F;
F=F.parentNode;
}}return null;
}}),getAncestors:function(K){return this._recursivelyCollect(K,a);
},getChildElements:function(L){L=L.firstChild;

if(!L){return [];
}var M=this.getNextSiblings(L);

if(L.nodeType===1){M.unshift(L);
}return M;
},getDescendants:function(N){return qx.lang.Array.fromCollection(N.getElementsByTagName(c));
},getFirstDescendant:function(O){O=O.firstChild;

while(O&&O.nodeType!=1){O=O.nextSibling;
}return O;
},getLastDescendant:function(P){P=P.lastChild;

while(P&&P.nodeType!=1){P=P.previousSibling;
}return P;
},getPreviousSiblings:function(Q){return this._recursivelyCollect(Q,d);
},getNextSiblings:function(R){return this._recursivelyCollect(R,b);
},_recursivelyCollect:function(S,T){var U=[];

while(S=S[T]){if(S.nodeType==1){U.push(S);
}}return U;
},getSiblings:function(V){return this.getPreviousSiblings(V).reverse().concat(this.getNextSiblings(V));
},isEmpty:function(W){W=W.firstChild;

while(W){if(W.nodeType===qx.dom.Node.ELEMENT||W.nodeType===qx.dom.Node.TEXT){return false;
}W=W.nextSibling;
}return true;
},cleanWhitespace:function(X){var Y=X.firstChild;

while(Y){var ba=Y.nextSibling;

if(Y.nodeType==3&&!/\S/.test(Y.nodeValue)){X.removeChild(Y);
}Y=ba;
}}}});
})();
(function(){var a="qx.event.handler.Capture";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{capture:true,losecapture:true},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:true},members:{canHandleEvent:function(b,c){},registerEvent:function(d,e,f){},unregisterEvent:function(g,h,i){}},defer:function(j){qx.event.Registration.addHandler(j);
}});
})();
(function(){var m="keydown",l="engine.name",k="keypress",j="NumLock",i="keyup",h="os.name",g="Enter",f="0",e="engine.version",d="9",bx="-",bw="+",bv="PrintScreen",bu="PageUp",bt="gecko",bs="A",br="Space",bq="Left",bp="F5",bo="Down",t="Up",u="F11",r="F6",s="useraction",p="F3",q="keyinput",n="Insert",o="F8",B="End",C="/",Q="Delete",M="*",Y="F1",T="F4",bk="Home",be="F2",H="F12",bn="PageDown",bm="mshtml",bl="F7",F="Win",J="osx",L="F9",O="webkit",R="cmd",U="F10",bb="Right",bg="Z",v="text",w="Escape",I="5",X="3",W="Meta",V="7",bd="Scroll",bc="CapsLock",S="input",ba="Control",a="Tab",bf="Shift",x="Pause",y="Unidentified",N="qx.event.handler.Keyboard",b="win",c="1",E="Apps",z="6",A="off",D="4",P="Alt",bi="2",bh="8",K="Backspace",bj="autoComplete",G=",";
qx.Class.define(N,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(by){qx.core.Object.call(this);
this.__eI=by;
this.__cf=by.getWindow();
if((qx.core.Environment.get(l)==bt)){this.__cX=this.__cf;
}else{this.__cX=this.__cf.document.documentElement;
}this.__gi={};
this._initKeyObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{keyup:1,keydown:1,keypress:1,keyinput:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:true,isValidKeyIdentifier:function(bz){if(this._identifierToKeyCodeMap[bz]){return true;
}
if(bz.length!=1){return false;
}
if(bz>=f&&bz<=d){return true;
}
if(bz>=bs&&bz<=bg){return true;
}
switch(bz){case bw:case bx:case M:case C:return true;
default:return false;
}},isPrintableKeyIdentifier:function(bA){if(bA===br){return true;
}else{return this._identifierToKeyCodeMap[bA]?false:true;
}}},members:{__gj:null,__eI:null,__cf:null,__cX:null,__gi:null,__gk:null,__gl:null,__gm:null,canHandleEvent:function(bB,bC){},registerEvent:function(bD,bE,bF){},unregisterEvent:function(bG,bH,bI){},_fireInputEvent:function(bJ,bK){var bL=this.__gn();
if(bL&&bL.offsetWidth!=0){var event=qx.event.Registration.createEvent(q,qx.event.type.KeyInput,[bJ,bL,bK]);
this.__eI.dispatchEvent(bL,event);
}if(this.__cf){qx.event.Registration.fireEvent(this.__cf,s,qx.event.type.Data,[q]);
}},_fireSequenceEvent:function(bM,bN,bO){var bP=this.__gn();
var bQ=bM.keyCode;
var event=qx.event.Registration.createEvent(bN,qx.event.type.KeySequence,[bM,bP,bO]);
this.__eI.dispatchEvent(bP,event);
if(qx.core.Environment.get(l)==bm||qx.core.Environment.get(l)==O){if(bN==m&&event.getDefaultPrevented()){if(!this._isNonPrintableKeyCode(bQ)&&!this._emulateKeyPress[bQ]){this._fireSequenceEvent(bM,k,bO);
}}}if(this.__cf){qx.event.Registration.fireEvent(this.__cf,s,qx.event.type.Data,[bN]);
}},__gn:function(){var bR=this.__eI.getHandler(qx.event.handler.Focus);
var bS=bR.getActive();
if(!bS||bS.offsetWidth==0){bS=bR.getFocus();
}if(!bS||bS.offsetWidth==0){bS=this.__eI.getWindow().document.body;
}return bS;
},_initKeyObserver:function(){this.__gj=qx.lang.Function.listener(this.__go,this);
this.__gm=qx.lang.Function.listener(this.__gq,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__cX,i,this.__gj);
Event.addNativeListener(this.__cX,m,this.__gj);
Event.addNativeListener(this.__cX,k,this.__gm);
},_stopKeyObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__cX,i,this.__gj);
Event.removeNativeListener(this.__cX,m,this.__gj);
Event.removeNativeListener(this.__cX,k,this.__gm);

for(var bU in (this.__gl||{})){var bT=this.__gl[bU];
Event.removeNativeListener(bT.target,k,bT.callback);
}delete (this.__gl);
},__go:qx.event.GlobalError.observeMethod(qx.core.Environment.select(l,{"mshtml":function(bV){bV=window.event||bV;
var bY=bV.keyCode;
var bW=0;
var bX=bV.type;
if(!(this.__gi[bY]==m&&bX==m)){this._idealKeyHandler(bY,bW,bX,bV);
}if(bX==m){if(this._isNonPrintableKeyCode(bY)||this._emulateKeyPress[bY]){this._idealKeyHandler(bY,bW,k,bV);
}}this.__gi[bY]=bX;
},"gecko":function(ca){var ce=this._keyCodeFix[ca.keyCode]||ca.keyCode;
var cc=0;
var cd=ca.type;
if(qx.core.Environment.get(h)==b){var cb=ce?this._keyCodeToIdentifier(ce):this._charCodeToIdentifier(cc);

if(!(this.__gi[cb]==m&&cd==m)){this._idealKeyHandler(ce,cc,cd,ca);
}this.__gi[cb]=cd;
}else{this._idealKeyHandler(ce,cc,cd,ca);
}this.__gp(ca.target,cd,ce);
},"webkit":function(cf){var ci=0;
var cg=0;
var ch=cf.type;
if(parseFloat(qx.core.Environment.get(e))<525.13){if(ch==i||ch==m){ci=this._charCode2KeyCode[cf.charCode]||cf.keyCode;
}else{if(this._charCode2KeyCode[cf.charCode]){ci=this._charCode2KeyCode[cf.charCode];
}else{cg=cf.charCode;
}}this._idealKeyHandler(ci,cg,ch,cf);
}else{ci=cf.keyCode;
this._idealKeyHandler(ci,cg,ch,cf);
if(ch==m){if(this._isNonPrintableKeyCode(ci)||this._emulateKeyPress[ci]){this._idealKeyHandler(ci,cg,k,cf);
}}this.__gi[ci]=ch;
}},"opera":function(cj){this.__gk=cj.keyCode;
this._idealKeyHandler(cj.keyCode,0,cj.type,cj);
}})),__gp:qx.core.Environment.select(l,{"gecko":function(ck,cl,cm){if(cl===m&&(cm==33||cm==34||cm==38||cm==40)&&ck.type==v&&ck.tagName.toLowerCase()===S&&ck.getAttribute(bj)!==A){if(!this.__gl){this.__gl={};
}var co=qx.core.ObjectRegistry.toHashCode(ck);

if(this.__gl[co]){return;
}var self=this;
this.__gl[co]={target:ck,callback:function(cp){qx.bom.Event.stopPropagation(cp);
self.__gq(cp);
}};
var cn=qx.event.GlobalError.observeMethod(this.__gl[co].callback);
qx.bom.Event.addNativeListener(ck,k,cn);
}},"default":null}),__gq:qx.event.GlobalError.observeMethod(qx.core.Environment.select(l,{"mshtml":function(cq){cq=window.event||cq;

if(this._charCode2KeyCode[cq.keyCode]){this._idealKeyHandler(this._charCode2KeyCode[cq.keyCode],0,cq.type,cq);
}else{this._idealKeyHandler(0,cq.keyCode,cq.type,cq);
}},"gecko":function(cr){var cu=this._keyCodeFix[cr.keyCode]||cr.keyCode;
var cs=cr.charCode;
var ct=cr.type;
this._idealKeyHandler(cu,cs,ct,cr);
},"webkit":function(cv){if(parseFloat(qx.core.Environment.get(e))<525.13){var cy=0;
var cw=0;
var cx=cv.type;

if(cx==i||cx==m){cy=this._charCode2KeyCode[cv.charCode]||cv.keyCode;
}else{if(this._charCode2KeyCode[cv.charCode]){cy=this._charCode2KeyCode[cv.charCode];
}else{cw=cv.charCode;
}}this._idealKeyHandler(cy,cw,cx,cv);
}else{if(this._charCode2KeyCode[cv.keyCode]){this._idealKeyHandler(this._charCode2KeyCode[cv.keyCode],0,cv.type,cv);
}else{this._idealKeyHandler(0,cv.keyCode,cv.type,cv);
}}},"opera":function(cz){var cB=cz.keyCode;
var cA=cz.type;
if(cB!=this.__gk){this._idealKeyHandler(0,this.__gk,cA,cz);
}else{if(this._keyCodeToIdentifierMap[cz.keyCode]){this._idealKeyHandler(cz.keyCode,0,cz.type,cz);
}else{this._idealKeyHandler(0,cz.keyCode,cz.type,cz);
}}}})),_idealKeyHandler:function(cC,cD,cE,cF){var cG;
if(cC||(!cC&&!cD)){cG=this._keyCodeToIdentifier(cC);
this._fireSequenceEvent(cF,cE,cG);
}else{cG=this._charCodeToIdentifier(cD);
this._fireSequenceEvent(cF,k,cG);
this._fireInputEvent(cF,cD);
}},_specialCharCodeMap:{8:K,9:a,13:g,27:w,32:br},_emulateKeyPress:qx.core.Environment.select(l,{"mshtml":{8:true,9:true},"webkit":{8:true,9:true,27:true},"default":{}}),_keyCodeToIdentifierMap:{16:bf,17:ba,18:P,20:bc,224:W,37:bq,38:t,39:bb,40:bo,33:bu,34:bn,35:B,36:bk,45:n,46:Q,112:Y,113:be,114:p,115:T,116:bp,117:r,118:bl,119:o,120:L,121:U,122:u,123:H,144:j,44:bv,145:bd,19:x,91:qx.core.Environment.get(h)==J?R:F,92:F,93:qx.core.Environment.get(h)==J?R:E},_numpadToCharCode:{96:f.charCodeAt(0),97:c.charCodeAt(0),98:bi.charCodeAt(0),99:X.charCodeAt(0),100:D.charCodeAt(0),101:I.charCodeAt(0),102:z.charCodeAt(0),103:V.charCodeAt(0),104:bh.charCodeAt(0),105:d.charCodeAt(0),106:M.charCodeAt(0),107:bw.charCodeAt(0),109:bx.charCodeAt(0),110:G.charCodeAt(0),111:C.charCodeAt(0)},_charCodeA:bs.charCodeAt(0),_charCodeZ:bg.charCodeAt(0),_charCode0:f.charCodeAt(0),_charCode9:d.charCodeAt(0),_isNonPrintableKeyCode:function(cH){return this._keyCodeToIdentifierMap[cH]?true:false;
},_isIdentifiableKeyCode:function(cI){if(cI>=this._charCodeA&&cI<=this._charCodeZ){return true;
}if(cI>=this._charCode0&&cI<=this._charCode9){return true;
}if(this._specialCharCodeMap[cI]){return true;
}if(this._numpadToCharCode[cI]){return true;
}if(this._isNonPrintableKeyCode(cI)){return true;
}return false;
},_keyCodeToIdentifier:function(cJ){if(this._isIdentifiableKeyCode(cJ)){var cK=this._numpadToCharCode[cJ];

if(cK){return String.fromCharCode(cK);
}return (this._keyCodeToIdentifierMap[cJ]||this._specialCharCodeMap[cJ]||String.fromCharCode(cJ));
}else{return y;
}},_charCodeToIdentifier:function(cL){return this._specialCharCodeMap[cL]||String.fromCharCode(cL).toUpperCase();
},_identifierToKeyCode:function(cM){return qx.event.handler.Keyboard._identifierToKeyCodeMap[cM]||cM.charCodeAt(0);
}},destruct:function(){this._stopKeyObserver();
this.__gk=this.__eI=this.__cf=this.__cX=this.__gi=null;
},defer:function(cN,cO){qx.event.Registration.addHandler(cN);
if(!cN._identifierToKeyCodeMap){cN._identifierToKeyCodeMap={};

for(var cP in cO._keyCodeToIdentifierMap){cN._identifierToKeyCodeMap[cO._keyCodeToIdentifierMap[cP]]=parseInt(cP,10);
}
for(var cP in cO._specialCharCodeMap){cN._identifierToKeyCodeMap[cO._specialCharCodeMap[cP]]=parseInt(cP,10);
}}
if((qx.core.Environment.get(l)==bm)){cO._charCode2KeyCode={13:13,27:27};
}else if((qx.core.Environment.get(l)==bt)){cO._keyCodeFix={12:cO._identifierToKeyCode(j)};
}else if((qx.core.Environment.get(l)==O)){if(parseFloat(qx.core.Environment.get(e))<525.13){cO._charCode2KeyCode={63289:cO._identifierToKeyCode(j),63276:cO._identifierToKeyCode(bu),63277:cO._identifierToKeyCode(bn),63275:cO._identifierToKeyCode(B),63273:cO._identifierToKeyCode(bk),63234:cO._identifierToKeyCode(bq),63232:cO._identifierToKeyCode(t),63235:cO._identifierToKeyCode(bb),63233:cO._identifierToKeyCode(bo),63272:cO._identifierToKeyCode(Q),63302:cO._identifierToKeyCode(n),63236:cO._identifierToKeyCode(Y),63237:cO._identifierToKeyCode(be),63238:cO._identifierToKeyCode(p),63239:cO._identifierToKeyCode(T),63240:cO._identifierToKeyCode(bp),63241:cO._identifierToKeyCode(r),63242:cO._identifierToKeyCode(bl),63243:cO._identifierToKeyCode(o),63244:cO._identifierToKeyCode(L),63245:cO._identifierToKeyCode(U),63246:cO._identifierToKeyCode(u),63247:cO._identifierToKeyCode(H),63248:cO._identifierToKeyCode(bv),3:cO._identifierToKeyCode(g),12:cO._identifierToKeyCode(j),13:cO._identifierToKeyCode(g)};
}else{cO._charCode2KeyCode={13:13,27:27};
}}}});
})();
(function(){var a="qx.event.type.KeyInput";
qx.Class.define(a,{extend:qx.event.type.Dom,members:{init:function(b,c,d){qx.event.type.Dom.prototype.init.call(this,b,c,null,true,true);
this._charCode=d;
return this;
},clone:function(e){var f=qx.event.type.Dom.prototype.clone.call(this,e);
f._charCode=this._charCode;
return f;
},getCharCode:function(){return this._charCode;
},getChar:function(){return String.fromCharCode(this._charCode);
}}});
})();
(function(){var a="qx.event.type.KeySequence";
qx.Class.define(a,{extend:qx.event.type.Dom,members:{init:function(b,c,d){qx.event.type.Dom.prototype.init.call(this,b,c,null,true,true);
this._keyCode=b.keyCode;
this._identifier=d;
return this;
},clone:function(e){var f=qx.event.type.Dom.prototype.clone.call(this,e);
f._keyCode=this._keyCode;
f._identifier=this._identifier;
return f;
},getKeyIdentifier:function(){return this._identifier;
},getKeyCode:function(){return this._keyCode;
},isPrintable:function(){return qx.event.handler.Keyboard.isPrintableKeyIdentifier(this._identifier);
}}});
})();
(function(){var j="engine.name",i="mousedown",h="mouseup",g="blur",f="focus",e="on",d="selectstart",c="DOMFocusOut",b="focusin",a="focusout",z="DOMFocusIn",y="draggesture",x="qx.event.handler.Focus",w="_applyFocus",v="deactivate",u="textarea",t="_applyActive",s='character',r="input",q="qxSelectable",o="tabIndex",p="off",m="activate",n="mshtml",k="qxKeepFocus",l="qxKeepActive";
qx.Class.define(x,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(A){qx.core.Object.call(this);
this._manager=A;
this._window=A.getWindow();
this._document=this._window.document;
this._root=this._document.documentElement;
this._body=this._document.body;
this._initObserver();
},properties:{active:{apply:t,nullable:true},focus:{apply:w,nullable:true}},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{focus:1,blur:1,focusin:1,focusout:1,activate:1,deactivate:1},IGNORE_CAN_HANDLE:true,FOCUSABLE_ELEMENTS:qx.core.Environment.select("engine.name",{"mshtml|gecko":{a:1,body:1,button:1,frame:1,iframe:1,img:1,input:1,object:1,select:1,textarea:1},"opera|webkit":{button:1,input:1,select:1,textarea:1}})},members:{__gr:null,__gs:null,__gt:null,__gu:null,__gv:null,__gw:null,__gx:null,__gy:null,__gz:null,__gA:null,canHandleEvent:function(B,C){},registerEvent:function(D,E,F){},unregisterEvent:function(G,H,I){},focus:function(J){if((qx.core.Environment.get(j)==n)){window.setTimeout(function(){try{J.focus();
var K=qx.bom.Selection.get(J);

if(K.length==0){var L=J.createTextRange();
L.moveStart(s,J.value.length);
L.collapse();
L.select();
}}catch(M){}},0);
}else{try{J.focus();
}catch(N){}}this.setFocus(J);
this.setActive(J);
},activate:function(O){this.setActive(O);
},blur:function(P){try{P.blur();
}catch(Q){}
if(this.getActive()===P){this.resetActive();
}
if(this.getFocus()===P){this.resetFocus();
}},deactivate:function(R){if(this.getActive()===R){this.resetActive();
}},tryActivate:function(S){var T=this.__gO(S);

if(T){this.setActive(T);
}},__fF:function(U,V,W,X){var ba=qx.event.Registration;
var Y=ba.createEvent(W,qx.event.type.Focus,[U,V,X]);
ba.dispatchEvent(U,Y);
},_windowFocused:true,__gB:function(){if(this._windowFocused){this._windowFocused=false;
this.__fF(this._window,null,g,false);
}},__gC:function(){if(!this._windowFocused){this._windowFocused=true;
this.__fF(this._window,null,f,false);
}},_initObserver:qx.core.Environment.select(j,{"gecko":function(){this.__gr=qx.lang.Function.listener(this.__gI,this);
this.__gs=qx.lang.Function.listener(this.__gJ,this);
this.__gt=qx.lang.Function.listener(this.__gH,this);
this.__gu=qx.lang.Function.listener(this.__gG,this);
this.__gv=qx.lang.Function.listener(this.__gD,this);
qx.bom.Event.addNativeListener(this._document,i,this.__gr,true);
qx.bom.Event.addNativeListener(this._document,h,this.__gs,true);
qx.bom.Event.addNativeListener(this._window,f,this.__gt,true);
qx.bom.Event.addNativeListener(this._window,g,this.__gu,true);
qx.bom.Event.addNativeListener(this._window,y,this.__gv,true);
},"mshtml":function(){this.__gr=qx.lang.Function.listener(this.__gI,this);
this.__gs=qx.lang.Function.listener(this.__gJ,this);
this.__gx=qx.lang.Function.listener(this.__gE,this);
this.__gy=qx.lang.Function.listener(this.__gF,this);
this.__gw=qx.lang.Function.listener(this.__gL,this);
qx.bom.Event.addNativeListener(this._document,i,this.__gr);
qx.bom.Event.addNativeListener(this._document,h,this.__gs);
qx.bom.Event.addNativeListener(this._document,b,this.__gx);
qx.bom.Event.addNativeListener(this._document,a,this.__gy);
qx.bom.Event.addNativeListener(this._document,d,this.__gw);
},"webkit":function(){this.__gr=qx.lang.Function.listener(this.__gI,this);
this.__gs=qx.lang.Function.listener(this.__gJ,this);
this.__gy=qx.lang.Function.listener(this.__gF,this);
this.__gt=qx.lang.Function.listener(this.__gH,this);
this.__gu=qx.lang.Function.listener(this.__gG,this);
this.__gw=qx.lang.Function.listener(this.__gL,this);
qx.bom.Event.addNativeListener(this._document,i,this.__gr,true);
qx.bom.Event.addNativeListener(this._document,h,this.__gs,true);
qx.bom.Event.addNativeListener(this._document,d,this.__gw,false);
qx.bom.Event.addNativeListener(this._window,c,this.__gy,true);
qx.bom.Event.addNativeListener(this._window,f,this.__gt,true);
qx.bom.Event.addNativeListener(this._window,g,this.__gu,true);
},"opera":function(){this.__gr=qx.lang.Function.listener(this.__gI,this);
this.__gs=qx.lang.Function.listener(this.__gJ,this);
this.__gx=qx.lang.Function.listener(this.__gE,this);
this.__gy=qx.lang.Function.listener(this.__gF,this);
qx.bom.Event.addNativeListener(this._document,i,this.__gr,true);
qx.bom.Event.addNativeListener(this._document,h,this.__gs,true);
qx.bom.Event.addNativeListener(this._window,z,this.__gx,true);
qx.bom.Event.addNativeListener(this._window,c,this.__gy,true);
}}),_stopObserver:qx.core.Environment.select(j,{"gecko":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__gr,true);
qx.bom.Event.removeNativeListener(this._document,h,this.__gs,true);
qx.bom.Event.removeNativeListener(this._window,f,this.__gt,true);
qx.bom.Event.removeNativeListener(this._window,g,this.__gu,true);
qx.bom.Event.removeNativeListener(this._window,y,this.__gv,true);
},"mshtml":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__gr);
qx.bom.Event.removeNativeListener(this._document,h,this.__gs);
qx.bom.Event.removeNativeListener(this._document,b,this.__gx);
qx.bom.Event.removeNativeListener(this._document,a,this.__gy);
qx.bom.Event.removeNativeListener(this._document,d,this.__gw);
},"webkit":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__gr,true);
qx.bom.Event.removeNativeListener(this._document,h,this.__gs,true);
qx.bom.Event.removeNativeListener(this._document,d,this.__gw,false);
qx.bom.Event.removeNativeListener(this._window,c,this.__gy,true);
qx.bom.Event.removeNativeListener(this._window,f,this.__gt,true);
qx.bom.Event.removeNativeListener(this._window,g,this.__gu,true);
},"opera":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__gr,true);
qx.bom.Event.removeNativeListener(this._document,h,this.__gs,true);
qx.bom.Event.removeNativeListener(this._window,z,this.__gx,true);
qx.bom.Event.removeNativeListener(this._window,c,this.__gy,true);
}}),__gD:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"gecko":function(bb){var bc=qx.bom.Event.getTarget(bb);

if(!this.__gP(bc)){qx.bom.Event.preventDefault(bb);
}},"default":null})),__gE:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"mshtml":function(bd){this.__gC();
var bf=qx.bom.Event.getTarget(bd);
var be=this.__gN(bf);

if(be){this.setFocus(be);
}this.tryActivate(bf);
},"opera":function(bg){var bh=qx.bom.Event.getTarget(bg);

if(bh==this._document||bh==this._window){this.__gC();

if(this.__gz){this.setFocus(this.__gz);
delete this.__gz;
}
if(this.__gA){this.setActive(this.__gA);
delete this.__gA;
}}else{this.setFocus(bh);
this.tryActivate(bh);
if(!this.__gP(bh)){bh.selectionStart=0;
bh.selectionEnd=0;
}}},"default":null})),__gF:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"mshtml":function(bi){var bj=qx.bom.Event.getRelatedTarget(bi);
if(bj==null){this.__gB();
this.resetFocus();
this.resetActive();
}},"webkit":function(bk){var bl=qx.bom.Event.getTarget(bk);

if(bl===this.getFocus()){this.resetFocus();
}
if(bl===this.getActive()){this.resetActive();
}},"opera":function(bm){var bn=qx.bom.Event.getTarget(bm);

if(bn==this._document){this.__gB();
this.__gz=this.getFocus();
this.__gA=this.getActive();
this.resetFocus();
this.resetActive();
}else{if(bn===this.getFocus()){this.resetFocus();
}
if(bn===this.getActive()){this.resetActive();
}}},"default":null})),__gG:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"gecko":function(bo){var bp=qx.bom.Event.getTarget(bo);

if(bp===this._window||bp===this._document){this.__gB();
this.resetActive();
this.resetFocus();
}},"webkit":function(bq){var br=qx.bom.Event.getTarget(bq);

if(br===this._window||br===this._document){this.__gB();
this.__gz=this.getFocus();
this.__gA=this.getActive();
this.resetActive();
this.resetFocus();
}},"default":null})),__gH:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"gecko":function(bs){var bt=qx.bom.Event.getTarget(bs);

if(bt===this._window||bt===this._document){this.__gC();
bt=this._body;
}this.setFocus(bt);
this.tryActivate(bt);
},"webkit":function(bu){var bv=qx.bom.Event.getTarget(bu);

if(bv===this._window||bv===this._document){this.__gC();

if(this.__gz){this.setFocus(this.__gz);
delete this.__gz;
}
if(this.__gA){this.setActive(this.__gA);
delete this.__gA;
}}else{this.setFocus(bv);
this.tryActivate(bv);
}},"default":null})),__gI:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"gecko":function(bw){var by=qx.bom.Event.getTarget(bw);
var bx=this.__gN(by);

if(!bx){qx.bom.Event.preventDefault(bw);
}else if(bx===this._body){this.setFocus(bx);
}},"mshtml":function(bz){var bB=qx.bom.Event.getTarget(bz);
var bA=this.__gN(bB);

if(bA){if(!this.__gP(bB)){bB.unselectable=e;
try{document.selection.empty();
}catch(bC){}try{bA.focus();
}catch(bD){}}}else{qx.bom.Event.preventDefault(bz);
if(!this.__gP(bB)){bB.unselectable=e;
}}},"webkit":function(bE){var bG=qx.bom.Event.getTarget(bE);
var bF=this.__gN(bG);

if(bF){this.setFocus(bF);
}else{qx.bom.Event.preventDefault(bE);
}},"opera":function(bH){var bK=qx.bom.Event.getTarget(bH);
var bI=this.__gN(bK);

if(!this.__gP(bK)){qx.bom.Event.preventDefault(bH);
if(bI){var bJ=this.getFocus();

if(bJ&&bJ.selectionEnd){bJ.selectionStart=0;
bJ.selectionEnd=0;
bJ.blur();
}if(bI){this.setFocus(bI);
}}}else if(bI){this.setFocus(bI);
}},"default":null})),__gJ:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"mshtml":function(bL){var bM=qx.bom.Event.getTarget(bL);

if(bM.unselectable){bM.unselectable=p;
}this.tryActivate(this.__gK(bM));
},"gecko":function(bN){var bO=qx.bom.Event.getTarget(bN);

while(bO&&bO.offsetWidth===undefined){bO=bO.parentNode;
}
if(bO){this.tryActivate(bO);
}},"webkit|opera":function(bP){var bQ=qx.bom.Event.getTarget(bP);
this.tryActivate(this.__gK(bQ));
},"default":null})),__gK:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"mshtml|webkit":function(bR){var bS=this.getFocus();

if(bS&&bR!=bS&&(bS.nodeName.toLowerCase()===r||bS.nodeName.toLowerCase()===u)){bR=bS;
}return bR;
},"default":function(bT){return bT;
}})),__gL:qx.event.GlobalError.observeMethod(qx.core.Environment.select(j,{"mshtml|webkit":function(bU){var bV=qx.bom.Event.getTarget(bU);

if(!this.__gP(bV)){qx.bom.Event.preventDefault(bU);
}},"default":null})),__gM:function(bW){var bX=qx.bom.element.Attribute.get(bW,o);

if(bX>=1){return true;
}var bY=qx.event.handler.Focus.FOCUSABLE_ELEMENTS;

if(bX>=0&&bY[bW.tagName]){return true;
}return false;
},__gN:function(ca){while(ca&&ca.nodeType===1){if(ca.getAttribute(k)==e){return null;
}
if(this.__gM(ca)){return ca;
}ca=ca.parentNode;
}return this._body;
},__gO:function(cb){var cc=cb;

while(cb&&cb.nodeType===1){if(cb.getAttribute(l)==e){return null;
}cb=cb.parentNode;
}return cc;
},__gP:function(cd){while(cd&&cd.nodeType===1){var ce=cd.getAttribute(q);

if(ce!=null){return ce===e;
}cd=cd.parentNode;
}return true;
},_applyActive:function(cf,cg){if(cg){this.__fF(cg,cf,v,true);
}
if(cf){this.__fF(cf,cg,m,true);
}},_applyFocus:function(ch,ci){if(ci){this.__fF(ci,ch,a,true);
}
if(ch){this.__fF(ch,ci,b,true);
}if(ci){this.__fF(ci,ch,g,false);
}
if(ch){this.__fF(ch,ci,f,false);
}}},destruct:function(){this._stopObserver();
this._manager=this._window=this._document=this._root=this._body=this.__gQ=null;
},defer:function(cj){qx.event.Registration.addHandler(cj);
var ck=cj.FOCUSABLE_ELEMENTS;

for(var cl in ck){ck[cl.toUpperCase()]=1;
}}});
})();
(function(){var k="engine.name",j="character",i="EndToEnd",h="input",g="StartToStart",f="textarea",e='character',d="qx.bom.Selection",c="button",b="#text",a="body";
qx.Class.define(d,{statics:{getSelectionObject:qx.core.Environment.select(k,{"mshtml":function(l){return l.selection;
},"default":function(m){return qx.dom.Node.getWindow(m).getSelection();
}}),get:qx.core.Environment.select(k,{"mshtml":function(n){var o=qx.bom.Range.get(qx.dom.Node.getDocument(n));
return o.text;
},"default":function(p){if(this.__gR(p)){return p.value.substring(p.selectionStart,p.selectionEnd);
}else{return this.getSelectionObject(qx.dom.Node.getDocument(p)).toString();
}}}),getLength:qx.core.Environment.select(k,{"mshtml":function(q){var s=this.get(q);
var r=qx.util.StringSplit.split(s,/\r\n/);
return s.length-(r.length-1);
},"opera":function(t){var y,w,u;

if(this.__gR(t)){var x=t.selectionStart;
var v=t.selectionEnd;
y=t.value.substring(x,v);
w=v-x;
}else{y=qx.bom.Selection.get(t);
w=y.length;
}u=qx.util.StringSplit.split(y,/\r\n/);
return w-(u.length-1);
},"default":function(z){if(this.__gR(z)){return z.selectionEnd-z.selectionStart;
}else{return this.get(z).length;
}}}),getStart:qx.core.Environment.select(k,{"mshtml":function(A){if(this.__gR(A)){var F=qx.bom.Range.get();
if(!A.contains(F.parentElement())){return -1;
}var G=qx.bom.Range.get(A);
var E=A.value.length;
G.moveToBookmark(F.getBookmark());
G.moveEnd(e,E);
return E-G.text.length;
}else{var G=qx.bom.Range.get(A);
var C=G.parentElement();
var H=qx.bom.Range.get();

try{H.moveToElementText(C);
}catch(J){return 0;
}var B=qx.bom.Range.get(qx.dom.Node.getBodyElement(A));
B.setEndPoint(g,G);
B.setEndPoint(i,H);
if(H.compareEndPoints(g,B)==0){return 0;
}var D;
var I=0;

while(true){D=B.moveStart(j,-1);
if(H.compareEndPoints(g,B)==0){break;
}if(D==0){break;
}else{I++;
}}return ++I;
}},"gecko|webkit":function(K){if(this.__gR(K)){return K.selectionStart;
}else{var M=qx.dom.Node.getDocument(K);
var L=this.getSelectionObject(M);
if(L.anchorOffset<L.focusOffset){return L.anchorOffset;
}else{return L.focusOffset;
}}},"default":function(N){if(this.__gR(N)){return N.selectionStart;
}else{return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(N)).anchorOffset;
}}}),getEnd:qx.core.Environment.select(k,{"mshtml":function(O){if(this.__gR(O)){var T=qx.bom.Range.get();
if(!O.contains(T.parentElement())){return -1;
}var U=qx.bom.Range.get(O);
var S=O.value.length;
U.moveToBookmark(T.getBookmark());
U.moveStart(e,-S);
return U.text.length;
}else{var U=qx.bom.Range.get(O);
var Q=U.parentElement();
var V=qx.bom.Range.get();

try{V.moveToElementText(Q);
}catch(X){return 0;
}var S=V.text.length;
var P=qx.bom.Range.get(qx.dom.Node.getBodyElement(O));
P.setEndPoint(i,U);
P.setEndPoint(g,V);
if(V.compareEndPoints(i,P)==0){return S-1;
}var R;
var W=0;

while(true){R=P.moveEnd(j,1);
if(V.compareEndPoints(i,P)==0){break;
}if(R==0){break;
}else{W++;
}}return S-(++W);
}},"gecko|webkit":function(Y){if(this.__gR(Y)){return Y.selectionEnd;
}else{var bb=qx.dom.Node.getDocument(Y);
var ba=this.getSelectionObject(bb);
if(ba.focusOffset>ba.anchorOffset){return ba.focusOffset;
}else{return ba.anchorOffset;
}}},"default":function(bc){if(this.__gR(bc)){return bc.selectionEnd;
}else{return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(bc)).focusOffset;
}}}),__gR:function(bd){return qx.dom.Node.isElement(bd)&&(bd.nodeName.toLowerCase()==h||bd.nodeName.toLowerCase()==f);
},set:qx.core.Environment.select(k,{"mshtml":function(be,bf,bg){var bh;
if(qx.dom.Node.isDocument(be)){be=be.body;
}
if(qx.dom.Node.isElement(be)||qx.dom.Node.isText(be)){switch(be.nodeName.toLowerCase()){case h:case f:case c:if(bg===undefined){bg=be.value.length;
}
if(bf>=0&&bf<=be.value.length&&bg>=0&&bg<=be.value.length){bh=qx.bom.Range.get(be);
bh.collapse(true);
bh.moveStart(j,bf);
bh.moveEnd(j,bg-bf);
bh.select();
return true;
}break;
case b:if(bg===undefined){bg=be.nodeValue.length;
}
if(bf>=0&&bf<=be.nodeValue.length&&bg>=0&&bg<=be.nodeValue.length){bh=qx.bom.Range.get(qx.dom.Node.getBodyElement(be));
bh.moveToElementText(be.parentNode);
bh.collapse(true);
bh.moveStart(j,bf);
bh.moveEnd(j,bg-bf);
bh.select();
return true;
}break;
default:if(bg===undefined){bg=be.childNodes.length-1;
}if(be.childNodes[bf]&&be.childNodes[bg]){bh=qx.bom.Range.get(qx.dom.Node.getBodyElement(be));
bh.moveToElementText(be.childNodes[bf]);
bh.collapse(true);
var bi=qx.bom.Range.get(qx.dom.Node.getBodyElement(be));
bi.moveToElementText(be.childNodes[bg]);
bh.setEndPoint(i,bi);
bh.select();
return true;
}}}return false;
},"default":function(bj,bk,bl){var bp=bj.nodeName.toLowerCase();

if(qx.dom.Node.isElement(bj)&&(bp==h||bp==f)){if(bl===undefined){bl=bj.value.length;
}if(bk>=0&&bk<=bj.value.length&&bl>=0&&bl<=bj.value.length){bj.focus();
bj.select();
bj.setSelectionRange(bk,bl);
return true;
}}else{var bn=false;
var bo=qx.dom.Node.getWindow(bj).getSelection();
var bm=qx.bom.Range.get(bj);
if(qx.dom.Node.isText(bj)){if(bl===undefined){bl=bj.length;
}
if(bk>=0&&bk<bj.length&&bl>=0&&bl<=bj.length){bn=true;
}}else if(qx.dom.Node.isElement(bj)){if(bl===undefined){bl=bj.childNodes.length-1;
}
if(bk>=0&&bj.childNodes[bk]&&bl>=0&&bj.childNodes[bl]){bn=true;
}}else if(qx.dom.Node.isDocument(bj)){bj=bj.body;

if(bl===undefined){bl=bj.childNodes.length-1;
}
if(bk>=0&&bj.childNodes[bk]&&bl>=0&&bj.childNodes[bl]){bn=true;
}}
if(bn){if(!bo.isCollapsed){bo.collapseToStart();
}bm.setStart(bj,bk);
if(qx.dom.Node.isText(bj)){bm.setEnd(bj,bl);
}else{bm.setEndAfter(bj.childNodes[bl]);
}if(bo.rangeCount>0){bo.removeAllRanges();
}bo.addRange(bm);
return true;
}}return false;
}}),setAll:function(bq){return qx.bom.Selection.set(bq,0);
},clear:qx.core.Environment.select(k,{"mshtml":function(br){var bs=qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(br));
var bt=qx.bom.Range.get(br);
var parent=bt.parentElement();
var bu=qx.bom.Range.get(qx.dom.Node.getDocument(br));
if(parent==bu.parentElement()&&parent==br){bs.empty();
}},"default":function(bv){var bx=qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(bv));
var bz=bv.nodeName.toLowerCase();
if(qx.dom.Node.isElement(bv)&&(bz==h||bz==f)){bv.setSelectionRange(0,0);
qx.bom.Element.blur(bv);
}else if(qx.dom.Node.isDocument(bv)||bz==a){bx.collapse(bv.body?bv.body:bv,0);
}else{var by=qx.bom.Range.get(bv);

if(!by.collapsed){var bA;
var bw=by.commonAncestorContainer;
if(qx.dom.Node.isElement(bv)&&qx.dom.Node.isText(bw)){bA=bw.parentNode;
}else{bA=bw;
}
if(bA==bv){bx.collapse(bv,0);
}}}}})}});
})();
(function(){var l="button",k="qx.bom.Range",j="text",i="engine.name",h="password",g="file",f="submit",e="reset",d="textarea",c="input",a="hidden",b="body";
qx.Class.define(k,{statics:{get:qx.core.Environment.select(i,{"mshtml":function(m){if(qx.dom.Node.isElement(m)){switch(m.nodeName.toLowerCase()){case c:switch(m.type){case j:case h:case a:case l:case e:case g:case f:return m.createTextRange();
break;
default:return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(m)).createRange();
}break;
case d:case b:case l:return m.createTextRange();
break;
default:return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(m)).createRange();
}}else{if(m==null){m=window;
}return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(m)).createRange();
}},"default":function(n){var o=qx.dom.Node.getDocument(n);
var p=qx.bom.Selection.getSelectionObject(o);

if(p.rangeCount>0){return p.getRangeAt(0);
}else{return o.createRange();
}}})}});
})();
(function(){var j="",h="m",g="g",f="^",e="qx.util.StringSplit",d="i",c="$(?!\\s)",b="[object RegExp]",a="y";
qx.Class.define(e,{statics:{split:function(k,l,m){if(Object.prototype.toString.call(l)!==b){return String.prototype.split.call(k,l,m);
}var t=[],n=0,r=(l.ignoreCase?d:j)+(l.multiline?h:j)+(l.sticky?a:j),l=RegExp(l.source,r+g),q,u,o,p,s=/()??/.exec(j)[1]===undefined;
k=k+j;

if(!s){q=RegExp(f+l.source+c,r);
}if(m===undefined||+m<0){m=Infinity;
}else{m=Math.floor(+m);

if(!m){return [];
}}
while(u=l.exec(k)){o=u.index+u[0].length;

if(o>n){t.push(k.slice(n,u.index));
if(!s&&u.length>1){u[0].replace(q,function(){for(var i=1;i<arguments.length-2;i++){if(arguments[i]===undefined){u[i]=undefined;
}}});
}
if(u.length>1&&u.index<k.length){Array.prototype.push.apply(t,u.slice(1));
}p=u[0].length;
n=o;

if(t.length>=m){break;
}}
if(l.lastIndex===u.index){l.lastIndex++;
}}
if(n===k.length){if(p||!l.test(j)){t.push(j);
}}else{t.push(k.slice(n));
}return t.length>m?t.slice(0,m):t;
}}});
})();
(function(){var k="alias",j="copy",i="blur",h="mouseout",g="keydown",f="Control",d="Shift",c="mousemove",b="move",a="mouseover",C="Alt",B="keyup",A="mouseup",z="keypress",y="dragend",x="on",w="mousedown",v="qxDraggable",u="Escape",t="drag",r="drop",s="qxDroppable",p="qx.event.handler.DragDrop",q="droprequest",n="dragstart",o="dragchange",l="dragleave",m="dragover";
qx.Class.define(p,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(D){qx.core.Object.call(this);
this.__eI=D;
this.__cX=D.getWindow().document.documentElement;
this.__eI.addListener(this.__cX,w,this._onMouseDown,this);
this.__hd();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{dragstart:1,dragend:1,dragover:1,dragleave:1,drop:1,drag:1,dragchange:1,droprequest:1},IGNORE_CAN_HANDLE:true},members:{__eI:null,__cX:null,__gS:null,__gT:null,__gU:null,__gV:null,__gW:null,__j:null,__gX:null,__gY:null,__ha:false,__hb:0,__hc:0,canHandleEvent:function(E,F){},registerEvent:function(G,H,I){},unregisterEvent:function(J,K,L){},addType:function(M){this.__gU[M]=true;
},addAction:function(N){this.__gV[N]=true;
},supportsType:function(O){return !!this.__gU[O];
},supportsAction:function(P){return !!this.__gV[P];
},getData:function(Q){if(!this.__hj||!this.__gS){throw new Error("This method must not be used outside the drop event listener!");
}
if(!this.__gU[Q]){throw new Error("Unsupported data type: "+Q+"!");
}
if(!this.__j[Q]){this.__gX=Q;
this.__fF(q,this.__gT,this.__gS,false);
}
if(!this.__j[Q]){throw new Error("Please use a droprequest listener to the drag source to fill the manager with data!");
}return this.__j[Q]||null;
},getCurrentAction:function(){return this.__gY;
},addData:function(R,S){this.__j[R]=S;
},getCurrentType:function(){return this.__gX;
},isSessionActive:function(){return this.__ha;
},__hd:function(){this.__gU={};
this.__gV={};
this.__gW={};
this.__j={};
},__he:function(){if(this.__gT==null){return;
}var V=this.__gV;
var T=this.__gW;
var U=null;

if(this.__hj){if(T.Shift&&T.Control&&V.alias){U=k;
}else if(T.Shift&&T.Alt&&V.copy){U=j;
}else if(T.Shift&&V.move){U=b;
}else if(T.Alt&&V.alias){U=k;
}else if(T.Control&&V.copy){U=j;
}else if(V.move){U=b;
}else if(V.copy){U=j;
}else if(V.alias){U=k;
}}
if(U!=this.__gY){this.__gY=U;
this.__fF(o,this.__gT,this.__gS,false);
}},__fF:function(W,X,Y,ba,bb){var bd=qx.event.Registration;
var bc=bd.createEvent(W,qx.event.type.Drag,[ba,bb]);

if(X!==Y){bc.setRelatedTarget(Y);
}return bd.dispatchEvent(X,bc);
},__hf:function(be){while(be&&be.nodeType==1){if(be.getAttribute(v)==x){return be;
}be=be.parentNode;
}return null;
},__hg:function(bf){while(bf&&bf.nodeType==1){if(bf.getAttribute(s)==x){return bf;
}bf=bf.parentNode;
}return null;
},__hh:function(){this.__gT=null;
this.__eI.removeListener(this.__cX,c,this._onMouseMove,this,true);
this.__eI.removeListener(this.__cX,A,this._onMouseUp,this,true);
qx.event.Registration.removeListener(window,i,this._onWindowBlur,this);
this.__hd();
},__hi:function(){if(this.__ha){this.__eI.removeListener(this.__cX,a,this._onMouseOver,this,true);
this.__eI.removeListener(this.__cX,h,this._onMouseOut,this,true);
this.__eI.removeListener(this.__cX,g,this._onKeyDown,this,true);
this.__eI.removeListener(this.__cX,B,this._onKeyUp,this,true);
this.__eI.removeListener(this.__cX,z,this._onKeyPress,this,true);
this.__fF(y,this.__gT,this.__gS,false);
this.__ha=false;
}this.__hj=false;
this.__gS=null;
this.__hh();
},__hj:false,_onWindowBlur:function(e){this.__hi();
},_onKeyDown:function(e){var bg=e.getKeyIdentifier();

switch(bg){case C:case f:case d:if(!this.__gW[bg]){this.__gW[bg]=true;
this.__he();
}}},_onKeyUp:function(e){var bh=e.getKeyIdentifier();

switch(bh){case C:case f:case d:if(this.__gW[bh]){this.__gW[bh]=false;
this.__he();
}}},_onKeyPress:function(e){var bi=e.getKeyIdentifier();

switch(bi){case u:this.__hi();
}},_onMouseDown:function(e){if(this.__ha){return;
}var bj=this.__hf(e.getTarget());

if(bj){this.__hb=e.getDocumentLeft();
this.__hc=e.getDocumentTop();
this.__gT=bj;
this.__eI.addListener(this.__cX,c,this._onMouseMove,this,true);
this.__eI.addListener(this.__cX,A,this._onMouseUp,this,true);
qx.event.Registration.addListener(window,i,this._onWindowBlur,this);
}},_onMouseUp:function(e){if(this.__hj){this.__fF(r,this.__gS,this.__gT,false,e);
}if(this.__ha){e.stopPropagation();
}this.__hi();
},_onMouseMove:function(e){if(this.__ha){if(!this.__fF(t,this.__gT,this.__gS,true,e)){this.__hi();
}}else{if(Math.abs(e.getDocumentLeft()-this.__hb)>3||Math.abs(e.getDocumentTop()-this.__hc)>3){if(this.__fF(n,this.__gT,this.__gS,true,e)){this.__ha=true;
this.__eI.addListener(this.__cX,a,this._onMouseOver,this,true);
this.__eI.addListener(this.__cX,h,this._onMouseOut,this,true);
this.__eI.addListener(this.__cX,g,this._onKeyDown,this,true);
this.__eI.addListener(this.__cX,B,this._onKeyUp,this,true);
this.__eI.addListener(this.__cX,z,this._onKeyPress,this,true);
var bk=this.__gW;
bk.Control=e.isCtrlPressed();
bk.Shift=e.isShiftPressed();
bk.Alt=e.isAltPressed();
this.__he();
}else{this.__fF(y,this.__gT,this.__gS,false);
this.__hh();
}}}},_onMouseOver:function(e){var bl=e.getTarget();
var bm=this.__hg(bl);

if(bm&&bm!=this.__gS){this.__hj=this.__fF(m,bm,this.__gT,true,e);
this.__gS=bm;
this.__he();
}},_onMouseOut:function(e){var bo=this.__hg(e.getTarget());
var bn=this.__hg(e.getRelatedTarget());

if(bo&&bo!==bn&&bo==this.__gS){this.__fF(l,this.__gS,bn,false,e);
this.__gS=null;
this.__hj=false;
qx.event.Timer.once(this.__he,this,0);
}}},destruct:function(){this.__gT=this.__gS=this.__eI=this.__cX=this.__gU=this.__gV=this.__gW=this.__j=null;
},defer:function(bp){qx.event.Registration.addHandler(bp);
}});
})();
(function(){var a="qx.event.type.Drag";
qx.Class.define(a,{extend:qx.event.type.Event,members:{init:function(b,c){qx.event.type.Event.prototype.init.call(this,true,b);

if(c){this._native=c.getNativeEvent()||null;
this._originalTarget=c.getTarget()||null;
}else{this._native=null;
this._originalTarget=null;
}return this;
},clone:function(d){var e=qx.event.type.Event.prototype.clone.call(this,d);
e._native=this._native;
return e;
},getDocumentLeft:function(){if(this._native==null){return 0;
}
if(this._native.pageX!==undefined){return this._native.pageX;
}else{var f=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientX+qx.bom.Viewport.getScrollLeft(f);
}},getDocumentTop:function(){if(this._native==null){return 0;
}
if(this._native.pageY!==undefined){return this._native.pageY;
}else{var g=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientY+qx.bom.Viewport.getScrollTop(g);
}},getManager:function(){return qx.event.Registration.getManager(this.getTarget()).getHandler(qx.event.handler.DragDrop);
},addType:function(h){this.getManager().addType(h);
},addAction:function(i){this.getManager().addAction(i);
},supportsType:function(j){return this.getManager().supportsType(j);
},supportsAction:function(k){return this.getManager().supportsAction(k);
},addData:function(l,m){this.getManager().addData(l,m);
},getData:function(n){return this.getManager().getData(n);
},getCurrentType:function(){return this.getManager().getCurrentType();
},getCurrentAction:function(){return this.getManager().getCurrentAction();
}}});
})();
(function(){var r="engine.name",q="mshtml",p="",o=" ",n=">",m="<",k="='",h="none",g="<INPUT TYPE='RADIO' NAME='RADIOTEST' VALUE='Second Choice'>",f="qx.bom.Element",b="webkit",d="' ",c="div",a="></";
qx.Class.define(f,{statics:{__hk:{"onload":true,"onpropertychange":true,"oninput":true,"onchange":true,"name":true,"type":true,"checked":true,"disabled":true},__hl:{},__hm:{},allowCreationWithMarkup:function(s){if(!s){s=window;
}var t=s.location.href;

if(qx.bom.Element.__hm[t]==undefined){try{s.document.createElement(g);
qx.bom.Element.__hm[t]=true;
}catch(e){qx.bom.Element.__hm[t]=false;
}}return qx.bom.Element.__hm[t];
},getHelperElement:function(u){if(!u){u=window;
}var w=u.location.href;

if(!qx.bom.Element.__hl[w]){var v=qx.bom.Element.__hl[w]=u.document.createElement(c);
if(qx.core.Environment.get(r)==b){v.style.display=h;
u.document.body.appendChild(v);
}}return qx.bom.Element.__hl[w];
},create:function(name,x,y){if(!y){y=window;
}
if(!name){throw new Error("The tag name is missing!");
}var A=this.__hk;
var z=p;

for(var C in x){if(A[C]){z+=C+k+x[C]+d;
}}var D;
if(z!=p){if(qx.bom.Element.allowCreationWithMarkup(y)){D=y.document.createElement(m+name+o+z+n);
}else{var B=qx.bom.Element.getHelperElement(y);
B.innerHTML=m+name+o+z+a+name+n;
D=B.firstChild;
}}else{D=y.document.createElement(name);
}
for(var C in x){if(!A[C]){qx.bom.element.Attribute.set(D,C,x[C]);
}}return D;
},empty:function(E){return E.innerHTML=p;
},addListener:function(F,G,H,self,I){return qx.event.Registration.addListener(F,G,H,self,I);
},removeListener:function(J,K,L,self,M){return qx.event.Registration.removeListener(J,K,L,self,M);
},removeListenerById:function(N,O){return qx.event.Registration.removeListenerById(N,O);
},hasListener:function(P,Q,R){return qx.event.Registration.hasListener(P,Q,R);
},focus:function(S){qx.event.Registration.getManager(S).getHandler(qx.event.handler.Focus).focus(S);
},blur:function(T){qx.event.Registration.getManager(T).getHandler(qx.event.handler.Focus).blur(T);
},activate:function(U){qx.event.Registration.getManager(U).getHandler(qx.event.handler.Focus).activate(U);
},deactivate:function(V){qx.event.Registration.getManager(V).getHandler(qx.event.handler.Focus).deactivate(V);
},capture:function(W,X){qx.event.Registration.getManager(W).getDispatcher(qx.event.dispatch.MouseCapture).activateCapture(W,X);
},releaseCapture:function(Y){qx.event.Registration.getManager(Y).getDispatcher(qx.event.dispatch.MouseCapture).releaseCapture(Y);
},matchesSelector:function(ba,bb){if(bb){return qx.bom.Selector.query(bb,ba.parentNode).length>0;
}else{return false;
}},clone:function(bc,bd){var bg;

if(bd||((qx.core.Environment.get(r)==q)&&!qx.xml.Document.isXmlDocument(bc))){var bk=qx.event.Registration.getManager(bc);
var be=qx.dom.Hierarchy.getDescendants(bc);
be.push(bc);
}if((qx.core.Environment.get(r)==q)){for(var i=0,l=be.length;i<l;i++){bk.toggleAttachedEvents(be[i],false);
}}var bg=bc.cloneNode(true);
if((qx.core.Environment.get(r)==q)){for(var i=0,l=be.length;i<l;i++){bk.toggleAttachedEvents(be[i],true);
}}if(bd===true){var bn=qx.dom.Hierarchy.getDescendants(bg);
bn.push(bg);
var bf,bi,bm,bh;

for(var i=0,bl=be.length;i<bl;i++){bm=be[i];
bf=bk.serializeListeners(bm);

if(bf.length>0){bi=bn[i];

for(var j=0,bj=bf.length;j<bj;j++){bh=bf[j];
bk.addListener(bi,bh.type,bh.handler,bh.self,bh.capture);
}}}}return bg;
}}});
})();
(function(){var j="",i="undefined",h="engine.name",g="readOnly",f="accessKey",e="qx.bom.element.Attribute",d="rowSpan",c="vAlign",b="className",a="textContent",y="'",x="htmlFor",w="longDesc",v="cellSpacing",u="frameBorder",t="='",s="useMap",r="innerText",q="innerHTML",p="tabIndex",n="dateTime",o="maxLength",l="mshtml",m="cellPadding",k="colSpan";
qx.Class.define(e,{statics:{__hn:{names:{"class":b,"for":x,html:q,text:(qx.core.Environment.get(h)==l)?r:a,colspan:k,rowspan:d,valign:c,datetime:n,accesskey:f,tabindex:p,maxlength:o,readonly:g,longdesc:w,cellpadding:m,cellspacing:v,frameborder:u,usemap:s},runtime:{"html":1,"text":1},bools:{compact:1,nowrap:1,ismap:1,declare:1,noshade:1,checked:1,disabled:1,readOnly:1,multiple:1,selected:1,noresize:1,defer:1,allowTransparency:1},property:{$$html:1,$$widget:1,disabled:1,checked:1,readOnly:1,multiple:1,selected:1,value:1,maxLength:1,className:1,innerHTML:1,innerText:1,textContent:1,htmlFor:1,tabIndex:1},qxProperties:{$$widget:1,$$html:1},propertyDefault:{disabled:false,checked:false,readOnly:false,multiple:false,selected:false,value:j,className:j,innerHTML:j,innerText:j,textContent:j,htmlFor:j,tabIndex:0,maxLength:qx.core.Environment.select(h,{"mshtml":2147483647,"webkit":524288,"default":-1})},removeableProperties:{disabled:1,multiple:1,maxLength:1},original:{href:1,src:1,type:1}},compile:function(z){var A=[];
var C=this.__hn.runtime;

for(var B in z){if(!C[B]){A.push(B,t,z[B],y);
}}return A.join(j);
},get:qx.core.Environment.select(h,{"mshtml":function(D,name){var F=this.__hn;
var E;
name=F.names[name]||name;
if(F.original[name]){E=D.getAttribute(name,2);
}else if(F.property[name]){E=D[name];

if(typeof F.propertyDefault[name]!==i&&E==F.propertyDefault[name]){if(typeof F.bools[name]===i){return null;
}else{return E;
}}}else{E=D.getAttribute(name);
}if(F.bools[name]){return !!E;
}return E;
},"default":function(G,name){var I=this.__hn;
var H;
name=I.names[name]||name;
if(I.property[name]){H=G[name];

if(typeof I.propertyDefault[name]!==i&&H==I.propertyDefault[name]){if(typeof I.bools[name]===i){return null;
}else{return H;
}}}else{H=G.getAttribute(name);
}if(I.bools[name]){return !!H;
}return H;
}}),set:function(J,name,K){if(typeof K===i){return;
}var L=this.__hn;
name=L.names[name]||name;
if(L.bools[name]){K=!!K;
}if(L.property[name]&&(!(J[name]===undefined)||L.qxProperties[name])){if(K==null){if(L.removeableProperties[name]){J.removeAttribute(name);
return;
}else if(typeof L.propertyDefault[name]!==i){K=L.propertyDefault[name];
}}J[name]=K;
}else{if(K===true){J.setAttribute(name,name);
}else if(K===false||K===null){J.removeAttribute(name);
}else{J.setAttribute(name,K);
}}},reset:function(M,name){this.set(M,name,null);
}}});
})();
(function(){var i="engine.name",h="losecapture",g="mshtml",f="blur",e="focus",d="click",c="qx.event.dispatch.MouseCapture",b="capture",a="scroll";
qx.Class.define(c,{extend:qx.event.dispatch.AbstractBubbling,construct:function(j,k){qx.event.dispatch.AbstractBubbling.call(this,j);
this.__cf=j.getWindow();
this.__ch=k;
j.addListener(this.__cf,f,this.releaseCapture,this);
j.addListener(this.__cf,e,this.releaseCapture,this);
j.addListener(this.__cf,a,this.releaseCapture,this);
},statics:{PRIORITY:qx.event.Registration.PRIORITY_FIRST},members:{__ch:null,__ho:null,__hp:true,__cf:null,_getParent:function(l){return l.parentNode;
},canDispatchEvent:function(m,event,n){return !!(this.__ho&&this.__hq[n]);
},dispatchEvent:function(o,event,p){if(p==d){event.stopPropagation();
this.releaseCapture();
return;
}
if(this.__hp||!qx.dom.Hierarchy.contains(this.__ho,o)){o=this.__ho;
}qx.event.dispatch.AbstractBubbling.prototype.dispatchEvent.call(this,o,event,p);
},__hq:{"mouseup":1,"mousedown":1,"click":1,"dblclick":1,"mousemove":1,"mouseout":1,"mouseover":1},activateCapture:function(q,r){var r=r!==false;

if(this.__ho===q&&this.__hp==r){return;
}
if(this.__ho){this.releaseCapture();
}this.nativeSetCapture(q,r);

if(this.hasNativeCapture){var self=this;
qx.bom.Event.addNativeListener(q,h,function(){qx.bom.Event.removeNativeListener(q,h,arguments.callee);
self.releaseCapture();
});
}this.__hp=r;
this.__ho=q;
this.__ch.fireEvent(q,b,qx.event.type.Event,[true,false]);
},getCaptureElement:function(){return this.__ho;
},releaseCapture:function(){var s=this.__ho;

if(!s){return;
}this.__ho=null;
this.__ch.fireEvent(s,h,qx.event.type.Event,[true,false]);
this.nativeReleaseCapture(s);
},hasNativeCapture:qx.core.Environment.get(i)==g,nativeSetCapture:qx.core.Environment.select(i,{"mshtml":function(t,u){t.setCapture(u!==false);
},"default":qx.lang.Function.empty}),nativeReleaseCapture:qx.core.Environment.select(i,{"mshtml":function(v){v.releaseCapture();
},"default":qx.lang.Function.empty})},destruct:function(){this.__ho=this.__cf=this.__ch=null;
},defer:function(w){qx.event.Registration.addDispatcher(w);
}});
})();
(function(){var c="qx.bom.Selector";
qx.Class.define(c,{statics:{query:null,matches:null}});
(function(){var o=/((?:\((?:\([^()]+\)|[^()]+)+\)|\[(?:\[[^\[\]]*\]|['"][^'"]*['"]|[^\[\]'"]+)+\]|\\.|[^ >+~,(\[\\]+)+|[>+~])(\s*,\s*)?((?:.|\r|\n)*)/g,v=0,x=Object.prototype.toString,p=false,z=true,t=/\\/g,g=/\W/;
[0,0].sort(function(){z=false;
return 0;
});
var s=function(B,C,D,E){D=D||[];
C=C||document;
var N=C;

if(C.nodeType!==1&&C.nodeType!==9){return [];
}
if(!B||typeof B!=="string"){return D;
}var m,H,F,J,L,I,O,i,P=true,G=s.isXML(C),K=[],M=B;
do{o.exec("");
m=o.exec(M);

if(m){M=m[3];
K.push(m[1]);

if(m[2]){J=m[3];
break;
}}}while(m);

if(K.length>1&&q.exec(B)){if(K.length===2&&k.relative[K[0]]){H=h(K[0]+K[1],C);
}else{H=k.relative[K[0]]?[C]:s(K.shift(),C);

while(K.length){B=K.shift();

if(k.relative[B]){B+=K.shift();
}H=h(B,H);
}}}else{if(!E&&K.length>1&&C.nodeType===9&&!G&&k.match.ID.test(K[0])&&!k.match.ID.test(K[K.length-1])){L=s.find(K.shift(),C,G);
C=L.expr?s.filter(L.expr,L.set)[0]:L.set[0];
}
if(C){L=E?{expr:K.pop(),set:f(E)}:s.find(K.pop(),K.length===1&&(K[0]==="~"||K[0]==="+")&&C.parentNode?C.parentNode:C,G);
H=L.expr?s.filter(L.expr,L.set):L.set;

if(K.length>0){F=f(H);
}else{P=false;
}
while(K.length){I=K.pop();
O=I;

if(!k.relative[I]){I="";
}else{O=K.pop();
}
if(O==null){O=C;
}k.relative[I](F,O,G);
}}else{F=K=[];
}}
if(!F){F=H;
}
if(!F){s.error(I||B);
}
if(x.call(F)==="[object Array]"){if(!P){D.push.apply(D,F);
}else if(C&&C.nodeType===1){for(i=0;F[i]!=null;i++){if(F[i]&&(F[i]===true||F[i].nodeType===1&&s.contains(C,F[i]))){D.push(H[i]);
}}}else{for(i=0;F[i]!=null;i++){if(F[i]&&F[i].nodeType===1){D.push(H[i]);
}}}}else{f(F,D);
}
if(J){s(J,N,D,E);
s.uniqueSort(D);
}return D;
};
s.uniqueSort=function(Q){if(u){p=z;
Q.sort(u);

if(p){for(var i=1;i<Q.length;i++){if(Q[i]===Q[i-1]){Q.splice(i--,1);
}}}}return Q;
};
s.matches=function(R,S){return s(R,null,null,S);
};
s.matchesSelector=function(T,U){return s(U,null,null,[T]).length>0;
};
s.find=function(V,W,X){var Y;

if(!V){return [];
}
for(var i=0,l=k.order.length;i<l;i++){var bb,ba=k.order[i];

if((bb=k.leftMatch[ba].exec(V))){var bc=bb[1];
bb.splice(1,1);

if(bc.substr(bc.length-1)!=="\\"){bb[1]=(bb[1]||"").replace(t,"");
Y=k.find[ba](bb,W,X);

if(Y!=null){V=V.replace(k.match[ba],"");
break;
}}}}
if(!Y){Y=typeof W.getElementsByTagName!=="undefined"?W.getElementsByTagName("*"):[];
}return {set:Y,expr:V};
};
s.filter=function(bd,be,bf,bg){var bt,bs,bh=bd,bn=[],bi=be,bj=be&&be[0]&&s.isXML(be[0]);

while(bd&&be.length){for(var br in k.filter){if((bt=k.leftMatch[br].exec(bd))!=null&&bt[2]){var bq,bm,bk=k.filter[br],bu=bt[1];
bs=false;
bt.splice(1,1);

if(bu.substr(bu.length-1)==="\\"){continue;
}
if(bi===bn){bn=[];
}
if(k.preFilter[br]){bt=k.preFilter[br](bt,bi,bf,bn,bg,bj);

if(!bt){bs=bq=true;
}else if(bt===true){continue;
}}
if(bt){for(var i=0;(bm=bi[i])!=null;i++){if(bm){bq=bk(bm,bt,i,bi);
var bo=bg^!!bq;

if(bf&&bq!=null){if(bo){bs=true;
}else{bi[i]=false;
}}else if(bo){bn.push(bm);
bs=true;
}}}}
if(bq!==undefined){if(!bf){bi=bn;
}bd=bd.replace(k.match[br],"");

if(!bs){return [];
}break;
}}}if(bd===bh){if(bs==null){s.error(bd);
}else{break;
}}bh=bd;
}return bi;
};
s.error=function(bv){throw "Syntax error, unrecognized expression: "+bv;
};
var k=s.selectors={order:["ID","NAME","TAG"],match:{ID:/#((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,CLASS:/\.((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,NAME:/\[name=['"]*((?:[\w\u00c0-\uFFFF\-]|\\.)+)['"]*\]/,ATTR:/\[\s*((?:[\w\u00c0-\uFFFF\-]|\\.)+)\s*(?:(\S?=)\s*(?:(['"])(.*?)\3|(#?(?:[\w\u00c0-\uFFFF\-]|\\.)*)|)|)\s*\]/,TAG:/^((?:[\w\u00c0-\uFFFF\*\-]|\\.)+)/,CHILD:/:(only|nth|last|first)-child(?:\(\s*(even|odd|(?:[+\-]?\d+|(?:[+\-]?\d*)?n\s*(?:[+\-]\s*\d+)?))\s*\))?/,POS:/:(nth|eq|gt|lt|first|last|even|odd)(?:\((\d*)\))?(?=[^\-]|$)/,PSEUDO:/:((?:[\w\u00c0-\uFFFF\-]|\\.)+)(?:\((['"]?)((?:\([^\)]+\)|[^\(\)]*)+)\2\))?/},leftMatch:{},attrMap:{"class":"className","for":"htmlFor"},attrHandle:{href:function(bw){return bw.getAttribute("href");
},type:function(bx){return bx.getAttribute("type");
}},relative:{"+":function(by,bz){var bA=typeof bz==="string",bC=bA&&!g.test(bz),bD=bA&&!bC;

if(bC){bz=bz.toLowerCase();
}
for(var i=0,l=by.length,bB;i<l;i++){if((bB=by[i])){while((bB=bB.previousSibling)&&bB.nodeType!==1){}by[i]=bD||bB&&bB.nodeName.toLowerCase()===bz?bB||false:bB===bz;
}}
if(bD){s.filter(bz,by,true);
}},">":function(bE,bF){var bH,bG=typeof bF==="string",i=0,l=bE.length;

if(bG&&!g.test(bF)){bF=bF.toLowerCase();

for(;i<l;i++){bH=bE[i];

if(bH){var parent=bH.parentNode;
bE[i]=parent.nodeName.toLowerCase()===bF?parent:false;
}}}else{for(;i<l;i++){bH=bE[i];

if(bH){bE[i]=bG?bH.parentNode:bH.parentNode===bF;
}}
if(bG){s.filter(bF,bE,true);
}}},"":function(bI,bJ,bK){var bN,bL=v++,bM=y;

if(typeof bJ==="string"&&!g.test(bJ)){bJ=bJ.toLowerCase();
bN=bJ;
bM=A;
}bM("parentNode",bJ,bL,bI,bN,bK);
},"~":function(bO,bP,bQ){var bT,bR=v++,bS=y;

if(typeof bP==="string"&&!g.test(bP)){bP=bP.toLowerCase();
bT=bP;
bS=A;
}bS("previousSibling",bP,bR,bO,bT,bQ);
}},find:{ID:function(bU,bV,bW){if(typeof bV.getElementById!=="undefined"&&!bW){var m=bV.getElementById(bU[1]);
return m&&m.parentNode?[m]:[];
}},NAME:function(bX,bY){if(typeof bY.getElementsByName!=="undefined"){var cb=[],ca=bY.getElementsByName(bX[1]);

for(var i=0,l=ca.length;i<l;i++){if(ca[i].getAttribute("name")===bX[1]){cb.push(ca[i]);
}}return cb.length===0?null:cb;
}},TAG:function(cc,cd){if(typeof cd.getElementsByTagName!=="undefined"){return cd.getElementsByTagName(cc[1]);
}}},preFilter:{CLASS:function(ce,cf,cg,ch,ci,cj){ce=" "+ce[1].replace(t,"")+" ";

if(cj){return ce;
}
for(var i=0,ck;(ck=cf[i])!=null;i++){if(ck){if(ci^(ck.className&&(" "+ck.className+" ").replace(/[\t\n\r]/g," ").indexOf(ce)>=0)){if(!cg){ch.push(ck);
}}else if(cg){cf[i]=false;
}}}return false;
},ID:function(cl){return cl[1].replace(t,"");
},TAG:function(cm,cn){return cm[1].replace(t,"").toLowerCase();
},CHILD:function(co){if(co[1]==="nth"){if(!co[2]){s.error(co[0]);
}co[2]=co[2].replace(/^\+|\s*/g,'');
var cp=/(-?)(\d*)(?:n([+\-]?\d*))?/.exec(co[2]==="even"&&"2n"||co[2]==="odd"&&"2n+1"||!/\D/.test(co[2])&&"0n+"+co[2]||co[2]);
co[2]=(cp[1]+(cp[2]||1))-0;
co[3]=cp[3]-0;
}else if(co[2]){s.error(co[0]);
}co[0]=v++;
return co;
},ATTR:function(cq,cr,cs,ct,cu,cv){var name=cq[1]=cq[1].replace(t,"");

if(!cv&&k.attrMap[name]){cq[1]=k.attrMap[name];
}cq[4]=(cq[4]||cq[5]||"").replace(t,"");

if(cq[2]==="~="){cq[4]=" "+cq[4]+" ";
}return cq;
},PSEUDO:function(cw,cx,cy,cz,cA){if(cw[1]==="not"){if((o.exec(cw[3])||"").length>1||/^\w/.test(cw[3])){cw[3]=s(cw[3],null,null,cx);
}else{var cB=s.filter(cw[3],cx,cy,true^cA);

if(!cy){cz.push.apply(cz,cB);
}return false;
}}else if(k.match.POS.test(cw[0])||k.match.CHILD.test(cw[0])){return true;
}return cw;
},POS:function(cC){cC.unshift(true);
return cC;
}},filters:{enabled:function(cD){return cD.disabled===false&&cD.type!=="hidden";
},disabled:function(cE){return cE.disabled===true;
},checked:function(cF){return cF.checked===true;
},selected:function(cG){if(cG.parentNode){cG.parentNode.selectedIndex;
}return cG.selected===true;
},parent:function(cH){return !!cH.firstChild;
},empty:function(cI){return !cI.firstChild;
},has:function(cJ,i,cK){return !!s(cK[3],cJ).length;
},header:function(cL){return (/h\d/i).test(cL.nodeName);
},text:function(cM){return "text"===cM.getAttribute('type');
},radio:function(cN){return "radio"===cN.type;
},checkbox:function(cO){return "checkbox"===cO.type;
},file:function(cP){return "file"===cP.type;
},password:function(cQ){return "password"===cQ.type;
},submit:function(cR){return "submit"===cR.type;
},image:function(cS){return "image"===cS.type;
},reset:function(cT){return "reset"===cT.type;
},button:function(cU){return "button"===cU.type||cU.nodeName.toLowerCase()==="button";
},input:function(cV){return (/input|select|textarea|button/i).test(cV.nodeName);
}},setFilters:{first:function(cW,i){return i===0;
},last:function(cX,i,cY,da){return i===da.length-1;
},even:function(db,i){return i%2===0;
},odd:function(dc,i){return i%2===1;
},lt:function(dd,i,de){return i<de[3]-0;
},gt:function(df,i,dg){return i>dg[3]-0;
},nth:function(dh,i,di){return di[3]-0===i;
},eq:function(dj,i,dk){return dk[3]-0===i;
}},filter:{PSEUDO:function(dl,dm,i,dn){var name=dm[1],dp=k.filters[name];

if(dp){return dp(dl,i,dm,dn);
}else if(name==="contains"){return (dl.textContent||dl.innerText||s.getText([dl])||"").indexOf(dm[3])>=0;
}else if(name==="not"){var dq=dm[3];

for(var j=0,l=dq.length;j<l;j++){if(dq[j]===dl){return false;
}}return true;
}else{s.error(name);
}},CHILD:function(dr,ds){var dy=ds[1],dt=dr;

switch(dy){case "only":case "first":while((dt=dt.previousSibling)){if(dt.nodeType===1){return false;
}}
if(dy==="first"){return true;
}dt=dr;
case "last":while((dt=dt.nextSibling)){if(dt.nodeType===1){return false;
}}return true;
case "nth":var dz=ds[2],dv=ds[3];

if(dz===1&&dv===0){return true;
}var dx=ds[0],parent=dr.parentNode;

if(parent&&(parent.sizcache!==dx||!dr.nodeIndex)){var du=0;

for(dt=parent.firstChild;dt;dt=dt.nextSibling){if(dt.nodeType===1){dt.nodeIndex=++du;
}}parent.sizcache=dx;
}var dw=dr.nodeIndex-dv;

if(dz===0){return dw===0;
}else{return (dw%dz===0&&dw/dz>=0);
}}},ID:function(dA,dB){return dA.nodeType===1&&dA.getAttribute("id")===dB;
},TAG:function(dC,dD){return (dD==="*"&&dC.nodeType===1)||dC.nodeName.toLowerCase()===dD;
},CLASS:function(dE,dF){return (" "+(dE.className||dE.getAttribute("class"))+" ").indexOf(dF)>-1;
},ATTR:function(dG,dH){var name=dH[1],dL=k.attrHandle[name]?k.attrHandle[name](dG):dG[name]!=null?dG[name]:dG.getAttribute(name),dK=dL+"",dJ=dH[2],dI=dH[4];
return dL==null?dJ==="!=":dJ==="="?dK===dI:dJ==="*="?dK.indexOf(dI)>=0:dJ==="~="?(" "+dK+" ").indexOf(dI)>=0:!dI?dK&&dL!==false:dJ==="!="?dK!==dI:dJ==="^="?dK.indexOf(dI)===0:dJ==="$="?dK.substr(dK.length-dI.length)===dI:dJ==="|="?dK===dI||dK.substr(0,dI.length+1)===dI+"-":false;
},POS:function(dM,dN,i,dO){var name=dN[2],dP=k.setFilters[name];

if(dP){return dP(dM,i,dN,dO);
}}}};
var q=k.match.POS,d=function(dQ,dR){return "\\"+(dR-0+1);
};

for(var w in k.match){k.match[w]=new RegExp(k.match[w].source+(/(?![^\[]*\])(?![^\(]*\))/.source));
k.leftMatch[w]=new RegExp(/(^(?:.|\r|\n)*?)/.source+k.match[w].source.replace(/\\(\d+)/g,d));
}var f=function(dS,dT){dS=Array.prototype.slice.call(dS,0);

if(dT){dT.push.apply(dT,dS);
return dT;
}return dS;
};
try{Array.prototype.slice.call(document.documentElement.childNodes,0)[0].nodeType;
}catch(e){f=function(dU,dV){var i=0,dW=dV||[];

if(x.call(dU)==="[object Array]"){Array.prototype.push.apply(dW,dU);
}else{if(typeof dU.length==="number"){for(var l=dU.length;i<l;i++){dW.push(dU[i]);
}}else{for(;dU[i];i++){dW.push(dU[i]);
}}}return dW;
};
}var u,n;

if(document.documentElement.compareDocumentPosition){u=function(a,b){if(a===b){p=true;
return 0;
}
if(!a.compareDocumentPosition||!b.compareDocumentPosition){return a.compareDocumentPosition?-1:1;
}return a.compareDocumentPosition(b)&4?-1:1;
};
}else{u=function(a,b){var ec,ea,ed=[],ee=[],dY=a.parentNode,eb=b.parentNode,dX=dY;
if(a===b){p=true;
return 0;
}else if(dY===eb){return n(a,b);
}else if(!dY){return -1;
}else if(!eb){return 1;
}while(dX){ed.unshift(dX);
dX=dX.parentNode;
}dX=eb;

while(dX){ee.unshift(dX);
dX=dX.parentNode;
}ec=ed.length;
ea=ee.length;
for(var i=0;i<ec&&i<ea;i++){if(ed[i]!==ee[i]){return n(ed[i],ee[i]);
}}return i===ec?n(a,ee[i],-1):n(ed[i],b,1);
};
n=function(a,b,ef){if(a===b){return ef;
}var eg=a.nextSibling;

while(eg){if(eg===b){return -1;
}eg=eg.nextSibling;
}return 1;
};
}s.getText=function(eh){var ej="",ei;

for(var i=0;eh[i];i++){ei=eh[i];
if(ei.nodeType===3||ei.nodeType===4){ej+=ei.nodeValue;
}else if(ei.nodeType!==8){ej+=s.getText(ei.childNodes);
}}return ej;
};
(function(){var em=document.createElement("div"),el="script"+(new Date()).getTime(),ek=document.documentElement;
em.innerHTML="<a name='"+el+"'/>";
ek.insertBefore(em,ek.firstChild);
if(document.getElementById(el)){k.find.ID=function(en,eo,ep){if(typeof eo.getElementById!=="undefined"&&!ep){var m=eo.getElementById(en[1]);
return m?m.id===en[1]||typeof m.getAttributeNode!=="undefined"&&m.getAttributeNode("id").nodeValue===en[1]?[m]:undefined:[];
}};
k.filter.ID=function(eq,er){var es=typeof eq.getAttributeNode!=="undefined"&&eq.getAttributeNode("id");
return eq.nodeType===1&&es&&es.nodeValue===er;
};
}ek.removeChild(em);
ek=em=null;
})();
(function(){var et=document.createElement("div");
et.appendChild(document.createComment(""));
if(et.getElementsByTagName("*").length>0){k.find.TAG=function(eu,ev){var ex=ev.getElementsByTagName(eu[1]);
if(eu[1]==="*"){var ew=[];

for(var i=0;ex[i];i++){if(ex[i].nodeType===1){ew.push(ex[i]);
}}ex=ew;
}return ex;
};
}et.innerHTML="<a href='#'></a>";

if(et.firstChild&&typeof et.firstChild.getAttribute!=="undefined"&&et.firstChild.getAttribute("href")!=="#"){k.attrHandle.href=function(ey){return ey.getAttribute("href",2);
};
}et=null;
})();

if(document.querySelectorAll){(function(){var eA=s,ez=document.createElement("div"),eB="__sizzle__";
ez.innerHTML="<p class='TEST'></p>";
if(ez.querySelectorAll&&ez.querySelectorAll(".TEST").length===0){return;
}s=function(eD,eE,eF,eG){eE=eE||document;
if(!eG&&!s.isXML(eE)){var eL=/^(\w+$)|^\.([\w\-]+$)|^#([\w\-]+$)/.exec(eD);

if(eL&&(eE.nodeType===1||eE.nodeType===9)){if(eL[1]){return f(eE.getElementsByTagName(eD),eF);
}else if(eL[2]&&k.find.CLASS&&eE.getElementsByClassName){return f(eE.getElementsByClassName(eL[2]),eF);
}}
if(eE.nodeType===9){if(eD==="body"&&eE.body){return f([eE.body],eF);
}else if(eL&&eL[3]){var eJ=eE.getElementById(eL[3]);
if(eJ&&eJ.parentNode){if(eJ.id===eL[3]){return f([eJ],eF);
}}else{return f([],eF);
}}
try{return f(eE.querySelectorAll(eD),eF);
}catch(eO){}}else if(eE.nodeType===1&&eE.nodeName.toLowerCase()!=="object"){var eN=eE,eI=eE.getAttribute("id"),eK=eI||eB,eH=eE.parentNode,eM=/^\s*[+~]/.test(eD);

if(!eI){eE.setAttribute("id",eK);
}else{eK=eK.replace(/'/g,"\\$&");
}
if(eM&&eH){eE=eE.parentNode;
}
try{if(!eM||eH){return f(eE.querySelectorAll("[id='"+eK+"'] "+eD),eF);
}}catch(eP){}finally{if(!eI){eN.removeAttribute("id");
}}}}return eA(eD,eE,eF,eG);
};

for(var eC in eA){s[eC]=eA[eC];
}ez=null;
})();
}(function(){var eS=document.documentElement,eQ=eS.matchesSelector||eS.mozMatchesSelector||eS.webkitMatchesSelector||eS.msMatchesSelector,eR=false;

try{eQ.call(document.documentElement,"[test!='']:sizzle");
}catch(eT){eR=true;
}
if(eQ){s.matchesSelector=function(eU,eV){eV=eV.replace(/\=\s*([^'"\]]*)\s*\]/g,"='$1']");

if(!s.isXML(eU)){try{if(eR||!k.match.PSEUDO.test(eV)&&!/!=/.test(eV)){return eQ.call(eU,eV);
}}catch(e){}}return s(eV,null,null,[eU]).length>0;
};
}})();
(function(){var eW=document.createElement("div");
eW.innerHTML="<div class='test e'></div><div class='test'></div>";
if(!eW.getElementsByClassName||eW.getElementsByClassName("e").length===0){return;
}eW.lastChild.className="e";

if(eW.getElementsByClassName("e").length===1){return;
}k.order.splice(1,0,"CLASS");
k.find.CLASS=function(eX,eY,fa){if(typeof eY.getElementsByClassName!=="undefined"&&!fa){return eY.getElementsByClassName(eX[1]);
}};
eW=null;
})();
function A(fb,fc,fd,fe,ff,fg){for(var i=0,l=fe.length;i<l;i++){var fi=fe[i];

if(fi){var fh=false;
fi=fi[fb];

while(fi){if(fi.sizcache===fd){fh=fe[fi.sizset];
break;
}
if(fi.nodeType===1&&!fg){fi.sizcache=fd;
fi.sizset=i;
}
if(fi.nodeName.toLowerCase()===fc){fh=fi;
break;
}fi=fi[fb];
}fe[i]=fh;
}}}function y(fj,fk,fl,fm,fn,fo){for(var i=0,l=fm.length;i<l;i++){var fq=fm[i];

if(fq){var fp=false;
fq=fq[fj];

while(fq){if(fq.sizcache===fl){fp=fm[fq.sizset];
break;
}
if(fq.nodeType===1){if(!fo){fq.sizcache=fl;
fq.sizset=i;
}
if(typeof fk!=="string"){if(fq===fk){fp=true;
break;
}}else if(s.filter(fk,[fq]).length>0){fp=fq;
break;
}}fq=fq[fj];
}fm[i]=fp;
}}}
if(document.documentElement.contains){s.contains=function(a,b){return a!==b&&(a.contains?a.contains(b):true);
};
}else if(document.documentElement.compareDocumentPosition){s.contains=function(a,b){return !!(a.compareDocumentPosition(b)&16);
};
}else{s.contains=function(){return false;
};
}s.isXML=function(fr){var fs=(fr?fr.ownerDocument||fr:0).documentElement;
return fs?fs.nodeName!=="HTML":false;
};
var h=function(ft,fu){var fy,fw=[],fv="",fx=fu.nodeType?[fu]:fu;
while((fy=k.match.PSEUDO.exec(ft))){fv+=fy[0];
ft=ft.replace(k.match.PSEUDO,"");
}ft=k.relative[ft]?ft+"*":ft;

for(var i=0,l=fx.length;i<l;i++){s(ft,fx[i],fw);
}return s.filter(fv,fw);
};
var r=qx.bom.Selector;
r.query=function(fz,fA){return s(fz,fA);
};
r.matches=function(fB,fC){return s(fB,null,null,fC);
};
})();
})();
(function(){var r="engine.name",q="",p="MSXML2.DOMDocument.3.0",o="mshtml",n="SelectionLanguage",m="qx.xml.Document",k=" />",j="'",h="MSXML2.XMLHTTP.3.0",g="MSXML2.XMLHTTP.6.0",c=" xmlns='",f='<\?xml version="1.0" encoding="utf-8"?>\n<',e="text/xml",b="XPath",a="MSXML2.DOMDocument.6.0",d="HTML";
qx.Class.define(m,{statics:{DOMDOC:null,XMLHTTP:null,isXmlDocument:function(s){if(s.nodeType===9){return s.documentElement.nodeName!==d;
}else if(s.ownerDocument){return this.isXmlDocument(s.ownerDocument);
}else{return false;
}},create:qx.core.Environment.select(r,{"mshtml":function(t,u){var v=new ActiveXObject(this.DOMDOC);
if(this.DOMDOC==p){v.setProperty(n,b);
}
if(u){var w=f;
w+=u;

if(t){w+=c+t+j;
}w+=k;
v.loadXML(w);
}return v;
},"default":function(x,y){return document.implementation.createDocument(x||q,y||q,null);
}}),fromString:qx.core.Environment.select(r,{"mshtml":function(z){var A=qx.xml.Document.create();
A.loadXML(z);
return A;
},"default":function(B){var C=new DOMParser();
return C.parseFromString(B,e);
}})},defer:function(D){if((qx.core.Environment.get(r)==o)){var E=[a,p];
var F=[g,h];

for(var i=0,l=E.length;i<l;i++){try{new ActiveXObject(E[i]);
new ActiveXObject(F[i]);
}catch(G){continue;
}D.DOMDOC=E[i];
D.XMLHTTP=F[i];
break;
}}}});
})();
(function(){var a="qx.event.type.Focus";
qx.Class.define(a,{extend:qx.event.type.Event,members:{init:function(b,c,d){qx.event.type.Event.prototype.init.call(this,d,false);
this._target=b;
this._relatedTarget=c;
return this;
}}});
})();
(function(){var k="visible",j="scroll",i="borderBottomWidth",h="borderTopWidth",g="left",f="borderLeftWidth",e="bottom",d="top",c="right",b="qx.bom.element.Scroll",a="borderRightWidth";
qx.Class.define(b,{statics:{intoViewX:function(l,stop,m){var parent=l.parentNode;
var r=qx.dom.Node.getDocument(l);
var n=r.body;
var z,x,u;
var B,s,C;
var v,D,G;
var E,p,y,o;
var t,F,w;
var q=m===g;
var A=m===c;
stop=stop?stop.parentNode:r;
while(parent&&parent!=stop){if(parent.scrollWidth>parent.clientWidth&&(parent===n||qx.bom.element.Overflow.getY(parent)!=k)){if(parent===n){x=parent.scrollLeft;
u=x+qx.bom.Viewport.getWidth();
B=qx.bom.Viewport.getWidth();
s=parent.clientWidth;
C=parent.scrollWidth;
v=0;
D=0;
G=0;
}else{z=qx.bom.element.Location.get(parent);
x=z.left;
u=z.right;
B=parent.offsetWidth;
s=parent.clientWidth;
C=parent.scrollWidth;
v=parseInt(qx.bom.element.Style.get(parent,f),10)||0;
D=parseInt(qx.bom.element.Style.get(parent,a),10)||0;
G=B-s-v-D;
}E=qx.bom.element.Location.get(l);
p=E.left;
y=E.right;
o=l.offsetWidth;
t=p-x-v;
F=y-u+D;
w=0;
if(q){w=t;
}else if(A){w=F+G;
}else if(t<0||o>s){w=t;
}else if(F>0){w=F+G;
}parent.scrollLeft+=w;
qx.event.Registration.fireNonBubblingEvent(parent,j);
}
if(parent===n){break;
}parent=parent.parentNode;
}},intoViewY:function(H,stop,I){var parent=H.parentNode;
var O=qx.dom.Node.getDocument(H);
var J=O.body;
var W,K,S;
var Y,V,Q;
var M,N,L;
var bb,bc,X,R;
var U,P,bd;
var ba=I===d;
var T=I===e;
stop=stop?stop.parentNode:O;
while(parent&&parent!=stop){if(parent.scrollHeight>parent.clientHeight&&(parent===J||qx.bom.element.Overflow.getY(parent)!=k)){if(parent===J){K=parent.scrollTop;
S=K+qx.bom.Viewport.getHeight();
Y=qx.bom.Viewport.getHeight();
V=parent.clientHeight;
Q=parent.scrollHeight;
M=0;
N=0;
L=0;
}else{W=qx.bom.element.Location.get(parent);
K=W.top;
S=W.bottom;
Y=parent.offsetHeight;
V=parent.clientHeight;
Q=parent.scrollHeight;
M=parseInt(qx.bom.element.Style.get(parent,h),10)||0;
N=parseInt(qx.bom.element.Style.get(parent,i),10)||0;
L=Y-V-M-N;
}bb=qx.bom.element.Location.get(H);
bc=bb.top;
X=bb.bottom;
R=H.offsetHeight;
U=bc-K-M;
P=X-S+N;
bd=0;
if(ba){bd=U;
}else if(T){bd=P+L;
}else if(U<0||R>V){bd=U;
}else if(P>0){bd=P+L;
}parent.scrollTop+=bd;
qx.event.Registration.fireNonBubblingEvent(parent,j);
}
if(parent===J){break;
}parent=parent.parentNode;
}},intoView:function(be,stop,bf,bg){this.intoViewX(be,stop,bf);
this.intoViewY(be,stop,bg);
}}});
})();
(function(){var j="borderTopWidth",i="borderLeftWidth",h="marginTop",g="marginLeft",f="engine.name",e="scroll",d="engine.version",c="border-box",b="borderBottomWidth",a="borderRightWidth",C="auto",B="padding",A="browser.quirksmode",z="qx.bom.element.Location",y="paddingLeft",x="static",w="marginBottom",v="visible",u="BODY",t="opera",q="paddingBottom",r="paddingTop",o="marginRight",p="position",m="margin",n="overflow",k="paddingRight",l="browser.documentmode",s="border";
qx.Class.define(z,{statics:{__hr:function(D,E){return qx.bom.element.Style.get(D,E,qx.bom.element.Style.COMPUTED_MODE,false);
},__hs:function(F,G){return parseInt(qx.bom.element.Style.get(F,G,qx.bom.element.Style.COMPUTED_MODE,false),10)||0;
},__ht:function(H){var K=0,top=0;
if(H.getBoundingClientRect&&qx.core.Environment.get(f)!=t){var J=qx.dom.Node.getWindow(H);
K-=qx.bom.Viewport.getScrollLeft(J);
top-=qx.bom.Viewport.getScrollTop(J);
}else{var I=qx.dom.Node.getDocument(H).body;
H=H.parentNode;
while(H&&H!=I){K+=H.scrollLeft;
top+=H.scrollTop;
H=H.parentNode;
}}return {left:K,top:top};
},__hu:qx.core.Environment.select(f,{"mshtml":function(L){var N=qx.dom.Node.getDocument(L);
var M=N.body;
var O=0;
var top=0;
O-=M.clientLeft+N.documentElement.clientLeft;
top-=M.clientTop+N.documentElement.clientTop;

if(!qx.core.Environment.get(A)){O+=this.__hs(M,i);
top+=this.__hs(M,j);
}return {left:O,top:top};
},"webkit":function(P){var R=qx.dom.Node.getDocument(P);
var Q=R.body;
var S=Q.offsetLeft;
var top=Q.offsetTop;
if(parseFloat(qx.core.Environment.get(d))<530.17){S+=this.__hs(Q,i);
top+=this.__hs(Q,j);
}return {left:S,top:top};
},"gecko":function(T){var U=qx.dom.Node.getDocument(T).body;
var V=U.offsetLeft;
var top=U.offsetTop;
if(parseFloat(qx.core.Environment.get(d))<1.9){V+=this.__hs(U,g);
top+=this.__hs(U,h);
}if(qx.bom.element.BoxSizing.get(U)!==c){V+=this.__hs(U,i);
top+=this.__hs(U,j);
}return {left:V,top:top};
},"default":function(W){var X=qx.dom.Node.getDocument(W).body;
var Y=X.offsetLeft;
var top=X.offsetTop;
return {left:Y,top:top};
}}),__hv:qx.core.Environment.select(f,{"mshtml|webkit":function(ba){var bc=qx.dom.Node.getDocument(ba);
if(ba.getBoundingClientRect){var bd=ba.getBoundingClientRect();
var be=bd.left;
var top=bd.top;
}else{var be=ba.offsetLeft;
var top=ba.offsetTop;
ba=ba.offsetParent;
var bb=bc.body;
while(ba&&ba!=bb){be+=ba.offsetLeft;
top+=ba.offsetTop;
be+=this.__hs(ba,i);
top+=this.__hs(ba,j);
ba=ba.offsetParent;
}}return {left:be,top:top};
},"gecko":function(bf){if(bf.getBoundingClientRect){var bi=bf.getBoundingClientRect();
var bj=Math.round(bi.left);
var top=Math.round(bi.top);
}else{var bj=0;
var top=0;
var bg=qx.dom.Node.getDocument(bf).body;
var bh=qx.bom.element.BoxSizing;

if(bh.get(bf)!==c){bj-=this.__hs(bf,i);
top-=this.__hs(bf,j);
}
while(bf&&bf!==bg){bj+=bf.offsetLeft;
top+=bf.offsetTop;
if(bh.get(bf)!==c){bj+=this.__hs(bf,i);
top+=this.__hs(bf,j);
}if(bf.parentNode&&this.__hr(bf.parentNode,n)!=v){bj+=this.__hs(bf.parentNode,i);
top+=this.__hs(bf.parentNode,j);
}bf=bf.offsetParent;
}}return {left:bj,top:top};
},"default":function(bk){var bm=0;
var top=0;
var bl=qx.dom.Node.getDocument(bk).body;
while(bk&&bk!==bl){bm+=bk.offsetLeft;
top+=bk.offsetTop;
bk=bk.offsetParent;
}return {left:bm,top:top};
}}),get:function(bn,bo){if(bn.tagName==u){var location=this.__hw(bn);
var bv=location.left;
var top=location.top;
}else{var bp=this.__hu(bn);
var bu=this.__hv(bn);
var scroll=this.__ht(bn);
var bv=bu.left+bp.left-scroll.left;
var top=bu.top+bp.top-scroll.top;
}var bq=bv+bn.offsetWidth;
var br=top+bn.offsetHeight;

if(bo){if(bo==B||bo==e){var bs=qx.bom.element.Overflow.getX(bn);

if(bs==e||bs==C){bq+=bn.scrollWidth-bn.offsetWidth+this.__hs(bn,i)+this.__hs(bn,a);
}var bt=qx.bom.element.Overflow.getY(bn);

if(bt==e||bt==C){br+=bn.scrollHeight-bn.offsetHeight+this.__hs(bn,j)+this.__hs(bn,b);
}}
switch(bo){case B:bv+=this.__hs(bn,y);
top+=this.__hs(bn,r);
bq-=this.__hs(bn,k);
br-=this.__hs(bn,q);
case e:bv-=bn.scrollLeft;
top-=bn.scrollTop;
bq-=bn.scrollLeft;
br-=bn.scrollTop;
case s:bv+=this.__hs(bn,i);
top+=this.__hs(bn,j);
bq-=this.__hs(bn,a);
br-=this.__hs(bn,b);
break;
case m:bv-=this.__hs(bn,g);
top-=this.__hs(bn,h);
bq+=this.__hs(bn,o);
br+=this.__hs(bn,w);
break;
}}return {left:bv,top:top,right:bq,bottom:br};
},__hw:qx.core.Environment.select(f,{"default":function(bw){var top=bw.offsetTop+this.__hs(bw,h);
var bx=bw.offsetLeft+this.__hs(bw,g);
return {left:bx,top:top};
},"mshtml":function(by){var top=by.offsetTop;
var bz=by.offsetLeft;

if(!((parseFloat(qx.core.Environment.get(d))<8||qx.core.Environment.get(l)<8)&&!qx.core.Environment.get(A))){top+=this.__hs(by,h);
bz+=this.__hs(by,g);
}return {left:bz,top:top};
},"gecko":function(bA){var top=bA.offsetTop+this.__hs(bA,h)+this.__hs(bA,i);
var bB=bA.offsetLeft+this.__hs(bA,g)+this.__hs(bA,j);
return {left:bB,top:top};
}}),getLeft:function(bC,bD){return this.get(bC,bD).left;
},getTop:function(bE,bF){return this.get(bE,bF).top;
},getRight:function(bG,bH){return this.get(bG,bH).right;
},getBottom:function(bI,bJ){return this.get(bI,bJ).bottom;
},getRelative:function(bK,bL,bM,bN){var bP=this.get(bK,bM);
var bO=this.get(bL,bN);
return {left:bP.left-bO.left,top:bP.top-bO.top,right:bP.right-bO.right,bottom:bP.bottom-bO.bottom};
},getPosition:function(bQ){return this.getRelative(bQ,this.getOffsetParent(bQ));
},getOffsetParent:function(bR){var bT=bR.offsetParent||document.body;
var bS=qx.bom.element.Style;

while(bT&&(!/^body|html$/i.test(bT.tagName)&&bS.get(bT,p)===x)){bT=bT.offsetParent;
}return bT;
}}});
})();
(function(){var d="event.pointer",c="none",b="qx.html.Decorator",a="absolute";
qx.Class.define(b,{extend:qx.html.Element,construct:function(e,f){var g={position:a,top:0,left:0};

if(qx.core.Environment.get(d)){g.pointerEvents=c;
}qx.html.Element.call(this,null,g);
this.__hx=e;
this.__cA=f||e.toHashCode();
this.useMarkup(e.getMarkup());
},members:{__cA:null,__hx:null,getId:function(){return this.__cA;
},getDecorator:function(){return this.__hx;
},resize:function(h,i){this.__hx.resize(this.getDomElement(),h,i);
},tint:function(j){this.__hx.tint(this.getDomElement(),j);
},getInsets:function(){return this.__hx.getInsets();
}},destruct:function(){this.__hx=null;
}});
})();
(function(){var j="Integer",i="_applyDimension",h="Boolean",g="_applyStretching",f="_applyMargin",e="shorthand",d="_applyAlign",c="allowShrinkY",b="bottom",a="baseline",x="marginBottom",w="qx.ui.core.LayoutItem",v="center",u="marginTop",t="allowGrowX",s="middle",r="marginLeft",q="allowShrinkX",p="top",o="right",m="marginRight",n="abstract",k="allowGrowY",l="left";
qx.Class.define(w,{type:n,extend:qx.core.Object,properties:{minWidth:{check:j,nullable:true,apply:i,init:null,themeable:true},width:{check:j,nullable:true,apply:i,init:null,themeable:true},maxWidth:{check:j,nullable:true,apply:i,init:null,themeable:true},minHeight:{check:j,nullable:true,apply:i,init:null,themeable:true},height:{check:j,nullable:true,apply:i,init:null,themeable:true},maxHeight:{check:j,nullable:true,apply:i,init:null,themeable:true},allowGrowX:{check:h,apply:g,init:true,themeable:true},allowShrinkX:{check:h,apply:g,init:true,themeable:true},allowGrowY:{check:h,apply:g,init:true,themeable:true},allowShrinkY:{check:h,apply:g,init:true,themeable:true},allowStretchX:{group:[t,q],mode:e,themeable:true},allowStretchY:{group:[k,c],mode:e,themeable:true},marginTop:{check:j,init:0,apply:f,themeable:true},marginRight:{check:j,init:0,apply:f,themeable:true},marginBottom:{check:j,init:0,apply:f,themeable:true},marginLeft:{check:j,init:0,apply:f,themeable:true},margin:{group:[u,m,x,r],mode:e,themeable:true},alignX:{check:[l,v,o],nullable:true,apply:d,themeable:true},alignY:{check:[p,s,b,a],nullable:true,apply:d,themeable:true}},members:{__hy:null,__hz:null,__hA:null,__hB:null,__hC:null,__hD:null,__hE:null,getBounds:function(){return this.__hD||this.__hz||null;
},clearSeparators:function(){},renderSeparator:function(y,z){},renderLayout:function(A,top,B,C){var D;
var E=null;

if(this.getHeight()==null&&this._hasHeightForWidth()){var E=this._getHeightForWidth(B);
}
if(E!=null&&E!==this.__hy){this.__hy=E;
qx.ui.core.queue.Layout.add(this);
return null;
}var G=this.__hz;

if(!G){G=this.__hz={};
}var F={};

if(A!==G.left||top!==G.top){F.position=true;
G.left=A;
G.top=top;
}
if(B!==G.width||C!==G.height){F.size=true;
G.width=B;
G.height=C;
}if(this.__hA){F.local=true;
delete this.__hA;
}
if(this.__hC){F.margin=true;
delete this.__hC;
}return F;
},isExcluded:function(){return false;
},hasValidLayout:function(){return !this.__hA;
},scheduleLayoutUpdate:function(){qx.ui.core.queue.Layout.add(this);
},invalidateLayoutCache:function(){this.__hA=true;
this.__hB=null;
},getSizeHint:function(H){var I=this.__hB;

if(I){return I;
}
if(H===false){return null;
}I=this.__hB=this._computeSizeHint();
if(this._hasHeightForWidth()&&this.__hy&&this.getHeight()==null){I.height=this.__hy;
}if(I.minWidth>I.width){I.width=I.minWidth;
}
if(I.maxWidth<I.width){I.width=I.maxWidth;
}
if(!this.getAllowGrowX()){I.maxWidth=I.width;
}
if(!this.getAllowShrinkX()){I.minWidth=I.width;
}if(I.minHeight>I.height){I.height=I.minHeight;
}
if(I.maxHeight<I.height){I.height=I.maxHeight;
}
if(!this.getAllowGrowY()){I.maxHeight=I.height;
}
if(!this.getAllowShrinkY()){I.minHeight=I.height;
}return I;
},_computeSizeHint:function(){var N=this.getMinWidth()||0;
var K=this.getMinHeight()||0;
var O=this.getWidth()||N;
var M=this.getHeight()||K;
var J=this.getMaxWidth()||Infinity;
var L=this.getMaxHeight()||Infinity;
return {minWidth:N,width:O,maxWidth:J,minHeight:K,height:M,maxHeight:L};
},_hasHeightForWidth:function(){var P=this._getLayout();

if(P){return P.hasHeightForWidth();
}return false;
},_getHeightForWidth:function(Q){var R=this._getLayout();

if(R&&R.hasHeightForWidth()){return R.getHeightForWidth(Q);
}return null;
},_getLayout:function(){return null;
},_applyMargin:function(){this.__hC=true;
var parent=this.$$parent;

if(parent){parent.updateLayoutProperties();
}},_applyAlign:function(){var parent=this.$$parent;

if(parent){parent.updateLayoutProperties();
}},_applyDimension:function(){qx.ui.core.queue.Layout.add(this);
},_applyStretching:function(){qx.ui.core.queue.Layout.add(this);
},hasUserBounds:function(){return !!this.__hD;
},setUserBounds:function(S,top,T,U){this.__hD={left:S,top:top,width:T,height:U};
qx.ui.core.queue.Layout.add(this);
},resetUserBounds:function(){delete this.__hD;
qx.ui.core.queue.Layout.add(this);
},__hF:{},setLayoutProperties:function(V){if(V==null){return;
}var W=this.__hE;

if(!W){W=this.__hE={};
}var parent=this.getLayoutParent();

if(parent){parent.updateLayoutProperties(V);
}for(var X in V){if(V[X]==null){delete W[X];
}else{W[X]=V[X];
}}},getLayoutProperties:function(){return this.__hE||this.__hF;
},clearLayoutProperties:function(){delete this.__hE;
},updateLayoutProperties:function(Y){var ba=this._getLayout();

if(ba){var bb;
ba.invalidateChildrenCache();
}qx.ui.core.queue.Layout.add(this);
},getApplicationRoot:function(){return qx.core.Init.getApplication().getRoot();
},getLayoutParent:function(){return this.$$parent||null;
},setLayoutParent:function(parent){if(this.$$parent===parent){return;
}this.$$parent=parent||null;
qx.ui.core.queue.Visibility.add(this);
},isRootWidget:function(){return false;
},_getRoot:function(){var parent=this;

while(parent){if(parent.isRootWidget()){return parent;
}parent=parent.$$parent;
}return null;
},clone:function(){var bc=qx.core.Object.prototype.clone.call(this);
var bd=this.__hE;

if(bd){bc.__hE=qx.lang.Object.clone(bd);
}return bc;
}},destruct:function(){this.$$parent=this.$$subparent=this.__hE=this.__hz=this.__hD=this.__hB=null;
}});
})();
(function(){var b="qx.ui.core.queue.Layout",a="layout";
qx.Class.define(b,{statics:{__dF:{},remove:function(c){delete this.__dF[c.$$hash];
},add:function(d){this.__dF[d.$$hash]=d;
qx.ui.core.queue.Manager.scheduleFlush(a);
},isScheduled:function(e){return !!this.__dF[e.$$hash];
},flush:function(){var f=this.__hI();
for(var i=f.length-1;i>=0;i--){var g=f[i];
if(g.hasValidLayout()){continue;
}if(g.isRootWidget()&&!g.hasUserBounds()){var j=g.getSizeHint();
g.renderLayout(0,0,j.width,j.height);
}else{var h=g.getBounds();
g.renderLayout(h.left,h.top,h.width,h.height);
}}},getNestingLevel:function(k){var l=this.__hH;
var n=0;
var parent=k;
while(true){if(l[parent.$$hash]!=null){n+=l[parent.$$hash];
break;
}
if(!parent.$$parent){break;
}parent=parent.$$parent;
n+=1;
}var m=n;

while(k&&k!==parent){l[k.$$hash]=m--;
k=k.$$parent;
}return n;
},__hG:function(){var t=qx.ui.core.queue.Visibility;
this.__hH={};
var s=[];
var r=this.__dF;
var o,q;

for(var p in r){o=r[p];

if(t.isVisible(o)){q=this.getNestingLevel(o);
if(!s[q]){s[q]={};
}s[q][p]=o;
delete r[p];
}}return s;
},__hI:function(){var x=[];
var z=this.__hG();

for(var w=z.length-1;w>=0;w--){if(!z[w]){continue;
}
for(var v in z[w]){var u=z[w][v];
if(w==0||u.isRootWidget()||u.hasUserBounds()){x.push(u);
u.invalidateLayoutCache();
continue;
}var B=u.getSizeHint(false);

if(B){u.invalidateLayoutCache();
var y=u.getSizeHint();
var A=(!u.getBounds()||B.minWidth!==y.minWidth||B.width!==y.width||B.maxWidth!==y.maxWidth||B.minHeight!==y.minHeight||B.height!==y.height||B.maxHeight!==y.maxHeight);
}else{A=true;
}
if(A){var parent=u.getLayoutParent();

if(!z[w-1]){z[w-1]={};
}z[w-1][parent.$$hash]=parent;
}else{x.push(u);
}}}return x;
}}});
})();
(function(){var h="useraction",g="touchend",f='ie',d="browser.version",c="event.touch",b="qx.ui.core.queue.Manager",a="browser.name";
qx.Class.define(b,{statics:{__hJ:false,__hK:{},__hL:0,MAX_RETRIES:10,scheduleFlush:function(i){var self=qx.ui.core.queue.Manager;
self.__hK[i]=true;

if(!self.__hJ){self.__fq.schedule();
self.__hJ=true;
}},flush:function(){if(qx.ui.core.queue.Manager.PAUSE){return;
}var self=qx.ui.core.queue.Manager;
if(self.__hM){return;
}self.__hM=true;
self.__fq.cancel();
var j=self.__hK;
self.__hN(function(){while(j.visibility||j.widget||j.appearance||j.layout||j.element){if(j.widget){delete j.widget;
qx.ui.core.queue.Widget.flush();
}
if(j.visibility){delete j.visibility;
qx.ui.core.queue.Visibility.flush();
}
if(j.appearance){delete j.appearance;
qx.ui.core.queue.Appearance.flush();
}if(j.widget||j.visibility||j.appearance){continue;
}
if(j.layout){delete j.layout;
qx.ui.core.queue.Layout.flush();
}if(j.widget||j.visibility||j.appearance||j.layout){continue;
}
if(j.element){delete j.element;
qx.html.Element.flush();
}}},function(){self.__hJ=false;
});
self.__hN(function(){if(j.dispose){delete j.dispose;
qx.ui.core.queue.Dispose.flush();
}},function(){self.__hM=false;
});
self.__hL=0;
},__hN:function(k,l){var self=qx.ui.core.queue.Manager;

try{k();
}catch(e){self.__hJ=false;
self.__hM=false;
self.__hL+=1;
if(qx.core.Environment.get(a)==f&&qx.core.Environment.get(d)<=7){l();
}
if(self.__hL<=self.MAX_RETRIES){self.scheduleFlush();
}else{throw new Error("Fatal Error: Flush terminated "+(self.__hL-1)+" times in a row"+" due to exceptions in user code. The application has to be reloaded!");
}throw e;
}finally{l();
}},__hO:function(e){var m=qx.ui.core.queue.Manager;
if(e.getData()==g){m.PAUSE=true;

if(m.__hP){window.clearTimeout(m.__hP);
}m.__hP=window.setTimeout(function(){m.PAUSE=false;
m.__hP=null;
m.flush();
},500);
}else{m.flush();
}}},defer:function(n){n.__fq=new qx.util.DeferredCall(n.flush);
qx.html.Element._scheduleFlush=n.scheduleFlush;
qx.event.Registration.addListener(window,h,qx.core.Environment.get(c)?n.__hO:n.flush);
}});
})();
(function(){var b="qx.ui.core.queue.Widget",a="widget";
qx.Class.define(b,{statics:{__dF:[],remove:function(c){qx.lang.Array.remove(this.__dF,c);
},add:function(d){var e=this.__dF;

if(qx.lang.Array.contains(e,d)){return;
}e.unshift(d);
qx.ui.core.queue.Manager.scheduleFlush(a);
},flush:function(){var f=this.__dF;
var g;

for(var i=f.length-1;i>=0;i--){g=f[i];
f.splice(i,1);
g.syncWidget();
}if(f.length!=0){return;
}this.__dF=[];
}}});
})();
(function(){var b="qx.ui.core.queue.Visibility",a="visibility";
qx.Class.define(b,{statics:{__dF:[],__cN:{},remove:function(c){delete this.__cN[c.$$hash];
qx.lang.Array.remove(this.__dF,c);
},isVisible:function(d){return this.__cN[d.$$hash]||false;
},__hQ:function(e){var g=this.__cN;
var f=e.$$hash;
var h;
if(e.isExcluded()){h=false;
}else{var parent=e.$$parent;

if(parent){h=this.__hQ(parent);
}else{h=e.isRootWidget();
}}return g[f]=h;
},add:function(j){var k=this.__dF;

if(qx.lang.Array.contains(k,j)){return;
}k.unshift(j);
qx.ui.core.queue.Manager.scheduleFlush(a);
},flush:function(){var o=this.__dF;
var p=this.__cN;
for(var i=o.length-1;i>=0;i--){var n=o[i].$$hash;

if(p[n]!=null){o[i].addChildrenToQueue(o);
}}var l={};

for(var i=o.length-1;i>=0;i--){var n=o[i].$$hash;
l[n]=p[n];
p[n]=null;
}for(var i=o.length-1;i>=0;i--){var m=o[i];
var n=m.$$hash;
o.splice(i,1);
if(p[n]==null){this.__hQ(m);
}if(p[n]&&p[n]!=l[n]){m.checkAppearanceNeeds();
}}this.__dF=[];
}}});
})();
(function(){var b="appearance",a="qx.ui.core.queue.Appearance";
qx.Class.define(a,{statics:{__dF:[],remove:function(c){qx.lang.Array.remove(this.__dF,c);
},add:function(d){var e=this.__dF;

if(qx.lang.Array.contains(e,d)){return;
}e.unshift(d);
qx.ui.core.queue.Manager.scheduleFlush(b);
},has:function(f){return qx.lang.Array.contains(this.__dF,f);
},flush:function(){var j=qx.ui.core.queue.Visibility;
var g=this.__dF;
var h;

for(var i=g.length-1;i>=0;i--){h=g[i];
g.splice(i,1);
if(j.isVisible(h)){h.syncAppearance();
}else{h.$$stateChanges=true;
}}}}});
})();
(function(){var b="dispose",a="qx.ui.core.queue.Dispose";
qx.Class.define(a,{statics:{__dF:[],add:function(c){var d=this.__dF;

if(qx.lang.Array.contains(d,c)){return;
}d.unshift(c);
qx.ui.core.queue.Manager.scheduleFlush(b);
},isEmpty:function(){return this.__dF.length==0;
},flush:function(){var e=this.__dF;

for(var i=e.length-1;i>=0;i--){var f=e[i];
e.splice(i,1);
f.dispose();
}if(e.length!=0){return;
}this.__dF=[];
}}});
})();
(function(){var bY="px",bX="Boolean",bW="qx.event.type.Drag",bV="qx.event.type.Mouse",bU="visible",bT="qx.event.type.Focus",bS="Integer",bR="qx.event.type.Touch",bQ="qx.event.type.Data",bP="excluded",bx="_applyPadding",bw="qx.event.type.Event",bv="on",bu="hidden",bt="engine.name",bs="contextmenu",br="String",bq="tabIndex",bp="focused",bo="changeVisibility",cg="mshtml",ch="hovered",ce="qx.event.type.KeySequence",cf="absolute",cc="backgroundColor",cd="drag",ca="div",cb="disabled",ci="move",cj="dragstart",bI="qx.dynlocale",bH="dragchange",bK="dragend",bJ="resize",bM="Decorator",bL="zIndex",bO="opacity",bN="default",bG="Color",bF="changeToolTipText",c="beforeContextmenuOpen",d="_applyNativeContextMenu",f="__hR",g="__id",h="_applyBackgroundColor",j="event.pointer",k="_applyFocusable",m="changeShadow",n="qx.event.type.KeyInput",o="createChildControl",cn="__hS",cm="Font",cl="_applyShadow",ck="_applyEnabled",cr="_applySelectable",cq="Number",cp="_applyKeepActive",co="_applyVisibility",ct="repeat",cs="qxDraggable",N="syncAppearance",O="paddingLeft",L="__ib",M="_applyDroppable",R="#",S="qx.event.type.MouseWheel",P="_applyCursor",Q="_applyDraggable",J="changeTextColor",K="$$widget",w="changeContextMenu",v="paddingTop",y="changeSelectable",x="hideFocus",s="none",r="outline",u="_applyAppearance",t="_applyOpacity",q="url(",p=")",X="qx.ui.core.Widget",Y="_applyFont",ba="cursor",bb="qxDroppable",T="changeZIndex",U="__hV",V="changeEnabled",W="__hW",bc="changeFont",bd="_applyDecorator",G="_applyZIndex",F="_applyTextColor",E="qx.ui.menu.Menu",D="_applyToolTipText",C="true",B="__if",A="widget",z="changeDecorator",I="_applyTabIndex",H="changeAppearance",be="shorthand",bf="/",bg="",bh="_applyContextMenu",bi="paddingBottom",bj="changeNativeContextMenu",bk="undefined",bl="qx.ui.tooltip.ToolTip",bm="qxKeepActive",bn="_applyKeepFocus",bB="paddingRight",bA="changeBackgroundColor",bz="changeLocale",by="__hX",bE="qxKeepFocus",bD="opera",bC="qx/static/blank.gif";
qx.Class.define(X,{extend:qx.ui.core.LayoutItem,include:[qx.locale.MTranslation],construct:function(){qx.ui.core.LayoutItem.call(this);
this.__hR=this._createContainerElement();
this.__hS=this.__ie();
this.__hR.add(this.__hS);
this.initFocusable();
this.initSelectable();
this.initNativeContextMenu();
},events:{appear:bw,disappear:bw,createChildControl:bQ,resize:bQ,move:bQ,syncAppearance:bQ,mousemove:bV,mouseover:bV,mouseout:bV,mousedown:bV,mouseup:bV,click:bV,dblclick:bV,contextmenu:bV,beforeContextmenuOpen:bQ,mousewheel:S,touchstart:bR,touchend:bR,touchmove:bR,touchcancel:bR,tap:bR,swipe:bR,keyup:ce,keydown:ce,keypress:ce,keyinput:n,focus:bT,blur:bT,focusin:bT,focusout:bT,activate:bT,deactivate:bT,capture:bw,losecapture:bw,drop:bW,dragleave:bW,dragover:bW,drag:bW,dragstart:bW,dragend:bW,dragchange:bW,droprequest:bW},properties:{paddingTop:{check:bS,init:0,apply:bx,themeable:true},paddingRight:{check:bS,init:0,apply:bx,themeable:true},paddingBottom:{check:bS,init:0,apply:bx,themeable:true},paddingLeft:{check:bS,init:0,apply:bx,themeable:true},padding:{group:[v,bB,bi,O],mode:be,themeable:true},zIndex:{nullable:true,init:null,apply:G,event:T,check:bS,themeable:true},decorator:{nullable:true,init:null,apply:bd,event:z,check:bM,themeable:true},shadow:{nullable:true,init:null,apply:cl,event:m,check:bM,themeable:true},backgroundColor:{nullable:true,check:bG,apply:h,event:bA,themeable:true},textColor:{nullable:true,check:bG,apply:F,event:J,themeable:true,inheritable:true},font:{nullable:true,apply:Y,check:cm,event:bc,themeable:true,inheritable:true,dereference:true},opacity:{check:cq,apply:t,themeable:true,nullable:true,init:null},cursor:{check:br,apply:P,themeable:true,inheritable:true,nullable:true,init:null},toolTip:{check:bl,nullable:true},toolTipText:{check:br,nullable:true,event:bF,apply:D},toolTipIcon:{check:br,nullable:true,event:bF},blockToolTip:{check:bX,init:false},visibility:{check:[bU,bu,bP],init:bU,apply:co,event:bo},enabled:{init:true,check:bX,inheritable:true,apply:ck,event:V},anonymous:{init:false,check:bX},tabIndex:{check:bS,nullable:true,apply:I},focusable:{check:bX,init:false,apply:k},keepFocus:{check:bX,init:false,apply:bn},keepActive:{check:bX,init:false,apply:cp},draggable:{check:bX,init:false,apply:Q},droppable:{check:bX,init:false,apply:M},selectable:{check:bX,init:false,event:y,apply:cr},contextMenu:{check:E,apply:bh,nullable:true,event:w},nativeContextMenu:{check:bX,init:false,themeable:true,event:bj,apply:d},appearance:{check:br,init:A,apply:u,event:H}},statics:{DEBUG:false,getWidgetByElement:function(cu,cv){while(cu){var cw=cu.$$widget;
if(cw!=null){var cx=qx.core.ObjectRegistry.fromHashCode(cw);
if(!cv||!cx.getAnonymous()){return cx;
}}try{cu=cu.parentNode;
}catch(e){return null;
}}return null;
},contains:function(parent,cy){while(cy){if(parent==cy){return true;
}cy=cy.getLayoutParent();
}return false;
},__hT:new qx.ui.core.DecoratorFactory(),__hU:new qx.ui.core.DecoratorFactory()},members:{__hR:null,__hS:null,__hV:null,__hW:null,__hX:null,__hY:null,__ia:null,__ib:null,_getLayout:function(){return this.__ib;
},_setLayout:function(cz){if(this.__ib){this.__ib.connectToWidget(null);
}
if(cz){cz.connectToWidget(this);
}this.__ib=cz;
qx.ui.core.queue.Layout.add(this);
},setLayoutParent:function(parent){if(this.$$parent===parent){return;
}var cA=this.getContainerElement();

if(this.$$parent&&!this.$$parent.$$disposed){this.$$parent.getContentElement().remove(cA);
}this.$$parent=parent||null;

if(parent&&!parent.$$disposed){this.$$parent.getContentElement().add(cA);
}this.$$refreshInheritables();
qx.ui.core.queue.Visibility.add(this);
},_updateInsets:null,__ic:function(a,b){if(a==b){return false;
}
if(a==null||b==null){return true;
}var cB=qx.theme.manager.Decoration.getInstance();
var cD=cB.resolve(a).getInsets();
var cC=cB.resolve(b).getInsets();

if(cD.top!=cC.top||cD.right!=cC.right||cD.bottom!=cC.bottom||cD.left!=cC.left){return true;
}return false;
},renderLayout:function(cE,top,cF,cG){var cP=qx.ui.core.LayoutItem.prototype.renderLayout.call(this,cE,top,cF,cG);
if(!cP){return null;
}var cI=this.getContainerElement();
var content=this.getContentElement();
var cM=cP.size||this._updateInsets;
var cQ=bY;
var cN={};
if(cP.position){cN.left=cE+cQ;
cN.top=top+cQ;
}if(cP.size){cN.width=cF+cQ;
cN.height=cG+cQ;
}
if(cP.position||cP.size){cI.setStyles(cN);
}
if(cM||cP.local||cP.margin){var cH=this.getInsets();
var innerWidth=cF-cH.left-cH.right;
var innerHeight=cG-cH.top-cH.bottom;
innerWidth=innerWidth<0?0:innerWidth;
innerHeight=innerHeight<0?0:innerHeight;
}var cK={};

if(this._updateInsets){cK.left=cH.left+cQ;
cK.top=cH.top+cQ;
}
if(cM){cK.width=innerWidth+cQ;
cK.height=innerHeight+cQ;
}
if(cM||this._updateInsets){content.setStyles(cK);
}
if(cP.size){var cO=this.__hX;

if(cO){cO.setStyles({width:cF+bY,height:cG+bY});
}}
if(cP.size||this._updateInsets){if(this.__hV){this.__hV.resize(cF,cG);
}}
if(cP.size){if(this.__hW){var cH=this.__hW.getInsets();
var cL=cF+cH.left+cH.right;
var cJ=cG+cH.top+cH.bottom;
this.__hW.resize(cL,cJ);
}}
if(cM||cP.local||cP.margin){if(this.__ib&&this.hasLayoutChildren()){this.__ib.renderLayout(innerWidth,innerHeight);
}else if(this.hasLayoutChildren()){throw new Error("At least one child in control "+this._findTopControl()+" requires a layout, but no one was defined!");
}}if(cP.position&&this.hasListener(ci)){this.fireDataEvent(ci,this.getBounds());
}
if(cP.size&&this.hasListener(bJ)){this.fireDataEvent(bJ,this.getBounds());
}delete this._updateInsets;
return cP;
},__id:null,clearSeparators:function(){var cS=this.__id;

if(!cS){return;
}var cT=qx.ui.core.Widget.__hT;
var content=this.getContentElement();
var cR;

for(var i=0,l=cS.length;i<l;i++){cR=cS[i];
cT.poolDecorator(cR);
content.remove(cR);
}cS.length=0;
},renderSeparator:function(cU,cV){var cW=qx.ui.core.Widget.__hT.getDecoratorElement(cU);
this.getContentElement().add(cW);
cW.resize(cV.width,cV.height);
cW.setStyles({left:cV.left+bY,top:cV.top+bY});
if(!this.__id){this.__id=[cW];
}else{this.__id.push(cW);
}},_computeSizeHint:function(){var de=this.getWidth();
var dd=this.getMinWidth();
var cY=this.getMaxWidth();
var dc=this.getHeight();
var da=this.getMinHeight();
var db=this.getMaxHeight();
var df=this._getContentHint();
var cX=this.getInsets();
var dh=cX.left+cX.right;
var dg=cX.top+cX.bottom;

if(de==null){de=df.width+dh;
}
if(dc==null){dc=df.height+dg;
}
if(dd==null){dd=dh;

if(df.minWidth!=null){dd+=df.minWidth;
if(dd>cY&&cY!=null){dd=cY;
}}}
if(da==null){da=dg;

if(df.minHeight!=null){da+=df.minHeight;
if(da>db&&db!=null){da=db;
}}}
if(cY==null){if(df.maxWidth==null){cY=Infinity;
}else{cY=df.maxWidth+dh;
if(cY<dd&&dd!=null){cY=dd;
}}}
if(db==null){if(df.maxHeight==null){db=Infinity;
}else{db=df.maxHeight+dg;
if(db<da&&da!=null){db=da;
}}}return {width:de,minWidth:dd,maxWidth:cY,height:dc,minHeight:da,maxHeight:db};
},invalidateLayoutCache:function(){qx.ui.core.LayoutItem.prototype.invalidateLayoutCache.call(this);

if(this.__ib){this.__ib.invalidateLayoutCache();
}},_getContentHint:function(){var dj=this.__ib;

if(dj){if(this.hasLayoutChildren()){var di;
var dk=dj.getSizeHint();
return dk;
}else{return {width:0,height:0};
}}else{return {width:100,height:50};
}},_getHeightForWidth:function(dl){var dq=this.getInsets();
var dt=dq.left+dq.right;
var ds=dq.top+dq.bottom;
var dr=dl-dt;
var dn=this._getLayout();

if(dn&&dn.hasHeightForWidth()){var dm=dn.getHeightForWidth(dl);
}else{dm=this._getContentHeightForWidth(dr);
}var dp=dm+ds;
return dp;
},_getContentHeightForWidth:function(du){throw new Error("Abstract method call: _getContentHeightForWidth()!");
},getInsets:function(){var top=this.getPaddingTop();
var dw=this.getPaddingRight();
var dy=this.getPaddingBottom();
var dx=this.getPaddingLeft();

if(this.__hV){var dv=this.__hV.getInsets();
top+=dv.top;
dw+=dv.right;
dy+=dv.bottom;
dx+=dv.left;
}return {"top":top,"right":dw,"bottom":dy,"left":dx};
},getInnerSize:function(){var dA=this.getBounds();

if(!dA){return null;
}var dz=this.getInsets();
return {width:dA.width-dz.left-dz.right,height:dA.height-dz.top-dz.bottom};
},show:function(){this.setVisibility(bU);
},hide:function(){this.setVisibility(bu);
},exclude:function(){this.setVisibility(bP);
},isVisible:function(){return this.getVisibility()===bU;
},isHidden:function(){return this.getVisibility()!==bU;
},isExcluded:function(){return this.getVisibility()===bP;
},isSeeable:function(){var dC=this.getContainerElement().getDomElement();

if(dC){return dC.offsetWidth>0;
}var dB=this;

do{if(!dB.isVisible()){return false;
}
if(dB.isRootWidget()){return true;
}dB=dB.getLayoutParent();
}while(dB);
return false;
},_createContainerElement:function(){var dE={"$$widget":this.toHashCode()};
var dD={zIndex:0,position:cf};
return new qx.html.Element(ca,dD,dE);
},__ie:function(){var dF=this._createContentElement();
dF.setStyles({"position":cf,"zIndex":10});
return dF;
},_createContentElement:function(){return new qx.html.Element(ca,{overflowX:bu,overflowY:bu});
},getContainerElement:function(){return this.__hR;
},getContentElement:function(){return this.__hS;
},getDecoratorElement:function(){return this.__hV||null;
},getShadowElement:function(){return this.__hW||null;
},__if:null,getLayoutChildren:function(){var dH=this.__if;

if(!dH){return this.__ig;
}var dI;

for(var i=0,l=dH.length;i<l;i++){var dG=dH[i];

if(dG.hasUserBounds()||dG.isExcluded()){if(dI==null){dI=dH.concat();
}qx.lang.Array.remove(dI,dG);
}}return dI||dH;
},scheduleLayoutUpdate:function(){qx.ui.core.queue.Layout.add(this);
},invalidateLayoutChildren:function(){var dJ=this.__ib;

if(dJ){dJ.invalidateChildrenCache();
}qx.ui.core.queue.Layout.add(this);
},hasLayoutChildren:function(){var dK=this.__if;

if(!dK){return false;
}var dL;

for(var i=0,l=dK.length;i<l;i++){dL=dK[i];

if(!dL.hasUserBounds()&&!dL.isExcluded()){return true;
}}return false;
},getChildrenContainer:function(){return this;
},__ig:[],_getChildren:function(){return this.__if||this.__ig;
},_indexOf:function(dM){var dN=this.__if;

if(!dN){return -1;
}return dN.indexOf(dM);
},_hasChildren:function(){var dO=this.__if;
return dO!=null&&(!!dO[0]);
},addChildrenToQueue:function(dP){var dQ=this.__if;

if(!dQ){return;
}var dR;

for(var i=0,l=dQ.length;i<l;i++){dR=dQ[i];
dP.push(dR);
dR.addChildrenToQueue(dP);
}},_add:function(dS,dT){if(dS.getLayoutParent()==this){qx.lang.Array.remove(this.__if,dS);
}
if(this.__if){this.__if.push(dS);
}else{this.__if=[dS];
}this.__ih(dS,dT);
},_addAt:function(dU,dV,dW){if(!this.__if){this.__if=[];
}if(dU.getLayoutParent()==this){qx.lang.Array.remove(this.__if,dU);
}var dX=this.__if[dV];

if(dX===dU){dU.setLayoutProperties(dW);
}
if(dX){qx.lang.Array.insertBefore(this.__if,dU,dX);
}else{this.__if.push(dU);
}this.__ih(dU,dW);
},_addBefore:function(dY,ea,eb){if(dY==ea){return;
}
if(!this.__if){this.__if=[];
}if(dY.getLayoutParent()==this){qx.lang.Array.remove(this.__if,dY);
}qx.lang.Array.insertBefore(this.__if,dY,ea);
this.__ih(dY,eb);
},_addAfter:function(ec,ed,ee){if(ec==ed){return;
}
if(!this.__if){this.__if=[];
}if(ec.getLayoutParent()==this){qx.lang.Array.remove(this.__if,ec);
}qx.lang.Array.insertAfter(this.__if,ec,ed);
this.__ih(ec,ee);
},_remove:function(ef){if(!this.__if){throw new Error("This widget has no children!");
}qx.lang.Array.remove(this.__if,ef);
this.__ii(ef);
},_removeAt:function(eg){if(!this.__if){throw new Error("This widget has no children!");
}var eh=this.__if[eg];
qx.lang.Array.removeAt(this.__if,eg);
this.__ii(eh);
return eh;
},_removeAll:function(){if(!this.__if){return [];
}var ei=this.__if.concat();
this.__if.length=0;

for(var i=ei.length-1;i>=0;i--){this.__ii(ei[i]);
}qx.ui.core.queue.Layout.add(this);
return ei;
},_afterAddChild:null,_afterRemoveChild:null,__ih:function(ej,ek){var parent=ej.getLayoutParent();

if(parent&&parent!=this){parent._remove(ej);
}ej.setLayoutParent(this);
if(ek){ej.setLayoutProperties(ek);
}else{this.updateLayoutProperties();
}if(this._afterAddChild){this._afterAddChild(ej);
}},__ii:function(em){if(em.getLayoutParent()!==this){throw new Error("Remove Error: "+em+" is not a child of this widget!");
}em.setLayoutParent(null);
if(this.__ib){this.__ib.invalidateChildrenCache();
}qx.ui.core.queue.Layout.add(this);
if(this._afterRemoveChild){this._afterRemoveChild(em);
}},capture:function(en){this.getContainerElement().capture(en);
},releaseCapture:function(){this.getContainerElement().releaseCapture();
},_applyPadding:function(eo,ep,name){this._updateInsets=true;
qx.ui.core.queue.Layout.add(this);
},_createProtectorElement:function(){if(this.__hX){return;
}var eq=this.__hX=new qx.html.Element;
eq.setStyles({position:cf,top:0,left:0,zIndex:7});
var er=this.getBounds();

if(er){this.__hX.setStyles({width:er.width+bY,height:er.height+bY});
}if((qx.core.Environment.get(bt)==cg)){eq.setStyles({backgroundImage:q+qx.util.ResourceManager.getInstance().toUri(bC)+p,backgroundRepeat:ct});
}this.getContainerElement().add(eq);
},_applyDecorator:function(es,et){var ew=qx.ui.core.Widget.__hT;
var eu=this.getContainerElement();
if(!this.__hX&&!qx.core.Environment.get(j)){this._createProtectorElement();
}if(et){eu.remove(this.__hV);
ew.poolDecorator(this.__hV);
}if(es){var ev=this.__hV=ew.getDecoratorElement(es);
ev.setStyle(bL,5);
eu.add(ev);
}else{delete this.__hV;
}this._applyBackgroundColor(this.getBackgroundColor());
if(this.__ic(et,es)){this._updateInsets=true;
qx.ui.core.queue.Layout.add(this);
}else if(es){var ex=this.getBounds();

if(ex){ev.resize(ex.width,ex.height);
this.__hX&&this.__hX.setStyles({width:ex.width+bY,height:ex.height+bY});
}}},_applyShadow:function(ey,ez){var eG=qx.ui.core.Widget.__hU;
var eB=this.getContainerElement();
if(ez){eB.remove(this.__hW);
eG.poolDecorator(this.__hW);
}if(ey){var eD=this.__hW=eG.getDecoratorElement(ey);
eB.add(eD);
var eF=eD.getInsets();
eD.setStyles({left:(-eF.left)+bY,top:(-eF.top)+bY});
var eE=this.getBounds();

if(eE){var eC=eE.width+eF.left+eF.right;
var eA=eE.height+eF.top+eF.bottom;
eD.resize(eC,eA);
}eD.tint(null);
}else{delete this.__hW;
}},_applyToolTipText:function(eH,eI){if(qx.core.Environment.get(bI)){if(this.__ia){return;
}var eJ=qx.locale.Manager.getInstance();
this.__ia=eJ.addListener(bz,function(){var eK=this.getToolTipText();

if(eK&&eK.translate){this.setToolTipText(eK.translate());
}},this);
}},_applyTextColor:function(eL,eM){},_applyZIndex:function(eN,eO){this.getContainerElement().setStyle(bL,eN==null?0:eN);
},_applyVisibility:function(eP,eQ){var eR=this.getContainerElement();

if(eP===bU){eR.show();
}else{eR.hide();
}var parent=this.$$parent;

if(parent&&(eQ==null||eP==null||eQ===bP||eP===bP)){parent.invalidateLayoutChildren();
}qx.ui.core.queue.Visibility.add(this);
},_applyOpacity:function(eS,eT){this.getContainerElement().setStyle(bO,eS==1?null:eS);
if((qx.core.Environment.get(bt)==cg)&&qx.bom.element.Decoration.isAlphaImageLoaderEnabled()){if(!qx.Class.isSubClassOf(this.getContentElement().constructor,qx.html.Image)){var eU=(eS==1||eS==null)?null:0.99;
this.getContentElement().setStyle(bO,eU);
}}},_applyCursor:function(eV,eW){if(eV==null&&!this.isSelectable()){eV=bN;
}this.getContainerElement().setStyle(ba,eV,qx.core.Environment.get(bt)==bD);
},_applyBackgroundColor:function(eX,eY){var fa=this.getBackgroundColor();
var fc=this.getContainerElement();

if(this.__hV){this.__hV.tint(fa);
fc.setStyle(cc,null);
}else{var fb=qx.theme.manager.Color.getInstance().resolve(fa);
fc.setStyle(cc,fb);
}},_applyFont:function(fd,fe){},__ij:null,$$stateChanges:null,_forwardStates:null,hasState:function(ff){var fg=this.__ij;
return !!fg&&!!fg[ff];
},addState:function(fh){var fi=this.__ij;

if(!fi){fi=this.__ij={};
}
if(fi[fh]){return;
}this.__ij[fh]=true;
if(fh===ch){this.syncAppearance();
}else if(!qx.ui.core.queue.Visibility.isVisible(this)){this.$$stateChanges=true;
}else{qx.ui.core.queue.Appearance.add(this);
}var forward=this._forwardStates;
var fl=this.__im;

if(forward&&forward[fh]&&fl){var fj;

for(var fk in fl){fj=fl[fk];

if(fj instanceof qx.ui.core.Widget){fl[fk].addState(fh);
}}}},removeState:function(fm){var fn=this.__ij;

if(!fn||!fn[fm]){return;
}delete this.__ij[fm];
if(fm===ch){this.syncAppearance();
}else if(!qx.ui.core.queue.Visibility.isVisible(this)){this.$$stateChanges=true;
}else{qx.ui.core.queue.Appearance.add(this);
}var forward=this._forwardStates;
var fq=this.__im;

if(forward&&forward[fm]&&fq){for(var fp in fq){var fo=fq[fp];

if(fo instanceof qx.ui.core.Widget){fo.removeState(fm);
}}}},replaceState:function(fr,fs){var ft=this.__ij;

if(!ft){ft=this.__ij={};
}
if(!ft[fs]){ft[fs]=true;
}
if(ft[fr]){delete ft[fr];
}
if(!qx.ui.core.queue.Visibility.isVisible(this)){this.$$stateChanges=true;
}else{qx.ui.core.queue.Appearance.add(this);
}var forward=this._forwardStates;
var fw=this.__im;

if(forward&&forward[fs]&&fw){for(var fv in fw){var fu=fw[fv];

if(fu instanceof qx.ui.core.Widget){fu.replaceState(fr,fs);
}}}},__ik:null,__il:null,syncAppearance:function(){var fB=this.__ij;
var fA=this.__ik;
var fC=qx.theme.manager.Appearance.getInstance();
var fy=qx.core.Property.$$method.setThemed;
var fG=qx.core.Property.$$method.resetThemed;
if(this.__il){delete this.__il;
if(fA){var fx=fC.styleFrom(fA,fB,null,this.getAppearance());
fA=null;
}}if(!fA){var fz=this;
var fF=[];

do{fF.push(fz.$$subcontrol||fz.getAppearance());
}while(fz=fz.$$subparent);
fA=fF.reverse().join(bf).replace(/#[0-9]+/g,bg);
this.__ik=fA;
}var fD=fC.styleFrom(fA,fB,null,this.getAppearance());

if(fD){var fE;

if(fx){for(var fE in fx){if(fD[fE]===undefined){this[fG[fE]]();
}}}for(var fE in fD){fD[fE]===undefined?this[fG[fE]]():this[fy[fE]](fD[fE]);
}}else if(fx){for(var fE in fx){this[fG[fE]]();
}}this.fireDataEvent(N,this.__ij);
},_applyAppearance:function(fH,fI){this.updateAppearance();
},checkAppearanceNeeds:function(){if(!this.__hY){qx.ui.core.queue.Appearance.add(this);
this.__hY=true;
}else if(this.$$stateChanges){qx.ui.core.queue.Appearance.add(this);
delete this.$$stateChanges;
}},updateAppearance:function(){this.__il=true;
qx.ui.core.queue.Appearance.add(this);
var fL=this.__im;

if(fL){var fJ;

for(var fK in fL){fJ=fL[fK];

if(fJ instanceof qx.ui.core.Widget){fJ.updateAppearance();
}}}},syncWidget:function(){},getEventTarget:function(){var fM=this;

while(fM.getAnonymous()){fM=fM.getLayoutParent();

if(!fM){return null;
}}return fM;
},getFocusTarget:function(){var fN=this;

if(!fN.getEnabled()){return null;
}
while(fN.getAnonymous()||!fN.getFocusable()){fN=fN.getLayoutParent();

if(!fN||!fN.getEnabled()){return null;
}}return fN;
},getFocusElement:function(){return this.getContainerElement();
},isTabable:function(){return (!!this.getContainerElement().getDomElement())&&this.isFocusable();
},_applyFocusable:function(fO,fP){var fQ=this.getFocusElement();
if(fO){var fR=this.getTabIndex();

if(fR==null){fR=1;
}fQ.setAttribute(bq,fR);
if((qx.core.Environment.get(bt)==cg)){fQ.setAttribute(x,C);
}else{fQ.setStyle(r,s);
}}else{if(fQ.isNativelyFocusable()){fQ.setAttribute(bq,-1);
}else if(fP){fQ.setAttribute(bq,null);
}}},_applyKeepFocus:function(fS){var fT=this.getFocusElement();
fT.setAttribute(bE,fS?bv:null);
},_applyKeepActive:function(fU){var fV=this.getContainerElement();
fV.setAttribute(bm,fU?bv:null);
},_applyTabIndex:function(fW){if(fW==null){fW=1;
}else if(fW<1||fW>32000){throw new Error("TabIndex property must be between 1 and 32000");
}
if(this.getFocusable()&&fW!=null){this.getFocusElement().setAttribute(bq,fW);
}},_applySelectable:function(fX,fY){if(fY!==null){this._applyCursor(this.getCursor());
}this.getContentElement().setSelectable(fX);
},_applyEnabled:function(ga,gb){if(ga===false){this.addState(cb);
this.removeState(ch);
if(this.isFocusable()){this.removeState(bp);
this._applyFocusable(false,true);
}if(this.isDraggable()){this._applyDraggable(false,true);
}if(this.isDroppable()){this._applyDroppable(false,true);
}}else{this.removeState(cb);
if(this.isFocusable()){this._applyFocusable(true,false);
}if(this.isDraggable()){this._applyDraggable(true,false);
}if(this.isDroppable()){this._applyDroppable(true,false);
}}},_applyNativeContextMenu:function(gc,gd,name){},_applyContextMenu:function(ge,gf){if(gf){gf.removeState(bs);

if(gf.getOpener()==this){gf.resetOpener();
}
if(!ge){this.removeListener(bs,this._onContextMenuOpen);
gf.removeListener(bo,this._onBeforeContextMenuOpen,this);
}}
if(ge){ge.setOpener(this);
ge.addState(bs);

if(!gf){this.addListener(bs,this._onContextMenuOpen);
ge.addListener(bo,this._onBeforeContextMenuOpen,this);
}}},_onContextMenuOpen:function(e){this.getContextMenu().openAtMouse(e);
e.stop();
},_onBeforeContextMenuOpen:function(e){if(e.getData()==bU&&this.hasListener(c)){this.fireDataEvent(c,e);
}},_onStopEvent:function(e){e.stopPropagation();
},_applyDraggable:function(gg,gh){if(!this.isEnabled()&&gg===true){gg=false;
}qx.ui.core.DragDropCursor.getInstance();
if(gg){this.addListener(cj,this._onDragStart);
this.addListener(cd,this._onDrag);
this.addListener(bK,this._onDragEnd);
this.addListener(bH,this._onDragChange);
}else{this.removeListener(cj,this._onDragStart);
this.removeListener(cd,this._onDrag);
this.removeListener(bK,this._onDragEnd);
this.removeListener(bH,this._onDragChange);
}this.getContainerElement().setAttribute(cs,gg?bv:null);
},_applyDroppable:function(gi,gj){if(!this.isEnabled()&&gi===true){gi=false;
}this.getContainerElement().setAttribute(bb,gi?bv:null);
},_onDragStart:function(e){qx.ui.core.DragDropCursor.getInstance().placeToMouse(e);
this.getApplicationRoot().setGlobalCursor(bN);
},_onDrag:function(e){qx.ui.core.DragDropCursor.getInstance().placeToMouse(e);
},_onDragEnd:function(e){qx.ui.core.DragDropCursor.getInstance().moveTo(-1000,-1000);
this.getApplicationRoot().resetGlobalCursor();
},_onDragChange:function(e){var gk=qx.ui.core.DragDropCursor.getInstance();
var gl=e.getCurrentAction();
gl?gk.setAction(gl):gk.resetAction();
},visualizeFocus:function(){this.addState(bp);
},visualizeBlur:function(){this.removeState(bp);
},scrollChildIntoView:function(gm,gn,go,gp){gp=typeof gp==bk?true:gp;
var gq=qx.ui.core.queue.Layout;
var parent;
if(gp){gp=!gq.isScheduled(gm);
parent=gm.getLayoutParent();
if(gp&&parent){gp=!gq.isScheduled(parent);
if(gp){parent.getChildren().forEach(function(gr){gp=gp&&!gq.isScheduled(gr);
});
}}}this.scrollChildIntoViewX(gm,gn,gp);
this.scrollChildIntoViewY(gm,go,gp);
},scrollChildIntoViewX:function(gs,gt,gu){this.getContentElement().scrollChildIntoViewX(gs.getContainerElement(),gt,gu);
},scrollChildIntoViewY:function(gv,gw,gx){this.getContentElement().scrollChildIntoViewY(gv.getContainerElement(),gw,gx);
},focus:function(){if(this.isFocusable()){this.getFocusElement().focus();
}else{throw new Error("Widget is not focusable!");
}},blur:function(){if(this.isFocusable()){this.getFocusElement().blur();
}else{throw new Error("Widget is not focusable!");
}},activate:function(){this.getContainerElement().activate();
},deactivate:function(){this.getContainerElement().deactivate();
},tabFocus:function(){this.getFocusElement().focus();
},hasChildControl:function(gy){if(!this.__im){return false;
}return !!this.__im[gy];
},__im:null,_getCreatedChildControls:function(){return this.__im;
},getChildControl:function(gz,gA){if(!this.__im){if(gA){return null;
}this.__im={};
}var gB=this.__im[gz];

if(gB){return gB;
}
if(gA===true){return null;
}return this._createChildControl(gz);
},_showChildControl:function(gC){var gD=this.getChildControl(gC);
gD.show();
return gD;
},_excludeChildControl:function(gE){var gF=this.getChildControl(gE,true);

if(gF){gF.exclude();
}},_isChildControlVisible:function(gG){var gH=this.getChildControl(gG,true);

if(gH){return gH.isVisible();
}return false;
},_createChildControl:function(gI){if(!this.__im){this.__im={};
}else if(this.__im[gI]){throw new Error("Child control '"+gI+"' already created!");
}var gM=gI.indexOf(R);

if(gM==-1){var gJ=this._createChildControlImpl(gI);
}else{var gJ=this._createChildControlImpl(gI.substring(0,gM),gI.substring(gM+1,gI.length));
}
if(!gJ){throw new Error("Unsupported control: "+gI);
}gJ.$$subcontrol=gI;
gJ.$$subparent=this;
var gK=this.__ij;
var forward=this._forwardStates;

if(gK&&forward&&gJ instanceof qx.ui.core.Widget){for(var gL in gK){if(forward[gL]){gJ.addState(gL);
}}}this.fireDataEvent(o,gJ);
return this.__im[gI]=gJ;
},_createChildControlImpl:function(gN,gO){return null;
},_disposeChildControls:function(){var gS=this.__im;

if(!gS){return;
}var gQ=qx.ui.core.Widget;

for(var gR in gS){var gP=gS[gR];

if(!gQ.contains(this,gP)){gP.destroy();
}else{gP.dispose();
}}delete this.__im;
},_findTopControl:function(){var gT=this;

while(gT){if(!gT.$$subparent){return gT;
}gT=gT.$$subparent;
}return null;
},getContainerLocation:function(gU){var gV=this.getContainerElement().getDomElement();
return gV?qx.bom.element.Location.get(gV,gU):null;
},getContentLocation:function(gW){var gX=this.getContentElement().getDomElement();
return gX?qx.bom.element.Location.get(gX,gW):null;
},setDomLeft:function(gY){var ha=this.getContainerElement().getDomElement();

if(ha){ha.style.left=gY+bY;
}else{throw new Error("DOM element is not yet created!");
}},setDomTop:function(hb){var hc=this.getContainerElement().getDomElement();

if(hc){hc.style.top=hb+bY;
}else{throw new Error("DOM element is not yet created!");
}},setDomPosition:function(hd,top){var he=this.getContainerElement().getDomElement();

if(he){he.style.left=hd+bY;
he.style.top=top+bY;
}else{throw new Error("DOM element is not yet created!");
}},destroy:function(){if(this.$$disposed){return;
}var parent=this.$$parent;

if(parent){parent._remove(this);
}qx.ui.core.queue.Dispose.add(this);
},clone:function(){var hf=qx.ui.core.LayoutItem.prototype.clone.call(this);

if(this.getChildren){var hg=this.getChildren();

for(var i=0,l=hg.length;i<l;i++){hf.add(hg[i].clone());
}}return hf;
}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){if(qx.core.Environment.get(bI)){if(this.__ia){qx.locale.Manager.getInstance().removeListenerById(this.__ia);
}}this.getContainerElement().setAttribute(K,null,true);
this._disposeChildControls();
qx.ui.core.queue.Appearance.remove(this);
qx.ui.core.queue.Layout.remove(this);
qx.ui.core.queue.Visibility.remove(this);
qx.ui.core.queue.Widget.remove(this);
}if(!qx.core.ObjectRegistry.inShutDown){var hi=qx.ui.core.Widget;
var hh=this.getContainerElement();

if(this.__hV){hh.remove(this.__hV);
hi.__hT.poolDecorator(this.__hV);
}
if(this.__hW){hh.remove(this.__hW);
hi.__hU.poolDecorator(this.__hW);
}this.clearSeparators();
this.__hV=this.__hW=this.__id=null;
}else{this._disposeArray(g);
this._disposeObjects(U,W);
}this._disposeArray(B);
this.__ij=this.__im=null;
this._disposeObjects(L,f,cn,by);
}});
})();
(function(){var f="blur",e="focus",d="input",c="load",b="qx.ui.core.EventHandler",a="activate";
qx.Class.define(b,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(){qx.core.Object.call(this);
this.__eI=qx.event.Registration.getManager(window);
},statics:{PRIORITY:qx.event.Registration.PRIORITY_FIRST,SUPPORTED_TYPES:{mousemove:1,mouseover:1,mouseout:1,mousedown:1,mouseup:1,click:1,dblclick:1,contextmenu:1,mousewheel:1,keyup:1,keydown:1,keypress:1,keyinput:1,capture:1,losecapture:1,focusin:1,focusout:1,focus:1,blur:1,activate:1,deactivate:1,appear:1,disappear:1,dragstart:1,dragend:1,dragover:1,dragleave:1,drop:1,drag:1,dragchange:1,droprequest:1,touchstart:1,touchend:1,touchmove:1,touchcancel:1,tap:1,swipe:1},IGNORE_CAN_HANDLE:false},members:{__eI:null,__in:{focusin:1,focusout:1,focus:1,blur:1},__io:{mouseover:1,mouseout:1,appear:1,disappear:1},canHandleEvent:function(g,h){return g instanceof qx.ui.core.Widget;
},_dispatchEvent:function(j){var p=j.getTarget();
var o=qx.ui.core.Widget.getWidgetByElement(p);
var q=false;

while(o&&o.isAnonymous()){var q=true;
o=o.getLayoutParent();
}if(o&&q&&j.getType()==a){o.getContainerElement().activate();
}if(this.__in[j.getType()]){o=o&&o.getFocusTarget();
if(!o){return;
}}if(j.getRelatedTarget){var x=j.getRelatedTarget();
var w=qx.ui.core.Widget.getWidgetByElement(x);

while(w&&w.isAnonymous()){w=w.getLayoutParent();
}
if(w){if(this.__in[j.getType()]){w=w.getFocusTarget();
}if(w===o){return;
}}}var s=j.getCurrentTarget();
var u=qx.ui.core.Widget.getWidgetByElement(s);

if(!u||u.isAnonymous()){return;
}if(this.__in[j.getType()]){u=u.getFocusTarget();
}var v=j.getType();

if(!u||!(u.isEnabled()||this.__io[v])){return;
}var k=j.getEventPhase()==qx.event.type.Event.CAPTURING_PHASE;
var r=this.__eI.getListeners(u,v,k);

if(!r||r.length===0){return;
}var m=qx.event.Pool.getInstance().getObject(j.constructor);
j.clone(m);
m.setTarget(o);
m.setRelatedTarget(w||null);
m.setCurrentTarget(u);
var y=j.getOriginalTarget();

if(y){var n=qx.ui.core.Widget.getWidgetByElement(y);

while(n&&n.isAnonymous()){n=n.getLayoutParent();
}m.setOriginalTarget(n);
}else{m.setOriginalTarget(p);
}for(var i=0,l=r.length;i<l;i++){var t=r[i].context||u;
r[i].handler.call(t,m);
}if(m.getPropagationStopped()){j.stopPropagation();
}
if(m.getDefaultPrevented()){j.preventDefault();
}qx.event.Pool.getInstance().poolObject(m);
},registerEvent:function(z,A,B){var C;

if(A===e||A===f){C=z.getFocusElement();
}else if(A===c||A===d){C=z.getContentElement();
}else{C=z.getContainerElement();
}
if(C){C.addListener(A,this._dispatchEvent,this,B);
}},unregisterEvent:function(D,E,F){var G;

if(E===e||E===f){G=D.getFocusElement();
}else if(E===c||E===d){G=D.getContentElement();
}else{G=D.getContainerElement();
}
if(G){G.removeListener(E,this._dispatchEvent,this,F);
}}},destruct:function(){this.__eI=null;
},defer:function(H){qx.event.Registration.addHandler(H);
}});
})();
(function(){var t="",s='indexOf',r='slice',q='concat',p='toLocaleLowerCase',o="qx.type.BaseString",n='match',m='toLocaleUpperCase',k='search',j='replace',c='toLowerCase',h='charCodeAt',f='split',b='substring',a='lastIndexOf',e='substr',d='toUpperCase',g='charAt';
qx.Class.define(o,{extend:Object,construct:function(u){var u=u||t;
this.__ip=u;
this.length=u.length;
},members:{$$isString:true,length:0,__ip:null,toString:function(){return this.__ip;
},charAt:null,valueOf:null,charCodeAt:null,concat:null,indexOf:null,lastIndexOf:null,match:null,replace:null,search:null,slice:null,split:null,substr:null,substring:null,toLowerCase:null,toUpperCase:null,toHashCode:function(){return qx.core.ObjectRegistry.toHashCode(this);
},toLocaleLowerCase:null,toLocaleUpperCase:null,base:function(v,w){return qx.core.Object.prototype.base.apply(this,arguments);
}},defer:function(x,y){var z=[g,h,q,s,a,n,j,k,r,f,e,b,c,d,p,m];
y.valueOf=y.toString;

if(new x(t).valueOf()==null){delete y.valueOf;
}
for(var i=0,l=z.length;i<l;i++){y[z[i]]=String.prototype[z[i]];
}}});
})();
(function(){var a="qx.locale.LocalizedString";
qx.Class.define(a,{extend:qx.type.BaseString,construct:function(b,c,d){qx.type.BaseString.call(this,b);
this.__iq=c;
this.__ir=d;
},members:{__iq:null,__ir:null,translate:function(){return qx.locale.Manager.getInstance().translate(this.__iq,this.__ir);
}}});
})();
(function(){var l="_",k="",j="locale",h="_applyLocale",g="changeLocale",f="C",e="locale.variant",d="qx.dynlocale",c="qx.locale.Manager",b="String",a="singleton";
qx.Class.define(c,{type:a,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__is=qx.$$translations||{};
this.__it=qx.$$locales||{};
var m=qx.core.Environment.get(j);
var n=qx.core.Environment.get(e);

if(n!==k){m+=l+n;
}this.__iu=m;
this.setLocale(m||this.__iv);
},statics:{tr:function(o,p){var q=qx.lang.Array.fromArguments(arguments);
q.splice(0,1);
return qx.locale.Manager.getInstance().translate(o,q);
},trn:function(r,s,t,u){var v=qx.lang.Array.fromArguments(arguments);
v.splice(0,3);
if(t!=1){return qx.locale.Manager.getInstance().translate(s,v);
}else{return qx.locale.Manager.getInstance().translate(r,v);
}},trc:function(w,x,y){var z=qx.lang.Array.fromArguments(arguments);
z.splice(0,2);
return qx.locale.Manager.getInstance().translate(x,z);
},marktr:function(A){return A;
}},properties:{locale:{check:b,nullable:true,apply:h,event:g}},members:{__iv:f,__iw:null,__ix:null,__is:null,__it:null,__iu:null,getLanguage:function(){return this.__ix;
},getTerritory:function(){return this.getLocale().split(l)[1]||k;
},getAvailableLocales:function(){var C=[];

for(var B in this.__it){if(B!=this.__iv){C.push(B);
}}return C;
},__iy:function(D){var F;

if(D==null){return null;
}var E=D.indexOf(l);

if(E==-1){F=D;
}else{F=D.substring(0,E);
}return F;
},_applyLocale:function(G,H){this.__iw=G;
this.__ix=this.__iy(G);
},addTranslation:function(I,J){var K=this.__is;

if(K[I]){for(var L in J){K[I][L]=J[L];
}}else{K[I]=J;
}},addLocale:function(M,N){var O=this.__it;

if(O[M]){for(var P in N){O[M][P]=N[P];
}}else{O[M]=N;
}},translate:function(Q,R,S){var T=this.__is;
return this.__iz(T,Q,R,S);
},localize:function(U,V,W){var X=this.__it;
return this.__iz(X,U,V,W);
},__iz:function(Y,ba,bb,bc){var bd;

if(!Y){return ba;
}
if(bc){var bf=this.__iy(bc);
}else{bc=this.__iw;
bf=this.__ix;
}if(!bd&&Y[bc]){bd=Y[bc][ba];
}if(!bd&&Y[bf]){bd=Y[bf][ba];
}if(!bd&&Y[this.__iv]){bd=Y[this.__iv][ba];
}
if(!bd){bd=ba;
}
if(bb.length>0){var be=[];

for(var i=0;i<bb.length;i++){var bg=bb[i];

if(bg&&bg.translate){be[i]=bg.translate();
}else{be[i]=bg;
}}bd=qx.lang.String.format(bd,be);
}
if(qx.core.Environment.get(d)){bd=new qx.locale.LocalizedString(bd,ba,bb);
}return bd;
}},destruct:function(){this.__is=this.__it=null;
}});
})();
(function(){var k="px",j="engine.name",i="div",h="img",g="",f="no-repeat",d="scale-x",c="mshtml",b="scale",a="b64",I="scale-y",H="qx/icon",G="repeat",F=".png",E="crop",D="engine.version",C="progid:DXImageTransform.Microsoft.AlphaImageLoader(src='",B='<div style="',A="repeat-y",z='<img src="',r="qx.bom.element.Decoration",s="', sizingMethod='",p='"/>',q="png",n="')",o='"></div>',l='" style="',m="none",t="webkit",u=" ",w="repeat-x",v="DXImageTransform.Microsoft.AlphaImageLoader",y="qx/static/blank.gif",x="absolute";
qx.Class.define(r,{statics:{DEBUG:false,__iA:{},__iB:(qx.core.Environment.get(j)==c)&&qx.core.Environment.get(D)<9,__iC:qx.core.Environment.select(j,{"mshtml":{"scale-x":true,"scale-y":true,"scale":true,"no-repeat":true},"default":null}),__iD:{"scale-x":h,"scale-y":h,"scale":h,"repeat":i,"no-repeat":i,"repeat-x":i,"repeat-y":i},update:function(J,K,L,M){var O=this.getTagName(L,K);

if(O!=J.tagName.toLowerCase()){throw new Error("Image modification not possible because elements could not be replaced at runtime anymore!");
}var P=this.getAttributes(K,L,M);

if(O===h){J.src=P.src||qx.util.ResourceManager.getInstance().toUri(y);
}if(J.style.backgroundPosition!=g&&P.style.backgroundPosition===undefined){P.style.backgroundPosition=null;
}if(J.style.clip!=g&&P.style.clip===undefined){P.style.clip=null;
}var N=qx.bom.element.Style;
N.setStyles(J,P.style);
if(this.__iB){try{J.filters[v].apply();
}catch(e){}}},create:function(Q,R,S){var T=this.getTagName(R,Q);
var V=this.getAttributes(Q,R,S);
var U=qx.bom.element.Style.compile(V.style);

if(T===h){return z+V.src+l+U+p;
}else{return B+U+o;
}},getTagName:function(W,X){if((qx.core.Environment.get(j)==c)){if(X&&this.__iB&&this.__iC[W]&&qx.lang.String.endsWith(X,F)){return i;
}}return this.__iD[W];
},getAttributes:function(Y,ba,bb){if(!bb){bb={};
}
if(!bb.position){bb.position=x;
}
if((qx.core.Environment.get(j)==c)){bb.fontSize=0;
bb.lineHeight=0;
}else if((qx.core.Environment.get(j)==t)){bb.WebkitUserDrag=m;
}var bd=qx.util.ResourceManager.getInstance().getImageFormat(Y)||qx.io.ImageLoader.getFormat(Y);
var bc;
if(this.__iB&&this.__iC[ba]&&bd===q){bc=this.__iG(bb,ba,Y);
}else{if(ba===b){bc=this.__iH(bb,ba,Y);
}else if(ba===d||ba===I){bc=this.__iI(bb,ba,Y);
}else{bc=this.__iL(bb,ba,Y);
}}return bc;
},__iE:function(be,bf,bh){if(be.width==null&&bf!=null){be.width=bf+k;
}
if(be.height==null&&bh!=null){be.height=bh+k;
}return be;
},__iF:function(bi){var bj=qx.util.ResourceManager.getInstance().getImageWidth(bi)||qx.io.ImageLoader.getWidth(bi);
var bk=qx.util.ResourceManager.getInstance().getImageHeight(bi)||qx.io.ImageLoader.getHeight(bi);
return {width:bj,height:bk};
},__iG:function(bl,bm,bn){var bq=this.__iF(bn);
bl=this.__iE(bl,bq.width,bq.height);
var bp=bm==f?E:b;
var bo=C+qx.util.ResourceManager.getInstance().toUri(bn)+s+bp+n;
bl.filter=bo;
bl.backgroundImage=bl.backgroundRepeat=g;
return {style:bl};
},__iH:function(br,bs,bt){var bu=qx.util.ResourceManager.getInstance().toUri(bt);
var bv=this.__iF(bt);
br=this.__iE(br,bv.width,bv.height);
return {src:bu,style:br};
},__iI:function(bw,bx,by){var bz=qx.util.ResourceManager.getInstance();
var bC=bz.getCombinedFormat(by);
var bE=this.__iF(by);
var bA;

if(bC){var bD=bz.getData(by);
var bB=bD[4];

if(bC==a){bA=bz.toDataUri(by);
}else{bA=bz.toUri(bB);
}
if(bx===d){bw=this.__iJ(bw,bD,bE.height);
}else{bw=this.__iK(bw,bD,bE.width);
}return {src:bA,style:bw};
}else{if(bx==d){bw.height=bE.height==null?null:bE.height+k;
}else if(bx==I){bw.width=bE.width==null?null:bE.width+k;
}bA=bz.toUri(by);
return {src:bA,style:bw};
}},__iJ:function(bF,bG,bH){var bI=qx.util.ResourceManager.getInstance().getImageHeight(bG[4]);
bF.clip={top:-bG[6],height:bH};
bF.height=bI+k;
if(bF.top!=null){bF.top=(parseInt(bF.top,10)+bG[6])+k;
}else if(bF.bottom!=null){bF.bottom=(parseInt(bF.bottom,10)+bH-bI-bG[6])+k;
}return bF;
},__iK:function(bJ,bK,bL){var bM=qx.util.ResourceManager.getInstance().getImageWidth(bK[4]);
bJ.clip={left:-bK[5],width:bL};
bJ.width=bM+k;
if(bJ.left!=null){bJ.left=(parseInt(bJ.left,10)+bK[5])+k;
}else if(bJ.right!=null){bJ.right=(parseInt(bJ.right,10)+bL-bM-bK[5])+k;
}return bJ;
},__iL:function(bN,bO,bP){var bS=qx.util.ResourceManager.getInstance();
var bX=bS.getCombinedFormat(bP);
var ca=this.__iF(bP);
if(bX&&bO!==G){var bY=bS.getData(bP);
var bW=bY[4];

if(bX==a){var bV=bS.toDataUri(bP);
var bU=bT=0;
}else{var bV=bS.toUri(bW);
var bU=bY[5];
var bT=bY[6];
}var bQ=qx.bom.element.Background.getStyles(bV,bO,bU,bT);

for(var bR in bQ){bN[bR]=bQ[bR];
}
if(ca.width!=null&&bN.width==null&&(bO==A||bO===f)){bN.width=ca.width+k;
}
if(ca.height!=null&&bN.height==null&&(bO==w||bO===f)){bN.height=ca.height+k;
}return {style:bN};
}else{bN=this.__iE(bN,ca.width,ca.height);
bN=this.__iM(bN,bP,bO);
return {style:bN};
}},__iM:function(cb,cc,cd){var top=null;
var ch=null;

if(cb.backgroundPosition){var ce=cb.backgroundPosition.split(u);
ch=parseInt(ce[0],10);

if(isNaN(ch)){ch=ce[0];
}top=parseInt(ce[1],10);

if(isNaN(top)){top=ce[1];
}}var cg=qx.bom.element.Background.getStyles(cc,cd,ch,top);

for(var cf in cg){cb[cf]=cg[cf];
}if(cb.filter){cb.filter=g;
}return cb;
},__iN:function(ci){if(this.DEBUG&&qx.util.ResourceManager.getInstance().has(ci)&&ci.indexOf(H)==-1){if(!this.__iA[ci]){qx.log.Logger.debug("Potential clipped image candidate: "+ci);
this.__iA[ci]=true;
}}},isAlphaImageLoaderEnabled:qx.core.Environment.select(j,{"mshtml":function(){return qx.bom.element.Decoration.__iB;
},"default":function(){return false;
}})}});
})();
(function(){var c="engine.name",b="load",a="qx.io.ImageLoader";
qx.Bootstrap.define(a,{statics:{__cN:{},__iO:{width:null,height:null},__iP:/\.(png|gif|jpg|jpeg|bmp)\b/i,isLoaded:function(d){var e=this.__cN[d];
return !!(e&&e.loaded);
},isFailed:function(f){var g=this.__cN[f];
return !!(g&&g.failed);
},isLoading:function(h){var j=this.__cN[h];
return !!(j&&j.loading);
},getFormat:function(k){var m=this.__cN[k];
return m?m.format:null;
},getSize:function(n){var o=this.__cN[n];
return o?{width:o.width,height:o.height}:this.__iO;
},getWidth:function(p){var q=this.__cN[p];
return q?q.width:null;
},getHeight:function(r){var s=this.__cN[r];
return s?s.height:null;
},load:function(t,u,v){var w=this.__cN[t];

if(!w){w=this.__cN[t]={};
}if(u&&!v){v=window;
}if(w.loaded||w.loading||w.failed){if(u){if(w.loading){w.callbacks.push(u,v);
}else{u.call(v,t,w);
}}}else{w.loading=true;
w.callbacks=[];

if(u){w.callbacks.push(u,v);
}var y=new Image();
var x=qx.lang.Function.listener(this.__iQ,this,y,t);
y.onload=x;
y.onerror=x;
y.src=t;
w.element=y;
}},abort:function(z){var A=this.__cN[z];

if(A&&!A.loaded){A.aborted=true;
var C=A.callbacks;
var B=A.element;
B.onload=B.onerror=null;
delete A.callbacks;
delete A.element;
delete A.loading;

for(var i=0,l=C.length;i<l;i+=2){C[i].call(C[i+1],z,A);
}}this.__cN[z]=null;
},__iQ:qx.event.GlobalError.observeMethod(function(event,D,E){var F=this.__cN[E];
if(event.type===b){F.loaded=true;
F.width=this.__iR(D);
F.height=this.__iS(D);
var G=this.__iP.exec(E);

if(G!=null){F.format=G[1];
}}else{F.failed=true;
}D.onload=D.onerror=null;
var H=F.callbacks;
delete F.loading;
delete F.callbacks;
delete F.element;
for(var i=0,l=H.length;i<l;i+=2){H[i].call(H[i+1],E,F);
}}),__iR:qx.core.Environment.select(c,{"gecko":function(I){return I.naturalWidth;
},"default":function(J){return J.width;
}}),__iS:qx.core.Environment.select(c,{"gecko":function(K){return K.naturalHeight;
},"default":function(L){return L.height;
}})}});
})();
(function(){var u="number",t="0",s="px",r=";",q="'",p="')",o="gecko",n="background-image:url(",m=");",l="",e=")",k="background-repeat:",h="engine.version",c="data:",b=" ",g="qx.bom.element.Background",f="url(",i="background-position:",a="base64",j="url('",d="engine.name";
qx.Class.define(g,{statics:{__iT:[n,null,m,i,null,r,k,null,r],__iU:{backgroundImage:null,backgroundPosition:null,backgroundRepeat:null},__iV:function(v,top){var w=qx.core.Environment.get(d);
var x=qx.core.Environment.get(h);

if(w==o&&x<1.9&&v==top&&typeof v==u){top+=0.01;
}
if(v){var z=(typeof v==u)?v+s:v;
}else{z=t;
}
if(top){var y=(typeof top==u)?top+s:top;
}else{y=t;
}return z+b+y;
},__iW:function(A){var String=qx.lang.String;
var B=A.substr(0,50);
return String.startsWith(B,c)&&String.contains(B,a);
},compile:function(C,D,E,top){var F=this.__iV(E,top);
var G=qx.util.ResourceManager.getInstance().toUri(C);

if(this.__iW(G)){G=q+G+q;
}var H=this.__iT;
H[1]=G;
H[4]=F;
H[7]=D;
return H.join(l);
},getStyles:function(I,J,K,top){if(!I){return this.__iU;
}var L=this.__iV(K,top);
var N=qx.util.ResourceManager.getInstance().toUri(I);
var O;

if(this.__iW(N)){O=j+N+p;
}else{O=f+N+e;
}var M={backgroundPosition:L,backgroundImage:O};

if(J!=null){M.backgroundRepeat=J;
}return M;
},set:function(P,Q,R,S,top){var T=this.getStyles(Q,R,S,top);

for(var U in T){P.style[U]=T[U];
}}}});
})();
(function(){var k="source",j="scale",i="engine.name",h="no-repeat",g="",f="mshtml",e="backgroundImage",d="webkit",c="div",b="qx.html.Image",a="qx/static/blank.gif";
qx.Class.define(b,{extend:qx.html.Element,members:{tagNameHint:null,_applyProperty:function(name,l){qx.html.Element.prototype._applyProperty.call(this,name,l);

if(name===k){var p=this.getDomElement();
var m=this.getAllStyles();

if(this.getNodeName()==c&&this.getStyle(e)){m.backgroundPosition=null;
m.backgroundRepeat=null;
}var n=this._getProperty(k);
var o=this._getProperty(j);
var q=o?j:h;
if(n!=null){n=n||null;
qx.bom.element.Decoration.update(p,n,q,m);
}}},_removeProperty:function(r,s){if(r==k){this._setProperty(r,g,s);
}else{this._setProperty(r,null,s);
}},_createDomElement:function(){var u=this._getProperty(j);
var v=u?j:h;

if((qx.core.Environment.get(i)==f)){var t=this._getProperty(k);

if(this.tagNameHint!=null){this.setNodeName(this.tagNameHint);
}else{this.setNodeName(qx.bom.element.Decoration.getTagName(v,t));
}}else{this.setNodeName(qx.bom.element.Decoration.getTagName(v));
}return qx.html.Element.prototype._createDomElement.call(this);
},_copyData:function(w){return qx.html.Element.prototype._copyData.call(this,true);
},setSource:function(x){this._setProperty(k,x);
return this;
},getSource:function(){return this._getProperty(k);
},resetSource:function(){if((qx.core.Environment.get(i)==d)){this._setProperty(k,a);
}else{this._removeProperty(k,true);
}return this;
},setScale:function(y){this._setProperty(j,y);
return this;
},getScale:function(){return this._getProperty(j);
}}});
})();
(function(){var j="Integer",i="interval",h="keep-align",g="disappear",f="best-fit",e="mouse",d="bottom-left",c="direct",b="Boolean",a="bottom-right",x="widget",w="qx.ui.core.MPlacement",v="left-top",u="offsetRight",t="shorthand",s="offsetLeft",r="top-left",q="appear",p="offsetBottom",o="top-right",m="offsetTop",n="right-bottom",k="right-top",l="left-bottom";
qx.Mixin.define(w,{statics:{__eU:null,setVisibleElement:function(y){this.__eU=y;
},getVisibleElement:function(){return this.__eU;
}},properties:{position:{check:[r,o,d,a,v,l,k,n],init:d,themeable:true},placeMethod:{check:[x,e],init:e,themeable:true},domMove:{check:b,init:false},placementModeX:{check:[c,h,f],init:h,themeable:true},placementModeY:{check:[c,h,f],init:h,themeable:true},offsetLeft:{check:j,init:0,themeable:true},offsetTop:{check:j,init:0,themeable:true},offsetRight:{check:j,init:0,themeable:true},offsetBottom:{check:j,init:0,themeable:true},offset:{group:[m,u,p,s],mode:t,themeable:true}},members:{__iX:null,__iY:null,__ja:null,getLayoutLocation:function(z){var C,B,D,top;
B=z.getBounds();
D=B.left;
top=B.top;
var E=B;
z=z.getLayoutParent();

while(z&&!z.isRootWidget()){B=z.getBounds();
D+=B.left;
top+=B.top;
C=z.getInsets();
D+=C.left;
top+=C.top;
z=z.getLayoutParent();
}if(z.isRootWidget()){var A=z.getContainerLocation();

if(A){D+=A.left;
top+=A.top;
}}return {left:D,top:top,right:D+E.width,bottom:top+E.height};
},moveTo:function(F,top){var H=qx.ui.core.MPlacement.getVisibleElement();
if(H){var J=this.getBounds();
var G=H.getContentLocation();
if(J&&G){var K=top+J.height;
var I=F+J.width;
if((I>G.left&&F<G.right)&&(K>G.top&&top<G.bottom)){F=Math.max(G.left-J.width,0);
}}}
if(this.getDomMove()){this.setDomPosition(F,top);
}else{this.setLayoutProperties({left:F,top:top});
}},placeToWidget:function(L,M){if(M){this.__jb();
this.__iX=qx.lang.Function.bind(this.placeToWidget,this,L,false);
qx.event.Idle.getInstance().addListener(i,this.__iX);
this.__ja=function(){this.__jb();
};
this.addListener(g,this.__ja,this);
}var N=L.getContainerLocation()||this.getLayoutLocation(L);
this.__jd(N);
},__jb:function(){if(this.__iX){qx.event.Idle.getInstance().removeListener(i,this.__iX);
this.__iX=null;
}
if(this.__ja){this.removeListener(g,this.__ja,this);
this.__ja=null;
}},placeToMouse:function(event){var P=event.getDocumentLeft();
var top=event.getDocumentTop();
var O={left:P,top:top,right:P,bottom:top};
this.__jd(O);
},placeToElement:function(Q,R){var location=qx.bom.element.Location.get(Q);
var S={left:location.left,top:location.top,right:location.left+Q.offsetWidth,bottom:location.top+Q.offsetHeight};
if(R){this.__iX=qx.lang.Function.bind(this.placeToElement,this,Q,false);
qx.event.Idle.getInstance().addListener(i,this.__iX);
this.addListener(g,function(){if(this.__iX){qx.event.Idle.getInstance().removeListener(i,this.__iX);
this.__iX=null;
}},this);
}this.__jd(S);
},placeToPoint:function(T){var U={left:T.left,top:T.top,right:T.left,bottom:T.top};
this.__jd(U);
},_getPlacementOffsets:function(){return {left:this.getOffsetLeft(),top:this.getOffsetTop(),right:this.getOffsetRight(),bottom:this.getOffsetBottom()};
},__jc:function(V){var W=null;

if(this._computePlacementSize){var W=this._computePlacementSize();
}else if(this.isVisible()){var W=this.getBounds();
}
if(W==null){this.addListenerOnce(q,function(){this.__jc(V);
},this);
}else{V.call(this,W);
}},__jd:function(X){this.__jc(function(Y){var ba=qx.util.placement.Placement.compute(Y,this.getLayoutParent().getBounds(),X,this._getPlacementOffsets(),this.getPosition(),this.getPlacementModeX(),this.getPlacementModeY());
this.moveTo(ba.left,ba.top);
});
}},destruct:function(){this.__jb();
}});
})();
(function(){var f="interval",e="Number",d="_applyTimeoutInterval",c="qx.event.type.Event",b="qx.event.Idle",a="singleton";
qx.Class.define(b,{extend:qx.core.Object,type:a,construct:function(){qx.core.Object.call(this);
var g=new qx.event.Timer(this.getTimeoutInterval());
g.addListener(f,this._onInterval,this);
g.start();
this.__je=g;
},events:{"interval":c},properties:{timeoutInterval:{check:e,init:100,apply:d}},members:{__je:null,_applyTimeoutInterval:function(h){this.__je.setInterval(h);
},_onInterval:function(){this.fireEvent(f);
}},destruct:function(){if(this.__je){this.__je.stop();
}this.__je=null;
}});
})();
(function(){var o="top",n="right",m="bottom",l="left",k="align-start",j="qx.util.placement.AbstractAxis",i="edge-start",h="align-end",g="edge-end",f="-",c="best-fit",e="qx.util.placement.Placement",d="keep-align",b='__jf',a="direct";
qx.Class.define(e,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__jf=new qx.util.placement.DirectAxis();
},properties:{axisX:{check:j},axisY:{check:j},edge:{check:[o,n,m,l],init:o},align:{check:[o,n,m,l],init:n}},statics:{__jg:null,compute:function(p,q,r,s,t,u,v){this.__jg=this.__jg||new qx.util.placement.Placement();
var y=t.split(f);
var x=y[0];
var w=y[1];
this.__jg.set({axisX:this.__jk(u),axisY:this.__jk(v),edge:x,align:w});
return this.__jg.compute(p,q,r,s);
},__jh:null,__ji:null,__jj:null,__jk:function(z){switch(z){case a:this.__jh=this.__jh||new qx.util.placement.DirectAxis();
return this.__jh;
case d:this.__ji=this.__ji||new qx.util.placement.KeepAlignAxis();
return this.__ji;
case c:this.__jj=this.__jj||new qx.util.placement.BestFitAxis();
return this.__jj;
default:throw new Error("Invalid 'mode' argument!'");
}}},members:{__jf:null,compute:function(A,B,C,D){var E=this.getAxisX()||this.__jf;
var G=E.computeStart(A.width,{start:C.left,end:C.right},{start:D.left,end:D.right},B.width,this.__jl());
var F=this.getAxisY()||this.__jf;
var top=F.computeStart(A.height,{start:C.top,end:C.bottom},{start:D.top,end:D.bottom},B.height,this.__jm());
return {left:G,top:top};
},__jl:function(){var I=this.getEdge();
var H=this.getAlign();

if(I==l){return i;
}else if(I==n){return g;
}else if(H==l){return k;
}else if(H==n){return h;
}},__jm:function(){var K=this.getEdge();
var J=this.getAlign();

if(K==o){return i;
}else if(K==m){return g;
}else if(J==o){return k;
}else if(J==m){return h;
}}},destruct:function(){this._disposeObjects(b);
}});
})();
(function(){var e="edge-start",d="align-start",c="align-end",b="edge-end",a="qx.util.placement.AbstractAxis";
qx.Class.define(a,{extend:qx.core.Object,members:{computeStart:function(f,g,h,i,j){throw new Error("abstract method call!");
},_moveToEdgeAndAlign:function(k,l,m,n){switch(n){case e:return l.start-m.end-k;
case b:return l.end+m.start;
case d:return l.start+m.start;
case c:return l.end-m.end-k;
}},_isInRange:function(o,p,q){return o>=0&&o+p<=q;
}}});
})();
(function(){var a="qx.util.placement.DirectAxis";
qx.Class.define(a,{extend:qx.util.placement.AbstractAxis,members:{computeStart:function(b,c,d,e,f){return this._moveToEdgeAndAlign(b,c,d,f);
}}});
})();
(function(){var c="qx.util.placement.KeepAlignAxis",b="edge-start",a="edge-end";
qx.Class.define(c,{extend:qx.util.placement.AbstractAxis,members:{computeStart:function(d,e,f,g,h){var i=this._moveToEdgeAndAlign(d,e,f,h);
var j,k;

if(this._isInRange(i,d,g)){return i;
}
if(h==b||h==a){j=e.start-f.end;
k=e.end+f.start;
}else{j=e.end-f.end;
k=e.start+f.start;
}
if(j>g-k){i=j-d;
}else{i=k;
}return i;
}}});
})();
(function(){var a="qx.util.placement.BestFitAxis";
qx.Class.define(a,{extend:qx.util.placement.AbstractAxis,members:{computeStart:function(b,c,d,e,f){var g=this._moveToEdgeAndAlign(b,c,d,f);

if(this._isInRange(g,b,e)){return g;
}
if(g<0){g=Math.min(0,e-b);
}
if(g+b>e){g=Math.max(0,e-b);
}return g;
}}});
})();
(function(){var j="nonScaled",i="scaled",h="alphaScaled",g=".png",f="div",e="replacement",d="qx.event.type.Event",c="engine.name",b="hidden",a="__jn",y="Boolean",x="px",w="scale",v="changeSource",u="qx.ui.basic.Image",t="loaded",s="-disabled.$1",r="loadingFailed",q="String",p="_applySource",n="img",o="image",l="mshtml",m="_applyScale",k="no-repeat";
qx.Class.define(u,{extend:qx.ui.core.Widget,construct:function(z){this.__jn={};
qx.ui.core.Widget.call(this);

if(z){this.setSource(z);
}},properties:{source:{check:q,init:null,nullable:true,event:v,apply:p,themeable:true},scale:{check:y,init:false,themeable:true,apply:m},appearance:{refine:true,init:o},allowShrinkX:{refine:true,init:false},allowShrinkY:{refine:true,init:false},allowGrowX:{refine:true,init:false},allowGrowY:{refine:true,init:false}},events:{loadingFailed:d,loaded:d},members:{__jo:null,__jp:null,__fv:null,__jn:null,getContentElement:function(){return this.__jt();
},_createContentElement:function(){return this.__jt();
},_getContentHint:function(){return {width:this.__jo||0,height:this.__jp||0};
},_applyEnabled:function(A,B){qx.ui.core.Widget.prototype._applyEnabled.call(this,A,B);

if(this.getSource()){this._styleSource();
}},_applySource:function(C){this._styleSource();
},_applyScale:function(D){this._styleSource();
},__jq:function(E){this.__fv=E;
},__jr:function(){if(this.__fv==null){var G=this.getSource();
var F=false;

if(G!=null){F=qx.lang.String.endsWith(G,g);
}
if(this.getScale()&&F&&qx.bom.element.Decoration.isAlphaImageLoaderEnabled()){this.__fv=h;
}else if(this.getScale()){this.__fv=i;
}else{this.__fv=j;
}}return this.__fv;
},__js:function(H){var I;
var J;

if(H==h){I=true;
J=f;
}else if(H==j){I=false;
J=f;
}else{I=true;
J=n;
}var K=new qx.html.Image(J);
K.setScale(I);
K.setStyles({"overflowX":b,"overflowY":b});
return K;
},__jt:function(){var L=this.__jr();

if(this.__jn[L]==null){this.__jn[L]=this.__js(L);
}return this.__jn[L];
},_styleSource:function(){var M=qx.util.AliasManager.getInstance().resolve(this.getSource());

if(!M){this.getContentElement().resetSource();
return;
}this.__ju(M);

if((qx.core.Environment.get(c)==l)){var N=this.getScale()?w:k;
this.getContentElement().tagNameHint=qx.bom.element.Decoration.getTagName(N,M);
}if(qx.util.ResourceManager.getInstance().has(M)){this.__jw(this.getContentElement(),M);
}else if(qx.io.ImageLoader.isLoaded(M)){this.__jx(this.getContentElement(),M);
}else{this.__jy(this.getContentElement(),M);
}},__ju:qx.core.Environment.select(c,{"mshtml":function(O){var Q=qx.bom.element.Decoration.isAlphaImageLoaderEnabled();
var P=qx.lang.String.endsWith(O,g);

if(Q&&P){if(this.getScale()&&this.__jr()!=h){this.__jq(h);
}else if(!this.getScale()&&this.__jr()!=j){this.__jq(j);
}}else{if(this.getScale()&&this.__jr()!=i){this.__jq(i);
}else if(!this.getScale()&&this.__jr()!=j){this.__jq(j);
}}this.__jv(this.__jt());
},"default":function(R){if(this.getScale()&&this.__jr()!=i){this.__jq(i);
}else if(!this.getScale()&&this.__jr(j)){this.__jq(j);
}this.__jv(this.__jt());
}}),__jv:function(S){var V=this.getContainerElement();
var W=V.getChild(0);

if(W!=S){if(W!=null){var Y=x;
var T={};
var U=this.getInnerSize();

if(U!=null){T.width=U.width+Y;
T.height=U.height+Y;
}var X=this.getInsets();
T.left=X.left+Y;
T.top=X.top+Y;
T.zIndex=10;
S.setStyles(T,true);
S.setSelectable(this.getSelectable());
}V.removeAt(0);
V.addAt(S,0);
}},__jw:function(ba,bb){var bd=qx.util.ResourceManager.getInstance();
if(!this.getEnabled()){var bc=bb.replace(/\.([a-z]+)$/,s);

if(bd.has(bc)){bb=bc;
this.addState(e);
}else{this.removeState(e);
}}if(ba.getSource()===bb){return;
}ba.setSource(bb);
this.__jA(bd.getImageWidth(bb),bd.getImageHeight(bb));
},__jx:function(be,bf){var bh=qx.io.ImageLoader;
be.setSource(bf);
var bg=bh.getWidth(bf);
var bi=bh.getHeight(bf);
this.__jA(bg,bi);
},__jy:function(bj,bk){var self;
var bl=qx.io.ImageLoader;
if(!bl.isFailed(bk)){bl.load(bk,this.__jz,this);
}else{if(bj!=null){bj.resetSource();
}}},__jz:function(bm,bn){if(this.$$disposed===true){return;
}if(bm!==qx.util.AliasManager.getInstance().resolve(this.getSource())){return;
}if(bn.failed){this.warn("Image could not be loaded: "+bm);
this.fireEvent(r);
}else if(bn.aborted){return ;
}else{this.fireEvent(t);
}this._styleSource();
},__jA:function(bo,bp){if(bo!==this.__jo||bp!==this.__jp){this.__jo=bo;
this.__jp=bp;
qx.ui.core.queue.Layout.add(this);
}}},destruct:function(){this._disposeMap(a);
}});
})();
(function(){var g="dragdrop-cursor",f="_applyAction",e="alias",d="qx.ui.core.DragDropCursor",c="move",b="singleton",a="copy";
qx.Class.define(d,{extend:qx.ui.basic.Image,include:qx.ui.core.MPlacement,type:b,construct:function(){qx.ui.basic.Image.call(this);
this.setZIndex(1e8);
this.setDomMove(true);
var h=this.getApplicationRoot();
h.add(this,{left:-1000,top:-1000});
},properties:{appearance:{refine:true,init:g},action:{check:[e,a,c],apply:f,nullable:true}},members:{_applyAction:function(i,j){if(j){this.removeState(j);
}
if(i){this.addState(i);
}}}});
})();
(function(){var d="qx.event.type.Data",c="qx.ui.container.Composite",b="addChildWidget",a="removeChildWidget";
qx.Class.define(c,{extend:qx.ui.core.Widget,include:[qx.ui.core.MChildrenHandling,qx.ui.core.MLayoutHandling],construct:function(e){qx.ui.core.Widget.call(this);

if(e!=null){this._setLayout(e);
}},events:{addChildWidget:d,removeChildWidget:d},members:{_afterAddChild:function(f){this.fireNonBubblingEvent(b,qx.event.type.Data,[f]);
},_afterRemoveChild:function(g){this.fireNonBubblingEvent(a,qx.event.type.Data,[g]);
}},defer:function(h,i){qx.ui.core.MChildrenHandling.remap(i);
qx.ui.core.MLayoutHandling.remap(i);
}});
})();
(function(){var e="qx.ui.popup.Popup",d="visible",c="excluded",b="popup",a="Boolean";
qx.Class.define(e,{extend:qx.ui.container.Composite,include:qx.ui.core.MPlacement,construct:function(f){qx.ui.container.Composite.call(this,f);
this.initVisibility();
},properties:{appearance:{refine:true,init:b},visibility:{refine:true,init:c},autoHide:{check:a,init:true}},members:{show:function(){if(this.getLayoutParent()==null){qx.core.Init.getApplication().getRoot().add(this);
}qx.ui.container.Composite.prototype.show.call(this);
},_applyVisibility:function(g,h){qx.ui.container.Composite.prototype._applyVisibility.call(this,g,h);
var i=qx.ui.popup.Manager.getInstance();
g===d?i.add(this):i.remove(this);
}},destruct:function(){qx.ui.popup.Manager.getInstance().remove(this);
}});
})();
(function(){var f="mousedown",d="__jB",c="blur",b="singleton",a="qx.ui.popup.Manager";
qx.Class.define(a,{type:b,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__jB=[];
qx.event.Registration.addListener(document.documentElement,f,this.__jD,this,true);
qx.bom.Element.addListener(window,c,this.hideAll,this);
},members:{__jB:null,add:function(g){this.__jB.push(g);
this.__jC();
},remove:function(h){if(this.__jB){qx.lang.Array.remove(this.__jB,h);
this.__jC();
}},hideAll:function(){var j;
var k=this.__jB;

if(k){for(var i=0,l=k.length;i<l;i++){var j=k[i];
j.getAutoHide()&&j.exclude();
}}},__jC:function(){var m=1e7;

for(var i=0;i<this.__jB.length;i++){this.__jB[i].setZIndex(m++);
}},__jD:function(e){var o=qx.ui.core.Widget.getWidgetByElement(e.getTarget());
var p=this.__jB;

for(var i=0;i<p.length;i++){var n=p[i];

if(!n.getAutoHide()||o==n||qx.ui.core.Widget.contains(n,o)){continue;
}n.exclude();
}}},destruct:function(){qx.event.Registration.removeListener(document.documentElement,f,this.__jD,this,true);
this._disposeArray(d);
}});
})();
(function(){var l="atom",k="Integer",j="String",i="_applyRich",h="qx.ui.tooltip.ToolTip",g="_applyIcon",f="tooltip",d="qx.ui.core.Widget",c="mouseover",b="Boolean",a="_applyLabel";
qx.Class.define(h,{extend:qx.ui.popup.Popup,construct:function(m,n){qx.ui.popup.Popup.call(this);
this.setLayout(new qx.ui.layout.Grow);
this._createChildControl(l);
if(m!=null){this.setLabel(m);
}
if(n!=null){this.setIcon(n);
}this.addListener(c,this._onMouseOver,this);
},properties:{appearance:{refine:true,init:f},showTimeout:{check:k,init:700,themeable:true},hideTimeout:{check:k,init:4000,themeable:true},label:{check:j,nullable:true,apply:a},icon:{check:j,nullable:true,apply:g,themeable:true},rich:{check:b,init:false,apply:i},opener:{check:d,nullable:true}},members:{_createChildControlImpl:function(o,p){var q;

switch(o){case l:q=new qx.ui.basic.Atom;
this._add(q);
break;
}return q||qx.ui.popup.Popup.prototype._createChildControlImpl.call(this,o);
},_onMouseOver:function(e){this.hide();
},_applyIcon:function(r,s){var t=this.getChildControl(l);
r==null?t.resetIcon():t.setIcon(r);
},_applyLabel:function(u,v){var w=this.getChildControl(l);
u==null?w.resetLabel():w.setLabel(u);
},_applyRich:function(x,y){var z=this.getChildControl(l);
z.setRich(x);
}}});
})();
(function(){var b="abstract",a="qx.ui.layout.Abstract";
qx.Class.define(a,{type:b,extend:qx.core.Object,members:{__hB:null,_invalidChildrenCache:null,__jE:null,invalidateLayoutCache:function(){this.__hB=null;
},renderLayout:function(c,d){this.warn("Missing renderLayout() implementation!");
},getSizeHint:function(){if(this.__hB){return this.__hB;
}return this.__hB=this._computeSizeHint();
},hasHeightForWidth:function(){return false;
},getHeightForWidth:function(e){this.warn("Missing getHeightForWidth() implementation!");
return null;
},_computeSizeHint:function(){return null;
},invalidateChildrenCache:function(){this._invalidChildrenCache=true;
},verifyLayoutProperty:null,_clearSeparators:function(){var f=this.__jE;

if(f instanceof qx.ui.core.LayoutItem){f.clearSeparators();
}},_renderSeparator:function(g,h){this.__jE.renderSeparator(g,h);
},connectToWidget:function(i){if(i&&this.__jE){throw new Error("It is not possible to manually set the connected widget.");
}this.__jE=i;
this.invalidateChildrenCache();
},_getWidget:function(){return this.__jE;
},_applyLayoutChange:function(){if(this.__jE){this.__jE.scheduleLayoutUpdate();
}},_getLayoutChildren:function(){return this.__jE.getLayoutChildren();
}},destruct:function(){this.__jE=this.__hB=null;
}});
})();
(function(){var a="qx.ui.layout.Grow";
qx.Class.define(a,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(b,c){var g=this._getLayoutChildren();
var f,h,e,d;
for(var i=0,l=g.length;i<l;i++){f=g[i];
h=f.getSizeHint();
e=b;

if(e<h.minWidth){e=h.minWidth;
}else if(e>h.maxWidth){e=h.maxWidth;
}d=c;

if(d<h.minHeight){d=h.minHeight;
}else if(d>h.maxHeight){d=h.maxHeight;
}f.renderLayout(0,0,e,d);
}},_computeSizeHint:function(){var q=this._getLayoutChildren();
var o,s;
var r=0,p=0;
var n=0,k=0;
var j=Infinity,m=Infinity;
for(var i=0,l=q.length;i<l;i++){o=q[i];
s=o.getSizeHint();
r=Math.max(r,s.width);
p=Math.max(p,s.height);
n=Math.max(n,s.minWidth);
k=Math.max(k,s.minHeight);
j=Math.min(j,s.maxWidth);
m=Math.min(m,s.maxHeight);
}return {width:r,height:p,minWidth:n,minHeight:k,maxWidth:j,maxHeight:m};
}}});
})();
(function(){var j="label",i="icon",h="Boolean",g="both",f="String",e="left",d="changeGap",c="changeShow",b="bottom",a="_applyCenter",y="changeIcon",x="qx.ui.basic.Atom",w="changeLabel",v="Integer",u="_applyIconPosition",t="bottom-left",s="top-left",r="top",q="right",p="_applyRich",n="_applyIcon",o="_applyShow",l="_applyLabel",m="_applyGap",k="atom";
qx.Class.define(x,{extend:qx.ui.core.Widget,construct:function(z,A){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.Atom());

if(z!=null){this.setLabel(z);
}
if(A!=null){this.setIcon(A);
}},properties:{appearance:{refine:true,init:k},label:{apply:l,nullable:true,check:f,event:w},rich:{check:h,init:false,apply:p},icon:{check:f,apply:n,nullable:true,themeable:true,event:y},gap:{check:v,nullable:false,event:d,apply:m,themeable:true,init:4},show:{init:g,check:[g,j,i],themeable:true,inheritable:true,apply:o,event:c},iconPosition:{init:e,check:[r,q,b,e,s,t],themeable:true,apply:u},center:{init:false,check:h,themeable:true,apply:a}},members:{_createChildControlImpl:function(B,C){var D;

switch(B){case j:D=new qx.ui.basic.Label(this.getLabel());
D.setAnonymous(true);
D.setRich(this.getRich());
this._add(D);

if(this.getLabel()==null||this.getShow()===i){D.exclude();
}break;
case i:D=new qx.ui.basic.Image(this.getIcon());
D.setAnonymous(true);
this._addAt(D,0);

if(this.getIcon()==null||this.getShow()===j){D.exclude();
}break;
}return D||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,B);
},_forwardStates:{focused:true,hovered:true},_handleLabel:function(){if(this.getLabel()==null||this.getShow()===i){this._excludeChildControl(j);
}else{this._showChildControl(j);
}},_handleIcon:function(){if(this.getIcon()==null||this.getShow()===j){this._excludeChildControl(i);
}else{this._showChildControl(i);
}},_applyLabel:function(E,F){var G=this.getChildControl(j,true);

if(G){G.setValue(E);
}this._handleLabel();
},_applyRich:function(H,I){var J=this.getChildControl(j,true);

if(J){J.setRich(H);
}},_applyIcon:function(K,L){var M=this.getChildControl(i,true);

if(M){M.setSource(K);
}this._handleIcon();
},_applyGap:function(N,O){this._getLayout().setGap(N);
},_applyShow:function(P,Q){this._handleLabel();
this._handleIcon();
},_applyIconPosition:function(R,S){this._getLayout().setIconPosition(R);
},_applyCenter:function(T,U){this._getLayout().setCenter(T);
},_applySelectable:function(V,W){qx.ui.core.Widget.prototype._applySelectable.call(this,V,W);
var X=this.getChildControl(j,true);

if(X){this.getChildControl(j).setSelectable(V);
}}}});
})();
(function(){var m="bottom",l="top",k="_applyLayoutChange",j="top-left",h="bottom-left",g="left",f="right",e="middle",d="center",c="qx.ui.layout.Atom",a="Integer",b="Boolean";
qx.Class.define(c,{extend:qx.ui.layout.Abstract,properties:{gap:{check:a,init:4,apply:k},iconPosition:{check:[g,l,f,m,j,h],init:g,apply:k},center:{check:b,init:false,apply:k}},members:{verifyLayoutProperty:null,renderLayout:function(n,o){var x=qx.ui.layout.Util;
var q=this.getIconPosition();
var t=this._getLayoutChildren();
var length=t.length;
var I,top,y,r;
var D,w;
var B=this.getGap();
var G=this.getCenter();
if(q===m||q===f){var z=length-1;
var u=-1;
var s=-1;
}else{var z=0;
var u=length;
var s=1;
}if(q==l||q==m){if(G){var C=0;

for(var i=z;i!=u;i+=s){r=t[i].getSizeHint().height;

if(r>0){C+=r;

if(i!=z){C+=B;
}}}top=Math.round((o-C)/2);
}else{top=0;
}
for(var i=z;i!=u;i+=s){D=t[i];
w=D.getSizeHint();
y=Math.min(w.maxWidth,Math.max(n,w.minWidth));
r=w.height;
I=x.computeHorizontalAlignOffset(d,y,n);
D.renderLayout(I,top,y,r);
if(r>0){top+=r+B;
}}}else{var v=n;
var p=null;
var F=0;

for(var i=z;i!=u;i+=s){D=t[i];
y=D.getSizeHint().width;

if(y>0){if(!p&&D instanceof qx.ui.basic.Label){p=D;
}else{v-=y;
}F++;
}}
if(F>1){var E=(F-1)*B;
v-=E;
}
if(p){var w=p.getSizeHint();
var A=Math.max(w.minWidth,Math.min(v,w.maxWidth));
v-=A;
}
if(G&&v>0){I=Math.round(v/2);
}else{I=0;
}
for(var i=z;i!=u;i+=s){D=t[i];
w=D.getSizeHint();
r=Math.min(w.maxHeight,Math.max(o,w.minHeight));

if(D===p){y=A;
}else{y=w.width;
}var H=e;

if(q==j){H=l;
}else if(q==h){H=m;
}top=x.computeVerticalAlignOffset(H,w.height,o);
D.renderLayout(I,top,y,r);
if(y>0){I+=y+B;
}}}},_computeSizeHint:function(){var T=this._getLayoutChildren();
var length=T.length;
var L,R;
if(length===1){var L=T[0].getSizeHint();
R={width:L.width,height:L.height,minWidth:L.minWidth,minHeight:L.minHeight};
}else{var P=0,Q=0;
var M=0,O=0;
var N=this.getIconPosition();
var S=this.getGap();

if(N===l||N===m){var J=0;

for(var i=0;i<length;i++){L=T[i].getSizeHint();
Q=Math.max(Q,L.width);
P=Math.max(P,L.minWidth);
if(L.height>0){O+=L.height;
M+=L.minHeight;
J++;
}}
if(J>1){var K=(J-1)*S;
O+=K;
M+=K;
}}else{var J=0;

for(var i=0;i<length;i++){L=T[i].getSizeHint();
O=Math.max(O,L.height);
M=Math.max(M,L.minHeight);
if(L.width>0){Q+=L.width;
P+=L.minWidth;
J++;
}}
if(J>1){var K=(J-1)*S;
Q+=K;
P+=K;
}}R={minWidth:P,width:Q,minHeight:M,height:O};
}return R;
}}});
})();
(function(){var g="middle",f="qx.ui.layout.Util",e="left",d="center",c="top",b="bottom",a="right";
qx.Class.define(f,{statics:{PERCENT_VALUE:/[0-9]+(?:\.[0-9]+)?%/,computeFlexOffsets:function(h,j,k){var n,r,m,s;
var o=j>k;
var t=Math.abs(j-k);
var u,p;
var q={};

for(r in h){n=h[r];
q[r]={potential:o?n.max-n.value:n.value-n.min,flex:o?n.flex:1/n.flex,offset:0};
}while(t!=0){s=Infinity;
m=0;

for(r in q){n=q[r];

if(n.potential>0){m+=n.flex;
s=Math.min(s,n.potential/n.flex);
}}if(m==0){break;
}s=Math.min(t,s*m)/m;
u=0;

for(r in q){n=q[r];

if(n.potential>0){p=Math.min(t,n.potential,Math.ceil(s*n.flex));
u+=p-s*n.flex;

if(u>=1){u-=1;
p-=1;
}n.potential-=p;

if(o){n.offset+=p;
}else{n.offset-=p;
}t-=p;
}}}return q;
},computeHorizontalAlignOffset:function(v,w,x,y,z){if(y==null){y=0;
}
if(z==null){z=0;
}var A=0;

switch(v){case e:A=y;
break;
case a:A=x-w-z;
break;
case d:A=Math.round((x-w)/2);
if(A<y){A=y;
}else if(A<z){A=Math.max(y,x-w-z);
}break;
}return A;
},computeVerticalAlignOffset:function(B,C,D,E,F){if(E==null){E=0;
}
if(F==null){F=0;
}var G=0;

switch(B){case c:G=E;
break;
case b:G=D-C-F;
break;
case g:G=Math.round((D-C)/2);
if(G<E){G=E;
}else if(G<F){G=Math.max(E,D-C-F);
}break;
}return G;
},collapseMargins:function(H){var I=0,K=0;

for(var i=0,l=arguments.length;i<l;i++){var J=arguments[i];

if(J<0){K=Math.min(K,J);
}else if(J>0){I=Math.max(I,J);
}}return I+K;
},computeHorizontalGaps:function(L,M,N){if(M==null){M=0;
}var O=0;

if(N){O+=L[0].getMarginLeft();

for(var i=1,l=L.length;i<l;i+=1){O+=this.collapseMargins(M,L[i-1].getMarginRight(),L[i].getMarginLeft());
}O+=L[l-1].getMarginRight();
}else{for(var i=1,l=L.length;i<l;i+=1){O+=L[i].getMarginLeft()+L[i].getMarginRight();
}O+=(M*(l-1));
}return O;
},computeVerticalGaps:function(P,Q,R){if(Q==null){Q=0;
}var S=0;

if(R){S+=P[0].getMarginTop();

for(var i=1,l=P.length;i<l;i+=1){S+=this.collapseMargins(Q,P[i-1].getMarginBottom(),P[i].getMarginTop());
}S+=P[l-1].getMarginBottom();
}else{for(var i=1,l=P.length;i<l;i+=1){S+=P[i].getMarginTop()+P[i].getMarginBottom();
}S+=(Q*(l-1));
}return S;
},computeHorizontalSeparatorGaps:function(T,U,V){var Y=qx.theme.manager.Decoration.getInstance().resolve(V);
var X=Y.getInsets();
var W=X.left+X.right;
var ba=0;

for(var i=0,l=T.length;i<l;i++){var bb=T[i];
ba+=bb.getMarginLeft()+bb.getMarginRight();
}ba+=(U+W+U)*(l-1);
return ba;
},computeVerticalSeparatorGaps:function(bc,bd,be){var bh=qx.theme.manager.Decoration.getInstance().resolve(be);
var bg=bh.getInsets();
var bf=bg.top+bg.bottom;
var bi=0;

for(var i=0,l=bc.length;i<l;i++){var bj=bc[i];
bi+=bj.getMarginTop()+bj.getMarginBottom();
}bi+=(bd+bf+bd)*(l-1);
return bi;
},arrangeIdeals:function(bk,bl,bm,bn,bo,bp){if(bl<bk||bo<bn){if(bl<bk&&bo<bn){bl=bk;
bo=bn;
}else if(bl<bk){bo-=(bk-bl);
bl=bk;
if(bo<bn){bo=bn;
}}else if(bo<bn){bl-=(bn-bo);
bo=bn;
if(bl<bk){bl=bk;
}}}
if(bl>bm||bo>bp){if(bl>bm&&bo>bp){bl=bm;
bo=bp;
}else if(bl>bm){bo+=(bl-bm);
bl=bm;
if(bo>bp){bo=bp;
}}else if(bo>bp){bl+=(bo-bp);
bo=bp;
if(bl>bm){bl=bm;
}}}return {begin:bl,end:bo};
}}});
})();
(function(){var b="qx.event.type.Data",a="qx.ui.form.IStringForm";
qx.Interface.define(a,{events:{"changeValue":b},members:{setValue:function(c){return arguments.length==1;
},resetValue:function(){},getValue:function(){}}});
})();
(function(){var k="qx.dynlocale",j="Boolean",i="color",h="enabled",g="changeLocale",f="_applyTextAlign",d="qx.ui.core.Widget",c="nowrap",b="changeStatus",a="changeTextAlign",E="_applyWrap",D="changeValue",C="qx.ui.basic.Label",B="whiteSpace",A="css.textoverflow",z="html.xul",y="_applyValue",x="center",w="_applyBuddy",v="String",r="textAlign",s="right",p="justify",q="changeRich",n="normal",o="_applyRich",l="click",m="label",t="left",u="A";
qx.Class.define(C,{extend:qx.ui.core.Widget,implement:[qx.ui.form.IStringForm],construct:function(F){qx.ui.core.Widget.call(this);

if(F!=null){this.setValue(F);
}
if(qx.core.Environment.get(k)){qx.locale.Manager.getInstance().addListener(g,this._onChangeLocale,this);
}},properties:{rich:{check:j,init:false,event:q,apply:o},wrap:{check:j,init:true,apply:E},value:{check:v,apply:y,event:D,nullable:true},buddy:{check:d,apply:w,nullable:true,init:null,dereference:true},textAlign:{check:[t,x,s,p],nullable:true,themeable:true,apply:f,event:a},appearance:{refine:true,init:m},selectable:{refine:true,init:false},allowGrowX:{refine:true,init:false},allowGrowY:{refine:true,init:false},allowShrinkY:{refine:true,init:false}},members:{__jF:null,__jG:null,__jH:null,__jI:null,__jJ:null,_getContentHint:function(){if(this.__jG){this.__jK=this.__jL();
delete this.__jG;
}return {width:this.__jK.width,height:this.__jK.height};
},_hasHeightForWidth:function(){return this.getRich()&&this.getWrap();
},_applySelectable:function(G){if(!qx.core.Environment.get(A)&&qx.core.Environment.get(z)){if(G&&!this.isRich()){return;
}}qx.ui.core.Widget.prototype._applySelectable.call(this,G);
},_getContentHeightForWidth:function(H){if(!this.getRich()&&!this.getWrap()){return null;
}return this.__jL(H).height;
},_createContentElement:function(){return new qx.html.Label;
},_applyTextAlign:function(I,J){this.getContentElement().setStyle(r,I);
},_applyTextColor:function(K,L){if(K){this.getContentElement().setStyle(i,qx.theme.manager.Color.getInstance().resolve(K));
}else{this.getContentElement().removeStyle(i);
}},__jK:{width:0,height:0},_applyFont:function(M,N){if(N&&this.__jF&&this.__jJ){this.__jF.removeListenerById(this.__jJ);
this.__jJ=null;
}var O;

if(M){this.__jF=qx.theme.manager.Font.getInstance().resolve(M);

if(this.__jF instanceof qx.bom.webfonts.WebFont){this.__jJ=this.__jF.addListener(b,this._onWebFontStatusChange,this);
}O=this.__jF.getStyles();
}else{this.__jF=null;
O=qx.bom.Font.getDefaultStyles();
}this.getContentElement().setStyles(O);
this.__jG=true;
qx.ui.core.queue.Layout.add(this);
},__jL:function(P){var T=qx.bom.Label;
var R=this.getFont();
var Q=R?this.__jF.getStyles():qx.bom.Font.getDefaultStyles();
var content=this.getValue()||u;
var S=this.getRich();
return S?T.getHtmlSize(content,Q,P):T.getTextSize(content,Q);
},_applyBuddy:function(U,V){if(V!=null){V.removeBinding(this.__jH);
this.__jH=null;
this.removeListenerById(this.__jI);
this.__jI=null;
}
if(U!=null){this.__jH=U.bind(h,this,h);
this.__jI=this.addListener(l,function(){if(U.isFocusable()){U.focus.apply(U);
}},this);
}},_applyRich:function(W){this.getContentElement().setRich(W);
this.__jG=true;
qx.ui.core.queue.Layout.add(this);
},_applyWrap:function(X,Y){if(X&&!this.isRich()){}
if(this.isRich()){var ba=X?n:c;
this.getContentElement().setStyle(B,ba);
}},_onChangeLocale:qx.core.Environment.select(k,{"true":function(e){var content=this.getValue();

if(content&&content.translate){this.setValue(content.translate());
}},"false":null}),_onWebFontStatusChange:function(bb){if(bb.getData().valid===true){this.__jG=true;
qx.ui.core.queue.Layout.add(this);
}},_applyValue:function(bc,bd){this.getContentElement().setValue(bc);
this.__jG=true;
qx.ui.core.queue.Layout.add(this);
}},destruct:function(){if(qx.core.Environment.get(k)){qx.locale.Manager.getInstance().removeListener(g,this._onChangeLocale,this);
}if(this.__jH!=null){var be=this.getBuddy();

if(be!=null&&!be.isDisposed()){be.removeBinding(this.__jH);
}}
if(this.__jF&&this.__jJ){this.__jF.removeListenerById(this.__jJ);
}this.__jF=this.__jH=null;
}});
})();
(function(){var b="value",a="qx.html.Label";
qx.Class.define(a,{extend:qx.html.Element,members:{__jM:null,_applyProperty:function(name,c){qx.html.Element.prototype._applyProperty.call(this,name,c);

if(name==b){var d=this.getDomElement();
qx.bom.Label.setValue(d,c);
}},_createDomElement:function(){var f=this.__jM;
var e=qx.bom.Label.create(this._content,f);
return e;
},_copyData:function(g){return qx.html.Element.prototype._copyData.call(this,true);
},setRich:function(h){var i=this.getDomElement();

if(i){throw new Error("The label mode cannot be modified after initial creation");
}h=!!h;

if(this.__jM==h){return;
}this.__jM=h;
return this;
},setValue:function(j){this._setProperty(b,j);
return this;
},getValue:function(){return this._getProperty(b);
}}});
})();
(function(){var j="css.textoverflow",i="html.xul",h="div",g="auto",f="0",e="inherit",d="text",c="value",b="",a="engine.name",C="hidden",B="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul",A="nowrap",z="ellipsis",y="normal",x="block",w="label",v="px",u="crop",t="gecko",q="end",r="100%",o="visible",p="qx.bom.Label",m="opera",n="engine.version",k="mshtml",l="-1000px",s="absolute";
qx.Class.define(p,{statics:{__jN:{fontFamily:1,fontSize:1,fontWeight:1,fontStyle:1,lineHeight:1},__jO:function(){var D=this.__jQ(false);
document.body.insertBefore(D,document.body.firstChild);
return this._textElement=D;
},__jP:function(){var E=this.__jQ(true);
document.body.insertBefore(E,document.body.firstChild);
return this._htmlElement=E;
},__jQ:function(F){var G=qx.bom.Element.create(h);
var H=G.style;
H.width=H.height=g;
H.left=H.top=l;
H.visibility=C;
H.position=s;
H.overflow=o;
H.display=x;

if(F){H.whiteSpace=y;
}else{H.whiteSpace=A;

if(!qx.core.Environment.get(j)&&qx.core.Environment.get(i)){var I=document.createElementNS(B,w);
var H=I.style;
H.padding=f;
H.margin=f;
H.width=g;

for(var J in this.__jN){H[J]=e;
}G.appendChild(I);
}}return G;
},__jR:function(K){var L={};

if(K){L.whiteSpace=y;
}else if(!qx.core.Environment.get(j)&&qx.core.Environment.get(i)){L.display=x;
}else{L.overflow=C;
L.whiteSpace=A;
L.textOverflow=z;
if((qx.core.Environment.get(a)==m)){L.OTextOverflow=z;
}}return L;
},create:function(content,M,N){if(!N){N=window;
}
if(M){var O=N.document.createElement(h);
O.useHtml=true;
}else if(!qx.core.Environment.get(j)&&qx.core.Environment.get(i)){var O=N.document.createElement(h);
var Q=N.document.createElementNS(B,w);
var P=Q.style;
P.cursor=e;
P.color=e;
P.overflow=C;
P.maxWidth=r;
P.padding=f;
P.margin=f;
P.width=g;
for(var R in this.__jN){Q.style[R]=e;
}Q.setAttribute(u,q);
O.appendChild(Q);
}else{var O=N.document.createElement(h);
qx.bom.element.Style.setStyles(O,this.__jR(M));
}
if(content){this.setValue(O,content);
}return O;
},setValue:function(S,T){T=T||b;

if(S.useHtml){S.innerHTML=T;
}else if(!qx.core.Environment.get(j)&&qx.core.Environment.get(i)){S.firstChild.setAttribute(c,T);
}else{qx.bom.element.Attribute.set(S,d,T);
}},getValue:function(U){if(U.useHtml){return U.innerHTML;
}else if(!qx.core.Environment.get(j)&&qx.core.Environment.get(i)){return U.firstChild.getAttribute(c)||b;
}else{return qx.bom.element.Attribute.get(U,d);
}},getHtmlSize:function(content,V,W){var X=this._htmlElement||this.__jP();
X.style.width=W!=undefined?W+v:g;
X.innerHTML=content;
return this.__jS(X,V);
},getTextSize:function(Y,ba){var bb=this._textElement||this.__jO();

if(!qx.core.Environment.get(j)&&qx.core.Environment.get(i)){bb.firstChild.setAttribute(c,Y);
}else{qx.bom.element.Attribute.set(bb,d,Y);
}return this.__jS(bb,ba);
},__jS:function(bc,bd){var be=this.__jN;

if(!bd){bd={};
}
for(var bf in be){bc.style[bf]=bd[bf]||b;
}var bg=qx.bom.element.Dimension.getSize(bc);
if((qx.core.Environment.get(a)==t)){bg.width++;
}if((qx.core.Environment.get(a)==k)&&parseFloat(qx.core.Environment.get(n))>=9){bg.width++;
}return bg;
}}});
})();
(function(){var b="qx.event.type.Data",a="qx.ui.form.IForm";
qx.Interface.define(a,{events:{"changeEnabled":b,"changeValid":b,"changeInvalidMessage":b,"changeRequired":b},members:{setEnabled:function(c){return arguments.length==1;
},getEnabled:function(){},setRequired:function(d){return arguments.length==1;
},getRequired:function(){},setValid:function(e){return arguments.length==1;
},getValid:function(){},setInvalidMessage:function(f){return arguments.length==1;
},getInvalidMessage:function(){},setRequiredInvalidMessage:function(g){return arguments.length==1;
},getRequiredInvalidMessage:function(){}}});
})();
(function(){var a="qx.application.Standalone";
qx.Class.define(a,{extend:qx.application.AbstractGui,members:{_createRootWidget:function(){return new qx.ui.root.Application(document);
}}});
})();
(function(){var i="qx.ui.window.Window",h="changeModal",g="changeVisibility",f="changeActive",d="_applyActiveWindow",c="__eI",b="__jT",a="qx.ui.window.MDesktop";
qx.Mixin.define(a,{properties:{activeWindow:{check:i,apply:d,init:null,nullable:true}},members:{__jT:null,__eI:null,getWindowManager:function(){if(!this.__eI){this.setWindowManager(new qx.ui.window.Window.DEFAULT_MANAGER_CLASS());
}return this.__eI;
},supportsMaximize:function(){return true;
},setWindowManager:function(j){if(this.__eI){this.__eI.setDesktop(null);
}j.setDesktop(this);
this.__eI=j;
},_onChangeActive:function(e){if(e.getData()){this.setActiveWindow(e.getTarget());
}else if(this.getActiveWindow()==e.getTarget()){this.setActiveWindow(null);
}},_applyActiveWindow:function(k,l){this.getWindowManager().changeActiveWindow(k,l);
this.getWindowManager().updateStack();
},_onChangeModal:function(e){this.getWindowManager().updateStack();
},_onChangeVisibility:function(){this.getWindowManager().updateStack();
},_afterAddChild:function(m){if(qx.Class.isDefined(i)&&m instanceof qx.ui.window.Window){this._addWindow(m);
}},_addWindow:function(n){if(!qx.lang.Array.contains(this.getWindows(),n)){this.getWindows().push(n);
n.addListener(f,this._onChangeActive,this);
n.addListener(h,this._onChangeModal,this);
n.addListener(g,this._onChangeVisibility,this);
}
if(n.getActive()){this.setActiveWindow(n);
}this.getWindowManager().updateStack();
},_afterRemoveChild:function(o){if(qx.Class.isDefined(i)&&o instanceof qx.ui.window.Window){this._removeWindow(o);
}},_removeWindow:function(p){qx.lang.Array.remove(this.getWindows(),p);
p.removeListener(f,this._onChangeActive,this);
p.removeListener(h,this._onChangeModal,this);
p.removeListener(g,this._onChangeVisibility,this);
this.getWindowManager().updateStack();
},getWindows:function(){if(!this.__jT){this.__jT=[];
}return this.__jT;
}},destruct:function(){this._disposeArray(b);
this._disposeObjects(c);
}});
})();
(function(){var f="__jU",e="_applyBlockerColor",d="Number",c="qx.ui.core.MBlocker",b="_applyBlockerOpacity",a="Color";
qx.Mixin.define(c,{construct:function(){this.__jU=this._createBlocker();
},properties:{blockerColor:{check:a,init:null,nullable:true,apply:e,themeable:true},blockerOpacity:{check:d,init:1,apply:b,themeable:true}},members:{__jU:null,_createBlocker:function(){return new qx.ui.core.Blocker(this);
},_applyBlockerColor:function(g,h){this.__jU.setColor(g);
},_applyBlockerOpacity:function(i,j){this.__jU.setOpacity(i);
},block:function(){this.__jU.block();
},isBlocked:function(){return this.__jU.isBlocked();
},unblock:function(){this.__jU.unblock();
},forceUnblock:function(){this.__jU.forceUnblock();
},blockContent:function(k){this.__jU.blockContent(k);
},isContentBlocked:function(){return this.__jU.isContentBlocked();
},unblockContent:function(){this.__jU.unblockContent();
},forceUnblockContent:function(){this.__jU.forceUnblockContent();
},getBlocker:function(){return this.__jU;
}},destruct:function(){this._disposeObjects(f);
}});
})();
(function(){var l="zIndex",k="px",j="keydown",h="deactivate",g="resize",f="keyup",d="keypress",c="backgroundColor",b="_applyOpacity",a="Boolean",x="__jU",w="opacity",v="interval",u="Tab",t="Color",s="qx.ui.root.Page",r="__ka",q="Number",p="qx.ui.core.Blocker",o="__je",m="qx.ui.root.Application",n="_applyColor";
qx.Class.define(p,{extend:qx.core.Object,construct:function(y){qx.core.Object.call(this);
this._widget=y;
this._isPageRoot=(qx.Class.isDefined(s)&&y instanceof qx.ui.root.Page);

if(this._isPageRoot){y.addListener(g,this.__kc,this);
}
if(qx.Class.isDefined(m)&&y instanceof qx.ui.root.Application){this.setKeepBlockerActive(true);
}this.__jV=[];
this.__jW=[];
this.__jX=[];
},properties:{color:{check:t,init:null,nullable:true,apply:n,themeable:true},opacity:{check:q,init:1,apply:b,themeable:true},keepBlockerActive:{check:a,init:false}},members:{__jU:null,__jY:0,__ka:null,__jX:null,__jV:null,__jW:null,__kb:null,__je:null,_isPageRoot:false,_widget:null,__kc:function(e){var z=e.getData();

if(this.isContentBlocked()){this.getContentBlockerElement().setStyles({width:z.width,height:z.height});
}
if(this.isBlocked()){this.getBlockerElement().setStyles({width:z.width,height:z.height});
}},_applyColor:function(A,B){var C=qx.theme.manager.Color.getInstance().resolve(A);
this.__kd(c,C);
},_applyOpacity:function(D,E){this.__kd(w,D);
},__kd:function(F,G){var H=[];
this.__jU&&H.push(this.__jU);
this.__ka&&H.push(this.__ka);

for(var i=0;i<H.length;i++){H[i].setStyle(F,G);
}},_backupActiveWidget:function(){var I=qx.event.Registration.getManager(window).getHandler(qx.event.handler.Focus);
this.__jV.push(I.getActive());
this.__jW.push(I.getFocus());

if(this._widget.isFocusable()){this._widget.focus();
}},_restoreActiveWidget:function(){var L=this.__jV.length;

if(L>0){var K=this.__jV[L-1];

if(K){qx.bom.Element.activate(K);
}this.__jV.pop();
}var J=this.__jW.length;

if(J>0){var K=this.__jW[J-1];

if(K){qx.bom.Element.focus(this.__jW[J-1]);
}this.__jW.pop();
}},__ke:function(){return new qx.html.Blocker(this.getColor(),this.getOpacity());
},getBlockerElement:function(){if(!this.__jU){this.__jU=this.__ke();
this.__jU.setStyle(l,15);
this._widget.getContainerElement().add(this.__jU);
this.__jU.exclude();
}return this.__jU;
},block:function(){this.__jY++;

if(this.__jY<2){this._backupActiveWidget();
var M=this.getBlockerElement();
M.include();
M.activate();
M.addListener(h,this.__kj,this);
M.addListener(d,this.__ki,this);
M.addListener(j,this.__ki,this);
M.addListener(f,this.__ki,this);
}},isBlocked:function(){return this.__jY>0;
},unblock:function(){if(!this.isBlocked()){return;
}this.__jY--;

if(this.__jY<1){this.__kf();
this.__jY=0;
}},forceUnblock:function(){if(!this.isBlocked()){return;
}this.__jY=0;
this.__kf();
},__kf:function(){this._restoreActiveWidget();
var N=this.getBlockerElement();
N.removeListener(h,this.__kj,this);
N.removeListener(d,this.__ki,this);
N.removeListener(j,this.__ki,this);
N.removeListener(f,this.__ki,this);
N.exclude();
},getContentBlockerElement:function(){if(!this.__ka){this.__ka=this.__ke();
this._widget.getContentElement().add(this.__ka);
this.__ka.exclude();
}return this.__ka;
},blockContent:function(O){var P=this.getContentBlockerElement();
P.setStyle(l,O);
this.__jX.push(O);

if(this.__jX.length<2){P.include();

if(this._isPageRoot){if(!this.__je){this.__je=new qx.event.Timer(300);
this.__je.addListener(v,this.__kh,this);
}this.__je.start();
this.__kh();
}}},isContentBlocked:function(){return this.__jX.length>0;
},unblockContent:function(){if(!this.isContentBlocked()){return;
}this.__jX.pop();
var Q=this.__jX[this.__jX.length-1];
var R=this.getContentBlockerElement();
R.setStyle(l,Q);

if(this.__jX.length<1){this.__kg();
this.__jX=[];
}},forceUnblockContent:function(){if(!this.isContentBlocked()){return;
}this.__jX=[];
var S=this.getContentBlockerElement();
S.setStyle(l,null);
this.__kg();
},__kg:function(){this.getContentBlockerElement().exclude();

if(this._isPageRoot){this.__je.stop();
}},__kh:function(){var T=this._widget.getContainerElement().getDomElement();
var U=qx.dom.Node.getDocument(T);
this.getContentBlockerElement().setStyles({height:U.documentElement.scrollHeight+k,width:U.documentElement.scrollWidth+k});
},__ki:function(e){if(e.getKeyIdentifier()==u){e.stop();
}},__kj:function(){if(this.getKeepBlockerActive()){this.getBlockerElement().activate();
}}},destruct:function(){if(this._isPageRoot){this._widget.removeListener(g,this.__kc,this);
}this._disposeObjects(r,x,o);
this.__kb=this.__jV=this.__jW=this._widget=this.__jX=null;
}});
})();
(function(){var t="engine.name",s="help",r="contextmenu",q="changeGlobalCursor",p="keypress",o="Boolean",n="root",m="",l=" !important",k="input",d="_applyGlobalCursor",j="Space",h="_applyNativeHelp",c=";",b="qx.ui.root.Abstract",g="abstract",f="textarea",i="String",a="*";
qx.Class.define(b,{type:g,extend:qx.ui.core.Widget,include:[qx.ui.core.MChildrenHandling,qx.ui.core.MBlocker,qx.ui.window.MDesktop],construct:function(){qx.ui.core.Widget.call(this);
qx.ui.core.FocusHandler.getInstance().addRoot(this);
qx.ui.core.queue.Visibility.add(this);
this.initNativeHelp();
this.addListener(p,this.__kl,this);
},properties:{appearance:{refine:true,init:n},enabled:{refine:true,init:true},focusable:{refine:true,init:true},globalCursor:{check:i,nullable:true,themeable:true,apply:d,event:q},nativeContextMenu:{refine:true,init:false},nativeHelp:{check:o,init:false,apply:h}},members:{__kk:null,isRootWidget:function(){return true;
},getLayout:function(){return this._getLayout();
},_applyGlobalCursor:qx.core.Environment.select(t,{"mshtml":function(u,v){},"default":function(w,x){var y=qx.bom.Stylesheet;
var z=this.__kk;

if(!z){this.__kk=z=y.createElement();
}y.removeAllRules(z);

if(w){y.addRule(z,a,qx.bom.element.Cursor.compile(w).replace(c,m)+l);
}}}),_applyNativeContextMenu:function(A,B){if(A){this.removeListener(r,this._onNativeContextMenu,this,true);
}else{this.addListener(r,this._onNativeContextMenu,this,true);
}},_onNativeContextMenu:function(e){if(e.getTarget().getNativeContextMenu()){return;
}e.preventDefault();
},__kl:function(e){if(e.getKeyIdentifier()!==j){return;
}var D=e.getTarget();
var C=qx.ui.core.FocusHandler.getInstance();

if(!C.isFocused(D)){return;
}var E=D.getContentElement().getNodeName();

if(E===k||E===f){return;
}e.preventDefault();
},_applyNativeHelp:qx.core.Environment.select(t,{"mshtml":function(F,G){if(G===false){qx.bom.Event.removeNativeListener(document,s,qx.lang.Function.returnFalse);
}
if(F===false){qx.bom.Event.addNativeListener(document,s,qx.lang.Function.returnFalse);
}},"default":function(){}})},destruct:function(){this.__kk=null;
},defer:function(H,I){qx.ui.core.MChildrenHandling.remap(I);
}});
})();
(function(){var k="keypress",j="focusout",h="activate",g="Tab",f="singleton",d="deactivate",c="__km",b="focusin",a="qx.ui.core.FocusHandler";
qx.Class.define(a,{extend:qx.core.Object,type:f,construct:function(){qx.core.Object.call(this);
this.__km={};
},members:{__km:null,__kn:null,__ko:null,__kp:null,connectTo:function(m){m.addListener(k,this.__gq,this);
m.addListener(b,this._onFocusIn,this,true);
m.addListener(j,this._onFocusOut,this,true);
m.addListener(h,this._onActivate,this,true);
m.addListener(d,this._onDeactivate,this,true);
},addRoot:function(n){this.__km[n.$$hash]=n;
},removeRoot:function(o){delete this.__km[o.$$hash];
},getActiveWidget:function(){return this.__kn;
},isActive:function(p){return this.__kn==p;
},getFocusedWidget:function(){return this.__ko;
},isFocused:function(q){return this.__ko==q;
},isFocusRoot:function(r){return !!this.__km[r.$$hash];
},_onActivate:function(e){var t=e.getTarget();
this.__kn=t;
var s=this.__kq(t);

if(s!=this.__kp){this.__kp=s;
}},_onDeactivate:function(e){var u=e.getTarget();

if(this.__kn==u){this.__kn=null;
}},_onFocusIn:function(e){var v=e.getTarget();

if(v!=this.__ko){this.__ko=v;
v.visualizeFocus();
}},_onFocusOut:function(e){var w=e.getTarget();

if(w==this.__ko){this.__ko=null;
w.visualizeBlur();
}},__gq:function(e){if(e.getKeyIdentifier()!=g){return;
}
if(!this.__kp){return;
}e.stopPropagation();
e.preventDefault();
var x=this.__ko;

if(!e.isShiftPressed()){var y=x?this.__ku(x):this.__ks();
}else{var y=x?this.__kv(x):this.__kt();
}if(y){y.tabFocus();
}},__kq:function(z){var A=this.__km;

while(z){if(A[z.$$hash]){return z;
}z=z.getLayoutParent();
}return null;
},__kr:function(B,C){if(B===C){return 0;
}var E=B.getTabIndex()||0;
var D=C.getTabIndex()||0;

if(E!=D){return E-D;
}var J=B.getContainerElement().getDomElement();
var I=C.getContainerElement().getDomElement();
var H=qx.bom.element.Location;
var G=H.get(J);
var F=H.get(I);
if(G.top!=F.top){return G.top-F.top;
}if(G.left!=F.left){return G.left-F.left;
}var K=B.getZIndex();
var L=C.getZIndex();

if(K!=L){return K-L;
}return 0;
},__ks:function(){return this.__ky(this.__kp,null);
},__kt:function(){return this.__kz(this.__kp,null);
},__ku:function(M){var N=this.__kp;

if(N==M){return this.__ks();
}
while(M&&M.getAnonymous()){M=M.getLayoutParent();
}
if(M==null){return [];
}var O=[];
this.__kw(N,M,O);
O.sort(this.__kr);
var P=O.length;
return P>0?O[0]:this.__ks();
},__kv:function(Q){var R=this.__kp;

if(R==Q){return this.__kt();
}
while(Q&&Q.getAnonymous()){Q=Q.getLayoutParent();
}
if(Q==null){return [];
}var S=[];
this.__kx(R,Q,S);
S.sort(this.__kr);
var T=S.length;
return T>0?S[T-1]:this.__kt();
},__kw:function(parent,U,V){var W=parent.getLayoutChildren();
var X;

for(var i=0,l=W.length;i<l;i++){X=W[i];
if(!(X instanceof qx.ui.core.Widget)){continue;
}
if(!this.isFocusRoot(X)&&X.isEnabled()&&X.isVisible()){if(X.isTabable()&&this.__kr(U,X)<0){V.push(X);
}this.__kw(X,U,V);
}}},__kx:function(parent,Y,ba){var bb=parent.getLayoutChildren();
var bc;

for(var i=0,l=bb.length;i<l;i++){bc=bb[i];
if(!(bc instanceof qx.ui.core.Widget)){continue;
}
if(!this.isFocusRoot(bc)&&bc.isEnabled()&&bc.isVisible()){if(bc.isTabable()&&this.__kr(Y,bc)>0){ba.push(bc);
}this.__kx(bc,Y,ba);
}}},__ky:function(parent,bd){var be=parent.getLayoutChildren();
var bf;

for(var i=0,l=be.length;i<l;i++){bf=be[i];
if(!(bf instanceof qx.ui.core.Widget)){continue;
}if(!this.isFocusRoot(bf)&&bf.isEnabled()&&bf.isVisible()){if(bf.isTabable()){if(bd==null||this.__kr(bf,bd)<0){bd=bf;
}}bd=this.__ky(bf,bd);
}}return bd;
},__kz:function(parent,bg){var bh=parent.getLayoutChildren();
var bi;

for(var i=0,l=bh.length;i<l;i++){bi=bh[i];
if(!(bi instanceof qx.ui.core.Widget)){continue;
}if(!this.isFocusRoot(bi)&&bi.isEnabled()&&bi.isVisible()){if(bi.isTabable()){if(bg==null||this.__kr(bi,bg)>0){bg=bi;
}}bg=this.__kz(bi,bg);
}}return bg;
}},destruct:function(){this._disposeMap(c);
this.__ko=this.__kn=this.__kp=null;
}});
})();
(function(){var n="resize",m="engine.name",l="position",k="0px",j="webkit",i="paddingLeft",h="$$widget",g="qx.ui.root.Application",f="hidden",d="div",a="paddingTop",c="100%",b="absolute";
qx.Class.define(g,{extend:qx.ui.root.Abstract,construct:function(o){this.__cf=qx.dom.Node.getWindow(o);
this.__kA=o;
qx.ui.root.Abstract.call(this);
qx.event.Registration.addListener(this.__cf,n,this._onResize,this);
this._setLayout(new qx.ui.layout.Canvas());
qx.ui.core.queue.Layout.add(this);
qx.ui.core.FocusHandler.getInstance().connectTo(this);
this.getContentElement().disableScrolling();
},members:{__cf:null,__kA:null,_createContainerElement:function(){var p=this.__kA;
if((qx.core.Environment.get(m)==j)){if(!p.body){alert("The application could not be started due to a missing body tag in the HTML file!");
}}var t=p.documentElement.style;
var q=p.body.style;
t.overflow=q.overflow=f;
t.padding=t.margin=q.padding=q.margin=k;
t.width=t.height=q.width=q.height=c;
var s=p.createElement(d);
p.body.appendChild(s);
var r=new qx.html.Root(s);
r.setStyle(l,b);
r.setAttribute(h,this.toHashCode());
return r;
},_onResize:function(e){qx.ui.core.queue.Layout.add(this);
},_computeSizeHint:function(){var u=qx.bom.Viewport.getWidth(this.__cf);
var v=qx.bom.Viewport.getHeight(this.__cf);
return {minWidth:u,width:u,maxWidth:u,minHeight:v,height:v,maxHeight:v};
},_applyPadding:function(w,x,name){if(w&&(name==a||name==i)){throw new Error("The root widget does not support 'left', or 'top' paddings!");
}qx.ui.root.Abstract.prototype._applyPadding.call(this,w,x,name);
},_applyDecorator:function(y,z){qx.ui.root.Abstract.prototype._applyDecorator.call(this,y,z);

if(!y){return;
}var A=this.getDecoratorElement().getInsets();

if(A.left||A.top){throw new Error("The root widget does not support decorators with 'left', or 'top' insets!");
}}},destruct:function(){this.__cf=this.__kA=null;
}});
})();
(function(){var b="number",a="qx.ui.layout.Canvas";
qx.Class.define(a,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(c,d){var q=this._getLayoutChildren();
var g,p,n;
var s,top,e,f,j,h;
var o,m,r,k;

for(var i=0,l=q.length;i<l;i++){g=q[i];
p=g.getSizeHint();
n=g.getLayoutProperties();
o=g.getMarginTop();
m=g.getMarginRight();
r=g.getMarginBottom();
k=g.getMarginLeft();
s=n.left!=null?n.left:n.edge;

if(qx.lang.Type.isString(s)){s=Math.round(parseFloat(s)*c/100);
}e=n.right!=null?n.right:n.edge;

if(qx.lang.Type.isString(e)){e=Math.round(parseFloat(e)*c/100);
}top=n.top!=null?n.top:n.edge;

if(qx.lang.Type.isString(top)){top=Math.round(parseFloat(top)*d/100);
}f=n.bottom!=null?n.bottom:n.edge;

if(qx.lang.Type.isString(f)){f=Math.round(parseFloat(f)*d/100);
}if(s!=null&&e!=null){j=c-s-e-k-m;
if(j<p.minWidth){j=p.minWidth;
}else if(j>p.maxWidth){j=p.maxWidth;
}s+=k;
}else{j=n.width;

if(j==null){j=p.width;
}else{j=Math.round(parseFloat(j)*c/100);
if(j<p.minWidth){j=p.minWidth;
}else if(j>p.maxWidth){j=p.maxWidth;
}}
if(e!=null){s=c-j-e-m-k;
}else if(s==null){s=k;
}else{s+=k;
}}if(top!=null&&f!=null){h=d-top-f-o-r;
if(h<p.minHeight){h=p.minHeight;
}else if(h>p.maxHeight){h=p.maxHeight;
}top+=o;
}else{h=n.height;

if(h==null){h=p.height;
}else{h=Math.round(parseFloat(h)*d/100);
if(h<p.minHeight){h=p.minHeight;
}else if(h>p.maxHeight){h=p.maxHeight;
}}
if(f!=null){top=d-h-f-r-o;
}else if(top==null){top=o;
}else{top+=o;
}}g.renderLayout(s,top,j,h);
}},_computeSizeHint:function(){var I=0,H=0;
var F=0,D=0;
var B,A;
var z,x;
var t=this._getLayoutChildren();
var w,G,v;
var J,top,u,y;

for(var i=0,l=t.length;i<l;i++){w=t[i];
G=w.getLayoutProperties();
v=w.getSizeHint();
var E=w.getMarginLeft()+w.getMarginRight();
var C=w.getMarginTop()+w.getMarginBottom();
B=v.width+E;
A=v.minWidth+E;
J=G.left!=null?G.left:G.edge;

if(J&&typeof J===b){B+=J;
A+=J;
}u=G.right!=null?G.right:G.edge;

if(u&&typeof u===b){B+=u;
A+=u;
}I=Math.max(I,B);
H=Math.max(H,A);
z=v.height+C;
x=v.minHeight+C;
top=G.top!=null?G.top:G.edge;

if(top&&typeof top===b){z+=top;
x+=top;
}y=G.bottom!=null?G.bottom:G.edge;

if(y&&typeof y===b){z+=y;
x+=y;
}F=Math.max(F,z);
D=Math.max(D,x);
}return {width:I,minWidth:H,height:F,minHeight:D};
}}});
})();
(function(){var a="qx.html.Root";
qx.Class.define(a,{extend:qx.html.Element,construct:function(b){qx.html.Element.call(this);

if(b!=null){this.useElement(b);
}},members:{useElement:function(c){qx.html.Element.prototype.useElement.call(this,c);
this.setRoot(true);
qx.html.Element._modified[this.$$hash]=this;
}}});
})();
(function(){var k="cursor",j="100%",i="repeat",h="mousedown",g="url(",f=")",d="mouseout",c="div",b="dblclick",a="mousewheel",w="qx.html.Blocker",v="mousemove",u="mouseover",t="appear",s="click",r="mshtml",q="engine.name",p="mouseup",o="contextmenu",n="disappear",l="qx/static/blank.gif",m="absolute";
qx.Class.define(w,{extend:qx.html.Element,construct:function(x,y){var x=x?qx.theme.manager.Color.getInstance().resolve(x):null;
var z={position:m,width:j,height:j,opacity:y||0,backgroundColor:x};
if((qx.core.Environment.get(q)==r)){z.backgroundImage=g+qx.util.ResourceManager.getInstance().toUri(l)+f;
z.backgroundRepeat=i;
}qx.html.Element.call(this,c,z);
this.addListener(h,this._stopPropagation,this);
this.addListener(p,this._stopPropagation,this);
this.addListener(s,this._stopPropagation,this);
this.addListener(b,this._stopPropagation,this);
this.addListener(v,this._stopPropagation,this);
this.addListener(u,this._stopPropagation,this);
this.addListener(d,this._stopPropagation,this);
this.addListener(a,this._stopPropagation,this);
this.addListener(o,this._stopPropagation,this);
this.addListener(t,this.__kB,this);
this.addListener(n,this.__kB,this);
},members:{_stopPropagation:function(e){e.stopPropagation();
},__kB:function(){var A=this.getStyle(k);
this.setStyle(k,null,true);
this.setStyle(k,A,true);
}}});
})();
(function(){var q="execute",p='100%',o='Server Eintragen',n='84.201.4.47',m='Scoville Infrastructure',l='192.168.0.13',k="scoville_admin.Application",j='scoville_admin/scoville.png',h="First Button",g="scoville_admin/config_header.png",b="LOL BUTTON",d='Server',c="scoville_admin/test.png",a='192.168.0.104';
qx.Class.define(k,{extend:qx.application.Standalone,members:{loadServer:function(r,s,t,u){var w=this.tree.getRoot().getChildren();

for(var i=0;i<w.length;i++){if(r==w[i].ip){return 0;
}}
try{var v=new scoville_admin.Server(this,r,t,u);
this.tree.getRoot().add(v);
}catch(e){}return 1;
},main:function(){qx.application.Standalone.prototype.main.call(this);
this.mainpane=new qx.ui.splitpane.Pane();
this.vbox=new qx.ui.layout.VBox();
this.vcontainer=new qx.ui.container.Composite(this.vbox);
this.tabview=new qx.ui.tabview.TabView();
this.menu=new qx.ui.menubar.MenuBar();
this.button1=new qx.ui.form.Button(h,c);
this.button2=new qx.ui.form.Button(b);
this.testimg=new qx.ui.basic.Image(g);
this.tree=new qx.ui.tree.Tree();
var y=this.getRoot();
var x=new qx.ui.tree.TreeFolder(m);
x.setIcon(j);
this.treecontextmenu=new scoville_admin.TreeContextMenu(this);
this.tree.setContextMenu(this.treecontextmenu);
this.tree.setRoot(x);
this.men_server=new qx.ui.menu.Menu();
this.but_server=new qx.ui.menubar.Button(d,null,this.men_server);
this.but_server_register_new=new qx.ui.menu.Button(o);
this.men_server.add(this.but_server_register_new);
this.menu.add(this.but_server);
this.but_server_register_new.addListener(q,this.createNewServerCallback(this));
this.mainpane.add(this.tree);
this.mainpane.add(this.tabview);
this.vcontainer.add(this.testimg);
this.vcontainer.add(this.menu);
this.vcontainer.add(this.mainpane,{flex:1});
y.add(this.vcontainer,{width:p,height:p});
this.button1.addListener(q,function(e){alert("Hello World!");
});
this.loadServer(a);
this.loadServer(l);
this.loadServer(n);
},createNewServerCallback:function(z){var f=function(e){new scoville_admin.NewServerPage(z);
};
return f;
}}});
})();
(function(){var b="qx.ui.form.IModel",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"changeModel":a},members:{setModel:function(c){},getModel:function(){},resetModel:function(){}}});
})();
(function(){var b="changeModel",a="qx.ui.form.MModelProperty";
qx.Mixin.define(a,{properties:{model:{nullable:true,event:b,dereference:true}}});
})();
(function(){var k="open",j="icon",i="auto",h="middle",g="String",f="label",d="changeOpen",c="opened",b="always",a="_applyIconOpened",D="Boolean",C="changeIcon",B="changeIconOpened",A="changeLabel",z="__kE",y="Integer",x="_applyIndent",w="changeOpenSymbolMode",v="_applyOpenSymbolMode",u="resize",r="",s="iconOpened",p="abstract",q="never",n="_applyIcon",o="_applyOpen",l="changeIndent",m="qx.ui.tree.core.AbstractItem",t="_applyLabel";
qx.Class.define(m,{extend:qx.ui.core.Widget,type:p,include:[qx.ui.form.MModelProperty],implement:[qx.ui.form.IModel],construct:function(E){qx.ui.core.Widget.call(this);

if(E!=null){this.setLabel(E);
}this._setLayout(new qx.ui.layout.HBox());
this._addWidgets();
this.initOpen();
},properties:{open:{check:D,init:false,event:d,apply:o},openSymbolMode:{check:[b,q,i],init:i,event:w,apply:v},indent:{check:y,init:19,apply:x,event:l,themeable:true},icon:{check:g,apply:n,event:C,nullable:true,themeable:true},iconOpened:{check:g,apply:a,event:B,nullable:true,themeable:true},label:{check:g,apply:t,event:A,init:r}},members:{__kC:null,__kD:null,__kE:null,_addWidgets:function(){throw new Error("Abstract method call.");
},_createChildControlImpl:function(F,G){var H;

switch(F){case f:H=new qx.ui.basic.Label().set({alignY:h,anonymous:true,value:this.getLabel()});
break;
case j:H=new qx.ui.basic.Image().set({alignY:h,anonymous:true,source:this.getIcon()});
break;
case k:H=new qx.ui.tree.core.FolderOpenButton().set({alignY:h});
H.addListener(d,this._onChangeOpen,this);
H.addListener(u,this._updateIndent,this);
break;
}return H||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,F);
},addWidget:function(I,J){this._add(I,J);
},addSpacer:function(){if(!this.__kE){this.__kE=new qx.ui.core.Spacer();
}else{this._remove(this.__kE);
}this._add(this.__kE);
},addOpenButton:function(){this._add(this.getChildControl(k));
},_onChangeOpen:function(e){if(this.isOpenable()){this.setOpen(e.getData());
}},addIcon:function(){var K=this.getChildControl(j);

if(this.__kD){this._remove(K);
}this._add(K);
this.__kD=true;
},addLabel:function(L){var M=this.getChildControl(f);

if(this.__kC){this._remove(M);
}
if(L){this.setLabel(L);
}else{M.setValue(this.getLabel());
}this._add(M);
this.__kC=true;
},_applyIcon:function(N,O){if(!this.__kG()){this.__kH(N);
}else if(!this.isOpen()){this.__kH(N);
}},_applyIconOpened:function(P,Q){if(this.isOpen()){if(this.__kF()&&this.__kG()){this.__kH(P);
}else if(!this.__kF()&&this.__kG()){this.__kH(P);
}}},_applyLabel:function(R,S){var T=this.getChildControl(f,true);

if(T){T.setValue(R);
}},_applyOpen:function(U,V){var open=this.getChildControl(k,true);

if(open){open.setOpen(U);
}var W;
if(U){W=this.__kG()?this.getIconOpened():null;
}else{W=this.getIcon();
}
if(W){this.__kH(W);
}U?this.addState(c):this.removeState(c);
},__kF:function(){return qx.util.PropertyUtil.getUserValue(this,j);
},__kG:function(){return qx.util.PropertyUtil.getUserValue(this,s);
},__kH:function(X){var Y=this.getChildControl(j,true);

if(Y){Y.setSource(X);
}},isOpenable:function(){var ba=this.getOpenSymbolMode();
return (ba===b||ba===i&&this.hasChildren());
},_shouldShowOpenSymbol:function(){throw new Error("Abstract method call.");
},_applyOpenSymbolMode:function(bb,bc){this._updateIndent();
},_updateIndent:function(){var be=0;
var open=this.getChildControl(k,true);

if(open){if(this._shouldShowOpenSymbol()){open.show();
var bd=open.getBounds();

if(bd){be=bd.width;
}else{return;
}}else{open.exclude();
}}
if(this.__kE){this.__kE.setWidth((this.getLevel()+1)*this.getIndent()-be);
}},_applyIndent:function(bf,bg){this._updateIndent();
},getLevel:function(){throw new Error("Abstract method call.");
},syncWidget:function(){this._updateIndent();
},hasChildren:function(){throw new Error("Abstract method call.");
}},destruct:function(){this._disposeObjects(z);
}});
})();
(function(){var n="_applyLayoutChange",m="left",k="center",j="top",h="Decorator",g="middle",f="_applyReversed",e="bottom",d="Boolean",c="right",a="Integer",b="qx.ui.layout.HBox";
qx.Class.define(b,{extend:qx.ui.layout.Abstract,construct:function(o,p,q){qx.ui.layout.Abstract.call(this);

if(o){this.setSpacing(o);
}
if(p){this.setAlignX(p);
}
if(q){this.setSeparator(q);
}},properties:{alignX:{check:[m,k,c],init:m,apply:n},alignY:{check:[j,g,e],init:j,apply:n},spacing:{check:a,init:0,apply:n},separator:{check:h,nullable:true,apply:n},reversed:{check:d,init:false,apply:f}},members:{__kI:null,__kJ:null,__kK:null,__ff:null,_applyReversed:function(){this._invalidChildrenCache=true;
this._applyLayoutChange();
},__kL:function(){var w=this._getLayoutChildren();
var length=w.length;
var t=false;
var r=this.__kI&&this.__kI.length!=length&&this.__kJ&&this.__kI;
var u;
var s=r?this.__kI:new Array(length);
var v=r?this.__kJ:new Array(length);
if(this.getReversed()){w=w.concat().reverse();
}for(var i=0;i<length;i++){u=w[i].getLayoutProperties();

if(u.width!=null){s[i]=parseFloat(u.width)/100;
}
if(u.flex!=null){v[i]=u.flex;
t=true;
}else{v[i]=0;
}}if(!r){this.__kI=s;
this.__kJ=v;
}this.__kK=t;
this.__ff=w;
delete this._invalidChildrenCache;
},verifyLayoutProperty:null,renderLayout:function(x,y){if(this._invalidChildrenCache){this.__kL();
}var E=this.__ff;
var length=E.length;
var N=qx.ui.layout.Util;
var M=this.getSpacing();
var Q=this.getSeparator();

if(Q){var B=N.computeHorizontalSeparatorGaps(E,M,Q);
}else{var B=N.computeHorizontalGaps(E,M,true);
}var i,z,K,J;
var P=[];
var F=B;

for(i=0;i<length;i+=1){J=this.__kI[i];
K=J!=null?Math.floor((x-B)*J):E[i].getSizeHint().width;
P.push(K);
F+=K;
}if(this.__kK&&F!=x){var H={};
var L,O;

for(i=0;i<length;i+=1){L=this.__kJ[i];

if(L>0){G=E[i].getSizeHint();
H[i]={min:G.minWidth,value:P[i],max:G.maxWidth,flex:L};
}}var C=N.computeFlexOffsets(H,x,F);

for(i in C){O=C[i].offset;
P[i]+=O;
F+=O;
}}var U=E[0].getMarginLeft();
if(F<x&&this.getAlignX()!=m){U=x-F;

if(this.getAlignX()===k){U=Math.round(U/2);
}}var G,top,A,K,D,S,I;
var M=this.getSpacing();
this._clearSeparators();
if(Q){var R=qx.theme.manager.Decoration.getInstance().resolve(Q).getInsets();
var T=R.left+R.right;
}for(i=0;i<length;i+=1){z=E[i];
K=P[i];
G=z.getSizeHint();
S=z.getMarginTop();
I=z.getMarginBottom();
A=Math.max(G.minHeight,Math.min(y-S-I,G.maxHeight));
top=N.computeVerticalAlignOffset(z.getAlignY()||this.getAlignY(),A,y,S,I);
if(i>0){if(Q){U+=D+M;
this._renderSeparator(Q,{left:U,top:0,width:T,height:y});
U+=T+M+z.getMarginLeft();
}else{U+=N.collapseMargins(M,D,z.getMarginLeft());
}}z.renderLayout(U,top,K,A);
U+=K;
D=z.getMarginRight();
}},_computeSizeHint:function(){if(this._invalidChildrenCache){this.__kL();
}var bc=qx.ui.layout.Util;
var bk=this.__ff;
var V=0,bd=0,ba=0;
var Y=0,bb=0;
var bh,W,bj;
for(var i=0,l=bk.length;i<l;i+=1){bh=bk[i];
W=bh.getSizeHint();
bd+=W.width;
var bg=this.__kJ[i];
var X=this.__kI[i];

if(bg){V+=W.minWidth;
}else if(X){ba=Math.max(ba,Math.round(W.minWidth/X));
}else{V+=W.width;
}bj=bh.getMarginTop()+bh.getMarginBottom();
if((W.height+bj)>bb){bb=W.height+bj;
}if((W.minHeight+bj)>Y){Y=W.minHeight+bj;
}}V+=ba;
var bf=this.getSpacing();
var bi=this.getSeparator();

if(bi){var be=bc.computeHorizontalSeparatorGaps(bk,bf,bi);
}else{var be=bc.computeHorizontalGaps(bk,bf,true);
}return {minWidth:V+be,width:bd+be,minHeight:Y,height:bb};
}},destruct:function(){this.__kI=this.__kJ=this.__ff=null;
}});
})();
(function(){var n="execute",m="toolTipText",l="icon",k="label",j="qx.ui.core.MExecutable",h="value",g="qx.event.type.Event",f="_applyCommand",d="enabled",c="menu",a="changeCommand",b="qx.ui.core.Command";
qx.Mixin.define(j,{events:{"execute":g},properties:{command:{check:b,apply:f,event:a,nullable:true}},members:{__kM:null,__kN:false,__kO:null,_bindableProperties:[d,k,l,m,h,c],execute:function(){var o=this.getCommand();

if(o){if(this.__kN){this.__kN=false;
}else{this.__kN=true;
o.execute(this);
}}this.fireEvent(n);
},__kP:function(e){if(this.__kN){this.__kN=false;
return;
}this.__kN=true;
this.execute();
},_applyCommand:function(p,q){if(q!=null){q.removeListenerById(this.__kO);
}
if(p!=null){this.__kO=p.addListener(n,this.__kP,this);
}var t=this.__kM;

if(t==null){this.__kM=t={};
}var u;

for(var i=0;i<this._bindableProperties.length;i++){var s=this._bindableProperties[i];
if(q!=null&&!q.isDisposed()&&t[s]!=null){q.removeBinding(t[s]);
t[s]=null;
}if(p!=null&&qx.Class.hasProperty(this.constructor,s)){var r=p.get(s);

if(r==null){u=this.get(s);
}else{u=null;
}t[s]=p.bind(s,this,s);
if(u){this.set(s,u);
}}}}},destruct:function(){this._applyCommand(null,this.getCommand());
this.__kM=null;
}});
})();
(function(){var i="opened",h="click",g="mousedown",f="Boolean",d="changeOpen",c="_applyOpen",b="mouseup",a="qx.ui.tree.core.FolderOpenButton";
qx.Class.define(a,{extend:qx.ui.basic.Image,include:qx.ui.core.MExecutable,construct:function(){qx.ui.basic.Image.call(this);
this.initOpen();
this.addListener(h,this._onClick);
this.addListener(g,this._stopPropagation,this);
this.addListener(b,this._stopPropagation,this);
},properties:{open:{check:f,init:false,event:d,apply:c}},members:{_applyOpen:function(j,k){j?this.addState(i):this.removeState(i);
this.execute();
},_stopPropagation:function(e){e.stopPropagation();
},_onClick:function(e){this.toggleOpen();
e.stopPropagation();
}}});
})();
(function(){var a="qx.ui.core.Spacer";
qx.Class.define(a,{extend:qx.ui.core.LayoutItem,construct:function(b,c){qx.ui.core.LayoutItem.call(this);
this.setWidth(b!=null?b:0);
this.setHeight(c!=null?c:0);
},members:{checkAppearanceNeeds:function(){},addChildrenToQueue:function(d){},destroy:function(){if(this.$$disposed){return;
}var parent=this.$$parent;

if(parent){parent._remove(this);
}qx.ui.core.queue.Dispose.add(this);
}}});
})();
(function(){var d="$$theme_",c="$$user_",b="$$init_",a="qx.util.PropertyUtil";
qx.Class.define(a,{statics:{getProperties:function(e){return e.$$properties;
},getAllProperties:function(f){var i={};
var j=f;
while(j!=qx.core.Object){var h=this.getProperties(j);

for(var g in h){i[g]=h[g];
}j=j.superclass;
}return i;
},getUserValue:function(k,l){return k[c+l];
},setUserValue:function(m,n,o){m[c+n]=o;
},deleteUserValue:function(p,q){delete (p[c+q]);
},getInitValue:function(r,s){return r[b+s];
},setInitValue:function(t,u,v){t[b+u]=v;
},deleteInitValue:function(w,x){delete (w[b+x]);
},getThemeValue:function(y,z){return y[d+z];
},setThemeValue:function(A,B,C){A[d+B]=C;
},deleteThemeValue:function(D,E){delete (D[d+E]);
},setThemed:function(F,G,H){var I=qx.core.Property.$$method.setThemed;
F[I[G]](H);
},resetThemed:function(J,K){var L=qx.core.Property.$$method.resetThemed;
J[L[K]]();
}}});
})();
(function(){var j="visible",h="excluded",g="qx.ui.tree.core.AbstractTreeItem",f="open",e="abstract",d="addItem",c="removeItem",b="__kQ",a="__ff";
qx.Class.define(g,{extend:qx.ui.tree.core.AbstractItem,type:e,construct:function(k){qx.ui.tree.core.AbstractItem.call(this,k);
this.__ff=[];
},properties:{parent:{check:g,nullable:true}},members:{__ff:null,__kQ:null,getTree:function(){var n=this;

while(n.getParent()){n=n.getParent();
}var m=n.getLayoutParent()?n.getLayoutParent().getLayoutParent():0;

if(m&&m instanceof qx.ui.core.scroll.ScrollPane){return m.getLayoutParent();
}return null;
},_applyOpen:function(o,p){if(this.hasChildren()){this.getChildrenContainer().setVisibility(o?j:h);
}qx.ui.tree.core.AbstractItem.prototype._applyOpen.call(this,o,p);
},_shouldShowOpenSymbol:function(){var open=this.getChildControl(f,true);

if(!open){return false;
}var q=this.getTree();

if(!q.getRootOpenClose()){if(q.getHideRoot()){if(q.getRoot()==this.getParent()){return false;
}}else{if(q.getRoot()==this){return false;
}}}return this.isOpenable();
},_updateIndent:function(){if(!this.getTree()){return;
}qx.ui.tree.core.AbstractItem.prototype._updateIndent.call(this);
},getLevel:function(){var r=this.getTree();

if(!r){return;
}var s=this;
var t=-1;

while(s){s=s.getParent();
t+=1;
}if(r.getHideRoot()){t-=1;
}
if(!r.getRootOpenClose()){t-=1;
}return t;
},addState:function(u){qx.ui.tree.core.AbstractItem.prototype.addState.call(this,u);
var w=this._getChildren();

for(var i=0,l=w.length;i<l;i++){var v=w[i];

if(v.addState){w[i].addState(u);
}}},removeState:function(x){qx.ui.tree.core.AbstractItem.prototype.removeState.call(this,x);
var z=this._getChildren();

for(var i=0,l=z.length;i<l;i++){var y=z[i];

if(y.removeState){z[i].removeState(x);
}}},getChildrenContainer:function(){if(!this.__kQ){this.__kQ=new qx.ui.container.Composite(new qx.ui.layout.VBox()).set({visibility:this.isOpen()?j:h});
}return this.__kQ;
},hasChildrenContainer:function(){return this.__kQ;
},getParentChildrenContainer:function(){if(this.getParent()){return this.getParent().getChildrenContainer();
}else if(this.getLayoutParent()){return this.getLayoutParent();
}else{return null;
}},getChildren:function(){return this.__ff;
},hasChildren:function(){return this.__ff?this.__ff.length>0:false;
},getItems:function(A,B,C){if(C!==false){var D=[];
}else{var D=[this];
}var G=this.hasChildren()&&(B!==false||this.isOpen());

if(G){var F=this.getChildren();

if(A===false){D=D.concat(F);
}else{for(var i=0,E=F.length;i<E;i++){D=D.concat(F[i].getItems(A,B,false));
}}}return D;
},recursiveAddToWidgetQueue:function(){var H=this.getItems(true,true,false);

for(var i=0,l=H.length;i<l;i++){qx.ui.core.queue.Widget.add(H[i]);
}},__kR:function(){if(this.getParentChildrenContainer()){this.getParentChildrenContainer()._addAfter(this.getChildrenContainer(),this);
}},add:function(I){var J=this.getChildrenContainer();
var M=this.getTree();

for(var i=0,l=arguments.length;i<l;i++){var N=arguments[i];
var L=N.getParent();

if(L){L.remove(N);
}N.setParent(this);
var K=this.hasChildren();
J.add(N);

if(N.hasChildren()){J.add(N.getChildrenContainer());
}this.__ff.push(N);

if(!K){this.__kR();
}
if(M){N.recursiveAddToWidgetQueue();
M.fireNonBubblingEvent(d,qx.event.type.Data,[N]);
}}
if(M){qx.ui.core.queue.Widget.add(this);
}},addAt:function(O,P){if(P==this.__ff.length){this.add(O);
return;
}var T=O.getParent();

if(T){T.remove(O);
}var R=this.getChildrenContainer();
O.setParent(this);
var S=this.hasChildren();
var Q=this.__ff[P];
R.addBefore(O,Q);

if(O.hasChildren()){R.addAfter(O.getChildrenContainer(),O);
}qx.lang.Array.insertAt(this.__ff,O,P);

if(!S){this.__kR();
}
if(this.getTree()){O.recursiveAddToWidgetQueue();
qx.ui.core.queue.Widget.add(this);
}},addBefore:function(U,V){var W=U.getParent();

if(W){W.remove(U);
}this.addAt(U,this.__ff.indexOf(V));
},addAfter:function(X,Y){var ba=X.getParent();

if(ba){ba.remove(X);
}this.addAt(X,this.__ff.indexOf(Y)+1);
},addAtBegin:function(bb){this.addAt(bb,0);
},remove:function(bc){for(var i=0,l=arguments.length;i<l;i++){var bg=arguments[i];

if(this.__ff.indexOf(bg)==-1){this.warn("Cannot remove treeitem '"+bg+"'. It is not a child of this tree item.");
return;
}var bd=this.getChildrenContainer();

if(bg.hasChildrenContainer()){var bf=bg.getChildrenContainer();

if(bd.getChildren().indexOf(bf)>=0){bd.remove(bf);
}}qx.lang.Array.remove(this.__ff,bg);
bg.setParent(null);
bd.remove(bg);
}var be=this.getTree();

if(be){be.fireNonBubblingEvent(c,qx.event.type.Data,[bg]);
}qx.ui.core.queue.Widget.add(this);
},removeAt:function(bh){var bi=this.__ff[bh];

if(bi){this.remove(bi);
}},removeAll:function(){var bj=this.__ff.concat();

for(var i=this.__ff.length-1;i>=0;i--){this.remove(this.__ff[i]);
}return bj;
}},destruct:function(){this._disposeArray(a);
this._disposeObjects(b);
}});
})();
(function(){var m="resize",l="scrollY",k="update",j="scrollX",i="_applyScrollX",h="_applyScrollY",g="qx.lang.Type.isNumber(value)&&value>=0&&value<=this.getScrollMaxX()",f="appear",d="qx.lang.Type.isNumber(value)&&value>=0&&value<=this.getScrollMaxY()",c="qx.event.type.Event",a="qx.ui.core.scroll.ScrollPane",b="scroll";
qx.Class.define(a,{extend:qx.ui.core.Widget,construct:function(){qx.ui.core.Widget.call(this);
this.set({minWidth:0,minHeight:0});
this._setLayout(new qx.ui.layout.Grow());
this.addListener(m,this._onUpdate);
var n=this.getContentElement();
n.addListener(b,this._onScroll,this);
n.addListener(f,this._onAppear,this);
},events:{update:c},properties:{scrollX:{check:g,apply:i,event:j,init:0},scrollY:{check:d,apply:h,event:l,init:0}},members:{add:function(o){var p=this._getChildren()[0];

if(p){this._remove(p);
p.removeListener(m,this._onUpdate,this);
}
if(o){this._add(o);
o.addListener(m,this._onUpdate,this);
}},remove:function(q){if(q){this._remove(q);
q.removeListener(m,this._onUpdate,this);
}},getChildren:function(){return this._getChildren();
},_onUpdate:function(e){this.fireEvent(k);
},_onScroll:function(e){var r=this.getContentElement();
this.setScrollX(r.getScrollX());
this.setScrollY(r.getScrollY());
},_onAppear:function(e){var v=this.getContentElement();
var s=this.getScrollX();
var t=v.getScrollX();

if(s!=t){v.scrollToX(s);
}var w=this.getScrollY();
var u=v.getScrollY();

if(w!=u){v.scrollToY(w);
}},getItemTop:function(z){var top=0;

do{top+=z.getBounds().top;
z=z.getLayoutParent();
}while(z&&z!==this);
return top;
},getItemBottom:function(A){return this.getItemTop(A)+A.getBounds().height;
},getItemLeft:function(B){var C=0;
var parent;

do{C+=B.getBounds().left;
parent=B.getLayoutParent();

if(parent){C+=parent.getInsets().left;
}B=parent;
}while(B&&B!==this);
return C;
},getItemRight:function(D){return this.getItemLeft(D)+D.getBounds().width;
},getScrollSize:function(){return this.getChildren()[0].getBounds();
},getScrollMaxX:function(){var F=this.getInnerSize();
var E=this.getScrollSize();

if(F&&E){return Math.max(0,E.width-F.width);
}return 0;
},getScrollMaxY:function(){var H=this.getInnerSize();
var G=this.getScrollSize();

if(H&&G){return Math.max(0,G.height-H.height);
}return 0;
},scrollToX:function(I){var J=this.getScrollMaxX();

if(I<0){I=0;
}else if(I>J){I=J;
}this.setScrollX(I);
},scrollToY:function(K){var L=this.getScrollMaxY();

if(K<0){K=0;
}else if(K>L){K=L;
}this.setScrollY(K);
},scrollByX:function(x){this.scrollToX(this.getScrollX()+x);
},scrollByY:function(y){this.scrollToY(this.getScrollY()+y);
},_applyScrollX:function(M){this.getContentElement().scrollToX(M);
},_applyScrollY:function(N){this.getContentElement().scrollToY(N);
}}});
})();
(function(){var n="_applyLayoutChange",m="top",k="left",j="middle",h="Decorator",g="center",f="_applyReversed",e="bottom",d="qx.ui.layout.VBox",c="Integer",a="right",b="Boolean";
qx.Class.define(d,{extend:qx.ui.layout.Abstract,construct:function(o,p,q){qx.ui.layout.Abstract.call(this);

if(o){this.setSpacing(o);
}
if(p){this.setAlignY(p);
}
if(q){this.setSeparator(q);
}},properties:{alignY:{check:[m,j,e],init:m,apply:n},alignX:{check:[k,g,a],init:k,apply:n},spacing:{check:c,init:0,apply:n},separator:{check:h,nullable:true,apply:n},reversed:{check:b,init:false,apply:f}},members:{__kS:null,__kJ:null,__kK:null,__ff:null,_applyReversed:function(){this._invalidChildrenCache=true;
this._applyLayoutChange();
},__kL:function(){var w=this._getLayoutChildren();
var length=w.length;
var s=false;
var r=this.__kS&&this.__kS.length!=length&&this.__kJ&&this.__kS;
var u;
var t=r?this.__kS:new Array(length);
var v=r?this.__kJ:new Array(length);
if(this.getReversed()){w=w.concat().reverse();
}for(var i=0;i<length;i++){u=w[i].getLayoutProperties();

if(u.height!=null){t[i]=parseFloat(u.height)/100;
}
if(u.flex!=null){v[i]=u.flex;
s=true;
}else{v[i]=0;
}}if(!r){this.__kS=t;
this.__kJ=v;
}this.__kK=s;
this.__ff=w;
delete this._invalidChildrenCache;
},verifyLayoutProperty:null,renderLayout:function(x,y){if(this._invalidChildrenCache){this.__kL();
}var F=this.__ff;
var length=F.length;
var P=qx.ui.layout.Util;
var O=this.getSpacing();
var S=this.getSeparator();

if(S){var C=P.computeVerticalSeparatorGaps(F,O,S);
}else{var C=P.computeVerticalGaps(F,O,true);
}var i,A,B,J;
var K=[];
var Q=C;

for(i=0;i<length;i+=1){J=this.__kS[i];
B=J!=null?Math.floor((y-C)*J):F[i].getSizeHint().height;
K.push(B);
Q+=B;
}if(this.__kK&&Q!=y){var H={};
var N,R;

for(i=0;i<length;i+=1){N=this.__kJ[i];

if(N>0){G=F[i].getSizeHint();
H[i]={min:G.minHeight,value:K[i],max:G.maxHeight,flex:N};
}}var D=P.computeFlexOffsets(H,y,Q);

for(i in D){R=D[i].offset;
K[i]+=R;
Q+=R;
}}var top=F[0].getMarginTop();
if(Q<y&&this.getAlignY()!=m){top=y-Q;

if(this.getAlignY()===j){top=Math.round(top/2);
}}var G,U,L,B,I,M,E;
this._clearSeparators();
if(S){var T=qx.theme.manager.Decoration.getInstance().resolve(S).getInsets();
var z=T.top+T.bottom;
}for(i=0;i<length;i+=1){A=F[i];
B=K[i];
G=A.getSizeHint();
M=A.getMarginLeft();
E=A.getMarginRight();
L=Math.max(G.minWidth,Math.min(x-M-E,G.maxWidth));
U=P.computeHorizontalAlignOffset(A.getAlignX()||this.getAlignX(),L,x,M,E);
if(i>0){if(S){top+=I+O;
this._renderSeparator(S,{top:top,left:0,height:z,width:x});
top+=z+O+A.getMarginTop();
}else{top+=P.collapseMargins(O,I,A.getMarginTop());
}}A.renderLayout(U,top,L,B);
top+=B;
I=A.getMarginBottom();
}},_computeSizeHint:function(){if(this._invalidChildrenCache){this.__kL();
}var bc=qx.ui.layout.Util;
var bk=this.__ff;
var X=0,bb=0,ba=0;
var V=0,bd=0;
var bh,W,bj;
for(var i=0,l=bk.length;i<l;i+=1){bh=bk[i];
W=bh.getSizeHint();
bb+=W.height;
var bg=this.__kJ[i];
var Y=this.__kS[i];

if(bg){X+=W.minHeight;
}else if(Y){ba=Math.max(ba,Math.round(W.minHeight/Y));
}else{X+=W.height;
}bj=bh.getMarginLeft()+bh.getMarginRight();
if((W.width+bj)>bd){bd=W.width+bj;
}if((W.minWidth+bj)>V){V=W.minWidth+bj;
}}X+=ba;
var bf=this.getSpacing();
var bi=this.getSeparator();

if(bi){var be=bc.computeVerticalSeparatorGaps(bk,bf,bi);
}else{var be=bc.computeVerticalGaps(bk,bf,true);
}return {minHeight:X+be,height:bb+be,minWidth:V,width:bd};
}},destruct:function(){this.__kS=this.__kJ=this.__ff=null;
}});
})();
(function(){var b="tree-folder",a="qx.ui.tree.TreeFolder";
qx.Class.define(a,{extend:qx.ui.tree.core.AbstractTreeItem,properties:{appearance:{refine:true,init:b}},members:{_addWidgets:function(){this.addSpacer();
this.addOpenButton();
this.addIcon();
this.addLabel();
}}});
})();
(function(){var m="]",l="/rpc/",k="http://",j="scoville_admin.scvRpc",h='scoville_admin/server_invalid.png',g='scoville_admin/module.png',d='Modules',c='scoville_admin/site.png',b='dblclick',a='Userroles',K='',J='scoville_admin/role.png',I='Users',H="TestServer1",G="authenticateUser",F="Auth Error [",E="testseite",D="",C="Invalid Server [",B="scoville_admin.Server",t='scoville_admin/loading.gif',u="kochchef",r='scoville_admin/server_locked.png',s='Sites',p="grindhold",q='scoville_admin/user.png',n="getUsers",o="zigapeda",v=" [",w="getServerInfo",y='scoville_admin/server.png',x="-> loading <- [",A="testseite1";
var z={"name":H,"users":[{"name":p},{"name":o},{"name":u}],"projects":[{"name":A,"modules":[],"sites":[]},{"name":E,"modules":[],"sites":[]}],"permissions":[]};
qx.Class.define(B,{extend:qx.ui.tree.TreeFolder,construct:function(L,M,N,O){this.app=L;
qx.ui.tree.TreeFolder.call(this);
this.ip=M;
this.username=N;
this.password=O;
this.setLabel(x+this.ip+m);
this.setIcon(t);
var P=new qx.io.remote.Rpc(k+M+l,j);
P.setCrossDomain(true);
P.callAsync(this.createGetServerInfoHandler(this),w,D);
},members:{createGetUsersHandler:function(Q){var f=function(R,S){if(S==null){if(R===false){return;
}Q.users=new qx.ui.tree.TreeFolder(I);
Q.users.setIcon(q);
Q.add(Q.users);

for(var i=0;i<R.length;i++){var T=new scoville_admin.User(Q.app,R[i]);
T.addListener(b,Q.createUserCallback(Q.app,T));
Q.users.add(T);
}}else{}};
return f;
},createAuthenticationHandler:function(U){var f=function(V,W){if(W==null){if(V===true){U.loggedin=true;
U.sites=new qx.ui.tree.TreeFolder(s);
U.modules=new qx.ui.tree.TreeFolder(d);
U.roles=new qx.ui.tree.TreeFolder(a);
U.sites.setIcon(c);
U.modules.setIcon(g);
U.roles.setIcon(J);
U.add(U.sites);
U.add(U.modules);
U.add(U.roles);
var X=new qx.io.remote.Rpc(k+U.ip+l,j);
X.setCrossDomain(true);
X.callAsync(U.createGetUsersHandler(U),n);
}else{U.password=K;
U.loggedin=false;
U.setIcon(r);
}}else{U.setLabel(F+U.ip+m);
U.setIcon(h);
}};
return f;
},createUserCallback:function(Y,ba){var f=function(e){new scoville_admin.UserPage(Y,ba);
};
return f;
},createGetServerInfoHandler:function(bb){var f=function(bc,bd){if(bd==null){bb.id=this.loadedServers++;
var bf=z;
bb.name=bc;
bb.setLabel(bb.name+v+bb.ip+m);
bb.setIcon(y);
bb.invalid=false;
var be=new qx.io.remote.Rpc(k+bb.ip+l,j);
be.setCrossDomain(true);
be.callAsync(bb.createAuthenticationHandler(bb),G,bb.username,bb.password);
}else{bb.setLabel(C+bb.ip+m);
bb.setIcon(h);
}};
return f;
},app:null,ip:null,name:null,id:null,invalid:true,loggedin:false},statics:{loadedServers:0}});
})();
(function(){var k=": ",j=",",h="qx1",g="qx.event.type.Event",f="failed",e="String",d="",c="Boolean",b="new Date(Date.UTC(",a="application/json",S=")",R="aborted",Q="refreshSession",P="completed",O="Content-Type",N="2.0",M="timeout",L="application/x-www-form-urlencoded",K="?instanceId=",J="Integer",s="string",t="Object",q="qx.io.remote.Rpc",r="error",o="))",p=" error ",l='(',n="Local error ",u="Application error ",v="Local time-out expired for ",B="Transport error ",A=" (",D="(",C="/.qxrpc",F="POST",E="result",x="UNEXPECTED origin ",I="Error ",H=')',G=".",w="Aborted ",y="Server error ",z="id";
qx.Class.define(q,{extend:qx.core.Object,construct:function(T,U){qx.core.Object.call(this);

if(T!==undefined){this.setUrl(T);
}
if(U!=null){this.setServiceName(U);
}
if(qx.core.ServerSettings){this.__kT=qx.core.ServerSettings.serverPathSuffix;
}},events:{"completed":g,"aborted":g,"failed":g,"timeout":g},statics:{origin:{server:1,application:2,transport:3,local:4},localError:{timeout:1,abort:2},CONVERT_DATES:null,RESPONSE_JSON:null,makeServerURL:function(V){var W=null;

if(qx.core.ServerSettings){W=qx.core.ServerSettings.serverPathPrefix+C+qx.core.ServerSettings.serverPathSuffix;

if(V!=null){W+=K+V;
}}return W;
}},properties:{timeout:{check:J,nullable:true},crossDomain:{check:c,init:false},url:{check:e,nullable:true},serviceName:{check:e,nullable:true},serverData:{check:t,nullable:true},username:{check:e,nullable:true},password:{check:e,nullable:true},useBasicHttpAuth:{check:c,nullable:true},protocol:{init:h,check:function(X){return X==h||X==N;
}}},members:{__kU:null,__kT:null,createRequest:function(){return new qx.io.remote.Request(this.getUrl(),F,a);
},createRpcData:function(Y,ba,bb,bc){var be;
var bd;
if(this.getProtocol()==h){be={"service":ba==Q?null:this.getServiceName(),"method":ba,"id":Y,"params":bb};
if(bc){be.server_data=bc;
}}else{bd=this.getServiceName();

if(bd&&bd!=d){bd+=G;
}else{bd=d;
}be={"jsonrpc":N,"method":bd+ba,"id":Y,"params":bb};
}return be;
},_callInternal:function(bf,bg,bh){var self=this;
var bv=(bg==0?0:1);
var bz=(bh?Q:bf[bv]);
var bs=bf[0];
var bk=[];
var bq=this;
var bl=this.getProtocol();

for(var i=bv+1;i<bf.length;++i){bk.push(bf[i]);
}var bm=this.createRequest();
var by=this.getServerData();
var bo=this.createRpcData(bm.getSequenceNumber(),bz,bk,by);
bm.setCrossDomain(this.getCrossDomain());

if(this.getUsername()){bm.setUseBasicHttpAuth(this.getUseBasicHttpAuth());
bm.setUsername(this.getUsername());
bm.setPassword(this.getPassword());
}bm.setTimeout(this.getTimeout());
var bt=null;
var bp=null;
var bi=null;
var bw=null;
var bj=function(bA,bB){switch(bg){case 0:break;
case 1:bs(bi,bt,bp);
break;
case 2:if(!bt){bB.fireDataEvent(bA,bw);
}else{bt.id=bp;

if(bf[0]){bB.fireDataEvent(f,bt);
}else{bB.fireDataEvent(bA,bt);
}}}};
var br=function(bC){if(bl==h){bC.toString=function(){switch(bC.origin){case qx.io.remote.Rpc.origin.server:return y+bC.code+k+bC.message;
case qx.io.remote.Rpc.origin.application:return u+bC.code+k+bC.message;
case qx.io.remote.Rpc.origin.transport:return B+bC.code+k+bC.message;
case qx.io.remote.Rpc.origin.local:return n+bC.code+k+bC.message;
default:return (x+bC.origin+p+bC.code+k+bC.message);
}};
}else{bC.toString=function(){var bD;
bD=I+bC.code+k+bC.message;

if(bC.data){bD+=A+bC.data+S;
}return bD;
};
}};
var bx=function(bE,bF,bG){var bH=new Object();

if(bl==h){bH.origin=bE;
}bH.code=bF;
bH.message=bG;
br(bH);
return bH;
};
bm.addListener(f,function(bI){var bJ=bI.getStatusCode();
bt=bx(qx.io.remote.Rpc.origin.transport,bJ,qx.io.remote.Exchange.statusCodeToString(bJ));
bp=this.getSequenceNumber();
bj(f,bq);
});
bm.addListener(M,function(bK){this.debug("TIMEOUT OCCURRED");
bt=bx(qx.io.remote.Rpc.origin.local,qx.io.remote.Rpc.localError.timeout,v+bz);
bp=this.getSequenceNumber();
bj(M,bq);
});
bm.addListener(R,function(bL){bt=bx(qx.io.remote.Rpc.origin.local,qx.io.remote.Rpc.localError.abort,w+bz);
bp=this.getSequenceNumber();
bj(R,bq);
});
bm.addListener(P,function(bM){bw=bM.getContent();
if(!qx.lang.Type.isObject(bw)){if(self._isConvertDates()){if(self._isResponseJson()){bw=qx.lang.Json.parse(bw,function(bQ,bR){if(bR&&typeof bR===s){if(bR.indexOf(b)>=0){var m=bR.match(/new Date\(Date.UTC\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)\)/);
return new Date(Date.UTC(m[1],m[2],m[3],m[4],m[5],m[6],m[7]));
}}return bR;
});
}else{bw=bw&&bw.length>0?eval(l+bw+H):null;
}}else{bw=qx.lang.Json.parse(bw);
}}bp=bw[z];

if(bp!=this.getSequenceNumber()){this.warn("Received id ("+bp+") does not match requested id "+"("+this.getSequenceNumber()+")!");
}var bO=P;
var bP=bw[r];

if(bP!=null){bi=null;
br(bP);
bt=bP;
bO=f;
}else{bi=bw[E];

if(bh){bi=eval(D+bi+S);
var bN=qx.core.ServerSettings.serverPathSuffix;

if(self.__kT!=bN){self.__kU=self.__kT;
self.__kT=bN;
}self.setUrl(self.fixUrl(self.getUrl()));
}}bj(bO,bq);
});
var bn=null;

if(this._isConvertDates()){bn=function(bS,bT){bT=this[bS];

if(qx.lang.Type.isDate(bT)){var bU=bT.getUTCFullYear()+j+bT.getUTCMonth()+j+bT.getUTCDate()+j+bT.getUTCHours()+j+bT.getUTCMinutes()+j+bT.getUTCSeconds()+j+bT.getUTCMilliseconds();
return b+bU+o;
}return bT;
};
}bm.setData(qx.lang.Json.stringify(bo,bn));
bm.setAsynchronous(bg>0);

if(bm.getCrossDomain()){bm.setRequestHeader(O,L);
}else{bm.setRequestHeader(O,a);
}bm.setParseJson(false);
bm.send();

if(bg==0){if(bt!=null){var bu=new Error(bt.toString());
bu.rpcdetails=bt;
throw bu;
}return bi;
}else{return bm;
}},fixUrl:function(bV){if(this.__kU==null||this.__kT==null||this.__kU==d||this.__kU==this.__kT){return bV;
}var bW=bV.indexOf(this.__kU);

if(bW==-1){return bV;
}return (bV.substring(0,bW)+this.__kT+bV.substring(bW+this.__kU.length));
},callSync:function(bX){return this._callInternal(arguments,0);
},callAsync:function(bY,ca){return this._callInternal(arguments,1);
},callAsyncListeners:function(cb,cc){return this._callInternal(arguments,2);
},refreshSession:function(cd){if(qx.core.ServerSettings&&qx.core.ServerSettings.serverPathSuffix){var ce=(new Date()).getTime()-qx.core.ServerSettings.lastSessionRefresh;

if(ce/1000>(qx.core.ServerSettings.sessionTimeoutInSeconds-30)){this._callInternal([cd],1,true);
}else{cd(true);
}}else{cd(false);
}},_isConvertDates:function(){return !!((qx.util&&qx.util.Json&&qx.util.Json.CONVERT_DATES)||qx.io.remote.Rpc.CONVERT_DATES);
},_isResponseJson:function(){return !!(qx.io.remote.Rpc.RESPONSE_JSON);
},abort:function(cf){cf.abort();
}}});
})();
(function(){var k="Boolean",j="qx.event.type.Event",i="queued",h="String",g="sending",f="receiving",d="aborted",c="failed",b="nocache",a="completed",P="qx.io.remote.Response",O="POST",N="configured",M="timeout",L="GET",K="Pragma",J="no-url-params-on-post",I="PUT",H="no-cache",G="Cache-Control",r="Content-Type",s="text/plain",p="application/xml",q="application/json",n="text/html",o="application/x-www-form-urlencoded",l="qx.io.remote.Exchange",m="Integer",t="X-Qooxdoo-Response-Type",u="HEAD",y="qx.io.remote.Request",x="_applyResponseType",A="_applyState",z="text/javascript",C="changeState",B="_applyProhibitCaching",w="",F="_applyMethod",E="DELETE",D="boolean";
qx.Class.define(y,{extend:qx.core.Object,construct:function(Q,R,S){qx.core.Object.call(this);
this.__kV={};
this.__kW={};
this.__kX={};
this.__kY={};

if(Q!==undefined){this.setUrl(Q);
}
if(R!==undefined){this.setMethod(R);
}
if(S!==undefined){this.setResponseType(S);
}this.setProhibitCaching(true);
this.__la=++qx.io.remote.Request.__la;
},events:{"created":j,"configured":j,"sending":j,"receiving":j,"completed":P,"aborted":j,"failed":P,"timeout":P},statics:{__la:0,methodAllowsRequestBody:function(T){return (T==O)||(T==I);
}},properties:{url:{check:h,init:w},method:{check:[L,O,I,u,E],apply:F,init:L},asynchronous:{check:k,init:true},data:{check:h,nullable:true},username:{check:h,nullable:true},password:{check:h,nullable:true},state:{check:[N,i,g,f,a,d,M,c],init:N,apply:A,event:C},responseType:{check:[s,z,q,p,n],init:s,apply:x},timeout:{check:m,nullable:true},prohibitCaching:{check:function(v){return typeof v==D||v===J;
},init:true,apply:B},crossDomain:{check:k,init:false},fileUpload:{check:k,init:false},transport:{check:l,nullable:true},useBasicHttpAuth:{check:k,init:false},parseJson:{check:k,init:true}},members:{__kV:null,__kW:null,__kX:null,__kY:null,__la:null,send:function(){qx.io.remote.RequestQueue.getInstance().add(this);
},abort:function(){qx.io.remote.RequestQueue.getInstance().abort(this);
},reset:function(){switch(this.getState()){case g:case f:this.error("Aborting already sent request!");
case i:this.abort();
break;
}},isConfigured:function(){return this.getState()===N;
},isQueued:function(){return this.getState()===i;
},isSending:function(){return this.getState()===g;
},isReceiving:function(){return this.getState()===f;
},isCompleted:function(){return this.getState()===a;
},isAborted:function(){return this.getState()===d;
},isTimeout:function(){return this.getState()===M;
},isFailed:function(){return this.getState()===c;
},__lb:qx.event.GlobalError.observeMethod(function(e){var U=e.clone();
U.setTarget(this);
this.dispatchEvent(U);
}),_onqueued:function(e){this.setState(i);
this.__lb(e);
},_onsending:function(e){this.setState(g);
this.__lb(e);
},_onreceiving:function(e){this.setState(f);
this.__lb(e);
},_oncompleted:function(e){this.setState(a);
this.__lb(e);
this.dispose();
},_onaborted:function(e){this.setState(d);
this.__lb(e);
this.dispose();
},_ontimeout:function(e){this.setState(M);
this.__lb(e);
this.dispose();
},_onfailed:function(e){this.setState(c);
this.__lb(e);
this.dispose();
},_applyState:function(V,W){},_applyProhibitCaching:function(X,Y){if(!X){this.removeParameter(b);
this.removeRequestHeader(K);
this.removeRequestHeader(G);
return;
}if(X!==J||this.getMethod()!=O){this.setParameter(b,new Date().valueOf());
}else{this.removeParameter(b);
}this.setRequestHeader(K,H);
this.setRequestHeader(G,H);
},_applyMethod:function(ba,bb){if(qx.io.remote.Request.methodAllowsRequestBody(ba)){this.setRequestHeader(r,o);
}else{this.removeRequestHeader(r);
}var bc=this.getProhibitCaching();
this._applyProhibitCaching(bc,bc);
},_applyResponseType:function(bd,be){this.setRequestHeader(t,bd);
},setRequestHeader:function(bf,bg){this.__kV[bf]=bg;
},removeRequestHeader:function(bh){delete this.__kV[bh];
},getRequestHeader:function(bi){return this.__kV[bi]||null;
},getRequestHeaders:function(){return this.__kV;
},setParameter:function(bj,bk,bl){if(bl){this.__kX[bj]=bk;
}else{this.__kW[bj]=bk;
}},removeParameter:function(bm,bn){if(bn){delete this.__kX[bm];
}else{delete this.__kW[bm];
}},getParameter:function(bo,bp){if(bp){return this.__kX[bo]||null;
}else{return this.__kW[bo]||null;
}},getParameters:function(bq){return (bq?this.__kX:this.__kW);
},setFormField:function(br,bs){this.__kY[br]=bs;
},removeFormField:function(bt){delete this.__kY[bt];
},getFormField:function(bu){return this.__kY[bu]||null;
},getFormFields:function(){return this.__kY;
},getSequenceNumber:function(){return this.__la;
}},destruct:function(){this.setTransport(null);
this.__kV=this.__kW=this.__kX=this.__kY=null;
}});
})();
(function(){var t="Integer",s="aborted",r="_onaborted",q="_on",p="_applyEnabled",o="Boolean",n="sending",m="interval",l="failed",k="qx.io.remote.RequestQueue",c="timeout",j="completed",g="__je",b="queued",a="io.maxrequests",f="__lc",d="receiving",h="singleton";
qx.Class.define(k,{type:h,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__dF=[];
this.__lc=[];
this.__ld=0;
this.__je=new qx.event.Timer(500);
this.__je.addListener(m,this._oninterval,this);
},properties:{enabled:{init:true,check:o,apply:p},maxTotalRequests:{check:t,nullable:true},maxConcurrentRequests:{check:t,init:qx.core.Environment.get(a)},defaultTimeout:{check:t,init:5000}},members:{__dF:null,__lc:null,__ld:null,__je:null,getRequestQueue:function(){return this.__dF;
},getActiveQueue:function(){return this.__lc;
},_debug:function(){var u;
},_check:function(){this._debug();
if(this.__lc.length==0&&this.__dF.length==0){this.__je.stop();
}if(!this.getEnabled()){return;
}if(this.__dF.length==0||(this.__dF[0].isAsynchronous()&&this.__lc.length>=this.getMaxConcurrentRequests())){return;
}if(this.getMaxTotalRequests()!=null&&this.__ld>=this.getMaxTotalRequests()){return;
}var v=this.__dF.shift();
var w=new qx.io.remote.Exchange(v);
this.__ld++;
this.__lc.push(w);
this._debug();
w.addListener(n,this._onsending,this);
w.addListener(d,this._onreceiving,this);
w.addListener(j,this._oncompleted,this);
w.addListener(s,this._oncompleted,this);
w.addListener(c,this._oncompleted,this);
w.addListener(l,this._oncompleted,this);
w._start=(new Date).valueOf();
w.send();
if(this.__dF.length>0){this._check();
}},_remove:function(x){qx.lang.Array.remove(this.__lc,x);
x.dispose();
this._check();
},__le:0,_onsending:function(e){e.getTarget().getRequest()._onsending(e);
},_onreceiving:function(e){e.getTarget().getRequest()._onreceiving(e);
},_oncompleted:function(e){var z=e.getTarget().getRequest();
var y=q+e.getType();
this._remove(e.getTarget());
try{if(z[y]){z[y](e);
}}catch(A){this.error("Request "+z+" handler "+y+" threw an error: ",A);
try{if(z[r]){var event=qx.event.Registration.createEvent(s,qx.event.type.Event);
z[r](event);
}}catch(B){}}},_oninterval:function(e){var I=this.__lc;

if(I.length==0){this.__je.stop();
return;
}var D=(new Date).valueOf();
var G;
var E;
var H=this.getDefaultTimeout();
var F;
var C;

for(var i=I.length-1;i>=0;i--){G=I[i];
E=G.getRequest();

if(E.isAsynchronous()){F=E.getTimeout();
if(F==0){continue;
}
if(F==null){F=H;
}C=D-G._start;

if(C>F){this.warn("Timeout: transport "+G.toHashCode());
this.warn(C+"ms > "+F+"ms");
G.timeout();
}}}},_applyEnabled:function(J,K){if(J){this._check();
}this.__je.setEnabled(J);
},add:function(L){L.setState(b);

if(L.isAsynchronous()){this.__dF.push(L);
}else{this.__dF.unshift(L);
}this._check();

if(this.getEnabled()){this.__je.start();
}},abort:function(M){var N=M.getTransport();

if(N){N.abort();
}else if(qx.lang.Array.contains(this.__dF,M)){qx.lang.Array.remove(this.__dF,M);
}}},destruct:function(){this._disposeArray(f);
this._disposeObjects(g);
this.__dF=null;
}});
})();
(function(){var o="failed",n="sending",m="completed",k="receiving",j="aborted",h="timeout",g="qx.event.type.Event",f="Connection dropped",d="qx.io.remote.Response",c="=",bp="configured",bo="&",bn="Unknown status code. ",bm="qx.io.remote.transport.XmlHttp",bl="qx.io.remote.transport.Abstract",bk="Request-URL too large",bj="MSHTML-specific HTTP status code",bi="Not available",bh="Precondition failed",bg="Server error",v="Moved temporarily",w="qx.io.remote.Exchange",t="Possibly due to a cross-domain request?",u="Bad gateway",r="Gone",s="See other",p="Partial content",q="Server timeout",B="qx.io.remote.transport.Script",C="HTTP version not supported",L="Unauthorized",I="Possibly due to application URL using 'file:' protocol?",T="Multiple choices",O="Payment required",bc="Not implemented",Y="Proxy authentication required",E="Length required",bf="_applyState",be="changeState",bd="Not modified",D="qx.io.remote.Request",G="Connection closed by server",H="Moved permanently",K="_applyImplementation",M="",P="Method not allowed",V="Forbidden",bb="Use proxy",x="Ok",y="Conflict",F="Not found",S="Not acceptable",R="Request time-out",Q="Bad request",X="No content",W="file:",N="qx.io.remote.transport.Iframe",U="Request entity too large",a="Unknown status code",ba="Unsupported media type",z="Gateway time-out",A="created",J="Out of resources",b="undefined";
qx.Class.define(w,{extend:qx.core.Object,construct:function(bq){qx.core.Object.call(this);
this.setRequest(bq);
bq.setTransport(this);
},events:{"sending":g,"receiving":g,"completed":d,"aborted":g,"failed":d,"timeout":d},statics:{typesOrder:[bm,N,B],typesReady:false,typesAvailable:{},typesSupported:{},registerType:function(br,bs){qx.io.remote.Exchange.typesAvailable[bs]=br;
},initTypes:function(){if(qx.io.remote.Exchange.typesReady){return;
}
for(var bu in qx.io.remote.Exchange.typesAvailable){var bt=qx.io.remote.Exchange.typesAvailable[bu];

if(bt.isSupported()){qx.io.remote.Exchange.typesSupported[bu]=bt;
}}qx.io.remote.Exchange.typesReady=true;

if(qx.lang.Object.isEmpty(qx.io.remote.Exchange.typesSupported)){throw new Error("No supported transport types were found!");
}},canHandle:function(bv,bw,bx){if(!qx.lang.Array.contains(bv.handles.responseTypes,bx)){return false;
}
for(var by in bw){if(!bv.handles[by]){return false;
}}return true;
},_nativeMap:{0:A,1:bp,2:n,3:k,4:m},wasSuccessful:function(bz,bA,bB){if(bB){switch(bz){case null:case 0:return true;
case -1:return bA<4;
default:return typeof bz===b;
}}else{switch(bz){case -1:{};
return bA<4;
case 200:case 304:return true;
case 201:case 202:case 203:case 204:case 205:return true;
case 206:{};
return bA!==4;
case 300:case 301:case 302:case 303:case 305:case 400:case 401:case 402:case 403:case 404:case 405:case 406:case 407:case 408:case 409:case 410:case 411:case 412:case 413:case 414:case 415:case 500:case 501:case 502:case 503:case 504:case 505:{};
return false;
case 12002:case 12007:case 12029:case 12030:case 12031:case 12152:case 13030:{};
return false;
default:if(bz>206&&bz<300){return true;
}qx.log.Logger.debug(this,"Unknown status code: "+bz+" ("+bA+")");
return false;
}}},statusCodeToString:function(bC){switch(bC){case -1:return bi;
case 0:var bD=window.location.href;
if(qx.lang.String.startsWith(bD.toLowerCase(),W)){return (bn+I);
}else{return (bn+t);
}break;
case 200:return x;
case 304:return bd;
case 206:return p;
case 204:return X;
case 300:return T;
case 301:return H;
case 302:return v;
case 303:return s;
case 305:return bb;
case 400:return Q;
case 401:return L;
case 402:return O;
case 403:return V;
case 404:return F;
case 405:return P;
case 406:return S;
case 407:return Y;
case 408:return R;
case 409:return y;
case 410:return r;
case 411:return E;
case 412:return bh;
case 413:return U;
case 414:return bk;
case 415:return ba;
case 500:return bg;
case 501:return bc;
case 502:return u;
case 503:return J;
case 504:return z;
case 505:return C;
case 12002:return q;
case 12029:return f;
case 12030:return f;
case 12031:return f;
case 12152:return G;
case 13030:return bj;
default:return a;
}}},properties:{request:{check:D,nullable:true},implementation:{check:bl,nullable:true,apply:K},state:{check:[bp,n,k,m,j,h,o],init:bp,event:be,apply:bf}},members:{send:function(){var bH=this.getRequest();

if(!bH){return this.error("Please attach a request object first");
}qx.io.remote.Exchange.initTypes();
var bF=qx.io.remote.Exchange.typesOrder;
var bE=qx.io.remote.Exchange.typesSupported;
var bJ=bH.getResponseType();
var bK={};

if(bH.getAsynchronous()){bK.asynchronous=true;
}else{bK.synchronous=true;
}
if(bH.getCrossDomain()){bK.crossDomain=true;
}
if(bH.getFileUpload()){bK.fileUpload=true;
}for(var bI in bH.getFormFields()){bK.programaticFormFields=true;
break;
}var bL,bG;

for(var i=0,l=bF.length;i<l;i++){bL=bE[bF[i]];

if(bL){if(!qx.io.remote.Exchange.canHandle(bL,bK,bJ)){continue;
}
try{bG=new bL;
this.setImplementation(bG);
bG.setUseBasicHttpAuth(bH.getUseBasicHttpAuth());
bG.send();
return true;
}catch(bM){this.error("Request handler throws error");
this.error(bM);
return;
}}}this.error("There is no transport implementation available to handle this request: "+bH);
},abort:function(){var bN=this.getImplementation();

if(bN){bN.abort();
}else{this.setState(j);
}},timeout:function(){var bQ=this.getImplementation();

if(bQ){var bP=M;

for(var bO in bQ.getParameters()){bP+=bo+bO+c+bQ.getParameters()[bO];
}this.warn("Timeout: implementation "+bQ.toHashCode()+", "+bQ.getUrl()+" ["+bQ.getMethod()+"], "+bP);
bQ.timeout();
}else{this.warn("Timeout: forcing state to timeout");
this.setState(h);
}this.__lf();
},__lf:function(){var bR=this.getRequest();

if(bR){bR.setTimeout(0);
}},_onsending:function(e){this.setState(n);
},_onreceiving:function(e){this.setState(k);
},_oncompleted:function(e){this.setState(m);
},_onabort:function(e){this.setState(j);
},_onfailed:function(e){this.setState(o);
},_ontimeout:function(e){this.setState(h);
},_applyImplementation:function(bS,bT){if(bT){bT.removeListener(n,this._onsending,this);
bT.removeListener(k,this._onreceiving,this);
bT.removeListener(m,this._oncompleted,this);
bT.removeListener(j,this._onabort,this);
bT.removeListener(h,this._ontimeout,this);
bT.removeListener(o,this._onfailed,this);
}
if(bS){var bV=this.getRequest();
bS.setUrl(bV.getUrl());
bS.setMethod(bV.getMethod());
bS.setAsynchronous(bV.getAsynchronous());
bS.setUsername(bV.getUsername());
bS.setPassword(bV.getPassword());
bS.setParameters(bV.getParameters(false));
bS.setFormFields(bV.getFormFields());
bS.setRequestHeaders(bV.getRequestHeaders());
if(bS instanceof qx.io.remote.transport.XmlHttp){bS.setParseJson(bV.getParseJson());
}var bY=bV.getData();

if(bY===null){var ca=bV.getParameters(true);
var bX=[];

for(var bU in ca){var bW=ca[bU];

if(bW instanceof Array){for(var i=0;i<bW.length;i++){bX.push(encodeURIComponent(bU)+c+encodeURIComponent(bW[i]));
}}else{bX.push(encodeURIComponent(bU)+c+encodeURIComponent(bW));
}}
if(bX.length>0){bS.setData(bX.join(bo));
}}else{bS.setData(bY);
}bS.setResponseType(bV.getResponseType());
bS.addListener(n,this._onsending,this);
bS.addListener(k,this._onreceiving,this);
bS.addListener(m,this._oncompleted,this);
bS.addListener(j,this._onabort,this);
bS.addListener(h,this._ontimeout,this);
bS.addListener(o,this._onfailed,this);
}},_applyState:function(cb,cc){switch(cb){case n:this.fireEvent(n);
break;
case k:this.fireEvent(k);
break;
case m:case j:case h:case o:var ce=this.getImplementation();

if(!ce){break;
}this.__lf();

if(this.hasListener(cb)){var cf=qx.event.Registration.createEvent(cb,qx.io.remote.Response);

if(cb==m){var cd=ce.getResponseContent();
cf.setContent(cd);
if(cd===null){cb=o;
}}else if(cb==o){cf.setContent(ce.getResponseContent());
}cf.setStatusCode(ce.getStatusCode());
cf.setResponseHeaders(ce.getResponseHeaders());
this.dispatchEvent(cf);
}this.setImplementation(null);
ce.dispose();
break;
}}},environment:{"qx.ioRemoteDebug":false,"qx.ioRemoteDebugData":false},destruct:function(){var cg=this.getImplementation();

if(cg){this.setImplementation(null);
cg.dispose();
}this.setRequest(null);
}});
})();
(function(){var q="qx.event.type.Event",p="String",o="failed",n="timeout",m="created",l="aborted",k="sending",j="configured",i="receiving",h="completed",c="Object",g="Boolean",f="abstract",b="_applyState",a="GET",e="changeState",d="qx.io.remote.transport.Abstract";
qx.Class.define(d,{type:f,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.setRequestHeaders({});
this.setParameters({});
this.setFormFields({});
},events:{"created":q,"configured":q,"sending":q,"receiving":q,"completed":q,"aborted":q,"failed":q,"timeout":q},properties:{url:{check:p,nullable:true},method:{check:p,nullable:true,init:a},asynchronous:{check:g,nullable:true,init:true},data:{check:p,nullable:true},username:{check:p,nullable:true},password:{check:p,nullable:true},state:{check:[m,j,k,i,h,l,n,o],init:m,event:e,apply:b},requestHeaders:{check:c,nullable:true},parameters:{check:c,nullable:true},formFields:{check:c,nullable:true},responseType:{check:p,nullable:true},useBasicHttpAuth:{check:g,nullable:true}},members:{send:function(){throw new Error("send is abstract");
},abort:function(){this.setState(l);
},timeout:function(){this.setState(n);
},failed:function(){this.setState(o);
},setRequestHeader:function(r,s){throw new Error("setRequestHeader is abstract");
},getResponseHeader:function(t){throw new Error("getResponseHeader is abstract");
},getResponseHeaders:function(){throw new Error("getResponseHeaders is abstract");
},getStatusCode:function(){throw new Error("getStatusCode is abstract");
},getStatusText:function(){throw new Error("getStatusText is abstract");
},getResponseText:function(){throw new Error("getResponseText is abstract");
},getResponseXml:function(){throw new Error("getResponseXml is abstract");
},getFetchedLength:function(){throw new Error("getFetchedLength is abstract");
},_applyState:function(u,v){switch(u){case m:this.fireEvent(m);
break;
case j:this.fireEvent(j);
break;
case k:this.fireEvent(k);
break;
case i:this.fireEvent(i);
break;
case h:this.fireEvent(h);
break;
case l:this.fireEvent(l);
break;
case o:this.fireEvent(o);
break;
case n:this.fireEvent(n);
break;
}return true;
}},destruct:function(){this.setRequestHeaders(null);
this.setParameters(null);
this.setFormFields(null);
}});
})();
(function(){var l="=",k="",j="engine.name",h="&",g="application/xml",f="application/json",d="text/html",c="textarea",b="_data_",a="load",G="text/plain",F="text/javascript",E="readystatechange",D="completed",C="?",B="qx.io.remote.transport.Iframe",A="none",z="display",y="gecko",x="frame_",s="aborted",t="pre",q="javascript:void(0)",r="sending",o="form",p="failed",m="mshtml",n="form_",u="opera",v="timeout",w="qx/static/blank.gif";
qx.Class.define(B,{extend:qx.io.remote.transport.Abstract,construct:function(){qx.io.remote.transport.Abstract.call(this);
var H=(new Date).valueOf();
var I=x+H;
var J=n+H;
var K;

if((qx.core.Environment.get(j)==m)){K=q;
}this.__lg=qx.bom.Iframe.create({id:I,name:I,src:K});
qx.bom.element.Style.set(this.__lg,z,A);
this.__lh=qx.bom.Element.create(o,{id:J,name:J,target:I});
qx.bom.element.Style.set(this.__lh,z,A);
qx.dom.Element.insertEnd(this.__lh,qx.dom.Node.getBodyElement(document));
this.__cN=qx.bom.Element.create(c,{id:b,name:b});
qx.dom.Element.insertEnd(this.__cN,this.__lh);
qx.dom.Element.insertEnd(this.__lg,qx.dom.Node.getBodyElement(document));
qx.event.Registration.addListener(this.__lg,a,this._onload,this);
this.__li=qx.lang.Function.listener(this._onreadystatechange,this);
qx.bom.Event.addNativeListener(this.__lg,E,this.__li);
},statics:{handles:{synchronous:false,asynchronous:true,crossDomain:false,fileUpload:true,programaticFormFields:true,responseTypes:[G,F,f,g,d]},isSupported:function(){return true;
},_numericMap:{"uninitialized":1,"loading":2,"loaded":2,"interactive":3,"complete":4}},members:{__cN:null,__lj:0,__lh:null,__lg:null,__li:null,send:function(){var M=this.getMethod();
var O=this.getUrl();
var S=this.getParameters(false);
var R=[];

for(var N in S){var P=S[N];

if(P instanceof Array){for(var i=0;i<P.length;i++){R.push(encodeURIComponent(N)+l+encodeURIComponent(P[i]));
}}else{R.push(encodeURIComponent(N)+l+encodeURIComponent(P));
}}
if(R.length>0){O+=(O.indexOf(C)>=0?h:C)+R.join(h);
}if(this.getData()===null){var S=this.getParameters(true);
var R=[];

for(var N in S){var P=S[N];

if(P instanceof Array){for(var i=0;i<P.length;i++){R.push(encodeURIComponent(N)+l+encodeURIComponent(P[i]));
}}else{R.push(encodeURIComponent(N)+l+encodeURIComponent(P));
}}
if(R.length>0){this.setData(R.join(h));
}}var L=this.getFormFields();

for(var N in L){var Q=document.createElement(c);
Q.name=N;
Q.appendChild(document.createTextNode(L[N]));
this.__lh.appendChild(Q);
}this.__lh.action=O;
this.__lh.method=M;
this.__cN.appendChild(document.createTextNode(this.getData()));
this.__lh.submit();
this.setState(r);
},_onload:qx.event.GlobalError.observeMethod(function(e){if(qx.core.Environment.get(j)==u&&this.getIframeHtmlContent()==k){return;
}
if(this.__lh.src){return;
}this._switchReadyState(qx.io.remote.transport.Iframe._numericMap.complete);
}),_onreadystatechange:qx.event.GlobalError.observeMethod(function(e){this._switchReadyState(qx.io.remote.transport.Iframe._numericMap[this.__lg.readyState]);
}),_switchReadyState:function(T){switch(this.getState()){case D:case s:case p:case v:this.warn("Ignore Ready State Change");
return;
}while(this.__lj<T){this.setState(qx.io.remote.Exchange._nativeMap[++this.__lj]);
}},setRequestHeader:function(U,V){},getResponseHeader:function(W){return null;
},getResponseHeaders:function(){return {};
},getStatusCode:function(){return 200;
},getStatusText:function(){return k;
},getIframeWindow:function(){return qx.bom.Iframe.getWindow(this.__lg);
},getIframeDocument:function(){return qx.bom.Iframe.getDocument(this.__lg);
},getIframeBody:function(){return qx.bom.Iframe.getBody(this.__lg);
},getIframeTextContent:function(){var X=this.getIframeBody();

if(!X){return null;
}
if(!X.firstChild){return k;
}if(X.firstChild.tagName&&X.firstChild.tagName.toLowerCase()==t){return X.firstChild.innerHTML;
}else{return X.innerHTML;
}},getIframeHtmlContent:function(){var Y=this.getIframeBody();
return Y?Y.innerHTML:null;
},getFetchedLength:function(){return 0;
},getResponseContent:function(){if(this.getState()!==D){return null;
}var ba=this.getIframeTextContent();

switch(this.getResponseType()){case G:{};
return ba;
break;
case d:ba=this.getIframeHtmlContent();
{};
return ba;
break;
case f:ba=this.getIframeHtmlContent();
{};

try{return ba&&ba.length>0?qx.lang.Json.parse(ba):null;
}catch(bb){return this.error("Could not execute json: ("+ba+")",bb);
}case F:ba=this.getIframeHtmlContent();
{};

try{return ba&&ba.length>0?window.eval(ba):null;
}catch(bc){return this.error("Could not execute javascript: ("+ba+")",bc);
}case g:ba=this.getIframeDocument();
{};
return ba;
default:this.warn("No valid responseType specified ("+this.getResponseType()+")!");
return null;
}}},defer:function(){qx.io.remote.Exchange.registerType(qx.io.remote.transport.Iframe,B);
},destruct:function(){if(this.__lg){qx.event.Registration.removeListener(this.__lg,a,this._onload,this);
qx.bom.Event.removeNativeListener(this.__lg,E,this.__li);
if((qx.core.Environment.get(j)==y)){this.__lg.src=qx.util.ResourceManager.getInstance().toUri(w);
}qx.dom.Element.remove(this.__lg);
}
if(this.__lh){qx.dom.Element.remove(this.__lh);
}this.__lg=this.__lh=this.__cN=null;
}});
})();
(function(){var d="qx.event.handler.Iframe",c="load",b="iframe",a="navigate";
qx.Class.define(d,{extend:qx.core.Object,implement:qx.event.IEventHandler,statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{load:1,navigate:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:false,onevent:qx.event.GlobalError.observeMethod(function(e){var f=qx.bom.Iframe.queryCurrentUrl(e);

if(f!==e.$$url){qx.event.Registration.fireEvent(e,a,qx.event.type.Data,[f]);
e.$$url=f;
}qx.event.Registration.fireEvent(e,c);
})},members:{canHandleEvent:function(g,h){return g.tagName.toLowerCase()===b;
},registerEvent:function(i,j,k){},unregisterEvent:function(l,m,n){}},defer:function(o){qx.event.Registration.addHandler(o);
}});
})();
(function(){var i="engine.name",h="load",g="",f="qx.bom.Iframe",e="osx",d="os.name",c="webkit",b="iframe",a="body";
qx.Class.define(f,{statics:{DEFAULT_ATTRIBUTES:{onload:"qx.event.handler.Iframe.onevent(this)",frameBorder:0,frameSpacing:0,marginWidth:0,marginHeight:0,hspace:0,vspace:0,border:0,allowTransparency:true},create:function(j,k){var j=j?qx.lang.Object.clone(j):{};
var l=qx.bom.Iframe.DEFAULT_ATTRIBUTES;

for(var m in l){if(j[m]==null){j[m]=l[m];
}}return qx.bom.Element.create(b,j,k);
},getWindow:function(n){try{return n.contentWindow;
}catch(o){return null;
}},getDocument:qx.core.Environment.select(i,{"mshtml":function(p){try{var q=this.getWindow(p);
return q?q.document:null;
}catch(r){return null;
}},"default":function(s){try{return s.contentDocument;
}catch(t){return null;
}}}),getBody:function(u){try{var v=this.getDocument(u);
return v?v.getElementsByTagName(a)[0]:null;
}catch(w){return null;
}},setSource:function(x,y){try{if(this.getWindow(x)&&qx.dom.Hierarchy.isRendered(x)){try{if((qx.core.Environment.get(i)==c)&&qx.core.Environment.get(d)==e){var z=this.getWindow(x);

if(z){z.stop();
}}this.getWindow(x).location.replace(y);
}catch(A){x.src=y;
}}else{x.src=y;
}this.__lk(x);
}catch(B){qx.log.Logger.warn("Iframe source could not be set!");
}},queryCurrentUrl:function(C){var D=this.getDocument(C);

try{if(D&&D.location){return D.location.href;
}}catch(E){}return g;
},__lk:function(F){var G=function(){qx.bom.Event.removeNativeListener(F,h,G);
F.$$url=qx.bom.Iframe.queryCurrentUrl(F);
};
qx.bom.Event.addNativeListener(F,h,G);
}}});
})();
(function(){var r="&",q="=",p="?",o="application/json",n="completed",m="text/plain",l="text/javascript",k="qx.io.remote.transport.Script",j="",h="_ScriptTransport_data",c="script",g="timeout",f="_ScriptTransport_",b="_ScriptTransport_id",a="aborted",e="utf-8",d="failed";
qx.Class.define(k,{extend:qx.io.remote.transport.Abstract,construct:function(){qx.io.remote.transport.Abstract.call(this);
var s=++qx.io.remote.transport.Script.__ll;

if(s>=2000000000){qx.io.remote.transport.Script.__ll=s=1;
}this.__eS=null;
this.__ll=s;
},statics:{__ll:0,_instanceRegistry:{},ScriptTransport_PREFIX:f,ScriptTransport_ID_PARAM:b,ScriptTransport_DATA_PARAM:h,handles:{synchronous:false,asynchronous:true,crossDomain:true,fileUpload:false,programaticFormFields:false,responseTypes:[m,l,o]},isSupported:function(){return true;
},_numericMap:{"uninitialized":1,"loading":2,"loaded":2,"interactive":3,"complete":4},_requestFinished:qx.event.GlobalError.observeMethod(function(t,content){var u=qx.io.remote.transport.Script._instanceRegistry[t];

if(u==null){}else{u._responseContent=content;
u._switchReadyState(qx.io.remote.transport.Script._numericMap.complete);
}})},members:{__lj:0,__eS:null,__ll:null,send:function(){var x=this.getUrl();
x+=(x.indexOf(p)>=0?r:p)+qx.io.remote.transport.Script.ScriptTransport_ID_PARAM+q+this.__ll;
var A=this.getParameters();
var z=[];

for(var w in A){if(w.indexOf(qx.io.remote.transport.Script.ScriptTransport_PREFIX)==0){this.error("Illegal parameter name. The following prefix is used internally by qooxdoo): "+qx.io.remote.transport.Script.ScriptTransport_PREFIX);
}var y=A[w];

if(y instanceof Array){for(var i=0;i<y.length;i++){z.push(encodeURIComponent(w)+q+encodeURIComponent(y[i]));
}}else{z.push(encodeURIComponent(w)+q+encodeURIComponent(y));
}}
if(z.length>0){x+=r+z.join(r);
}var v=this.getData();

if(v!=null){x+=r+qx.io.remote.transport.Script.ScriptTransport_DATA_PARAM+q+encodeURIComponent(v);
}qx.io.remote.transport.Script._instanceRegistry[this.__ll]=this;
this.__eS=document.createElement(c);
this.__eS.charset=e;
this.__eS.src=x;
document.body.appendChild(this.__eS);
},_switchReadyState:function(B){switch(this.getState()){case n:case a:case d:case g:this.warn("Ignore Ready State Change");
return;
}while(this.__lj<B){this.setState(qx.io.remote.Exchange._nativeMap[++this.__lj]);
}},setRequestHeader:function(C,D){},getResponseHeader:function(E){return null;
},getResponseHeaders:function(){return {};
},getStatusCode:function(){return 200;
},getStatusText:function(){return j;
},getFetchedLength:function(){return 0;
},getResponseContent:function(){if(this.getState()!==n){return null;
}
switch(this.getResponseType()){case m:case o:case l:{};
var F=this._responseContent;
return (F===0?0:(F||null));
default:this.warn("No valid responseType specified ("+this.getResponseType()+")!");
return null;
}}},defer:function(){qx.io.remote.Exchange.registerType(qx.io.remote.transport.Script,k);
},destruct:function(){if(this.__eS){delete qx.io.remote.transport.Script._instanceRegistry[this.__ll];
document.body.removeChild(this.__eS);
}this.__eS=this._responseContent=null;
}});
})();
(function(){var m="failed",k="completed",j="=",h="aborted",g="sending",f="",d="&",c="engine.name",b="configured",a="timeout",L="application/xml",K="qx.io.remote.transport.XmlHttp",J="application/json",I="text/html",H="receiving",G="text/plain",F="text/javascript",E="?",D="created",C="Boolean",u='Referer',v="engine.version",r='Basic ',t="\n</pre>",p="string",q='Authorization',n="<pre>Could not execute json: \n",o="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",w="mshtml",x=':',z="parseerror",y="file:",B="webkit",A="object";
qx.Class.define(K,{extend:qx.io.remote.transport.Abstract,statics:{handles:{synchronous:true,asynchronous:true,crossDomain:false,fileUpload:false,programaticFormFields:false,responseTypes:[G,F,J,L,I]},createRequestObject:qx.core.Environment.select(c,{"default":function(){return new XMLHttpRequest;
},"mshtml":function(){if(window.ActiveXObject&&qx.xml.Document.XMLHTTP){return new ActiveXObject(qx.xml.Document.XMLHTTP);
}
if(window.XMLHttpRequest){return new XMLHttpRequest;
}}}),isSupported:function(){return !!this.createRequestObject();
}},properties:{parseJson:{check:C,init:true}},members:{__lm:false,__lj:0,__ln:null,getRequest:function(){if(this.__ln===null){this.__ln=qx.io.remote.transport.XmlHttp.createRequestObject();
this.__ln.onreadystatechange=qx.lang.Function.bind(this._onreadystatechange,this);
}return this.__ln;
},send:function(){this.__lj=0;
var Q=this.getRequest();
var M=this.getMethod();
var T=this.getAsynchronous();
var S=this.getUrl();
var O=(window.location.protocol===y&&!(/^http(s){0,1}\:/.test(S)));
this.__lm=O;
var W=this.getParameters(false);
var U=[];

for(var N in W){var R=W[N];

if(R instanceof Array){for(var i=0;i<R.length;i++){U.push(encodeURIComponent(N)+j+encodeURIComponent(R[i]));
}}else{U.push(encodeURIComponent(N)+j+encodeURIComponent(R));
}}
if(U.length>0){S+=(S.indexOf(E)>=0?d:E)+U.join(d);
}if(this.getData()===null){var W=this.getParameters(true);
var U=[];

for(var N in W){var R=W[N];

if(R instanceof Array){for(var i=0;i<R.length;i++){U.push(encodeURIComponent(N)+j+encodeURIComponent(R[i]));
}}else{U.push(encodeURIComponent(N)+j+encodeURIComponent(R));
}}
if(U.length>0){this.setData(U.join(d));
}}var V=function(X){var bd=o;
var bh=f;
var bb,ba,Y;
var be,bf,bg,bc;
var i=0;

do{bb=X.charCodeAt(i++);
ba=X.charCodeAt(i++);
Y=X.charCodeAt(i++);
be=bb>>2;
bf=((bb&3)<<4)|(ba>>4);
bg=((ba&15)<<2)|(Y>>6);
bc=Y&63;

if(isNaN(ba)){bg=bc=64;
}else if(isNaN(Y)){bc=64;
}bh+=bd.charAt(be)+bd.charAt(bf)+bd.charAt(bg)+bd.charAt(bc);
}while(i<X.length);
return bh;
};
try{if(this.getUsername()){if(this.getUseBasicHttpAuth()){Q.open(M,S,T);
Q.setRequestHeader(q,r+V(this.getUsername()+x+this.getPassword()));
}else{Q.open(M,S,T,this.getUsername(),this.getPassword());
}}else{Q.open(M,S,T);
}}catch(bi){this.error("Failed with exception: "+bi);
this.failed();
return;
}if(!(qx.core.Environment.get(c)==B)){Q.setRequestHeader(u,window.location.href);
}var P=this.getRequestHeaders();

for(var N in P){Q.setRequestHeader(N,P[N]);
}try{if(O&&T&&qx.core.Environment.get(c)==w&&qx.core.Environment.get(v)==9){qx.event.Timer.once(function(){Q.send(this.getData());
},this,0);
}else{Q.send(this.getData());
}}catch(bj){if(O){this.failedLocally();
}else{this.error("Failed to send data: "+bj,"send");
this.failed();
}return;
}if(!T){this._onreadystatechange();
}},failedLocally:function(){if(this.getState()===m){return;
}this.warn("Could not load from file: "+this.getUrl());
this.failed();
},_onreadystatechange:qx.event.GlobalError.observeMethod(function(e){switch(this.getState()){case k:case h:case m:case a:{};
return;
}var bk=this.getReadyState();

if(bk==4){if(!qx.io.remote.Exchange.wasSuccessful(this.getStatusCode(),bk,this.__lm)){if(this.getState()===b){this.setState(g);
}this.failed();
return;
}}if(bk==3&&this.__lj==1){this.setState(qx.io.remote.Exchange._nativeMap[++this.__lj]);
}while(this.__lj<bk){this.setState(qx.io.remote.Exchange._nativeMap[++this.__lj]);
}}),getReadyState:function(){var bl=null;

try{bl=this.getRequest().readyState;
}catch(bm){}return bl;
},setRequestHeader:function(bn,bo){this.getRequestHeaders()[bn]=bo;
},getResponseHeader:function(bp){var bq=null;

try{bq=this.getRequest().getResponseHeader(bp)||null;
}catch(br){}return bq;
},getStringResponseHeaders:function(){var bt=null;

try{var bs=this.getRequest().getAllResponseHeaders();

if(bs){bt=bs;
}}catch(bu){}return bt;
},getResponseHeaders:function(){var bx=this.getStringResponseHeaders();
var by={};

if(bx){var bv=bx.split(/[\r\n]+/g);

for(var i=0,l=bv.length;i<l;i++){var bw=bv[i].match(/^([^:]+)\s*:\s*(.+)$/i);

if(bw){by[bw[1]]=bw[2];
}}}return by;
},getStatusCode:function(){var bz=-1;

try{bz=this.getRequest().status;
if(bz===1223){bz=204;
}}catch(bA){}return bz;
},getStatusText:function(){var bB=f;

try{bB=this.getRequest().statusText;
}catch(bC){}return bB;
},getResponseText:function(){var bD=null;

try{bD=this.getRequest().responseText;
}catch(bE){bD=null;
}return bD;
},getResponseXml:function(){var bH=null;
var bF=this.getStatusCode();
var bG=this.getReadyState();

if(qx.io.remote.Exchange.wasSuccessful(bF,bG,this.__lm)){try{bH=this.getRequest().responseXML;
}catch(bI){}}if(typeof bH==A&&bH!=null){if(!bH.documentElement){var s=String(this.getRequest().responseText).replace(/<\?xml[^\?]*\?>/,f);
bH.loadXML(s);
}if(!bH.documentElement){throw new Error("Missing Document Element!");
}
if(bH.documentElement.tagName==z){throw new Error("XML-File is not well-formed!");
}}else{throw new Error("Response was not a valid xml document ["+this.getRequest().responseText+"]");
}return bH;
},getFetchedLength:function(){var bJ=this.getResponseText();
return typeof bJ==p?bJ.length:0;
},getResponseContent:function(){var bK=this.getState();

if(bK!==k&&bK!=m){return null;
}var bM=this.getResponseText();

if(bK==m){return bM;
}
switch(this.getResponseType()){case G:case I:{};
return bM;
case J:{};

try{if(bM&&bM.length>0){var bL;

if(this.getParseJson()){bL=qx.lang.Json.parse(bM);
bL=(bL===0?0:(bL||null));
}else{bL=bM;
}return bL;
}else{return null;
}}catch(bN){this.error("Could not execute json: ["+bM+"]",bN);
return n+bM+t;
}case F:{};

try{if(bM&&bM.length>0){var bL=window.eval(bM);
return (bL===0?0:(bL||null));
}else{return null;
}}catch(bO){this.error("Could not execute javascript: ["+bM+"]",bO);
return null;
}case L:bM=this.getResponseXml();
{};
return (bM===0?0:(bM||null));
default:this.warn("No valid responseType specified ("+this.getResponseType()+")!");
return null;
}},_applyState:function(bP,bQ){switch(bP){case D:this.fireEvent(D);
break;
case b:this.fireEvent(b);
break;
case g:this.fireEvent(g);
break;
case H:this.fireEvent(H);
break;
case k:this.fireEvent(k);
break;
case m:this.fireEvent(m);
break;
case h:this.getRequest().abort();
this.fireEvent(h);
break;
case a:this.getRequest().abort();
this.fireEvent(a);
break;
}}},defer:function(){qx.io.remote.Exchange.registerType(qx.io.remote.transport.XmlHttp,K);
},destruct:function(){var bR=this.getRequest();

if(bR){bR.onreadystatechange=qx.lang.Function.empty;
switch(bR.readyState){case 1:case 2:case 3:bR.abort();
}}this.__ln=null;
}});
})();
(function(){var c="Integer",b="Object",a="qx.io.remote.Response";
qx.Class.define(a,{extend:qx.event.type.Event,properties:{state:{check:c,nullable:true},statusCode:{check:c,nullable:true},content:{nullable:true},responseHeaders:{check:b,nullable:true}},members:{clone:function(d){var e=qx.event.type.Event.prototype.clone.call(this,d);
e.setType(this.getType());
e.setState(this.getState());
e.setStatusCode(this.getStatusCode());
e.setContent(this.getContent());
e.setResponseHeaders(this.getResponseHeaders());
return e;
},getResponseHeader:function(f){var g=this.getResponseHeaders();

if(g){return g[f]||null;
}return null;
}}});
})();
(function(){var b='scoville_admin/user.png',a="scoville_admin.User";
qx.Class.define(a,{extend:qx.ui.tree.TreeFolder,construct:function(c,d){this.app=c;
qx.ui.tree.TreeFolder.call(this);
this.name=d.name;
this.setLabel(this.name);
this.setIcon(b);
},members:{app:null,name:null}});
})();
(function(){var l="button",k="",j="close",i="String",h="_applyIcon",g="page",f="qx.event.type.Event",e="_applyShowCloseButton",d="tabview-page",c="qx.ui.tabview.Page",a="_applyLabel",b="Boolean";
qx.Class.define(c,{extend:qx.ui.container.Composite,construct:function(m,n){qx.ui.container.Composite.call(this);
this._createChildControl(l);
if(m!=null){this.setLabel(m);
}
if(n!=null){this.setIcon(n);
}},events:{"close":f},properties:{appearance:{refine:true,init:d},label:{check:i,init:k,apply:a},icon:{check:i,init:k,apply:h},showCloseButton:{check:b,init:false,apply:e}},members:{_forwardStates:{barTop:1,barRight:1,barBottom:1,barLeft:1,firstTab:1,lastTab:1},_applyIcon:function(o,p){this.getChildControl(l).setIcon(o);
},_applyLabel:function(q,r){this.getChildControl(l).setLabel(q);
},_applyEnabled:function(s,t){qx.ui.container.Composite.prototype._applyEnabled.call(this,s,t);
var u=this.getChildControl(l);
s==null?u.resetEnabled():u.setEnabled(s);
},_createChildControlImpl:function(v,w){var x;

switch(v){case l:x=new qx.ui.tabview.TabButton;
x.setAllowGrowX(true);
x.setAllowGrowY(true);
x.setUserData(g,this);
x.addListener(j,this._onButtonClose,this);
break;
}return x||qx.ui.container.Composite.prototype._createChildControlImpl.call(this,v);
},_applyShowCloseButton:function(y,z){this.getChildControl(l).setShowCloseButton(y);
},_onButtonClose:function(){this.fireEvent(j);
},getButton:function(){return this.getChildControl(l);
}}});
})();
(function(){var b="qx.ui.form.IExecutable",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"execute":a},members:{setCommand:function(c){return arguments.length==1;
},getCommand:function(){},execute:function(){}}});
})();
(function(){var o="pressed",n="abandoned",m="hovered",l="Enter",k="Space",j="dblclick",i="qx.ui.form.Button",h="mouseup",g="mousedown",f="mouseover",b="mouseout",d="keydown",c="button",a="keyup";
qx.Class.define(i,{extend:qx.ui.basic.Atom,include:[qx.ui.core.MExecutable],implement:[qx.ui.form.IExecutable],construct:function(p,q,r){qx.ui.basic.Atom.call(this,p,q);

if(r!=null){this.setCommand(r);
}this.addListener(f,this._onMouseOver);
this.addListener(b,this._onMouseOut);
this.addListener(g,this._onMouseDown);
this.addListener(h,this._onMouseUp);
this.addListener(d,this._onKeyDown);
this.addListener(a,this._onKeyUp);
this.addListener(j,this._onStopEvent);
},properties:{appearance:{refine:true,init:c},focusable:{refine:true,init:true}},members:{_forwardStates:{focused:true,hovered:true,pressed:true,disabled:true},press:function(){if(this.hasState(n)){return;
}this.addState(o);
},release:function(){if(this.hasState(o)){this.removeState(o);
}},reset:function(){this.removeState(o);
this.removeState(n);
this.removeState(m);
},_onMouseOver:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}
if(this.hasState(n)){this.removeState(n);
this.addState(o);
}this.addState(m);
},_onMouseOut:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}this.removeState(m);

if(this.hasState(o)){this.removeState(o);
this.addState(n);
}},_onMouseDown:function(e){if(!e.isLeftPressed()){return;
}e.stopPropagation();
this.capture();
this.removeState(n);
this.addState(o);
},_onMouseUp:function(e){this.releaseCapture();
var s=this.hasState(o);
var t=this.hasState(n);

if(s){this.removeState(o);
}
if(t){this.removeState(n);
}else{this.addState(m);

if(s){this.execute();
}}e.stopPropagation();
},_onKeyDown:function(e){switch(e.getKeyIdentifier()){case l:case k:this.removeState(n);
this.addState(o);
e.stopPropagation();
}},_onKeyUp:function(e){switch(e.getKeyIdentifier()){case l:case k:if(this.hasState(o)){this.removeState(n);
this.removeState(o);
this.execute();
e.stopPropagation();
}}}}});
})();
(function(){var b="qx.ui.form.IRadioItem",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"changeValue":a},members:{setValue:function(c){},getValue:function(){},setGroup:function(d){this.assertInstance(d,qx.ui.form.RadioGroup);
},getGroup:function(){}}});
})();
(function(){var f="change",d="__lo",c="qx.event.type.Data",b="qx.ui.form.MModelSelection",a="changeSelection";
qx.Mixin.define(b,{construct:function(){this.__lo=new qx.data.Array();
this.__lo.addListener(f,this.__lr,this);
this.addListener(a,this.__lq,this);
},events:{changeModelSelection:c},members:{__lo:null,__lp:false,__lq:function(){if(this.__lp){return;
}var k=this.getSelection();
var g=[];

for(var i=0;i<k.length;i++){var l=k[i];
var h=l.getModel?l.getModel():null;

if(h!==null){g.push(h);
}}if(g.length===k.length){try{this.setModelSelection(g);
}catch(e){throw new Error("Could not set the model selection. Maybe your models are not unique?");
}}},__lr:function(){this.__lp=true;
var n=this.getSelectables(true);
var p=[];
var o=this.__lo.toArray();

for(var i=0;i<o.length;i++){var r=o[i];

for(var j=0;j<n.length;j++){var s=n[j];
var m=s.getModel?s.getModel():null;

if(r===m){p.push(s);
break;
}}}this.setSelection(p);
this.__lp=false;
var q=this.getSelection();

if(!qx.lang.Array.equals(q,p)){this.__lq();
}},getModelSelection:function(){return this.__lo;
},setModelSelection:function(t){if(!t){this.__lo.removeAll();
return;
}t.unshift(this.__lo.getLength());
t.unshift(0);
var u=this.__lo.splice.apply(this.__lo,t);
u.dispose();
}},destruct:function(){this._disposeObjects(d);
}});
})();
(function(){var h="[",g="]",f=".",d="idBubble",c="changeBubble",b="qx.data.marshal.MEventBubbling",a="qx.event.type.Data";
qx.Mixin.define(b,{events:{"changeBubble":a},members:{_applyEventPropagation:function(i,j,name){this.fireDataEvent(c,{value:i,name:name,old:j});
this._registerEventChaining(i,j,name);
},_registerEventChaining:function(k,l,name){if((k instanceof qx.core.Object)&&qx.Class.hasMixin(k.constructor,qx.data.marshal.MEventBubbling)){var m=qx.lang.Function.bind(this.__ls,this,name);
var n=k.addListener(c,m,this);
k.setUserData(d,n);
}if(l!=null&&l.getUserData&&l.getUserData(d)!=null){l.removeListenerById(l.getUserData(d));
}},__ls:function(name,e){var v=e.getData();
var r=v.value;
var p=v.old;
if(qx.Class.hasInterface(e.getTarget().constructor,qx.data.IListData)){if(v.name.indexOf){var u=v.name.indexOf(f)!=-1?v.name.indexOf(f):v.name.length;
var s=v.name.indexOf(h)!=-1?v.name.indexOf(h):v.name.length;

if(u<s){var o=v.name.substring(0,u);
var t=v.name.substring(u+1,v.name.length);

if(t[0]!=h){t=f+t;
}var q=name+h+o+g+t;
}else if(s<u){var o=v.name.substring(0,s);
var t=v.name.substring(s,v.name.length);
var q=name+h+o+g+t;
}else{var q=name+h+v.name+g;
}}else{var q=name+h+v.name+g;
}}else{var q=name+f+v.name;
}this.fireDataEvent(c,{value:r,name:q,old:p});
}}});
})();
(function(){var o="change",n="changeBubble",m="add",l="remove",k="0-",j="order",h="-",g="0",f="qx.event.type.Data",e="Boolean",b="",d="qx.data.Array",c="number",a="changeLength";
qx.Class.define(d,{extend:qx.core.Object,include:qx.data.marshal.MEventBubbling,implement:[qx.data.IListData],construct:function(p){qx.core.Object.call(this);
if(p==undefined){this.__lt=[];
}else if(arguments.length>1){this.__lt=[];

for(var i=0;i<arguments.length;i++){this.__lt.push(arguments[i]);
}}else if(typeof p==c){this.__lt=new Array(p);
}else if(p instanceof Array){this.__lt=qx.lang.Array.clone(p);
}else{this.__lt=[];
throw new Error("Type of the parameter not supported!");
}for(var i=0;i<this.__lt.length;i++){this._applyEventPropagation(this.__lt[i],null,i);
}this.__lu();
},properties:{autoDisposeItems:{check:e,init:false}},events:{"change":f,"changeLength":f},members:{__lt:null,concat:function(q){if(q){var r=this.__lt.concat(q);
}else{var r=this.__lt.concat();
}return new qx.data.Array(r);
},join:function(s){return this.__lt.join(s);
},pop:function(){var t=this.__lt.pop();
this.__lu();
this._registerEventChaining(null,t,this.length-1);
this.fireDataEvent(n,{value:[],name:this.length,old:[t]});
this.fireDataEvent(o,{start:this.length-1,end:this.length-1,type:l,items:[t]},null);
return t;
},push:function(u){for(var i=0;i<arguments.length;i++){this.__lt.push(arguments[i]);
this.__lu();
this._registerEventChaining(arguments[i],null,this.length-1);
this.fireDataEvent(n,{value:[arguments[i]],name:this.length-1,old:[]});
this.fireDataEvent(o,{start:this.length-1,end:this.length-1,type:m,items:[arguments[i]]},null);
}return this.length;
},reverse:function(){if(this.length==0){return;
}var v=this.__lt.concat();
this.__lt.reverse();
this.fireDataEvent(o,{start:0,end:this.length-1,type:j,items:null},null);
this.fireDataEvent(n,{value:this.__lt,name:k+(this.__lt.length-1),old:v});
},shift:function(){if(this.length==0){return;
}var w=this.__lt.shift();
this.__lu();
this._registerEventChaining(null,w,this.length-1);
this.fireDataEvent(n,{value:[],name:g,old:[w]});
this.fireDataEvent(o,{start:0,end:this.length-1,type:l,items:[w]},null);
return w;
},slice:function(x,y){return new qx.data.Array(this.__lt.slice(x,y));
},splice:function(z,A,B){var J=this.__lt.length;
var F=this.__lt.splice.apply(this.__lt,arguments);
if(this.__lt.length!=J){this.__lu();
}var H=A>0;
var D=arguments.length>2;
var E=null;

if(H||D){if(this.__lt.length>J){var I=m;
}else if(this.__lt.length<J){var I=l;
E=F;
}else{var I=j;
}this.fireDataEvent(o,{start:z,end:this.length-1,type:I,items:E},null);
}for(var i=2;i<arguments.length;i++){this._registerEventChaining(arguments[i],null,z+i);
}var G=[];

for(var i=2;i<arguments.length;i++){G[i-2]=arguments[i];
}var C=(z+Math.max(arguments.length-3,A-1));
var name=z==C?C:z+h+C;
this.fireDataEvent(n,{value:G,name:name,old:F});
for(var i=0;i<F.length;i++){this._registerEventChaining(null,F[i],i);
}return (new qx.data.Array(F));
},sort:function(K){if(this.length==0){return;
}var L=this.__lt.concat();
this.__lt.sort.apply(this.__lt,arguments);
this.fireDataEvent(o,{start:0,end:this.length-1,type:j,items:null},null);
this.fireDataEvent(n,{value:this.__lt,name:k+(this.length-1),old:L});
},unshift:function(M){for(var i=arguments.length-1;i>=0;i--){this.__lt.unshift(arguments[i]);
this.__lu();
this._registerEventChaining(arguments[i],null,0);
this.fireDataEvent(n,{value:[this.__lt[0]],name:g,old:[this.__lt[1]]});
this.fireDataEvent(o,{start:0,end:this.length-1,type:m,items:[arguments[i]]},null);
}return this.length;
},toArray:function(){return this.__lt;
},getItem:function(N){return this.__lt[N];
},setItem:function(O,P){var Q=this.__lt[O];
if(Q===P){return;
}this.__lt[O]=P;
this._registerEventChaining(P,Q,O);
if(this.length!=this.__lt.length){this.__lu();
}this.fireDataEvent(n,{value:[P],name:O,old:[Q]});
this.fireDataEvent(o,{start:O,end:O,type:m,items:[P]},null);
},getLength:function(){return this.length;
},indexOf:function(R){return this.__lt.indexOf(R);
},toString:function(){if(this.__lt!=null){return this.__lt.toString();
}return b;
},contains:function(S){return this.__lt.indexOf(S)!==-1;
},copy:function(){return this.concat();
},insertAt:function(T,U){this.splice(T,0,U);
},insertBefore:function(V,W){var X=this.indexOf(V);

if(X==-1){this.push(W);
}else{this.splice(X,0,W);
}},insertAfter:function(Y,ba){var bb=this.indexOf(Y);

if(bb==-1||bb==(this.length-1)){this.push(ba);
}else{this.splice(bb+1,0,ba);
}},removeAt:function(bc){var be=this.splice(bc,1);
var bd=be.getItem(0);
be.dispose();
return bd;
},removeAll:function(){for(var i=0;i<this.__lt.length;i++){this._registerEventChaining(null,this.__lt[i],i);
}if(this.getLength()==0){return;
}var bg=this.getLength();
var bf=this.__lt.concat();
this.__lt.length=0;
this.__lu();
this.fireDataEvent(n,{value:[],name:k+(bg-1),old:bf});
this.fireDataEvent(o,{start:0,end:bg-1,type:l,items:bf},null);
return bf;
},append:function(bh){if(bh instanceof qx.data.Array){bh=bh.toArray();
}Array.prototype.push.apply(this.__lt,bh);
for(var i=0;i<bh.length;i++){this._registerEventChaining(bh[i],null,this.__lt.length+i);
}var bi=this.length;
this.__lu();
this.fireDataEvent(n,{value:bh,name:bi==(this.length-1)?bi:bi+h+(this.length-1),old:[]});
this.fireDataEvent(o,{start:bi,end:this.length-1,type:m,items:bh},null);
},remove:function(bj){var bk=this.indexOf(bj);

if(bk!=-1){this.splice(bk,1);
return bj;
}},equals:function(bl){if(this.length!==bl.length){return false;
}
for(var i=0;i<this.length;i++){if(this.getItem(i)!==bl.getItem(i)){return false;
}}return true;
},sum:function(){var bm=0;

for(var i=0;i<this.length;i++){bm+=this.getItem(i);
}return bm;
},max:function(){var bn=this.getItem(0);

for(var i=1;i<this.length;i++){if(this.getItem(i)>bn){bn=this.getItem(i);
}}return bn===undefined?null:bn;
},min:function(){var bo=this.getItem(0);

for(var i=1;i<this.length;i++){if(this.getItem(i)<bo){bo=this.getItem(i);
}}return bo===undefined?null:bo;
},forEach:function(bp,bq){for(var i=0;i<this.__lt.length;i++){bp.call(bq,this.__lt[i],i,this);
}},__lu:function(){var br=this.length;
this.length=this.__lt.length;
this.fireDataEvent(a,this.length,br);
}},destruct:function(){for(var i=0;i<this.__lt.length;i++){var bs=this.__lt[i];
this._applyEventPropagation(null,bs,i);
if(this.isAutoDisposeItems()&&bs&&bs instanceof qx.core.Object){bs.dispose();
}}this.__lt=null;
}});
})();
(function(){var b="qx.ui.core.ISingleSelection",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"changeSelection":a},members:{getSelection:function(){return true;
},setSelection:function(c){return arguments.length==1;
},resetSelection:function(){return true;
},isSelected:function(d){return arguments.length==1;
},isSelectionEmpty:function(){return true;
},getSelectables:function(e){return arguments.length==1;
}}});
})();
(function(){var f="qx.ui.core.MSingleSelectionHandling",d="__eI",c="changeSelection",b="changeSelected",a="qx.event.type.Data";
qx.Mixin.define(f,{events:{"changeSelection":a},members:{__eI:null,getSelection:function(){var g=this.__lv().getSelected();

if(g){return [g];
}else{return [];
}},setSelection:function(h){switch(h.length){case 0:this.resetSelection();
break;
case 1:this.__lv().setSelected(h[0]);
break;
default:throw new Error("Could only select one item, but the selection"+" array contains "+h.length+" items!");
}},resetSelection:function(){this.__lv().resetSelected();
},isSelected:function(i){return this.__lv().isSelected(i);
},isSelectionEmpty:function(){return this.__lv().isSelectionEmpty();
},getSelectables:function(j){return this.__lv().getSelectables(j);
},_onChangeSelected:function(e){var l=e.getData();
var k=e.getOldData();
l==null?l=[]:l=[l];
k==null?k=[]:k=[k];
this.fireDataEvent(c,l,k);
},__lv:function(){if(this.__eI==null){var m=this;
this.__eI=new qx.ui.core.SingleSelectionManager({getItems:function(){return m._getItems();
},isItemSelectable:function(n){if(m._isItemSelectable){return m._isItemSelectable(n);
}else{return n.isVisible();
}}});
this.__eI.addListener(b,this._onChangeSelected,this);
}this.__eI.setAllowEmptySelection(this._isAllowEmptySelection());
return this.__eI;
}},destruct:function(){this._disposeObjects(d);
}});
})();
(function(){var g="Boolean",f="qx.ui.core.SingleSelectionManager",e="__lw",d="changeSelected",c="qx.event.type.Data",b="__lx",a="__ly";
qx.Class.define(f,{extend:qx.core.Object,construct:function(h){qx.core.Object.call(this);
this.__lw=h;
},events:{"changeSelected":c},properties:{allowEmptySelection:{check:g,init:true,apply:a}},members:{__lx:null,__lw:null,getSelected:function(){return this.__lx;
},setSelected:function(j){if(!this.__lA(j)){throw new Error("Could not select "+j+", because it is not a child element!");
}this.__lz(j);
},resetSelected:function(){this.__lz(null);
},isSelected:function(k){if(!this.__lA(k)){throw new Error("Could not check if "+k+" is selected,"+" because it is not a child element!");
}return this.__lx===k;
},isSelectionEmpty:function(){return this.__lx==null;
},getSelectables:function(l){var m=this.__lw.getItems();
var n=[];

for(var i=0;i<m.length;i++){if(this.__lw.isItemSelectable(m[i])){n.push(m[i]);
}}if(!l){for(var i=n.length-1;i>=0;i--){if(!n[i].getEnabled()){n.splice(i,1);
}}}return n;
},__ly:function(o,p){if(!o){this.__lz(this.__lx);
}},__lz:function(q){var t=this.__lx;
var s=q;

if(s!=null&&t===s){return;
}
if(!this.isAllowEmptySelection()&&s==null){var r=this.getSelectables(true)[0];

if(r){s=r;
}}this.__lx=s;
this.fireDataEvent(d,s,t);
},__lA:function(u){var v=this.__lw.getItems();

for(var i=0;i<v.length;i++){if(v[i]===u){return true;
}}return false;
}},destruct:function(){if(this.__lw.toHashCode){this._disposeObjects(e);
}else{this.__lw=null;
}this._disposeObjects(b);
}});
})();
(function(){var a="qx.ui.form.IModelSelection";
qx.Interface.define(a,{members:{setModelSelection:function(b){},getModelSelection:function(){}}});
})();
(function(){var r="Boolean",q="changeInvalidMessage",p="changeValue",o="String",n="_applyAllowEmptySelection",m="_applyInvalidMessage",k="qx.ui.form.RadioGroup",j="_applyValid",h="",g="changeRequired",c="changeValid",f="changeEnabled",d="__lB",b="changeSelection",a="_applyEnabled";
qx.Class.define(k,{extend:qx.core.Object,implement:[qx.ui.core.ISingleSelection,qx.ui.form.IForm,qx.ui.form.IModelSelection],include:[qx.ui.core.MSingleSelectionHandling,qx.ui.form.MModelSelection],construct:function(s){qx.core.Object.call(this);
this.__lB=[];
this.addListener(b,this.__lC,this);

if(s!=null){this.add.apply(this,arguments);
}},properties:{enabled:{check:r,apply:a,event:f,init:true},wrap:{check:r,init:true},allowEmptySelection:{check:r,init:false,apply:n},valid:{check:r,init:true,apply:j,event:c},required:{check:r,init:false,event:g},invalidMessage:{check:o,init:h,event:q,apply:m},requiredInvalidMessage:{check:o,nullable:true,event:q}},members:{__lB:null,getItems:function(){return this.__lB;
},add:function(t){var u=this.__lB;
var v;

for(var i=0,l=arguments.length;i<l;i++){v=arguments[i];

if(qx.lang.Array.contains(u,v)){continue;
}v.addListener(p,this._onItemChangeChecked,this);
u.push(v);
v.setGroup(this);
if(v.getValue()){this.setSelection([v]);
}}if(!this.isAllowEmptySelection()&&u.length>0&&!this.getSelection()[0]){this.setSelection([u[0]]);
}},remove:function(w){var x=this.__lB;

if(qx.lang.Array.contains(x,w)){qx.lang.Array.remove(x,w);
if(w.getGroup()===this){w.resetGroup();
}w.removeListener(p,this._onItemChangeChecked,this);
if(w.getValue()){this.resetSelection();
}}},getChildren:function(){return this.__lB;
},_onItemChangeChecked:function(e){var y=e.getTarget();

if(y.getValue()){this.setSelection([y]);
}else if(this.getSelection()[0]==y){this.resetSelection();
}},_applyInvalidMessage:function(z,A){for(var i=0;i<this.__lB.length;i++){this.__lB[i].setInvalidMessage(z);
}},_applyValid:function(B,C){for(var i=0;i<this.__lB.length;i++){this.__lB[i].setValid(B);
}},_applyEnabled:function(D,E){var F=this.__lB;

if(D==null){for(var i=0,l=F.length;i<l;i++){F[i].resetEnabled();
}}else{for(var i=0,l=F.length;i<l;i++){F[i].setEnabled(D);
}}},_applyAllowEmptySelection:function(G,H){if(!G&&this.isSelectionEmpty()){this.resetSelection();
}},selectNext:function(){var I=this.getSelection()[0];
var K=this.__lB;
var J=K.indexOf(I);

if(J==-1){return;
}var i=0;
var length=K.length;
if(this.getWrap()){J=(J+1)%length;
}else{J=Math.min(J+1,length-1);
}
while(i<length&&!K[J].getEnabled()){J=(J+1)%length;
i++;
}this.setSelection([K[J]]);
},selectPrevious:function(){var L=this.getSelection()[0];
var N=this.__lB;
var M=N.indexOf(L);

if(M==-1){return;
}var i=0;
var length=N.length;
if(this.getWrap()){M=(M-1+length)%length;
}else{M=Math.max(M-1,0);
}
while(i<length&&!N[M].getEnabled()){M=(M-1+length)%length;
i++;
}this.setSelection([N[M]]);
},_getItems:function(){return this.getItems();
},_isAllowEmptySelection:function(){return this.isAllowEmptySelection();
},_isItemSelectable:function(O){return this.__lB.indexOf(O)!=-1;
},__lC:function(e){var Q=e.getData()[0];
var P=e.getOldData()[0];

if(P){P.setValue(false);
}
if(Q){Q.setValue(true);
}}},destruct:function(){this._disposeArray(d);
}});
})();
(function(){var l="qx.dynlocale",k="Boolean",j="changeLocale",i="changeInvalidMessage",h="String",g="invalid",f="",d="qx.ui.form.MForm",c="_applyValid",b="changeRequired",a="changeValid";
qx.Mixin.define(d,{construct:function(){if(qx.core.Environment.get(l)){qx.locale.Manager.getInstance().addListener(j,this.__lD,this);
}},properties:{valid:{check:k,init:true,apply:c,event:a},required:{check:k,init:false,event:b},invalidMessage:{check:h,init:f,event:i},requiredInvalidMessage:{check:h,nullable:true,event:i}},members:{_applyValid:function(m,n){m?this.removeState(g):this.addState(g);
},__lD:qx.core.Environment.select(l,{"true":function(e){var o=this.getInvalidMessage();

if(o&&o.translate){this.setInvalidMessage(o.translate());
}var p=this.getRequiredInvalidMessage();

if(p&&p.translate){this.setRequiredInvalidMessage(p.translate());
}},"false":null})},destruct:function(){if(qx.core.Environment.get(l)){qx.locale.Manager.getInstance().removeListener(j,this.__lD,this);
}}});
})();
(function(){var b="qx.ui.form.IBooleanForm",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"changeValue":a},members:{setValue:function(c){return arguments.length==1;
},resetValue:function(){},getValue:function(){}}});
})();
(function(){var t="checked",s="keypress",r="Boolean",q="Right",p="label",o="Left",n="_applyValue",m="changeValue",l="Up",k="value",d="qx.ui.form.RadioButton",j="radiobutton",h="toolTipText",c="enabled",b="qx.ui.form.RadioGroup",g="Down",f="_applyGroup",i="menu",a="execute";
qx.Class.define(d,{extend:qx.ui.form.Button,include:[qx.ui.form.MForm,qx.ui.form.MModelProperty],implement:[qx.ui.form.IRadioItem,qx.ui.form.IForm,qx.ui.form.IBooleanForm,qx.ui.form.IModel],construct:function(u){qx.ui.form.Button.call(this,u);
this.addListener(a,this._onExecute);
this.addListener(s,this._onKeyPress);
},properties:{group:{check:b,nullable:true,apply:f},value:{check:r,nullable:true,event:m,apply:n,init:false},appearance:{refine:true,init:j},allowGrowX:{refine:true,init:false}},members:{_forwardStates:{checked:true,focused:true,invalid:true,hovered:true},_bindableProperties:[c,p,h,k,i],_applyValue:function(v,w){v?this.addState(t):this.removeState(t);

if(v&&this.getFocusable()){this.focus();
}},_applyGroup:function(x,y){if(y){y.remove(this);
}
if(x){x.add(this);
}},_onExecute:function(e){var z=this.getGroup();

if(z&&z.getAllowEmptySelection()){this.toggleValue();
}else{this.setValue(true);
}},_onKeyPress:function(e){var A=this.getGroup();

if(!A){return;
}
switch(e.getKeyIdentifier()){case o:case l:A.selectPrevious();
break;
case q:case g:A.selectNext();
break;
}}}});
})();
(function(){var o="close-button",n="middle",m="left",l="icon",k="label",j="right",i="click",h="Boolean",g="bottom",f="qx.ui.tabview.TabButton",c="center",e="_applyShowCloseButton",d="top",b="close",a="qx.event.type.Data";
qx.Class.define(f,{extend:qx.ui.form.RadioButton,implement:qx.ui.form.IRadioItem,construct:function(){qx.ui.form.RadioButton.call(this);
var p=new qx.ui.layout.Grid(2,0);
p.setRowAlign(0,m,n);
p.setColumnAlign(0,j,n);
this._getLayout().dispose();
this._setLayout(p);
this.initShowCloseButton();
},events:{"close":a},properties:{showCloseButton:{check:h,init:false,apply:e}},members:{_forwardStates:{focused:true,checked:true},_applyIconPosition:function(q,r){var s={icon:this.getChildControl(l),label:this.getChildControl(k),closeButton:this.getShowCloseButton()?this.getChildControl(o):null};
for(var t in s){if(s[t]){this._remove(s[t]);
}}
switch(q){case d:this._add(s.label,{row:3,column:2});
this._add(s.icon,{row:1,column:2});

if(s.closeButton){this._add(s.closeButton,{row:0,column:4});
}break;
case g:this._add(s.label,{row:1,column:2});
this._add(s.icon,{row:3,column:2});

if(s.closeButton){this._add(s.closeButton,{row:0,column:4});
}break;
case m:this._add(s.label,{row:0,column:2});
this._add(s.icon,{row:0,column:0});

if(s.closeButton){this._add(s.closeButton,{row:0,column:4});
}break;
case j:this._add(s.label,{row:0,column:0});
this._add(s.icon,{row:0,column:2});

if(s.closeButton){this._add(s.closeButton,{row:0,column:4});
}break;
}},_createChildControlImpl:function(u,v){var w;

switch(u){case k:var w=new qx.ui.basic.Label(this.getLabel());
w.setAnonymous(true);
this._add(w,{row:0,column:2});
this._getLayout().setColumnFlex(2,1);
break;
case l:w=new qx.ui.basic.Image(this.getIcon());
w.setAnonymous(true);
this._add(w,{row:0,column:0});
break;
case o:w=new qx.ui.form.Button();
w.addListener(i,this._onCloseButtonClick,this);
this._add(w,{row:0,column:4});

if(!this.getShowCloseButton()){w.exclude();
}break;
}return w||qx.ui.form.RadioButton.prototype._createChildControlImpl.call(this,u);
},_onCloseButtonClick:function(){this.fireDataEvent(b,this);
},_applyShowCloseButton:function(x,y){if(x){this._showChildControl(o);
}else{this._excludeChildControl(o);
}},_applyCenter:function(z){var A=this._getLayout();

if(z){A.setColumnAlign(2,c,n);
}else{A.setColumnAlign(2,m,n);
}}}});
})();
(function(){var r="left",q="top",p="_applyLayoutChange",o="hAlign",n="flex",m="vAlign",h="Integer",g="minWidth",f="width",e="minHeight",b="qx.ui.layout.Grid",d="height",c="maxHeight",a="maxWidth";
qx.Class.define(b,{extend:qx.ui.layout.Abstract,construct:function(s,t){qx.ui.layout.Abstract.call(this);
this.__lE=[];
this.__lF=[];

if(s){this.setSpacingX(s);
}
if(t){this.setSpacingY(t);
}},properties:{spacingX:{check:h,init:0,apply:p},spacingY:{check:h,init:0,apply:p}},members:{__lG:null,__lE:null,__lF:null,__lH:null,__lI:null,__lJ:null,__lK:null,__lL:null,__lM:null,verifyLayoutProperty:null,__lN:function(){var B=[];
var A=[];
var C=[];
var w=-1;
var v=-1;
var E=this._getLayoutChildren();

for(var i=0,l=E.length;i<l;i++){var z=E[i];
var D=z.getLayoutProperties();
var F=D.row;
var u=D.column;
D.colSpan=D.colSpan||1;
D.rowSpan=D.rowSpan||1;
if(F==null||u==null){throw new Error("The layout properties 'row' and 'column' of the child widget '"+z+"' must be defined!");
}
if(B[F]&&B[F][u]){throw new Error("Cannot add widget '"+z+"'!. "+"There is already a widget '"+B[F][u]+"' in this cell ("+F+", "+u+")");
}
for(var x=u;x<u+D.colSpan;x++){for(var y=F;y<F+D.rowSpan;y++){if(B[y]==undefined){B[y]=[];
}B[y][x]=z;
v=Math.max(v,x);
w=Math.max(w,y);
}}
if(D.rowSpan>1){C.push(z);
}
if(D.colSpan>1){A.push(z);
}}for(var y=0;y<=w;y++){if(B[y]==undefined){B[y]=[];
}}this.__lG=B;
this.__lH=A;
this.__lI=C;
this.__lJ=w;
this.__lK=v;
this.__lL=null;
this.__lM=null;
delete this._invalidChildrenCache;
},_setRowData:function(G,H,I){var J=this.__lE[G];

if(!J){this.__lE[G]={};
this.__lE[G][H]=I;
}else{J[H]=I;
}},_setColumnData:function(K,L,M){var N=this.__lF[K];

if(!N){this.__lF[K]={};
this.__lF[K][L]=M;
}else{N[L]=M;
}},setSpacing:function(O){this.setSpacingY(O);
this.setSpacingX(O);
return this;
},setColumnAlign:function(P,Q,R){this._setColumnData(P,o,Q);
this._setColumnData(P,m,R);
this._applyLayoutChange();
return this;
},getColumnAlign:function(S){var T=this.__lF[S]||{};
return {vAlign:T.vAlign||q,hAlign:T.hAlign||r};
},setRowAlign:function(U,V,W){this._setRowData(U,o,V);
this._setRowData(U,m,W);
this._applyLayoutChange();
return this;
},getRowAlign:function(X){var Y=this.__lE[X]||{};
return {vAlign:Y.vAlign||q,hAlign:Y.hAlign||r};
},getCellWidget:function(ba,bb){if(this._invalidChildrenCache){this.__lN();
}var ba=this.__lG[ba]||{};
return ba[bb]||null;
},getRowCount:function(){if(this._invalidChildrenCache){this.__lN();
}return this.__lJ+1;
},getColumnCount:function(){if(this._invalidChildrenCache){this.__lN();
}return this.__lK+1;
},getCellAlign:function(bc,bd){var bj=q;
var bh=r;
var bi=this.__lE[bc];
var bf=this.__lF[bd];
var be=this.__lG[bc][bd];

if(be){var bg={vAlign:be.getAlignY(),hAlign:be.getAlignX()};
}else{bg={};
}if(bg.vAlign){bj=bg.vAlign;
}else if(bi&&bi.vAlign){bj=bi.vAlign;
}else if(bf&&bf.vAlign){bj=bf.vAlign;
}if(bg.hAlign){bh=bg.hAlign;
}else if(bf&&bf.hAlign){bh=bf.hAlign;
}else if(bi&&bi.hAlign){bh=bi.hAlign;
}return {vAlign:bj,hAlign:bh};
},setColumnFlex:function(bk,bl){this._setColumnData(bk,n,bl);
this._applyLayoutChange();
return this;
},getColumnFlex:function(bm){var bn=this.__lF[bm]||{};
return bn.flex!==undefined?bn.flex:0;
},setRowFlex:function(bo,bp){this._setRowData(bo,n,bp);
this._applyLayoutChange();
return this;
},getRowFlex:function(bq){var br=this.__lE[bq]||{};
var bs=br.flex!==undefined?br.flex:0;
return bs;
},setColumnMaxWidth:function(bt,bu){this._setColumnData(bt,a,bu);
this._applyLayoutChange();
return this;
},getColumnMaxWidth:function(bv){var bw=this.__lF[bv]||{};
return bw.maxWidth!==undefined?bw.maxWidth:Infinity;
},setColumnWidth:function(bx,by){this._setColumnData(bx,f,by);
this._applyLayoutChange();
return this;
},getColumnWidth:function(bz){var bA=this.__lF[bz]||{};
return bA.width!==undefined?bA.width:null;
},setColumnMinWidth:function(bB,bC){this._setColumnData(bB,g,bC);
this._applyLayoutChange();
return this;
},getColumnMinWidth:function(bD){var bE=this.__lF[bD]||{};
return bE.minWidth||0;
},setRowMaxHeight:function(bF,bG){this._setRowData(bF,c,bG);
this._applyLayoutChange();
return this;
},getRowMaxHeight:function(bH){var bI=this.__lE[bH]||{};
return bI.maxHeight||Infinity;
},setRowHeight:function(bJ,bK){this._setRowData(bJ,d,bK);
this._applyLayoutChange();
return this;
},getRowHeight:function(bL){var bM=this.__lE[bL]||{};
return bM.height!==undefined?bM.height:null;
},setRowMinHeight:function(bN,bO){this._setRowData(bN,e,bO);
this._applyLayoutChange();
return this;
},getRowMinHeight:function(bP){var bQ=this.__lE[bP]||{};
return bQ.minHeight||0;
},__lO:function(bR){var bV=bR.getSizeHint();
var bU=bR.getMarginLeft()+bR.getMarginRight();
var bT=bR.getMarginTop()+bR.getMarginBottom();
var bS={height:bV.height+bT,width:bV.width+bU,minHeight:bV.minHeight+bT,minWidth:bV.minWidth+bU,maxHeight:bV.maxHeight+bT,maxWidth:bV.maxWidth+bU};
return bS;
},_fixHeightsRowSpan:function(bW){var ce=this.getSpacingY();

for(var i=0,l=this.__lI.length;i<l;i++){var cl=this.__lI[i];
var ch=this.__lO(cl);
var ca=cl.getLayoutProperties();
var cg=ca.row;
var cq=ce*(ca.rowSpan-1);
var bX=cq;
var cb={};

for(var j=0;j<ca.rowSpan;j++){var cf=ca.row+j;
var cp=bW[cf];
var cr=this.getRowFlex(cf);

if(cr>0){cb[cf]={min:cp.minHeight,value:cp.height,max:cp.maxHeight,flex:cr};
}cq+=cp.height;
bX+=cp.minHeight;
}if(cq<ch.height){if(!qx.lang.Object.isEmpty(cb)){var cc=qx.ui.layout.Util.computeFlexOffsets(cb,ch.height,cq);

for(var k=0;k<ca.rowSpan;k++){var cn=cc[cg+k]?cc[cg+k].offset:0;
bW[cg+k].height+=cn;
}}else{var ck=ce*(ca.rowSpan-1);
var ci=ch.height-ck;
var co=Math.floor(ci/ca.rowSpan);
var cm=0;
var bY=0;

for(var k=0;k<ca.rowSpan;k++){var cd=bW[cg+k].height;
cm+=cd;

if(cd<co){bY++;
}}var cj=Math.floor((ci-cm)/bY);
for(var k=0;k<ca.rowSpan;k++){if(bW[cg+k].height<co){bW[cg+k].height+=cj;
}}}}if(bX<ch.minHeight){var cc=qx.ui.layout.Util.computeFlexOffsets(cb,ch.minHeight,bX);

for(var j=0;j<ca.rowSpan;j++){var cn=cc[cg+j]?cc[cg+j].offset:0;
bW[cg+j].minHeight+=cn;
}}}},_fixWidthsColSpan:function(cs){var cw=this.getSpacingX();

for(var i=0,l=this.__lH.length;i<l;i++){var ct=this.__lH[i];
var cv=this.__lO(ct);
var cy=ct.getLayoutProperties();
var cu=cy.column;
var cE=cw*(cy.colSpan-1);
var cx=cE;
var cz={};
var cB;

for(var j=0;j<cy.colSpan;j++){var cF=cy.column+j;
var cD=cs[cF];
var cC=this.getColumnFlex(cF);
if(cC>0){cz[cF]={min:cD.minWidth,value:cD.width,max:cD.maxWidth,flex:cC};
}cE+=cD.width;
cx+=cD.minWidth;
}if(cE<cv.width){var cA=qx.ui.layout.Util.computeFlexOffsets(cz,cv.width,cE);

for(var j=0;j<cy.colSpan;j++){cB=cA[cu+j]?cA[cu+j].offset:0;
cs[cu+j].width+=cB;
}}if(cx<cv.minWidth){var cA=qx.ui.layout.Util.computeFlexOffsets(cz,cv.minWidth,cx);

for(var j=0;j<cy.colSpan;j++){cB=cA[cu+j]?cA[cu+j].offset:0;
cs[cu+j].minWidth+=cB;
}}}},_getRowHeights:function(){if(this.__lL!=null){return this.__lL;
}var cP=[];
var cI=this.__lJ;
var cH=this.__lK;

for(var cQ=0;cQ<=cI;cQ++){var cJ=0;
var cL=0;
var cK=0;

for(var cO=0;cO<=cH;cO++){var cG=this.__lG[cQ][cO];

if(!cG){continue;
}var cM=cG.getLayoutProperties().rowSpan||0;

if(cM>1){continue;
}var cN=this.__lO(cG);

if(this.getRowFlex(cQ)>0){cJ=Math.max(cJ,cN.minHeight);
}else{cJ=Math.max(cJ,cN.height);
}cL=Math.max(cL,cN.height);
}var cJ=Math.max(cJ,this.getRowMinHeight(cQ));
var cK=this.getRowMaxHeight(cQ);

if(this.getRowHeight(cQ)!==null){var cL=this.getRowHeight(cQ);
}else{var cL=Math.max(cJ,Math.min(cL,cK));
}cP[cQ]={minHeight:cJ,height:cL,maxHeight:cK};
}
if(this.__lI.length>0){this._fixHeightsRowSpan(cP);
}this.__lL=cP;
return cP;
},_getColWidths:function(){if(this.__lM!=null){return this.__lM;
}var cV=[];
var cS=this.__lK;
var cU=this.__lJ;

for(var db=0;db<=cS;db++){var cY=0;
var cX=0;
var cT=Infinity;

for(var dc=0;dc<=cU;dc++){var cR=this.__lG[dc][db];

if(!cR){continue;
}var cW=cR.getLayoutProperties().colSpan||0;

if(cW>1){continue;
}var da=this.__lO(cR);

if(this.getColumnFlex(db)>0){cX=Math.max(cX,da.minWidth);
}else{cX=Math.max(cX,da.width);
}cY=Math.max(cY,da.width);
}cX=Math.max(cX,this.getColumnMinWidth(db));
cT=this.getColumnMaxWidth(db);

if(this.getColumnWidth(db)!==null){var cY=this.getColumnWidth(db);
}else{var cY=Math.max(cX,Math.min(cY,cT));
}cV[db]={minWidth:cX,width:cY,maxWidth:cT};
}
if(this.__lH.length>0){this._fixWidthsColSpan(cV);
}this.__lM=cV;
return cV;
},_getColumnFlexOffsets:function(dd){var de=this.getSizeHint();
var di=dd-de.width;

if(di==0){return {};
}var dg=this._getColWidths();
var df={};

for(var i=0,l=dg.length;i<l;i++){var dj=dg[i];
var dh=this.getColumnFlex(i);

if((dh<=0)||(dj.width==dj.maxWidth&&di>0)||(dj.width==dj.minWidth&&di<0)){continue;
}df[i]={min:dj.minWidth,value:dj.width,max:dj.maxWidth,flex:dh};
}return qx.ui.layout.Util.computeFlexOffsets(df,dd,de.width);
},_getRowFlexOffsets:function(dk){var dl=this.getSizeHint();
var dp=dk-dl.height;

if(dp==0){return {};
}var dq=this._getRowHeights();
var dm={};

for(var i=0,l=dq.length;i<l;i++){var dr=dq[i];
var dn=this.getRowFlex(i);

if((dn<=0)||(dr.height==dr.maxHeight&&dp>0)||(dr.height==dr.minHeight&&dp<0)){continue;
}dm[i]={min:dr.minHeight,value:dr.height,max:dr.maxHeight,flex:dn};
}return qx.ui.layout.Util.computeFlexOffsets(dm,dk,dl.height);
},renderLayout:function(ds,dt){if(this._invalidChildrenCache){this.__lN();
}var dH=qx.ui.layout.Util;
var dv=this.getSpacingX();
var dB=this.getSpacingY();
var dM=this._getColWidths();
var dL=this._getColumnFlexOffsets(ds);
var dw=[];
var dO=this.__lK;
var du=this.__lJ;
var dN;

for(var dP=0;dP<=dO;dP++){dN=dL[dP]?dL[dP].offset:0;
dw[dP]=dM[dP].width+dN;
}var dE=this._getRowHeights();
var dG=this._getRowFlexOffsets(dt);
var dV=[];

for(var dC=0;dC<=du;dC++){dN=dG[dC]?dG[dC].offset:0;
dV[dC]=dE[dC].height+dN;
}var dW=0;

for(var dP=0;dP<=dO;dP++){var top=0;

for(var dC=0;dC<=du;dC++){var dJ=this.__lG[dC][dP];
if(!dJ){top+=dV[dC]+dB;
continue;
}var dx=dJ.getLayoutProperties();
if(dx.row!==dC||dx.column!==dP){top+=dV[dC]+dB;
continue;
}var dU=dv*(dx.colSpan-1);

for(var i=0;i<dx.colSpan;i++){dU+=dw[dP+i];
}var dK=dB*(dx.rowSpan-1);

for(var i=0;i<dx.rowSpan;i++){dK+=dV[dC+i];
}var dy=dJ.getSizeHint();
var dS=dJ.getMarginTop();
var dI=dJ.getMarginLeft();
var dF=dJ.getMarginBottom();
var dA=dJ.getMarginRight();
var dD=Math.max(dy.minWidth,Math.min(dU-dI-dA,dy.maxWidth));
var dT=Math.max(dy.minHeight,Math.min(dK-dS-dF,dy.maxHeight));
var dQ=this.getCellAlign(dC,dP);
var dR=dW+dH.computeHorizontalAlignOffset(dQ.hAlign,dD,dU,dI,dA);
var dz=top+dH.computeVerticalAlignOffset(dQ.vAlign,dT,dK,dS,dF);
dJ.renderLayout(dR,dz,dD,dT);
top+=dV[dC]+dB;
}dW+=dw[dP]+dv;
}},invalidateLayoutCache:function(){qx.ui.layout.Abstract.prototype.invalidateLayoutCache.call(this);
this.__lM=null;
this.__lL=null;
},_computeSizeHint:function(){if(this._invalidChildrenCache){this.__lN();
}var ec=this._getColWidths();
var ee=0,ef=0;

for(var i=0,l=ec.length;i<l;i++){var eg=ec[i];

if(this.getColumnFlex(i)>0){ee+=eg.minWidth;
}else{ee+=eg.width;
}ef+=eg.width;
}var eh=this._getRowHeights();
var ea=0,ed=0;

for(var i=0,l=eh.length;i<l;i++){var ei=eh[i];

if(this.getRowFlex(i)>0){ea+=ei.minHeight;
}else{ea+=ei.height;
}ed+=ei.height;
}var dY=this.getSpacingX()*(ec.length-1);
var dX=this.getSpacingY()*(eh.length-1);
var eb={minWidth:ee+dY,width:ef+dY,minHeight:ea+dX,height:ed+dX};
return eb;
}},destruct:function(){this.__lG=this.__lE=this.__lF=this.__lH=this.__lI=this.__lM=this.__lL=null;
}});
})();
(function(){var o="test",n="Info",m="scoville_admin.UserPage",l=" → ",k='scoville_admin/user.png',j="Permissions/Roles",i="scoville_admin/role.png",h="</b>",g="scoville_admin/user.png",f="<b>Settings for User: ",b='test',d="scoville_admin.scvRpc",c="execute",a="http://192.168.0.30/rpc/";
qx.Class.define(m,{extend:qx.ui.tabview.Page,construct:function(p,q){this.app=p;
qx.ui.tabview.Page.call(this);
this.setLabel(q.getParent().getParent().name+l+q.name);
this.setIcon(k);
this.tabs=p.tabview;
this.user=q;
this.buildGui();
this.setShowCloseButton(true);
this.tabs.add(this);
},members:{buildGui:function(){this.setLayout(new qx.ui.layout.VBox());
this.labelpasswd=new qx.ui.basic.Label().set({value:f+this.user.name+h,rich:true});
this.infobox=new qx.ui.groupbox.GroupBox(n,g);
this.infobox.setLayout(new qx.ui.layout.Basic());
this.permissionbox=new qx.ui.groupbox.GroupBox(j,i);
this.permissionbox.setLayout(new qx.ui.layout.Basic());
this.testbutton=new qx.ui.form.Button(b);
this.testbutton.addListener(c,function(e){var r=new qx.io.remote.Rpc(a,d);
r.setCrossDomain(true);
var s=function(t,u){if(u==null){alert("Result of call"+t);
}else{alert("Error: "+u);
}};
r.callAsync(s,o,o);
});
this.infobox.add(this.testbutton,{top:200,left:300});
this.add(this.labelpasswd);
this.add(this.infobox);
this.add(this.permissionbox);
},app:null,tabs:null,user:null}});
})();
(function(){var l="indexOf",k="addAfter",j="add",i="addBefore",h="_",g="addAt",f="hasChildren",e="removeAt",d="removeAll",c="getChildren",a="remove",b="qx.ui.core.MRemoteChildrenHandling";
qx.Mixin.define(b,{members:{__lP:function(m,n,o,p){var q=this.getChildrenContainer();

if(q===this){m=h+m;
}return (q[m])(n,o,p);
},getChildren:function(){return this.__lP(c);
},hasChildren:function(){return this.__lP(f);
},add:function(r,s){return this.__lP(j,r,s);
},remove:function(t){return this.__lP(a,t);
},removeAll:function(){return this.__lP(d);
},indexOf:function(u){return this.__lP(l,u);
},addAt:function(v,w,x){this.__lP(g,v,w,x);
},addBefore:function(y,z,A){this.__lP(i,y,z,A);
},addAfter:function(B,C,D){this.__lP(k,B,C,D);
},removeAt:function(E){return this.__lP(e,E);
}}});
})();
(function(){var a="qx.ui.core.MRemoteLayoutHandling";
qx.Mixin.define(a,{members:{setLayout:function(b){return this.getChildrenContainer().setLayout(b);
},getLayout:function(){return this.getChildrenContainer().getLayout();
}}});
})();
(function(){var p="Integer",o="_applyContentPadding",n="resetPaddingRight",m="setPaddingBottom",l="resetPaddingTop",k="qx.ui.core.MContentPadding",j="resetPaddingLeft",i="setPaddingTop",h="setPaddingRight",g="resetPaddingBottom",c="contentPaddingLeft",f="setPaddingLeft",e="contentPaddingTop",b="shorthand",a="contentPaddingRight",d="contentPaddingBottom";
qx.Mixin.define(k,{properties:{contentPaddingTop:{check:p,init:0,apply:o,themeable:true},contentPaddingRight:{check:p,init:0,apply:o,themeable:true},contentPaddingBottom:{check:p,init:0,apply:o,themeable:true},contentPaddingLeft:{check:p,init:0,apply:o,themeable:true},contentPadding:{group:[e,a,d,c],mode:b,themeable:true}},members:{__lQ:{contentPaddingTop:i,contentPaddingRight:h,contentPaddingBottom:m,contentPaddingLeft:f},__lR:{contentPaddingTop:l,contentPaddingRight:n,contentPaddingBottom:g,contentPaddingLeft:j},_applyContentPadding:function(q,r,name){var s=this._getContentPaddingTarget();

if(q==null){var t=this.__lR[name];
s[t]();
}else{var u=this.__lQ[name];
s[u](q);
}}}});
})();
(function(){var i="legend",h="frame",g="middle",f="top",d="resize",c="qx.ui.groupbox.GroupBox",b="groupbox",a="_applyLegendPosition";
qx.Class.define(c,{extend:qx.ui.core.Widget,include:[qx.ui.core.MRemoteChildrenHandling,qx.ui.core.MRemoteLayoutHandling,qx.ui.core.MContentPadding,qx.ui.form.MForm],implement:[qx.ui.form.IForm],construct:function(j,k){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.Canvas);
this._createChildControl(h);
this._createChildControl(i);
if(j!=null){this.setLegend(j);
}
if(k!=null){this.setIcon(k);
}},properties:{appearance:{refine:true,init:b},legendPosition:{check:[f,g],init:g,apply:a,themeable:true}},members:{_forwardStates:{invalid:true},_createChildControlImpl:function(l,m){var n;

switch(l){case h:n=new qx.ui.container.Composite();
this._add(n,{left:0,top:6,right:0,bottom:0});
break;
case i:n=new qx.ui.basic.Atom();
n.addListener(d,this._repositionFrame,this);
this._add(n,{left:0,right:0});
break;
}return n||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,l);
},_getContentPaddingTarget:function(){return this.getChildControl(h);
},_applyLegendPosition:function(e){if(this.getChildControl(i).getBounds()){this._repositionFrame();
}},_repositionFrame:function(){var p=this.getChildControl(i);
var o=this.getChildControl(h);
var q=p.getBounds().height;
if(this.getLegendPosition()==g){o.setLayoutProperties({"top":Math.round(q/2)});
}else if(this.getLegendPosition()==f){o.setLayoutProperties({"top":q});
}},getChildrenContainer:function(){return this.getChildControl(h);
},setLegend:function(r){var s=this.getChildControl(i);

if(r!==null){s.setLabel(r);
s.show();
}else{s.exclude();
}},getLegend:function(){return this.getChildControl(i).getLabel();
},setIcon:function(t){this.getChildControl(i).setIcon(t);
},getIcon:function(){this.getChildControl(i).getIcon();
}}});
})();
(function(){var a="qx.ui.layout.Basic";
qx.Class.define(a,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(b,c){var g=this._getLayoutChildren();
var d,f,e,h,top;
for(var i=0,l=g.length;i<l;i++){d=g[i];
f=d.getSizeHint();
e=d.getLayoutProperties();
h=(e.left||0)+d.getMarginLeft();
top=(e.top||0)+d.getMarginTop();
d.renderLayout(h,top,f.width,f.height);
}},_computeSizeHint:function(){var p=this._getLayoutChildren();
var m,r,n;
var q=0,o=0;
var j,k;
for(var i=0,l=p.length;i<l;i++){m=p[i];
r=m.getSizeHint();
n=m.getLayoutProperties();
j=r.width+(n.left||0)+m.getMarginLeft()+m.getMarginRight();
k=r.height+(n.top||0)+m.getMarginTop()+m.getMarginBottom();

if(j>q){q=j;
}
if(k>o){o=k;
}}return {width:q,height:o};
}}});
})();
(function(){var k="slider",j="splitter",i="horizontal",h="px",g="vertical",f="knob",d="mousedown",c="mouseout",b="Integer",a="height",D="mousemove",C="move",B="maxHeight",A="resize",z="width",w="_applyOrientation",v="_applyOffset",u="splitpane",t="qx.ui.splitpane.Pane",s="top",q="minHeight",r="mouseup",o="minWidth",p="appear",m="losecapture",n="left",l="maxWidth";
qx.Class.define(t,{extend:qx.ui.core.Widget,construct:function(E){qx.ui.core.Widget.call(this);
this.__ff=[];
if(E){this.setOrientation(E);
}else{this.initOrientation();
}this.__jU.addListener(d,this._onMouseDown,this);
this.__jU.addListener(r,this._onMouseUp,this);
this.__jU.addListener(D,this._onMouseMove,this);
this.__jU.addListener(c,this._onMouseOut,this);
this.__jU.addListener(m,this._onMouseUp,this);
},properties:{appearance:{refine:true,init:u},offset:{check:b,init:6,apply:v},orientation:{init:i,check:[i,g],apply:w}},members:{__lS:null,__lT:false,__lU:null,__lV:null,__lW:null,__lX:null,__lY:null,__ff:null,__jU:null,_createChildControlImpl:function(F,G){var H;

switch(F){case k:H=new qx.ui.splitpane.Slider(this);
H.exclude();
this._add(H,{type:F});
break;
case j:H=new qx.ui.splitpane.Splitter(this);
this._add(H,{type:F});
H.addListener(C,this.__ma,this);
break;
}return H||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,F);
},__ma:function(e){this.__mc(e.getData());
},__mb:function(I){this.__jU=new qx.ui.splitpane.Blocker(I);
this.getContentElement().add(this.__jU);
var J=this.getChildControl(j);
var K=J.getWidth();

if(!K){J.addListenerOnce(p,function(){this.__mc();
},this);
}J.addListener(A,function(e){var L=e.getData();

if(L.height==0||L.width==0){this.__jU.hide();
}else{this.__jU.show();
}},this);
},getBlocker:function(){return this.__jU;
},_applyOrientation:function(M,N){var O=this.getChildControl(k);
var R=this.getChildControl(j);
this.__lW=M===i;

if(!this.__jU){this.__mb(M);
}this.__jU.setOrientation(M);
var Q=this._getLayout();

if(Q){Q.dispose();
}var P=M===g?new qx.ui.splitpane.VLayout:new qx.ui.splitpane.HLayout;
this._setLayout(P);
R.removeState(N);
R.addState(M);
R.getChildControl(f).removeState(N);
R.getChildControl(f).addState(M);
O.removeState(N);
O.addState(M);
qx.ui.core.queue.Manager.flush();
this.__mc();
},_applyOffset:function(S,T){this.__mc();
},__mc:function(U){var V=this.getChildControl(j);
var ba=this.getOffset();
var bb=V.getBounds();
var Y=V.getContainerElement().getDomElement();
if(!Y){return;
}if(this.__lW){var X=null;

if(U){X=U.width;
}else if(bb){X=bb.width;
}var bc=U&&U.left;

if(X){if(isNaN(bc)){bc=qx.bom.element.Location.getPosition(Y).left;
}this.__jU.setWidth(ba,X);
this.__jU.setLeft(ba,bc);
}}else{var W=null;

if(U){W=U.height;
}else if(bb){W=bb.height;
}var top=U&&U.top;

if(W){if(isNaN(top)){top=qx.bom.element.Location.getPosition(Y).top;
}this.__jU.setHeight(ba,W);
this.__jU.setTop(ba,top);
}}},add:function(bd,be){if(be==null){this._add(bd);
}else{this._add(bd,{flex:be});
}this.__ff.push(bd);
},remove:function(bf){this._remove(bf);
qx.lang.Array.remove(this.__ff,bf);
},getChildren:function(){return this.__ff;
},_onMouseDown:function(e){if(!e.isLeftPressed()){return;
}var bg=this.getChildControl(j);
var bi=bg.getContainerLocation();
var bh=this.getContentLocation();
this.__lS=this.__lW?e.getDocumentLeft()-bi.left+bh.left:e.getDocumentTop()-bi.top+bh.top;
var bk=this.getChildControl(k);
var bj=bg.getBounds();
bk.setUserBounds(bj.left,bj.top,bj.width,bj.height);
bk.setZIndex(bg.getZIndex()+1);
bk.show();
this.__lT=true;
this.__jU.capture();
e.stop();
},_onMouseMove:function(e){this._setLastMousePosition(e.getDocumentLeft(),e.getDocumentTop());
if(this.__lT){this.__md();
var bl=this.getChildControl(k);
var bm=this.__lX;

if(this.__lW){bl.setDomLeft(bm);
this.__jU.setStyle(n,(bm-this.getOffset())+h);
}else{bl.setDomTop(bm);
this.__jU.setStyle(s,(bm-this.getOffset())+h);
}e.stop();
}},_onMouseOut:function(e){this._setLastMousePosition(e.getDocumentLeft(),e.getDocumentTop());
},_onMouseUp:function(e){if(!this.__lT){return;
}this._finalizeSizes();
var bn=this.getChildControl(k);
bn.exclude();
this.__lT=false;
this.releaseCapture();
e.stop();
},_finalizeSizes:function(){var br=this.__lX;
var bo=this.__lY;

if(br==null){return;
}var bt=this._getChildren();
var bs=bt[2];
var bp=bt[3];
var bq=bs.getLayoutProperties().flex;
var bu=bp.getLayoutProperties().flex;
if((bq!=0)&&(bu!=0)){bs.setLayoutProperties({flex:br});
bp.setLayoutProperties({flex:bo});
}else{if(this.__lW){bs.setWidth(br);
bp.setWidth(bo);
}else{bs.setHeight(br);
bp.setHeight(bo);
}}},__md:function(){if(this.__lW){var bx=o,bE=z,by=l,bC=this.__lU;
}else{var bx=q,bE=a,by=B,bC=this.__lV;
}var bD=this._getChildren();
var bv=bD[2].getSizeHint();
var bA=bD[3].getSizeHint();
var bB=bD[2].getBounds()[bE]+bD[3].getBounds()[bE];
var bz=bC-this.__lS;
var bw=bB-bz;
if(bz<bv[bx]){bw-=bv[bx]-bz;
bz=bv[bx];
}else if(bw<bA[bx]){bz-=bA[bx]-bw;
bw=bA[bx];
}if(bz>bv[by]){bw+=bz-bv[by];
bz=bv[by];
}else if(bw>bA[by]){bz+=bw-bA[by];
bw=bA[by];
}this.__lX=bz;
this.__lY=bw;
},_isActiveDragSession:function(){return this.__lT;
},_setLastMousePosition:function(x,y){this.__lU=x;
this.__lV=y;
}},destruct:function(){this.__ff=null;
}});
})();
(function(){var a="qx.ui.splitpane.Slider";
qx.Class.define(a,{extend:qx.ui.core.Widget,properties:{allowShrinkX:{refine:true,init:false},allowShrinkY:{refine:true,init:false}}});
})();
(function(){var e="center",d="knob",c="middle",b="qx.ui.splitpane.Splitter",a="vertical";
qx.Class.define(b,{extend:qx.ui.core.Widget,construct:function(f){qx.ui.core.Widget.call(this);
if(f.getOrientation()==a){this._setLayout(new qx.ui.layout.HBox(0,e));
this._getLayout().setAlignY(c);
}else{this._setLayout(new qx.ui.layout.VBox(0,c));
this._getLayout().setAlignX(e);
}this._createChildControl(d);
},properties:{allowShrinkX:{refine:true,init:false},allowShrinkY:{refine:true,init:false}},members:{_createChildControlImpl:function(g,h){var i;

switch(g){case d:i=new qx.ui.basic.Image;
this._add(i);
break;
}return i||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,g);
}}});
})();
(function(){var u="px",t="horizontal",s="top",r="height",q="width",p="100%",o="left",n="cursor",m="mshtml",l="engine.name",e="repeat",k="_applyOrientation",h="url(",c="qx.ui.splitpane.Blocker",b=")",g="col-resize",f="row-resize",i="div",a="vertical",j="qx/static/blank.gif",d="absolute";
qx.Class.define(c,{extend:qx.html.Element,construct:function(v){var w={position:d,zIndex:11};
if((qx.core.Environment.get(l)==m)){w.backgroundImage=h+qx.util.ResourceManager.getInstance().toUri(j)+b;
w.backgroundRepeat=e;
}qx.html.Element.call(this,i,w);
if(v){this.setOrientation(v);
}else{this.initOrientation();
}},properties:{orientation:{init:t,check:[t,a],apply:k}},members:{_applyOrientation:function(x,y){if(x==t){this.setStyle(r,p);
this.setStyle(n,g);
this.setStyle(s,null);
}else{this.setStyle(q,p);
this.setStyle(o,null);
this.setStyle(n,f);
}},setWidth:function(z,A){var B=A+2*z;
this.setStyle(q,B+u);
},setHeight:function(C,D){var E=D+2*C;
this.setStyle(r,E+u);
},setLeft:function(F,G){var H=G-F;
this.setStyle(o,H+u);
},setTop:function(I,J){var top=J-I;
this.setStyle(s,top+u);
}}});
})();
(function(){var c="slider",b="splitter",a="qx.ui.splitpane.VLayout";
qx.Class.define(a,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(d,e){var v=this._getLayoutChildren();
var length=v.length;
var r,u;
var g,f,p,h;

for(var i=0;i<length;i++){r=v[i];
u=r.getLayoutProperties().type;

if(u===b){f=r;
}else if(u===c){p=r;
}else if(!g){g=r;
}else{h=r;
}}
if(g&&h){var x=g.getLayoutProperties().flex;
var k=h.getLayoutProperties().flex;

if(x==null){x=1;
}
if(k==null){k=1;
}var w=g.getSizeHint();
var n=f.getSizeHint();
var o=h.getSizeHint();
var j=w.height;
var s=n.height;
var t=o.height;

if(x>0&&k>0){var l=x+k;
var m=e-s;
var j=Math.round((m/l)*x);
var t=m-j;
var q=qx.ui.layout.Util.arrangeIdeals(w.minHeight,j,w.maxHeight,o.minHeight,t,o.maxHeight);
j=q.begin;
t=q.end;
}else if(x>0){j=e-s-t;

if(j<w.minHeight){j=w.minHeight;
}
if(j>w.maxHeight){j=w.maxHeight;
}}else if(k>0){t=e-j-s;

if(t<o.minHeight){t=o.minHeight;
}
if(t>o.maxHeight){t=o.maxHeight;
}}g.renderLayout(0,0,d,j);
f.renderLayout(0,j,d,s);
h.renderLayout(0,j+s,d,t);
}else{f.renderLayout(0,0,0,0);
if(g){g.renderLayout(0,0,d,e);
}else if(h){h.renderLayout(0,0,d,e);
}}},_computeSizeHint:function(){var H=this._getLayoutChildren();
var length=H.length;
var A,z,G;
var B=0,D=0,C=0;
var E=0,F=0,y=0;

for(var i=0;i<length;i++){A=H[i];
G=A.getLayoutProperties();
if(G.type===c){continue;
}z=A.getSizeHint();
B+=z.minHeight;
D+=z.height;
C+=z.maxHeight;

if(z.minWidth>E){E=z.minWidth;
}
if(z.width>F){F=z.width;
}
if(z.maxWidth>y){y=z.maxWidth;
}}return {minHeight:B,height:D,maxHeight:C,minWidth:E,width:F,maxWidth:y};
}}});
})();
(function(){var c="slider",b="splitter",a="qx.ui.splitpane.HLayout";
qx.Class.define(a,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(d,e){var v=this._getLayoutChildren();
var length=v.length;
var s,u;
var g,f,p,h;

for(var i=0;i<length;i++){s=v[i];
u=s.getLayoutProperties().type;

if(u===b){f=s;
}else if(u===c){p=s;
}else if(!g){g=s;
}else{h=s;
}}
if(g&&h){var x=g.getLayoutProperties().flex;
var j=h.getLayoutProperties().flex;

if(x==null){x=1;
}
if(j==null){j=1;
}var w=g.getSizeHint();
var m=f.getSizeHint();
var o=h.getSizeHint();
var t=w.width;
var r=m.width;
var q=o.width;

if(x>0&&j>0){var k=x+j;
var l=d-r;
var t=Math.round((l/k)*x);
var q=l-t;
var n=qx.ui.layout.Util.arrangeIdeals(w.minWidth,t,w.maxWidth,o.minWidth,q,o.maxWidth);
t=n.begin;
q=n.end;
}else if(x>0){t=d-r-q;

if(t<w.minWidth){t=w.minWidth;
}
if(t>w.maxWidth){t=w.maxWidth;
}}else if(j>0){q=d-t-r;

if(q<o.minWidth){q=o.minWidth;
}
if(q>o.maxWidth){q=o.maxWidth;
}}g.renderLayout(0,0,t,e);
f.renderLayout(t,0,r,e);
h.renderLayout(t+r,0,q,e);
}else{f.renderLayout(0,0,0,0);
if(g){g.renderLayout(0,0,d,e);
}else if(h){h.renderLayout(0,0,d,e);
}}},_computeSizeHint:function(){var H=this._getLayoutChildren();
var length=H.length;
var A,z,G;
var E=0,F=0,y=0;
var B=0,D=0,C=0;

for(var i=0;i<length;i++){A=H[i];
G=A.getLayoutProperties();
if(G.type===c){continue;
}z=A.getSizeHint();
E+=z.minWidth;
F+=z.width;
y+=z.maxWidth;

if(z.minHeight>B){B=z.minHeight;
}
if(z.height>D){D=z.height;
}
if(z.maxHeight>C){C=z.maxHeight;
}}return {minWidth:E,width:F,maxWidth:y,minHeight:B,height:D,maxHeight:C};
}}});
})();
(function(){var m="pane",k="lastTab",j="bar",h="page",g="firstTab",f="close",d="right",c="bottom",b="button",a="changeSelection",B="top",A="left",z="qx.event.type.Data",y="barRight",x="beforeChangeSelection",w="close-button",v="__mf",u="tabview",t="vertical",s="_applyBarPosition",q="barLeft",r="horizontal",o="qx.ui.tabview.TabView",p="barTop",n="barBottom";
qx.Class.define(o,{extend:qx.ui.core.Widget,implement:qx.ui.core.ISingleSelection,include:[qx.ui.core.MContentPadding],construct:function(C){qx.ui.core.Widget.call(this);
this.__me={top:p,right:y,bottom:n,left:q};
this._createChildControl(j);
this._createChildControl(m);
var D=this.__mf=new qx.ui.form.RadioGroup;
D.setWrap(false);
D.addListener(a,this._onChangeSelection,this);
if(C!=null){this.setBarPosition(C);
}else{this.initBarPosition();
}},events:{"changeSelection":z},properties:{appearance:{refine:true,init:u},barPosition:{check:[A,d,B,c],init:B,apply:s}},members:{__mf:null,_createChildControlImpl:function(E,F){var G;

switch(E){case j:G=new qx.ui.container.SlideBar();
G.setZIndex(10);
this._add(G);
break;
case m:G=new qx.ui.container.Stack;
G.setZIndex(5);
this._add(G,{flex:1});
break;
}return G||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,E);
},_getContentPaddingTarget:function(){return this.getChildControl(m);
},add:function(H){var I=H.getButton();
var J=this.getChildControl(j);
var L=this.getChildControl(m);
H.exclude();
J.add(I);
L.add(H);
this.__mf.add(I);
H.addState(this.__me[this.getBarPosition()]);
H.addState(k);
var K=this.getChildren();

if(K[0]==H){H.addState(g);
}else{K[K.length-2].removeState(k);
}H.addListener(f,this._onPageClose,this);
},addAt:function(M,N){var Q=this.getChildren();

if(!(N==null)&&N>Q.length){throw new Error("Index should be less than : "+Q.length);
}
if(N==null){N=Q.length;
}var O=M.getButton();
var P=this.getChildControl(j);
var R=this.getChildControl(m);
M.exclude();
P.addAt(O,N);
R.addAt(M,N);
this.__mf.add(O);
M.addState(this.__me[this.getBarPosition()]);
Q=this.getChildren();

if(N==Q.length-1){M.addState(k);
}
if(Q[0]==M){M.addState(g);
}else{Q[Q.length-2].removeState(k);
}M.addListener(f,this._onPageClose,this);
},remove:function(S){var X=this.getChildControl(m);
var V=this.getChildControl(j);
var U=S.getButton();
var W=X.getChildren();
if(this.getSelection()[0]==S){var T=W.indexOf(S);

if(T==0){if(W[1]){this.setSelection([W[1]]);
}else{this.resetSelection();
}}else{this.setSelection([W[T-1]]);
}}V.remove(U);
X.remove(S);
this.__mf.remove(U);
S.removeState(this.__me[this.getBarPosition()]);
if(S.hasState(g)){S.removeState(g);

if(W[0]){W[0].addState(g);
}}
if(S.hasState(k)){S.removeState(k);

if(W.length>0){W[W.length-1].addState(k);
}}S.removeListener(f,this._onPageClose,this);
},getChildren:function(){return this.getChildControl(m).getChildren();
},indexOf:function(Y){return this.getChildControl(m).indexOf(Y);
},__me:null,_applyBarPosition:function(ba,bb){var bc=this.getChildControl(j);
var bh=ba==A||ba==d;
var bf=ba==d||ba==c;
var bg=bh?qx.ui.layout.HBox:qx.ui.layout.VBox;
var bj=this._getLayout();

if(bj&&bj instanceof bg){}else{this._setLayout(bj=new bg);
}bj.setReversed(bf);
bc.setOrientation(bh?t:r);
var bi=this.getChildren();
if(bb){var bd=this.__me[bb];
bc.removeState(bd);
for(var i=0,l=bi.length;i<l;i++){bi[i].removeState(bd);
}}
if(ba){var be=this.__me[ba];
bc.addState(be);
for(var i=0,l=bi.length;i<l;i++){bi[i].addState(be);
}}},getSelection:function(){var bk=this.__mf.getSelection();
var bl=[];

for(var i=0;i<bk.length;i++){bl.push(bk[i].getUserData(h));
}return bl;
},setSelection:function(bm){var bn=[];

for(var i=0;i<bm.length;i++){bn.push(bm[i].getChildControl(b));
}this.__mf.setSelection(bn);
},resetSelection:function(){this.__mf.resetSelection();
},isSelected:function(bo){var bp=bo.getChildControl(b);
return this.__mf.isSelected(bp);
},isSelectionEmpty:function(){return this.__mf.isSelectionEmpty();
},getSelectables:function(bq){var br=this.__mf.getSelectables(bq);
var bs=[];

for(var i=0;i<br.length;i++){bs.push(br[i].getUserData(h));
}return bs;
},_onChangeSelection:function(e){var bx=this.getChildControl(m);
var bu=e.getData()[0];
var bw=e.getOldData()[0];
var bt=[];
var bv=[];

if(bu){bt=[bu.getUserData(h)];
bx.setSelection(bt);
bu.focus();
this.scrollChildIntoView(bu,null,null,false);
}else{bx.resetSelection();
}
if(bw){bv=[bw.getUserData(h)];
}this.fireDataEvent(a,bt,bv);
},_onBeforeChangeSelection:function(e){if(!this.fireNonBubblingEvent(x,qx.event.type.Event,[false,true])){e.preventDefault();
}},_onRadioChangeSelection:function(e){var by=e.getData()[0];

if(by){this.setSelection([by.getUserData(h)]);
}else{this.resetSelection();
}},_onPageClose:function(e){var bA=e.getTarget();
var bz=bA.getButton().getChildControl(w);
bz.reset();
this.remove(bA);
}},destruct:function(){this._disposeObjects(v);
this.__me=null;
}});
})();
(function(){var u="horizontal",t="scrollpane",s="button-backward",r="button-forward",q="vertical",p="content",o="execute",n="qx.ui.container.SlideBar",m="scrollY",l="engine.name",d="removeChildWidget",k="scrollX",h="_applyOrientation",c="mousewheel",b="gecko",g="x",f="y",i="Integer",a="slidebar",j="update";
qx.Class.define(n,{extend:qx.ui.core.Widget,include:[qx.ui.core.MRemoteChildrenHandling,qx.ui.core.MRemoteLayoutHandling],construct:function(v){qx.ui.core.Widget.call(this);
var w=this.getChildControl(t);
this._add(w,{flex:1});

if(v!=null){this.setOrientation(v);
}else{this.initOrientation();
}this.addListener(c,this._onMouseWheel,this);
},properties:{appearance:{refine:true,init:a},orientation:{check:[u,q],init:u,apply:h},scrollStep:{check:i,init:15,themeable:true}},members:{getChildrenContainer:function(){return this.getChildControl(p);
},_createChildControlImpl:function(x,y){var z;

switch(x){case r:z=new qx.ui.form.RepeatButton;
z.addListener(o,this._onExecuteForward,this);
z.setFocusable(false);
this._addAt(z,2);
break;
case s:z=new qx.ui.form.RepeatButton;
z.addListener(o,this._onExecuteBackward,this);
z.setFocusable(false);
this._addAt(z,0);
break;
case p:z=new qx.ui.container.Composite();
if(qx.core.Environment.get(l)==b){z.addListener(d,this._onRemoveChild,this);
}this.getChildControl(t).add(z);
break;
case t:z=new qx.ui.core.scroll.ScrollPane();
z.addListener(j,this._onResize,this);
z.addListener(k,this._onScroll,this);
z.addListener(m,this._onScroll,this);
break;
}return z||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,x);
},_forwardStates:{barLeft:true,barTop:true,barRight:true,barBottom:true},scrollBy:function(A){var B=this.getChildControl(t);

if(this.getOrientation()===u){B.scrollByX(A);
}else{B.scrollByY(A);
}},scrollTo:function(C){var D=this.getChildControl(t);

if(this.getOrientation()===u){D.scrollToX(C);
}else{D.scrollToY(C);
}},_applyEnabled:function(E,F,name){qx.ui.core.Widget.prototype._applyEnabled.call(this,E,F,name);
this._updateArrowsEnabled();
},_applyOrientation:function(G,H){var K=[this.getLayout(),this._getLayout()];
var J=this.getChildControl(r);
var I=this.getChildControl(s);
if(H==q){J.removeState(q);
I.removeState(q);
J.addState(u);
I.addState(u);
}else if(H==u){J.removeState(u);
I.removeState(u);
J.addState(q);
I.addState(q);
}
if(G==u){this._setLayout(new qx.ui.layout.HBox());
this.setLayout(new qx.ui.layout.HBox());
}else{this._setLayout(new qx.ui.layout.VBox());
this.setLayout(new qx.ui.layout.VBox());
}
if(K[0]){K[0].dispose();
}
if(K[1]){K[1].dispose();
}},_onMouseWheel:function(e){var L=0;

if(this.getOrientation()===u){L=e.getWheelDelta(g);
}else{L=e.getWheelDelta(f);
}this.scrollBy(L*this.getScrollStep());
e.stop();
},_onScroll:function(){this._updateArrowsEnabled();
},_onResize:function(e){var content=this.getChildControl(t).getChildren()[0];

if(!content){return;
}var M=this.getInnerSize();
var O=content.getBounds();
var N=(this.getOrientation()===u)?O.width>M.width:O.height>M.height;

if(N){this._showArrows();
this._updateArrowsEnabled();
}else{this._hideArrows();
}},_onExecuteBackward:function(){this.scrollBy(-this.getScrollStep());
},_onExecuteForward:function(){this.scrollBy(this.getScrollStep());
},_onRemoveChild:function(){qx.event.Timer.once(function(){this.scrollBy(this.getChildControl(t).getScrollX());
},this,50);
},_updateArrowsEnabled:function(){if(!this.getEnabled()){this.getChildControl(s).setEnabled(false);
this.getChildControl(r).setEnabled(false);
return;
}var Q=this.getChildControl(t);

if(this.getOrientation()===u){var P=Q.getScrollX();
var R=Q.getScrollMaxX();
}else{var P=Q.getScrollY();
var R=Q.getScrollMaxY();
}this.getChildControl(s).setEnabled(P>0);
this.getChildControl(r).setEnabled(P<R);
},_showArrows:function(){this._showChildControl(r);
this._showChildControl(s);
},_hideArrows:function(){this._excludeChildControl(r);
this._excludeChildControl(s);
this.scrollTo(0);
}}});
})();
(function(){var n="pressed",m="abandoned",l="Integer",k="hovered",j="qx.event.type.Event",i="Enter",h="Space",g="press",f="qx.ui.form.RepeatButton",d="release",a="interval",c="__je",b="execute";
qx.Class.define(f,{extend:qx.ui.form.Button,construct:function(o,p){qx.ui.form.Button.call(this,o,p);
this.__je=new qx.event.AcceleratingTimer();
this.__je.addListener(a,this._onInterval,this);
},events:{"execute":j,"press":j,"release":j},properties:{interval:{check:l,init:100},firstInterval:{check:l,init:500},minTimer:{check:l,init:20},timerDecrease:{check:l,init:2}},members:{__mg:null,__je:null,press:function(){if(this.isEnabled()){if(!this.hasState(n)){this.__mh();
}this.removeState(m);
this.addState(n);
}},release:function(q){if(!this.isEnabled()){return;
}if(this.hasState(n)){if(!this.__mg){this.execute();
}}this.removeState(n);
this.removeState(m);
this.__mi();
},_applyEnabled:function(r,s){qx.ui.form.Button.prototype._applyEnabled.call(this,r,s);

if(!r){this.removeState(n);
this.removeState(m);
this.__mi();
}},_onMouseOver:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}
if(this.hasState(m)){this.removeState(m);
this.addState(n);
this.__je.start();
}this.addState(k);
},_onMouseOut:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}this.removeState(k);

if(this.hasState(n)){this.removeState(n);
this.addState(m);
this.__je.stop();
}},_onMouseDown:function(e){if(!e.isLeftPressed()){return;
}this.capture();
this.__mh();
e.stopPropagation();
},_onMouseUp:function(e){this.releaseCapture();

if(!this.hasState(m)){this.addState(k);

if(this.hasState(n)&&!this.__mg){this.execute();
}}this.__mi();
e.stopPropagation();
},_onKeyUp:function(e){switch(e.getKeyIdentifier()){case i:case h:if(this.hasState(n)){if(!this.__mg){this.execute();
}this.removeState(n);
this.removeState(m);
e.stopPropagation();
this.__mi();
}}},_onKeyDown:function(e){switch(e.getKeyIdentifier()){case i:case h:this.removeState(m);
this.addState(n);
e.stopPropagation();
this.__mh();
}},_onInterval:function(e){this.__mg=true;
this.fireEvent(b);
},__mh:function(){this.fireEvent(g);
this.__mg=false;
this.__je.set({interval:this.getInterval(),firstInterval:this.getFirstInterval(),minimum:this.getMinTimer(),decrease:this.getTimerDecrease()}).start();
this.removeState(m);
this.addState(n);
},__mi:function(){this.fireEvent(d);
this.__je.stop();
this.removeState(m);
this.removeState(n);
}},destruct:function(){this._disposeObjects(c);
}});
})();
(function(){var e="Integer",d="interval",c="__je",b="qx.event.type.Event",a="qx.event.AcceleratingTimer";
qx.Class.define(a,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__je=new qx.event.Timer(this.getInterval());
this.__je.addListener(d,this._onInterval,this);
},events:{"interval":b},properties:{interval:{check:e,init:100},firstInterval:{check:e,init:500},minimum:{check:e,init:20},decrease:{check:e,init:2}},members:{__je:null,__mj:null,start:function(){this.__je.setInterval(this.getFirstInterval());
this.__je.start();
},stop:function(){this.__je.stop();
this.__mj=null;
},_onInterval:function(){this.__je.stop();

if(this.__mj==null){this.__mj=this.getInterval();
}this.__mj=Math.max(this.getMinimum(),this.__mj-this.getDecrease());
this.__je.setInterval(this.__mj);
this.__je.start();
this.fireEvent(d);
}},destruct:function(){this._disposeObjects(c);
}});
})();
(function(){var d="_applyDynamic",c="changeSelection",b="Boolean",a="qx.ui.container.Stack";
qx.Class.define(a,{extend:qx.ui.core.Widget,implement:qx.ui.core.ISingleSelection,include:[qx.ui.core.MSingleSelectionHandling,qx.ui.core.MChildrenHandling],construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.Grow);
this.addListener(c,this.__lC,this);
},properties:{dynamic:{check:b,init:false,apply:d}},members:{_applyDynamic:function(f){var h=this._getChildren();
var g=this.getSelection()[0];
var j;

for(var i=0,l=h.length;i<l;i++){j=h[i];

if(j!=g){if(f){h[i].exclude();
}else{h[i].hide();
}}}},_getItems:function(){return this.getChildren();
},_isAllowEmptySelection:function(){return true;
},_isItemSelectable:function(k){return true;
},__lC:function(e){var m=e.getOldData()[0];
var n=e.getData()[0];

if(m){if(this.isDynamic()){m.exclude();
}else{m.hide();
}}
if(n){n.show();
}},_afterAddChild:function(o){var p=this.getSelection()[0];

if(!p){this.setSelection([o]);
}else if(p!==o){if(this.isDynamic()){o.exclude();
}else{o.hide();
}}},_afterRemoveChild:function(q){if(this.getSelection()[0]===q){var r=this._getChildren()[0];

if(r){this.setSelection([r]);
}else{this.resetSelection();
}}},previous:function(){var u=this.getSelection()[0];
var s=this._indexOf(u)-1;
var v=this._getChildren();

if(s<0){s=v.length-1;
}var t=v[s];
this.setSelection([t]);
},next:function(){var x=this.getSelection()[0];
var w=this._indexOf(x)+1;
var y=this._getChildren();
var z=y[w]||y[0];
this.setSelection([z]);
}}});
})();
(function(){var w="visible",v="excluded",u="resize",t="qx.event.type.Data",s="both",r="qx.ui.menu.Menu",q="_applySpacing",p="showItem",o="Boolean",n="icon",d="label",m="qx.ui.core.Widget",h="_applyOverflowIndicator",c="_applyOverflowHandling",b="changeShow",g="Integer",f="qx.ui.toolbar.ToolBar",j="hideItem",a="toolbar",k="changeOpenMenu";
qx.Class.define(f,{extend:qx.ui.core.Widget,include:qx.ui.core.MChildrenHandling,construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.HBox());
this.__mk=[];
this.__ml=[];
},properties:{appearance:{refine:true,init:a},openMenu:{check:r,event:k,nullable:true},show:{init:s,check:[s,d,n],inheritable:true,event:b},spacing:{nullable:true,check:g,themeable:true,apply:q},overflowIndicator:{check:m,nullable:true,apply:h},overflowHandling:{init:false,check:o,apply:c}},events:{"hideItem":t,"showItem":t},members:{__mk:null,__ml:null,_computeSizeHint:function(){var z=qx.ui.core.Widget.prototype._computeSizeHint.call(this);

if(true&&this.getOverflowHandling()){var x=0;
var y=this.getOverflowIndicator();

if(y){x=y.getSizeHint().width+this.getSpacing();
}z.minWidth=x;
}return z;
},_onResize:function(e){this._recalculateOverflow(e.getData().width);
},_recalculateOverflow:function(A,B){if(!this.getOverflowHandling()){return;
}B=B||this.getSizeHint().width;
var C=this.getOverflowIndicator();
var I=0;

if(C){I=C.getSizeHint().width;
}
if(A==undefined&&this.getBounds()!=null){A=this.getBounds().width;
}if(A==undefined){return ;
}if(A<B){do{var J=this._getNextToHide();
if(!J){return;
}var L=J.getMarginLeft()+J.getMarginRight();
L=Math.max(L,this.getSpacing());
var G=J.getSizeHint().width+L;
this.__mn(J);
B-=G;
if(C&&C.getVisibility()!=w){C.setVisibility(w);
B+=I;
var E=C.getMarginLeft()+C.getMarginRight();
B+=Math.max(E,this.getSpacing());
}}while(B>A);
}else if(this.__mk.length>0){do{var M=this.__mk[0];
if(M){var L=M.getMarginLeft()+M.getMarginRight();
L=Math.max(L,this.getSpacing());
if(M.getDecoratorElement()==null){M.syncAppearance();
M.invalidateLayoutCache();
}var F=M.getSizeHint().width;
var K=false;
if(this.__mk.length==1&&I>0){var D=L-this.getSpacing();
var H=B-I+F+D;
K=A>H;
}if(A>B+F+L||K){this.__mm(M);
B+=F;
if(C&&this.__mk.length==0){C.setVisibility(v);
}}else{return;
}}}while(A>=B&&this.__mk.length>0);
}},__mm:function(N){N.setVisibility(w);
this.__mk.shift();
this.fireDataEvent(p,N);
},__mn:function(O){if(!O){return;
}this.__mk.unshift(O);
O.setVisibility(v);
this.fireDataEvent(j,O);
},_getNextToHide:function(){for(var i=this.__ml.length-1;i>=0;i--){var P=this.__ml[i];
if(P&&P.getVisibility&&P.getVisibility()==w){return P;
}}var Q=this._getChildren();

for(var i=Q.length-1;i>=0;i--){var R=Q[i];
if(R==this.getOverflowIndicator()){continue;
}if(R.getVisibility&&R.getVisibility()==w){return R;
}}},setRemovePriority:function(S,T,U){if(!U&&this.__ml[T]!=undefined){throw new Error("Priority already in use!");
}this.__ml[T]=S;
},_applyOverflowHandling:function(V,W){this.invalidateLayoutCache();
var parent=this.getLayoutParent();

if(parent){parent.invalidateLayoutCache();
}var Y=this.getBounds();

if(Y&&Y.width){this._recalculateOverflow(Y.width);
}if(V){this.addListener(u,this._onResize,this);
}else{this.removeListener(u,this._onResize,this);
var X=this.getOverflowIndicator();

if(X){X.setVisibility(v);
}for(var i=0;i<this.__mk.length;i++){this.__mk[i].setVisibility(w);
}this.__mk=[];
}},_applyOverflowIndicator:function(ba,bb){if(bb){this._remove(bb);
}
if(ba){if(this._indexOf(ba)==-1){throw new Error("Widget must be child of the toolbar.");
}ba.setVisibility(v);
}},__mo:false,_setAllowMenuOpenHover:function(bc){this.__mo=bc;
},_isAllowMenuOpenHover:function(){return this.__mo;
},_applySpacing:function(bd,be){var bf=this._getLayout();
bd==null?bf.resetSpacing():bf.setSpacing(bd);
},_add:function(bg,bh){qx.ui.core.Widget.prototype._add.call(this,bg,bh);
var bi=this.getSizeHint().width+bg.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bi);
},_addAt:function(bj,bk,bl){qx.ui.core.Widget.prototype._addAt.call(this,bj,bk,bl);
var bm=this.getSizeHint().width+bj.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bm);
},_addBefore:function(bn,bo,bp){qx.ui.core.Widget.prototype._addBefore.call(this,bn,bo,bp);
var bq=this.getSizeHint().width+bn.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bq);
},_addAfter:function(br,bs,bt){qx.ui.core.Widget.prototype._addAfter.call(this,br,bs,bt);
var bu=this.getSizeHint().width+br.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bu);
},_remove:function(bv){qx.ui.core.Widget.prototype._remove.call(this,bv);
var bw=this.getSizeHint().width-bv.getSizeHint().width-2*this.getSpacing();
this._recalculateOverflow(null,bw);
},_removeAt:function(bx){var bz=this._getChildren()[bx];
qx.ui.core.Widget.prototype._removeAt.call(this,bx);
var by=this.getSizeHint().width-bz.getSizeHint().width-2*this.getSpacing();
this._recalculateOverflow(null,by);
},_removeAll:function(){qx.ui.core.Widget.prototype._removeAll.call(this);
this._recalculateOverflow(null,0);
},addSpacer:function(){var bA=new qx.ui.core.Spacer;
this._add(bA,{flex:1});
return bA;
},addSeparator:function(){this.add(new qx.ui.toolbar.Separator);
},getMenuButtons:function(){var bC=this.getChildren();
var bB=[];
var bD;

for(var i=0,l=bC.length;i<l;i++){bD=bC[i];

if(bD instanceof qx.ui.menubar.Button){bB.push(bD);
}else if(bD instanceof qx.ui.toolbar.Part){bB.push.apply(bB,bD.getMenuButtons());
}}return bB;
}},destruct:function(){if(this.hasListener(u)){this.removeListener(u,this._onResize,this);
}}});
})();
(function(){var b="toolbar-separator",a="qx.ui.toolbar.Separator";
qx.Class.define(a,{extend:qx.ui.core.Widget,properties:{appearance:{refine:true,init:b},anonymous:{refine:true,init:true},width:{refine:true,init:0},height:{refine:true,init:0}}});
})();
(function(){var m="pressed",l="hovered",k="changeVisibility",j="qx.ui.menu.Menu",i="submenu",h="Enter",g="abandoned",f="contextmenu",d="changeMenu",c="qx.ui.form.MenuButton",a="left",b="_applyMenu";
qx.Class.define(c,{extend:qx.ui.form.Button,construct:function(n,o,p){qx.ui.form.Button.call(this,n,o);
if(p!=null){this.setMenu(p);
}},properties:{menu:{check:j,nullable:true,apply:b,event:d}},members:{_applyMenu:function(q,r){if(r){r.removeListener(k,this._onMenuChange,this);
r.resetOpener();
}
if(q){q.addListener(k,this._onMenuChange,this);
q.setOpener(this);
q.removeState(i);
q.removeState(f);
}},open:function(s){var t=this.getMenu();

if(t){qx.ui.menu.Manager.getInstance().hideAll();
t.setOpener(this);
t.open();
if(s){var u=t.getSelectables()[0];

if(u){t.setSelectedButton(u);
}}}},_onMenuChange:function(e){var v=this.getMenu();

if(v.isVisible()){this.addState(m);
}else{this.removeState(m);
}},_onMouseDown:function(e){qx.ui.form.Button.prototype._onMouseDown.call(this,e);
if(e.getButton()!=a){return;
}var w=this.getMenu();

if(w){if(!w.isVisible()){this.open();
}else{w.exclude();
}e.stopPropagation();
}},_onMouseUp:function(e){qx.ui.form.Button.prototype._onMouseUp.call(this,e);
e.stopPropagation();
},_onMouseOver:function(e){this.addState(l);
},_onMouseOut:function(e){this.removeState(l);
},_onKeyDown:function(e){switch(e.getKeyIdentifier()){case h:this.removeState(g);
this.addState(m);
var x=this.getMenu();

if(x){if(!x.isVisible()){this.open();
}else{x.exclude();
}}e.stopPropagation();
}},_onKeyUp:function(e){}}});
})();
(function(){var u="keypress",t="interval",s="keydown",r="mousedown",q="keyup",p="__jB",o="__mq",n="blur",m="Enter",l="__mp",d="Up",k="Escape",h="event.touch",c="qx.ui.menu.Manager",b="Left",g="Down",f="Right",j="singleton",a="Space";
qx.Class.define(c,{type:j,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__jB=[];
var v=document.body;
var w=qx.event.Registration;
w.addListener(window.document.documentElement,r,this._onMouseDown,this,true);
w.addListener(v,s,this._onKeyUpDown,this,true);
w.addListener(v,q,this._onKeyUpDown,this,true);
w.addListener(v,u,this._onKeyPress,this,true);
if(!qx.core.Environment.get(h)){qx.bom.Element.addListener(window,n,this.hideAll,this);
}this.__mp=new qx.event.Timer;
this.__mp.addListener(t,this._onOpenInterval,this);
this.__mq=new qx.event.Timer;
this.__mq.addListener(t,this._onCloseInterval,this);
},members:{__mr:null,__ms:null,__mp:null,__mq:null,__jB:null,_getChild:function(x,y,z,A){var B=x.getChildren();
var length=B.length;
var C;

for(var i=y;i<length&&i>=0;i+=z){C=B[i];

if(C.isEnabled()&&!C.isAnonymous()){return C;
}}
if(A){i=i==length?0:length-1;

for(;i!=y;i+=z){C=B[i];

if(C.isEnabled()&&!C.isAnonymous()){return C;
}}}return null;
},_isInMenu:function(D){while(D){if(D instanceof qx.ui.menu.Menu){return true;
}D=D.getLayoutParent();
}return false;
},_getMenuButton:function(E){while(E){if(E instanceof qx.ui.menu.AbstractButton){return E;
}E=E.getLayoutParent();
}return null;
},add:function(F){var G=this.__jB;
G.push(F);
F.setZIndex(1e6+G.length);
},remove:function(H){var I=this.__jB;

if(I){qx.lang.Array.remove(I,H);
}},hideAll:function(){var J=this.__jB;

if(J){for(var i=J.length-1;i>=0;i--){J[i].exclude();
}}},getActiveMenu:function(){var K=this.__jB;
return K.length>0?K[K.length-1]:null;
},scheduleOpen:function(L){this.cancelClose(L);
if(L.isVisible()){if(this.__mr){this.cancelOpen(this.__mr);
}}else if(this.__mr!=L){this.__mr=L;
this.__mp.restartWith(L.getOpenInterval());
}},scheduleClose:function(M){this.cancelOpen(M);
if(!M.isVisible()){if(this.__ms){this.cancelClose(this.__ms);
}}else if(this.__ms!=M){this.__ms=M;
this.__mq.restartWith(M.getCloseInterval());
}},cancelOpen:function(N){if(this.__mr==N){this.__mp.stop();
this.__mr=null;
}},cancelClose:function(O){if(this.__ms==O){this.__mq.stop();
this.__ms=null;
}},_onOpenInterval:function(e){this.__mp.stop();
this.__mr.open();
this.__mr=null;
},_onCloseInterval:function(e){this.__mq.stop();
this.__ms.exclude();
this.__ms=null;
},_onMouseDown:function(e){var P=e.getTarget();
P=qx.ui.core.Widget.getWidgetByElement(P,true);
if(P==null){this.hideAll();
return;
}if(P.getMenu&&P.getMenu()&&P.getMenu().isVisible()){return;
}if(this.__jB.length>0&&!this._isInMenu(P)){this.hideAll();
}},__mt:{"Enter":1,"Space":1},__mu:{"Escape":1,"Up":1,"Down":1,"Left":1,"Right":1},_onKeyUpDown:function(e){var Q=this.getActiveMenu();

if(!Q){return;
}var R=e.getKeyIdentifier();

if(this.__mu[R]||(this.__mt[R]&&Q.getSelectedButton())){e.stopPropagation();
}},_onKeyPress:function(e){var S=this.getActiveMenu();

if(!S){return;
}var T=e.getKeyIdentifier();
var V=this.__mu[T];
var U=this.__mt[T];

if(V){switch(T){case d:this._onKeyPressUp(S);
break;
case g:this._onKeyPressDown(S);
break;
case b:this._onKeyPressLeft(S);
break;
case f:this._onKeyPressRight(S);
break;
case k:this.hideAll();
break;
}e.stopPropagation();
e.preventDefault();
}else if(U){var W=S.getSelectedButton();

if(W){switch(T){case m:this._onKeyPressEnter(S,W,e);
break;
case a:this._onKeyPressSpace(S,W,e);
break;
}e.stopPropagation();
e.preventDefault();
}}},_onKeyPressUp:function(X){var Y=X.getSelectedButton();
var ba=X.getChildren();
var bc=Y?X.indexOf(Y)-1:ba.length-1;
var bb=this._getChild(X,bc,-1,true);
if(bb){X.setSelectedButton(bb);
}else{X.resetSelectedButton();
}},_onKeyPressDown:function(bd){var be=bd.getSelectedButton();
var bg=be?bd.indexOf(be)+1:0;
var bf=this._getChild(bd,bg,1,true);
if(bf){bd.setSelectedButton(bf);
}else{bd.resetSelectedButton();
}},_onKeyPressLeft:function(bh){var bm=bh.getOpener();

if(!bm){return;
}if(bm instanceof qx.ui.menu.AbstractButton){var bj=bm.getLayoutParent();
bj.resetOpenedButton();
bj.setSelectedButton(bm);
}else if(bm instanceof qx.ui.menubar.Button){var bl=bm.getMenuBar().getMenuButtons();
var bi=bl.indexOf(bm);
if(bi===-1){return;
}var bn=null;
var length=bl.length;

for(var i=1;i<=length;i++){var bk=bl[(bi-i+length)%length];

if(bk.isEnabled()){bn=bk;
break;
}}
if(bn&&bn!=bm){bn.open(true);
}}},_onKeyPressRight:function(bo){var bq=bo.getSelectedButton();
if(bq){var bp=bq.getMenu();

if(bp){bo.setOpenedButton(bq);
var bw=this._getChild(bp,0,1);

if(bw){bp.setSelectedButton(bw);
}return;
}}else if(!bo.getOpenedButton()){var bw=this._getChild(bo,0,1);

if(bw){bo.setSelectedButton(bw);

if(bw.getMenu()){bo.setOpenedButton(bw);
}return;
}}var bu=bo.getOpener();
if(bu instanceof qx.ui.menu.Button&&bq){while(bu){bu=bu.getLayoutParent();

if(bu instanceof qx.ui.menu.Menu){bu=bu.getOpener();

if(bu instanceof qx.ui.menubar.Button){break;
}}else{break;
}}
if(!bu){return;
}}if(bu instanceof qx.ui.menubar.Button){var bt=bu.getMenuBar().getMenuButtons();
var br=bt.indexOf(bu);
if(br===-1){return;
}var bv=null;
var length=bt.length;

for(var i=1;i<=length;i++){var bs=bt[(br+i)%length];

if(bs.isEnabled()){bv=bs;
break;
}}
if(bv&&bv!=bu){bv.open(true);
}}},_onKeyPressEnter:function(bx,by,e){if(by.hasListener(u)){var bz=e.clone();
bz.setBubbles(false);
bz.setTarget(by);
by.dispatchEvent(bz);
}this.hideAll();
},_onKeyPressSpace:function(bA,bB,e){if(bB.hasListener(u)){var bC=e.clone();
bC.setBubbles(false);
bC.setTarget(bB);
bB.dispatchEvent(bC);
}}},destruct:function(){var bE=qx.event.Registration;
var bD=document.body;
bE.removeListener(window.document.documentElement,r,this._onMouseDown,this,true);
bE.removeListener(bD,s,this._onKeyUpDown,this,true);
bE.removeListener(bD,q,this._onKeyUpDown,this,true);
bE.removeListener(bD,u,this._onKeyPress,this,true);
this._disposeObjects(l,o);
this._disposeArray(p);
}});
})();
(function(){var l="slidebar",k="Integer",j="resize",h="qx.ui.core.Widget",g="selected",f="visible",d="Boolean",c="mouseout",b="excluded",a="menu",A="_applySelectedButton",z="_applyOpenInterval",y="_applySpacingY",x="_blocker",w="_applyCloseInterval",v="_applyBlockerColor",u="_applyIconColumnWidth",t="mouseover",s="qx.ui.menu.Menu",r="Color",p="Number",q="_applyOpenedButton",n="_applySpacingX",o="_applyBlockerOpacity",m="_applyArrowColumnWidth";
qx.Class.define(s,{extend:qx.ui.core.Widget,include:[qx.ui.core.MPlacement,qx.ui.core.MRemoteChildrenHandling],construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.menu.Layout);
var B=this.getApplicationRoot();
B.add(this);
this.addListener(t,this._onMouseOver);
this.addListener(c,this._onMouseOut);
this.addListener(j,this._onResize,this);
B.addListener(j,this._onResize,this);
this._blocker=new qx.ui.core.Blocker(B);
this.initVisibility();
this.initKeepFocus();
this.initKeepActive();
},properties:{appearance:{refine:true,init:a},allowGrowX:{refine:true,init:false},allowGrowY:{refine:true,init:false},visibility:{refine:true,init:b},keepFocus:{refine:true,init:true},keepActive:{refine:true,init:true},spacingX:{check:k,apply:n,init:0,themeable:true},spacingY:{check:k,apply:y,init:0,themeable:true},iconColumnWidth:{check:k,init:0,themeable:true,apply:u},arrowColumnWidth:{check:k,init:0,themeable:true,apply:m},blockerColor:{check:r,init:null,nullable:true,apply:v,themeable:true},blockerOpacity:{check:p,init:1,apply:o,themeable:true},selectedButton:{check:h,nullable:true,apply:A},openedButton:{check:h,nullable:true,apply:q},opener:{check:h,nullable:true},openInterval:{check:k,themeable:true,init:250,apply:z},closeInterval:{check:k,themeable:true,init:250,apply:w},blockBackground:{check:d,themeable:true,init:false}},members:{__mv:null,__mw:null,_blocker:null,open:function(){if(this.getOpener()!=null){this.placeToWidget(this.getOpener());
this.__my();
this.show();
this._placementTarget=this.getOpener();
}else{this.warn("The menu instance needs a configured 'opener' widget!");
}},openAtMouse:function(e){this.placeToMouse(e);
this.__my();
this.show();
this._placementTarget={left:e.getDocumentLeft(),top:e.getDocumentTop()};
},openAtPoint:function(C){this.placeToPoint(C);
this.__my();
this.show();
this._placementTarget=C;
},addSeparator:function(){this.add(new qx.ui.menu.Separator);
},getColumnSizes:function(){return this._getMenuLayout().getColumnSizes();
},getSelectables:function(){var D=[];
var E=this.getChildren();

for(var i=0;i<E.length;i++){if(E[i].isEnabled()){D.push(E[i]);
}}return D;
},_applyIconColumnWidth:function(F,G){this._getMenuLayout().setIconColumnWidth(F);
},_applyArrowColumnWidth:function(H,I){this._getMenuLayout().setArrowColumnWidth(H);
},_applySpacingX:function(J,K){this._getMenuLayout().setColumnSpacing(J);
},_applySpacingY:function(L,M){this._getMenuLayout().setSpacing(L);
},_applyVisibility:function(N,O){qx.ui.core.Widget.prototype._applyVisibility.call(this,N,O);
var P=qx.ui.menu.Manager.getInstance();

if(N===f){P.add(this);
var Q=this.getParentMenu();

if(Q){Q.setOpenedButton(this.getOpener());
}}else if(O===f){P.remove(this);
var Q=this.getParentMenu();

if(Q&&Q.getOpenedButton()==this.getOpener()){Q.resetOpenedButton();
}this.resetOpenedButton();
this.resetSelectedButton();
}this.__mx();
},__mx:function(){if(this.isVisible()){if(this.getBlockBackground()){var R=this.getZIndex();
this._blocker.blockContent(R-1);
}}else{if(this._blocker.isContentBlocked()){this._blocker.unblockContent();
}}},getParentMenu:function(){var S=this.getOpener();

if(!S||!(S instanceof qx.ui.menu.AbstractButton)){return null;
}
if(S&&S.getContextMenu()===this){return null;
}
while(S&&!(S instanceof qx.ui.menu.Menu)){S=S.getLayoutParent();
}return S;
},_applySelectedButton:function(T,U){if(U){U.removeState(g);
}
if(T){T.addState(g);
}},_applyOpenedButton:function(V,W){if(W&&W.getMenu()){W.getMenu().exclude();
}
if(V){V.getMenu().open();
}},_applyBlockerColor:function(X,Y){this._blocker.setColor(X);
},_applyBlockerOpacity:function(ba,bb){this._blocker.setOpacity(ba);
},getChildrenContainer:function(){return this.getChildControl(l,true)||this;
},_createChildControlImpl:function(bc,bd){var be;

switch(bc){case l:var be=new qx.ui.menu.MenuSlideBar();
var bg=this._getLayout();
this._setLayout(new qx.ui.layout.Grow());
var bf=be.getLayout();
be.setLayout(bg);
bf.dispose();
var bh=qx.lang.Array.clone(this.getChildren());

for(var i=0;i<bh.length;i++){be.add(bh[i]);
}this.removeListener(j,this._onResize,this);
be.getChildrenContainer().addListener(j,this._onResize,this);
this._add(be);
break;
}return be||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,bc);
},_getMenuLayout:function(){if(this.hasChildControl(l)){return this.getChildControl(l).getChildrenContainer().getLayout();
}else{return this._getLayout();
}},_getMenuBounds:function(){if(this.hasChildControl(l)){return this.getChildControl(l).getChildrenContainer().getBounds();
}else{return this.getBounds();
}},_computePlacementSize:function(){return this._getMenuBounds();
},__my:function(){var bj=this._getMenuBounds();

if(!bj){this.addListenerOnce(j,this.__my,this);
return;
}var bi=this.getLayoutParent().getBounds().height;
var top=this.getLayoutProperties().top;
var bk=this.getLayoutProperties().left;
if(top<0){this._assertSlideBar(function(){this.setHeight(bj.height+top);
this.moveTo(bk,0);
});
}else if(top+bj.height>bi){this._assertSlideBar(function(){this.setHeight(bi-top);
});
}else{this.setHeight(null);
}},_assertSlideBar:function(bl){if(this.hasChildControl(l)){return bl.call(this);
}this.__mw=bl;
qx.ui.core.queue.Widget.add(this);
},syncWidget:function(){this.getChildControl(l);

if(this.__mw){this.__mw.call(this);
delete this.__mw;
}},_onResize:function(){if(this.isVisible()){var bm=this._placementTarget;

if(!bm){return;
}else if(bm instanceof qx.ui.core.Widget){this.placeToWidget(bm);
}else if(bm.top!==undefined){this.placeToPoint(bm);
}else{throw new Error("Unknown target: "+bm);
}this.__my();
}},_onMouseOver:function(e){var bo=qx.ui.menu.Manager.getInstance();
bo.cancelClose(this);
var bp=e.getTarget();

if(bp.isEnabled()&&bp instanceof qx.ui.menu.AbstractButton){this.setSelectedButton(bp);
var bn=bp.getMenu&&bp.getMenu();

if(bn){bn.setOpener(bp);
bo.scheduleOpen(bn);
this.__mv=bn;
}else{var bq=this.getOpenedButton();

if(bq){bo.scheduleClose(bq.getMenu());
}
if(this.__mv){bo.cancelOpen(this.__mv);
this.__mv=null;
}}}else if(!this.getOpenedButton()){this.resetSelectedButton();
}},_onMouseOut:function(e){var br=qx.ui.menu.Manager.getInstance();
if(!qx.ui.core.Widget.contains(this,e.getRelatedTarget())){var bs=this.getOpenedButton();
bs?this.setSelectedButton(bs):this.resetSelectedButton();
if(bs){br.cancelClose(bs.getMenu());
}if(this.__mv){br.cancelOpen(this.__mv);
}}}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){qx.ui.menu.Manager.getInstance().remove(this);
}this.getApplicationRoot().removeListener(j,this._onResize,this);
this._placementTarget=null;
this._disposeObjects(x);
}});
})();
(function(){var c="Integer",b="_applyLayoutChange",a="qx.ui.menu.Layout";
qx.Class.define(a,{extend:qx.ui.layout.VBox,properties:{columnSpacing:{check:c,init:0,apply:b},spanColumn:{check:c,init:1,nullable:true,apply:b},iconColumnWidth:{check:c,init:0,themeable:true,apply:b},arrowColumnWidth:{check:c,init:0,themeable:true,apply:b}},members:{__mz:null,_computeSizeHint:function(){var q=this._getLayoutChildren();
var o,g,j;
var e=this.getSpanColumn();
var h=this.__mz=[0,0,0,0];
var m=this.getColumnSpacing();
var k=0;
var f=0;
for(var i=0,l=q.length;i<l;i++){o=q[i];

if(o.isAnonymous()){continue;
}g=o.getChildrenSizes();

for(var n=0;n<g.length;n++){if(e!=null&&n==e&&g[e+1]==0){k=Math.max(k,g[n]);
}else{h[n]=Math.max(h[n],g[n]);
}}var d=q[i].getInsets();
f=Math.max(f,d.left+d.right);
}if(e!=null&&h[e]+m+h[e+1]<k){h[e]=k-h[e+1]-m;
}if(k==0){j=m*2;
}else{j=m*3;
}if(h[0]==0){h[0]=this.getIconColumnWidth();
}if(h[3]==0){h[3]=this.getArrowColumnWidth();
}var p=qx.ui.layout.VBox.prototype._computeSizeHint.call(this).height;
return {minHeight:p,height:p,width:qx.lang.Array.sum(h)+f+j};
},getColumnSizes:function(){return this.__mz||null;
}},destruct:function(){this.__mz=null;
}});
})();
(function(){var b="menu-separator",a="qx.ui.menu.Separator";
qx.Class.define(a,{extend:qx.ui.core.Widget,properties:{appearance:{refine:true,init:b},anonymous:{refine:true,init:true}}});
})();
(function(){var s="icon",r="label",q="arrow",p="shortcut",o="changeLocale",n="qx.dynlocale",m="submenu",l="String",k="changeCommand",j="qx.ui.menu.Menu",c="qx.ui.menu.AbstractButton",i="keypress",g="",b="_applyIcon",a="mouseup",f="abstract",d="_applyLabel",h="_applyMenu";
qx.Class.define(c,{extend:qx.ui.core.Widget,include:[qx.ui.core.MExecutable],implement:[qx.ui.form.IExecutable],type:f,construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.menu.ButtonLayout);
this.addListener(a,this._onMouseUp);
this.addListener(i,this._onKeyPress);
this.addListener(k,this._onChangeCommand,this);
},properties:{blockToolTip:{refine:true,init:true},label:{check:l,apply:d,nullable:true},menu:{check:j,apply:h,nullable:true,dereference:true},icon:{check:l,apply:b,themeable:true,nullable:true}},members:{_createChildControlImpl:function(t,u){var v;

switch(t){case s:v=new qx.ui.basic.Image;
v.setAnonymous(true);
this._add(v,{column:0});
break;
case r:v=new qx.ui.basic.Label;
v.setAnonymous(true);
this._add(v,{column:1});
break;
case p:v=new qx.ui.basic.Label;
v.setAnonymous(true);
this._add(v,{column:2});
break;
case q:v=new qx.ui.basic.Image;
v.setAnonymous(true);
this._add(v,{column:3});
break;
}return v||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,t);
},_forwardStates:{selected:1},getChildrenSizes:function(){var w=0,x=0,y=0,C=0;

if(this._isChildControlVisible(s)){var D=this.getChildControl(s);
w=D.getMarginLeft()+D.getSizeHint().width+D.getMarginRight();
}
if(this._isChildControlVisible(r)){var A=this.getChildControl(r);
x=A.getMarginLeft()+A.getSizeHint().width+A.getMarginRight();
}
if(this._isChildControlVisible(p)){var z=this.getChildControl(p);
y=z.getMarginLeft()+z.getSizeHint().width+z.getMarginRight();
}
if(this._isChildControlVisible(q)){var B=this.getChildControl(q);
C=B.getMarginLeft()+B.getSizeHint().width+B.getMarginRight();
}return [w,x,y,C];
},_onMouseUp:function(e){},_onKeyPress:function(e){},_onChangeCommand:function(e){var G=e.getData();
if(G==null){return;
}
if(qx.core.Environment.get(n)){var E=e.getOldData();

if(!E){qx.locale.Manager.getInstance().addListener(o,this._onChangeLocale,this);
}
if(!G){qx.locale.Manager.getInstance().removeListener(o,this._onChangeLocale,this);
}}var F=G!=null?G.toString():g;
this.getChildControl(p).setValue(F);
},_onChangeLocale:qx.core.Environment.select(n,{"true":function(e){var H=this.getCommand();

if(H!=null){this.getChildControl(p).setValue(H.toString());
}},"false":null}),_applyIcon:function(I,J){if(I){this._showChildControl(s).setSource(I);
}else{this._excludeChildControl(s);
}},_applyLabel:function(K,L){if(K){this._showChildControl(r).setValue(K);
}else{this._excludeChildControl(r);
}},_applyMenu:function(M,N){if(N){N.resetOpener();
N.removeState(m);
}
if(M){this._showChildControl(q);
M.setOpener(this);
M.addState(m);
}else{this._excludeChildControl(q);
}}},destruct:function(){this.removeListener(k,this._onChangeCommand,this);

if(this.getMenu()){if(!qx.core.ObjectRegistry.inShutDown){this.getMenu().destroy();
}}
if(qx.core.Environment.get(n)){qx.locale.Manager.getInstance().removeListener(o,this._onChangeLocale,this);
}}});
})();
(function(){var c="middle",b="qx.ui.menu.ButtonLayout",a="left";
qx.Class.define(b,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(d,e){var q=this._getLayoutChildren();
var p;
var g;
var h=[];

for(var i=0,l=q.length;i<l;i++){p=q[i];
g=p.getLayoutProperties().column;
h[g]=p;
}var o=this.__mA(q[0]);
var r=o.getColumnSizes();
var k=o.getSpacingX();
var j=qx.lang.Array.sum(r)+k*(r.length-1);

if(j<d){r[1]+=d-j;
}var s=0,top=0;
var m=qx.ui.layout.Util;

for(var i=0,l=r.length;i<l;i++){p=h[i];

if(p){var f=p.getSizeHint();
var top=m.computeVerticalAlignOffset(p.getAlignY()||c,f.height,e,0,0);
var n=m.computeHorizontalAlignOffset(p.getAlignX()||a,f.width,r[i],p.getMarginLeft(),p.getMarginRight());
p.renderLayout(s+n,top,f.width,f.height);
}s+=r[i]+k;
}},__mA:function(t){while(!(t instanceof qx.ui.menu.Menu)){t=t.getLayoutParent();
}return t;
},_computeSizeHint:function(){var w=this._getLayoutChildren();
var v=0;
var x=0;

for(var i=0,l=w.length;i<l;i++){var u=w[i].getSizeHint();
x+=u.width;
v=Math.max(v,u.height);
}return {width:x,height:v};
}}});
})();
(function(){var f="execute",e="button-backward",d="vertical",c="button-forward",b="menu-slidebar",a="qx.ui.menu.MenuSlideBar";
qx.Class.define(a,{extend:qx.ui.container.SlideBar,construct:function(){qx.ui.container.SlideBar.call(this,d);
},properties:{appearance:{refine:true,init:b}},members:{_createChildControlImpl:function(g,h){var i;

switch(g){case c:i=new qx.ui.form.HoverButton();
i.addListener(f,this._onExecuteForward,this);
this._addAt(i,2);
break;
case e:i=new qx.ui.form.HoverButton();
i.addListener(f,this._onExecuteBackward,this);
this._addAt(i,0);
break;
}return i||qx.ui.container.SlideBar.prototype._createChildControlImpl.call(this,g);
}}});
})();
(function(){var i="Integer",h="hovered",g="hover-button",f="interval",d="mouseover",c="mouseout",b="__je",a="qx.ui.form.HoverButton";
qx.Class.define(a,{extend:qx.ui.basic.Atom,include:[qx.ui.core.MExecutable],implement:[qx.ui.form.IExecutable],construct:function(j,k){qx.ui.basic.Atom.call(this,j,k);
this.addListener(d,this._onMouseOver,this);
this.addListener(c,this._onMouseOut,this);
this.__je=new qx.event.AcceleratingTimer();
this.__je.addListener(f,this._onInterval,this);
},properties:{appearance:{refine:true,init:g},interval:{check:i,init:80},firstInterval:{check:i,init:200},minTimer:{check:i,init:20},timerDecrease:{check:i,init:2}},members:{__je:null,_onMouseOver:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}this.__je.set({interval:this.getInterval(),firstInterval:this.getFirstInterval(),minimum:this.getMinTimer(),decrease:this.getTimerDecrease()}).start();
this.addState(h);
},_onMouseOut:function(e){this.__je.stop();
this.removeState(h);

if(!this.isEnabled()||e.getTarget()!==this){return;
}},_onInterval:function(){if(this.isEnabled()){this.execute();
}else{this.__je.stop();
}}},destruct:function(){this._disposeObjects(b);
}});
})();
(function(){var h="pressed",g="hovered",f="inherit",d="qx.ui.menubar.Button",c="keydown",b="menubar-button",a="keyup";
qx.Class.define(d,{extend:qx.ui.form.MenuButton,construct:function(i,j,k){qx.ui.form.MenuButton.call(this,i,j,k);
this.removeListener(c,this._onKeyDown);
this.removeListener(a,this._onKeyUp);
},properties:{appearance:{refine:true,init:b},show:{refine:true,init:f},focusable:{refine:true,init:false}},members:{getMenuBar:function(){var parent=this;

while(parent){if(parent instanceof qx.ui.toolbar.ToolBar){return parent;
}parent=parent.getLayoutParent();
}return null;
},open:function(l){qx.ui.form.MenuButton.prototype.open.call(this,l);
var menubar=this.getMenuBar();
menubar._setAllowMenuOpenHover(true);
},_onMenuChange:function(e){var m=this.getMenu();
var menubar=this.getMenuBar();

if(m.isVisible()){this.addState(h);
if(menubar){menubar.setOpenMenu(m);
}}else{this.removeState(h);
if(menubar&&menubar.getOpenMenu()==m){menubar.resetOpenMenu();
menubar._setAllowMenuOpenHover(false);
}}},_onMouseUp:function(e){qx.ui.form.MenuButton.prototype._onMouseUp.call(this,e);
var n=this.getMenu();

if(n&&n.isVisible()&&!this.hasState(h)){this.addState(h);
}},_onMouseOver:function(e){this.addState(g);
if(this.getMenu()){var menubar=this.getMenuBar();

if(menubar._isAllowMenuOpenHover()){qx.ui.menu.Manager.getInstance().hideAll();
menubar._setAllowMenuOpenHover(true);
if(this.isEnabled()){this.open();
}}}}}});
})();
(function(){var b="qx.ui.menu.Button",a="menu-button";
qx.Class.define(b,{extend:qx.ui.menu.AbstractButton,construct:function(c,d,f,g){qx.ui.menu.AbstractButton.call(this);
if(c!=null){this.setLabel(c);
}
if(d!=null){this.setIcon(d);
}
if(f!=null){this.setCommand(f);
}
if(g!=null){this.setMenu(g);
}},properties:{appearance:{refine:true,init:a}},members:{_onMouseUp:function(e){if(e.isLeftPressed()){this.execute();
if(this.getMenu()){return;
}}else{if(this.getContextMenu()){return;
}}qx.ui.menu.Manager.getInstance().hideAll();
},_onKeyPress:function(e){this.execute();
}}});
})();
(function(){var p="middle",o="left",n="right",m="container",k="handle",j="both",h="Integer",g="qx.ui.toolbar.Part",f="icon",e="label",b="syncAppearance",d="changeShow",c="_applySpacing",a="toolbar/part";
qx.Class.define(g,{extend:qx.ui.core.Widget,include:[qx.ui.core.MRemoteChildrenHandling],construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.HBox);
this._createChildControl(k);
},properties:{appearance:{refine:true,init:a},show:{init:j,check:[j,e,f],inheritable:true,event:d},spacing:{nullable:true,check:h,themeable:true,apply:c}},members:{_createChildControlImpl:function(q,r){var s;

switch(q){case k:s=new qx.ui.basic.Image();
s.setAlignY(p);
this._add(s);
break;
case m:s=new qx.ui.toolbar.PartContainer();
s.addListener(b,this.__mB,this);
this._add(s);
break;
}return s||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,q);
},getChildrenContainer:function(){return this.getChildControl(m);
},_applySpacing:function(t,u){var v=this.getChildControl(m).getLayout();
t==null?v.resetSpacing():v.setSpacing(t);
},__mB:function(){var w=this.getChildrenContainer().getChildren();

for(var i=0;i<w.length;i++){if(i==0&&i!=w.length-1){w[i].addState(o);
w[i].removeState(n);
w[i].removeState(p);
}else if(i==w.length-1&&i!=0){w[i].addState(n);
w[i].removeState(o);
w[i].removeState(p);
}else if(i==0&&i==w.length-1){w[i].removeState(o);
w[i].removeState(p);
w[i].removeState(n);
}else{w[i].addState(p);
w[i].removeState(n);
w[i].removeState(o);
}}},addSeparator:function(){this.add(new qx.ui.toolbar.Separator);
},getMenuButtons:function(){var y=this.getChildren();
var x=[];
var z;

for(var i=0,l=y.length;i<l;i++){z=y[i];

if(z instanceof qx.ui.menubar.Button){x.push(z);
}}return x;
}}});
})();
(function(){var f="both",e="toolbar/part/container",d="icon",c="changeShow",b="qx.ui.toolbar.PartContainer",a="label";
qx.Class.define(b,{extend:qx.ui.container.Composite,construct:function(){qx.ui.container.Composite.call(this);
this._setLayout(new qx.ui.layout.HBox);
},properties:{appearance:{refine:true,init:e},show:{init:f,check:[f,a,d],inheritable:true,event:c}}});
})();
(function(){var b="qx.ui.menubar.MenuBar",a="menubar";
qx.Class.define(b,{extend:qx.ui.toolbar.ToolBar,properties:{appearance:{refine:true,init:a}}});
})();
(function(){var o="one",n="single",m="selected",k="additive",j="multi",h="os.name",g="osx",f="under",d="PageUp",c="Left",O="lead",N="Down",M="Up",L="Boolean",K="PageDown",J="anchor",I="End",H="Home",G="Right",F="right",v="click",w="above",t="left",u="Escape",r="A",s="Space",p="_applyMode",q="__mE",x="interval",y="changeSelection",A="qx.event.type.Data",z="quick",C="key",B="abstract",E="drag",D="qx.ui.core.selection.Abstract";
qx.Class.define(D,{type:B,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__eM={};
},events:{"changeSelection":A},properties:{mode:{check:[n,j,k,o],init:n,apply:p},drag:{check:L,init:false},quick:{check:L,init:false}},members:{__mC:0,__mD:0,__mE:null,__mF:null,__mG:null,__mH:null,__mI:null,__mJ:null,__mK:null,__mL:null,__mM:null,__mN:null,__mO:null,__mP:null,__mQ:null,__mR:null,__mS:null,__eM:null,__mT:null,__mU:null,_userInteraction:false,__mV:null,getSelectionContext:function(){return this.__mR;
},selectAll:function(){var P=this.getMode();

if(P==n||P==o){throw new Error("Can not select all items in selection mode: "+P);
}this._selectAllItems();
this._fireChange();
},selectItem:function(Q){this._setSelectedItem(Q);
var R=this.getMode();

if(R!==n&&R!==o){this._setLeadItem(Q);
this._setAnchorItem(Q);
}this._scrollItemIntoView(Q);
this._fireChange();
},addItem:function(S){var T=this.getMode();

if(T===n||T===o){this._setSelectedItem(S);
}else{if(this._getAnchorItem()==null){this._setAnchorItem(S);
}this._setLeadItem(S);
this._addToSelection(S);
}this._scrollItemIntoView(S);
this._fireChange();
},removeItem:function(U){this._removeFromSelection(U);

if(this.getMode()===o&&this.isSelectionEmpty()){var V=this._applyDefaultSelection();
if(V==U){return;
}}
if(this.getLeadItem()==U){this._setLeadItem(null);
}
if(this._getAnchorItem()==U){this._setAnchorItem(null);
}this._fireChange();
},selectItemRange:function(W,X){var Y=this.getMode();

if(Y==n||Y==o){throw new Error("Can not select multiple items in selection mode: "+Y);
}this._selectItemRange(W,X);
this._setAnchorItem(W);
this._setLeadItem(X);
this._scrollItemIntoView(X);
this._fireChange();
},clearSelection:function(){if(this.getMode()==o){var ba=this._applyDefaultSelection(true);

if(ba!=null){return;
}}this._clearSelection();
this._setLeadItem(null);
this._setAnchorItem(null);
this._fireChange();
},replaceSelection:function(bb){var bc=this.getMode();

if(bc==o||bc===n){if(bb.length>1){throw new Error("Could not select more than one items in mode: "+bc+"!");
}
if(bb.length==1){this.selectItem(bb[0]);
}else{this.clearSelection();
}return;
}else{this._replaceMultiSelection(bb);
}},getSelectedItem:function(){var bd=this.getMode();

if(bd===n||bd===o){var be=this._getSelectedItem();
return be!=undefined?be:null;
}throw new Error("The method getSelectedItem() is only supported in 'single' and 'one' selection mode!");
},getSelection:function(){return qx.lang.Object.getValues(this.__eM);
},getSortedSelection:function(){var bg=this.getSelectables();
var bf=qx.lang.Object.getValues(this.__eM);
bf.sort(function(a,b){return bg.indexOf(a)-bg.indexOf(b);
});
return bf;
},isItemSelected:function(bh){var bi=this._selectableToHashCode(bh);
return this.__eM[bi]!==undefined;
},isSelectionEmpty:function(){return qx.lang.Object.isEmpty(this.__eM);
},invertSelection:function(){var bk=this.getMode();

if(bk===n||bk===o){throw new Error("The method invertSelection() is only supported in 'multi' and 'additive' selection mode!");
}var bj=this.getSelectables();

for(var i=0;i<bj.length;i++){this._toggleInSelection(bj[i]);
}this._fireChange();
},_setLeadItem:function(bl){var bm=this.__mS;

if(bm!==null){this._styleSelectable(bm,O,false);
}
if(bl!==null){this._styleSelectable(bl,O,true);
}this.__mS=bl;
},getLeadItem:function(){return this.__mS!==null?this.__mS:null;
},_setAnchorItem:function(bn){var bo=this.__mT;

if(bo!=null){this._styleSelectable(bo,J,false);
}
if(bn!=null){this._styleSelectable(bn,J,true);
}this.__mT=bn;
},_getAnchorItem:function(){return this.__mT!==null?this.__mT:null;
},_isSelectable:function(bp){throw new Error("Abstract method call: _isSelectable()");
},_getSelectableFromMouseEvent:function(event){var bq=event.getTarget();
if(bq&&this._isSelectable(bq)){return bq;
}return null;
},_selectableToHashCode:function(br){throw new Error("Abstract method call: _selectableToHashCode()");
},_styleSelectable:function(bs,bt,bu){throw new Error("Abstract method call: _styleSelectable()");
},_capture:function(){throw new Error("Abstract method call: _capture()");
},_releaseCapture:function(){throw new Error("Abstract method call: _releaseCapture()");
},_getLocation:function(){throw new Error("Abstract method call: _getLocation()");
},_getDimension:function(){throw new Error("Abstract method call: _getDimension()");
},_getSelectableLocationX:function(bv){throw new Error("Abstract method call: _getSelectableLocationX()");
},_getSelectableLocationY:function(bw){throw new Error("Abstract method call: _getSelectableLocationY()");
},_getScroll:function(){throw new Error("Abstract method call: _getScroll()");
},_scrollBy:function(bx,by){throw new Error("Abstract method call: _scrollBy()");
},_scrollItemIntoView:function(bz){throw new Error("Abstract method call: _scrollItemIntoView()");
},getSelectables:function(bA){throw new Error("Abstract method call: getSelectables()");
},_getSelectableRange:function(bB,bC){throw new Error("Abstract method call: _getSelectableRange()");
},_getFirstSelectable:function(){throw new Error("Abstract method call: _getFirstSelectable()");
},_getLastSelectable:function(){throw new Error("Abstract method call: _getLastSelectable()");
},_getRelatedSelectable:function(bD,bE){throw new Error("Abstract method call: _getRelatedSelectable()");
},_getPage:function(bF,bG){throw new Error("Abstract method call: _getPage()");
},_applyMode:function(bH,bI){this._setLeadItem(null);
this._setAnchorItem(null);
this._clearSelection();
if(bH===o){this._applyDefaultSelection(true);
}this._fireChange();
},handleMouseOver:function(event){if(this.__mV!=null&&this.__mV!=this._getScroll().top){this.__mV=null;
return;
}this._userInteraction=true;

if(!this.getQuick()){this._userInteraction=false;
return;
}var bK=this.getMode();

if(bK!==o&&bK!==n){this._userInteraction=false;
return;
}var bJ=this._getSelectableFromMouseEvent(event);

if(bJ===null){this._userInteraction=false;
return;
}this._setSelectedItem(bJ);
this._fireChange(z);
this._userInteraction=false;
},handleMouseDown:function(event){this._userInteraction=true;
var bM=this._getSelectableFromMouseEvent(event);

if(bM===null){this._userInteraction=false;
return;
}var bO=event.isCtrlPressed()||(qx.core.Environment.get(h)==g&&event.isMetaPressed());
var bL=event.isShiftPressed();
if(this.isItemSelected(bM)&&!bL&&!bO&&!this.getDrag()){this.__mU=bM;
this._userInteraction=false;
return;
}else{this.__mU=null;
}this._scrollItemIntoView(bM);
switch(this.getMode()){case n:case o:this._setSelectedItem(bM);
break;
case k:this._setLeadItem(bM);
this._setAnchorItem(bM);
this._toggleInSelection(bM);
break;
case j:this._setLeadItem(bM);
if(bL){var bN=this._getAnchorItem();

if(bN===null){bN=this._getFirstSelectable();
this._setAnchorItem(bN);
}this._selectItemRange(bN,bM,bO);
}else if(bO){this._setAnchorItem(bM);
this._toggleInSelection(bM);
}else{this._setAnchorItem(bM);
this._setSelectedItem(bM);
}break;
}var bP=this.getMode();

if(this.getDrag()&&bP!==n&&bP!==o&&!bL&&!bO){this.__mI=this._getLocation();
this.__mF=this._getScroll();
this.__mJ=event.getDocumentLeft()+this.__mF.left;
this.__mK=event.getDocumentTop()+this.__mF.top;
this.__mL=true;
this._capture();
}this._fireChange(v);
this._userInteraction=false;
},handleMouseUp:function(event){this._userInteraction=true;
var bT=event.isCtrlPressed()||(qx.core.Environment.get(h)==g&&event.isMetaPressed());
var bQ=event.isShiftPressed();

if(!bT&&!bQ&&this.__mU!=null){var bR=this._getSelectableFromMouseEvent(event);

if(bR===null||!this.isItemSelected(bR)){this._userInteraction=false;
return;
}var bS=this.getMode();

if(bS===k){this._removeFromSelection(bR);
}else{this._setSelectedItem(bR);

if(this.getMode()===j){this._setLeadItem(bR);
this._setAnchorItem(bR);
}}this._userInteraction=false;
}this._cleanup();
},handleLoseCapture:function(event){this._cleanup();
},handleMouseMove:function(event){if(!this.__mL){return;
}this.__mM=event.getDocumentLeft();
this.__mN=event.getDocumentTop();
this._userInteraction=true;
var bV=this.__mM+this.__mF.left;

if(bV>this.__mJ){this.__mO=1;
}else if(bV<this.__mJ){this.__mO=-1;
}else{this.__mO=0;
}var bU=this.__mN+this.__mF.top;

if(bU>this.__mK){this.__mP=1;
}else if(bU<this.__mK){this.__mP=-1;
}else{this.__mP=0;
}var location=this.__mI;

if(this.__mM<location.left){this.__mC=this.__mM-location.left;
}else if(this.__mM>location.right){this.__mC=this.__mM-location.right;
}else{this.__mC=0;
}
if(this.__mN<location.top){this.__mD=this.__mN-location.top;
}else if(this.__mN>location.bottom){this.__mD=this.__mN-location.bottom;
}else{this.__mD=0;
}if(!this.__mE){this.__mE=new qx.event.Timer(100);
this.__mE.addListener(x,this._onInterval,this);
}this.__mE.start();
this._autoSelect();
event.stopPropagation();
this._userInteraction=false;
},handleAddItem:function(e){var bW=e.getData();

if(this.getMode()===o&&this.isSelectionEmpty()){this.addItem(bW);
}},handleRemoveItem:function(e){this.removeItem(e.getData());
},_cleanup:function(){if(!this.getDrag()&&this.__mL){return;
}if(this.__mQ){this._fireChange(v);
}delete this.__mL;
delete this.__mG;
delete this.__mH;
this._releaseCapture();
if(this.__mE){this.__mE.stop();
}},_onInterval:function(e){this._scrollBy(this.__mC,this.__mD);
this.__mF=this._getScroll();
this._autoSelect();
},_autoSelect:function(){var cg=this._getDimension();
var bY=Math.max(0,Math.min(this.__mM-this.__mI.left,cg.width))+this.__mF.left;
var bX=Math.max(0,Math.min(this.__mN-this.__mI.top,cg.height))+this.__mF.top;
if(this.__mG===bY&&this.__mH===bX){return;
}this.__mG=bY;
this.__mH=bX;
var ci=this._getAnchorItem();
var cb=ci;
var ce=this.__mO;
var ch,ca;

while(ce!==0){ch=ce>0?this._getRelatedSelectable(cb,F):this._getRelatedSelectable(cb,t);
if(ch!==null){ca=this._getSelectableLocationX(ch);
if((ce>0&&ca.left<=bY)||(ce<0&&ca.right>=bY)){cb=ch;
continue;
}}break;
}var cf=this.__mP;
var cd,cc;

while(cf!==0){cd=cf>0?this._getRelatedSelectable(cb,f):this._getRelatedSelectable(cb,w);
if(cd!==null){cc=this._getSelectableLocationY(cd);
if((cf>0&&cc.top<=bX)||(cf<0&&cc.bottom>=bX)){cb=cd;
continue;
}}break;
}var cj=this.getMode();

if(cj===j){this._selectItemRange(ci,cb);
}else if(cj===k){if(this.isItemSelected(ci)){this._selectItemRange(ci,cb,true);
}else{this._deselectItemRange(ci,cb);
}this._setAnchorItem(cb);
}this._fireChange(E);
},__mu:{Home:1,Down:1,Right:1,PageDown:1,End:1,Up:1,Left:1,PageUp:1},handleKeyPress:function(event){this._userInteraction=true;
var cp,co;
var cr=event.getKeyIdentifier();
var cq=this.getMode();
var cl=event.isCtrlPressed()||(qx.core.Environment.get(h)==g&&event.isMetaPressed());
var cm=event.isShiftPressed();
var cn=false;

if(cr===r&&cl){if(cq!==n&&cq!==o){this._selectAllItems();
cn=true;
}}else if(cr===u){if(cq!==n&&cq!==o){this._clearSelection();
cn=true;
}}else if(cr===s){var ck=this.getLeadItem();

if(ck!=null&&!cm){if(cl||cq===k){this._toggleInSelection(ck);
}else{this._setSelectedItem(ck);
}cn=true;
}}else if(this.__mu[cr]){cn=true;

if(cq===n||cq==o){cp=this._getSelectedItem();
}else{cp=this.getLeadItem();
}
if(cp!==null){switch(cr){case H:co=this._getFirstSelectable();
break;
case I:co=this._getLastSelectable();
break;
case M:co=this._getRelatedSelectable(cp,w);
break;
case N:co=this._getRelatedSelectable(cp,f);
break;
case c:co=this._getRelatedSelectable(cp,t);
break;
case G:co=this._getRelatedSelectable(cp,F);
break;
case d:co=this._getPage(cp,true);
break;
case K:co=this._getPage(cp,false);
break;
}}else{switch(cr){case H:case N:case G:case K:co=this._getFirstSelectable();
break;
case I:case M:case c:case d:co=this._getLastSelectable();
break;
}}if(co!==null){switch(cq){case n:case o:this._setSelectedItem(co);
break;
case k:this._setLeadItem(co);
break;
case j:if(cm){var cs=this._getAnchorItem();

if(cs===null){this._setAnchorItem(cs=this._getFirstSelectable());
}this._setLeadItem(co);
this._selectItemRange(cs,co,cl);
}else{this._setAnchorItem(co);
this._setLeadItem(co);

if(!cl){this._setSelectedItem(co);
}}break;
}this.__mV=this._getScroll().top;
this._scrollItemIntoView(co);
}}
if(cn){event.stop();
this._fireChange(C);
}this._userInteraction=false;
},_selectAllItems:function(){var ct=this.getSelectables();

for(var i=0,l=ct.length;i<l;i++){this._addToSelection(ct[i]);
}},_clearSelection:function(){var cu=this.__eM;

for(var cv in cu){this._removeFromSelection(cu[cv]);
}this.__eM={};
},_selectItemRange:function(cw,cx,cy){var cB=this._getSelectableRange(cw,cx);
if(!cy){var cA=this.__eM;
var cC=this.__mW(cB);

for(var cz in cA){if(!cC[cz]){this._removeFromSelection(cA[cz]);
}}}for(var i=0,l=cB.length;i<l;i++){this._addToSelection(cB[i]);
}},_deselectItemRange:function(cD,cE){var cF=this._getSelectableRange(cD,cE);

for(var i=0,l=cF.length;i<l;i++){this._removeFromSelection(cF[i]);
}},__mW:function(cG){var cI={};
var cH;

for(var i=0,l=cG.length;i<l;i++){cH=cG[i];
cI[this._selectableToHashCode(cH)]=cH;
}return cI;
},_getSelectedItem:function(){for(var cJ in this.__eM){return this.__eM[cJ];
}return null;
},_setSelectedItem:function(cK){if(this._isSelectable(cK)){var cL=this.__eM;
var cM=this._selectableToHashCode(cK);

if(!cL[cM]||qx.lang.Object.hasMinLength(cL,2)){this._clearSelection();
this._addToSelection(cK);
}}},_addToSelection:function(cN){var cO=this._selectableToHashCode(cN);

if(this.__eM[cO]==null&&this._isSelectable(cN)){this.__eM[cO]=cN;
this._styleSelectable(cN,m,true);
this.__mQ=true;
}},_toggleInSelection:function(cP){var cQ=this._selectableToHashCode(cP);

if(this.__eM[cQ]==null){this.__eM[cQ]=cP;
this._styleSelectable(cP,m,true);
}else{delete this.__eM[cQ];
this._styleSelectable(cP,m,false);
}this.__mQ=true;
},_removeFromSelection:function(cR){var cS=this._selectableToHashCode(cR);

if(this.__eM[cS]!=null){delete this.__eM[cS];
this._styleSelectable(cR,m,false);
this.__mQ=true;
}},_replaceMultiSelection:function(cT){var cW=false;
var da,cY;
var cU={};

for(var i=0,l=cT.length;i<l;i++){da=cT[i];

if(this._isSelectable(da)){cY=this._selectableToHashCode(da);
cU[cY]=da;
}}var db=cT[0];
var cV=da;
var cX=this.__eM;

for(var cY in cX){if(cU[cY]){delete cU[cY];
}else{da=cX[cY];
delete cX[cY];
this._styleSelectable(da,m,false);
cW=true;
}}for(var cY in cU){da=cX[cY]=cU[cY];
this._styleSelectable(da,m,true);
cW=true;
}if(!cW){return false;
}this._scrollItemIntoView(cV);
this._setLeadItem(db);
this._setAnchorItem(db);
this.__mQ=true;
this._fireChange();
},_fireChange:function(dc){if(this.__mQ){this.__mR=dc||null;
this.fireDataEvent(y,this.getSelection());
delete this.__mQ;
}},_applyDefaultSelection:function(dd){if(dd===true||this.getMode()===o&&this.isSelectionEmpty()){var de=this._getFirstSelectable();

if(de!=null){this.selectItem(de);
}return de;
}return null;
}},destruct:function(){this._disposeObjects(q);
this.__eM=this.__mU=this.__mT=null;
this.__mS=null;
}});
})();
(function(){var f="vertical",e="under",d="above",c="qx.ui.core.selection.Widget",b="left",a="right";
qx.Class.define(c,{extend:qx.ui.core.selection.Abstract,construct:function(g){qx.ui.core.selection.Abstract.call(this);
this.__jE=g;
},members:{__jE:null,_isSelectable:function(h){return this._isItemSelectable(h)&&h.getLayoutParent()===this.__jE;
},_selectableToHashCode:function(j){return j.$$hash;
},_styleSelectable:function(k,m,n){n?k.addState(m):k.removeState(m);
},_capture:function(){this.__jE.capture();
},_releaseCapture:function(){this.__jE.releaseCapture();
},_isItemSelectable:function(o){if(this._userInteraction){return o.isVisible()&&o.isEnabled();
}else{return o.isVisible();
}},_getWidget:function(){return this.__jE;
},_getLocation:function(){var p=this.__jE.getContentElement().getDomElement();
return p?qx.bom.element.Location.get(p):null;
},_getDimension:function(){return this.__jE.getInnerSize();
},_getSelectableLocationX:function(q){var r=q.getBounds();

if(r){return {left:r.left,right:r.left+r.width};
}},_getSelectableLocationY:function(s){var t=s.getBounds();

if(t){return {top:t.top,bottom:t.top+t.height};
}},_getScroll:function(){return {left:0,top:0};
},_scrollBy:function(u,v){},_scrollItemIntoView:function(w){this.__jE.scrollChildIntoView(w);
},getSelectables:function(x){var y=false;

if(!x){y=this._userInteraction;
this._userInteraction=true;
}var B=this.__jE.getChildren();
var z=[];
var A;

for(var i=0,l=B.length;i<l;i++){A=B[i];

if(this._isItemSelectable(A)){z.push(A);
}}this._userInteraction=y;
return z;
},_getSelectableRange:function(C,D){if(C===D){return [C];
}var H=this.__jE.getChildren();
var E=[];
var G=false;
var F;

for(var i=0,l=H.length;i<l;i++){F=H[i];

if(F===C||F===D){if(G){E.push(F);
break;
}else{G=true;
}}
if(G&&this._isItemSelectable(F)){E.push(F);
}}return E;
},_getFirstSelectable:function(){var I=this.__jE.getChildren();

for(var i=0,l=I.length;i<l;i++){if(this._isItemSelectable(I[i])){return I[i];
}}return null;
},_getLastSelectable:function(){var J=this.__jE.getChildren();

for(var i=J.length-1;i>0;i--){if(this._isItemSelectable(J[i])){return J[i];
}}return null;
},_getRelatedSelectable:function(K,L){var O=this.__jE.getOrientation()===f;
var N=this.__jE.getChildren();
var M=N.indexOf(K);
var P;

if((O&&L===d)||(!O&&L===b)){for(var i=M-1;i>=0;i--){P=N[i];

if(this._isItemSelectable(P)){return P;
}}}else if((O&&L===e)||(!O&&L===a)){for(var i=M+1;i<N.length;i++){P=N[i];

if(this._isItemSelectable(P)){return P;
}}}return null;
},_getPage:function(Q,R){if(R){return this._getFirstSelectable();
}else{return this._getLastSelectable();
}}},destruct:function(){this.__jE=null;
}});
})();
(function(){var a="qx.ui.core.selection.ScrollArea";
qx.Class.define(a,{extend:qx.ui.core.selection.Widget,members:{_isSelectable:function(b){return this._isItemSelectable(b)&&b.getLayoutParent()===this._getWidget().getChildrenContainer();
},_getDimension:function(){return this._getWidget().getPaneSize();
},_getScroll:function(){var c=this._getWidget();
return {left:c.getScrollX(),top:c.getScrollY()};
},_scrollBy:function(d,e){var f=this._getWidget();
f.scrollByX(d);
f.scrollByY(e);
},_getPage:function(g,h){var m=this.getSelectables();
var length=m.length;
var p=m.indexOf(g);
if(p===-1){throw new Error("Invalid lead item: "+g);
}var j=this._getWidget();
var r=j.getScrollY();
var innerHeight=j.getInnerSize().height;
var top,l,q;

if(h){var o=r;
var i=p;
while(1){for(;i>=0;i--){top=j.getItemTop(m[i]);
if(top<o){q=i+1;
break;
}}if(q==null){var s=this._getFirstSelectable();
return s==g?null:s;
}if(q>=p){o-=innerHeight+r-j.getItemBottom(g);
q=null;
continue;
}return m[q];
}}else{var n=innerHeight+r;
var i=p;
while(1){for(;i<length;i++){l=j.getItemBottom(m[i]);
if(l>n){q=i-1;
break;
}}if(q==null){var k=this._getLastSelectable();
return k==g?null:k;
}if(q<=p){n+=j.getItemTop(g)-r;
q=null;
continue;
}return m[q];
}}}}});
})();
(function(){var e="qx.ui.tree.selection.SelectionManager",d="above",c="under",b="right",a="left";
qx.Class.define(e,{extend:qx.ui.core.selection.ScrollArea,members:{_getSelectableLocationY:function(f){var g=f.getBounds();

if(g){var top=this._getWidget().getItemTop(f);
return {top:top,bottom:top+g.height};
}},_isSelectable:function(h){return this._isItemSelectable(h)&&h instanceof qx.ui.tree.core.AbstractTreeItem;
},_getSelectableFromMouseEvent:function(event){return this._getWidget().getTreeItem(event.getTarget());
},getSelectables:function(j){var m=false;

if(!j){m=this._userInteraction;
this._userInteraction=true;
}var l=this._getWidget();
var n=[];

if(l.getRoot()!=null){var k=l.getRoot().getItems(true,!!j,l.getHideRoot());

for(var i=0;i<k.length;i++){if(this._isSelectable(k[i])){n.push(k[i]);
}}}this._userInteraction=m;
return n;
},_getSelectableRange:function(o,p){if(o===p){return [o];
}var q=this.getSelectables();
var r=q.indexOf(o);
var s=q.indexOf(p);

if(r<0||s<0){return [];
}
if(r<s){return q.slice(r,s+1);
}else{return q.slice(s,r+1);
}},_getFirstSelectable:function(){return this.getSelectables()[0]||null;
},_getLastSelectable:function(){var t=this.getSelectables();

if(t.length>0){return t[t.length-1];
}else{return null;
}},_getRelatedSelectable:function(u,v){var w=this._getWidget();
var x=null;

switch(v){case d:x=w.getPreviousNodeOf(u,false);
break;
case c:x=w.getNextNodeOf(u,false);
break;
case a:case b:break;
}
if(!x){return null;
}
if(this._isSelectable(x)){return x;
}else{return this._getRelatedSelectable(x,v);
}}}});
})();
(function(){var v="single",u="Boolean",t="one",s="changeSelection",r="__eI",q="mouseup",p="mousedown",o="losecapture",n="multi",m="_applyQuickSelection",d="mouseover",l="_applySelectionMode",h="_applyDragSelection",c="qx.ui.core.MMultiSelectionHandling",b="removeItem",g="keypress",f="qx.event.type.Data",j="addItem",a="additive",k="mousemove";
qx.Mixin.define(c,{construct:function(){var x=this.SELECTION_MANAGER;
var w=this.__eI=new x(this);
this.addListener(p,w.handleMouseDown,w);
this.addListener(q,w.handleMouseUp,w);
this.addListener(d,w.handleMouseOver,w);
this.addListener(k,w.handleMouseMove,w);
this.addListener(o,w.handleLoseCapture,w);
this.addListener(g,w.handleKeyPress,w);
this.addListener(j,w.handleAddItem,w);
this.addListener(b,w.handleRemoveItem,w);
w.addListener(s,this._onSelectionChange,this);
},events:{"changeSelection":f},properties:{selectionMode:{check:[v,n,a,t],init:v,apply:l},dragSelection:{check:u,init:false,apply:h},quickSelection:{check:u,init:false,apply:m}},members:{__eI:null,selectAll:function(){this.__eI.selectAll();
},isSelected:function(y){if(!qx.ui.core.Widget.contains(this,y)){throw new Error("Could not test if "+y+" is selected, because it is not a child element!");
}return this.__eI.isItemSelected(y);
},addToSelection:function(z){if(!qx.ui.core.Widget.contains(this,z)){throw new Error("Could not add + "+z+" to selection, because it is not a child element!");
}this.__eI.addItem(z);
},removeFromSelection:function(A){if(!qx.ui.core.Widget.contains(this,A)){throw new Error("Could not remove "+A+" from selection, because it is not a child element!");
}this.__eI.removeItem(A);
},selectRange:function(B,C){this.__eI.selectItemRange(B,C);
},resetSelection:function(){this.__eI.clearSelection();
},setSelection:function(D){for(var i=0;i<D.length;i++){if(!qx.ui.core.Widget.contains(this,D[i])){throw new Error("Could not select "+D[i]+", because it is not a child element!");
}}
if(D.length===0){this.resetSelection();
}else{var E=this.getSelection();

if(!qx.lang.Array.equals(E,D)){this.__eI.replaceSelection(D);
}}},getSelection:function(){return this.__eI.getSelection();
},getSortedSelection:function(){return this.__eI.getSortedSelection();
},isSelectionEmpty:function(){return this.__eI.isSelectionEmpty();
},getSelectionContext:function(){return this.__eI.getSelectionContext();
},_getManager:function(){return this.__eI;
},getSelectables:function(F){return this.__eI.getSelectables(F);
},invertSelection:function(){this.__eI.invertSelection();
},_getLeadItem:function(){var G=this.__eI.getMode();

if(G===v||G===t){return this.__eI.getSelectedItem();
}else{return this.__eI.getLeadItem();
}},_applySelectionMode:function(H,I){this.__eI.setMode(H);
},_applyDragSelection:function(J,K){this.__eI.setDrag(J);
},_applyQuickSelection:function(L,M){this.__eI.setQuick(L);
},_onSelectionChange:function(e){this.fireDataEvent(s,e.getData());
}},destruct:function(){this._disposeObjects(r);
}});
})();
(function(){var a="qx.ui.core.IMultiSelection";
qx.Interface.define(a,{extend:qx.ui.core.ISingleSelection,members:{selectAll:function(){return true;
},addToSelection:function(b){return arguments.length==1;
},removeFromSelection:function(c){return arguments.length==1;
}}});
})();
(function(){var f="scrollbar-x",d="scrollbar-y",c="qx.ui.core.scroll.MWheelHandling",b="x",a="y";
qx.Mixin.define(c,{members:{_onMouseWheel:function(e){var l=this._isChildControlVisible(f);
var m=this._isChildControlVisible(d);
var q=m?this.getChildControl(d,true):null;
var p=l?this.getChildControl(f,true):null;
var j=e.getWheelDelta(a);
var i=e.getWheelDelta(b);
var k=!m;
var n=!l;
if(q){var o=parseInt(j);

if(o!==0){q.scrollBySteps(o);
}var h=q.getPosition();
var g=q.getMaximum();
if(o<0&&h<=0||o>0&&h>=g){k=true;
}}if(p){var o=parseInt(i);

if(o!==0){p.scrollBySteps(o);
}var h=p.getPosition();
var g=p.getMaximum();
if(o<0&&h<=0||o>0&&h>=g){n=true;
}}if(!k||!n){e.stop();
}}}});
})();
(function(){var b="qx.nativeScrollBars",a="qx.ui.core.scroll.MScrollBarFactory";
qx.core.Environment.add(b,false);
qx.Mixin.define(a,{members:{_createScrollBar:function(c){if(qx.core.Environment.get(b)){return new qx.ui.core.scroll.NativeScrollBar(c);
}else{return new qx.ui.core.scroll.ScrollBar(c);
}}}});
})();
(function(){var b="qx.ui.core.scroll.IScrollBar",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"scroll":a},properties:{orientation:{},maximum:{},position:{},knobFactor:{}},members:{scrollTo:function(c){this.assertNumber(c);
},scrollBy:function(d){this.assertNumber(d);
},scrollBySteps:function(e){this.assertNumber(e);
}}});
})();
(function(){var k="horizontal",j="px",i="scroll",h="vertical",g="-1px",f="0",d="engine.name",c="hidden",b="mousedown",a="qx.ui.core.scroll.NativeScrollBar",z="PositiveNumber",y="Integer",x="__mX",w="mousemove",v="_applyMaximum",u="_applyOrientation",t="appear",s="opera",r="PositiveInteger",q="mshtml",o="mouseup",p="Number",m="_applyPosition",n="scrollbar",l="native";
qx.Class.define(a,{extend:qx.ui.core.Widget,implement:qx.ui.core.scroll.IScrollBar,construct:function(A){qx.ui.core.Widget.call(this);
this.addState(l);
this.getContentElement().addListener(i,this._onScroll,this);
this.addListener(b,this._stopPropagation,this);
this.addListener(o,this._stopPropagation,this);
this.addListener(w,this._stopPropagation,this);

if((qx.core.Environment.get(d)==s)){this.addListener(t,this._onAppear,this);
}this.getContentElement().add(this._getScrollPaneElement());
if(A!=null){this.setOrientation(A);
}else{this.initOrientation();
}},properties:{appearance:{refine:true,init:n},orientation:{check:[k,h],init:k,apply:u},maximum:{check:r,apply:v,init:100},position:{check:p,init:0,apply:m,event:i},singleStep:{check:y,init:20},knobFactor:{check:z,nullable:true}},members:{__lW:null,__mX:null,_getScrollPaneElement:function(){if(!this.__mX){this.__mX=new qx.html.Element();
}return this.__mX;
},renderLayout:function(B,top,C,D){var E=qx.ui.core.Widget.prototype.renderLayout.call(this,B,top,C,D);
this._updateScrollBar();
return E;
},_getContentHint:function(){var F=qx.bom.element.Overflow.getScrollbarWidth();
return {width:this.__lW?100:F,maxWidth:this.__lW?null:F,minWidth:this.__lW?null:F,height:this.__lW?F:100,maxHeight:this.__lW?F:null,minHeight:this.__lW?F:null};
},_applyEnabled:function(G,H){qx.ui.core.Widget.prototype._applyEnabled.call(this,G,H);
this._updateScrollBar();
},_applyMaximum:function(I){this._updateScrollBar();
},_applyPosition:function(J){var content=this.getContentElement();

if(this.__lW){content.scrollToX(J);
}else{content.scrollToY(J);
}},_applyOrientation:function(K,L){var M=this.__lW=K===k;
this.set({allowGrowX:M,allowShrinkX:M,allowGrowY:!M,allowShrinkY:!M});

if(M){this.replaceState(h,k);
}else{this.replaceState(k,h);
}this.getContentElement().setStyles({overflowX:M?i:c,overflowY:M?c:i});
qx.ui.core.queue.Layout.add(this);
},_updateScrollBar:function(){var O=this.__lW;
var P=this.getBounds();

if(!P){return;
}
if(this.isEnabled()){var Q=O?P.width:P.height;
var N=this.getMaximum()+Q;
}else{N=0;
}if((qx.core.Environment.get(d)==q)){var P=this.getBounds();
this.getContentElement().setStyles({left:O?f:g,top:O?g:f,width:(O?P.width:P.width+1)+j,height:(O?P.height+1:P.height)+j});
}this._getScrollPaneElement().setStyles({left:0,top:0,width:(O?N:1)+j,height:(O?1:N)+j});
this.scrollTo(this.getPosition());
},scrollTo:function(R){this.setPosition(Math.max(0,Math.min(this.getMaximum(),R)));
},scrollBy:function(S){this.scrollTo(this.getPosition()+S);
},scrollBySteps:function(T){var U=this.getSingleStep();
this.scrollBy(T*U);
},_onScroll:function(e){var W=this.getContentElement();
var V=this.__lW?W.getScrollX():W.getScrollY();
this.setPosition(V);
},_onAppear:function(e){this.scrollTo(this.getPosition());
},_stopPropagation:function(e){e.stopPropagation();
}},destruct:function(){this._disposeObjects(x);
}});
})();
(function(){var k="slider",j="horizontal",i="button-begin",h="vertical",g="button-end",f="Integer",d="execute",c="right",b="left",a="down",z="up",y="PositiveNumber",x="changeValue",w="qx.lang.Type.isNumber(value)&&value>=0&&value<=this.getMaximum()",v="_applyKnobFactor",u="knob",t="qx.ui.core.scroll.ScrollBar",s="resize",r="_applyOrientation",q="_applyPageStep",o="PositiveInteger",p="scroll",m="_applyPosition",n="scrollbar",l="_applyMaximum";
qx.Class.define(t,{extend:qx.ui.core.Widget,implement:qx.ui.core.scroll.IScrollBar,construct:function(A){qx.ui.core.Widget.call(this);
this._createChildControl(i);
this._createChildControl(k).addListener(s,this._onResizeSlider,this);
this._createChildControl(g);
if(A!=null){this.setOrientation(A);
}else{this.initOrientation();
}},properties:{appearance:{refine:true,init:n},orientation:{check:[j,h],init:j,apply:r},maximum:{check:o,apply:l,init:100},position:{check:w,init:0,apply:m,event:p},singleStep:{check:f,init:20},pageStep:{check:f,init:10,apply:q},knobFactor:{check:y,apply:v,nullable:true}},members:{__mY:2,_createChildControlImpl:function(B,C){var D;

switch(B){case k:D=new qx.ui.core.scroll.ScrollSlider();
D.setPageStep(100);
D.setFocusable(false);
D.addListener(x,this._onChangeSliderValue,this);
this._add(D,{flex:1});
break;
case i:D=new qx.ui.form.RepeatButton();
D.setFocusable(false);
D.addListener(d,this._onExecuteBegin,this);
this._add(D);
break;
case g:D=new qx.ui.form.RepeatButton();
D.setFocusable(false);
D.addListener(d,this._onExecuteEnd,this);
this._add(D);
break;
}return D||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,B);
},_applyMaximum:function(E){this.getChildControl(k).setMaximum(E);
},_applyPosition:function(F){this.getChildControl(k).setValue(F);
},_applyKnobFactor:function(G){this.getChildControl(k).setKnobFactor(G);
},_applyPageStep:function(H){this.getChildControl(k).setPageStep(H);
},_applyOrientation:function(I,J){var K=this._getLayout();

if(K){K.dispose();
}if(I===j){this._setLayout(new qx.ui.layout.HBox());
this.setAllowStretchX(true);
this.setAllowStretchY(false);
this.replaceState(h,j);
this.getChildControl(i).replaceState(z,b);
this.getChildControl(g).replaceState(a,c);
}else{this._setLayout(new qx.ui.layout.VBox());
this.setAllowStretchX(false);
this.setAllowStretchY(true);
this.replaceState(j,h);
this.getChildControl(i).replaceState(b,z);
this.getChildControl(g).replaceState(c,a);
}this.getChildControl(k).setOrientation(I);
},scrollTo:function(L){this.getChildControl(k).slideTo(L);
},scrollBy:function(M){this.getChildControl(k).slideBy(M);
},scrollBySteps:function(N){var O=this.getSingleStep();
this.getChildControl(k).slideBy(N*O);
},_onExecuteBegin:function(e){this.scrollBy(-this.getSingleStep());
},_onExecuteEnd:function(e){this.scrollBy(this.getSingleStep());
},_onChangeSliderValue:function(e){this.setPosition(e.getData());
},_onResizeSlider:function(e){var P=this.getChildControl(k).getChildControl(u);
var S=P.getSizeHint();
var Q=false;
var R=this.getChildControl(k).getInnerSize();

if(this.getOrientation()==h){if(R.height<S.minHeight+this.__mY){Q=true;
}}else{if(R.width<S.minWidth+this.__mY){Q=true;
}}
if(Q){P.exclude();
}else{P.show();
}}}});
})();
(function(){var a="qx.ui.form.IRange";
qx.Interface.define(a,{members:{setMinimum:function(b){return arguments.length==1;
},getMinimum:function(){},setMaximum:function(c){return arguments.length==1;
},getMaximum:function(){},setSingleStep:function(d){return arguments.length==1;
},getSingleStep:function(){},setPageStep:function(e){return arguments.length==1;
},getPageStep:function(){}}});
})();
(function(){var b="qx.ui.form.INumberForm",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"changeValue":a},members:{setValue:function(c){return arguments.length==1;
},resetValue:function(){},getValue:function(){}}});
})();
(function(){var k="knob",j="horizontal",i="vertical",h="Integer",g="hovered",f="left",d="top",c="mouseup",b="pressed",a="px",X="changeValue",W="interval",V="mousemove",U="resize",T="slider",S="mousedown",R="PageUp",Q="mouseout",P="x",O='qx.event.type.Data',r="Left",s="Down",p="Up",q="dblclick",n="qx.ui.form.Slider",o="PageDown",l="mousewheel",m="_applyValue",u="_applyKnobFactor",v="End",C="height",A="y",G="Right",E="width",K="_applyOrientation",I="Home",x="mouseover",N="floor",M="_applyMinimum",L="click",w="typeof value==='number'&&value>=this.getMinimum()&&value<=this.getMaximum()",y="keypress",z="ceil",B="losecapture",D="contextmenu",F="_applyMaximum",H="Number",J="changeMaximum",t="changeMinimum";
qx.Class.define(n,{extend:qx.ui.core.Widget,implement:[qx.ui.form.IForm,qx.ui.form.INumberForm,qx.ui.form.IRange],include:[qx.ui.form.MForm],construct:function(Y){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.Canvas());
this.addListener(y,this._onKeyPress);
this.addListener(l,this._onMouseWheel);
this.addListener(S,this._onMouseDown);
this.addListener(c,this._onMouseUp);
this.addListener(B,this._onMouseUp);
this.addListener(U,this._onUpdate);
this.addListener(D,this._onStopEvent);
this.addListener(L,this._onStopEvent);
this.addListener(q,this._onStopEvent);
if(Y!=null){this.setOrientation(Y);
}else{this.initOrientation();
}},events:{changeValue:O},properties:{appearance:{refine:true,init:T},focusable:{refine:true,init:true},orientation:{check:[j,i],init:j,apply:K},value:{check:w,init:0,apply:m,nullable:true},minimum:{check:h,init:0,apply:M,event:t},maximum:{check:h,init:100,apply:F,event:J},singleStep:{check:h,init:1},pageStep:{check:h,init:10},knobFactor:{check:H,apply:u,nullable:true}},members:{__na:null,__nb:null,__nc:null,__nd:null,__ne:null,__nf:null,__ng:null,__nh:null,__je:null,__ni:null,__nj:null,__nk:null,_forwardStates:{invalid:true},_createChildControlImpl:function(ba,bb){var bc;

switch(ba){case k:bc=new qx.ui.core.Widget();
bc.addListener(U,this._onUpdate,this);
bc.addListener(x,this._onMouseOver);
bc.addListener(Q,this._onMouseOut);
this._add(bc);
break;
}return bc||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,ba);
},_onMouseOver:function(e){this.addState(g);
},_onMouseOut:function(e){this.removeState(g);
},_onMouseWheel:function(e){var bf=this.getOrientation()===j?P:A;
var be=e.getWheelDelta(bf);
var bd=be>0?1:be<0?-1:0;
this.slideBy(bd*this.getSingleStep());
e.stop();
},_onKeyPress:function(e){var bh=this.getOrientation()===j;
var bg=bh?r:p;
var forward=bh?G:s;

switch(e.getKeyIdentifier()){case forward:this.slideForward();
break;
case bg:this.slideBack();
break;
case o:this.slidePageForward();
break;
case R:this.slidePageBack();
break;
case I:this.slideToBegin();
break;
case v:this.slideToEnd();
break;
default:return;
}e.stop();
},_onMouseDown:function(e){if(this.__nd){return;
}var bk=this.__lW;
var bi=this.getChildControl(k);
var bj=bk?f:d;
var bm=bk?e.getDocumentLeft():e.getDocumentTop();
var bn=this.__na=qx.bom.element.Location.get(this.getContentElement().getDomElement())[bj];
var bl=this.__nb=qx.bom.element.Location.get(bi.getContainerElement().getDomElement())[bj];

if(e.getTarget()===bi){this.__nd=true;

if(!this.__ni){this.__ni=new qx.event.Timer(100);
this.__ni.addListener(W,this._fireValue,this);
}this.__ni.start();
this.__ne=bm+bn-bl;
bi.addState(b);
}else{this.__nf=true;
this.__ng=bm<=bl?-1:1;
this.__nm(e);
this._onInterval();
if(!this.__je){this.__je=new qx.event.Timer(100);
this.__je.addListener(W,this._onInterval,this);
}this.__je.start();
}this.addListener(V,this._onMouseMove);
this.capture();
e.stopPropagation();
},_onMouseUp:function(e){if(this.__nd){this.releaseCapture();
delete this.__nd;
this.__ni.stop();
this._fireValue();
delete this.__ne;
this.getChildControl(k).removeState(b);
if(e.getType()===c){var bp;
var bq;
var bo;

if(this.__lW){bp=e.getDocumentLeft()-(this._valueToPosition(this.getValue())+this.__na);
bo=qx.bom.element.Location.get(this.getContentElement().getDomElement())[d];
bq=e.getDocumentTop()-(bo+this.getChildControl(k).getBounds().top);
}else{bp=e.getDocumentTop()-(this._valueToPosition(this.getValue())+this.__na);
bo=qx.bom.element.Location.get(this.getContentElement().getDomElement())[f];
bq=e.getDocumentLeft()-(bo+this.getChildControl(k).getBounds().left);
}
if(bq<0||bq>this.__nc||bp<0||bp>this.__nc){this.getChildControl(k).removeState(g);
}}}else if(this.__nf){this.__je.stop();
this.releaseCapture();
delete this.__nf;
delete this.__ng;
delete this.__nh;
}this.removeListener(V,this._onMouseMove);
if(e.getType()===c){e.stopPropagation();
}},_onMouseMove:function(e){if(this.__nd){var bs=this.__lW?e.getDocumentLeft():e.getDocumentTop();
var br=bs-this.__ne;
this.slideTo(this._positionToValue(br));
}else if(this.__nf){this.__nm(e);
}e.stopPropagation();
},_onInterval:function(e){var bt=this.getValue()+(this.__ng*this.getPageStep());
if(bt<this.getMinimum()){bt=this.getMinimum();
}else if(bt>this.getMaximum()){bt=this.getMaximum();
}var bu=this.__ng==-1;

if((bu&&bt<=this.__nh)||(!bu&&bt>=this.__nh)){bt=this.__nh;
}this.slideTo(bt);
},_onUpdate:function(e){var bw=this.getInnerSize();
var bx=this.getChildControl(k).getBounds();
var bv=this.__lW?E:C;
this._updateKnobSize();
this.__nl=bw[bv]-bx[bv];
this.__nc=bx[bv];
this._updateKnobPosition();
},__lW:false,__nl:0,__nm:function(e){var by=this.__lW;
var bF=by?e.getDocumentLeft():e.getDocumentTop();
var bH=this.__na;
var bz=this.__nb;
var bJ=this.__nc;
var bG=bF-bH;

if(bF>=bz){bG-=bJ;
}var bD=this._positionToValue(bG);
var bA=this.getMinimum();
var bB=this.getMaximum();

if(bD<bA){bD=bA;
}else if(bD>bB){bD=bB;
}else{var bE=this.getValue();
var bC=this.getPageStep();
var bI=this.__ng<0?N:z;
bD=bE+(Math[bI]((bD-bE)/bC)*bC);
}if(this.__nh==null||(this.__ng==-1&&bD<=this.__nh)||(this.__ng==1&&bD>=this.__nh)){this.__nh=bD;
}},_positionToValue:function(bK){var bL=this.__nl;
if(bL==null||bL==0){return 0;
}var bN=bK/bL;

if(bN<0){bN=0;
}else if(bN>1){bN=1;
}var bM=this.getMaximum()-this.getMinimum();
return this.getMinimum()+Math.round(bM*bN);
},_valueToPosition:function(bO){var bP=this.__nl;

if(bP==null){return 0;
}var bQ=this.getMaximum()-this.getMinimum();
if(bQ==0){return 0;
}var bO=bO-this.getMinimum();
var bR=bO/bQ;

if(bR<0){bR=0;
}else if(bR>1){bR=1;
}return Math.round(bP*bR);
},_updateKnobPosition:function(){this._setKnobPosition(this._valueToPosition(this.getValue()));
},_setKnobPosition:function(bS){var bT=this.getChildControl(k).getContainerElement();

if(this.__lW){bT.setStyle(f,bS+a,true);
}else{bT.setStyle(d,bS+a,true);
}},_updateKnobSize:function(){var bV=this.getKnobFactor();

if(bV==null){return;
}var bU=this.getInnerSize();

if(bU==null){return;
}if(this.__lW){this.getChildControl(k).setWidth(Math.round(bV*bU.width));
}else{this.getChildControl(k).setHeight(Math.round(bV*bU.height));
}},slideToBegin:function(){this.slideTo(this.getMinimum());
},slideToEnd:function(){this.slideTo(this.getMaximum());
},slideForward:function(){this.slideBy(this.getSingleStep());
},slideBack:function(){this.slideBy(-this.getSingleStep());
},slidePageForward:function(){this.slideBy(this.getPageStep());
},slidePageBack:function(){this.slideBy(-this.getPageStep());
},slideBy:function(bW){this.slideTo(this.getValue()+bW);
},slideTo:function(bX){if(bX<this.getMinimum()){bX=this.getMinimum();
}else if(bX>this.getMaximum()){bX=this.getMaximum();
}else{bX=this.getMinimum()+Math.round((bX-this.getMinimum())/this.getSingleStep())*this.getSingleStep();
}this.setValue(bX);
},_applyOrientation:function(bY,ca){var cb=this.getChildControl(k);
this.__lW=bY===j;
if(this.__lW){this.removeState(i);
cb.removeState(i);
this.addState(j);
cb.addState(j);
cb.setLayoutProperties({top:0,right:null,bottom:0});
}else{this.removeState(j);
cb.removeState(j);
this.addState(i);
cb.addState(i);
cb.setLayoutProperties({right:0,bottom:null,left:0});
}this._updateKnobPosition();
},_applyKnobFactor:function(cc,cd){if(cc!=null){this._updateKnobSize();
}else{if(this.__lW){this.getChildControl(k).resetWidth();
}else{this.getChildControl(k).resetHeight();
}}},_applyValue:function(ce,cf){if(ce!=null){this._updateKnobPosition();

if(this.__nd){this.__nk=[ce,cf];
}else{this.fireEvent(X,qx.event.type.Data,[ce,cf]);
}}else{this.resetValue();
}},_fireValue:function(){if(!this.__nk){return;
}var cg=this.__nk;
this.__nk=null;
this.fireEvent(X,qx.event.type.Data,cg);
},_applyMinimum:function(ch,ci){if(this.getValue()<ch){this.setValue(ch);
}this._updateKnobPosition();
},_applyMaximum:function(cj,ck){if(this.getValue()>cj){this.setValue(cj);
}this._updateKnobPosition();
}}});
})();
(function(){var d="horizontal",c="mousewheel",b="qx.ui.core.scroll.ScrollSlider",a="keypress";
qx.Class.define(b,{extend:qx.ui.form.Slider,construct:function(e){qx.ui.form.Slider.call(this,e);
this.removeListener(a,this._onKeyPress);
this.removeListener(c,this._onMouseWheel);
},members:{getSizeHint:function(f){var g=qx.ui.form.Slider.prototype.getSizeHint.call(this);
if(this.getOrientation()===d){g.width=0;
}else{g.height=0;
}return g;
}}});
})();
(function(){var k="scrollbar-y",j="scrollbar-x",i="pane",h="auto",g="corner",f="scrollbar-",d="on",c="_computeScrollbars",b="getDocument",a="changeVisibility",E="off",D="x",C="scroll",B="touchmove",A="scrollY",z="Left",y="mousewheel",x="scrollbarX",w="event.touch",v="scrollarea",r="y",s="vertical",p="scrollX",q="touchstart",n="horizontal",o="qx.ui.core.scroll.AbstractScrollArea",l="abstract",m="update",t="scrollbarY",u="Top";
qx.Class.define(o,{extend:qx.ui.core.Widget,include:[qx.ui.core.scroll.MScrollBarFactory,qx.ui.core.scroll.MWheelHandling],type:l,construct:function(){qx.ui.core.Widget.call(this);
var F=new qx.ui.layout.Grid();
F.setColumnFlex(0,1);
F.setRowFlex(0,1);
this._setLayout(F);
this.addListener(y,this._onMouseWheel,this);
if(qx.core.Environment.get(w)){this.addListener(B,this._onTouchMove,this);
this.addListener(q,function(){this.__cO={"x":0,"y":0};
},this);
this.__cO={};
this.__nn={};
}},properties:{appearance:{refine:true,init:v},width:{refine:true,init:100},height:{refine:true,init:200},scrollbarX:{check:[h,d,E],init:h,themeable:true,apply:c},scrollbarY:{check:[h,d,E],init:h,themeable:true,apply:c},scrollbar:{group:[x,t]}},members:{__cO:null,__nn:null,_createChildControlImpl:function(G,H){var I;

switch(G){case i:I=new qx.ui.core.scroll.ScrollPane();
I.addListener(m,this._computeScrollbars,this);
I.addListener(p,this._onScrollPaneX,this);
I.addListener(A,this._onScrollPaneY,this);
this._add(I,{row:0,column:0});
break;
case j:I=this._createScrollBar(n);
I.setMinWidth(0);
I.exclude();
I.addListener(C,this._onScrollBarX,this);
I.addListener(a,this._onChangeScrollbarXVisibility,this);
this._add(I,{row:1,column:0});
break;
case k:I=this._createScrollBar(s);
I.setMinHeight(0);
I.exclude();
I.addListener(C,this._onScrollBarY,this);
I.addListener(a,this._onChangeScrollbarYVisibility,this);
this._add(I,{row:0,column:1});
break;
case g:I=new qx.ui.core.Widget();
I.setWidth(0);
I.setHeight(0);
I.exclude();
this._add(I,{row:1,column:1});
break;
}return I||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,G);
},getPaneSize:function(){return this.getChildControl(i).getInnerSize();
},getItemTop:function(J){return this.getChildControl(i).getItemTop(J);
},getItemBottom:function(K){return this.getChildControl(i).getItemBottom(K);
},getItemLeft:function(L){return this.getChildControl(i).getItemLeft(L);
},getItemRight:function(M){return this.getChildControl(i).getItemRight(M);
},scrollToX:function(N){qx.ui.core.queue.Manager.flush();
this.getChildControl(j).scrollTo(N);
},scrollByX:function(O){qx.ui.core.queue.Manager.flush();
this.getChildControl(j).scrollBy(O);
},getScrollX:function(){var P=this.getChildControl(j,true);
return P?P.getPosition():0;
},scrollToY:function(Q){qx.ui.core.queue.Manager.flush();
this.getChildControl(k).scrollTo(Q);
},scrollByY:function(R){qx.ui.core.queue.Manager.flush();
this.getChildControl(k).scrollBy(R);
},getScrollY:function(){var S=this.getChildControl(k,true);
return S?S.getPosition():0;
},_onScrollBarX:function(e){this.getChildControl(i).scrollToX(e.getData());
},_onScrollBarY:function(e){this.getChildControl(i).scrollToY(e.getData());
},_onScrollPaneX:function(e){this.scrollToX(e.getData());
},_onScrollPaneY:function(e){this.scrollToY(e.getData());
},_onTouchMove:function(e){this._onTouchMoveDirectional(D,e);
this._onTouchMoveDirectional(r,e);
e.stop();
},_onTouchMoveDirectional:function(T,e){var U=(T==D?z:u);
var W=this.getChildControl(f+T,true);
var X=this._isChildControlVisible(f+T);

if(X&&W){if(this.__cO[T]==0){var V=0;
}else{var V=-(e[b+U]()-this.__cO[T]);
}this.__cO[T]=e[b+U]();
W.scrollBy(V);
if(this.__nn[T]){clearTimeout(this.__nn[T]);
this.__nn[T]=null;
}this.__nn[T]=setTimeout(qx.lang.Function.bind(function(Y){this.__no(Y,T);
},this,V),100);
}},__no:function(ba,bb){this.__nn[bb]=null;
var bd=this._isChildControlVisible(f+bb);

if(ba==0||!bd){return;
}if(ba>0){ba=Math.max(0,ba-3);
}else{ba=Math.min(0,ba+3);
}this.__nn[bb]=setTimeout(qx.lang.Function.bind(function(be,bf){this.__no(be,bf);
},this,ba,bb),20);
var bc=this.getChildControl(f+bb,true);
bc.scrollBy(ba);
},_onChangeScrollbarXVisibility:function(e){var bg=this._isChildControlVisible(j);
var bh=this._isChildControlVisible(k);

if(!bg){this.scrollToX(0);
}bg&&bh?this._showChildControl(g):this._excludeChildControl(g);
},_onChangeScrollbarYVisibility:function(e){var bi=this._isChildControlVisible(j);
var bj=this._isChildControlVisible(k);

if(!bj){this.scrollToY(0);
}bi&&bj?this._showChildControl(g):this._excludeChildControl(g);
},_computeScrollbars:function(){var bq=this.getChildControl(i);
var content=bq.getChildren()[0];

if(!content){this._excludeChildControl(j);
this._excludeChildControl(k);
return;
}var bk=this.getInnerSize();
var bp=bq.getInnerSize();
var bn=bq.getScrollSize();
if(!bp||!bn){return;
}var br=this.getScrollbarX();
var bs=this.getScrollbarY();

if(br===h&&bs===h){var bo=bn.width>bk.width;
var bt=bn.height>bk.height;
if((bo||bt)&&!(bo&&bt)){if(bo){bt=bn.height>bp.height;
}else if(bt){bo=bn.width>bp.width;
}}}else{var bo=br===d;
var bt=bs===d;
if(bn.width>(bo?bp.width:bk.width)&&br===h){bo=true;
}
if(bn.height>(bo?bp.height:bk.height)&&bs===h){bt=true;
}}if(bo){var bm=this.getChildControl(j);
bm.show();
bm.setMaximum(Math.max(0,bn.width-bp.width));
bm.setKnobFactor((bn.width===0)?0:bp.width/bn.width);
}else{this._excludeChildControl(j);
}
if(bt){var bl=this.getChildControl(k);
bl.show();
bl.setMaximum(Math.max(0,bn.height-bp.height));
bl.setKnobFactor((bn.height===0)?0:bp.height/bn.height);
}else{this._excludeChildControl(k);
}}}});
})();
(function(){var l="dblclick",k="click",j="Boolean",h="excluded",g="visible",f="qx.event.type.Data",d="_applyOpenMode",c="Space",b="Left",a="Enter",z="changeOpenMode",y="_applyRootOpenClose",x="changeSelection",w="qx.ui.tree.Tree",v="qx.ui.tree.core.AbstractTreeItem",u="tree",t="_applyHideRoot",s="changeRoot",r="_applyRoot",q="__np",o="keypress",p="none",m="pane",n="Right";
qx.Class.define(w,{extend:qx.ui.core.scroll.AbstractScrollArea,implement:[qx.ui.core.IMultiSelection,qx.ui.form.IModelSelection,qx.ui.form.IForm],include:[qx.ui.core.MMultiSelectionHandling,qx.ui.core.MContentPadding,qx.ui.form.MModelSelection,qx.ui.form.MForm],construct:function(){qx.ui.core.scroll.AbstractScrollArea.call(this);
this.__np=new qx.ui.container.Composite(new qx.ui.layout.VBox()).set({allowShrinkY:false,allowGrowX:true});
this.getChildControl(m).add(this.__np);
this.initOpenMode();
this.initRootOpenClose();
this.addListener(x,this._onChangeSelection,this);
this.addListener(o,this._onKeyPress,this);
},events:{addItem:f,removeItem:f},properties:{openMode:{check:[k,l,p],init:l,apply:d,event:z,themeable:true},root:{check:v,init:null,nullable:true,event:s,apply:r},hideRoot:{check:j,init:false,apply:t},rootOpenClose:{check:j,init:false,apply:y},appearance:{refine:true,init:u},focusable:{refine:true,init:true}},members:{__np:null,SELECTION_MANAGER:qx.ui.tree.selection.SelectionManager,getChildrenContainer:function(){return this.__np;
},_applyRoot:function(A,B){var C=this.getChildrenContainer();

if(B&&!B.isDisposed()){C.remove(B);

if(B.hasChildren()){C.remove(B.getChildrenContainer());
}}
if(A){C.add(A);

if(A.hasChildren()){C.add(A.getChildrenContainer());
}A.setVisibility(this.getHideRoot()?h:g);
A.recursiveAddToWidgetQueue();
}},_applyHideRoot:function(D,E){var F=this.getRoot();

if(!F){return;
}F.setVisibility(D?h:g);
F.recursiveAddToWidgetQueue();
},_applyRootOpenClose:function(G,H){var I=this.getRoot();

if(!I){return;
}I.recursiveAddToWidgetQueue();
},_getContentPaddingTarget:function(){return this.__np;
},getNextNodeOf:function(J,K){if((K!==false||J.isOpen())&&J.hasChildren()){return J.getChildren()[0];
}
while(J){var parent=J.getParent();

if(!parent){return null;
}var M=parent.getChildren();
var L=M.indexOf(J);

if(L>-1&&L<M.length-1){return M[L+1];
}J=parent;
}return null;
},getPreviousNodeOf:function(N,O){var parent=N.getParent();

if(!parent){return null;
}
if(this.getHideRoot()){if(parent==this.getRoot()){if(parent.getChildren()[0]==N){return null;
}}}else{if(N==this.getRoot()){return null;
}}var R=parent.getChildren();
var P=R.indexOf(N);

if(P>0){var Q=R[P-1];

while((O!==false||Q.isOpen())&&Q.hasChildren()){var S=Q.getChildren();
Q=S[S.length-1];
}return Q;
}else{return parent;
}},getNextSiblingOf:function(T){if(T==this.getRoot()){return null;
}var parent=T.getParent();
var U=parent.getChildren();
var V=U.indexOf(T);

if(V<U.length-1){return U[V+1];
}return null;
},getPreviousSiblingOf:function(W){if(W==this.getRoot()){return null;
}var parent=W.getParent();
var X=parent.getChildren();
var Y=X.indexOf(W);

if(Y>0){return X[Y-1];
}return null;
},getItems:function(ba,bb){if(this.getRoot()!=null){return this.getRoot().getItems(ba,bb,this.getHideRoot());
}else{return [];
}},getChildren:function(){if(this.getRoot()!=null){return [this.getRoot()];
}else{return [];
}},getTreeItem:function(bc){while(bc){if(bc==this){return null;
}
if(bc instanceof qx.ui.tree.core.AbstractTreeItem){return bc;
}bc=bc.getLayoutParent();
}return null;
},_applyOpenMode:function(bd,be){if(be==k){this.removeListener(k,this._onOpen,this);
}else if(be==l){this.removeListener(l,this._onOpen,this);
}
if(bd==k){this.addListener(k,this._onOpen,this);
}else if(bd==l){this.addListener(l,this._onOpen,this);
}},_onOpen:function(e){var bf=this.getTreeItem(e.getTarget());

if(!bf||!bf.isOpenable()){return;
}bf.setOpen(!bf.isOpen());
e.stopPropagation();
},_onChangeSelection:function(e){var bh=e.getData();
for(var i=0;i<bh.length;i++){var bg=bh[i];
while(bg.getParent()!=null){bg=bg.getParent();
bg.setOpen(true);
}}},_onKeyPress:function(e){var bi=this._getLeadItem();

if(bi!==null){switch(e.getKeyIdentifier()){case b:if(bi.isOpenable()&&bi.isOpen()){bi.setOpen(false);
}else if(bi.getParent()){this.setSelection([bi.getParent()]);
}break;
case n:if(bi.isOpenable()&&!bi.isOpen()){bi.setOpen(true);
}break;
case a:case c:if(bi.isOpenable()){bi.toggleOpen();
}break;
}}}},destruct:function(){this._disposeObjects(q);
}});
})();
(function(){var c="appear",b='test',a="scoville_admin.TreeContextMenu";
qx.Class.define(a,{extend:qx.ui.menu.Menu,construct:function(d){this.app=d;
qx.ui.menu.Menu.call(this);
this.add(new qx.ui.menu.Button(b));
this.addListener(c,this.createAppearListener(this));
},members:{app:null,createAppearListener:function(e){return function(){var f=e.getOpener().getSelection()[0].classname;
};
}}});
})();
(function(){var i="execute",h="Username:",g="Server IP or Hostname:",f='scoville_admin/server.png',e="New Server",d="Cancel",c="Add Server",b="scoville_admin.NewServerPage",a="Password:";
qx.Class.define(b,{extend:qx.ui.tabview.Page,construct:function(j){this.app=j;
qx.ui.tabview.Page.call(this);
this.setLabel(e);
this.setIcon(f);
this.tabs=j.tabview;
this.buildGui();
this.setShowCloseButton(true);
this.tabs.add(this);
},members:{buttonEnter:null,buttonCancel:null,label:null,ipentry:null,buildGui:function(){this.setLayout(new qx.ui.layout.Basic());
this.buttonEnter=new qx.ui.form.Button(c);
this.buttonCancel=new qx.ui.form.Button(d);
this.iplabel=new qx.ui.basic.Label(g);
this.ipentry=new qx.ui.form.TextField();
this.userlabel=new qx.ui.basic.Label(h);
this.userentry=new qx.ui.form.TextField();
this.passwordlabel=new qx.ui.basic.Label(a);
this.passwordentry=new qx.ui.form.PasswordField();
this.buttonEnter.addListener(i,this.enterNewServerCallback(this));
this.buttonCancel.addListener(i,this.cancelCallback(this));
this.add(this.iplabel,{top:100,left:100});
this.add(this.ipentry,{top:100,left:250});
this.add(this.userlabel,{top:125,left:100});
this.add(this.userentry,{top:125,left:250});
this.add(this.passwordlabel,{top:150,left:100});
this.add(this.passwordentry,{top:150,left:250});
this.add(this.buttonCancel,{top:175,left:100});
this.add(this.buttonEnter,{top:175,left:250});
},enterNewServer:function(){},cancelCallback:function(k){return function(){k.tabs.remove(k);
};
},enterNewServerCallback:function(l){var r=function(){var m=l.ipentry.getValue();
var n=l.userentry.getValue();
var o=l.passwordentry.getValue();
l.app.loadServer(m,l,n,o);
l.tabs.remove(l);
};
return r;
}}});
})();
(function(){var k="showingPlaceholder",j="",i="engine.name",h="none",g="qx.dynlocale",f="Boolean",d="A",c="color",b="qx.event.type.Data",a="readonly",bf="placeholder",be="input",bd="focusin",bc="visibility",bb="gecko",ba="focusout",Y="changeLocale",X="hidden",W="absolute",V="readOnly",r="text",s="_applyTextAlign",p="px",q="RegExp",n=")",o="syncAppearance",l="changeValue",m="engine.version",v="change",w="changeStatus",E="textAlign",C="focused",L="center",G="visible",R="disabled",P="url(",y="String",U="resize",T="qx.ui.form.AbstractField",S="transparent",x="spellcheck",A="false",B="right",D="PositiveInteger",F="abstract",H="block",M="css.placeholder",Q="webkit",t="_applyReadOnly",u="_applyPlaceholder",z="left",K="off",J="mshtml",I="qx/static/blank.gif",O="text-placeholder",N="changeReadOnly";
qx.Class.define(T,{extend:qx.ui.core.Widget,implement:[qx.ui.form.IStringForm,qx.ui.form.IForm],include:[qx.ui.form.MForm],type:F,construct:function(bg){qx.ui.core.Widget.call(this);
this.__nq=!qx.core.Environment.get(M)||(qx.core.Environment.get(i)==bb&&parseFloat(qx.core.Environment.get(m))>=2);

if(bg!=null){this.setValue(bg);
}this.getContentElement().addListener(v,this._onChangeContent,this);
if(this.__nq){this.addListener(o,this._syncPlaceholder,this);
}if(qx.core.Environment.get(g)){qx.locale.Manager.getInstance().addListener(Y,this._onChangeLocale,this);
}},events:{"input":b,"changeValue":b},properties:{textAlign:{check:[z,L,B],nullable:true,themeable:true,apply:s},readOnly:{check:f,apply:t,event:N,init:false},selectable:{refine:true,init:true},focusable:{refine:true,init:true},maxLength:{check:D,init:Infinity},liveUpdate:{check:f,init:false},placeholder:{check:y,nullable:true,apply:u},filter:{check:q,nullable:true,init:null}},members:{__nr:true,__ns:null,__nt:null,__nu:null,__nq:true,__jF:null,__jJ:null,getFocusElement:function(){var bh=this.getContentElement();

if(bh){return bh;
}},_createInputElement:function(){return new qx.html.Input(r);
},renderLayout:function(bi,top,bj,bk){var bl=this._updateInsets;
var bp=qx.ui.core.Widget.prototype.renderLayout.call(this,bi,top,bj,bk);
if(!bp){return;
}var bn=bp.size||bl;
var bq=p;

if(bn||bp.local||bp.margin){var bm=this.getInsets();
var innerWidth=bj-bm.left-bm.right;
var innerHeight=bk-bm.top-bm.bottom;
innerWidth=innerWidth<0?0:innerWidth;
innerHeight=innerHeight<0?0:innerHeight;
}var bo=this.getContentElement();
if(bl&&this.__nq){this.__nx().setStyles({"left":bm.left+bq,"top":bm.top+bq});
}
if(bn){if(this.__nq){this.__nx().setStyles({"width":innerWidth+bq,"height":innerHeight+bq});
}bo.setStyles({"width":innerWidth+bq,"height":innerHeight+bq});
this._renderContentElement(innerHeight,bo);
}},_renderContentElement:function(innerHeight,br){},_createContentElement:function(){var bs=this._createInputElement();
bs.setStyles({"border":h,"padding":0,"margin":0,"display":H,"background":S,"outline":h,"appearance":h,"position":W,"autoComplete":K});
bs.setSelectable(this.getSelectable());
bs.setEnabled(this.getEnabled());
bs.addListener(be,this._onHtmlInput,this);
bs.setAttribute(x,A);
if(qx.core.Environment.get(i)==Q||qx.core.Environment.get(i)==bb){bs.setStyle(U,h);
}if((qx.core.Environment.get(i)==J)){bs.setStyles({backgroundImage:P+qx.util.ResourceManager.getInstance().toUri(I)+n});
}return bs;
},_applyEnabled:function(bt,bu){qx.ui.core.Widget.prototype._applyEnabled.call(this,bt,bu);
this.getContentElement().setEnabled(bt);

if(this.__nq){if(bt){this._showPlaceholder();
}else{this._removePlaceholder();
}}else{var bv=this.getContentElement();
bv.setAttribute(bf,bt?this.getPlaceholder():j);
}},__nv:{width:16,height:16},_getContentHint:function(){return {width:this.__nv.width*10,height:this.__nv.height||16};
},_applyFont:function(bw,bx){if(bx&&this.__jF&&this.__jJ){this.__jF.removeListenerById(this.__jJ);
this.__jJ=null;
}var by;

if(bw){this.__jF=qx.theme.manager.Font.getInstance().resolve(bw);

if(this.__jF instanceof qx.bom.webfonts.WebFont){this.__jJ=this.__jF.addListener(w,this._onWebFontStatusChange,this);
}by=this.__jF.getStyles();
}else{by=qx.bom.Font.getDefaultStyles();
}this.getContentElement().setStyles(by);
if(this.__nq){this.__nx().setStyles(by);
}if(bw){this.__nv=qx.bom.Label.getTextSize(d,by);
}else{delete this.__nv;
}qx.ui.core.queue.Layout.add(this);
},_applyTextColor:function(bz,bA){if(bz){this.getContentElement().setStyle(c,qx.theme.manager.Color.getInstance().resolve(bz));
}else{this.getContentElement().removeStyle(c);
}},tabFocus:function(){qx.ui.core.Widget.prototype.tabFocus.call(this);
this.selectAllText();
},_getTextSize:function(){return this.__nv;
},_onHtmlInput:function(e){var bE=e.getData();
var bD=true;
this.__nr=false;
if(this.getFilter()!=null){var bF=j;
var bB=bE.search(this.getFilter());
var bC=bE;

while(bB>=0){bF=bF+(bC.charAt(bB));
bC=bC.substring(bB+1,bC.length);
bB=bC.search(this.getFilter());
}
if(bF!=bE){bD=false;
bE=bF;
this.getContentElement().setValue(bE);
}}if(bE.length>this.getMaxLength()){bD=false;
this.getContentElement().setValue(bE.substr(0,this.getMaxLength()));
}if(bD){this.fireDataEvent(be,bE,this.__nu);
this.__nu=bE;
if(this.getLiveUpdate()){this.__nw(bE);
}}},_onWebFontStatusChange:function(bG){if(bG.getData().valid===true){var bH=this.__jF.getStyles();
this.__nv=qx.bom.Label.getTextSize(d,bH);
qx.ui.core.queue.Layout.add(this);
}},__nw:function(bI){var bJ=this.__nt;
this.__nt=bI;

if(bJ!=bI){this.fireNonBubblingEvent(l,qx.event.type.Data,[bI,bJ]);
}},setValue:function(bK){if(bK===null){if(this.__nr){return bK;
}bK=j;
this.__nr=true;
}else{this.__nr=false;
if(this.__nq){this._removePlaceholder();
}}
if(qx.lang.Type.isString(bK)){var bM=this.getContentElement();

if(bK.length>this.getMaxLength()){bK=bK.substr(0,this.getMaxLength());
}
if(bM.getValue()!=bK){var bN=bM.getValue();
bM.setValue(bK);
var bL=this.__nr?null:bK;
this.__nt=bN;
this.__nw(bL);
}if(this.__nq){this._showPlaceholder();
}return bK;
}throw new Error("Invalid value type: "+bK);
},getValue:function(){var bO=this.getContentElement().getValue();
return this.__nr?null:bO;
},resetValue:function(){this.setValue(null);
},_onChangeContent:function(e){this.__nr=e.getData()===null;
this.__nw(e.getData());
},getTextSelection:function(){return this.getContentElement().getTextSelection();
},getTextSelectionLength:function(){return this.getContentElement().getTextSelectionLength();
},getTextSelectionStart:function(){return this.getContentElement().getTextSelectionStart();
},getTextSelectionEnd:function(){return this.getContentElement().getTextSelectionEnd();
},setTextSelection:function(bP,bQ){this.getContentElement().setTextSelection(bP,bQ);
},clearTextSelection:function(){this.getContentElement().clearTextSelection();
},selectAllText:function(){this.setTextSelection(0);
},_showPlaceholder:function(){var bS=this.getValue()||j;
var bR=this.getPlaceholder();

if(bR!=null&&bS==j&&!this.hasState(C)&&!this.hasState(R)){if(this.hasState(k)){this._syncPlaceholder();
}else{this.addState(k);
}}},_removePlaceholder:function(){if(this.hasState(k)){this.__nx().setStyle(bc,X);
this.removeState(k);
}},_syncPlaceholder:function(){if(this.hasState(k)){this.__nx().setStyle(bc,G);
}},__nx:function(){if(this.__ns==null){this.__ns=new qx.html.Label();
var bT=qx.theme.manager.Color.getInstance();
this.__ns.setStyles({"visibility":X,"zIndex":6,"position":W,"color":bT.resolve(O)});
this.getContainerElement().add(this.__ns);
}return this.__ns;
},_onChangeLocale:qx.core.Environment.select(g,{"true":function(e){var content=this.getPlaceholder();

if(content&&content.translate){this.setPlaceholder(content.translate());
}},"false":null}),_applyPlaceholder:function(bU,bV){if(this.__nq){this.__nx().setValue(bU);

if(bU!=null){this.addListener(bd,this._removePlaceholder,this);
this.addListener(ba,this._showPlaceholder,this);
this._showPlaceholder();
}else{this.removeListener(bd,this._removePlaceholder,this);
this.removeListener(ba,this._showPlaceholder,this);
this._removePlaceholder();
}}else{if(this.getEnabled()){this.getContentElement().setAttribute(bf,bU);
}}},_applyTextAlign:function(bW,bX){this.getContentElement().setStyle(E,bW);
},_applyReadOnly:function(bY,ca){var cb=this.getContentElement();
cb.setAttribute(V,bY);

if(bY){this.addState(a);
this.setFocusable(false);
}else{this.removeState(a);
this.setFocusable(true);
}}},destruct:function(){this.__ns=this.__jF=null;

if(qx.core.Environment.get(g)){qx.locale.Manager.getInstance().removeListener(Y,this._onChangeLocale,this);
}
if(this.__jF&&this.__jJ){this.__jF.removeListenerById(this.__jJ);
}}});
})();
(function(){var n="wrap",m="value",l="textarea",k="engine.name",j="none",i="",h="overflow",g="input",f="qx.html.Input",e="select",b="disabled",d="read-only",c="overflowX",a="overflowY";
qx.Class.define(f,{extend:qx.html.Element,construct:function(o,p,q){if(o===e||o===l){var r=o;
}else{r=g;
}qx.html.Element.call(this,r,p,q);
this.__ny=o;
},members:{__ny:null,__nz:null,__nA:null,_createDomElement:function(){return qx.bom.Input.create(this.__ny);
},_applyProperty:function(name,s){qx.html.Element.prototype._applyProperty.call(this,name,s);
var t=this.getDomElement();

if(name===m){qx.bom.Input.setValue(t,s);
}else if(name===n){qx.bom.Input.setWrap(t,s);
this.setStyle(h,t.style.overflow,true);
this.setStyle(c,t.style.overflowX,true);
this.setStyle(a,t.style.overflowY,true);
}},setEnabled:qx.core.Environment.select(k,{"webkit":function(u){this.__nA=u;

if(!u){this.setStyles({"userModify":d,"userSelect":j});
}else{this.setStyles({"userModify":null,"userSelect":this.__nz?null:j});
}},"default":function(v){this.setAttribute(b,v===false);
}}),setSelectable:qx.core.Environment.select(k,{"webkit":function(w){this.__nz=w;
qx.html.Element.prototype.setSelectable.call(this,this.__nA&&w);
},"default":function(x){qx.html.Element.prototype.setSelectable.call(this,x);
}}),setValue:function(y){var z=this.getDomElement();

if(z){if(z.value!=y){qx.bom.Input.setValue(z,y);
}}else{this._setProperty(m,y);
}return this;
},getValue:function(){var A=this.getDomElement();

if(A){return qx.bom.Input.getValue(A);
}return this._getProperty(m)||i;
},setWrap:function(B,C){if(this.__ny===l){this._setProperty(n,B,C);
}else{throw new Error("Text wrapping is only support by textareas!");
}return this;
},getWrap:function(){if(this.__ny===l){return this._getProperty(n);
}else{throw new Error("Text wrapping is only support by textareas!");
}}}});
})();
(function(){var m="input",k="engine.name",j="change",h="text",g="password",f="engine.version",d="radio",c="textarea",b="checkbox",a="keypress",A="browser.documentmode",z="opera",y="keyup",x="mshtml",w="blur",v="keydown",u="propertychange",t="browser.version",s="select-multiple",r="value",p="select",q="qx.event.handler.Input",n="checked";
qx.Class.define(q,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(){qx.core.Object.call(this);
this._onChangeCheckedWrapper=qx.lang.Function.listener(this._onChangeChecked,this);
this._onChangeValueWrapper=qx.lang.Function.listener(this._onChangeValue,this);
this._onInputWrapper=qx.lang.Function.listener(this._onInput,this);
this._onPropertyWrapper=qx.lang.Function.listener(this._onProperty,this);
if((qx.core.Environment.get(k)==z)){this._onKeyDownWrapper=qx.lang.Function.listener(this._onKeyDown,this);
this._onKeyUpWrapper=qx.lang.Function.listener(this._onKeyUp,this);
this._onBlurWrapper=qx.lang.Function.listener(this._onBlur,this);
}},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{input:1,change:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:false},members:{__nB:false,__nC:null,__nt:null,__nu:null,canHandleEvent:function(B,C){var D=B.tagName.toLowerCase();

if(C===m&&(D===m||D===c)){return true;
}
if(C===j&&(D===m||D===c||D===p)){return true;
}return false;
},registerEvent:function(E,F,G){if(qx.core.Environment.get(k)==x&&(qx.core.Environment.get(f)<9||(qx.core.Environment.get(f)>=9&&qx.core.Environment.get(A)<9))){if(!E.__nD){var H=E.tagName.toLowerCase();
var I=E.type;

if(I===h||I===g||H===c||I===b||I===d){qx.bom.Event.addNativeListener(E,u,this._onPropertyWrapper);
}
if(I!==b&&I!==d){qx.bom.Event.addNativeListener(E,j,this._onChangeValueWrapper);
}
if(I===h||I===g){this._onKeyPressWrapped=qx.lang.Function.listener(this._onKeyPress,this,E);
qx.bom.Event.addNativeListener(E,a,this._onKeyPressWrapped);
}E.__nD=true;
}}else{if(F===m){this.__nE(E);
}else if(F===j){if(E.type===d||E.type===b){qx.bom.Event.addNativeListener(E,j,this._onChangeCheckedWrapper);
}else{qx.bom.Event.addNativeListener(E,j,this._onChangeValueWrapper);
}if((qx.core.Environment.get(k)==z)||(qx.core.Environment.get(k)==x)){if(E.type===h||E.type===g){this._onKeyPressWrapped=qx.lang.Function.listener(this._onKeyPress,this,E);
qx.bom.Event.addNativeListener(E,a,this._onKeyPressWrapped);
}}}}},__nE:qx.core.Environment.select(k,{"mshtml":function(J){if(qx.core.Environment.get(f)>=9&&qx.core.Environment.get(A)>=9){qx.bom.Event.addNativeListener(J,m,this._onInputWrapper);

if(J.type===h||J.type===g){this._inputFixWrapper=qx.lang.Function.listener(this._inputFix,this,J);
qx.bom.Event.addNativeListener(J,y,this._inputFixWrapper);
}}},"webkit":function(K){var L=K.tagName.toLowerCase();
if(parseFloat(qx.core.Environment.get(f))<532&&L==c){qx.bom.Event.addNativeListener(K,a,this._onInputWrapper);
}qx.bom.Event.addNativeListener(K,m,this._onInputWrapper);
},"opera":function(M){qx.bom.Event.addNativeListener(M,y,this._onKeyUpWrapper);
qx.bom.Event.addNativeListener(M,v,this._onKeyDownWrapper);
qx.bom.Event.addNativeListener(M,w,this._onBlurWrapper);
qx.bom.Event.addNativeListener(M,m,this._onInputWrapper);
},"default":function(N){qx.bom.Event.addNativeListener(N,m,this._onInputWrapper);
}}),unregisterEvent:function(O,P){if(qx.core.Environment.get(k)==x&&qx.core.Environment.get(f)<9&&qx.core.Environment.get(A)<9){if(O.__nD){var Q=O.tagName.toLowerCase();
var R=O.type;

if(R===h||R===g||Q===c||R===b||R===d){qx.bom.Event.removeNativeListener(O,u,this._onPropertyWrapper);
}
if(R!==b&&R!==d){qx.bom.Event.removeNativeListener(O,j,this._onChangeValueWrapper);
}
if(R===h||R===g){qx.bom.Event.removeNativeListener(O,a,this._onKeyPressWrapped);
}
try{delete O.__nD;
}catch(S){O.__nD=null;
}}}else{if(P===m){this.__nF(O);
}else if(P===j){if(O.type===d||O.type===b){qx.bom.Event.removeNativeListener(O,j,this._onChangeCheckedWrapper);
}else{qx.bom.Event.removeNativeListener(O,j,this._onChangeValueWrapper);
}}
if((qx.core.Environment.get(k)==z)||(qx.core.Environment.get(k)==x)){if(O.type===h||O.type===g){qx.bom.Event.removeNativeListener(O,a,this._onKeyPressWrapped);
}}}},__nF:qx.core.Environment.select(k,{"mshtml":function(T){if(qx.core.Environment.get(f)>=9&&qx.core.Environment.get(A)>=9){qx.bom.Event.removeNativeListener(T,m,this._onInputWrapper);

if(T.type===h||T.type===g){qx.bom.Event.removeNativeListener(T,y,this._inputFixWrapper);
}}},"webkit":function(U){var V=U.tagName.toLowerCase();
if(parseFloat(qx.core.Environment.get(f))<532&&V==c){qx.bom.Event.removeNativeListener(U,a,this._onInputWrapper);
}qx.bom.Event.removeNativeListener(U,m,this._onInputWrapper);
},"opera":function(W){qx.bom.Event.removeNativeListener(W,y,this._onKeyUpWrapper);
qx.bom.Event.removeNativeListener(W,v,this._onKeyDownWrapper);
qx.bom.Event.removeNativeListener(W,w,this._onBlurWrapper);
qx.bom.Event.removeNativeListener(W,m,this._onInputWrapper);
},"default":function(X){qx.bom.Event.removeNativeListener(X,m,this._onInputWrapper);
}}),_onKeyPress:qx.core.Environment.select(k,{"mshtml|opera":function(e,Y){if(e.keyCode===13){if(Y.value!==this.__nt){this.__nt=Y.value;
qx.event.Registration.fireEvent(Y,j,qx.event.type.Data,[Y.value]);
}}},"default":null}),_inputFix:qx.core.Environment.select(k,{"mshtml":function(e,ba){if(e.keyCode===46||e.keyCode===8){if(ba.value!==this.__nu){this.__nu=ba.value;
qx.event.Registration.fireEvent(ba,m,qx.event.type.Data,[ba.value]);
}}},"default":null}),_onKeyDown:qx.core.Environment.select(k,{"opera":function(e){if(e.keyCode===13){this.__nB=true;
}},"default":null}),_onKeyUp:qx.core.Environment.select(k,{"opera":function(e){if(e.keyCode===13){this.__nB=false;
}},"default":null}),_onBlur:qx.core.Environment.select(k,{"opera":function(e){if(this.__nC&&qx.core.Environment.get(t)<10.6){window.clearTimeout(this.__nC);
}},"default":null}),_onInput:qx.event.GlobalError.observeMethod(function(e){var bc=qx.bom.Event.getTarget(e);
var bb=bc.tagName.toLowerCase();
if(!this.__nB||bb!==m){if((qx.core.Environment.get(k)==z)&&qx.core.Environment.get(t)<10.6){this.__nC=window.setTimeout(function(){qx.event.Registration.fireEvent(bc,m,qx.event.type.Data,[bc.value]);
},0);
}else{qx.event.Registration.fireEvent(bc,m,qx.event.type.Data,[bc.value]);
}}}),_onChangeValue:qx.event.GlobalError.observeMethod(function(e){var be=qx.bom.Event.getTarget(e);
var bd=be.value;

if(be.type===s){var bd=[];

for(var i=0,o=be.options,l=o.length;i<l;i++){if(o[i].selected){bd.push(o[i].value);
}}}qx.event.Registration.fireEvent(be,j,qx.event.type.Data,[bd]);
}),_onChangeChecked:qx.event.GlobalError.observeMethod(function(e){var bf=qx.bom.Event.getTarget(e);

if(bf.type===d){if(bf.checked){qx.event.Registration.fireEvent(bf,j,qx.event.type.Data,[bf.value]);
}}else{qx.event.Registration.fireEvent(bf,j,qx.event.type.Data,[bf.checked]);
}}),_onProperty:qx.core.Environment.select(k,{"mshtml":qx.event.GlobalError.observeMethod(function(e){var bg=qx.bom.Event.getTarget(e);
var bh=e.propertyName;

if(bh===r&&(bg.type===h||bg.type===g||bg.tagName.toLowerCase()===c)){if(!bg.$$inValueSet){qx.event.Registration.fireEvent(bg,m,qx.event.type.Data,[bg.value]);
}}else if(bh===n){if(bg.type===b){qx.event.Registration.fireEvent(bg,j,qx.event.type.Data,[bg.checked]);
}else if(bg.checked){qx.event.Registration.fireEvent(bg,j,qx.event.type.Data,[bg.value]);
}}}),"default":function(){}})},defer:function(bi){qx.event.Registration.addHandler(bi);
}});
})();
(function(){var v="",u="select",t="engine.name",s="soft",r="off",q="textarea",p="auto",o="wrap",n="text",m="mshtml",d="number",k="checkbox",g="select-one",c="input",b="option",f="value",e="radio",h="qx.bom.Input",a="nowrap",j="normal";
qx.Class.define(h,{statics:{__gU:{text:1,textarea:1,select:1,checkbox:1,radio:1,password:1,hidden:1,submit:1,image:1,file:1,search:1,reset:1,button:1},create:function(w,x,y){var x=x?qx.lang.Object.clone(x):{};
var z;

if(w===q||w===u){z=w;
}else{z=c;
x.type=w;
}return qx.bom.Element.create(z,x,y);
},setValue:function(A,B){var G=A.nodeName.toLowerCase();
var D=A.type;
var Array=qx.lang.Array;
var H=qx.lang.Type;

if(typeof B===d){B+=v;
}
if((D===k||D===e)){if(H.isArray(B)){A.checked=Array.contains(B,A.value);
}else{A.checked=A.value==B;
}}else if(G===u){var C=H.isArray(B);
var I=A.options;
var E,F;

for(var i=0,l=I.length;i<l;i++){E=I[i];
F=E.getAttribute(f);

if(F==null){F=E.text;
}E.selected=C?Array.contains(B,F):B==F;
}
if(C&&B.length==0){A.selectedIndex=-1;
}}else if((D===n||D===q)&&(qx.core.Environment.get(t)==m)){A.$$inValueSet=true;
A.value=B;
A.$$inValueSet=null;
}else{A.value=B;
}},getValue:function(J){var P=J.nodeName.toLowerCase();

if(P===b){return (J.attributes.value||{}).specified?J.value:J.text;
}
if(P===u){var K=J.selectedIndex;
if(K<0){return null;
}var Q=[];
var S=J.options;
var R=J.type==g;
var O=qx.bom.Input;
var N;
for(var i=R?K:0,M=R?K+1:S.length;i<M;i++){var L=S[i];

if(L.selected){N=O.getValue(L);
if(R){return N;
}Q.push(N);
}}return Q;
}else{return (J.value||v).replace(/\r/g,v);
}},setWrap:qx.core.Environment.select(t,{"mshtml":function(T,U){var W=U?s:r;
var V=U?p:v;
T.wrap=W;
T.style.overflowY=V;
},"gecko|webkit":function(X,Y){var bb=Y?s:r;
var ba=Y?v:p;
X.setAttribute(o,bb);
X.style.overflow=ba;
},"default":function(bc,bd){bc.style.whiteSpace=bd?j:a;
}})}});
})();
(function(){var f="mshtml",e="engine.name",d="qx.ui.form.TextField",c='px',b="textfield",a="engine.version";
qx.Class.define(d,{extend:qx.ui.form.AbstractField,properties:{appearance:{refine:true,init:b},allowGrowY:{refine:true,init:false},allowShrinkY:{refine:true,init:false}},members:{_renderContentElement:function(innerHeight,g){if((qx.core.Environment.get(e)==f)&&qx.core.Environment.get(a)<9){g.setStyles({"line-height":innerHeight+c});
}}}});
})();
(function(){var c="password",b="qx.ui.form.PasswordField",a="input";
qx.Class.define(b,{extend:qx.ui.form.TextField,members:{_createInputElement:function(){var d=new qx.html.Input(c);
d.addListener(a,this._onHtmlInput,this);
return d;
}}});
})();
(function(){var bB="white",bA="#EEEEEE",bz="#E4E4E4",by="#F3F3F3",bx="#F0F0F0",bw="#E8E8E8",bv="#CCCCCC",bu="#EFEFEF",bt="#1a1a1a",bs="#00204D",bh="gray",bg="#F4F4F4",bf="#fffefe",be="#AFAFAF",bd="#084FAB",bc="#FCFCFC",bb="#CCC",ba="#F2F2F2",Y="black",X="#ffffdd",bI="#b6b6b6",bJ="#004DAD",bG="#BABABA",bH="#005BC3",bE="#334866",bF="#CECECE",bC="#D9D9D9",bD="#D8D8D8",bK="#99C3FE",bL="#001533",bl="#B3B3B3",bk="#D5D5D5",bn="#C3C3C3",bm="#DDDDDD",bp="#FF9999",bo="css.rgba",br="#E8E8E9",bq="#084FAA",bj="#C5C5C5",bi="rgba(0, 0, 0, 0.4)",a="#DBDBDB",b="#4a4a4a",c="#83BAEA",d="#D7E7F4",e="#07125A",f="#FAF2F2",g="#87AFE7",h="#F7EAEA",i="#777D8D",j="#FBFBFB",bP="#CACACA",bO="#909090",bN="#9B9B9B",bM="#F0F9FE",bT="#314a6e",bS="#B4B4B4",bR="#787878",bQ="qx.theme.modern.Color",bV="#000000",bU="#26364D",H="#A7A7A7",I="#D1E4FF",F="#5CB0FD",G="#EAEAEA",L="#003B91",M="#80B4EF",J="#FF6B78",K="#949494",D="#808080",E="#930000",r="#7B7B7B",q="#C82C2C",t="#DFDFDF",s="#B6B6B6",n="#0880EF",m="#4d4d4d",p="#f4f4f4",o="#7B7A7E",l="#D0D0D0",k="#f8f8f8",R="#404955",S="#959595",T="#AAAAAA",U="#F7E9E9",N="#314A6E",O="#C72B2B",P="#FAFAFA",Q="#FBFCFB",V="#B2D2FF",W="#666666",B="#CBC8CD",A="#999999",z="#8EB8D6",y="#b8b8b8",x="#727272",w="#33508D",v="#F1F1F1",u="#990000",C="#00368A";
qx.Theme.define(bQ,{colors:{"background-application":t,"background-pane":by,"background-light":bc,"background-medium":bA,"background-splitpane":be,"background-tip":X,"background-tip-error":O,"background-odd":bz,"htmlarea-background":bB,"progressbar-background":bB,"text-light":bO,"text-gray":b,"text-label":bt,"text-title":bT,"text-input":bV,"text-hovered":bL,"text-disabled":o,"text-selected":bf,"text-active":bU,"text-inactive":R,"text-placeholder":B,"border-inner-scrollbar":bB,"border-main":m,"menu-separator-top":bj,"menu-separator-bottom":P,"border-separator":D,"border-toolbar-button-outer":bI,"border-toolbar-border-inner":k,"border-toolbar-separator-right":p,"border-toolbar-separator-left":y,"border-input":bE,"border-inner-input":bB,"border-disabled":s,"border-pane":bs,"border-button":W,"border-column":bv,"border-focused":bK,"invalid":u,"border-focused-invalid":bp,"border-dragover":w,"keyboard-focus":Y,"table-pane":by,"table-focus-indicator":n,"table-row-background-focused-selected":bd,"table-row-background-focused":M,"table-row-background-selected":bd,"table-row-background-even":by,"table-row-background-odd":bz,"table-row-selected":bf,"table-row":bt,"table-row-line":bb,"table-column-line":bb,"table-header-hovered":bB,"progressive-table-header":T,"progressive-table-header-border-right":ba,"progressive-table-row-background-even":bg,"progressive-table-row-background-odd":bz,"progressive-progressbar-background":bh,"progressive-progressbar-indicator-done":bv,"progressive-progressbar-indicator-undone":bB,"progressive-progressbar-percent-background":bh,"progressive-progressbar-percent-text":bB,"selected-start":bJ,"selected-end":C,"tabview-background":e,"shadow":qx.core.Environment.get(bo)?bi:A,"pane-start":j,"pane-end":bx,"group-background":bw,"group-border":bS,"radiobutton-background":bu,"checkbox-border":N,"checkbox-focus":g,"checkbox-hovered":V,"checkbox-hovered-inner":I,"checkbox-inner":bA,"checkbox-start":bz,"checkbox-end":by,"checkbox-disabled-border":bR,"checkbox-disabled-inner":bP,"checkbox-disabled-start":l,"checkbox-disabled-end":bD,"checkbox-hovered-inner-invalid":f,"checkbox-hovered-invalid":U,"radiobutton-checked":bH,"radiobutton-disabled":bk,"radiobutton-checked-disabled":r,"radiobutton-hovered-invalid":h,"tooltip-error":q,"scrollbar-start":bv,"scrollbar-end":v,"scrollbar-slider-start":bA,"scrollbar-slider-end":bn,"button-border-disabeld":S,"button-start":bx,"button-end":be,"button-disabled-start":bg,"button-disabled-end":bG,"button-hovered-start":bM,"button-hovered-end":z,"button-focused":c,"border-invalid":E,"input-start":bx,"input-end":Q,"input-focused-start":d,"input-focused-end":F,"input-focused-inner-invalid":J,"input-border-disabled":bN,"input-border-inner":bB,"toolbar-start":bu,"toolbar-end":bm,"window-border":bs,"window-border-caption":x,"window-caption-active-text":bB,"window-caption-active-start":bq,"window-caption-active-end":L,"window-caption-inactive-start":ba,"window-caption-inactive-end":a,"window-statusbar-background":bu,"tabview-start":bc,"tabview-end":bA,"tabview-inactive":i,"tabview-inactive-start":G,"tabview-inactive-end":bF,"table-header-start":bw,"table-header-end":bl,"menu-start":br,"menu-end":bC,"menubar-start":bw,"groupitem-start":H,"groupitem-end":K,"groupitem-text":bB,"virtual-row-layer-background-even":bB,"virtual-row-layer-background-odd":bB}});
})();
(function(){var a="scoville_admin.theme.Color";
qx.Theme.define(a,{extend:qx.theme.modern.Color,colors:{}});
})();
(function(){var k="_applyBoxShadow",j="px ",i="Integer",h="shadowHorizontalLength",g="box-shadow",f="-webkit-box-shadow",e="shadowVerticalLength",d="-moz-box-shadow",c="shorthand",b="qx.ui.decoration.MBoxShadow",a="Color";
qx.Mixin.define(b,{properties:{shadowHorizontalLength:{nullable:true,check:i,apply:k},shadowVerticalLength:{nullable:true,check:i,apply:k},shadowBlurRadius:{nullable:true,check:i,apply:k},shadowColor:{nullable:true,check:a,apply:k},shadowLength:{group:[h,e],mode:c}},members:{_styleBoxShadow:function(l){var m=qx.theme.manager.Color.getInstance();
var p=m.resolve(this.getShadowColor());

if(p!=null){var q=this.getShadowVerticalLength()||0;
var n=this.getShadowHorizontalLength()||0;
var blur=this.getShadowBlurRadius()||0;
var o=n+j+q+j+blur+j+p;
l[d]=o;
l[f]=o;
l[g]=o;
}},_applyBoxShadow:function(){}}});
})();
(function(){var d="qx.ui.decoration.MBackgroundColor",c="Color",b="_applyBackgroundColor",a="";
qx.Mixin.define(d,{properties:{backgroundColor:{check:c,nullable:true,apply:b}},members:{_tintBackgroundColor:function(e,f,g){var h=qx.theme.manager.Color.getInstance();

if(f==null){f=this.getBackgroundColor();
}g.backgroundColor=h.resolve(f)||a;
},_resizeBackgroundColor:function(i,j,k){var l=this.getInsets();
j-=l.left+l.right;
k-=l.top+l.bottom;
return {left:l.left,top:l.top,width:j,height:k};
},_applyBackgroundColor:function(){}}});
})();
(function(){var t="_applyBackgroundImage",s="repeat",r="",q="mshtml",p="engine.name",o="backgroundPositionX",n='<div style="',m="backgroundPositionY",l='</div>',k="no-repeat",d="engine.version",j="scale",g='">',c=" ",b="repeat-x",f="repeat-y",e="hidden",h="qx.ui.decoration.MBackgroundImage",a="String",i="browser.quirksmode";
qx.Mixin.define(h,{properties:{backgroundImage:{check:a,nullable:true,apply:t},backgroundRepeat:{check:[s,b,f,k,j],init:s,apply:t},backgroundPositionX:{nullable:true,apply:t},backgroundPositionY:{nullable:true,apply:t},backgroundPosition:{group:[m,o]}},members:{_generateMarkup:this._generateBackgroundMarkup,_generateBackgroundMarkup:function(u,content){var y=r;
var x=this.getBackgroundImage();
var w=this.getBackgroundRepeat();
var top=this.getBackgroundPositionY();

if(top==null){top=0;
}var z=this.getBackgroundPositionX();

if(z==null){z=0;
}u.backgroundPosition=z+c+top;
if(x){var v=qx.util.AliasManager.getInstance().resolve(x);
y=qx.bom.element.Decoration.create(v,w,u);
}else{if((qx.core.Environment.get(p)==q)){if(parseFloat(qx.core.Environment.get(d))<7||qx.core.Environment.get(i)){u.overflow=e;
}}
if(!content){content=r;
}y=n+qx.bom.element.Style.compile(u)+g+content+l;
}return y;
},_applyBackgroundImage:function(){}}});
})();
(function(){var j="solid",i="_applyStyle",h="double",g="px ",f="dotted",e="_applyWidth",d="Color",c="",b="dashed",a="Number",D=" ",C="shorthand",B="widthTop",A="styleRight",z="styleBottom",y="widthBottom",x="widthLeft",w="styleTop",v="colorBottom",u="styleLeft",q="widthRight",r="colorLeft",o="colorRight",p="colorTop",m="border-top",n="border-left",k="border-right",l="qx.ui.decoration.MSingleBorder",s="border-bottom",t="absolute";
qx.Mixin.define(l,{properties:{widthTop:{check:a,init:0,apply:e},widthRight:{check:a,init:0,apply:e},widthBottom:{check:a,init:0,apply:e},widthLeft:{check:a,init:0,apply:e},styleTop:{nullable:true,check:[j,f,b,h],init:j,apply:i},styleRight:{nullable:true,check:[j,f,b,h],init:j,apply:i},styleBottom:{nullable:true,check:[j,f,b,h],init:j,apply:i},styleLeft:{nullable:true,check:[j,f,b,h],init:j,apply:i},colorTop:{nullable:true,check:d,apply:i},colorRight:{nullable:true,check:d,apply:i},colorBottom:{nullable:true,check:d,apply:i},colorLeft:{nullable:true,check:d,apply:i},left:{group:[x,u,r]},right:{group:[q,A,o]},top:{group:[B,w,p]},bottom:{group:[y,z,v]},width:{group:[B,q,y,x],mode:C},style:{group:[w,A,z,u],mode:C},color:{group:[p,o,v,r],mode:C}},members:{_styleBorder:function(E){var F=qx.theme.manager.Color.getInstance();
var G=this.getWidthTop();

if(G>0){E[m]=G+g+this.getStyleTop()+D+(F.resolve(this.getColorTop())||c);
}var G=this.getWidthRight();

if(G>0){E[k]=G+g+this.getStyleRight()+D+(F.resolve(this.getColorRight())||c);
}var G=this.getWidthBottom();

if(G>0){E[s]=G+g+this.getStyleBottom()+D+(F.resolve(this.getColorBottom())||c);
}var G=this.getWidthLeft();

if(G>0){E[n]=G+g+this.getStyleLeft()+D+(F.resolve(this.getColorLeft())||c);
}E.position=t;
E.top=0;
E.left=0;
},_resizeBorder:function(H,I,J){var K=this.getInsets();
I-=K.left+K.right;
J-=K.top+K.bottom;
if(I<0){I=0;
}
if(J<0){J=0;
}return {left:K.left-this.getWidthLeft(),top:K.top-this.getWidthTop(),width:I,height:J};
},_getDefaultInsetsForBorder:function(){return {top:this.getWidthTop(),right:this.getWidthRight(),bottom:this.getWidthBottom(),left:this.getWidthLeft()};
},_applyWidth:function(){this._applyStyle();
this._resetInsets();
},_applyStyle:function(){}}});
})();
(function(){var b="px",a="qx.ui.decoration.Single";
qx.Class.define(a,{extend:qx.ui.decoration.Abstract,include:[qx.ui.decoration.MBackgroundImage,qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MSingleBorder],construct:function(c,d,e){qx.ui.decoration.Abstract.call(this);
if(c!=null){this.setWidth(c);
}
if(d!=null){this.setStyle(d);
}
if(e!=null){this.setColor(e);
}},members:{_markup:null,getMarkup:function(f){if(this._markup){return this._markup;
}var g={};
this._styleBorder(g,f);
var h=this._generateBackgroundMarkup(g);
return this._markup=h;
},resize:function(i,j,k){var l=this._resizeBorder(i,j,k);
i.style.width=l.width+b;
i.style.height=l.height+b;
i.style.left=parseInt(i.style.left)+l.left+b;
i.style.top=parseInt(i.style.top)+l.top+b;
},tint:function(m,n){this._tintBackgroundColor(m,n,m.style);
},_isInitialized:function(){return !!this._markup;
},_getDefaultInsets:function(){return this._getDefaultInsetsForBorder();
}},destruct:function(){this._markup=null;
}});
})();
(function(){var c="px",b="qx.ui.decoration.Background",a="absolute";
qx.Class.define(b,{extend:qx.ui.decoration.Abstract,include:[qx.ui.decoration.MBackgroundImage,qx.ui.decoration.MBackgroundColor],construct:function(d){qx.ui.decoration.Abstract.call(this);

if(d!=null){this.setBackgroundColor(d);
}},members:{__nG:null,_getDefaultInsets:function(){return {top:0,right:0,bottom:0,left:0};
},_isInitialized:function(){return !!this.__nG;
},getMarkup:function(e){if(this.__nG){return this.__nG;
}var f={position:a,top:0,left:0};
var g=this._generateBackgroundMarkup(f);
return this.__nG=g;
},resize:function(h,i,j){var k=this.getInsets();
h.style.width=(i-k.left-k.right)+c;
h.style.height=(j-k.top-k.bottom)+c;
h.style.left=-k.left+c;
h.style.top=-k.top+c;
},tint:function(l,m){this._tintBackgroundColor(l,m,l.style);
}},destruct:function(){this.__nG=null;
}});
})();
(function(){var a="qx.ui.decoration.Uniform";
qx.Class.define(a,{extend:qx.ui.decoration.Single,construct:function(b,c,d){qx.ui.decoration.Single.call(this);
if(b!=null){this.setWidth(b);
}
if(c!=null){this.setStyle(c);
}
if(d!=null){this.setColor(d);
}}});
})();
(function(){var j="px ",i=" ",h='',g="Color",f="Number",e="border-top",d="border-left",c="border-bottom",b="border-right",a="shorthand",C="line-height",B="engine.name",A="mshtml",z="innerWidthRight",y="top",x="innerColorBottom",w="innerWidthTop",v="innerColorRight",u="innerColorTop",t="relative",q="browser.documentmode",r="innerColorLeft",o="qx.ui.decoration.MDoubleBorder",p="left",m="engine.version",n="innerWidthBottom",k="innerWidthLeft",l="position",s="absolute";
qx.Mixin.define(o,{include:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBackgroundImage],construct:function(){this._getDefaultInsetsForBorder=this.__nL;
this._resizeBorder=this.__nK;
this._styleBorder=this.__nI;
this._generateMarkup=this.__nJ;
},properties:{innerWidthTop:{check:f,init:0},innerWidthRight:{check:f,init:0},innerWidthBottom:{check:f,init:0},innerWidthLeft:{check:f,init:0},innerWidth:{group:[w,z,n,k],mode:a},innerColorTop:{nullable:true,check:g},innerColorRight:{nullable:true,check:g},innerColorBottom:{nullable:true,check:g},innerColorLeft:{nullable:true,check:g},innerColor:{group:[u,v,x,r],mode:a}},members:{__nH:null,__nI:function(D){var E=qx.theme.manager.Color.getInstance();
D.position=t;
var F=this.getInnerWidthTop();

if(F>0){D[e]=F+j+this.getStyleTop()+i+E.resolve(this.getInnerColorTop());
}var F=this.getInnerWidthRight();

if(F>0){D[b]=F+j+this.getStyleRight()+i+E.resolve(this.getInnerColorRight());
}var F=this.getInnerWidthBottom();

if(F>0){D[c]=F+j+this.getStyleBottom()+i+E.resolve(this.getInnerColorBottom());
}var F=this.getInnerWidthLeft();

if(F>0){D[d]=F+j+this.getStyleLeft()+i+E.resolve(this.getInnerColorLeft());
}},__nJ:function(G){var J=this._generateBackgroundMarkup(G);
var H=qx.theme.manager.Color.getInstance();
G[e]=h;
G[b]=h;
G[c]=h;
G[d]=h;
G[C]=0;
if((qx.core.Environment.get(B)==A&&parseFloat(qx.core.Environment.get(m))<8)||(qx.core.Environment.get(B)==A&&qx.core.Environment.get(q)<8)){G[C]=h;
}var I=this.getWidthTop();

if(I>0){G[e]=I+j+this.getStyleTop()+i+H.resolve(this.getColorTop());
}var I=this.getWidthRight();

if(I>0){G[b]=I+j+this.getStyleRight()+i+H.resolve(this.getColorRight());
}var I=this.getWidthBottom();

if(I>0){G[c]=I+j+this.getStyleBottom()+i+H.resolve(this.getColorBottom());
}var I=this.getWidthLeft();

if(I>0){G[d]=I+j+this.getStyleLeft()+i+H.resolve(this.getColorLeft());
}G[l]=s;
G[y]=0;
G[p]=0;
return this.__nH=this._generateBackgroundMarkup(G,J);
},__nK:function(K,L,M){var N=this.getInsets();
L-=N.left+N.right;
M-=N.top+N.bottom;
var O=N.left-this.getWidthLeft()-this.getInnerWidthLeft();
var top=N.top-this.getWidthTop()-this.getInnerWidthTop();
return {left:O,top:top,width:L,height:M,elementToApplyDimensions:K.firstChild};
},__nL:function(){return {top:this.getWidthTop()+this.getInnerWidthTop(),right:this.getWidthRight()+this.getInnerWidthRight(),bottom:this.getWidthBottom()+this.getInnerWidthBottom(),left:this.getWidthLeft()+this.getInnerWidthLeft()};
}}});
})();
(function(){var j='"></div>',i="_applyStyle",h="1px",g='<div style="',f='border:',e="1px solid ",d="Color",c=";",b="px",a='</div>',x="qx.ui.decoration.Beveled",w="css.boxmodel",v='<div style="position:absolute;top:1px;left:1px;',u='border-bottom:',t='border-right:',s="",r="content",q='border-left:',p='border-top:',o="Number",m='<div style="position:absolute;top:1px;left:0px;',n='position:absolute;top:0px;left:1px;',k='<div style="overflow:hidden;font-size:0;line-height:0;">',l="absolute";
qx.Class.define(x,{extend:qx.ui.decoration.Abstract,include:[qx.ui.decoration.MBackgroundImage,qx.ui.decoration.MBackgroundColor],construct:function(y,z,A){qx.ui.decoration.Abstract.call(this);
if(y!=null){this.setOuterColor(y);
}
if(z!=null){this.setInnerColor(z);
}
if(A!=null){this.setInnerOpacity(A);
}},properties:{innerColor:{check:d,nullable:true,apply:i},innerOpacity:{check:o,init:1,apply:i},outerColor:{check:d,nullable:true,apply:i}},members:{__nG:null,_getDefaultInsets:function(){return {top:2,right:2,bottom:2,left:2};
},_isInitialized:function(){return !!this.__nG;
},_applyStyle:function(){},getMarkup:function(){if(this.__nG){return this.__nG;
}var B=qx.theme.manager.Color.getInstance();
var C=[];
var F=e+B.resolve(this.getOuterColor())+c;
var E=e+B.resolve(this.getInnerColor())+c;
C.push(k);
C.push(g);
C.push(f,F);
C.push(qx.bom.element.Opacity.compile(0.35));
C.push(j);
C.push(m);
C.push(q,F);
C.push(t,F);
C.push(qx.bom.element.Opacity.compile(1));
C.push(j);
C.push(g);
C.push(n);
C.push(p,F);
C.push(u,F);
C.push(qx.bom.element.Opacity.compile(1));
C.push(j);
var D={position:l,top:h,left:h,opacity:1};
C.push(this._generateBackgroundMarkup(D));
C.push(v);
C.push(f,E);
C.push(qx.bom.element.Opacity.compile(this.getInnerOpacity()));
C.push(j);
C.push(a);
return this.__nG=C.join(s);
},resize:function(G,H,I){if(H<4){H=4;
}
if(I<4){I=4;
}if(qx.core.Environment.get(w)==r){var outerWidth=H-2;
var outerHeight=I-2;
var O=outerWidth;
var N=outerHeight;
var innerWidth=H-4;
var innerHeight=I-4;
}else{var outerWidth=H;
var outerHeight=I;
var O=H-2;
var N=I-2;
var innerWidth=O;
var innerHeight=N;
}var Q=b;
var M=G.childNodes[0].style;
M.width=outerWidth+Q;
M.height=outerHeight+Q;
var L=G.childNodes[1].style;
L.width=outerWidth+Q;
L.height=N+Q;
var K=G.childNodes[2].style;
K.width=O+Q;
K.height=outerHeight+Q;
var J=G.childNodes[3].style;
J.width=O+Q;
J.height=N+Q;
var P=G.childNodes[4].style;
P.width=innerWidth+Q;
P.height=innerHeight+Q;
},tint:function(R,S){this._tintBackgroundColor(R,S,R.childNodes[3].style);
}},destruct:function(){this.__nG=null;
}});
})();
(function(){var j="_applyLinearBackgroundGradient",i=" ",h=")",g="engine.name",f="horizontal",e=",",d=" 0",c="px",b="browser.name",a="0",K="shorthand",J="Color",I="vertical",H="",G="Number",F="webkit",E="%",D="),to(",C="from(",B="background-image",q="engine.version",r="-moz-",o="-webkit-gradient(linear,",p="startColorPosition",m="-o-",n="deg, ",k="startColor",l="ie",s="qx.ui.decoration.MLinearBackgroundGradient",t="endColorPosition",w="opera",v="linear-gradient(",y="endColor",x="-ms-",A="gecko",z="background",u="-webkit-";
qx.Mixin.define(s,{properties:{startColor:{check:J,nullable:true,apply:j},endColor:{check:J,nullable:true,apply:j},orientation:{check:[f,I],init:I,apply:j},startColorPosition:{check:G,init:0,apply:j},endColorPosition:{check:G,init:100,apply:j},colorPositionUnit:{check:[c,E],init:E,apply:j},gradientStart:{group:[k,p],mode:K},gradientEnd:{group:[y,t],mode:K}},members:{_styleLinearBackgroundGradient:function(L){var O=qx.theme.manager.Color.getInstance();
var U=this.getColorPositionUnit();
if(qx.core.Environment.get(g)==F&&parseFloat(qx.core.Environment.get(q))<534.16){U=U===c?H:U;

if(this.getOrientation()==f){var T=this.getStartColorPosition()+U+d+U;
var S=this.getEndColorPosition()+U+d+U;
}else{var T=a+U+i+this.getStartColorPosition()+U;
var S=a+U+i+this.getEndColorPosition()+U;
}var Q=C+O.resolve(this.getStartColor())+D+O.resolve(this.getEndColor())+h;
var P=o+T+e+S+e+Q+h;
L[z]=P;
}else{var V=this.getOrientation()==f?0:270;
var N=O.resolve(this.getStartColor())+i+this.getStartColorPosition()+U;
var M=O.resolve(this.getEndColor())+i+this.getEndColorPosition()+U;
var R=H;

if(qx.core.Environment.get(g)==A){R=r;
}else if(qx.core.Environment.get(b)==w){R=m;
}else if(qx.core.Environment.get(b)==l){R=x;
}else if(qx.core.Environment.get(g)==F){R=u;
}L[B]=R+v+V+n+N+e+M+h;
}},_resizeLinearBackgroundGradient:function(W,X,Y){var ba=this.getInsets();
X-=ba.left+ba.right;
Y-=ba.top+ba.bottom;
return {left:ba.left,top:ba.top,width:X,height:Y};
},_applyLinearBackgroundGradient:function(){}}});
})();
(function(){var o="Number",n="_applyInsets",m="-l",l="insetRight",k="insetTop",j="_applyBaseImage",i="insetBottom",h="-b",g="set",f="shorthand",c="-t",e="insetLeft",d="String",b="qx.ui.decoration.Grid",a="-r";
qx.Class.define(b,{extend:qx.core.Object,implement:[qx.ui.decoration.IDecorator],construct:function(p,q){qx.core.Object.call(this);

if(qx.ui.decoration.css3.BorderImage.IS_SUPPORTED){this.__nM=new qx.ui.decoration.css3.BorderImage();

if(p){this.__nN(p);
}}else{this.__nM=new qx.ui.decoration.GridDiv(p);
}
if(q!=null){this.__nM.setInsets(q);
}},properties:{baseImage:{check:d,nullable:true,apply:j},insetLeft:{check:o,nullable:true,apply:n},insetRight:{check:o,nullable:true,apply:n},insetBottom:{check:o,nullable:true,apply:n},insetTop:{check:o,nullable:true,apply:n},insets:{group:[k,l,i,e],mode:f}},members:{__nM:null,getMarkup:function(){return this.__nM.getMarkup();
},resize:function(r,s,t){this.__nM.resize(r,s,t);
},tint:function(u,v){},getInsets:function(){return this.__nM.getInsets();
},_applyInsets:function(w,x,name){var y=g+qx.lang.String.firstUp(name);
this.__nM[y](w);
},_applyBaseImage:function(z,A){if(this.__nM instanceof qx.ui.decoration.GridDiv){this.__nM.setBaseImage(z);
}else{this.__nN(z);
}},__nN:function(B){var G,H,J,I;
this.__nM.setBorderImage(B);
var L=qx.util.AliasManager.getInstance().resolve(B);
var M=/(.*)(\.[a-z]+)$/.exec(L);
var K=M[1];
var C=M[2];
var F=qx.util.ResourceManager.getInstance();
var N=F.getImageHeight(K+c+C);
var D=F.getImageWidth(K+a+C);
var E=F.getImageHeight(K+h+C);
var O=F.getImageWidth(K+m+C);
this.__nM.setSlice([N,D,E,O]);
}},destruct:function(){this.__nM=null;
}});
})();
(function(){var j="_applyStyle",i="stretch",h="Integer",g="px",f=" ",e="repeat",d="round",c="shorthand",b="px ",a="sliceBottom",y=";'></div>",x="<div style='",w="sliceLeft",v="sliceRight",u="repeatX",t="String",s="qx.ui.decoration.css3.BorderImage",r="border-box",q="",p='") ',n="sliceTop",o='url("',l="hidden",m="repeatY",k="absolute";
qx.Class.define(s,{extend:qx.ui.decoration.Abstract,construct:function(z,A){qx.ui.decoration.Abstract.call(this);
if(z!=null){this.setBorderImage(z);
}
if(A!=null){this.setSlice(A);
}},statics:{IS_SUPPORTED:qx.bom.element.Style.isPropertySupported("borderImage")},properties:{borderImage:{check:t,nullable:true,apply:j},sliceTop:{check:h,init:0,apply:j},sliceRight:{check:h,init:0,apply:j},sliceBottom:{check:h,init:0,apply:j},sliceLeft:{check:h,init:0,apply:j},slice:{group:[n,v,a,w],mode:c},repeatX:{check:[i,e,d],init:i,apply:j},repeatY:{check:[i,e,d],init:i,apply:j},repeat:{group:[u,m],mode:c}},members:{__nG:null,_getDefaultInsets:function(){return {top:0,right:0,bottom:0,left:0};
},_isInitialized:function(){return !!this.__nG;
},getMarkup:function(){if(this.__nG){return this.__nG;
}var B=this._resolveImageUrl(this.getBorderImage());
var C=[this.getSliceTop(),this.getSliceRight(),this.getSliceBottom(),this.getSliceLeft()];
var D=[this.getRepeatX(),this.getRepeatY()].join(f);
this.__nG=[x,qx.bom.element.Style.compile({"borderImage":o+B+p+C.join(f)+f+D,position:k,lineHeight:0,fontSize:0,overflow:l,boxSizing:r,borderWidth:C.join(b)+g}),y].join(q);
return this.__nG;
},resize:function(E,F,G){E.style.width=F+g;
E.style.height=G+g;
},tint:function(H,I){},_applyStyle:function(){},_resolveImageUrl:function(J){return qx.util.ResourceManager.getInstance().toUri(qx.util.AliasManager.getInstance().resolve(J));
}},destruct:function(){this.__nG=null;
}});
})();
(function(){var j="px",i="0px",h="-1px",g="no-repeat",f="engine.version",e="scale-x",d="scale-y",c="-tr",b="-l",a='</div>',z="scale",y="-br",x="-t",w="browser.quirksmode",v="-tl",u="-r",t='<div style="position:absolute;top:0;left:0;overflow:hidden;font-size:0;line-height:0;">',s="_applyBaseImage",r="-b",q="String",o="",p="-bl",m="qx.ui.decoration.GridDiv",n="-c",k="mshtml",l="engine.name";
qx.Class.define(m,{extend:qx.ui.decoration.Abstract,construct:function(A,B){qx.ui.decoration.Abstract.call(this);
if(A!=null){this.setBaseImage(A);
}
if(B!=null){this.setInsets(B);
}},properties:{baseImage:{check:q,nullable:true,apply:s}},members:{_markup:null,_images:null,_edges:null,_getDefaultInsets:function(){return {top:0,right:0,bottom:0,left:0};
},_isInitialized:function(){return !!this._markup;
},getMarkup:function(){if(this._markup){return this._markup;
}var C=qx.bom.element.Decoration;
var D=this._images;
var E=this._edges;
var F=[];
F.push(t);
F.push(C.create(D.tl,g,{top:0,left:0}));
F.push(C.create(D.t,e,{top:0,left:E.left+j}));
F.push(C.create(D.tr,g,{top:0,right:0}));
F.push(C.create(D.bl,g,{bottom:0,left:0}));
F.push(C.create(D.b,e,{bottom:0,left:E.left+j}));
F.push(C.create(D.br,g,{bottom:0,right:0}));
F.push(C.create(D.l,d,{top:E.top+j,left:0}));
F.push(C.create(D.c,z,{top:E.top+j,left:E.left+j}));
F.push(C.create(D.r,d,{top:E.top+j,right:0}));
F.push(a);
return this._markup=F.join(o);
},resize:function(G,H,I){var J=this._edges;
var innerWidth=H-J.left-J.right;
var innerHeight=I-J.top-J.bottom;
if(innerWidth<0){innerWidth=0;
}
if(innerHeight<0){innerHeight=0;
}G.style.width=H+j;
G.style.height=I+j;
G.childNodes[1].style.width=innerWidth+j;
G.childNodes[4].style.width=innerWidth+j;
G.childNodes[7].style.width=innerWidth+j;
G.childNodes[6].style.height=innerHeight+j;
G.childNodes[7].style.height=innerHeight+j;
G.childNodes[8].style.height=innerHeight+j;

if((qx.core.Environment.get(l)==k)){if(parseFloat(qx.core.Environment.get(f))<7||(qx.core.Environment.get(w)&&parseFloat(qx.core.Environment.get(f))<8)){if(H%2==1){G.childNodes[2].style.marginRight=h;
G.childNodes[5].style.marginRight=h;
G.childNodes[8].style.marginRight=h;
}else{G.childNodes[2].style.marginRight=i;
G.childNodes[5].style.marginRight=i;
G.childNodes[8].style.marginRight=i;
}
if(I%2==1){G.childNodes[3].style.marginBottom=h;
G.childNodes[4].style.marginBottom=h;
G.childNodes[5].style.marginBottom=h;
}else{G.childNodes[3].style.marginBottom=i;
G.childNodes[4].style.marginBottom=i;
G.childNodes[5].style.marginBottom=i;
}}}},tint:function(K,L){},_applyBaseImage:function(M,N){if(M){var R=this._resolveImageUrl(M);
var S=/(.*)(\.[a-z]+)$/.exec(R);
var Q=S[1];
var P=S[2];
var O=this._images={tl:Q+v+P,t:Q+x+P,tr:Q+c+P,bl:Q+p+P,b:Q+r+P,br:Q+y+P,l:Q+b+P,c:Q+n+P,r:Q+u+P};
this._edges=this._computeEdgeSizes(O);
}},_resolveImageUrl:function(T){return qx.util.AliasManager.getInstance().resolve(T);
},_computeEdgeSizes:function(U){var V=qx.util.ResourceManager.getInstance();
return {top:V.getImageHeight(U.t),bottom:V.getImageHeight(U.b),left:V.getImageWidth(U.l),right:V.getImageWidth(U.r)};
}},destruct:function(){this._markup=this._images=this._edges=null;
}});
})();
(function(){var j="px",i="Integer",h="_applyBorderRadius",g="radiusTopRight",f="radiusTopLeft",e="-webkit-border-bottom-left-radius",d="-webkit-background-clip",c="radiusBottomRight",b="-webkit-border-bottom-right-radius",a="border-top-left-radius",w="border-top-right-radius",v="border-bottom-left-radius",u="radiusBottomLeft",t="-webkit-border-top-left-radius",s="shorthand",r="-moz-border-radius-bottomright",q="padding-box",p="border-bottom-right-radius",o="qx.ui.decoration.MBorderRadius",n="-moz-border-radius-topright",l="-webkit-border-top-right-radius",m="-moz-border-radius-topleft",k="-moz-border-radius-bottomleft";
qx.Mixin.define(o,{properties:{radiusTopLeft:{nullable:true,check:i,apply:h},radiusTopRight:{nullable:true,check:i,apply:h},radiusBottomLeft:{nullable:true,check:i,apply:h},radiusBottomRight:{nullable:true,check:i,apply:h},radius:{group:[f,g,c,u],mode:s}},members:{_styleBorderRadius:function(x){x[d]=q;
var y=this.getRadiusTopLeft();

if(y>0){x[m]=y+j;
x[t]=y+j;
x[a]=y+j;
}y=this.getRadiusTopRight();

if(y>0){x[n]=y+j;
x[l]=y+j;
x[w]=y+j;
}y=this.getRadiusBottomLeft();

if(y>0){x[k]=y+j;
x[e]=y+j;
x[v]=y+j;
}y=this.getRadiusBottomRight();

if(y>0){x[r]=y+j;
x[b]=y+j;
x[p]=y+j;
}},_applyBorderRadius:function(){}}});
})();
(function(){var cJ="solid",cI="invalid",cH="scale",cG="border-main",cF="border-invalid",cE="shadow",cD="border-separator",cC="checkbox-hovered",cB="button-start",cA="button-end",bK="background-light",bJ="tabview-background",bI="repeat-x",bH="radiobutton",bG="button-css",bF="border-input",bE="border-inner-input",bD="border-inner-scrollbar",bC="radiobutton-checked",bB="tabview-inactive",cQ="checkbox",cR="window-border",cO="radiobutton-disabled",cP="radiobutton-hovered-invalid",cM="tabview-page-button-top-active-css",cN="button-border-disabeld",cK="tabview-page-button-top-inactive-css",cL="decoration/form/input.png",cS="border-toolbar-border-inner",cT="input-css",cj="border-toolbar-button-outer",ci="border-disabled",cl="background-pane",ck="checkbox-disabled-border",cn="button-hovered-end",cm="repeat-y",cp="border-dragover",co="button-hovered-start",ch="progressive-table-header-border-right",cg="decoration/scrollbar/scrollbar-button-bg-vertical.png",k="radiobutton-background",l="checkbox-focus",m="scrollbar-slider-horizontal-css",n="menu-end",o="decoration/selection.png",p="horizontal",q="table-header-start",r="decoration/scrollbar/scrollbar-button-bg-horizontal.png",s="decoration/form/input-focused.png",t="checkbox-hovered-invalid",di="decoration/table/header-cell.png",dh="tabview-inactive-start",dg="table-header-end",df="border-button",dm="border-focused-invalid",dl="button-focused-css",dk="checkbox-border",dj="tabview-start",dp="checkbox-start",dn="decoration/tabview/tab-button-top-active.png",bb="group-background",bc="decoration/form/button-c.png",Y="keyboard-focus",ba="button-disabled-start",bf="selected-end",bg="table-header-hovered",bd="decoration/groupbox/groupbox.png",be="decoration/pane/pane.png",W="decoration/menu/background.png",X="tooltip-error",J="decoration/toolbar/toolbar-part.gif",I="input-focused-css",L="decoration/menu/bar-background.png",K="window-border-caption",F="radiobutton-hovered",E="decoration/tabview/tab-button-bottom-active.png",H="radiobutton-checked-focused",G="groupitem-end",D="button-disabled-css",C="group-border",bl="scrollbar-slider-vertical-css",bm="decoration/form/button-checked.png",bn="window-css",bo="selected-start",bh="window-resize-frame-css",bi="tabview-end",bj="window-statusbar-background",bk="decoration/scrollbar/scrollbar-bg-vertical.png",bp="button-pressed-css",bq="toolbar-button-hovered-css",T="window-caption-active-end",S="dotted",R="checkbox-disabled-end",Q="window-caption-active-start",P="button-focused",O="menu-start",N="decoration/form/tooltip-error.png",M="window-captionbar-active-css",V="qx/decoration/Modern",U="border-toolbar-separator-left",br="decoration/scrollbar/scrollbar-bg-horizontal.png",bs="decoration/tabview/tab-button-left-active.png",bt="decoration/tabview/tab-button-right-inactive.png",bu="decoration/tabview/tab-button-bottom-inactive.png",bv="decoration/form/button-disabled.png",bw="decoration/form/button-pressed.png",bx="background-splitpane",by="decoration/form/button-checked-focused.png",bz="px",bA="decoration/window/statusbar.png",bO="input-border-disabled",bN="checkbox-inner",bM="scrollbar-horizontal-css",bL="button-disabled-end",bS="center",bR="toolbar-end",bQ="groupitem-start",bP="decoration/form/button-hovered.png",bU="checkbox-hovered-inner",bT="input-focused-start",cc="scrollbar-start",cd="scrollbar-slider-start",ca="radiobutton-checked-disabled",cb="checkbox-focused",bX="qx.theme.modern.Decoration",bY="decoration/form/button.png",bV="decoration/app-header.png",bW="decoration/form/button-focused.png",ce="radiobutton-checked-hovered",cf="button-hovered-css",ct="checkbox-disabled-inner",cs="border-toolbar-separator-right",cv="border-focused",cu="decoration/shadow/shadow.png",cx="scrollbar-end",cw="decoration/group-item.png",cz="window-caption-inactive-end",cy="checkbox-end",cr="tabview-inactive-end",cq="input-end",db="no-repeat",dc="decoration/tabview/tab-button-left-inactive.png",dd="input-focused-inner-invalid",de="menu-separator-top",cW="window-caption-inactive-start",cX="scrollbar-slider-end",cY="decoration/window/captionbar-inactive.png",da="decoration/tabview/tab-button-top-inactive.png",cU="pane-end",cV="input-focused-end",j="decoration/form/tooltip-error-arrow.png",i="menubar-start",h="toolbar-start",g="checkbox-disabled-start",f="radiobutton-focused",e="pane-start",d="table-focus-indicator",c="button-checked-css",b="decoration/form/button-checked-c.png",a="menu-separator-bottom",w="decoration/shadow/shadow-small.png",x="input-start",u="decoration/tabview/tabview-pane.png",v="decoration/window/captionbar-active.png",A="decoration/tabview/tab-button-right-active.png",B="button-checked-focused-css",y="decoration/toolbar/toolbar-gradient.png",z="checkbox-hovered-inner-invalid";
qx.Theme.define(bX,{aliases:{decoration:V},decorations:{"main":{decorator:qx.ui.decoration.Uniform,style:{width:1,color:cG}},"selected":{decorator:qx.ui.decoration.Background,style:{backgroundImage:o,backgroundRepeat:cH}},"selected-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{startColorPosition:0,endColorPosition:100,startColor:bo,endColor:bf}},"selected-dragover":{decorator:qx.ui.decoration.Single,style:{backgroundImage:o,backgroundRepeat:cH,bottom:[2,cJ,cp]}},"dragover":{decorator:qx.ui.decoration.Single,style:{bottom:[2,cJ,cp]}},"pane":{decorator:qx.ui.decoration.Grid,style:{baseImage:be,insets:[0,2,3,0]}},"pane-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MLinearBackgroundGradient],style:{width:1,color:bJ,radius:3,shadowColor:cE,shadowBlurRadius:2,shadowLength:0,gradientStart:[e,0],gradientEnd:[cU,100]}},"group":{decorator:qx.ui.decoration.Grid,style:{baseImage:bd}},"group-css":{decorator:[qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MSingleBorder],style:{backgroundColor:bb,radius:4,color:C,width:1}},"border-invalid":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cI,innerColor:bE,innerOpacity:0.5,backgroundImage:cL,backgroundRepeat:bI,backgroundColor:bK}},"keyboard-focus":{decorator:qx.ui.decoration.Single,style:{width:1,color:Y,style:S}},"radiobutton":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow],style:{backgroundColor:k,radius:5,width:1,innerWidth:2,color:dk,innerColor:k,shadowLength:0,shadowBlurRadius:0,shadowColor:l,insetLeft:5}},"radiobutton-checked":{include:bH,style:{backgroundColor:bC}},"radiobutton-checked-focused":{include:bC,style:{shadowBlurRadius:4}},"radiobutton-checked-hovered":{include:bC,style:{innerColor:cC}},"radiobutton-focused":{include:bH,style:{shadowBlurRadius:4}},"radiobutton-hovered":{include:bH,style:{backgroundColor:cC,innerColor:cC}},"radiobutton-disabled":{include:bH,style:{innerColor:cO,backgroundColor:cO,color:ck}},"radiobutton-checked-disabled":{include:cO,style:{backgroundColor:ca}},"radiobutton-invalid":{include:bH,style:{color:cI}},"radiobutton-checked-invalid":{include:bC,style:{color:cI}},"radiobutton-checked-focused-invalid":{include:H,style:{color:cI,shadowColor:cI}},"radiobutton-checked-hovered-invalid":{include:ce,style:{color:cI,innerColor:cP}},"radiobutton-focused-invalid":{include:f,style:{color:cI,shadowColor:cI}},"radiobutton-hovered-invalid":{include:F,style:{color:cI,innerColor:cP,backgroundColor:cP}},"separator-horizontal":{decorator:qx.ui.decoration.Single,style:{widthLeft:1,colorLeft:cD}},"separator-vertical":{decorator:qx.ui.decoration.Single,style:{widthTop:1,colorTop:cD}},"tooltip-error":{decorator:qx.ui.decoration.Grid,style:{baseImage:N,insets:[2,5,5,2]}},"tooltip-error-css":{decorator:[qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow],style:{backgroundColor:X,radius:4,shadowColor:cE,shadowBlurRadius:2,shadowLength:1}},"tooltip-error-arrow":{decorator:qx.ui.decoration.Background,style:{backgroundImage:j,backgroundPositionY:bS,backgroundRepeat:db,insets:[0,0,0,10]}},"shadow-window":{decorator:qx.ui.decoration.Grid,style:{baseImage:cu,insets:[4,8,8,4]}},"shadow-window-css":{decorator:[qx.ui.decoration.MBoxShadow,qx.ui.decoration.MBackgroundColor],style:{shadowColor:cE,shadowBlurRadius:2,shadowLength:1}},"shadow-popup":{decorator:qx.ui.decoration.Grid,style:{baseImage:w,insets:[0,3,3,0]}},"popup-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MBackgroundColor],style:{width:1,color:cG,shadowColor:cE,shadowBlurRadius:3,shadowLength:1}},"scrollbar-horizontal":{decorator:qx.ui.decoration.Background,style:{backgroundImage:br,backgroundRepeat:bI}},"scrollbar-vertical":{decorator:qx.ui.decoration.Background,style:{backgroundImage:bk,backgroundRepeat:cm}},"scrollbar-slider-horizontal":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:r,backgroundRepeat:cH,outerColor:cG,innerColor:bD,innerOpacity:0.5}},"scrollbar-slider-horizontal-disabled":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:r,backgroundRepeat:cH,outerColor:ci,innerColor:bD,innerOpacity:0.3}},"scrollbar-slider-vertical":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:cg,backgroundRepeat:cH,outerColor:cG,innerColor:bD,innerOpacity:0.5}},"scrollbar-slider-vertical-disabled":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:cg,backgroundRepeat:cH,outerColor:ci,innerColor:bD,innerOpacity:0.3}},"scrollbar-horizontal-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[cc,0],gradientEnd:[cx,100]}},"scrollbar-vertical-css":{include:bM,style:{orientation:p}},"scrollbar-slider-horizontal-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[cd,0],gradientEnd:[cX,100],color:cG,width:1}},"scrollbar-slider-vertical-css":{include:m,style:{orientation:p}},"scrollbar-slider-horizontal-disabled-css":{include:m,style:{color:cN}},"scrollbar-slider-vertical-disabled-css":{include:bl,style:{color:cN}},"button-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBorderRadius],style:{radius:3,color:df,width:1,startColor:cB,endColor:cA,startColorPosition:35,endColorPosition:100}},"button-disabled-css":{include:bG,style:{color:cN,startColor:ba,endColor:bL}},"button-hovered-css":{include:bG,style:{startColor:co,endColor:cn}},"button-checked-css":{include:bG,style:{endColor:cB,startColor:cA}},"button-pressed-css":{include:bG,style:{endColor:co,startColor:cn}},"button-focused-css":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBorderRadius],style:{radius:3,color:df,width:1,innerColor:P,innerWidth:2,startColor:cB,endColor:cA,startColorPosition:30,endColorPosition:100}},"button-checked-focused-css":{include:dl,style:{endColor:cB,startColor:cA}},"button-invalid-css":{include:bG,style:{color:cF}},"button-disabled-invalid-css":{include:D,style:{color:cF}},"button-hovered-invalid-css":{include:cf,style:{color:cF}},"button-checked-invalid-css":{include:c,style:{color:cF}},"button-pressed-invalid-css":{include:bp,style:{color:cF}},"button-focused-invalid-css":{include:dl,style:{color:cF}},"button-checked-focused-invalid-css":{include:B,style:{color:cF}},"button":{decorator:qx.ui.decoration.Grid,style:{baseImage:bY,insets:2}},"button-disabled":{decorator:qx.ui.decoration.Grid,style:{baseImage:bv,insets:2}},"button-focused":{decorator:qx.ui.decoration.Grid,style:{baseImage:bW,insets:2}},"button-hovered":{decorator:qx.ui.decoration.Grid,style:{baseImage:bP,insets:2}},"button-pressed":{decorator:qx.ui.decoration.Grid,style:{baseImage:bw,insets:2}},"button-checked":{decorator:qx.ui.decoration.Grid,style:{baseImage:bm,insets:2}},"button-checked-focused":{decorator:qx.ui.decoration.Grid,style:{baseImage:by,insets:2}},"button-invalid-shadow":{decorator:qx.ui.decoration.Single,style:{color:cI,width:1}},"checkbox-invalid-shadow":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cI,innerColor:dm,insets:[0]}},"checkbox":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBoxShadow],style:{width:1,color:dk,innerWidth:1,innerColor:bN,gradientStart:[dp,0],gradientEnd:[cy,100],shadowLength:0,shadowBlurRadius:0,shadowColor:l,insetLeft:4}},"checkbox-hovered":{include:cQ,style:{innerColor:bU,gradientStart:[cC,0],gradientEnd:[cC,100]}},"checkbox-focused":{include:cQ,style:{shadowBlurRadius:4}},"checkbox-disabled":{include:cQ,style:{color:ck,innerColor:ct,gradientStart:[g,0],gradientEnd:[R,100]}},"checkbox-invalid":{include:cQ,style:{color:cI}},"checkbox-hovered-invalid":{include:cC,style:{color:cI,innerColor:z,gradientStart:[t,0],gradientEnd:[t,100]}},"checkbox-focused-invalid":{include:cb,style:{color:cI,shadowColor:cI}},"input-css":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBackgroundColor],style:{color:bF,innerColor:bE,innerWidth:1,width:1,backgroundColor:bK,startColor:x,endColor:cq,startColorPosition:0,endColorPosition:12,colorPositionUnit:bz}},"border-invalid-css":{include:cT,style:{color:cF}},"input-focused-css":{include:cT,style:{startColor:bT,innerColor:cV,endColorPosition:4}},"input-focused-invalid-css":{include:I,style:{innerColor:dd,color:cF}},"input-disabled-css":{include:cT,style:{color:bO}},"input":{decorator:qx.ui.decoration.Beveled,style:{outerColor:bF,innerColor:bE,innerOpacity:0.5,backgroundImage:cL,backgroundRepeat:bI,backgroundColor:bK}},"input-focused":{decorator:qx.ui.decoration.Beveled,style:{outerColor:bF,innerColor:cv,backgroundImage:s,backgroundRepeat:bI,backgroundColor:bK}},"input-focused-invalid":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cI,innerColor:dm,backgroundImage:s,backgroundRepeat:bI,backgroundColor:bK,insets:[2]}},"input-disabled":{decorator:qx.ui.decoration.Beveled,style:{outerColor:ci,innerColor:bE,innerOpacity:0.5,backgroundImage:cL,backgroundRepeat:bI,backgroundColor:bK}},"toolbar":{decorator:qx.ui.decoration.Background,style:{backgroundImage:y,backgroundRepeat:cH}},"toolbar-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{startColorPosition:40,endColorPosition:60,startColor:h,endColor:bR}},"toolbar-button-hovered":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cj,innerColor:cS,backgroundImage:bc,backgroundRepeat:cH}},"toolbar-button-checked":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cj,innerColor:cS,backgroundImage:b,backgroundRepeat:cH}},"toolbar-button-hovered-css":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBorderRadius],style:{color:cj,width:1,innerWidth:1,innerColor:cS,radius:2,gradientStart:[cB,30],gradientEnd:[cA,100]}},"toolbar-button-checked-css":{include:bq,style:{gradientStart:[cA,30],gradientEnd:[cB,100]}},"toolbar-separator":{decorator:qx.ui.decoration.Single,style:{widthLeft:1,widthRight:1,colorLeft:U,colorRight:cs,styleLeft:cJ,styleRight:cJ}},"toolbar-part":{decorator:qx.ui.decoration.Background,style:{backgroundImage:J,backgroundRepeat:cm}},"tabview-pane":{decorator:qx.ui.decoration.Grid,style:{baseImage:u,insets:[4,6,7,4]}},"tabview-pane-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MSingleBorder],style:{width:1,color:cR,radius:3,gradientStart:[dj,90],gradientEnd:[bi,100]}},"tabview-page-button-top-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:dn}},"tabview-page-button-top-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:da}},"tabview-page-button-bottom-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:E}},"tabview-page-button-bottom-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:bu}},"tabview-page-button-left-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:bs}},"tabview-page-button-left-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:dc}},"tabview-page-button-right-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:A}},"tabview-page-button-right-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:bt}},"tabview-page-button-top-active-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBoxShadow],style:{radius:[3,3,0,0],width:[1,1,0,1],color:bJ,backgroundColor:dj,shadowLength:1,shadowColor:cE,shadowBlurRadius:2}},"tabview-page-button-top-inactive-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{radius:[3,3,0,0],color:bB,colorBottom:bJ,width:1,gradientStart:[dh,0],gradientEnd:[cr,100]}},"tabview-page-button-bottom-active-css":{include:cM,style:{radius:[0,0,3,3],width:[0,1,1,1],backgroundColor:dh}},"tabview-page-button-bottom-inactive-css":{include:cK,style:{radius:[0,0,3,3],width:[0,1,1,1],colorBottom:bB,colorTop:bJ}},"tabview-page-button-left-active-css":{include:cM,style:{radius:[3,0,0,3],width:[1,0,1,1],shadowLength:0,shadowBlurRadius:0}},"tabview-page-button-left-inactive-css":{include:cK,style:{radius:[3,0,0,3],width:[1,0,1,1],colorBottom:bB,colorRight:bJ}},"tabview-page-button-right-active-css":{include:cM,style:{radius:[0,3,3,0],width:[1,1,1,0],shadowLength:0,shadowBlurRadius:0}},"tabview-page-button-right-inactive-css":{include:cK,style:{radius:[0,3,3,0],width:[1,1,1,0],colorBottom:bB,colorLeft:bJ}},"splitpane":{decorator:qx.ui.decoration.Uniform,style:{backgroundColor:cl,width:3,color:bx,style:cJ}},"window":{decorator:qx.ui.decoration.Single,style:{backgroundColor:cl,width:1,color:cG,widthTop:0}},"window-captionbar-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:v}},"window-captionbar-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:cY}},"window-statusbar":{decorator:qx.ui.decoration.Grid,style:{baseImage:bA}},"window-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MSingleBorder],style:{radius:[5,5,0,0],shadowBlurRadius:4,shadowLength:2,shadowColor:cE}},"window-incl-statusbar-css":{include:bn,style:{radius:[5,5,5,5]}},"window-resize-frame-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MSingleBorder],style:{radius:[5,5,0,0],width:1,color:cG}},"window-resize-frame-incl-statusbar-css":{include:bh,style:{radius:[5,5,5,5]}},"window-captionbar-active-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MLinearBackgroundGradient],style:{width:1,color:cR,colorBottom:K,radius:[5,5,0,0],gradientStart:[Q,30],gradientEnd:[T,70]}},"window-captionbar-inactive-css":{include:M,style:{gradientStart:[cW,30],gradientEnd:[cz,70]}},"window-statusbar-css":{decorator:[qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBorderRadius],style:{backgroundColor:bj,width:[0,1,1,1],color:cR,radius:[0,0,5,5]}},"window-pane-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBackgroundColor],style:{backgroundColor:cl,width:1,color:cR,widthTop:0}},"table":{decorator:qx.ui.decoration.Single,style:{width:1,color:cG,style:cJ}},"table-statusbar":{decorator:qx.ui.decoration.Single,style:{widthTop:1,colorTop:cG,style:cJ}},"table-scroller-header":{decorator:qx.ui.decoration.Single,style:{backgroundImage:di,backgroundRepeat:cH,widthBottom:1,colorBottom:cG,style:cJ}},"table-scroller-header-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[q,10],gradientEnd:[dg,90],widthBottom:1,colorBottom:cG}},"table-header-cell":{decorator:qx.ui.decoration.Single,style:{widthRight:1,colorRight:cD,styleRight:cJ}},"table-header-cell-hovered":{decorator:qx.ui.decoration.Single,style:{widthRight:1,colorRight:cD,styleRight:cJ,widthBottom:1,colorBottom:bg,styleBottom:cJ}},"table-scroller-focus-indicator":{decorator:qx.ui.decoration.Single,style:{width:2,color:d,style:cJ}},"progressive-table-header":{decorator:qx.ui.decoration.Single,style:{width:1,color:cG,style:cJ}},"progressive-table-header-cell":{decorator:qx.ui.decoration.Single,style:{backgroundImage:di,backgroundRepeat:cH,widthRight:1,colorRight:ch,style:cJ}},"progressive-table-header-cell-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[q,10],gradientEnd:[dg,90],widthRight:1,colorRight:ch}},"menu":{decorator:qx.ui.decoration.Single,style:{backgroundImage:W,backgroundRepeat:cH,width:1,color:cG,style:cJ}},"menu-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MSingleBorder],style:{gradientStart:[O,0],gradientEnd:[n,100],shadowColor:cE,shadowBlurRadius:2,shadowLength:1,width:1,color:cG}},"menu-separator":{decorator:qx.ui.decoration.Single,style:{widthTop:1,colorTop:de,widthBottom:1,colorBottom:a}},"menubar":{decorator:qx.ui.decoration.Single,style:{backgroundImage:L,backgroundRepeat:cH,width:1,color:cD,style:cJ}},"menubar-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[i,0],gradientEnd:[n,100],width:1,color:cD}},"app-header":{decorator:qx.ui.decoration.Background,style:{backgroundImage:bV,backgroundRepeat:cH}},"progressbar":{decorator:qx.ui.decoration.Single,style:{width:1,color:bF}},"group-item":{decorator:qx.ui.decoration.Background,style:{backgroundImage:cw,backgroundRepeat:cH}},"group-item-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{startColorPosition:0,endColorPosition:100,startColor:bQ,endColor:G}}}});
})();
(function(){var a="scoville_admin.theme.Decoration";
qx.Theme.define(a,{extend:qx.theme.modern.Decoration,decorations:{}});
})();
(function(){var c="Tango",b="qx/icon/Tango",a="qx.theme.icon.Tango";
qx.Theme.define(a,{title:c,aliases:{"icon":b}});
})();
(function(){var eq="css.gradients",ep="widget",eo="atom",en="-css",em="button-frame",el="css.borderradius",ek="css.boxshadow",ej="main",ei="button",eh="bold",cC="text-selected",cB="image",cA="text-disabled",cz="middle",cy="selected",cx="background-light",cw="label",cv="groupbox",cu="decoration/arrows/down.png",ct="popup",ex="cell",ey="border-invalid",ev="input",ew="input-disabled",et="menu-button",eu="input-focused-invalid",er="toolbar-button",es="spinner",ez="input-focused",eA="tooltip",dI="qx/static/blank.gif",dH="radiobutton",dK="list",dJ="tree-item",dM="combobox",dL="treevirtual-contract",dO="scrollbar",dN="datechooser/nav-button",dF="center",dE="checkbox",v="treevirtual-expand",w="",x="textfield",y="-invalid",z="decoration/arrows/right.png",A="background-application",B="invalid",C="right-top",D="selectbox",E="text-title",eQ="icon/16/places/folder-open.png",eP="radiobutton-hovered",eO="group-item",eN="scrollbar/button",eU="right",eT="combobox/button",eS="virtual-list",eR="icon/16/places/folder.png",eW="radiobutton-checked-focused",eV="text-label",bz="decoration/tree/closed.png",bA="table-scroller-header",bx="scrollbar-slider-horizontal",by="checkbox-hovered",bD="checkbox-checked",bE="decoration/arrows/left.png",bB="radiobutton-checked",bC="button-focused",bv="text-light",bw="menu-slidebar-button",bb="tree",ba="checkbox-undetermined",bd="table-scroller-header-css",bc="text-input",W="slidebar/button-forward",V="background-splitpane",Y="text-hovered",X=".png",U="decoration/tree/open.png",T="default",bK="decoration/arrows/down-small.png",bL="datechooser",bM="slidebar/button-backward",bN="radiobutton-checked-disabled",bG="checkbox-focused",bH="radiobutton-checked-hovered",bI="treevirtual-folder",bJ="shadow-popup",bO="icon/16/mimetypes/office-document.png",bP="background-medium",bo="icon/32/places/folder-open.png",bn="icon/22/places/folder-open.png",bm="table",bl="decoration/arrows/up.png",bk="decoration/form/",bj="radiobutton-focused",bi="button-checked",bh="decoration/window/maximize-active-hovered.png",bs="keyboard-focus",br="menu-css",bQ="decoration/cursors/",bR="slidebar",bS="tooltip-error-arrow",bT="table-scroller-focus-indicator",bU="popup-css",bV="move-frame",bW="nodrop",bX="decoration/table/boolean-true.png",bY="-invalid-css",ca="menu",cK="app-header",cJ="row-layer",cI="text-inactive",cH="move",cO="decoration/window/restore-active-hovered.png",cN="border-separator",cM="shadow-window",cL="tree-folder",cS="window-pane-css",cR="right.png",ds="checkbox-undetermined-hovered",dt="window-incl-statusbar-css",dq="tabview-page-button-bottom-inactive",dr="tooltip-error",dn="window-css",dp="window-statusbar",dl="button-hovered",dm="decoration/scrollbar/scrollbar-",dA="background-tip",dB="menubar-css",dT="scrollbar-slider-horizontal-disabled",dS="radiobutton-disabled",dV="window-resize-frame-css",dU="button-pressed",dX="table-pane",dW="decoration/window/close-active.png",ea="native",dY="button-invalid-shadow",dQ="decoration/window/minimize-active-hovered.png",dP="menubar",eH="icon/16/actions/dialog-cancel.png",eI="tabview-page-button-top-inactive",eJ="tabview-page-button-left-inactive",eK="menu-slidebar",eD="toolbar-button-checked",eE="decoration/tree/open-selected.png",eF="decoration/window/minimize-inactive.png",eG="icon/16/apps/office-calendar.png",eB="group-item-css",eC="group",k="tabview-page-button-right-inactive",j="decoration/window/minimize-active.png",i="decoration/window/restore-inactive.png",h="checkbox-checked-focused",g="splitpane",f="combobox/textfield",e="decoration/window/close-active-hovered.png",d="qx/icon/Tango/16/actions/window-close.png",c="checkbox-pressed",b="button-disabled",J="selected-dragover",K="tooltip-error-css",H="decoration/window/maximize-inactive.png",I="dragover",N="scrollarea",O="scrollbar-vertical",L="decoration/menu/checkbox-invert.gif",M="decoration/toolbar/toolbar-handle-knob.gif",Q="icon/22/mimetypes/office-document.png",R="table-header-cell",cW="button-checked-focused",cQ="up.png",de="best-fit",da="pane-css",cF="decoration/tree/closed-selected.png",cD="qx.theme.modern.Appearance",bf="text-active",cG="checkbox-disabled",bq="toolbar-button-hovered",bp="window-resize-frame-incl-statusbar-css",ck="decoration/form/checked.png",cl="progressive-table-header",cm="decoration/table/select-column-order.png",cn="decoration/menu/radiobutton.gif",co="decoration/arrows/forward.png",cp="decoration/table/descending.png",cq="decoration/form/undetermined.png",cr="tree-file",ch="window-captionbar-active",ci="checkbox-checked-hovered",cE="scrollbar-slider-vertical",dd="toolbar",dc="alias",db="decoration/window/restore-active.png",di="decoration/table/boolean-false.png",dh="icon/32/mimetypes/office-document.png",dg="tabview-pane",df="decoration/arrows/rewind.png",cY="top",cX="icon/16/actions/dialog-ok.png",P="progressbar-background",bu="table-header-cell-hovered",bt="window-statusbar-css",cP="window",bF="text-gray",cV="decoration/menu/radiobutton-invert.gif",cU="text-placeholder",cT="slider",be="toolbar-css",dk="keep-align",S="down.png",bg="groupitem-text",cb="tabview-page-button-top-active",cc="icon/22/places/folder.png",cd="decoration/window/maximize-active.png",ce="checkbox-checked-pressed",cf="decoration/window/close-inactive.png",cg="tabview-page-button-left-active",dD="toolbar-part",cj="decoration/splitpane/knob-vertical.png",ec=".gif",eb="virtual-row-layer-background-odd",ee="table-statusbar",ed="progressive-table-header-cell-css",eg="window-captionbar-inactive",ef="copy",cs="decoration/arrows/down-invert.png",dR="decoration/menu/checkbox.gif",dj="window-caption-active-text",dG="decoration/splitpane/knob-horizontal.png",F="group-css",G="icon/32/places/folder.png",dy="virtual-row-layer-background-even",dz="toolbar-separator",dw="tabview-page-button-bottom-active",dx="decoration/arrows/up-small.png",du="decoration/table/ascending.png",dv="decoration/arrows/up-invert.png",a="small",dC="tabview-page-button-right-active",s="-disabled",r="scrollbar-horizontal",q="progressbar",p="checkbox-undetermined-focused",o="progressive-table-header-cell",n="menu-separator",m="tabview-pane-css",l="pane",u="htmlarea-background",t="decoration/arrows/right-invert.png",eL="left.png",eM="icon/16/actions/view-refresh.png";
qx.Theme.define(cD,{appearances:{"widget":{},"root":{style:function(eX){return {backgroundColor:A,textColor:eV,font:T};
}},"label":{style:function(eY){return {textColor:eY.disabled?cA:undefined};
}},"move-frame":{style:function(fa){return {decorator:ej};
}},"resize-frame":bV,"dragdrop-cursor":{style:function(fb){var fc=bW;

if(fb.copy){fc=ef;
}else if(fb.move){fc=cH;
}else if(fb.alias){fc=dc;
}return {source:bQ+fc+ec,position:C,offset:[2,16,2,6]};
}},"image":{style:function(fd){return {opacity:!fd.replacement&&fd.disabled?0.3:1};
}},"atom":{},"atom/label":cw,"atom/icon":cB,"popup":{style:function(fe){var ff=qx.core.Environment.get(ek);
return {decorator:ff?bU:ej,backgroundColor:cx,shadow:ff?undefined:bJ};
}},"button-frame":{alias:eo,style:function(fg){var fk,fj;
var fh=[3,9];

if(fg.checked&&fg.focused&&!fg.inner){fk=cW;
fj=undefined;
fh=[1,7];
}else if(fg.disabled){fk=b;
fj=undefined;
}else if(fg.pressed){fk=dU;
fj=Y;
}else if(fg.checked){fk=bi;
fj=undefined;
}else if(fg.hovered){fk=dl;
fj=Y;
}else if(fg.focused&&!fg.inner){fk=bC;
fj=undefined;
fh=[1,7];
}else{fk=ei;
fj=undefined;
}var fi;
if(qx.core.Environment.get(el)&&qx.core.Environment.get(eq)){if(fg.invalid&&!fg.disabled){fk+=bY;
}else{fk+=en;
}}else{fi=fg.invalid&&!fg.disabled?dY:undefined;
fh=[2,8];
}return {decorator:fk,textColor:fj,shadow:fi,padding:fh,margin:[1,0]};
}},"button-frame/image":{style:function(fl){return {opacity:!fl.replacement&&fl.disabled?0.5:1};
}},"button":{alias:em,include:em,style:function(fm){return {center:true};
}},"hover-button":{alias:eo,include:eo,style:function(fn){var fo=fn.hovered?cy:undefined;

if(fo&&qx.core.Environment.get(eq)){fo+=en;
}return {decorator:fo,textColor:fn.hovered?cC:undefined};
}},"splitbutton":{},"splitbutton/button":ei,"splitbutton/arrow":{alias:ei,include:ei,style:function(fp,fq){return {icon:cu,padding:[fq.padding[0],fq.padding[1]-6],marginLeft:1};
}},"checkbox":{alias:eo,style:function(fr){var fs=qx.core.Environment.get(eq)&&qx.core.Environment.get(ek);
var fu;

if(fs){if(fr.checked){fu=ck;
}else if(fr.undetermined){fu=cq;
}else{fu=dI;
}}else{if(fr.checked){if(fr.disabled){fu=bD;
}else if(fr.focused){fu=h;
}else if(fr.pressed){fu=ce;
}else if(fr.hovered){fu=ci;
}else{fu=bD;
}}else if(fr.undetermined){if(fr.disabled){fu=ba;
}else if(fr.focused){fu=p;
}else if(fr.hovered){fu=ds;
}else{fu=ba;
}}else if(!fr.disabled){if(fr.focused){fu=bG;
}else if(fr.pressed){fu=c;
}else if(fr.hovered){fu=by;
}}fu=fu||dE;
var ft=fr.invalid&&!fr.disabled?y:w;
fu=bk+fu+ft+X;
}return {icon:fu,minWidth:fs?14:undefined,gap:fs?8:6};
}},"checkbox/icon":{style:function(fv){var fx=qx.core.Environment.get(eq)&&qx.core.Environment.get(ek);

if(!fx){return {opacity:!fv.replacement&&fv.disabled?0.3:1};
}var fy;

if(fv.disabled){fy=cG;
}else if(fv.focused){fy=bG;
}else if(fv.hovered){fy=by;
}else{fy=dE;
}fy+=fv.invalid&&!fv.disabled?y:w;
var fw;
if(fv.undetermined){fw=[2,0];
}return {decorator:fy,padding:fw,width:12,height:10};
}},"radiobutton":{alias:eo,style:function(fz){var fA=qx.core.Environment.get(el)&&qx.core.Environment.get(ek);
var fC;

if(fA){fC=dI;
}else{if(fz.checked&&fz.focused){fC=eW;
}else if(fz.checked&&fz.disabled){fC=bN;
}else if(fz.checked&&fz.hovered){fC=bH;
}else if(fz.checked){fC=bB;
}else if(fz.focused){fC=bj;
}else if(fz.hovered){fC=eP;
}else{fC=dH;
}var fB=fz.invalid&&!fz.disabled?y:w;
fC=bk+fC+fB+X;
}return {icon:fC,gap:fA?8:6};
}},"radiobutton/icon":{style:function(fD){var fE=qx.core.Environment.get(el)&&qx.core.Environment.get(ek);

if(!fE){return {opacity:!fD.replacement&&fD.disabled?0.3:1};
}var fF;

if(fD.disabled&&!fD.checked){fF=dS;
}else if(fD.checked&&fD.focused){fF=eW;
}else if(fD.checked&&fD.disabled){fF=bN;
}else if(fD.checked&&fD.hovered){fF=bH;
}else if(fD.checked){fF=bB;
}else if(fD.focused){fF=bj;
}else if(fD.hovered){fF=eP;
}else{fF=dH;
}fF+=fD.invalid&&!fD.disabled?y:w;
return {decorator:fF,width:12,height:10};
}},"textfield":{style:function(fG){var fL;
var fJ=!!fG.focused;
var fK=!!fG.invalid;
var fH=!!fG.disabled;

if(fJ&&fK&&!fH){fL=eu;
}else if(fJ&&!fK&&!fH){fL=ez;
}else if(fH){fL=ew;
}else if(!fJ&&fK&&!fH){fL=ey;
}else{fL=ev;
}
if(qx.core.Environment.get(eq)){fL+=en;
}var fI;

if(fG.disabled){fI=cA;
}else if(fG.showingPlaceholder){fI=cU;
}else{fI=bc;
}return {decorator:fL,padding:[2,4,1],textColor:fI};
}},"textarea":{include:x,style:function(fM){return {padding:4};
}},"spinner":{style:function(fN){var fR;
var fP=!!fN.focused;
var fQ=!!fN.invalid;
var fO=!!fN.disabled;

if(fP&&fQ&&!fO){fR=eu;
}else if(fP&&!fQ&&!fO){fR=ez;
}else if(fO){fR=ew;
}else if(!fP&&fQ&&!fO){fR=ey;
}else{fR=ev;
}
if(qx.core.Environment.get(eq)){fR+=en;
}return {decorator:fR};
}},"spinner/textfield":{style:function(fS){return {marginRight:2,padding:[2,4,1],textColor:fS.disabled?cA:bc};
}},"spinner/upbutton":{alias:em,include:em,style:function(fT,fU){return {icon:dx,padding:[fU.padding[0]-1,fU.padding[1]-5],shadow:undefined,margin:0};
}},"spinner/downbutton":{alias:em,include:em,style:function(fV,fW){return {icon:bK,padding:[fW.padding[0]-1,fW.padding[1]-5],shadow:undefined,margin:0};
}},"datefield":dM,"datefield/button":{alias:eT,include:eT,style:function(fX){return {icon:eG,padding:[0,3],decorator:undefined};
}},"datefield/textfield":f,"datefield/list":{alias:bL,include:bL,style:function(fY){return {decorator:undefined};
}},"groupbox":{style:function(ga){return {legendPosition:cY};
}},"groupbox/legend":{alias:eo,style:function(gb){return {padding:[1,0,1,4],textColor:gb.invalid?B:E,font:eh};
}},"groupbox/frame":{style:function(gc){var gd=qx.core.Environment.get(el);
return {padding:gd?10:12,margin:gd?1:undefined,decorator:gd?F:eC};
}},"check-groupbox":cv,"check-groupbox/legend":{alias:dE,include:dE,style:function(ge){return {padding:[1,0,1,4],textColor:ge.invalid?B:E,font:eh};
}},"radio-groupbox":cv,"radio-groupbox/legend":{alias:dH,include:dH,style:function(gf){return {padding:[1,0,1,4],textColor:gf.invalid?B:E,font:eh};
}},"scrollarea":{style:function(gg){return {minWidth:50,minHeight:50};
}},"scrollarea/corner":{style:function(gh){return {backgroundColor:A};
}},"scrollarea/pane":ep,"scrollarea/scrollbar-x":dO,"scrollarea/scrollbar-y":dO,"scrollbar":{style:function(gi){if(gi[ea]){return {};
}var gj=qx.core.Environment.get(eq);
var gk=gi.horizontal?r:O;

if(gj){gk+=en;
}return {width:gi.horizontal?undefined:16,height:gi.horizontal?16:undefined,decorator:gk,padding:1};
}},"scrollbar/slider":{alias:cT,style:function(gl){return {padding:gl.horizontal?[0,1,0,1]:[1,0,1,0]};
}},"scrollbar/slider/knob":{include:em,style:function(gm){var gn=qx.core.Environment.get(eq);
var go=gm.horizontal?bx:cE;

if(gm.disabled){go+=s;
}
if(gn){go+=en;
}return {decorator:go,minHeight:gm.horizontal?undefined:9,minWidth:gm.horizontal?9:undefined,padding:undefined,margin:0};
}},"scrollbar/button":{alias:em,include:em,style:function(gp){var gs=dm;

if(gp.left){gs+=eL;
}else if(gp.right){gs+=cR;
}else if(gp.up){gs+=cQ;
}else{gs+=S;
}var gr=qx.core.Environment.get(eq);

if(gp.left||gp.right){var gq=gp.left?3:4;
return {padding:gr?[3,0,3,gq]:[2,0,2,gq],icon:gs,width:15,height:14,margin:0};
}else{return {padding:gr?3:[3,2],icon:gs,width:14,height:15,margin:0};
}}},"scrollbar/button-begin":eN,"scrollbar/button-end":eN,"slider":{style:function(gt){var gx;
var gv=!!gt.focused;
var gw=!!gt.invalid;
var gu=!!gt.disabled;

if(gv&&gw&&!gu){gx=eu;
}else if(gv&&!gw&&!gu){gx=ez;
}else if(gu){gx=ew;
}else if(!gv&&gw&&!gu){gx=ey;
}else{gx=ev;
}
if(qx.core.Environment.get(eq)){gx+=en;
}return {decorator:gx};
}},"slider/knob":{include:em,style:function(gy){return {decorator:gy.disabled?dT:bx,shadow:undefined,height:14,width:14,padding:0};
}},"list":{alias:N,style:function(gz){var gD;
var gB=!!gz.focused;
var gC=!!gz.invalid;
var gA=!!gz.disabled;

if(gB&&gC&&!gA){gD=eu;
}else if(gB&&!gC&&!gA){gD=ez;
}else if(gA){gD=ew;
}else if(!gB&&gC&&!gA){gD=ey;
}else{gD=ev;
}
if(qx.core.Environment.get(eq)){gD+=en;
}return {backgroundColor:cx,decorator:gD};
}},"list/pane":ep,"listitem":{alias:eo,style:function(gE){var gF;

if(gE.dragover){gF=gE.selected?J:I;
}else{gF=gE.selected?cy:undefined;

if(gF&&qx.core.Environment.get(eq)){gF+=en;
}}return {padding:gE.dragover?[4,4,2,4]:4,textColor:gE.selected?cC:undefined,decorator:gF};
}},"slidebar":{},"slidebar/scrollpane":{},"slidebar/content":{},"slidebar/button-forward":{alias:em,include:em,style:function(gG){return {padding:5,center:true,icon:gG.vertical?cu:z};
}},"slidebar/button-backward":{alias:em,include:em,style:function(gH){return {padding:5,center:true,icon:gH.vertical?bl:bE};
}},"tabview":{style:function(gI){return {contentPadding:16};
}},"tabview/bar":{alias:bR,style:function(gJ){var gK=qx.core.Environment.get(el)&&qx.core.Environment.get(ek)&&qx.core.Environment.get(eq);
var gL={marginBottom:gJ.barTop?-1:0,marginTop:gJ.barBottom?gK?-4:-7:0,marginLeft:gJ.barRight?gK?-3:-5:0,marginRight:gJ.barLeft?-1:0,paddingTop:0,paddingRight:0,paddingBottom:0,paddingLeft:0};

if(gJ.barTop||gJ.barBottom){gL.paddingLeft=5;
gL.paddingRight=7;
}else{gL.paddingTop=5;
gL.paddingBottom=7;
}return gL;
}},"tabview/bar/button-forward":{include:W,alias:W,style:function(gM){if(gM.barTop||gM.barBottom){return {marginTop:2,marginBottom:2};
}else{return {marginLeft:2,marginRight:2};
}}},"tabview/bar/button-backward":{include:bM,alias:bM,style:function(gN){if(gN.barTop||gN.barBottom){return {marginTop:2,marginBottom:2};
}else{return {marginLeft:2,marginRight:2};
}}},"tabview/bar/scrollpane":{},"tabview/pane":{style:function(gO){var gP=qx.core.Environment.get(eq)&&qx.core.Environment.get(el);
return {decorator:gP?m:dg,minHeight:100,marginBottom:gO.barBottom?-1:0,marginTop:gO.barTop?-1:0,marginLeft:gO.barLeft?-1:0,marginRight:gO.barRight?-1:0};
}},"tabview-page":{alias:ep,include:ep,style:function(gQ){var gR=qx.core.Environment.get(eq)&&qx.core.Environment.get(el);
return {padding:gR?[4,3]:undefined};
}},"tabview-page/button":{alias:eo,style:function(gS){var ha,gV=0;
var gY=0,gT=0,gW=0,gX=0;
var gU=qx.core.Environment.get(el)&&qx.core.Environment.get(ek)&&qx.core.Environment.get(eq);

if(gS.checked){if(gS.barTop){ha=cb;
gV=gU?[5,11]:[6,14];
gW=gS.firstTab?0:-5;
gX=gS.lastTab?0:-5;
}else if(gS.barBottom){ha=dw;
gV=gU?[5,11]:[6,14];
gW=gS.firstTab?0:-5;
gX=gS.lastTab?0:-5;
gY=3;
}else if(gS.barRight){ha=dC;
gV=gU?[5,10]:[6,13];
gY=gS.firstTab?0:-5;
gT=gS.lastTab?0:-5;
gW=2;
}else{ha=cg;
gV=gU?[5,10]:[6,13];
gY=gS.firstTab?0:-5;
gT=gS.lastTab?0:-5;
}}else{if(gS.barTop){ha=eI;
gV=gU?[3,9]:[4,10];
gY=4;
gW=gS.firstTab?5:1;
gX=1;
}else if(gS.barBottom){ha=dq;
gV=gU?[3,9]:[4,10];
gT=4;
gW=gS.firstTab?5:1;
gX=1;
gY=3;
}else if(gS.barRight){ha=k;
gV=gU?[3,9]:[4,10];
gX=5;
gY=gS.firstTab?5:1;
gT=1;
gW=3;
}else{ha=eJ;
gV=gU?[3,9]:[4,10];
gW=5;
gY=gS.firstTab?5:1;
gT=1;
gX=1;
}}
if(ha&&gU){ha+=en;
}return {zIndex:gS.checked?10:5,decorator:ha,padding:gV,marginTop:gY,marginBottom:gT,marginLeft:gW,marginRight:gX,textColor:gS.disabled?cA:gS.checked?bf:cI};
}},"tabview-page/button/label":{alias:cw,style:function(hb){return {padding:[0,1,0,1],margin:hb.focused?0:1,decorator:hb.focused?bs:undefined};
}},"tabview-page/button/close-button":{alias:eo,style:function(hc){return {icon:d};
}},"toolbar":{style:function(hd){var he=qx.core.Environment.get(eq);
return {decorator:he?be:dd,spacing:2};
}},"toolbar/part":{style:function(hf){return {decorator:dD,spacing:2};
}},"toolbar/part/container":{style:function(hg){return {paddingLeft:2,paddingRight:2};
}},"toolbar/part/handle":{style:function(hh){return {source:M,marginLeft:3,marginRight:3};
}},"toolbar-button":{alias:eo,style:function(hi){var hk;

if(hi.pressed||(hi.checked&&!hi.hovered)||(hi.checked&&hi.disabled)){hk=eD;
}else if(hi.hovered&&!hi.disabled){hk=bq;
}var hj=qx.core.Environment.get(eq)&&qx.core.Environment.get(el);

if(hj&&hk){hk+=en;
}return {marginTop:2,marginBottom:2,padding:(hi.pressed||hi.checked||hi.hovered)&&!hi.disabled||(hi.disabled&&hi.checked)?3:5,decorator:hk};
}},"toolbar-menubutton":{alias:er,include:er,style:function(hl){return {showArrow:true};
}},"toolbar-menubutton/arrow":{alias:cB,include:cB,style:function(hm){return {source:bK};
}},"toolbar-splitbutton":{style:function(hn){return {marginTop:2,marginBottom:2};
}},"toolbar-splitbutton/button":{alias:er,include:er,style:function(ho){return {icon:cu,marginTop:undefined,marginBottom:undefined};
}},"toolbar-splitbutton/arrow":{alias:er,include:er,style:function(hp){if(hp.pressed||hp.checked||(hp.hovered&&!hp.disabled)){var hq=1;
}else{var hq=3;
}return {padding:hq,icon:cu,marginTop:undefined,marginBottom:undefined};
}},"toolbar-separator":{style:function(hr){return {decorator:dz,margin:7};
}},"tree":dK,"tree-item":{style:function(hs){var ht=hs.selected?cy:undefined;

if(ht&&qx.core.Environment.get(eq)){ht+=en;
}return {padding:[2,6],textColor:hs.selected?cC:undefined,decorator:ht};
}},"tree-item/icon":{include:cB,style:function(hu){return {paddingRight:5};
}},"tree-item/label":cw,"tree-item/open":{include:cB,style:function(hv){var hw;

if(hv.selected&&hv.opened){hw=eE;
}else if(hv.selected&&!hv.opened){hw=cF;
}else if(hv.opened){hw=U;
}else{hw=bz;
}return {padding:[0,5,0,2],source:hw};
}},"tree-folder":{include:dJ,alias:dJ,style:function(hx){var hz,hy;

if(hx.small){hz=hx.opened?eQ:eR;
hy=eQ;
}else if(hx.large){hz=hx.opened?bo:G;
hy=bo;
}else{hz=hx.opened?bn:cc;
hy=bn;
}return {icon:hz,iconOpened:hy};
}},"tree-file":{include:dJ,alias:dJ,style:function(hA){return {icon:hA.small?bO:hA.large?dh:Q};
}},"treevirtual":bm,"treevirtual-folder":{style:function(hB){return {icon:hB.opened?eQ:eR};
}},"treevirtual-file":{include:bI,alias:bI,style:function(hC){return {icon:bO};
}},"treevirtual-line":{style:function(hD){return {icon:dI};
}},"treevirtual-contract":{style:function(hE){return {icon:U,paddingLeft:5,paddingTop:2};
}},"treevirtual-expand":{style:function(hF){return {icon:bz,paddingLeft:5,paddingTop:2};
}},"treevirtual-only-contract":dL,"treevirtual-only-expand":v,"treevirtual-start-contract":dL,"treevirtual-start-expand":v,"treevirtual-end-contract":dL,"treevirtual-end-expand":v,"treevirtual-cross-contract":dL,"treevirtual-cross-expand":v,"treevirtual-end":{style:function(hG){return {icon:dI};
}},"treevirtual-cross":{style:function(hH){return {icon:dI};
}},"tooltip":{include:ct,style:function(hI){return {backgroundColor:dA,padding:[1,3,2,3],offset:[15,5,5,5]};
}},"tooltip/atom":eo,"tooltip-error":{include:eA,style:function(hJ){var hK=qx.core.Environment.get(el)&&qx.core.Environment.get(ek);
return {textColor:cC,backgroundColor:undefined,placeMethod:ep,offset:[0,0,0,14],marginTop:-2,position:C,showTimeout:100,hideTimeout:10000,decorator:hK?K:dr,shadow:bS,font:eh,padding:hK?3:undefined};
}},"tooltip-error/atom":eo,"window":{style:function(hL){var hN=qx.core.Environment.get(el)&&qx.core.Environment.get(eq)&&qx.core.Environment.get(ek);
var hO;
var hM;

if(hN){if(hL.showStatusbar){hO=dt;
}else{hO=dn;
}}else{hM=cM;
}return {decorator:hO,shadow:hM,contentPadding:[10,10,10,10],margin:[0,5,5,0]};
}},"window-resize-frame":{style:function(hP){var hQ=qx.core.Environment.get(el);
var hR;

if(hQ){if(hP.showStatusbar){hR=bp;
}else{hR=dV;
}}else{hR=ej;
}return {decorator:hR};
}},"window/pane":{style:function(hS){var hT=qx.core.Environment.get(el)&&qx.core.Environment.get(eq)&&qx.core.Environment.get(ek);
return {decorator:hT?cS:cP};
}},"window/captionbar":{style:function(hU){var hV=qx.core.Environment.get(el)&&qx.core.Environment.get(eq)&&qx.core.Environment.get(ek);
var hW=hU.active?ch:eg;

if(hV){hW+=en;
}return {decorator:hW,textColor:hU.active?dj:bF,minHeight:26,paddingRight:2};
}},"window/icon":{style:function(hX){return {margin:[5,0,3,6]};
}},"window/title":{style:function(hY){return {alignY:cz,font:eh,marginLeft:6,marginRight:12};
}},"window/minimize-button":{alias:eo,style:function(ia){return {icon:ia.active?ia.hovered?dQ:j:eF,margin:[4,8,2,0]};
}},"window/restore-button":{alias:eo,style:function(ib){return {icon:ib.active?ib.hovered?cO:db:i,margin:[5,8,2,0]};
}},"window/maximize-button":{alias:eo,style:function(ic){return {icon:ic.active?ic.hovered?bh:cd:H,margin:[4,8,2,0]};
}},"window/close-button":{alias:eo,style:function(id){return {icon:id.active?id.hovered?e:dW:cf,margin:[4,8,2,0]};
}},"window/statusbar":{style:function(ie){var ig=qx.core.Environment.get(el)&&qx.core.Environment.get(eq)&&qx.core.Environment.get(ek);
return {padding:[2,6],decorator:ig?bt:dp,minHeight:18};
}},"window/statusbar-text":{style:function(ih){return {font:a};
}},"iframe":{style:function(ii){return {decorator:ej};
}},"resizer":{style:function(ij){var ik=qx.core.Environment.get(ek)&&qx.core.Environment.get(el)&&qx.core.Environment.get(eq);
return {decorator:ik?da:l};
}},"splitpane":{style:function(il){return {decorator:g};
}},"splitpane/splitter":{style:function(im){return {width:im.horizontal?3:undefined,height:im.vertical?3:undefined,backgroundColor:V};
}},"splitpane/splitter/knob":{style:function(io){return {source:io.horizontal?dG:cj};
}},"splitpane/slider":{style:function(ip){return {width:ip.horizontal?3:undefined,height:ip.vertical?3:undefined,backgroundColor:V};
}},"selectbox":em,"selectbox/atom":eo,"selectbox/popup":ct,"selectbox/list":{alias:dK},"selectbox/arrow":{include:cB,style:function(iq){return {source:cu,paddingLeft:5};
}},"datechooser":{style:function(ir){var iv;
var it=!!ir.focused;
var iu=!!ir.invalid;
var is=!!ir.disabled;

if(it&&iu&&!is){iv=eu;
}else if(it&&!iu&&!is){iv=ez;
}else if(is){iv=ew;
}else if(!it&&iu&&!is){iv=ey;
}else{iv=ev;
}
if(qx.core.Environment.get(eq)){iv+=en;
}return {padding:2,decorator:iv,backgroundColor:cx};
}},"datechooser/navigation-bar":{},"datechooser/nav-button":{include:em,alias:em,style:function(iw){var ix={padding:[2,4],shadow:undefined};

if(iw.lastYear){ix.icon=df;
ix.marginRight=1;
}else if(iw.lastMonth){ix.icon=bE;
}else if(iw.nextYear){ix.icon=co;
ix.marginLeft=1;
}else if(iw.nextMonth){ix.icon=z;
}return ix;
}},"datechooser/last-year-button-tooltip":eA,"datechooser/last-month-button-tooltip":eA,"datechooser/next-year-button-tooltip":eA,"datechooser/next-month-button-tooltip":eA,"datechooser/last-year-button":dN,"datechooser/last-month-button":dN,"datechooser/next-month-button":dN,"datechooser/next-year-button":dN,"datechooser/month-year-label":{style:function(iy){return {font:eh,textAlign:dF,textColor:iy.disabled?cA:undefined};
}},"datechooser/date-pane":{style:function(iz){return {textColor:iz.disabled?cA:undefined,marginTop:2};
}},"datechooser/weekday":{style:function(iA){return {textColor:iA.disabled?cA:iA.weekend?bv:undefined,textAlign:dF,paddingTop:2,backgroundColor:bP};
}},"datechooser/week":{style:function(iB){return {textAlign:dF,padding:[2,4],backgroundColor:bP};
}},"datechooser/day":{style:function(iC){var iD=iC.disabled?undefined:iC.selected?cy:undefined;

if(iD&&qx.core.Environment.get(eq)){iD+=en;
}return {textAlign:dF,decorator:iD,textColor:iC.disabled?cA:iC.selected?cC:iC.otherMonth?bv:undefined,font:iC.today?eh:undefined,padding:[2,4]};
}},"combobox":{style:function(iE){var iI;
var iG=!!iE.focused;
var iH=!!iE.invalid;
var iF=!!iE.disabled;

if(iG&&iH&&!iF){iI=eu;
}else if(iG&&!iH&&!iF){iI=ez;
}else if(iF){iI=ew;
}else if(!iG&&iH&&!iF){iI=ey;
}else{iI=ev;
}
if(qx.core.Environment.get(eq)){iI+=en;
}return {decorator:iI};
}},"combobox/popup":ct,"combobox/list":{alias:dK},"combobox/button":{include:em,alias:em,style:function(iJ,iK){var iL={icon:cu,padding:[iK.padding[0],iK.padding[1]-6],shadow:undefined,margin:undefined};

if(iJ.selected){iL.decorator=bC;
}return iL;
}},"combobox/textfield":{include:x,style:function(iM){return {decorator:undefined};
}},"menu":{style:function(iN){var iO=qx.core.Environment.get(eq)&&qx.core.Environment.get(ek);
var iP={decorator:iO?br:ca,shadow:iO?undefined:bJ,spacingX:6,spacingY:1,iconColumnWidth:16,arrowColumnWidth:4,placementModeY:iN.submenu||iN.contextmenu?de:dk};

if(iN.submenu){iP.position=C;
iP.offset=[-2,-3];
}return iP;
}},"menu/slidebar":eK,"menu-slidebar":ep,"menu-slidebar-button":{style:function(iQ){var iR=iQ.hovered?cy:undefined;

if(iR&&qx.core.Environment.get(eq)){iR+=en;
}return {decorator:iR,padding:7,center:true};
}},"menu-slidebar/button-backward":{include:bw,style:function(iS){return {icon:iS.hovered?dv:bl};
}},"menu-slidebar/button-forward":{include:bw,style:function(iT){return {icon:iT.hovered?cs:cu};
}},"menu-separator":{style:function(iU){return {height:0,decorator:n,margin:[4,2]};
}},"menu-button":{alias:eo,style:function(iV){var iW=iV.selected?cy:undefined;

if(iW&&qx.core.Environment.get(eq)){iW+=en;
}return {decorator:iW,textColor:iV.selected?cC:undefined,padding:[4,6]};
}},"menu-button/icon":{include:cB,style:function(iX){return {alignY:cz};
}},"menu-button/label":{include:cw,style:function(iY){return {alignY:cz,padding:1};
}},"menu-button/shortcut":{include:cw,style:function(ja){return {alignY:cz,marginLeft:14,padding:1};
}},"menu-button/arrow":{include:cB,style:function(jb){return {source:jb.selected?t:z,alignY:cz};
}},"menu-checkbox":{alias:et,include:et,style:function(jc){return {icon:!jc.checked?undefined:jc.selected?L:dR};
}},"menu-radiobutton":{alias:et,include:et,style:function(jd){return {icon:!jd.checked?undefined:jd.selected?cV:cn};
}},"menubar":{style:function(je){var jf=qx.core.Environment.get(eq);
return {decorator:jf?dB:dP};
}},"menubar-button":{alias:eo,style:function(jg){var jh=(jg.pressed||jg.hovered)&&!jg.disabled?cy:undefined;

if(jh&&qx.core.Environment.get(eq)){jh+=en;
}return {decorator:jh,textColor:jg.pressed||jg.hovered?cC:undefined,padding:[3,8]};
}},"colorselector":ep,"colorselector/control-bar":ep,"colorselector/control-pane":ep,"colorselector/visual-pane":cv,"colorselector/preset-grid":ep,"colorselector/colorbucket":{style:function(ji){return {decorator:ej,width:16,height:16};
}},"colorselector/preset-field-set":cv,"colorselector/input-field-set":cv,"colorselector/preview-field-set":cv,"colorselector/hex-field-composite":ep,"colorselector/hex-field":x,"colorselector/rgb-spinner-composite":ep,"colorselector/rgb-spinner-red":es,"colorselector/rgb-spinner-green":es,"colorselector/rgb-spinner-blue":es,"colorselector/hsb-spinner-composite":ep,"colorselector/hsb-spinner-hue":es,"colorselector/hsb-spinner-saturation":es,"colorselector/hsb-spinner-brightness":es,"colorselector/preview-content-old":{style:function(jj){return {decorator:ej,width:50,height:10};
}},"colorselector/preview-content-new":{style:function(jk){return {decorator:ej,backgroundColor:cx,width:50,height:10};
}},"colorselector/hue-saturation-field":{style:function(jl){return {decorator:ej,margin:5};
}},"colorselector/brightness-field":{style:function(jm){return {decorator:ej,margin:[5,7]};
}},"colorselector/hue-saturation-pane":ep,"colorselector/hue-saturation-handle":ep,"colorselector/brightness-pane":ep,"colorselector/brightness-handle":ep,"colorpopup":{alias:ct,include:ct,style:function(jn){return {padding:5,backgroundColor:A};
}},"colorpopup/field":{style:function(jo){return {decorator:ej,margin:2,width:14,height:14,backgroundColor:cx};
}},"colorpopup/selector-button":ei,"colorpopup/auto-button":ei,"colorpopup/preview-pane":cv,"colorpopup/current-preview":{style:function(jp){return {height:20,padding:4,marginLeft:4,decorator:ej,allowGrowX:true};
}},"colorpopup/selected-preview":{style:function(jq){return {height:20,padding:4,marginRight:4,decorator:ej,allowGrowX:true};
}},"colorpopup/colorselector-okbutton":{alias:ei,include:ei,style:function(jr){return {icon:cX};
}},"colorpopup/colorselector-cancelbutton":{alias:ei,include:ei,style:function(js){return {icon:eH};
}},"table":{alias:ep,style:function(jt){return {decorator:bm};
}},"table/statusbar":{style:function(ju){return {decorator:ee,padding:[0,2]};
}},"table/column-button":{alias:em,style:function(jv){var jw=qx.core.Environment.get(eq);
return {decorator:jw?bd:bA,padding:3,icon:cm};
}},"table-column-reset-button":{include:et,alias:et,style:function(){return {icon:eM};
}},"table-scroller":ep,"table-scroller/scrollbar-x":dO,"table-scroller/scrollbar-y":dO,"table-scroller/header":{style:function(jx){var jy=qx.core.Environment.get(eq);
return {decorator:jy?bd:bA};
}},"table-scroller/pane":{style:function(jz){return {backgroundColor:dX};
}},"table-scroller/focus-indicator":{style:function(jA){return {decorator:bT};
}},"table-scroller/resize-line":{style:function(jB){return {backgroundColor:cN,width:2};
}},"table-header-cell":{alias:eo,style:function(jC){return {minWidth:13,minHeight:20,padding:jC.hovered?[3,4,2,4]:[3,4],decorator:jC.hovered?bu:R,sortIcon:jC.sorted?(jC.sortedAscending?du:cp):undefined};
}},"table-header-cell/label":{style:function(jD){return {minWidth:0,alignY:cz,paddingRight:5};
}},"table-header-cell/sort-icon":{style:function(jE){return {alignY:cz,alignX:eU};
}},"table-header-cell/icon":{style:function(jF){return {minWidth:0,alignY:cz,paddingRight:5};
}},"table-editor-textfield":{include:x,style:function(jG){return {decorator:undefined,padding:[2,2],backgroundColor:cx};
}},"table-editor-selectbox":{include:D,alias:D,style:function(jH){return {padding:[0,2],backgroundColor:cx};
}},"table-editor-combobox":{include:dM,alias:dM,style:function(jI){return {decorator:undefined,backgroundColor:cx};
}},"progressive-table-header":{alias:ep,style:function(jJ){return {decorator:cl};
}},"progressive-table-header-cell":{alias:eo,style:function(jK){var jL=qx.core.Environment.get(eq);
return {minWidth:40,minHeight:25,paddingLeft:6,decorator:jL?ed:o};
}},"app-header":{style:function(jM){return {font:eh,textColor:cC,padding:[8,12],decorator:cK};
}},"app-header-label":cw,"virtual-list":dK,"virtual-list/row-layer":cJ,"row-layer":{style:function(jN){return {colorEven:dy,colorOdd:eb};
}},"group-item":{include:cw,alias:cw,style:function(jO){return {padding:4,decorator:qx.core.Environment.get(eq)?eB:eO,textColor:bg,font:eh};
}},"virtual-selectbox":D,"virtual-selectbox/dropdown":ct,"virtual-selectbox/dropdown/list":{alias:eS},"virtual-combobox":dM,"virtual-combobox/dropdown":ct,"virtual-combobox/dropdown/list":{alias:eS},"virtual-tree":{include:bb,alias:bb,style:function(jP){return {itemHeight:26};
}},"virtual-tree-folder":cL,"virtual-tree-file":cr,"column-layer":ep,"cell":{style:function(jQ){return {textColor:jQ.selected?cC:eV,padding:[3,6],font:T};
}},"cell-string":ex,"cell-number":{include:ex,style:function(jR){return {textAlign:eU};
}},"cell-image":ex,"cell-boolean":{include:ex,style:function(jS){return {iconTrue:bX,iconFalse:di};
}},"cell-atom":ex,"cell-date":ex,"cell-html":ex,"htmlarea":{"include":ep,style:function(jT){return {backgroundColor:u};
}},"progressbar":{style:function(jU){return {decorator:q,padding:[1],backgroundColor:P};
}},"progressbar/progress":{style:function(jV){var jW=jV.disabled?eO:cy;

if(qx.core.Environment.get(eq)){jW+=en;
}return {decorator:jW};
}}}});
})();
(function(){var a="scoville_admin.theme.Appearance";
qx.Theme.define(a,{extend:qx.theme.modern.Appearance,appearances:{}});
})();
(function(){var t="os.version",s="os.name",r="win",q="7",p="vista",o="osx",n="Liberation Sans",m="Tahoma",l="sans-serif",k="Arial",d="Lucida Grande",j="Candara",g="Segoe UI",c="Consolas",b="monospace",f="Courier New",e="Lucida Console",h="Monaco",a="qx.theme.modern.Font",i="DejaVu Sans Mono";
qx.Theme.define(a,{fonts:{"default":{size:(qx.core.Environment.get(s)==r&&(qx.core.Environment.get(t)==q||qx.core.Environment.get(t)==p))?12:11,lineHeight:1.4,family:qx.core.Environment.get(s)==o?[d]:((qx.core.Environment.get(s)==r&&(qx.core.Environment.get(t)==q||qx.core.Environment.get(t)==p)))?[g,j]:[m,n,k,l]},"bold":{size:(qx.core.Environment.get(s)==r&&(qx.core.Environment.get(t)==q||qx.core.Environment.get(t)==p))?12:11,lineHeight:1.4,family:qx.core.Environment.get(s)==o?[d]:((qx.core.Environment.get(s)==r&&(qx.core.Environment.get(t)==q||qx.core.Environment.get(t)==p)))?[g,j]:[m,n,k,l],bold:true},"small":{size:(qx.core.Environment.get(s)==r&&(qx.core.Environment.get(t)==q||qx.core.Environment.get(t)==p))?11:10,lineHeight:1.4,family:qx.core.Environment.get(s)==o?[d]:((qx.core.Environment.get(s)==r&&(qx.core.Environment.get(t)==q||qx.core.Environment.get(t)==p)))?[g,j]:[m,n,k,l]},"monospace":{size:11,lineHeight:1.4,family:qx.core.Environment.get(s)==o?[e,h]:((qx.core.Environment.get(s)==r&&(qx.core.Environment.get(t)==q||qx.core.Environment.get(t)==p)))?[c]:[c,i,f,b]}}});
})();
(function(){var a="scoville_admin.theme.Font";
qx.Theme.define(a,{extend:qx.theme.modern.Font,fonts:{}});
})();
(function(){var a="scoville_admin.theme.Theme";
qx.Theme.define(a,{meta:{color:scoville_admin.theme.Color,decoration:scoville_admin.theme.Decoration,font:scoville_admin.theme.Font,icon:qx.theme.icon.Tango,appearance:scoville_admin.theme.Appearance}});
})();


qx.$$loader.init();

