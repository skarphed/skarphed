<?php
namespace scv;

include_once 'core.php';

class RightsException extends \Exception{}

class Role {
	private $roleId = null;
	private $roleName = "";
	
	/**
	 * Get the role Id
	 * 
	 * Returns the Role ID of this Role
	 * 
	 * @return int Role ID
	 */
	public function getId(){
		return $this->roleId;
	}
	
	/**
	 * Get the Name
	 * 
	 * Returns the Name of this Role
	 * 
	 * @return string Rolename
	 */
	public function getName(){
		return $this->roleName;
	}
	
	/**
	 * Set the ID
	 * 
	 * Sets the id of this role by a given integer
	 * 
	 * @param int $roleId New role ID
	 */
	public function setId($roleId){
		$this->roleId = (int)$roleId;
	}
	
	
	/**
	 * Set the name
	 * 
	 * Sets the name of the role by a given string
	 * 
	 * @param string $roleName New rolename
	 */
	public function setName($roleName){
		if ($roleName != null and is_string($roleName)){
			$this->roleName = $roleName;
			return true;
		}
		return false;
	}
	
	/**
	 * Store the Role
	 * 
	 * Store the current state of the Role to the Database
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
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
		
		if (!$checkRight or $rightM->checkRight('scoville.roles.create', $userM->getSessionUser())){
			$stmnt = "UPDATE OR INSERT INTO ROLES (ROL_ID, ROL_NAME) VALUES (?,?) MATCHING (ROL_ID); ";
			$db->query($core,$stmnt, array($this->roleId, $this->roleName));
		}
		return;
	}
	
	/**
	 * Adding a Right
	 * 
	 * Adds a right to be linked to this role
	 * With permissioncheck, The sessionuser must have 'scoville.roles.modify' and have the right he wants to add himself
	 * 
	 * @param string $rightId The name of the right to be added
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
	public function addRight($rightId, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();		
		
		if (!$checkRight or $rightM->checkRight('scoville.roles.modify',$userM->getSessionUser())){
			if ($checkRight and !$rightM->checkRight($rightId,$userM->getSessionUser())){
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
	
	/**
	 * Remove a right
	 * 
	 * Removes the given right from the role.
	 * The sessionuser must have the right he wants to remove, along with 'scoville.roles.modify'
	 * 
	 * @param string rightId The right to remove
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
	public function removeRight($rightId, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
		
		$checkString="";
		if ($checkRight){
			$checkstring = " AND 1 = (SELECT AVAILABLE FROM CHECK_RIGHT(". $userM->getSessionUserId().",'scoville.roles.modify')) ";
		}
		
		if ($checkRight and !$rightM->checkRight($rightId,$userM->getSessionUser())){
				throw new RightsException("Remove Right: User Cannot edit a Roleright that he does not possess himself!");
		}
		
		$stmnt = "DELETE FROM ROLERIGHTS WHERE RRI_ROL_ID = ? AND RRI_RIG_ID = (SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME = ?) $checkString ; ";
		$db->query($core,$stmnt, array($this->roleId,$rightId));
		return;
	}
	
	/**
	 * Get Rights of Role
	 * 
	 * Returns the rights of this role in a string-array
	 * With checkrights on , the sessionUser must have 'scoville.roles.modify'
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 * @return Array an array with strings of the rightnames
	 */
	public function getRights($checkRight = true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		
		$checkstring="";
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
	
	/**
	 * Simple Right-Check
	 * 
	 * Returns true if the role has the given right, false if not
	 * 
	 * @param string $right A right string identifier
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 * @return bool has right (TRUE); does not have right (FALSE) 
	 */
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
		while ($set = $db->fetchArray($res)){
			return true;
		}
		return false;
	}
	
	/**
	 * Get grantable rights 
	 * 
	 * Gets the Rights that are available to grant to this role
	 * Returns them in a Array as json-like objects with the current state of assignment
	 * Redirects to RightsManager::getGrantableRights($object)
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 * @return Array Rights as associative arrays with their current state
	 */
	public function getGrantableRights($checkRight = true){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		$rightArray = $rightM->getGrantableRights($this);
		return $rightArray; 
	}
	
