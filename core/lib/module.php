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
require_once "core.php";
require_once "Crypt/RSA.php";
class ModuleException extends Exception{}

interface IModule{
	public function getName();
	
	public function renderHTML($moduleInstanceId);
	
	public function renderJavascript($moduleInstanceId);
	
}

class Module implements IModule {
	private $name = testmodul;
	
	public function __construct($modulename){}
	
	public function renderHTML($moduleInstanceId){
		
	}
	
	public function renderJavascript($moduleInstanceId){
		
	}
	
	/**
	 * Set the widgetId
	 * 
	 * Set the id of the widget the module has to operate on
	 */
	public function setWidgetId($widgetId){
		
	}
	
	public function getName(){
		return $this->name;
	}
}

class ModuleManager extends Singleton {
	/**
	 *  This function builds the tables that are necessary
	 *  to run the Module
	 */
	
	private static $instance = null;
	
	public static function getInstance(){
		if (ModuleManager::$instance==null){
			ModuleManager::$instance = new ModuleManager();
			ModuleManager::$instance->init();
		}
		return ModuleManager::$instance;
	}
	
	protected function init(){}
	
	private function updateDatabaseTables($tables,$moduleId){
		$core = Core::getInstance();
		$core->getDB()->updateTablesForModule($tables,$moduleId);
	}
	
	private function createDatabaseTables($tables,$moduleId){
		$core =  Core::getInstance();
		$core->getDB()->createTablesForModule($tables,$moduleId);
	}
	
	private function removeDatabaseTables($tables,$moduleId){
		$core = Core::getInstance();
		$core->getDB()->removeTablesForModule($tables,$moduleId);
	}
	
	/**
	 * This function creates Rights that are necessary for
	 * the module
	 */
	
	private function createRights($manifest, $moduleId){
		$rights = $manifest->rights;
		$core = Core::getInstance();
		$rightsManager = $core->getRightsManager();
		foreach($rights as $right){
		  $rightsManager->createRight($right,$manifest->name);	
		}
		return;
	}
	
	private function updateRights($manifest, $moduleId){
		$rights = $manifest->rights;
		$core = Core::getInstance();
		$rightsManager = $core->getRightsManager();
		foreach($rights as $right){
		  try{
		  $rightsManager->createRight($right,$manifest->name);
		  } catch(Exception $e){}	
		}
		return;
	}
	
	private function removeRights($manifest, $moduleId){
		$rights = $manifest->rights;
		$core = Core::getInstance();
		$rightsManager = $core->getRightsManager();
		foreach($rights as $right){
		  $rightsManager->removeRight($right,$manifest->name);	
		}
		return;
	}
		
	
	/**
	 * registerModule registers the Module and yields a unique moduleid
	 */
	public function registerModule($manifest){
		$core =  Core::getInstance();
		$db = $core->getDB();
		$newModuleId = $db->getSeqNext("MOD_GEN");
		$statement = "INSERT INTO MODULES (MOD_ID, MOD_NAME, MOD_DISPLAYNAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV)
		              VALUES (?,?,?,?,?,?);";
		$db->query($core,$statement,array($newModuleId, $manifest->name, $manifest->hrname, $manifest->version_major,
		                                  $manifest->version_minor, $manifest->revision));
	    return $newModuleId;
	}
	
	public function unregisterModule($manifest){
		$core =  Core::getInstance();
		$db = $core->getDB();
		
		$statement = "DELETE FROM MODULES WHERE MOD_NAME = ?;";
		$db->query($core,$statement,array($manifest->name,));
	    return;
	}
	
	public function updateModule($moduleId){
		$core = Core::getInstance();
		$modulesPath = $core->getConfig()->getEntry("modules.path");
		if (!is_dir("../".$modulesPath.$moduleId)){
			throw new ModuleException("InstallationError: Can't update Module, because it is not Installed");
		}
		$core->recursiveDelete('../".$modulesPath.$moduleId');
		mkdir('../'.$modulesPath.$moduleId);
		system('tar xfz /tmp/'.escapeshellarg($moduleId).'.tar.gz -C ../'.$modulesPath.escapeshellarg($moduleId).'/ > /dev/null');
		
		$manifestRaw = file_get_contents('../'.$modulesPath.$moduleId.'/manifest.json');
		if ($manifestRaw == false){
			throw new ModuleException("InstallationError: $moduleId is not a valid Scoville Module");
			return;
		}
		
		$manifest = json_decode($manifestRaw);
		
		if ($manifest == null){
			throw new ModuleException("InstallationError: Manifest seems to be broken. Validate!");
			return;
		}
		
		$db = $core->getDB();
		$db->query("UPDATE MODULES SET MOD_VERSIONMAJOR = ?, MOD_VERSIONMINOR = ? , MOD_VERSIONREV = ? WHERE MOD_NAME = ? ;", 
					array($manifest->version_major, $manifest->version_minor, $manifest->revision));
		$res = $db->query("SELECT MOD_ID FROM MODULES WHERE MOD_NAME = ?;", 
					array($manifest->name));
		$moduleId = null;
		if ($set = $db->fetchObject($res)){
			$moduleId = $set->MOD_ID;
		}
		
		$this->updateDatabaseTables($manifest->tables, $moduleId);
		$this->updateRights($manifest->rights, $moduleId);
	}
	
