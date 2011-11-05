<?php
namespace scv;

abstract class Singleton {
	abstract public static function getInstance();

	abstract protected function init();
}

include_once 'configuration.php';
include_once 'database.php';
include_once 'module.php';
include_once 'htmlparser.php';
include_once 'rightmanagement.php';
include_once 'user.php';
include_once 'css.php';

session_start();

class Core extends Singleton implements IModule{
	private static $instance = null;
	
	public static function getInstance(){
		if (Core::$instance==null){
			Core::$instance = new Core();
			Core::$instance->init();
		}
		return Core::$instance;
	}
	
	private $config = null;
	private $database = null;
	private $htmlparser = null;
	private $rights = null;
	private $users = null;
	private $css = null;
	
	public function getName(){
		return 'de.masterprogs.scoville.core';
	}
	
	protected function init(){
		$this->debugGrindlog("====== New Session! Time: ".time());
		$this->config = new Config();
		$this->database = new Database();
		$this->config->initFromDb($this->database);
		$this->rights = RightsManager::getInstance();
		$this->modules = ModuleManager::getInstance();
		$this->users = UserManager::getInstance();
		$this->css = CssManager::getInstance();
	}
	
	public function getDB(){
		return $this->database;
	}
	
	public function getConfig(){
		return $this->config;
	}
	
	public function getRightsManager(){
		return $this->rights;
	}
	
	public function getModuleManager(){
		return $this->modules;
	}
	
	public function getUserManager(){
		return $this->users;
	}
	
	public function getCssManager(){
		return $this->css;
	}
	
	public function renderModule($modulename, $moduleInstanceId){
		$module = new Module($modulename);
		return $module->render($moduleInstanceId);
	}
	
	public function getHtmlParser() {
	  if($this->htmlparser == null) {
	    $this->htmlparser = new HtmlParser();
	  }
	  return $this->htmlparser;
	}
	
	public function renderHTML($moduleInstanceId){
		return false;
	}
	public function renderJavascript($moduleInstanceId){
		return false;
	}
	
	//EIGENER LOG FUER DEBUGGING
	public function debugGrindlog($message){
		system("echo '".escapeshellarg($message)."' >> /tmp/Grindlog.log");
	}
	
	public function parseArrayToObject($array) {
	    $object = new \stdClass();
	    if (is_array($array) && count($array) > 0) {
	        foreach ($array as $name=>$value) {
	            $name = strtolower(trim($name));
	            if (!empty($name)) {
	                $object->$name = $value;
	            }
	        }
	    }
	    return $object;
	}
	
	public function parseObjectToArray($object) {
	    $array = array();
	    if (is_object($object)) {
	        $array = get_object_vars($object);
	    }
	    return $array;
	}
	
	private function getLockTypeId($locktype){
		$db = $this->getDB();
		if (!is_string($locktype)){
			throw new LockException("Must get String as parameter!");
		}
		$stmnt = "SELECT LKT_ID FROM LOCKTYPES WHERE LKT_TYPE = ?; ";
		$res = $db->query($this,$stmnt,array($locktype));
		if($set = $db->fetchArray($res)){
			return $res['LKT_ID'];
		}else{
			throw new LockException("Locktype does not exist");
		}
	}
	
	private function checkLockType($locktype){
		$db = $this->getDB();
		if (is_string($locktype)){
			$stmnt = "SELECT LKT_ID FROM LOCKTYPES WHERE LKT_TYPE = ?; ";
			$res = $db->query($this,$stmnt,array($locktype));
			if($set = $db->fetchArray($res)){
				return true;
			}else{
				return false;
			}
		}elseif (is_int($locktype)){
			$stmnt = "SELECT LKT_ID FROM LOCKTYPES WHERE LKT_ID = ?; ";
			$res = $db->query($this,$stmnt,array($locktype));
			if($set = $db->fetchArray($res)){
				return true;
			}else{
				return false;
			}
		}else{
			throw new LockException ("Invalid datatype for \$locktype");
		}
	}
	
	public function createLock($locktype, $data){
		$db = $this->getDB();
		$dataString = json_encode($data);
				
		if (is_string($locktype)){
			$stmnt = "SELECT LCK_ID FROM LOCKS INNER JOIN LOCKTYPES ON (LCK_LKT_ID = LKT_ID) WHERE LCK_DATA = ? AND LKT_TYPE = ?;";
		}elseif(is_int($locktype9)){
			$stmnt = "SELECT LCK_ID FROM LOCKS WHERE LCK_DATA = ? AND LCK_LKT_ID = ?;";
		}else{
			throw new LockException("Invalid Datatype: \$locktype must be string or int");
		}
		
		$res = $db->query($this,$stmnt,array($dataString,$locktype));
		if ($set = $db->fetchArray($res)){
			throw new LockSetException("This Lock is set!");
		}
		
		if ($this->checkLockType($locktype)){
		
			
			$lockId = $db->genSeqNext('LCK_GEN');
			$stmnt = "INSERT INTO LOCKS (LCK_ID, LCK_DATA, LCK_LKT_ID) VALUES (?,?,?); ";
			if (is_string($locktype)){
				$locktype = $this->getLockTypeId($locktype);
			}
			$db->query($this,$stmnt,array($lockId,$dataString,$locktype));
			return $lockId;
		}
			
	}
	
	public function removeLock($lockId){
		if (!is_int($lockId)){
			throw new LockException("Lock Id must be Integer!");
		}
		$db = $this->getDB();
		$stmnt = "DELETE FROM LOCKS WHERE LCK_ID = ? ;";
		$db->query($this,$stmnt, array($lockId));
	}
	
}

class LockException extends \Exception{}
class LockSetException extends LockException{}
?>