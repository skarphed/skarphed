<?php
	namespace scv;

	include_once("core.php");
	
	class OperationException extends \Exception{}
	
	class OperationManager extends Singleton {
		private static $instance = null;
	
		public static function getInstance(){
			if (OperationManager::$instance==null){
				OperationManager::$instance = new OperationManager();
				OperationManager::$instance->init();
			}
			return OperationManager::$instance;
		}
		
		protected function init(){}

		private $currentParent = null;
		
		public function dropOperation($operationId){
			$core = Core::getInstance();
			$db = $core->getDB();
			
			$stmnt = "SELECT OPE_ID FROM OPERATIONS WHERE OPE_OPE_PARENT = ? AND OPE_STATUS IN (0, 2) ;";
			$res = $db->query($core,$stmnt,array($operationId));
			while($set = $db->fetchArray($res)){
				$this->dropOperation($set['OPE_ID']);
			}
			$stmnt_del = "DELETE FROM OPERATIONS WHERE OPE_ID = ? AND OPE_STATUS IN (0, 2) ;";
			$db->query($core,$stmnt_del,array($operationId));
			return;
		}
		
		public function retryOperation($operationId){
			$core = Core::getInstance();
			$db = $core->getDB();
			
			$stmnt = "SELECT OPE_ID FROM OPERATIONS WHERE OPE_OPE_PARENT = ? AND OPE_STATUS = 2 ;";
			$res = $db->query($core,$stmnt,array($operationId));
			while($set = $db->fetchArray($res)){
				$this->retryOperation($set['OPE_ID']);
			}
			$stmnt_retry = "UPDATE OPERATIONS SET OPE_STATUS = 0 WHERE OPE_ID = ? AND OPE_STATUS = 2 ;";
			$db->query($core,$stmnt_retry,array($operationId));
			return;
		} 
		
		public function cancelOperation($operationId){
			$core = Core::getInstance();
			$db = $core->getDB();
			
			$stmnt = "SELECT OPE_ID FROM OPERATIONS WHERE OPE_OPE_PARENT = ? AND OPE_STATUS = 0 ;";
			$res = $db->query($core,$stmnt,array($operationId));
			while($set = $db->fetchArray($res)){
				$this->dropOperation($set['OPE_ID']);
			}
			$stmnt_del = "DELETE FROM OPERATIONS WHERE OPE_ID = ? AND OPE_STATUS = 0 ;";
			$db->query($core,$stmnt_del,array($operationId));
			return;
		}
		
		public function getOperations(){
			
		}
		
		public function restoreOperation($set){
			$classname = $set['OPE_TYPE'];
			$operationObject = new $classname();
			$operationObject->setId($set['OPE_ID']);
			
			$core = Core::getInstance();
			$db = $core->getDB();
			$stmnt = "SELECT OPD_KEY, OPD_VALUE, OPD_TYPE FROM OPERATIONDATA WHERE OPD_OPE_ID = ? ;";
			$res = $db->query($core, $stmnt, array($set['OPE_ID']));
			while($set = $db->fetchArray($res)){
				$val = $set['OPD_VALUE'];
				settype($val,$set['OPD_TYPE']);
				$operationObject->setValue($set['OPD_KEY'], $val);
			}
			return $operationObject;
		}
		
		public function processChildren($operation){
			$core = Core::getInstance();
			$db = $core->getDB();
			
			$stmnt = "SELECT OPE_ID, OPE_TYPE FROM OPERATIONS WHERE OPE_OPE_PARENT = ? ORDER BY OPE_INVOKED ;";
			$stmnt_lock = "UPDATE OPERATIONS SET OPE_STATUS = 1 WHERE OPE_ID = ? ;";
			$res = $db->query($core,$stmnt,array($operation->getId()));
			while($set = $db->fetchArray($res)){
				$childOperation = $this->restoreOperation($set);
				$db->query($core,$stmnt_lock,array($childOperation->getId()));
				try{
					$this->processChildren($childOperation);
					$childOperation->doWorkload();
				}catch(\Exception $e){
					$stmnt_err = "UPDATE OPERATIONS SET OPE_STATUS = 2 WHERE OPE_ID = ? ;";
					$db->query($core,$stmnt_err,array((int)$set['OPE_ID']));
					$core->debugGrindlog("While Operation: ".$e->getMessage());
					throw $e;
				}
				$delstmnt = "DELETE FROM OPERATIONS WHERE OPE_ID = ?;";
				$db->query($core,$delstmnt,array($childOperation->getId()));
			}
		}
		
		public function processNext(){
			$core = Core::getInstance();
			$db = $core->getDB();
			if (file_exists("/tmp/scv_operating.lck")){
				return;
			}
			touch("/tmp/scv_operating.lck");
			$stmnt_lock = "UPDATE OPERATIONS SET OPE_STATUS = 1 
							WHERE OPE_ID IN (
							  SELECT OPE_ID FROM OPERATIONS 
							  WHERE OPE_OPE_PARENT IS NULL AND OPE_STATUS = 0
							  AND OPE_INVOKED = (
							    SELECT MIN(OPE_INVOKED) FROM OPERATIONS 
							    WHERE OPE_OPE_PARENT IS NULL AND OPE_STATUS = 0)
							);";
			$stmnt = "SELECT OPE_ID, OPE_TYPE FROM OPERATIONS WHERE OPE_OPE_PARENT IS NULL AND OPE_STATUS = 1;";
			$db->query($core,$stmnt_lock);
			$db->commit();
			$res = $db->query($core,$stmnt);
			if ($set = $db->fetchArray($res)){
				$operation = $this->restoreOperation($set);
				try{
					$this->processChildren($operation);
					$operation->doWorkload();
				}catch (\Exception $e){
					$stmnt_err = "UPDATE OPERATIONS SET OPE_STATUS = 2 WHERE OPE_ID = ? ;";
					$db->query($core,$stmnt_err,array($operation->getId()));
					$core->debugGrindlog("While Operation: ".$e->getMessage());
				}
				$ret = true;
			}else{
				$ret = false;
			}
			$delstmnt = "DELETE FROM OPERATIONS WHERE OPE_STATUS = 1;";
			$db->query($core,$delstmnt);
			$db->commit();
			if (!unlink("/tmp/scv_operating.lck")){
				throw new OperationException("Processing: Could not remove Lock");
			}
			return $ret;
		}

		public function getCurrentOperationsForGUI($operationTypes=null){
			$mapping = function($name){return "scv\\".$name;};
			$core = Core::getInstance();
			$opM = $core->getOperationManager();
			$db = $core->getDB();
			
			if (isset($operationTypes) and is_array($operationTypes)){
				$operationTypes = array_map($mapping,$operationTypes);
				$core->debugGrindlog(json_encode($operationTypes));
				$stmnt = "SELECT OPE_ID, OPE_OPE_PARENT, OPE_INVOKED, OPE_TYPE, OPE_STATUS FROM OPERATIONS WHERE OPE_TYPE IN (?) ORDER BY OPE_INVOKED;";
				$res = $db->query($core,$stmnt,array($operationTypes));
			}else{
				$stmnt = "SELECT OPE_ID, OPE_OPE_PARENT, OPE_INVOKED, OPE_TYPE, OPE_STATUS FROM OPERATIONS ORDER BY OPE_INVOKED;";
				$res = $db->query($core,$stmnt);
			}
			$ret = array();
			while($set = $db->fetchArray($res)){
				$operation = $this->restoreOperation($set);
				$customValues = $operation->getValues();
				$valuesToSend = array();
				foreach ($customValues as $key=>$value){
					$valuesToSend[htmlentities($key)] = htmlentities($value);
				}
				
				$ret[$set['OPE_ID']] = array("id"=>$set['OPE_ID'],
							   "parent"=>$set['OPE_OPE_PARENT'],
							   "invoked"=>date("Y-m-d H:i:s",$set['OPE_INVOKED']),
							   "type"=>str_replace("scv\\","",$set['OPE_TYPE']),
							   "status"=>$set['OPE_STATUS'],
							   "data"=>$valuesToSend);
			}
			return $ret;
		}
	}
	
	abstract class Operation{
		private $_id = null;
		private $_parent = null;
		protected $_values = array();
		
		const STATUS_PENDING = 0;
		const STATUS_ACTIVE = 1;
		const STATUS_FAILED = 2;
		
		private static $validStorageTypes = array('integer','boolean','string'); 
		
		public function __const($parentId = null){
			$this->_parent = $parentId;
		}
		
		public function getValue($key){
			if (!isset($this->_values[$key])){
				throw new OperationException("GetValue: This value is not set $key!");
			}
			return $this->_values[$key];
		}
		
		public function getValues(){
			return $this->_values;
		}
		
		public function setValue($key,$value){
			if (!isset($this->_values[$key])){
				throw new OperationException("SetValue: This value is not set $key!");
			}
			
			$this->_values[$key] = $value;
		}
		
		public function setParent($parentId){
			$this->_parent = $parentId;
		}
		
		public function getParent(){
			return $this->_parent;
		}
		
		public function setDBID(){
			$core = Core::getInstance();
			$db = $core->getDB();
			if($this->_id == null){
				$this->_id = $db->getSeqNext('OPE_GEN');
			}
			return $this->_id;
		}
		
		public function setId($id){
			$this->_id = $id;
		}
		
		public function getId(){
			return $this->_id;
		}
		
		public function store(){
			$core  = Core::getInstance();
			$db = $core->getDB();
			
			if($this->_id == null){
				$this->_id = $db->getSeqNext('OPE_GEN');
			}
			$stmnt = "UPDATE OR INSERT INTO OPERATIONS (OPE_ID, OPE_OPE_PARENT, OPE_INVOKED, OPE_TYPE) 
			          VALUES (?,?,CURRENT_TIMESTAMP,?) MATCHING (OPE_ID);";
		    $db->query($core,$stmnt,array($this->_id, $this->_parent, get_class($this)));
			
			$stmnt = "UPDATE OR INSERT INTO OPERATIONDATA (OPD_OPE_ID, OPD_KEY, OPD_VALUE, OPD_TYPE)
					  VALUES ( ?, ?, ?, ?) MATCHING(OPD_OPE_ID,OPD_KEY);";
		    foreach ($this->_values as $key=>$value){
		    	$type = gettype($value);
		    	if (!in_array($type,Operation::$validStorageTypes)){
		    		continue;
		    	}
		    	$db->query($core,$stmnt,array($this->_id,$key,$value,gettype($value)));
			}
		} 
		
		abstract public function doWorkload();
	}
	
	abstract class ModuleOperation extends Operation {
		protected $_values = array("name"=>"",
									"hrname"=>"",
									"version_major"=>"",
									"version_minor"=>"",
									"revision"=>"",
									"md5"=>"");
		
		public function setValuesFromMeta($module){
			$this->setValue("name", $module["name"]);
			$this->setValue("hrname", $module["hrname"]);
			$this->setValue("version_major", $module["version_major"]);
			$this->setValue("version_minor", $module["version_minor"]);
			$this->setValue("revision", $module["revision"]);
			$this->setValue("md5", $module["md5"]);
			return;
		}
		
		public function getMeta(){
			return $this->_values;
		}
		
		public static function getCurrentlyProcessedModules(){
			$core = Core::getInstance();
			$opM = $core->getOperationManager();
			$db = $core->getDB();
			
			$stmnt = "SELECT OPE_ID, OPE_OPE_PARENT, OPE_TYPE FROM OPERATIONS WHERE OPE_TYPE = 'scv\ModuleInstallOperation' or OPE_TYPE = 'scv\ModuleUninstallOperation';";
			$res = $db->query($core,$stmnt);
			$ret = array();
			while($set = $db->fetchArray($res)){
				$ret[] = $opM->restoreOperation($set)->getMeta();
			}
			return $ret;
		}
		
		abstract public function optimizeQueue();
	}
	
	class ModuleInstallOperation extends ModuleOperation {
		public function doWorkload(){
			$core = Core::getInstance();
			$moduleM = $core->getModuleManager();
			$repositories = $moduleM->getRepositories();
			$repositories[0]->downloadModule($this->getMeta());
			$moduleM->installModule($this->getValue("name"));
		}
		
		public function optimizeQueue(){
			
		}	
	}
	
	class ModuleUninstallOperation extends ModuleOperation {
		public function doWorkload(){
			$core = Core::getInstance();
			$moduleM = $core->getModuleManager();
			$moduleM->uninstallModule($this->getValue("name"));
		}
		
		public function optimizeQueue(){
			
		}	
	}
	
	class FailOperation extends Operation{
		public $_values = array("val"=>10,"st"=>"test","bl"=>false);
  		public function doWorkload(){
  			$core = Core::getInstance();
			$core->debugGrindlog("IN WORKLOAD");
  			throw new \Exception("I failed so fuckin hard!");
  			
  			
  		}
	}
	
	class TestOperation extends Operation{
		public $_values = array("val"=>10,"st"=>"test","bl"=>false);
		public function doWorkload(){
			echo("ID:  ".(string)$this->getValue("val")."\n");
		}
	}
	
	
	
?>