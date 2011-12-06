<?php
namespace scv;

abstract class Singleton {
	abstract public static function getInstance();

	abstract protected function init();
}

include_once 'configuration.php';
include_once 'database.php';
include_once 'htmlparser.php';
include_once 'module.php';
include_once "user.php";
include_once "css.php";
include_once "operation.php";
include_once "template.php";
include_once "site.php";
include_once "rightmanagement.php";

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
	private $modules = null;
	private $rights = null;
	private $users = null;
	private $css = null;
	private $operations = null;
	private $templates = null;
	private $composite = null;
	
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
	// ACHTUNG!!1!! ESCAPESHELLARG ENTFERNT ANFUEHRuNGSZEICHEN! 
	public function debugGrindlog($message){
		system("echo '[LEN ".strlen($message)."] ".escapeshellarg($message)."' >> /tmp/Grindlog.log");
		//system("echo '[LEN ".strlen($message)."] ".$message."' >> /tmp/Grindlog.log");
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