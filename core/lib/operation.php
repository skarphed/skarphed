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
		
		
		private $queue = array();
		
		private $currentParent = null;
		
		
		public function addOperation($operation){
			if (!in_array(Operation,class_parents($operation))){
				throw new OperationException("Add Operation: Only Operations can be added to A Queue");
			}
			array_unshift($this->queue,$operation);
		}
		
		public function restoreOperation($set){
			$classname = $set['OPE_TYPE'];
			$operationObject = new $classname();
			
			$core = Core::getInstance();
			$db = $core->getDB();
			$stmnt = "SELECT OPD_KEY, OPD_VALUE FROM OPERATIONDATA WHERE OPD_OPE_ID = ? ;";
			$res = $db->query($core, $stmnt, array($set['OPE_ID']));
			while($set = $db->fetchArray($res)){
				$operationObject->setValue($set['OPD_KEY'], $set['OPD_VALUE']);
			}
			return $operationObject;
		}
		
		public function processNext(){
			$core = Core::getInstance();
			$db = $core->getDB();
			if (file_exists("/tmp/scv_operating.lck")){
				return;
			}
			touch("/tmp/scv_operating.lck");
			if ($this->currentParent == null){
				$stmnt_lock = "UPDATE OPERATIONS SET OPE_ACTIVE = 1 
								WHERE OPE_ID IN (SELECT FIRST 1 OPE_ID WHERE OPE_OPE_PARENT IS NULL ORDER BY OPE_INVOKED);";
				$stmnt = "SELECT FIRST 1 OPE_ID, OPE_TYPE WHERE OPE_OPE_PARENT IS NULL ORDER BY OPE_INVOKED ;";
				$db->query($core,$stmnt_lock);
				$res = $db->query($core,$stmnt);
				if ($set = $db->fetchArray($res)){
					$this->currentParent = $set['OPE_ID'];
					$operation = $this->restoreOperation($set);
					$operation->doWorkload();
				}else{
					return false;
				}
			}else{
				$stmnt_lock = "UPDATE OPERATIONS SET OPE_ACTIVE = 1 
								WHERE OPE_ID IN (SELECT FIRST 1 OPE_ID WHERE OPE_OPE_PARENT = ? ORDER BY OPE_INVOKED);";
				$stmnt = "SELECT FIRST 1 OPE_ID, OPE_TYPE WHERE OPE_OPE_PARENT = ? ORDER BY OPE_INVOKED ;";
				$res = $db->query($core,$stmnt_lock,array($this->currentParent));
				$res = $db->query($core,$stmnt,array($this->currentParent));
				if ($set = $db->fetchArray($res)){
					$operation = $this->restoreOperation($set);
					$operation->doWorkload();
				}else{
					$this->currentParent = null;
					return true;
				}
			}
			if (!unlink("/tmp/scv_operating.lck")){
				throw new OperationException("Processing: Could not remove Lock");
			}
		}
		
		public function doQueue(){
			while($this->processNext()){
				error_log("PROCESSED OPERATION");
			}
		}
	}
	
	abstract class Operation{
		private $_id = null;
		private $_parent = null;
		protected $_values = array();
		
		public function __const($parentId = null){
			$this->_parent = $parentId;
		}
		
		public function getValue($key){
			if (!isset($this->_values[$key])){
				throw new OperationException("GetValue: This value is not set!");
			}
			return $this->_values[$key];
		}
		
		public function setValue($key,$value){
			$core = Core::getInstance();
			
			foreach ($this->_values as $k=>$v){
				$core->debugGrindlog("[$k]$v");
			}
			if (!isset($this->_values[$key])){
				throw new OperationException("SetValue: This value is not set!");
			}
			
			$this->_values[$key] = $value;
		}
		
		public function setParent($parentId){
			$this->_parent = $parentId;
		}
		
		public function getParent(){
			return $this->_parent;
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
			
			$objectdata = get_object_vars($object);
			
			$stmnt = "UPDATE OR INSERT INTO OPERATIONDATA (OPD_OPE_ID, OPD_KEY, OPD_VALUE)
					  VALUES ( ?, ?, ?) MATCHING(OPD_OPE_ID,OPD_KEY);";
		    foreach ($objectdata as $key=>$value){
		    	if (strstr($key,"_")!==1){
		    		$db->query($core,$stmnt,array($this->_id,$key,$value));
		    	}
			}
		} 
		
		abstract public function doWorkload();
	}
	
	abstract class ModuleOperation extends Operation {
		public function __const (){
			$this->_values = array("name"=>null,
									"hrname"=>null,
									"version_major"=>null,
									"version_minor"=>null,
									"revision"=>null,
									"md5"=>null);
		}
		
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
			
			$stmnt = "SELECT OPE_ID, OPE_TYPE FROM OPERATIONS WHERE OPE_TYPE = 'ModuleInstallOperation' or OPE_TYPE = 'ModuleUninstallOperation';";
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
	
	class ModuleUninstallOperation extends Operation {
		public function doWorkload(){
			$core = Core::getInstance();
			$moduleM = $core->getModuleManager();
			$moduleM->uninstallModule($this->getValue("name"));
		}
		
		public function optimizeQueue(){
			
		}	
	}
?>