<?php

require_once '../lib/core.php';

$core = Core::getInstance();
$userM = $core->getUserManager();
$sessionUser = $userM->getSessionUser();

$output = "";

$mode = $_GET['a'];

if (isset($sessionUser)){
	switch($mode){
		case "template":
			$rightM = $core->getRightsManager();
			//if ($rightM->checkRight('scoville.rpc.upload'),$sessionUser){
		    if(true){
		    	if ($_FILES['uploadfile']["error"] > 0){
		   			break;
	    		}
				if(file_exists("/tmp/".$_FILES['uploadfile']['name'])){
					break;
				}
				$data = file_get_contents($_FILES['uploadfile']['tmp_name']);
				$handle = fopen("/tmp/".$_FILES['uploadfile']['name'],"w");
				fwrite($handle,$data);
				fclose($handle);
				$output.="Uploaded ".$_FILES['uploadfile']['name'];
				$templateM = $core->getTemplateManager();
				$template = $templateM->createFromFile($_FILES['uploadfile']['name']);
				$template->install();
			}
			break;
		default:
			break;		
	}
}

/*
$outputxml = "<xmlhttp><response><length>$output</length></response></xmlhttp>";


header('Content-Type: text/plain; name=response.xml');
header('Content-Disposition: inline; filename=response.xml');
header('Content-Length: '.strlen($outputxml."\n\n"));

echo($outputxml);
*/

echo("TROLOLOLLLPLAINTEXT");
?>