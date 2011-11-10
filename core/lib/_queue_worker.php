<?php
	use scv;
    $pid = pcntl_fork();
	if ($pid == -1){
		throw new Exception("NOT FORKED");
	}elseif($pid){
	}else{
		require 'core.php';
		$core = scv\Core::getInstance();
		$opM  = $core->getOperationManager();
		while(true){
			while($opM->processNext()){}
			sleep(2);
		}
	}
?>