<?php
namespace scv;

include_once 'core.php';

class RightsException extends \Exception{}

class Role {
	private $roleId = "";
	private $roleName = "";
	
	public function getId(){
		return $this->roleId;
	}
	
	public function getName(){
		return $this->roleName;
	}
	
	public function setId($roleId){
		$this->roleId = (int)$roleId;
	}
	
	public function setName($roleName){
		$this->roleName = $roleName;
	}
	
	public function store($checkRight=true){
		$core=Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
	    
		if ($rightM->checkRight('scoville.roles.create', $userM->getSessionUser()) or !$checkRight){
			$stmnt = "INSERT OR UPDATE INTO ROLE (ROL_ID, ROL_NAME) VALUES (?,?) MATCHING (ROL_ID); ";
			$db->query($core,$stmnt, $this->roleId, $this->roleName);
		}
		return;
	}
	
	public function addRight($rightId, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
		
		if ($rightM->checkRight('scoville.roles.modify',$userM->getSessionUser()) or !$checkRight){
			$stmnt = "UPDATE OR INSERT INTO ROLERIGHTS (RRI_ROL_ID, RRI_RIG_ID) 
		    	        VALUES (?, (SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME= ?)) 
		        	  MATCHING (RRI_ROL_ID, RRI_RIG_ID);";
			$db->query($core, $stmnt, $this->roleId, $rightId);	
		}
		return;
	}
	
	public function removeRight($rightId, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		
		$checkString="";
		if ($checkRight){
			$checkstring = " AND 1 = (SELECT AVAILABLE FROM CHECK_RIGHT(". $userM->getSessionUserId().",'scoville.roles.modify')) ";
		}
		
		$stmnt = "DELETE FROM ROLERIGHTS WHERE RRI_ROL_ID = ? AND RRI_RIG_ID = ? $checkString ; ";
		$db->query($stmnt);
		return;
	}
	
	public function getRights($checkRight = true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		
		$checkString="";
		if ($checkRight){
			$checkstring = " AND 1 = (SELECT AVAILABLE FROM CHECK_RIGHT(". $userM->getSessionUserId().",'scoville.roles.modify')) ";
		}
		
		$stmnt = "SELECT RIG_NAME, RIG_ID FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) 
		            WHERE RRI_ROL_ID = ? $checkstring;";
        $res = $db->query($core, $stmnt, $this->roleId);
		$ret = array();
		while ($set = $db->fetchArray($res)){
			$ret[] = $set["RIG_NAME"];  
		}
		return $ret;
	}
	
	public function getGrantableRights($checkRight = true){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		$rightArray = $rightM->getGrantableRights($this);
		return $rightArray; 
	}
	
	public function delete($checkRight=true){
		$core=Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		
		$checkString="";
		if ($checkRight){
			$checkstring = " AND 1 = (SELECT AVAILABLE FROM CHECK_RIGHT(". $userM->getSessionUserId().",'scoville.users.view')) ";
		}
		
		$stmntUserRoles = "DELETE FROM USERROLES WHERE URO_ROL_ID = ? $checkString ;";
		$stmntRole = "DELETE FROM ROLES WHERE ROL_ID = ? $checkString ;";
		$db->query($core,$stmntUserRoles, $this->roleId);
		$db->query($core,$stmntRole, $this->roleId);
	}
}

class RightsManager extends Singleton{
	private static $instance = null;
	
	public static function getInstance(){
		if (RightsManager::$instance==null){
			RightsManager::$instance = new RightsManager();
			RightsManager::$instance->init();
		}
		return RightsManager::$instance;
	}
	
	protected function init(){}
	
	public function checkRight($right,$user){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT AVAILABLE FROM CHECK_RIGHT(? , ?);";
		$res = $db->query($core,$stmnt,array($user->getId(),$right));
		$set = $db->fetchArray($res);
		return $set['AVAILABLE']; 
	}
	
	public function createRight($right, $moduleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$newRightId = $db->getSeqNext("RIG_GEN");
		$stmnt = "INSERT INTO RIGHTS (RIG_ID, RIG_NAME) VALUES (?,?);";
		$db->query($core, $stmnt, array($newRightId,$moduleId.".".$right));
		return;
	}
	
	public function removeRight($right, $moduleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "DELETE FROM RIGHTS WHERE RIG_NAME = ?;";
		$db->query($core, $stmnt, array($moduleId.".".$right));
		return;
	}
	
	public function getRightsForUser($user){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT RIG_NAME 
		          FROM USERRIGHTS 
		            INNER JOIN RIGHTS ON RIG_ID = URI_RIG_ID
		          WHERE URI_USR_ID = ?
		          UNION SELECT RIG_NAME
		          FROM USERROLES
		            INNER JOIN ROLERIGHTS ON URO_ROL_ID = RRI_ROL_ID
		            INNER JOIN RIGHTS ON RRI_RIG_ID = RIG_ID
		          WHERE URO_USR_ID = ?;";
		$result = $db->query($core, $stmnt, array($user->getId(),$user->getId()));
		$retval = array();
		while($set = $db->fetchArray($result)){
			$retval[] = $set['RIG_NAME'];
		}
		return $retval;
		
	}
	
	public function getGrantableRights($object){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();
		$sessionRights = $this->getRightsForUser($sessionUser);
		switch(get_class($object)){
			case 'User':
				$stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN USERRIGHTS ON (RIG_ID = URI_RIG_ID) WHERE URI_USR_ID = ? ;";
				break;
			case 'Role':
				$stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) WHERE RRI_ROL_ID = ? ;";
				break;
			default:
				throw new RightsException("Cannot get grantable Rights from Class: ".get_class($object));//TODO: Here be dragons. Injection von Klassennamen ueber Module	
		}
		
		$res = $db->query($core,$stmnt,array($object->getId()));
		$resrights = array();
		while($set = $db->fetchArray($res)){
			$resrights[] = $set['RIG_NAME'];
		}
		$result = array();
		foreach ($sessionRights as $sessionRight){
			if (in_array($sessionRight,$resrights)){
				$result[] = array('right'=>$sessionRight,'granted'=>true);
			}else{
				$result[] = array('right'=>$sessionRight,'granted'=>false);
			}
		}
		return $result;
	}
	
	public function getIdForRight($right){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME = ? ;";
		$res = $db->query($core,$stmnt, array($right));
		while($set = $db->fetchArray($res)){
			return $set['RIG_ID'];
		}
		return null;
	}
	
	public function getRoles($checkRight=false){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT ROL_ID, ROL_NAME FROM ROLES ;";
		$res = $db->query($core,$stmnt);
		$ret = array();
		while($set = $db->fetchArray($res)){
			$role = new Role();
			$role->setId($set["ROL_ID"]);
			$role->setName($set["ROL_NAME"]);
			$ret[] = $role;
		}
		return $ret;
	}
	
	public function getRole($roleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT ROL_ID, ROL_NAME FROM ROLES WHERE ROL_ID = ?;";
		$res = $db->query($core,$stmnt,$roleId);
		$set = $db->fetchArray($res);
		$role = new Role();
		$role->setId($set["ROL_ID"]);
		$role->setName($set["ROL_NAME"]);
		return $role;
	}
	
}