	/**
	 * Delete role
	 * 
	 * Deletes this Role from the database
	 * The sessionUser must have the right 'scoville.roles.delete'
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
	public function delete($checkRight=true){
		$core=Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		
		$checkString="";
		if ($checkRight){
			$checkstring = " AND 1 = (SELECT AVAILABLE FROM CHECK_RIGHT(". $userM->getSessionUserId().",'scoville.roles.delete')) ";
		}
		
		//USERROLES und ROLERIGHTS DURCH FOREIGN-KEY BERUECKSICHTIGT!
		
		$stmntRole = "DELETE FROM ROLES WHERE ROL_ID = ? $checkString ;";
		$db->query($core,$stmntRole, array($this->roleId));
	}
	
	/**
	 * Assign a role to a User
	 * 
	 * Assigns this role to a user given as parameter
	 * if checkRight is on:
	 *   sessionUser must have 'scoville.users.grant_revoke
	 *   sessionUser must have all rights, that this role is linked to
	 * 
	 * @param User $user The user that this role shall be assigned to
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
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
	
	/**
	 * Revoke Role From User
	 * 
	 * Revokes a Role from a User
	 * If checkRight is on, the user must have 'scoville.users.grant_revoke'
	 * 
	 * @param User $user The user this role shall be revoked from
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
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
	
	/**
	 * Get Singleton Instance
	 * 
	 * Returns the singleton Instance of the Rightsmanager
	 * 
	 * @return RightsManager The rights manager
	 */
	public static function getInstance(){
		if (RightsManager::$instance==null){
			RightsManager::$instance = new RightsManager();
			RightsManager::$instance->init();
		}
		return RightsManager::$instance;
	}
	
	protected function init(){}
	
	/**
	 * Check right of User
	 * 
	 * Returns TRUE if the right is assigned to the user by a given Role or a given Right
	 * Returns FALSE if not
	 * 
	 * @param string $right A string right identifier
	 * @param User $user The user to be checked
	 * @return bool If assigned: TRUE, if not assigned: FALSE
	 */
	public function checkRight($right,$user){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT AVAILABLE FROM CHECK_RIGHT(? , ?);";
		$res = $db->query($core,$stmnt,array($user->getId(),$right));
		$set = $db->fetchArray($res);
	    if($set['AVAILABLE'] == 1){
			return true;
		}
		return false; 
	}
	
	/**
	 * Create a right
	 * 
	 * Creates a new right in the Databse by given a new rightname and the modulename, the right belongs to
	 * 
	 * @param string $right The name of the new right
	 * @param string $moduleId The name of the module, the right belongs to 
	 */
	public function createRight($right, $moduleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$newRightId = $db->getSeqNext("RIG_GEN");
		$stmnt = "INSERT INTO RIGHTS (RIG_ID, RIG_NAME) VALUES (?,?);";
		$db->query($core, $stmnt, array($newRightId,$moduleId.".".$right));
		return;
	}
	
	/**
	 * Remove a right
	 * 
	 * Deletes a right from the database by the rights name and the name of the module it belongs to
	 * 
	 * @param string $right The name of the right
	 * @param string $moduleId The name of the module, the right belongs to
	 */
	public function removeRight($right, $moduleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "DELETE FROM RIGHTS WHERE RIG_NAME = ?;";
		$db->query($core, $stmnt, array($moduleId.".".$right));
		return;
	}
	
	/**
	 * Get Rights for User
	 * 
	 * Returns the rights that are assigned to a user by it's roles and rights as an Array of strings
	 * 
	 * @param User $user The user whose roles are to be returned
	 * @return Array An array of rightidentifier strings
	 */
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
	
