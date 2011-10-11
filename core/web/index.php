<?php
  require '../lib/core.php';
  
  use scv;
  
  $core = scv\Core::getInstance();
  $db = $core->getDB();
//  $db->getInfo();
  $parser = $core->getHtmlParser();
  $parser->parseHtml();
//   $core->getModuleManager()->installModule('de.zigapeda.scoville.clock');
//   $core->getModuleManager()->installModule('de.zigapeda.scoville.date');
//   $core->getModuleManager()->installModule('de.zigapeda.scoville.flatmenu');
  //init alles moegliche
  //html laden
//  echo "<!DOCTYPE HTML>
//<html>
//  <head>
//    <link type='text/css' href='style.php' rel='stylesheet'>
//  </head>
//  <body>";
//  //echo geladenes html
//  echo "    <div id='site'>
//      <div id='h1'>
//        <div id='s1'>
//        </div>
//      </div>
//      <div id='h2'>
//        <div id='v1'>
//          <div id='s2'>
//          </div>
//          <div id='s3'>
//          </div>
//        </div>
//        <div id='v2'>
//          <div id='s4'>
//          </div>
//        </div>
//        <div id='v3'>
//          <div id='s5'>
//          </div>
//        </div>
//      </div>
//      <div id='h3'>
//        <div id='s6'>
//        </div>
//      </div>
//    </div>";
//  echo "  </body>
//  <script type='text/javascript' src='scvjs.php'></script>
//</html>";
?>