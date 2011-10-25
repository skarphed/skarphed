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
	
}
?>