<?php
namespace scv;

include_once 'core.php';

class DatabaseException extends \Exception {}

class Database {
	private $connection = null;
	
	private $ip = null;
	private $dbname = null;
	private $user = null;
	private $password = null;
	
	private $queryCache = array();
	private $queryRating = array();
	
	public function __construct(){
		$config = Core::getInstance()->getConfig();
		assert($config->getConfigState() == Config::CONF_LOAD_LOCAL);
		$this->setIp($config->getEntry('db.ip'));
		$this->setDbName($config->getEntry('db.name'));
		$this->setUser($config->getEntry('db.user'));
		$this->setPassword($config->getEntry('db.password'));
		$this->connect();
	}
	
	public function setIp ($ip){
		if (preg_match("/\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/",$ip)){
			$this->ip = $ip;
		}else{
			throw new DatabaseException('IP is not valid: '.$ip);
		}
	}
	
	public function setDbName ($dbname){
	    $this->dbname = $dbname;	
	}
	
	public function setUser ($user){
		$this->user = $user;
	}
	
	public function setPassword($pw){
		$this->password = $pw; 
	}
	
	public function createBlob($data) {
		$blh = ibase_blob_create($this->connection);
		ibase_blob_add($blh, $data);
		$blobid = ibase_blob_close($blh);
		return $blobid;
	}
	
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
	
	private function getLowestUseQuery(){
		$firstloop = true;
		$lowest = null;
		$lstatement  = null;
		foreach ($this->queryRating as $statement => $rating){
			if ($firstloop){
				$lowest = $rating;
				$lstatement = $statement;
			}else{
				if($rating < $lowest){
					$lowest = $rating;
					$lstatement = $statement;
				}
			}
		}
		return $lstatement;
	}
	
	//HERE BE DRAGONS
	//TODO: Bessere loesung finden
	private function generateZeros($nr){
		$return = "";
		while($nr--!=0){
			$return.="0";
		}
		return $return;
	}
	
	private function replaceModuleTables($module, $statement){
        //Vorhandene Tabellennamen bestimmen und aus der Datenbank holen
		$tagpattern = "/\$\{[A-Za-z}]{1,}\}/g";
		$matches = null;
		$tablenames = array();
		preg_match_all($tagpattern,$statement,$matches);
		$matches = array_unique($matches);
		foreach($matches as $match){
			$tablename = substr($match,2,strlen($match)-3); 
			$tablenames[] = $tablename;
		}
		
		//TODO: Verhalten implementieren, wenn Tabellen von anderen Modulen mit angesprochen werden.
		$tableqry = "SELECT MDT_ID, MDT_NAME 
		             FROM MODULETABLES 
		              INNER JOIN MODULE ON (MDT_MOD_ID = MOD_ID )
		             WHERE MOD_NAME = ? 
		              AND MDT_NAME IN (?) ;";
        $prepared = ibase_prepare($tableqry);
		$cursor = ibase_execute($prepared,array($module->getName(),"'".join("','",$tablenames)."'"));
		
		//Tabellennamen ersetzen
		$replacementsDone = array();
		while($nameset = ibase_fetch_object($cursor)){
			$pattern = "/\$\{".$nameset->MDT_NAME."\}/g";
			$tableId = (string)$nameset->MDT_ID;
			$tableId = "TAB_".$this->generateZeros(6-strlen($tableId)).$tableId; // Entfernen von ${}
			preg_replace($pattern, $tableId, $statement);
			$replacementsDone[] = $nameset->MDT_NAME;
		}
		
		//Errorhandling falls Replacement nicht geklappt hat
		if (count($replacementsDone) != count($matches)){
			$errorResult = array();
			foreach($matches as $match){
				if (!in_array($match,$replacementsDone)){
					$errorResult[]=$match;
				}
			}
			throw new DatabaseException('Could not resolve Tablenames for: '.join(",",$errorResult));
		}
		return $statement;
	}
	
	private function createQueryInCache($statement){
		if (count($this->queryCache)>20){
			$oldstmnt = $this->getLowestUseQuery();
			unset($this->queryCache[$oldstmnt]);
			unset($this->queryRating[$oldstmnt]);
		}
		$this->queryCache[$statement] = ibase_prepare($statement);
		$this->queryRating[$statement] = 0;
		return $this->queryCache[$statement];
	}
	
	public function query($module, $statement, $args=array(), $forceNoCache=false){
		if(!$this->connection){
			throw new DatabaseException('Database is not Connected');
		}
		if ($module->getName() != 'de.masterprogs.scoville.core'){
		  $statement = $this->replaceModuleTables($module, $statement);	
		}
		if (isset($this->queryCache[$statement])){
			$query = $this->queryCache[$statement];
			$this->queryRating[$statement]++;
		}else{
			$query = $this->createQueryInCache($statement);
		}
		
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
	
	public function commit(){
		ibase_commit();
	}
	
	/**
	 * This function creates the tables necessary to run a module
	 * by interpreting the objectlist $table
	 */
	
	public function createTableForModule($tables, $modId){
		//TODO: Implement Sequence
		foreach ($tables as $table){
			$newTableId = $this->getSeqNext("MDT_GEN"); // Generiere TabellenId
			$newTableString = $this->generateZeros(6-strlen((string)$newTableId)).(string)$newTableId; //Mache string im stile '001234'
			$statement = "CREATE TABLE TAB_$newTableString ( MOD_INSTANCE_ID INT ";
			$first = false;
			foreach($table->columns as $column){				
				$statement.=", $column->name $column->type ";
			}
			$statement.=");";
			$updateModuleTables = ibase_prepare("INSERT INTO MODULETABLES (MDT_ID, MDT_NAME, MDT_MOD_ID ) VALUES ( ?, ?, ?);");
			ibase_execute($updateModuleTables, $newTableId, $table->name, $modId);
			ibase_query($statement);
		}
	}
	
	/**
	 * This function removes tables for a specific module
	 */
	
	
	public function removeTableForModule($tables, $modId){
		$gettableIds = "SELECT MDT_ID 
						FROM MODULETABLES 
						WHERE MDT_MOD_ID = ? ;";
	    $prepared = ibase_prepare($gettableIds);
		$cursor = ibase_execute($prepared, $modId);
		while($tableset = ibase_fetch_object($cursor)){
			$tabId = "TAB_".$this->generateZeros(6-strlen((string)$tableset->MDT_ID)).(string)$tableset->MDT_ID;
			$deletestmnt = "DROP TABLE $tabId ;";
			ibase_query($deletestmnt);
		}
		return;
	}

	/**
	 * Gets next value for sequence specified by $sequenceId
	 */
	
	public function getSeqNext($sequenceId){
		return ibase_gen_id($sequenceId);
	}
	
	/**
	 * Gets current value for sequence specified by $sequenceId
	 * 
	 * FIX BLUB
	 */
	
	public function getSeqCurrent($sequenceId){
		//TODO: Here Be Dragons! Absichern von sequenceId!!!
		$statement = "SELECT GEN_ID ( $sequenceId , 0) FROM DUAL;";		
		$cursor = ibase_query($statement);
		$row = ibase_fetch_row($cursor);
		return $row[0];
	}
		
	//DEBUG: Method for database-configurationinfo
	public function getInfo(){
		echo("<br>"."Name=".$this->dbname."<br>");
		echo("User=".$this->user."<br>");
		echo("Password=".$this->password."<br>");
		echo("IP=".$this->ip."<br>");
		return;
	}
	
}
?>