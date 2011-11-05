<?php
namespace scv;

include_once 'core.php';

class CssException extends \Exception {}

class CssManager extends Singleton{
	private static $instance = null;
	
	const ALL = -1;

	public static function getInstance(){
		if (CssManager::$instance==null){
			CssManager::$instance = new CssManager();
			CssManager::$instance->init();
		}
		return CssManager::$instance;
	}
	
	protected function init(){}
	
	/**
	 * Create CssPropertySet from Serialized Data
	 * 
	 * Creates a new CssPropertySet and tries to Load it with the Data from $set
	 * If succeeds, the new CssPropertyset will be returned
	 * 
	 * @param Array $set The serialized Data
	 * @return CssPropertySet The new CssPropertySet 
	 */
	public function createCssPropertySetFromSerial($set){
		$cssPropertySet = new CssPropertySet();
		$cssPropertySet->buildSerialized($set);
		return $cssPropertySet;
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
			                   INNER JOIN MODULES ON (CSS_MOD_ID = MOD_ID)
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
			                   INNER JOIN MODULES ON (CSS_MOD_ID = MOD_ID)
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
	    				   INNER JOIN WIDGETS ON (CSS_WGT_ID = WGT_ID)
	    				   INNER JOIN MODULES ON (WGT_MOD_ID = MOD_ID)
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
					$stmnt_moduleId = "SELECT WGT_MOD_ID FROM WIDGETS WHERE WGT_ID = ? ; ";
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
		    				   INNER JOIN WIDGETS ON (CSS_WGT_ID = WGT_ID)
		    				   INNER JOIN MODULES ON (WGT_MOD_ID = MOD_ID)
		    				 WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NOT NULL AND CSS_SESSION IS NULL AND CSS_WGT_ID = ? ;";
				$res = $db->query($core,$stmnt_widget,array($widgetId));
				while($set = $db->fetchArray($res)){
					$cssPropertySet->editValue($set['CSS_SELECTOR'], $set['CSS_TAG'], $set['CSS_VALUE']);
				}
				return $cssPropertySet;
			}
		}
		if ($sessionId != null){
			return null;
			//TODO: Implement
			
			/*$stmnt_session = "SELECT CSS_SELECTOR, CSS_TAG, CSS_VALUE FROM CSS
			WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NOT NULL;";*/
		}
		
		//The Standard CssPropertySet
		$cssPropertySet = new CssPropertySet();
		$cssPropertySet->setTypeGeneral();
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
	public function render($filename){
		$core = Core::getInstance();
		$css = "";
		if ($this->getCssPropertySet(null,null,session_id())==null){
			$genericSet = $this->getCssPropertySet();
			$moduleSets = $this->getCssPropertySet($moduleId=CssManager::ALL,null,null);
			$widgetSets = $this->getCssPropertySet(null,$widgetId=CssManager::ALL,null);
			
			$css.=$genericSet->render();
			foreach ($moduleSets as $moduleSet){
				$css.=$moduleSet->render();
			}
			foreach ($widgetSets as $widgetSet){
				$css.=$widgetSet->render();
			}
			$cssFile = fopen($filename,'w');
			fwrite($cssFile,$css);
			fclose($cssFile);
		}else{
			$genericSet = $this->getCssPropertySet();
			$moduleSets = $this->getCssPropertySet($moduleId=CssManager::ALL,null,null);
			$widgetSets = $this->getCssPropertySet(null,$widgetId=CssManager::ALL,null);
			
			$css.=$genericSet->render();
			foreach ($moduleSets as $moduleSet){
				$css.=$moduleSet->render();
			}
			foreach ($widgetSets as $widgetSet){
				$css.=$widgetSet->render();
			}
			$cssFile = fopen($filename,'w');
			fwrite($cssFile,$css);
			fclose($cssFile);
		}		
		return; 
	}
	
	/**
	 * Get Name of CSS File
	 *
	 * Gets the name of the CSS file for the current session User
	 */	
	public function getCssFile(){
		$cssFolder = "_css/"; // Auslagern in die config  UND Folder nicht mehr in der DB mitspeichern
		
		if(!file_exists($cssFolder) or !is_dir($cssFolder)){
			mkdir($cssFolder);
		}
		
		$core = Core::getInstance();
		$db = $core->getDB();
		if (isset($_SESSION['user']) and isset($_SESSION['loggedin']) and $_SESSION['loggedin'] == true){
			$stmnt ="SELECT CSE_FILE FROM CSSSESSION WHERE CSE_SESSION = ? AND CSE_OUTDATED = 0;";
			$res = $db->query($core,$stmnt,array(session_id()));
			if ($set = $db->fetchArray($res)){
				$filename =  $set['CSE_FILE'];
			}else{
				$filename = $cssFolder.'style_'.hash('md5',session_id().rand(0,9999)).'.css';
				$stmnt = "INSERT INTO CSSSESSION (CSE_SESSION,CSE_FILE,CSE_OUTDATED) VALUES (?,?,0) ;";
				$db->query($core,$stmnt,array(session_id(),$filename));
			}
		}else{
			$stmnt ="SELECT CSE_FILE FROM CSSSESSION WHERE CSE_SESSION = 'GENERAL' AND CSE_OUTDATED = 0 ;";
			$res = $db->query($core,$stmnt);
			if ($set = $db->fetchArray($res)){
				$filename = $set['CSE_FILE'];
			}else{
				$filename = $cssFolder.'style_'.hash('md5','general'.rand(0,9999)).'.css';
				$stmnt = "INSERT INTO CSSSESSION (CSE_SESSION,CSE_FILE,CSE_OUTDATED) VALUES ('GENERAL',?,0) ;";
				$db->query($core,$stmnt,array($filename));
			}
		}
		if (!file_exists($filename)){
			$this->render($filename);
		}
		$this->cleanUpCssSessionTable();
		return $filename;
		
	}
	
	/**
	 * Clean up CSS Session Table
	 * 
	 * Deletes all Entries from CSSSESSION with CSE_OUTDATED marked as TRUE
	 */
	private function cleanUpCssSessionTable(){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "DELETE FROM CSSSESSION WHERE CSE_OUTDATED = 1;";
		$db->query($core,$stmnt);
		return;
	}
	
	public function setSessionCssProperty(){
		
	}
	
}

