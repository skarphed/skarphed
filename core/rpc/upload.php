<?php

include_once '../lib/core.php';

$core = scv\Core::getInstance();
$userM = $core->getUserManager();
$sessionUser = $userM->getSessionUser();

$output = "";

if (isset($sessionUser)){
	$rightM = $core->getRightsManager();
	//if ($rightM->checkRight('scoville.rpc.upload'),$sessionUser){
    if(true){
	    if ($_FILES['uploadfile']["error"] > 0){
		   	$output.="Failed";
	    }else{
	    	if(file_exists("/tmp/".$_FILES['uploadfile']['name'])){
	    		$output.="File Already Exists";
	    	}else{
	    		$data = file_get_contents($_FILES['uploadfile']['tmp_name']);
				$handle = fopen("/tmp/".$_FILES['uploadfile']['name'],"w");
				fwrite($handle,$data);
				fclose($handle);
				$output.="Uploaded ".$_FILES['uploadfile']['name'];
	    	}
			
	    	
			
		    //echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
		    
	    }
	}else{
		$output.="This User has no right to upload";
	}
}else{
	$output.="No valid Session";
}

$outputxml = "<xmlhttp><response><length>$output</length></response></xmlhttp>";


header('Content-Type: text/plain; name=response.xml');
header('Content-Disposition: inline; filename=response.xml');
header('Content-Length: '.strlen($outputxml));

echo($outputxml);

?>