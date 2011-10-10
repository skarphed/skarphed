<?php

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
	
}

?>