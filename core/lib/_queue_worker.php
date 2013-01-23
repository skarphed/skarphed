<?php
###########################################################
# Copyright 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Scoville.
#
# Scoville is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Scoville is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with Scoville. 
# If not, see http://www.gnu.org/licenses/.
###########################################################
	//use scv;
	
	$lockname = "/tmp/.queue_worker.pid";
	
	$arg = "";
	if (isset($argv[1])){
		$arg = $argv[1];
	}
	
	$state_running = 1;
	if(file_exists($lockname)){
		$lockfile = fopen($lockname,"r");
		$pidlock = (int)file_get_contents($lockname);
		fclose($lockfile);
		$state_running = 1;
	}else{
		$state_running = 0;
	}
	
	switch($arg){
		case "start":
			if ($state_running == 1){
				echo("Queue is already running!\n");
				exit(0);
			}
			
			unlink("/tmp/scv_operating.lck");
			
			$pid = pcntl_fork();
			if ($pid == -1){
				throw new Exception("NOT FORKED\n");
			}elseif($pid){
				$pidfile = fopen($lockname,"w");
				fwrite ($pidfile,$pid);
				fclose ($pidfile);
			}else{
				require_once 'core.php';
				$core = scv\Core::getInstance();
				$opM  = $core->getOperationManager();
				while(true){
					while($opM->processNext()){}
					sleep(2);
				}
			}
			exit(0);
		case "stop":
			if ($state_running == 0){
				echo("Queue is not running!\n");
				exit(0);
			}
			posix_kill($pidlock, SIGKILL);
			unlink($lockname);
			exit(0);
		case "status":
			if ($state_running == 1){
				echo("RUNNING!\n");
			}else{
				echo("NOT RUNNING!\n");
			}
			exit(0);
		default:
			echo("False Argument\n");
			exit(1);
	}
	
    
?>