<?php
namespace scv;

include_once 'core.php';

class CssException extends \Exception {}

class CssManager extends Singleton{
	private static $instance = null;
	
	public static function getInstance(){
		if (CssManager::$instance==null){
			CssManager::$instance = new CssManager();
			CssManager::$instance->init();
		}
		return CssManager::$instance;
	}
	
	protected function init(){}
	
	
	/**
	 * Set Css PropertySet
	 * 
	 * Takes a Css Propertyset-Object and Saves Its contents to the database
	 * Automatically generates a new CSS-File Hash for all the sessions or
	 * The current session, depending on what has been changed
	 * 
	 * @param CssPropertySet $propertyset The CSS PropertySet that is to be entered to DB
	 * 
	 */
	public function setCssPropertySet($propertyset){
		
	}
	
	/**
	 * Get CSS Propertyset
	 * 
	 * Gets either the general Propertyset XOR The propertyset for a module, widget or a sessionid
	 * 
	 * @param int $moduleId A Module ID
	 * @param int $widgetId A Widget ID
	 * @param string $sessionId A PHP Session ID
	 * @return CssPropertySet A CssPropertySet Object
	 */
	public function getCssPropertySet($moduleId=null,$widgetId=null,$sessionId=null){
		$cssPropertySet = null;
		
		return $cssPropertySet;
	}
	
	/**
	 * Render CSS into a file
	 *
	 * Renders the CSS from the databasecontents into a Css file on the server. The CSS-File
	 * Is named after a MD5-Hash of the current user's PHPsession and a random value
	 */
	public function render(){
		
		
	}
	
	/**
	 * Get Name of CSS File
	 *
	 * Gets the name of the CSS file for the current session User
	 */
	public function getCssFile(){
		$core = Core::getInstance();
		$db = $core->getDB();
		if (isset($_SESSION['user']) and isset($_SESSION['loggedin']) and $_SESSION['loggedin'] == true){
			$stmnt ="SELECT CSE_FILE FROM CSSSESSION WHERE CSE_SESSION = ? ;";
			$res = $db->query($core,$stmnt,array(session_id()));
			if ($set = $db->fetchArray($res)){
				return ($set['CSE_FILE']);
			}else{
				return "css_generic.css";
			}
		}else{
			return "css_generic.css";
		}
	}
	
}

class CssPropertySet {
	private $properties = array();
	
	const GENERAL = 0;
	const MODULE = 1;
	const WIDGET = 2;
	const SESSION = 3;
	
	private $type = null;
	
	private $moduleId = null;
	private $widgetId = null;
	private $session = null;
}
