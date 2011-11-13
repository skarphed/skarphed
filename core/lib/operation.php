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
		
		public function restoreOperation($set){
			$classname = $set['OPE_TYPE'];
			$operationObject = new $classname();
			
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
		
		public function processNext(){
			$core = Core::getInstance();
			$db = $core->getDB();
			if (file_exists("/tmp/scv_operating.lck")){
				return;
			}
			touch("/tmp/scv_operating.lck");
			if ($this->currentParent == null){
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
					$this->currentParent = (int)$set['OPE_ID'];
					$operation = $this->restoreOperation($set);
					try{
						$operation->doWorkload();
					}catch (\Exception $e){
						$stmnt_err = "UPDATE OPERATIONS SET OPE_STATUS = 2 WHERE OPE_ID = ? ;";
						$db->query($core,$stmnt_err,array((int)$set['OPE_ID']));
						$core->debugGrindlog("While Operation: ".$e->getMessage());
					}
					
				}else{
					$delstmnt = "DELETE FROM OPERATIONS WHERE OPE_STATUS = 1;";
					$db->query($core,$delstmnt);
					$db->commit();
					if (!unlink("/tmp/scv_operating.lck")){
						throw new OperationException("Processing: Could not remove Lock");
					}
					return false;
				}
			}else{
				$stmnt_lock = "UPDATE OPERATIONS SET OPE_STATUS = 1 
								WHERE OPE_ID IN (
								  SELECT OPE_ID FROM OPERATIONS 
								  WHERE OPE_OPE_PARENT = ? AND OPE_STATUS = 0
								  AND OPE_INVOKED = (
								    SELECT MIN(OPE_INVOKED) FROM OPERATIONS 
								    WHERE OPE_OPE_PARENT = ? AND OPE_STATUS = 0)
								);";
				$stmnt = "SELECT OPE_ID, OPE_TYPE FROM OPERATIONS WHERE OPE_OPE_PARENT = ?  AND OPE_STATUS = 1;";
				$db->query($core,$stmnt_lock,array($this->currentParent, $this->currentParent));
				$db->commit();
				$res = $db->query($core,$stmnt,array($this->currentParent));
				if ($set = $db->fetchArray($res)){
					$operation = $this->restoreOperation($set);
					try{
						$operation->doWorkload();
					}catch (\Exception $e){
						$stmnt_err = "UPDATE OPERATIONS SET OPE_STATUS = 2 WHERE OPE_ID = ? ;";
						$db->query($core,$stmnt_err,array((int)$set['OPE_ID']));
						$core->debugGrindlog("While OperationChild ".$e->getMessage());
					}
					
				}else{
					$this->currentParent = null;
				}
			}
			$delstmnt = "DELETE FROM OPERATIONS WHERE OPE_STATUS = 1;";
			$db->query($core,$delstmnt);
			$db->commit();
			if (!unlink("/tmp/scv_operating.lck")){
				throw new OperationException("Processing: Could not remove Lock");;
			}
			return true;
		}
		
		public function doQueue(){
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
			if($this->_id == null){
				$this->_id = $db->getSeqNext('OPE_GEN');
			}
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
  		public function doWorkload(){
  			$core = Core::getInstance();
			$core->debugGrindlog("IN WORKLOAD");
			echo "IN WORLOAD";
  			throw new \Exception("I failed so fuckin hard!");
  			
  			
  		}
	}
	
?>