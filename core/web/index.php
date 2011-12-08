<?php
  require '../lib/core.php';
  
  use scv;
  
  $core = scv\Core::getInstance();
  $db = $core->getDB();
  
  $moduleM = $core->getModuleManager();
  
  $cm = $core->getCompositeManager();
  $site = $cm->getFirstSite();
  echo $site->getHTML();
//   $parser = $core->getHtmlParser();
//   $parser->parseHtml();

?>