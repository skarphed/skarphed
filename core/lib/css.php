<?php
namespace scv;

include_once 'core.php';

class CssException extends \Exception {}

class CssManager extends Singleton{
	private static $instance = null;
	
	const ALL = -1;
	const TAGS = array('accelerator','border');
	
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
	 * If $moduleId, $widgetId or $sessionId is given CssManager::ALL, it returns all CssSettings of that type
	 * 
	 * @param int $moduleId A Module ID
	 * @param int $widgetId A Widget ID
	 * @param string $sessionId A PHP Session ID
	 * @param bool $withInherited If TRUE, generates a CssPropertySet with all inherited values (ignored, when fetching ALL sets)
	 * @return CssPropertySet A CssPropertySet Object or an Array of CssPropertySet Objects
	 */
	public function getCssPropertySet($moduleId=null,$widgetId=null,$sessionId=null,$withInherited=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		if ($moduleId != null){
			if ($moduleId == CssManager::ALL){
				$ret = array();
				$stmnt_module = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME, MOD_ID
			                 FROM CSS 
			                   INNER JOIN MODULE ON (CSS_MOD_ID = MOD_ID)
			                 WHERE CSS_MOD_ID IS NOT NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL ;";
				$res = $db->query($core,$stmnt_module);
				while($set = $db->fetchArray($res)){
					if (!isset($ret[$set['MOD_ID']])){
						$ret[$set['MOD_ID']] = new CssPropertySet();
						$ret[$set['MOD_ID']]->setModuleId($set['MOD_ID']);
					}
					$ret[$set['MOD_ID']]->editValue($set['CSS_SELECTOR'],$set['CSS_TAG'],$set['CSS_VALUE']);
				}
				return $ret;
			}else{
				if ($withInherited){
					$cssPropertySet = $this->getCssPropertySet();
					$cssPropertySet->setAllInherited();
				}else{
					$cssPropertySet = new CssPropertySet();
				}
				$cssPropertySet->setModuleId($moduleId);
				
				$stmnt_module = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME
			                 FROM CSS 
			                   INNER JOIN MODULE ON (CSS_MOD_ID = MOD_ID)
			                 WHERE CSS_MOD_ID IS NOT NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL AND CSS_MOD_ID = ? ;";
				$res = $db->query($core,$stmnt_module,array($moduleId));
				while($set = $db->fetchArray($res)){
					$cssPropertySet->editValue($set['CSS_SELECTOR'], $set['CSS_TAG'], $set['CSS_VALUE']);
				}
				return $cssPropertySet;
			}
		}
		if ($widgetId != null){
			if ($widgetId = CssManager::ALL){
				$ret = array();
				$stmnt_widget = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME, MOD_ID, WGT_NAME, WGT_ID 
	    				 FROM CSS
	    				   INNER JOIN WIDGET ON (CSS_WGT_ID = WGT_ID)
	    				   INNER JOIN MODULE ON (WGT_MOD_ID = MOD_ID)
	    				 WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NOT NULL AND CSS_SESSION IS NULL;";
				$res = $db->query($core, $stmnt_widget);
				while($set=$db->fetchArray($res)){
					if (!isset($ret[$set['WGT_ID']])){
						$ret[$set['WGT_ID']] = new CssPropertySet();
						$ret[$set['WGT_ID']]->setWidgetId($set['WGT_ID']);
					}
					$ret[$set['WGT_ID']]->editValue($set['CSS_SELECTOR'], $set['CSS_TAG'], $set['CSS_VALUE']);
				}
				return $ret;
				
			}else{
				if ($withInherited){
					$stmnt_moduleId = "SELECT WGT_MOD_ID FROM WIDGET WHERE WGT_ID = ? ; ";
					$res = $db->query($core,$stmnt_moduleId,array($widgetId));
					if ($set = $db->fetchArray($res)){
						$cssPropertyset = $this->getCssPropertySet($moduleId=$set['WGT_MOD_ID']);
						$cssPropertyset->setAllInherited();
					}else{
						throw new CssException('Get CssPropertySet: This Widget does not exist!');
					}
				}else{
					$cssPropertySet = new CssPropertySet();
				}
				$cssPropertySet->setWidgetId=($widgetId);
				$stmnt_widget = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE, MOD_NAME, WGT_NAME 
		    				 FROM CSS
		    				   INNER JOIN WIDGET ON (CSS_WGT_ID = WGT_ID)
		    				   INNER JOIN MODULE ON (WGT_MOD_ID = MOD_ID)
		    				 WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NOT NULL AND CSS_SESSION IS NULL AND CSS_WGT_ID = ? ;";
				$res = $db->query($core,$stmnt_widget,array($widgetId));
				while($set = $db->fetchArray($res)){
					$cssPropertySet->editValue($set['CSS_SELECTOR'], $set['CSS_TAG'], $set['CSS_VALUE']);
				}
				return $cssPropertySet;
			}
		}
		if ($sessionId != null){
			return $cssPropertySet;
			//TODO: Implement
			
			/*$stmnt_session = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE FROM CSS
			WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NOT NULL;";*/
		}
		
		//The Standard CssPropertySet
		$cssPropertySet = new CssPropertySet();
		$stmnt = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL;";
		$res = $db->query($core,$stmnt);
		while($set = $db->fetchArray($res)){
			$cssPropertySet->editValue($set['CSS_SELECTOR'], $set['CSS_TAG'], $set['CSS_VALUE']);
		}
		
		return $cssPropertySet;
	}
	
