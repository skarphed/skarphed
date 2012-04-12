<?php
	session_start();
	
	if (isset($_REQUEST['j'])){
		include_once('protocolhandler.php');
		try{
			$protocolHandler = new ProtocolHandler($_REQUEST['j']);
			$protocolHandler->execute();
		} catch (Exception $e) {
			echo "{'error':$e}";
		}
		echo $protocolHandler->getResult();
	}
	
	
?>