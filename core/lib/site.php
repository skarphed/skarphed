<?php
namespace scv;

include_once 'core.php';

class SiteException extends \Exception{}
class WidgetException extends \Exception{}

class CompositeManager extends Singleton{
	private static $instance = null;
	
	/**
	 * Get Singleton Instance
	 * 
	 * Returns the singleton Instance of the Rightsmanager
	 * 
	 * @return RightsManager The rights manager
	 */
	public static function getInstance(){
		if (CompositeManager::$instance==null){
			CompositeManager::$instance = new CompositeManager();
			CompositeManager::$instance->init();
		}
		return CompositeManager::$instance;
	}
	
	protected function init(){}
	
	
	public function getSite($siteId){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$stmnt = "SELECT SIT_ID, SIT_NAME, SIT_DESCRIPTION, SIT_SPACES, SIT_FILENAME ;";
		$res=$db->query($core,$stmnt,array($siteId));
		if($set = $db->fetchArray($res)){
			$site = new Site();
			$site->setId($siteId);
			$site->setName($set['SIT_NAME']);
			$site->setDescription($set['SIT_DESCRIPTION']);
			$site->setFilename($set['SIT_FILENAME']);
			$site->setSpaces($set['SIT_SPACES']);
			return $site;
		}else{
			throw SiteException("Get: This Site does not exist in Database");
		}
	}
	
	public function getSitesMeta($withMinimap=false){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$ret = array();
		
		//Suboptimal, aber hoechstwahrscheinlich nicht performancekritisch
		$stmnt = "SELECT SIT_ID FROM SITES;";
		$res = $db->query($core,$stmnt);
		while($set= $db->fetchArray($res)){
			$site = $this->getSite($set['SIT_ID']);
			$ret[] = $site->getMeta($withMinimap);
		}
		return $ret;
	}
	
	public function getWidget($id){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$stmnt = "SELECT WGT_NAME, WGT_SIT_ID, WGT_MOD_ID, WGT_SPACE FROM WIDGETS WHERE WGT_ID = ?;";
		$res = $db->query($core,$stmnt,array($id));
		if ($set = $db->fetchArray($res)){
			$wgt = new Widget();
			$wgt->setId($id);
			$wgt->setName($set['WGT_NAME']);
			$wgt->setSiteId($set['WGT_SIT_ID']);
			$wgt->setModuleId($set['WGT_MOD_ID']);
			$wgt->setSpace($set['WGT_SPACE']);
			return $wgt;
		}else{
			throw new WidgetException("Get: There is now widget with the id $id");
		}
	}
	
	public function createWidget($moduleId,$name){
		$widget = new Widget();
		$widget->setName($name);
		$widget->setModuleId($moduleId);
		$widget->store();
		return $widget->getId();
	}
	
	public function getWidgetsForSiteMeta($site){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$ret = array();
		for ($i = 1;$i< $site->getSpaces()+1 ; $i++){
			$ret[$i] = 0;
		}
		
		$stmnt = "SELECT WGT_ID, WGT_NAME, WGT_MOD_ID, WGT_SPACE FROM WIDGETS WHERE WGT_SIT_ID = ? ;";
		$res = $db->query($core,$stmnt,array($site->getId()));
		while($set = $db->fetchArray($res)){
			$ret[$set['WGT_SPACE']] = array("id"=>$set['WGT_ID'],"name"=>$set['WGT_NAME'],"mouledId"=>$set['WGT_MOD_ID']);
		}
		return $ret;
	} 
}

class Site {
	private $id = null;
	private $name = null;
	private $description = null;
	private $spaces = null;
	private $html = null;
	private $filename = null;
	
	public function setId($id){
		$this->id = (int)$id;
	}
	
	public function getId(){
		return $this->id;
	}
	
	public function setName($name){
		$this->name=(string)$name;
	}
	
	public function setDescription($description){
		if (strlen($description) <=500){
			$this->description = (string)$description;
		}
	}
	
	public function setSpaces($spaces){
		$this->spaces = (int)$spaces;
	}
	
	public function getSpaces(){
		return $this->spaces;
	}
	
	public function setFilename($filename){
		$this->filename = (string)$filename;
	}
	
	public function assignWidget($spaceId,$widget,$checkRight=true){
		//TODO: Recht erfinden und drauf ueberpruefen
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$stmnt = "UPDATE WIDGETS SET WGT_SIT_ID = ? , WGT_SPACE = ? WHERE WGT_ID = ? ;";
		$db->query($core,$stmnt,array($this->id,$spaceId,$widget->getId()));
	}
	
	public function removeWidget($spaceId,$checkRight=true){
		//TODO: Recht erfinden und drauf ueberpruefen
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$stmnt = "UPDATE WIDGETS SET WGT_SIT_ID = NULL , WGT_SPACE = NULL  WHERE WGT_SIT_ID = ? AND WGT_SPACE = ? ;";
		$db->query($core,$stmnt,array($this->id,$spaceId));
	}
	
	private function loadHTML(){
		
	}
	
	public function getHTML(){
		if (!isset($this->html)){
			$this->loadHTML();
		}
		return $this->html;
	}
	
	public function getMeta($withMinimap=true){
		$ret=array();
		$ret["id"]=$this->id;
		$ret["name"]=$this->name;
		$ret["description"]=$this->description;
		$ret["spaces"]=Widget::getWidgetsForSiteMeta($this);
		$minimapfile = "minimap_".str_replace(".html", "", $this->filename).".png";
		$ret["minimap"] = base64_encode(file_get_contents("../web/".$minimapfile));
		return $ret;
	}
	
	
}

class Widget {
	private $id=null;
	private $name= null;
	private $siteId=null;
	private $moduleId=null;
	private $space=null;
	
	public function getId(){
		return $this->id;
	}
	
	
	public function setId($id){
		$this->id = (int)$id;
	}
	
	public function setName($name){
		$this->name = (string)$name;
	}
	
	public function setSiteId($siteId){
		$this->siteId = (int)$siteId;
	}
	
	public function setModuleId($moduleId){
		$this->moduleId = (int)$moduleId;
	}
	
	public function setSpace($space){
		$this->space = (int)$space;
	}
	
	public function store($checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		if ($this->id == null){
			$this->id = $db->getSeqNext('WGT_GEN');
		}
		
		if ($this->moduleId == null){
			throw new WidgetException("Store: Cannot store a Widget that is not linked to a Module (\$moduleId)");
		}
		
		$stmnt = "UPDATE OR INSERT INTO WIDGETS (WGT_ID, WGT_NAME, WGT_SIT_ID, WGT_MOD_ID, WGT_SPACE)
					VALUES (?,?,?,?,?) MATCHING (WGT_ID) ;";
	    $db->query($core,$stmnt,array($this->id,$this->name,$this->siteId,$this->moduleId,$this->space));
	    return;
	}
	
	public function delete($checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		if($this->id == null){
			throw new WidgetException("Delete: Cannot delete a Widget that does not exist in database");
		}
		
		$stmnt = "DELETE FROM WIDGETS WHERE WGT_ID = ? ;";
		$db->query($core,$stmnt,array($this->id));
	}
}
	
?>