	/**
	 * Render CSS into a file
	 *
	 * Renders the CSS from the databasecontents into a Css file on the server. The CSS-File
	 * Is named after a MD5-Hash of the current user's PHPsession and a random value
	 */
	public function render(){
		if ($this->getCssPropertySet($sessionId=session_id())==null){
			$filename = hash('md5','general'.rand(0,9999));
			
			
			
		}else{
			$filename = hash('md5',session_id().rand(0,9999));
		}		
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
	
	public function setSessionCssProperty(){
		
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
	
	/**
	 * Set Module Id
	 * 
	 * Sets the Id of the module to that this CssPropertySet-Object belongs.
	 * Automatically resets widgetId and session; Automatically changes The Type to CssPropertySet::MODULE
	 * 
	 * @param int $moduleId A module Id
	 */
	public function setModuleId($moduleId){
		$this->moduleId = (int)$moduleId;
		$this->session = null;
		$this->widgetId = null;
		$this->type = CssPropertySet::MODULE;
		return;
	}
	
	/**
	 * Set Widget Id
	 * 
	 * Sets the Id of the widget to that this CssPropertySet-Object belongs.
	 * Automatically resets moduleId and session; Automatically changes The Type to CssPropertySet::WIDGET
	 * 
	 * @param int $widgetId A widget Id
	 */
	public function setWidgetId($widgetId){
		$this->widgetId = (int)$widgetId;
		$this->session = null;
		$this->moduleId = null;
		$this->type = CssPropertySet::WIDGET;
		return;
	}
	
	/**
	 * Set Session Id
	 * 
	 * Sets the Id of the session to that this CssPropertySet-Object belongs.
	 * Automatically resets moduleId and widgetId; Automatically changes The Type to CssPropertySet::SESSION
	 * 
	 * @param string $session A PHP-Session Id
	 */
	public function setSessionId($session){
		$this->session = (string)$session;
		$this->moduleId = null;
		$this->widgetId = null;
		$this->type = CssPropertySet::SESSION;
		return;
	}
	
	/**
	 * Set Type to general
	 * 
	 * Sets this CssPropertySet-Object to be General. Automatically resets all IDs assigned to this object
	 * Automatically sets Type to CssPropertySet::GENERAL
	 */
	public function setTypeGeneral(){
		$this->session = null;
		$this->moduleId = null;
		$this->widgetId = null;
		$this->type = CssPropertySet::GENERAL;
		return;
	}
	
	/**
	 * Get Type
	 * 
	 * Returns this CssPropertySet Objects Type.
	 *  
	 * @return int A Type Constant
	 */
	public function getType(){
		return $this->type;
	}
	
	/**
	 * Get Module Id 
	 * 
	 * Returns this CssPropertySet Objects ModuleId
	 * 
	 * @return int a ModuleId
	 */
	public function getModuleId(){
		return $this->moduleId;
	}
	
	/**
	 * Get Widget Id 
	 * 
	 * Returns this CssPropertySet Objects WidgetId
	 * 
	 * @return int a WidgetId
	 */
	public function getWidgetId(){
		return $this->widgetId;
	}
	
	/**
	 * Get Session Id 
	 * 
	 * Returns this CssPropertySet Objects SessionID
	 * 
	 * @return string a PHP-Session Id
	 */
	public function getSessionId(){
		return $this->session;
	}
	
	/**
	 * Edit value 
	 * 
	 * Set a CSS-Value in this Set
	 * 
	 * @param string $selector A CSS Selector
	 * @param string $tag A CSS Tag for this selector to set
	 * @param string $value The value this tag should be set to
	 * @param bool $inherited If this flag is set, the value is inherited from a higher level
	 */
	public function editValue ($selector, $tag, $value, $inherited=false){
		$this->properties[$selector]= array('t'=>$tag,'v'=>$value,'i'=>false); //t Tag v Value i Inherited
	}
	
	public function getValue ($selector, $tag){
	
	}
	
	/**
	 * Set All Values Inherited
	 * 
	 * Marks every CSS Property as Inherited from another CssPropertySet of higher level
	 * Use is to easily Fetch a specialized CssPropertySet in CssManager::getCssPropertySet()
	 */	
	public function setAllInherited(){
		foreach($this->properties as $selector => $setting){
			$setting['i'] = true;
		}
	}
}