class CssPropertySet {
	private $properties = array();
	
	const SPLIT = "?";
	
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
		//$this->properties[array('s'=>$selector,'t'=>$tag)]= array('v'=>$value,'i'=>false); //t Tag v Value i Inherited
		$this->properties[$selector.CssPropertySet::SPLIT.$tag]= array('v'=>$value,'i'=>false); //t Tag v Value i Inherited
	}
	
	/**
	 * Get Value
	 * 
	 * Get A CSS Value of this CssPropertySet determined by a selector and a Tag
	 */
	public function getValue ($selector, $tag){
	    if (isset($this->properties[$selector.CssPropertySet::SPLIT.$tag])){
	    	return $this->properties[$selector.CssPropertySet::SPLIT.$tag];
	    }else{
	    	return null;
	    }
	     
	}
	
	/**
	 * Set All Values Inherited
	 * 
	 * Marks every CSS Property as Inherited from another CssPropertySet of higher level
	 * Use is to easily Fetch a specialized CssPropertySet in CssManager::getCssPropertySet()
	 */	
	public function setAllInherited(){
		foreach($this->properties as $selector => $setting){
			if (is_object($setting)){
				$this->properties[$selector]->i = true;
			}else{
				$this->properties[$selector]['i'] = true;
			}
		}
	}
	
	/**
	 * Get Non-Inherited Properties
	 * 
	 * GetAll non-Inherited Properties of this set
	 * 
	 * @return Array Non inherited Properties
	 */
	private function getNonInherited(){
		$core = Core::getInstance();
		$ret = array();
		foreach ($this->properties as $selector => $values){
			if (is_object($values)){
				if ($values->i != true){
					$ret[$selector] = $values;
				}
			}else{
				if ($values['i'] != true){
					$ret[$selector] = $values;
				}	
			}
		}
		return $ret;
	}

	/**
	 * Store the CssPropertySet
	 * 
	 * Store the Current State of the CssPropertyset into the Database
	 */
	public function store($checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		if ($checkRight){
			$userM = $core->getUserManager();
			$rightM = $core->getRightsManager();
			if (!$rightM->checkRight('scoville.css.edit',$userM->getSessionUser())){
				return;
			}
		}
		
		$this->delete(); //Effizienter implementieren
		
		$valuesToStore = $this->getNonInherited();
		$stmnt = "UPDATE OR INSERT INTO CSS (CSS_SELECTOR, CSS_TAG, CSS_VALUE, CSS_MOD_ID, CSS_WGT_ID, CSS_SESSION)
		           VALUES ( ?,?,?,?,?,?) MATCHING (CSS_SELECTOR,CSS_TAG,CSS_MOD_ID,CSS_WGT_ID, CSS_SESSION);";
		foreach($valuesToStore as $selector => $values){
			$splittedSelector = explode('?',$selector);
			
			//TODO: HERE BE DRAGONS -> OBJEKTZUGRIFF mit pfeil. koennte das probleme machen?
			$db->query($core,$stmnt,array($splittedSelector[0],$splittedSelector[1],$values->v,$this->moduleId,$this->widgetId,$this->session));
		}
		
		if ($this->type==CssPropertySet::SESSION){
			$stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1 WHERE CSE_SESSION = ? ;";
			$db->query($core,$stmnt,array(session_id()));
		}else{
			$stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1;";
			$db->query($core,$stmnt);
		}
		
		return;
	}
	
	/**
	 * Delete the CssPropertySet
	 * 
	 * Delete this CssPropertySet from the Database
	 */
	public function delete($checkRight=true){
		$core = Core::getInstance();
		
		if ($checkRight){
			$userM = $core->getUserManager();
			$rightM = $core->getRightsManager();
			if (!$rightM->checkRight('scoville.css.edit',$userM->getSessionUser())){
				return;
			}
		}
		
		$db = $core->getDB();
		switch($this->type){
			case CssPropertySet::GENERAL:
				$stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL;";
				$db->query($core,$stmnt);
				break;
			case CssPropertySet::MODULE:
				$stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID = ? AND CSS_WGT_ID IS NULL AND CSS_SESSION IS NULL;";
				$db->query($core,$stmnt,array($this->moduleId));
				break;
			case CssPropertySet::WIDGET:
				$stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID = ? AND CSS_SESSION IS NULL;";
				$db->query($core,$stmnt,array($this->widgetId));
				break;
			case CssPropertySet::SESSION:
				$stmnt = "DELETE FROM CSS WHERE CSS_MOD_ID IS NULL AND CSS_WGT_ID IS NULL AND CSS_SESSION = ? ;";
				$db->query($core,$stmnt,array($this->session));
				break;				
		}		
		
		if ($this->type==CssPropertySet::SESSION){
			$stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1 WHERE CSE_SESSION = ? ;";
			$db->query($core,$stmnt,array(session_id()));
		}else{
			$stmnt = "UPDATE CSSSESSION SET CSE_OUTDATED = 1;";
			$db->query($core,$stmnt);
		}
		return;
	}
	
	/**
	 * Render The CssPropertySet
	 * 
	 * Render This Css PropertySet
	 * 
	 * @return string CSS-Code
	 */
	public function render(){
		$core = Core::getInstance();
		$moduleM = $core->getModuleManager();
		$css = "";
		switch($this->type){
			case CssPropertySet::GENERAL:
				$selectorlist = array();
				foreach ($this->getNonInherited() as $selector => $values){
					$splittedSelector = explode('?',$selector);
					if (count($splittedSelector) == 1){
						array_unshift("",$splittedSelector);
					}
					if(!isset($selectorlist[$splittedSelector[0]])){
						$selectorlist[$splittedSelector[0]]= array();
					}
					$selectorlist[$splittedSelector[0]][]=array('t'=>$splittedSelector[1],'v'=>$values['v']);
				}
				foreach($selectorlist as $selector => $values){
					$css.=$selector."{\n";
					foreach ($values as $value){
						$css.=$value['t'].":".$value['v'].";\n";
					}
					$css.="}\n\n";
				}
				break;
			case CssPropertySet::MODULE:
				$selectorlist = array();
				$moduleName = $moduleM->loadModuleById($this->moduleId)->getName();
				$moduleName = str_replace(".", "_", $moduleName);
				foreach ($this->getNonInherited() as $selector => $values){
					
					$splittedSelector = explode('?',$selector);
					if (count($splittedSelector) == 1){
						array_unshift("",$splittedSelector);
					}
					if(!isset($selectorlist[$splittedSelector[0]])){
						$selectorlist[$splittedSelector[0]]= array();
					}
					$selectorlist[$splittedSelector[0]][]=array('t'=>$splittedSelector[1],'v'=>$values['v']);
				}
				foreach($selectorlist as $selector => $values){
					$css.=".".$moduleName." ".$selector."{\n";
					foreach ($values as $value){
						$css.=$value['t'].":".$value['v'].";\n";
					}
					$css.="}\n\n";
				}
				break;
			case CssPropertySet::WIDGET:
				$selectorlist = array();
				foreach ($this->getNonInherited() as $selector => $values){
					$splittedSelector = explode('?',$selector);
					if (count($splittedSelector) == 1){
						array_unshift("",$splittedSelector);
					}
					if(!isset($selectorlist[$splittedSelector[0]])){
						$selectorlist[$splittedSelector[0]]= array();
					}
					$selectorlist[$splittedSelector[0]][]=array('t'=>$splittedSelector[1],'v'=>$values['v']);
				}
				foreach($selectorlist as $selector => $values){
					$css.=".w".$this->widgetId." ".$selector."{\n";
					foreach ($values as $value){
						$css.=$value['t'].":".$value['v'].";\n";
					}
					$css.="}\n\n";
				}
				break;
			case CssPropertySet::SESSION:
				break;	
		}
		return $css;
	}

	/**
	 * SerializeSet
	 * 
	 * Serialize this object (preferably for json export to the Admin interface)
	 * 
	 * @return Array The serialized Object
	 */
	public function serializeSet(){
		$ret = array();
		$ret['type'] = $this->type;
		$ret['moduleId'] = $this->moduleId;
		$ret['widgetId'] = $this->widgetId;
		$ret['session'] = $this->session;
		$ret['properties'] = $this->properties;
		return $ret;
	}
	
	/**
	 * Build from Serialized Data
	 * 
	 * Checks whether the serialized data is valid. If yes, builds this CssPropertySet from the data
	 * 
	 * @param Array $set The Serialized CssPropertySet Data
	 */
	public function buildSerialized($set){
		switch($set->type){
			case CssPropertySet::GENERAL:
				if ($set->moduleId != null or $set->widgetId != null or $set->session !=null){
					throw new CssException('Invalid Propertyset: GENERAL type set must not have any Ids');
				}
				break;
			case CssPropertySet::MODULE:
				if ($set->moduleId == null or $set->widgetId != null or $set->session !=null){
					throw new CssException('Invalid Propertyset: MODULE type set must not have any Ids but must have ModuleId');
				}
				break;
			case CssPropertySet::WIDGET:
				if ($set->moduleId != null or $set->widgetId == null or $set->session !=null){
					throw new CssException('Invalid Propertyset: WIDGET type set must not have any Ids but must have WidgetId');
				}
				break;
			case CssPropertySet::SESSION:
				if ($set->moduleId != null or $set->widgetId != null or $set->session ==null){
					throw new CssException('Invalid Propertyset: SESSION type set must not have any Ids but must have Session');
				}
				break;
		}
		$this->moduleId = $set->moduleId;
		$this->widgetId = $set->widgetId;
		$this->session = $set->session;
		$this->type = $set->type;
		$this->properties = $set->properties;
	}
}