	public  function installModule($moduleId){
		$core = Core::getInstance();
		$modulesPath = $core->getConfig()->getEntry("modules.path");
		if (is_dir("../".$modulesPath.$moduleId)){
			throw new ModuleException("InstallationError: This Module is already installed (Directory Exists)");
		}
		mkdir('../'.$modulesPath.$moduleId);
		system('tar xfz /tmp/'.escapeshellarg($moduleId).'.tar.gz -C ../'.$modulesPath.escapeshellarg($moduleId).'/ > /dev/null');
		
		$manifestRaw = file_get_contents('../'.$modulesPath.$moduleId.'/manifest.json');
		if ($manifestRaw == false){
			throw new ModuleException("InstallationError: $moduleId is not a valid Scoville Module");
			return;
		}
		
		$manifest = json_decode($manifestRaw);
		
		if ($manifest == null){
			throw new ModuleException("InstallationError: Manifest seems to be broken. Validate!");
			return;
		}
				
		$moduleNumber = $this->registerModule($manifest);
		$this->createDatabaseTables($manifest->tables, $moduleNumber);
		$this->createRights($manifest, $moduleNumber); //TODO: Implementiere createRights
		
		//Cleanup
		unlink('/tmp/'.$moduleId.".tar.gz");
	}
	
	public function addRepository($ip, $port, $name = '') {
		$repository = new Repository(null, $name, $ip, $port, null);
		$repository->store(); //Wird ja in dem falle auch gleich gespeichert, ziga ;)
		return $repository;
	}
	
	public function removeRepository($id) {
		
	}
	
	public function getRepository($id) {
		$core = Core::getInstance();
		$db = $core->getDB();
		$result = $db->query($core,"select rep_id, rep_name, rep_ip, rep_port, rep_lastupdate from repositories where rep_id = ?;", array($id));
		if ($row = $db->fetchArray($result)){
			$repository = new Repository($row['REP_ID'],$row['REP_NAME'],$row['REP_IP'],$row['REP_PORT'],$row['REP_LASTUPDATE']);
			return $repository;
		}else{
			throw new RepositoryException("No such Repository");
		}
	}
	
	public function getRepositories(){
		$core = Core::getInstance();
		$db = $core->getDB();
		$ret = array();
		$result = $db->query($core,"select rep_id, rep_name, rep_ip, rep_port, rep_lastupdate from repositories;");
		while($set = $db->fetchArray($result)){
			$ret[] = new Repository($set['REP_ID'],$set['REP_NAME'],$set['REP_IP'],$set['REP_PORT'],$set['REP_LASTUPDATE']);
		}
		return $ret;
	}
	
	public function updateModuleFromRepository($repository, $module){
		$core = Core::getInstance();
		
		if(!is_array($module)){
			$module = $core->parseObjectToArray($module);
		}
		$opM = $core->getOperationManager();
		
		$operation = new ModuleUpdateOperation();
		$operation->setValuesFromMeta($module);
		$operation->store();
	}
	
	public function installModuleFromRepository($repository, $module, $operationId){
		$core = Core::getInstance();
		
		if(!is_array($module)){
			$module = $core->parseObjectToArray($module);
		}
		$opM = $core->getOperationManager();
		/*$repositories = $this->getRepositories();
		$repo = $repositories[0];
		$dependencies = $repo->getDescDependencies($module);*/
		
		$operation = new ModuleInstallOperation();
		$operation->setValuesFromMeta($module);
		/*$operationId = $operation->setDBID();
		
		foreach ($dependencies as $dep){
			$dep = $core->parseObjectToArray($dep);
			$subOp = new ModuleInstallOperation();
			$subOp->setValuesFromMeta($dep);
			$subOp->setParent($operationId);
			$subOp->optimizeQueue();
			$subOp->store();
		}*/
		
		$operation->optimizeQueue();
		$operation->store();
	}
	
	
	public function uninstallModuleRemote($repository, $module, $operationId){
		$core = Core::getInstance();
		if(!is_array($module)){
			$module = $core->parseObjectToArray($module);
		}
		$opM = $core->getOperationManager();
		/*$repositories = $this->getRepositories();
		$repo = $repositories[0];
		$dependencies = $repo->getDependencies($module);*/
		
		$operation = new ModuleUninstallOperation();
		$operation->setValuesFromMeta($module);
		/*$operationId = $operation->setDBID();
		
		foreach ($dependencies as $dep){
			$dep = $core->parseObjectToArray($dep);
			$subOp = new ModuleUninstallOperation();
			$subOp->setValuesFromMeta($dep);
			$subOp->setParent($operationId);
			$subOp->optimizeQueue();
			$subOp->store();
		}*/
		
		$operation->optimizeQueue();
		$operation->store();
		
	}
	
