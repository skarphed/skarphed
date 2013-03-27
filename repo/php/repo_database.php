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

class DatabaseException extends \Exception {}

class repo_database {

	private $connection = null;
	
	private $user = null;
	private $ip = null;
	private $dbname = null;
	private $password = null;
	
	public function connect() {
		if ($this->user == null or $this->ip == null or $this->dbname == null or $this->password == null){
			throw new DatabaseException ('The Parameters for Connection have not been set');
		}
		$connectionstring = $this->ip.":/var/lib/firebird/2.5/data/".$this->dbname;
		$this->connection = ibase_connect($connectionstring,$this->user,$this->password,'UTF8'); 
		if (!$this->connection){
			throw new DatabaseException ('Could not connect to Database due to: '.ibase_errmsg());
		}
		return;
	}
	
	public function set_all($d_user, $d_ip,  $d_dbname,  $d_password) {
		$this->user = $d_user;
		$this->ip = $d_ip;
		$this->dbname = $d_dbname;
		$this->password = $d_password;
	}
	
	public function query($statement, $args=array()){
		$prepared = ibase_prepare($statement);
        array_unshift($args,$prepared);
		$resultset = call_user_func_array('ibase_execute',$args);
		if (!$resultset && ibase_errmsg() != ""){
			throw new DatabaseException('Execution failed due to: '.ibase_errmsg());
		}
		return $resultset;
	}
	
	public function fetchArray($resultset) {
		return ibase_fetch_assoc($resultset,ibase_text);
	}
	
	public function fetchObject($resultset) {
		return ibase_fetch_object($resultset);
	}
	
	public function getSeqNext($sequenceId){
		return ibase_gen_id($sequenceId);
	}
	
	public function createBlob($data) {
		$blh = ibase_blob_create($this->connection);
		ibase_blob_add($blh, $data);
		$blobid = ibase_blob_close($blh);
		return $blobid;
	}
	
}

?>
