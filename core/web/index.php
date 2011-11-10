<?php
  require '../lib/core.php';
  
  use scv;
  
  $core = scv\Core::getInstance();
  $db = $core->getDB();
  
  $moduleM = $core->getModuleManager();
  
  $parser = $core->getHtmlParser();
  $parser->parseHtml();

?>