	public function uninstallModule($moduleId){
		$core = Core::getInstance();
		$modulesPath = $core->getConfig()->getEntry("modules.path");
		if (!is_dir("../".$modulesPath.$moduleId)){
			throw new ModuleException("InstallationError: This Module is not installed (Directory Exists)");
		}
		
		//TODO: Ueberpruefen, ob modul noch irgendwo verwendet wird.
		
		$db = $core->getDB();
		
		$result = $db->query($core,"SELECT MOD_ID FROM MODULES WHERE MOD_NAME = ?;", array($moduleId));
		$row = $db->fetchArray($result);
		$moduleNumber = $row['MOD_ID'];
		 
		
		$manifestRaw = file_get_contents('../'.$modulesPath.$moduleId.'/manifest.json');
		if ($manifestRaw == false){
			throw new ModuleException("InstallationError: $moduleId is not a valid Scoville Module");
			return;
		}
		
		$manifest = json_decode($manifestRaw);
		
		if ($manifest == null){
			throw new ModuleException("InstallationError: Manifest seems to be broken. Validate!");
			return;
		}
				
		$this->removeDatabaseTables($manifest->tables, $moduleNumber);
		$this->removeRights($manifest, $moduleNumber); //TODO: Implementiere createRights
		$moduleNumber = $this->unregisterModule($manifest);
		
		//Delete module on file system
		$core->recursiveDelete('../'.$modulesPath.$moduleId);
	}
	
	public function loadModule($moduleName){
		$core = Core::getInstance();
		try{
			require_once $moduleName."/module.php";
			$moduleClass = str_replace(".","_", $moduleName);
			//eval("\$module = new $moduleClass(\$core);");
			$module = new $moduleClass($core);
			return $module;
		}catch(ModuleException $e){}
	}
	
	public function loadModuleById($moduleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT MOD_NAME FROM MODULES WHERE MOD_ID = ? ;";
		$res = $db->query($core,$stmnt,array($moduleId));
		if ($set = $db->fetchArray($res)){
			$moduleName = $set['MOD_NAME'];
		}else{
			throw new ModuleException("Load Module: Module with id $moduleId does not exist!");
		}
		try{
			require_once $moduleName."/module.php";
			$moduleClass = str_replace(".","_", $moduleName);
			//eval("\$module = new $moduleClass(\$core);");
			$module = new $moduleClass($core);
			return $module;
		}catch(ModuleException $e){}
	}
	
	/**
	 * Module Version Compare
	 * 
	 * Compares the versions of Two modules
	 * 1  -> module1  > module2
	 * 0  -> module1 == module2
	 * -1 -> module1  < module2
	 * 
	 * @param Array $module1 A Module
	 * @param Array $module2 A Module
	 * @return int The compare value
	 */
	private function versionCompare($module1, $module2){
		$core = Core::getInstance();
		if (!is_object($module1)){
			$module1 = $core->parseArrayToObject($module1);
		}
		if (!is_object($module2)){
			$module2 = $core->parseArrayToObject($module2);
		}		
		if ($module1->version_major > $module2->version_major){
			return 1;
		}elseif($module1->version_major == $module2->version_major){
			if ($module1->version_minor > $module2->version_minor){
				return 1;
			}elseif($module1->version_minor == $module2->version_minor){
				if ($module1->revision > $module2->revision){
					return 1;
				}elseif($module1->revision == $module2->revision){
					return 0;
				}else{
					return -1;
				}
			}else{
				return -1;
			}
		}else{
			return -1;
		}
	}
	