	/**
	 * Get grantable rights
	 * 
	 * Gets the rights that are assignable to either a User or a Role
	 * The function basically delivers all rights that are assigned to the sessionUser and whether 
	 * the user to be edited has them granted or not.
	 * The return values are associative arrays that look like this:
	 * array('right'=>$sessionRight,'granted'=>true)
	 * 
	 * @param Object $object either a role or a user who is to be checked
	 * @return Array an Array of associative arrays as described above
	 */
	public function getGrantableRights($object){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();
		$sessionRights = $this->getRightsForUser($sessionUser);
		
		$result = array();
		$resrights = array();
		$skiprights = array();
		
		switch(get_class($object)){
			case 'scv\User':
				$stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN USERRIGHTS ON (RIG_ID = URI_RIG_ID) WHERE URI_USR_ID = ? ;";
				$stmnt2 = "SELECT RIG_NAME FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) INNER JOIN USERROLES ON (URO_ROL_ID = RRI_ROL_ID) WHERE URO_USR_ID = ?; ";
				$res = $db->query($core,$stmnt,array($object->getId()));
				$res2 = $db->query($core,$stmnt2,array($object->getId())); 
				break;
			case 'scv\Role':
				$stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) WHERE RRI_ROL_ID = ? ;";
				$res = $db->query($core,$stmnt,array($object->getId()));
				break;
			default:
				throw new RightsException("Cannot get grantable Rights from Class: ".get_class($object));//TODO: Here be dragons. Injection von Klassennamen ueber Module	
		}

		
		while($set = $db->fetchArray($res)){
		    $resrights[] = $set['RIG_NAME'];
		}
		
		if (isset($res2)){
			while($set = $db->fetchArray($res2)){
		    	$skiprights[] = $set['RIG_NAME'];
			}
		}
		
		
		foreach ($sessionRights as $sessionRight){
			if (in_array($sessionRight,$skiprights)){
				continue;
			}
			if (in_array($sessionRight,$resrights)){
				$result[] = array('right'=>$sessionRight,'granted'=>true);		
			}else{
				$result[] = array('right'=>$sessionRight,'granted'=>false);
			}
		}
		return $result;
	}
    
	/**
	 * Get grantable roles of User
	 * 
	 * Returns the Roles that can be granted to a User
	 * Basically returns all the roles that the sessionUser Owns and the ones that can be made up by the rights of 
	 * the sessionUser as associative arrays in this style:
	 * array('name'=>$role->getName(),'id'=>$role->getId(),'granted'=>true)
	 * 
	 * @param User $user The user that is to be checked
	 * @return Array Array of associative arrays like described above 
	 */
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
			$rolerights = $role->getRights();  //TODO Check this algorithm again.
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
	
	/**
	 * User has Role
	 * 
	 * Checks if a User has a role, specified by given user and role objects
	 * 
	 * @param Role $role The role for which Rightmanager should look
	 * @param User $user The user to check
	 * @return bool TRUE if user has role, FALSE if user does not have Role
	 */
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
	
	/**
	 * Get Id for Right
	 * 
	 * Returns the database Id for a given right string identifier
	 * 
	 * @param string $right The right that's id should be seeked
	 * @return int The id of the given right string identifier
	 */
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
	
	/**
	 * get all Roles
	 * 
	 * Returns all roles as an array of Objects
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 * @return Array an array of role objects
	 */
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
	
	/**
	 * get roles for User
	 * 
	 * Returns all roles that are assigned to a given user as Array of role objects
	 * 
	 * @param User $user The user that roles are to be given
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 * @return Array an array of role objects
	 */
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
	
	/**
	 * Get Role
	 * 
	 * Get a role from the database by a given roleId. returns a role object
	 * 
	 * @param int $roleId The roles roleID
	 * @return Role a role object
	 */
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
	
	/**
	 * create a new role
	 * 
	 * Creates a new role in the database by given data in the following form:
	 * {'name':string, 'rights':[{'name':string,'granted':bool},{'name',string,'granted':bool},...]}
	 * if checkright is on, the user has to have 'scoville.roles.create' and every right, he wants to add to the role
	 * 
	 * @param Array $data The data the role should be built on
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 * @return Role The created Role
	 * 
	 */
	public function createRole($data,$checkRight=true){
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
		
		if($checkRight) {
			if (!$rightM->checkRight('scoville.roles.create', $userM->getSessionUser())){
				throw new RightsException("Create Role: User is not permitted to create roles");
			}
		}
		
		$id = $db->getSeqNext('ROL_GEN');
		$role = new Role();
		$role->setId($id);
		$role->setName($data->name);
		$role->store($checkRight);
			
		if (isset($data->rights)){
			foreach ($data->rights as $right){
				if ($right->granted){
					$role->addRight($right->name,$checkRight);
				}else{
					$role->removeRight($right->name,$checkRight);
				}
			}
			$role->store($checkRight);
		}
		return $role;
		
		
		
	}
}
?>
