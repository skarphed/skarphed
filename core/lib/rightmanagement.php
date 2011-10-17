<?php
namespace scv;

include_once 'core.php';

class RightsException extends \Exception{}

class Role {
	private $roleId = null;
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
		if ($roleName != null and is_string($roleName)){
			$this->roleName = $roleName;
			return true;
		}
		return false;
	}
	
	public function store($checkRight=true){
		$core=Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
	    
		if ($this->roleId == null){
			throw new RightsException("Create Role: Can't save a role without Id");	
		}
		if ($this->roleName == ""){
			throw new RightsException("Create Role: Can't save a role without a Name");
		}
		
		if ($rightM->checkRight('scoville.roles.create', $userM->getSessionUser()) or !$checkRight){
			$stmnt = "UPDATE OR INSERT INTO ROLES (ROL_ID, ROL_NAME) VALUES (?,?) MATCHING (ROL_ID); ";
			$db->query($core,$stmnt, array($this->roleId, $this->roleName));
		}
		return;
	}
	
	public function addRight($rightId, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();		
		
		if ($rightM->checkRight('scoville.roles.modify',$userM->getSessionUser()) or !$checkRight){
			if (!$rightM->checkRight($rightId,$userM->getSessionUser())){
				throw new RightsException("Add Right: User Cannot edit a Roleright that he does not possess himself!");
			}
			$stmnt = "UPDATE OR INSERT INTO ROLERIGHTS (RRI_ROL_ID, RRI_RIG_ID) 
		    	        VALUES (?, (SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME= ?)) 
		        	  MATCHING (RRI_ROL_ID, RRI_RIG_ID);";
			$db->query($core, $stmnt, array($this->roleId, $rightId));	
		}else{
			throw new RightsException("Add Right: You are not Allowed to modify Roles");
		}
		return;
	}
	
	public function removeRight($rightId, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
		
		$checkString="";
		if ($checkRight){
			$checkstring = " AND 1 = (SELECT AVAILABLE FROM CHECK_RIGHT(". $userM->getSessionUserId().",'scoville.roles.modify')) ";
		}
		
		if (!$rightM->checkRight($rightId,$userM->getSessionUser())){
				throw new RightsException("Remove Right: User Cannot edit a Roleright that he does not possess himself!");
		}
		
		$stmnt = "DELETE FROM ROLERIGHTS WHERE RRI_ROL_ID = ? AND RRI_RIG_ID = (SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME = ?) $checkString ; ";
		$db->query($core,$stmnt, array($this->roleId,$rightId));
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
        $res = $db->query($core, $stmnt, array($this->roleId));
		$ret = array();
		while ($set = $db->fetchArray($res)){
			$ret[] = $set["RIG_NAME"];  
		}
		return $ret;
	}
	
	public function hasRight($right, $checkRight = true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		$rightM = $core->getRightsManager();
		
		if (!$rightM->checkRight('scoville.roles.modify', $userM->getSessionUser()) and $checkRight){
			throw new RightsException("hasRight: Not allowed To do that!");
		}
		
		$stmnt = "SELECT RIG_ID FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) 
		            WHERE RRI_ROL_ID = ? AND RIG_NAME = ?;";
        $res = $db->query($core, $stmnt, array($this->roleId, $right));
		$ret = array();
		while ($set = $db->fetchArray($res)){
			return true;
		}
		return false;
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
		
		//USERROLES und ROLERIGHTS DURCH FOREIGN-KEY BERUECKSICHTIGT!
		
		$stmntRole = "DELETE FROM ROLES WHERE ROL_ID = ? $checkString ;";
		$db->query($core,$stmntRole, array($this->roleId));
	}
	
	public function assignTo($user, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		if (!$checkRight){
			$stmnt = "UPDATE OR INSERT INTO USERROLES (URO_USR_ID, URO_ROL_ID) VALUES (?,?) MATCHING (URO_USR_ID, URO_ROL_ID) ;";
			$db->query($core,$stmnt,array($user->getId(),$this->roleId));
			return;
		}
		
		$userM = $core->getUserManager();
		$rightM = $core->getRightsManager();
		if(!$rightM->checkRight('scoville.users.grant_revoke', $userM->getSessionUser())){
			throw RightsException("Grant Role: This user is not allowed to grant Roles");
		}
		
		$grantableRoles = $user->getGrantableRoles();
		foreach ($grantableRoles as $gRole){
			if ($gRole['name'] == $this->roleName){
		 		$stmnt = "UPDATE OR INSERT INTO USERROLES (URO_USR_ID, URO_ROL_ID) VALUES (?,?) MATCHING (URO_USR_ID, URO_ROL_ID) ;";
				$db->query($core,$stmnt,array($user->getId(),$this->roleId));
				return;
			}
		}
		throw new RightsException("Grant Role: You can only allow Roles you possess yourself OR roles, that can be made up of the rights you own.");
	}
	
	public function revokeFrom($user, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		if (!$checkRight){
			$stmnt= "DELETE FROM USERROLES WHERE URO_USR_ID = ? AND URO_ROL_ID = ? ;";
			$db->query($core,$stmnt,array($user->getId(),$this->roleId));
			return;
		}
		
		$userM = $core->getUserManager();
		$rightM = $core->getRightsManager();
		if(!$rightM->checkRight('scoville.users.grant_revoke', $userM->getSessionUser())){
			throw RightsException("Grant Role: This user is not allowed to grant Roles");
		}
		$stmnt= "DELETE FROM USERROLES WHERE URO_USR_ID = ? AND URO_ROL_ID = ? ;";
		$db->query($core,$stmnt,array($user->getId(),$this->roleId));
		return;
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
			case 'scv\User':
				$stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN USERRIGHTS ON (RIG_ID = URI_RIG_ID) WHERE URI_USR_ID = ? 
				            AND RIG_ID NOT IN (SELECT RRI_RIG_ID FROM ROLERIGHTS INNER JOIN USERROLES ON (RRI_ROL_ID = URO_ROL_ID) WHERE URO_USR_ID = ?) ;";
				$res = $db->query($core,$stmnt,array($object->getId(),$object->getId()));
				break;
			case 'scv\Role':
				$stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) WHERE RRI_ROL_ID = ? ;";
				$res = $db->query($core,$stmnt,array($object->getId()));
				break;
			default:
				throw new RightsException("Cannot get grantable Rights from Class: ".get_class($object));//TODO: Here be dragons. Injection von Klassennamen ueber Module	
		}
		
		//TODO: Here be dragons (Performance leak)
		
		$resrights = array();
		$failrights = array();
		
		if (get_class($object) == 'scv\User'){
			$roles = $sessionUser->getRoles();
			while($set = $db->fetchArray($res)){
				foreach($roles as $role){
					if ($role->hasRight($set['RIG_NAME'])){
						$failrights[] = $set['RIG_NAME'];
						continue 2;
					}
				}
				$resrights[] = $set['RIG_NAME'];
				
			}
		}
		else{
			
			while($set = $db->fetchArray($res)){
				$resrights[] = $set['RIG_NAME'];
			}
		}
		
		
		
		$result = array();
		foreach ($sessionRights as $sessionRight){
			if (in_array($sessionRight,$resrights)){
				$result[] = array('right'=>$sessionRight,'granted'=>true);
			}elseif (in_array($sessionRight,$failrights)){
				
			}else{
				$result[] = array('right'=>$sessionRight,'granted'=>false);
			}
		}
		return $result;
	}

    public function getGrantableRoles($user){
    	$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();
		$sessionRights = $this->getRightsForUser($sessionUser);
		
		$ret = array();
		
		$roles = $this->getRoles();
		foreach ($roles as $role){
			if ($sessionUser->hasRole($role)){
				if ($user->hasRole($role)){
					$ret[] = array('name'=>$role->getName(),'id'=>$role->getId(),'granted'=>true); 
				}else{
					$ret[] = array('name'=>$role->getName(),'id'=>$role->getId(),'granted'=>false);
				}
				continue;
			}
			$rolerights = $role->getRights();
			foreach ($rolerights as $roleright){
				if(!in_array($roleright,$sessionRights)){
					continue 2;
				}
				if ($user->hasRole($role)){
					$ret[] = array('name'=>$role->getName(),'id'=>$role->getId(),'granted'=>true); 
				}else{
					$ret[] = array('name'=>$role->getName(),'id'=>$role->getId(),'granted'=>false);
				}
				continue 2;
			}
		}
		return $ret;
    }
	
	public function hasRoleUser($role, $user){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$stmnt = "SELECT URO_ROL_ID FROM USERROLES WHERE URO_ROL_ID = ? AND URO_USR_ID = ?;";
		$res = $db->query($core,$stmnt,array($role->getId(),$user->getId()));
		while($set = $db->fetchArray($res)){
			return true;
		}
		return false;
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
	
	public function getRolesForUser($user,$checkRight=false){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT ROL_ID, ROL_NAME FROM ROLES INNER JOIN USERROLES ON (ROL_ID = URO_ROL_ID) WHERE URO_USR_ID = ?;";
		$res = $db->query($core,$stmnt,array($user->getId()));
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
		$res = $db->query($core,$stmnt,array($roleId));
		$set = $db->fetchArray($res);
		$role = new Role();
		$role->setId($set["ROL_ID"]);
		$role->setName($set["ROL_NAME"]);
		return $role;
	}
	
	public function createRole($data){
		if ($data == null){
			throw new RightsException("Create Role: Cannot Create role without roleData");
		}
		if (!isset($data->name)){
			throw new RightsException("Create Role: Cannot Create a role without a name");
		}
		
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
		
		if($rightM->checkRight('scoville.roles.create', $userM->getSessionUser())){
			$id = $db->getSeqNext('ROL_GEN');
			$role = new Role();
			$role->setId($id);
			$role->setName($data->name);
			$role->store();
				
			if (isset($data->rights)){
				foreach ($data->rights as $right){
					if ($right->granted){
						$role->addRight($right->name);
					}else{
						$role->removeRight($right->name);
					}
				}
				$role->store();
			}
			return $role;
			
		}
		throw new RightsException("Create Role: User is not permitted to create roles");
	}
}
?>