	public function updateModules(){
		/*$core = Core::getInstance();
		$db = $core->getDB();
		$modules = array();
		
		$stmnt = "SELECT MOD_ID, MOD_NAME, MOD_DISPLAYNAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_REP_ID, MOD_MD5 FROM MODULES ;";
		$res = $db->query($core,$stmnt);
		
		$repositoryJobLocks = ModuleOperation::getCurrentlyProcessedModules();
		$repositories = $this->getRepositories();
		$repository = $repositories[0];
		
		while($set = $db->fetchArray($res)){
			$modules[]=array('name'=>$set['MOD_NAME'], 'hrname'=>$set['MOD_DISPLAYNAME'], 
							 'version_major'=>$set['MOD_VERSIONMAJOR'], 'version_minor'=>$set['MOD_VERSIONMINOR'], 
							 'revision'=>$set ['MOD_VERSIONREV'], 'md5'=>$set['MOD_MD5'], 'serverModuleId'=> $set['MOD_ID']);
		}
		
		foreach ($modules as $module){
			$versions = $repository->getAllVersions($module);
			foreach ($versions as $version){
				if ($this->versionCompare($module, $version) == -1){ // if version is bigger than modulesown version
					
				}
			}
		}*/
		
		
		
		//$repositoryJobLocks = ModuleOperation::getCurrentlyProcessedModules();
		$repositories = $this->getRepositories();
		$repository = $repositories[0];
		
		$modules = $this->getModules();
		foreach ($modules as $module){
			if (isset($module['toUpdate']) and $module['toUpdate']){
				$lastestModule = $repository->getLatestVersion($module);
				$this->updateModuleFromRepository($repository, $latestModule);
			}
		}
		
		
		
	}
	
	/**
	 * Get All modules of this server
	 * 
	 * Returns module meta descriptions
	 * 
	 * @param bool $onlyInstalled Returns only currently installed Modules if True
	 * @param bool $checkRight check for permission
	 * @return Array Array of Module Metadata as specified in module specs
	 */
	public function getModules($onlyInstalled=false, $checkRight=false){		
		//TODO: Check Rights sinnvoll einbauen
		$core = Core::getInstance();
		$db = $core->getDB();
		$modules = array();
		
		$stmnt = "SELECT MOD_ID, MOD_NAME, MOD_DISPLAYNAME, MOD_VERSIONMAJOR, MOD_VERSIONMINOR, MOD_VERSIONREV, MOD_REP_ID, MOD_MD5 FROM MODULES ;";
		$res = $db->query($core,$stmnt);
		
		$repositoryJobLocks = ModuleOperation::getCurrentlyProcessedModules();
		
		while($set = $db->fetchArray($res)){
			$modules[]=array('name'=>$set['MOD_NAME'], 'hrname'=>$set['MOD_DISPLAYNAME'], 
							 'version_major'=>$set['MOD_VERSIONMAJOR'], 'version_minor'=>$set['MOD_VERSIONMINOR'], 
							 'revision'=>$set ['MOD_VERSIONREV'], 'md5'=>$set['MOD_MD5'], 'serverModuleId'=> $set['MOD_ID'], 'installed'=>true);
		}
		
		if(!$onlyInstalled){
			$repositories = $this->getRepositories();
	    	foreach ($repositories as $repository){
	    		$repoModules = $repository->getAllModules();
				foreach ($repoModules as $repoModule){
				    for ($i = 0; $i < count($modules); $i++){
						if ($repoModule->name == $modules[$i]['name']){
							if ($this->versionCompare($modules[$i], $repoModule) == -1){
								$modules[$i]['toUpdate'] = true;
							}
							foreach($repositoryJobLocks as $rjl){
								if ($rjl['name'] == $modules[$i]['name']){
									$modules[$i]['processing'] = 'Unstalling';
								}
							}
							continue 2; 
						}
					}
					foreach($repositoryJobLocks as $rjl){
						if ($rjl['name'] == $repoModule->name){
							$repoModule->processing = 'Installing';
						}
					}
					$modules[] = $core->parseObjectToArray($repoModule);
				}
	    	}
		}
		
		return $modules;
	}
	
}

class RepositoryException extends Exception {}

class Repository {
	private $id = null;
	private $name = null;
	private $ip = null;
	private $port = null;
	private $lastupdate = null;
	private $publickey = null;
	
	public function __construct($id, $name, $ip, $port, $lastupdate) {
		$this->id = (int)$id;
		$this->name = (string)$name;
		$this->ip = (string)$ip;
		$this->port = (int)$port;
		$this->lastupdate = $lastupdate;
		$this->publickey = null;
	}
	
	public function getIp(){
		return $this->ip;
	}
	
	public function getId(){
		return $this->id;
	}
	
	public function getName(){
		return $this->name;
	}
	
