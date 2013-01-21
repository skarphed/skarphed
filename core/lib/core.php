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
namespace scv;

abstract class Singleton {
	abstract public static function getInstance();

	abstract protected function init();
}

require_once 'configuration.php';
require_once 'database.php';
require_once 'module.php';
require_once "user.php";
require_once "css.php";
require_once "operation.php";
require_once "template.php";
require_once "site.php";
require_once "rightmanagement.php";
require_once "binary.php";
require_once "action.php";

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
	private $modules = null;
	private $rights = null;
	private $users = null;
	private $css = null;
	private $operations = null;
	private $templates = null;
	private $composite = null;
	private $binary = null;
	private $action = null;
	
	public function getName(){
		return 'de.masterprogs.scoville.core';
	}
	
	protected function init(){
		$this->debugGrindlog("====== New Session! Time: ".time());
		$this->config = new Config();
		$this->database = new Database();
		$this->config->initFromDb($this->database);
	}
	
	public function getDB(){
		return $this->database;
	}
	
	public function getConfig(){
		return $this->config;
	}
	
	public function getRightsManager(){
		if (!isset($this->rights)){

			$this->rights = RightsManager::getInstance();
		}
		return $this->rights;
	}
	
	public function getModuleManager(){
		if (!isset($this->modules)){
			$this->modules = ModuleManager::getInstance();
		}
		return $this->modules;
	}
	
	public function getUserManager(){
		if (!isset($this->users)){

			$this->users = UserManager::getInstance();
		}
		return $this->users;
	}
	
	public function getCssManager(){
		if (!isset($this->css)){

			$this->css = CssManager::getInstance();
		}
		return $this->css;
	}
	
	public function getOperationManager(){
		if (!isset($this->operations)){

			$this->operations = OperationManager::getInstance();
		}
		return $this->operations;
	}
	
	public function getTemplateManager(){
		if (!isset($this->templates)){

			$this->templates = TemplateManager::getInstance();
		}
		return $this->templates;
	}
	
	public function getCompositeManager(){
		if (!isset($this->composite)){

			$this->composite = CompositeManager::getInstance();
		}
		return $this->composite;
	}
	
	public function getBinaryManager() {
		if(!isset($this->binary)) {
			$this->binary = BinaryManager::getInstance();
		}
		return $this->binary;
	}
	
	public function getActionManager(){
		if(!isset($this->action)) {
			$this->action = ActionManager::getInstance();
		}
		return $this->action;
	}
	
	public function renderModule($modulename, $moduleInstanceId){
		$module = new Module($modulename);
		return $module->render($moduleInstanceId);
	}
	
	public function renderHTML($moduleInstanceId){
		return false;
	}
	public function renderJavascript($moduleInstanceId){
		return false;
	}
	
	//EIGENER LOG FUER DEBUGGING
	// ACHTUNG!!1!! ESCAPESHELLARG ENTFERNT ANFUEHRuNGSZEICHEN! 
	public function debugGrindlog($message){
		$grindLog = fopen('/tmp/Grindlog.log','a+');
		fwrite($grindLog, "[LEN ".strlen($message)."] ".$message."\n");
		fclose($grindLog);
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
	
	public function recursiveDelete($dir){
		if (is_dir($dir)) {
			$objects = scandir($dir);
			foreach ($objects as $object) {
				if ($object != "." && $object != "..") {
					if (filetype($dir."/".$object) == "dir") $this->recursiveDelete($dir."/".$object); else unlink($dir."/".$object);
				}
			}
			reset($objects);
			rmdir($dir);
		}
	}
}
?>