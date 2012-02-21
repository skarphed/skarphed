<?php
	namespace scv;

	include_once("core.php");
	
	class OperationException extends \Exception{}
	
	
	/**
	 * OperationManager
	 * 
	 * Contais everything necessary to Handle Operations 
	 */
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
		
		/**
		 * Drop Operation
		 * 
		 * Drops an Operation, identified by it's Operation Id and
		 * it's children recursively
		 * Drop deletes the Operations from Database
		 * 
		 * @param int $operationId The operationId of the Operation to delete
		 */
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
		
		/**
		 * Retry Operation
		 * 
		 * Resets the state of an operation and it's children recursively to 0 (PENDING)
		 * The operation is identified by a given operationId
		 * 
		 * @param int $operationId The operationId of the Operation to retry
		 */
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
		
		/**
		 * Cancel Operation
		 * 
		 * Cancels an Operation, identified by it's Operation Id and
		 * it's children recursively
		 * Cancel Deletes the Operation from Database
		 * 
		 * @param int $operationId The operationId of the Operation to cancel
		 */
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
		
		/**
		 * Restore Operation
		 * 
		 * Restore an Operationobject stored in the database by a Dataset consisting of
		 * the operation's ID and the operation's TYPE:
		 * For example:   array("OPE_ID"=>100,"OPE_TYPE"=>"scv\\TestOperation")
		 * Restores the Operationobject's $_values-property by the data saved
		 * in the DB-Table OPERATIONDATA
		 * 
		 * @param Array $set The set defining the Operationobject
		 * @return Operation an Operationobject
		 */
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
		
		/**
		 * Process Children
		 * 
		 * Recursively executes the workloads of Operation's Childoperations
		 * It hereby catches exceptions in the workloads, sets the OPE_STATUS
		 * to 2 (FAILED) if a catch occurs, then passes the exception on to the 
		 * higher layer.
		 * If an Operation succeeds, it's entry in DB gets deleted
		 * 
		 * @param Operation $operation The operation that's children shall be executed
		 */
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
		
		/**
		 * Process Next Operation in Queue
		 * 
		 * Sets the status of the next toplevel operation to 1 (ACTIVE)
		 * Fetches the next toplevel-operation from the database, applies a FILESYSTEMLOCK!
		 * Which is /tmp/scv_operating.lck !!! . 
		 * 
		 * @return bool True if done, False if no more Operations are available in Queue
		 */
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
		
		/**
		 * Return Current Operations For Gui
		 * 
		 * Returns all Operations in an associative array.
		 * The array's indices are the operationIDs
		 * The Objects contain all information about the operations,
		 * including the Data
		 * 
		 * @param Array $operationTypes=null If set, limits the selected operations to that type.
		 * @return Array A list of Operation-Representations
		 */
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
							   //"invoked"=>date("Y-m-d H:i:s",$set['OPE_INVOKED']),
							   "invoked"=>$set['OPE_INVOKED'],
							   "type"=>str_replace("scv\\","",$set['OPE_TYPE']),
							   "status"=>$set['OPE_STATUS'],
							   "data"=>$valuesToSend);
			}
			return $ret;
		}
	}
	
	/**
	 * Operation
	 * 
	 * Abstract BaseClass for any Operation in the Queue
	 */
	abstract class Operation{
		private $_id = null;
		private $_parent = null;
		protected $_values = array();
		
		const STATUS_PENDING = 0;
		const STATUS_ACTIVE = 1;
		const STATUS_FAILED = 2;
		
		/**
		 * Valid types for $_values
		 * 
		 * Defines every type that is legal for user defined values in $_values
		 */
		private static $validStorageTypes = array('integer','boolean','string'); 
		
		public function __const($parentId = null){
			$this->_parent = $parentId;
		}
		
		/**
		 * Get a Userdefined Value
		 * 
		 * Returns a Value that is defined in $_values
		 * Only classes that inherit Operation can define those values,
		 * so make sure you look in the inherited class, that $key exists in _values
		 * 
		 * Throws a OperationException if the value does not exist.
		 * 
		 * @param string $key The key of the user-defined value
		 * @return ? The user-defined value 
		 */
		public function getValue($key){
			if (!isset($this->_values[$key])){
				throw new OperationException("GetValue: This value is not set $key!");
			}
			return $this->_values[$key];
		}
		
		/**
		 * Get all Values
		 * 
		 * Returns _values. It returns all userdefined values of this 
		 * inheritant of Operation.
		 * 
		 * @return Array The user-defined Values
		 */
		public function getValues(){
			return $this->_values;
		}
		
		/**
		 * Set a user-defined value
		 * 
		 * Sets a user defined value. Look into the $_value declaration of the 
		 * inheriting class to see which values are legitimate
		 * 
		 * Throws a OperationException if the value does not exist.
		 * 
		 * @param string $key The key of the user-defined value
		 * @param ? $value The value to set
		 */
		public function setValue($key,$value){
			if (!isset($this->_values[$key])){
				throw new OperationException("SetValue: This value is not set $key!");
			}
			
			$this->_values[$key] = $value;
		}
		
		/**
		 * Set Parent
		 * 
		 * Sets the parent attribute. It is the id of the Operation that
		 * acts as Parent to this Operation
		 * 
		 * @param int $parentId The id of the parent Operation
		 */
		public function setParent($parentId){
			$this->_parent = $parentId;
		}
		
		/**
		 * Get Parent
		 * 
		 * Returns the id of this Operation's parent Operation
		 * 
		 * @return int The parent Operation's Id
		 */
		public function getParent(){
			return $this->_parent;
		}
		
		/**
		 * Set Database Id
		 * 
		 * Get a new Operation Id from the Database and assign it to this
		 * Operation if this Operation's id is null. Afterwards return the 
		 * new Id
		 * 
		 * @return int The Id that has been assigned to this Operation 
		 */
		public function setDBID(){
			$core = Core::getInstance();
			$db = $core->getDB();
			if($this->_id == null){
				$this->_id = $db->getSeqNext('OPE_GEN');
			}
			return $this->_id;
		}
		
		/**
		 * Set Id
		 * 
		 * Set an Id to this Operation (should only used when restoring an Operation)
		 * 
		 * @param int $id The OperationId to set
		 */
		public function setId($id){
			$this->_id = $id;
		}
		
		/**
		 * Get ID
		 * 
		 * Return the Operation Id of this Operation
		 * 
		 * @return int The OperationId
		 */
		public function getId(){
			return $this->_id;
		}
		
		/**
		 * Store to Database
		 * 
		 * Stores this Operation to database.
		 * Also saves every user defined value in $_values as 
		 * long as it is a valid type 
		 */
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
		
		/**
		 * The Workload 
		 * 
		 * This method must be overridden by inheriting classes.
		 * The code inside this method will be executed when the
		 * Operation is processed by OperationManager::processNext or 
		 * OperationManager::processChild 
		 */
		abstract public function doWorkload();
	}
	
	/**
	 * Abstract BaseClass for Module-Concerning Operations
	 */
	abstract class ModuleOperation extends Operation {
		protected $_values = array("name"=>"",
									"hrname"=>"",
									"version_major"=>"",
									"version_minor"=>"",
									"revision"=>"",
									"md5"=>"");
		
		/**
		 * Set Values from Metadata
		 * 
		 * Sets this ModuleOperation's values from Module-metadata
		 * 
		 * @param Array $module The module Metadata
		 */
		public function setValuesFromMeta($module){
			$this->setValue("name", $module["name"]);
			$this->setValue("hrname", $module["hrname"]);
			$this->setValue("version_major", $module["version_major"]);
			$this->setValue("version_minor", $module["version_minor"]);
			$this->setValue("revision", $module["revision"]);
			$this->setValue("md5", $module["md5"]);
			return;
		}
		
		
		/**
		 * Get Metadata
		 * 
		 * Returns this ModuleOperations Metadata
		 * 
		 * @deprecated Use Operation::getValues() instead
		 * @return Array The Metadata
		 */
		public function getMeta(){
			return $this->_values;
		}
		
		/**
		 * Get currently processed Modules
		 * 
		 * Returns an Array of ModuleOperation-Objects that are
		 * currently listedin the queue 
		 * 
		 * @return Array an array of ModuleOperation-Objects
		 */
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
		
		/**
		 * Optimize the Queue for this module
		 */
		abstract public function optimizeQueue();
	}
	
	/**
	 * Operation for the Task of installing a Module
	 */
	class ModuleInstallOperation extends ModuleOperation {
		/**
		 * The Workload
		 * 
		 * Installs a Module defined in the user-defined values
		 */
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
	
	/**
	 * Operation for the Task of uninstalling a Module
	 */
	class ModuleUninstallOperation extends ModuleOperation {
		/**
		 * The Workload
		 * 
		 * Uninstalls a Module defined in the user-defined values
		 */
		public function doWorkload(){
			$core = Core::getInstance();
			$moduleM = $core->getModuleManager();
			$moduleM->uninstallModule($this->getValue("name"));
		}
		
		public function optimizeQueue(){
			
		}	
	}
	
	/**
	 * Always Failing Operation
	 *
	 * Operation used for TestCases
	 */
	class FailOperation extends Operation{
		public $_values = array("val"=>10,"st"=>"test","bl"=>false);
		
		/**
		 * The workload
		 * 
		 * Throw an exception
		 */
  		public function doWorkload(){
  			$core = Core::getInstance();
			$core->debugGrindlog("IN WORKLOAD");
  			throw new \Exception("I failed so fuckin hard!");
  			
  			
  		}
	}
	
	/**
	 * Always succeeding Operation
	 *
	 * Operation used for TestCases
	 */
	class TestOperation extends Operation{
		public $_values = array("val"=>10,"st"=>"test","bl"=>false);
		
		/**
		 * The workload
		 * 
		 * Do nothing
		 */
		public function doWorkload(){
			$core = Core::getInstance();
			throw new \Exception("I failed so fuckin hard!");
			$core->debugGrindlog("ID:  ".(string)$this->getValue("val")."\n");
		}
	}
	
	
	
?>