	public function getPort(){
		return $this->port;
	}
	
	public function getPublicKey(){
		if (is_null($this->publickey)){
			$this->publickey = $this->loadPublicKey();
		}
		return $this->publickey;
	}
	
	private function getHost() {
		if($this->port == 80) {
			$host = "http://{$this->ip}/";
		} else {
			$host = "http://{$this->ip}:{$this->port}/";
		}		
		return $host;
	}
	
	public function getAllModules() {
		$list = json_decode(file_get_contents($this->getHost()."?j=".json_encode(array("c"=>1))));
		return $list->r;
	}
	
	public function loadPublicKey() {
		$list = json_decode(file_get_contents($this->getHost()."?j=".json_encode(array("c"=>6))));
		return $list->r;
	}
	
	public function getAllVersions($modulemeta) {
		$list = json_decode(file_get_contents($this->getHost()."?j=".json_encode(array("c"=>2,"m"=>$modulemeta))));
		return $list->r;
	}
	
	public function getLatestVersion($modulemeta) {
		$module = json_decode(file_get_contents($this->getHost()."?j=".json_encode(array("c"=>7,"m"=>$modulemeta))));
		return $module->r;
	}
	
	public function getDependencies($modulemeta) {
		$list = json_decode(file_get_contents($this->getHost()."j=".json_encode(array("c"=>3,"m"=>$modulemeta))));
		return $list->r;
	}
	
	public function getDescDependencies($modulemeta) {
		$list = json_decode(file_get_contents($this->getHost()."j=".json_encode(array("c"=>4,"m"=>$modulemeta))));
		return $list->r;
	}
	
	public function verifyModule($data,$signature){
		error_log($signature);
		$decoded_signature = base64_decode($signature);
		$rsa = new \Crypt_RSA();
		$rsa->setSignatureMode(CRYPT_RSA_SIGNATURE_PKCS1);
		$rsa->setHash('sha256');
		$rsa->setMGFHash('sha256');
		$rsa->loadKey($this->getPublicKey());
		return $rsa->verify($data,$decoded_signature);
	}
	
	public function downloadModule($modulemeta){
		$core = Core::getInstance();
		if(!is_array($modulemeta)){
			$modulemeta = $core->parseObjectToArray($modulemeta);
		}
		$response = file_get_contents($this->getHost().'?j='.urlencode(json_encode(array('c'=>5,'m'=>$modulemeta))));
		error_log($response);
		$list = json_decode($response);
		if($list == null){
			throw new ModuleException("DownloadModule: Could not download module");
		}
		$modulefile = fopen("/tmp/".$list->r->name.".tar.gz",'w');
		if(!$modulefile){
			throw new ModuleException("DownloadModule: Could not write module to harddrive");
		}
		$data = base64_decode($list->data);
		if(!$this->verifyModule($data, $list->r->signature)){
			throw new ModuleException("Verify Module: The module verification failed.");
		}
		fwrite($modulefile,$data);
		fclose($modulefile);
	}
	
	public function getModule($moduleid) {
		
	}
	
	public function store() {
		$core = Core::getInstance();
		$moduleM = $core->getModuleManager();
		
		$db = $core->getDB();
		$currentRepos =count($moduleM->getRepositories());
		
		if ($currentRepos == 1){
			if (!is_int($this->id)){
				throw new RepositoryException("Storing Repo: There is a repository, but this one has no ID.");
			}
			try {
				$repo = $moduleM->getRepository($this->id);
			}catch(RepositoryException $e){
				throw new RepositoryException("Storing Repo: This repository is not the repository, that is already in the Database");
			}
		}elseif ($currentRepos == 0){
			if ($this->id == null){
				$this->id = $db->getSeqNext('REP_GEN');
			}
		}else{
			throw new RepositoryException("There are two, even more or negative repositories. Shit's massively fucked up here!") ;
		}
		$stmnt = "UPDATE OR INSERT INTO REPOSITORIES (REP_ID, REP_NAME, REP_IP, REP_PORT, REP_LASTUPDATE, REP_PUBLICKEY) VALUES (?,?,?,?,?,?) MATCHING (REP_ID);";
		$db->query($core,$stmnt,array($this->id,$this->name,$this->ip,$this->port,$this->lastupdate, $this->getPublicKey()));
		return;
	}

	public function delete(){
		if (is_null($this->id)){
			throw new RepositoryException("Can't delete Repo with null-id! ");
		}
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$stmnt = "DELETE FROM REPOSITORIES WHERE REP_ID = ? ;" ;
		$db->query($core,$stmnt,array($this->id));
		return;
	} 
}

?>
