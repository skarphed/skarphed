<?php
namespace scv;

include_once "core.php";

class HtmlParserException extends \Exception{}

class HtmlParser {
  
  public function __construct() {}
	
  public function parseHtml() {
    $core = Core::getInstance();
	$cssM = $core->getCssManager();
    $db = $core->getDB();
    $resultset = $db->query($core, "select first 1 sit_html, sit_filename from sites order by sit_id;");
    $result = $db->fetchArray($resultset);
	$cssName = str_replace(".html", ".css", $result['SIT_FILENAME']);
    echo "<!DOCTYPE HTML>
          <html>
            <head>
              <link type='text/css' href='".$cssM->getCssFile()."' rel='stylesheet'>
              <link type='text/css' href='".$cssName."' rel='stylesheet'>
            </head>
            <body>
              <div id='site'>";
    echo $result["SIT_HTML"];
	
	/*
	 * Der Parser Parst hier jeden Vorhandenen Space nach seinem Zugehoerigen modul und der Modulinstanz ab
	 * Ich gehe einfach mal davon aus, dass er bei jedem Fund die Core-Methode renderModule($moduleId, $moduleSubId) aufruft
	 * Die modul Sub-Id (wie auch immer sie aussehen wird, soll modulMehrfachinstanzen voneinander unterscheiden.)
	 */
	
    echo "    </div>
            </body>
            <script type='text/javascript' src='scvjs.php'></script>
          </html>";
  }
  
}
?>