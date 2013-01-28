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
require_once 'core.php';



class UserException extends Exception{}

class User {
	const SALT = 'ooj1nahMeeP4bohzJa2ied6eeir1IchijeyeiSh6zeG5TaiEang6peeiu0ohZie2';
	private $id = null;
	private $name = null;
	private $password = null;
	private $salt = null;
	
	/** 
	 * Sets The User's Id Attribute to an integer value
	 * 
	 * @param int $id The new Id
	 */
	public function setId($id){
		$this->id = (int)$id;
	}
	
	/** 
	 * Sets The User's Name Attribute to a string value
	 *  
	 * @param string $name The new Username
	 */
	public function setName($name){
		$this->name = (string)$name;
	}
	
	/** 
	 * Sets The User's Password to an string value 
	 * 
	 * Only to be used internally! To change the password use User::alterPassword()!
	 * The password is a sha512 hash
	 * 
	 * @param int $pwd The new Passwordhash
	 */
	public function setPassword($pwd){
		$this->password = (string)$pwd;
	}
	
	/** 
	 * Check Right 
	 * 
	 * Checks if a permission is assigned to this User
	 * 
	 * @param int $pwd The new Passwordhash
	 */

	public function checkRight($right){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		return $rightM->checkRight($right,$this->getId());
	}

	public function setSalt($salt){
		$this->salt = (string)$salt;
	}
	
	/**
	 * Alters the User's password. 
	 * 
	 * Must be given the old password. To create a password for a new user set the $newuser flag!
	 * 
	 * @param string $newpassword The new Password
	 */
	public function alterPassword($newpassword,$oldpassword,$newuser=false){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		if ((hash('sha512',$oldpassword.$this->salt) == $this->password) xor $newuser){
			$this->generateNewSalt();
			$this->password = hash('sha512',$newpassword.$this->salt);
			$this->store();
			$passwordqry = "SELECT USR_PASSWORD FROM USERS WHERE USR_ID = ?";
			$res = $db->query($core,$passwordqry,array($this->id));
			$set = $db->fetchObject($res);
			if ($this->password != $set->USR_PASSWORD){
				throw new UserException("Could not set Password: Some Error in Database");
			}
		}else{
			throw new UserException("Could not set Password: Old password is wrong");
		}
	}
	
	private function generateNewSalt(){
		$chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*?";
        $newSalt = "";
        $len = mt_rand(64,127);
        for ( $i = 0; $i < $len ; $i++ ) {
            $newSalt .= $characterList{mt_rand(0, (strlen($characterList) - 1))};
        }
        $this->setSalt($newSalt);
	}

	/**
	 * Get the Users current Name
	 * 
	 * @return string The users name
	 */
	public function getName(){
		return $this->name;
	}
	
	/**
	 * Get the users Id
	 * 
	 * @return int The users id
	 */
	public function getId(){
		return $this->id;
	}
	
	/**
	 * Authenticate the user
	 * 
	 * @param string $password The users plaitext password
	 * @return bool True if authentication successful
	 */
	public function authenticate($password){
		$core = Core::getInstance();
		if (hash('sha512',$password.$this->salt) == $this->password){
			return true;
		}
		return false;
	} 
	
	/**
	 * Delete the user
	 * 
	 * Checks for Permission to delete a user. If given, deletes the User in database and his Userroles and Userrights entries
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use) 
	 */
	public function delete($checkRight=true){
		$core = Core::getInstance();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();
		$db = $core->getDB();

		if ($checkRight and !$sessionUser->checkRight('scoville.users.delete')){
			throw new UserException("delete: Sessionuser is not allowed to delete users!");
		}
		
		$stmnt_usr="DELETE FROM USERS WHERE USR_ID = ? ;";
		$stmnt_uro="DELETE FROM USERROLES WHERE URO_USR_ID = ? ;";
		$stmnt_uri="DELETE FROM USERRIGHTS WHERE URI_USR_ID = ? ;";
		$res = $db->query($core,$stmnt_uri,array($this->getId()));
		$res = $db->query($core,$stmnt_uro,array($this->getId()));
		$res = $db->query($core,$stmnt_usr,array($this->getId()));
		return;
	}
	
	/**
	 * Store the user
	 * 
	 * Stores the current state of the User-object into the database. If the user has no Id, it will assign one and write this to User::id
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use) 
	 */
	public function store( $checkRight = true){
		$core = Core::getInstance();
		$db = $core->getDB();
		if ($this->id == null){
			$query = "INSERT INTO USERS (USR_ID, USR_NAME, USR_PASSWORD, USR_SALT)
			          VALUES (?,?,?,?);";
		    $this->setId($db->getSeqNext('USR_GEN'));
		    $db->query($core,$query,array($this->id,$this->name,$this->password,$this->salt));
		}else{
			$query = "UPDATE USERS SET 
						USR_NAME = ?,
						USR_PASSWORD = ?,
						USR_SALT = ?
					  WHERE USR_ID = ?";
					  
		    $db->query($core,$query,array($this->name,$this->password,$this->id, $this->salt));
			if (ibase_errmsg() != false){
				throw new UserException("Storing User: Something went wrong in the Database");
			} 
		}
	}
	
	/**
	 * Simple role check
	 * 
	 * Checks if the user is assigned a given Role.
	 * 
	 * @param Role $role The role-object to check for
	 * @return bool True if role is asigned to the user 
	 */
	public function hasRole($role){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		return $rightM->hasRoleUser($role,$this);
	}
	
	/**
	 * Get Rights, that are assigned to the user
	 * 
	 * Returns a string-array of rightnames, that are linked with the user
	 * 
	 * @return Array The assigned Rights
	 */
	public function getRights(){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		return $rightM->getRightsForUser($this);
	}
	
	/**
	 * Get Roles, that are assigned to the User
	 * 
	 * Returns an array of Role-objects that are linked with the user
	 * 
	 * @return Array The assignes Roles
	 */
	public function getRoles(){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		return $rightM->getRolesForUser($this);
	}	
	
	/**
	 * Grant a right to the user
	 * 
	 * Grants a given right to the user. If Permssioncheck is on, the current sessionuser has to possess the right himself or have a role that contains that right.
	 * He must have the right 'scoville.users.grant_revoke'
	 * 
	 * @param string $right The right to assign
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
	public function grantRight($right, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();
		if ($checkRight){
	        if (!$rightM->checkRight('scoville.users.grant_revoke', $sessionUser)){
	        	throw new UserException("Granting Right: This user is not allowed to grant rights!");
	        }
		} 
		$rightId = $rightM->getIdForRight($right);
		if ($rightId == null){
			throw new UserException("Granting Right: There is no such right as $right");
		}
		if ($rightId != null){
			if($checkRight and !$rightM->checkRight($right,$sessionUser)){
				return;
			}
			$db->query($core,"UPDATE OR INSERT INTO USERRIGHTS VALUES (?,?) MATCHING (URI_USR_ID,URI_RIG_ID) ;",array($this->id, $rightId));
			if (ibase_errmsg() != false){
				throw new UserException("Granting Right: Something went wrong in the Database");
			} 
		}
	}
	
	/**
	 * Revoke right from User
	 * 
	 * Revokes a given right from the user. If permissioncheck is on, the sessionuser has to have the right himself. He cannot revoke his own rights.
	 * He must have the right 'scoville.users.grant_revoke' 
	 * 
	 * @param string $right The right to revoke
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
	public function revokeRight($right, $checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$rightM = $core->getRightsManager();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();
		$checkstring = "";

		if ($checkRight and !$rightM->checkRight('scoville.users.grant_revoke', $sessionUser){
			throw new UserException("Revoking Right: This Sessionuser is not allowed to grant or revoke Permissions!" );
		}

		$rightId = $rightM->getIdForRight($right);
		if ($rightId == null){
			throw new UserException("Revoking Right: There is no such right as $right");
		}
		if ($checkRight and $sessionUser and $sessionUser->getId() == $this->getId()){
			throw new UserException("Revoking Right: You cannot revoke your own rights");
		}
		if ($rightId != null){
			if($checkRight and !$rightM->checkRight($right,$sessionUser)){
				return;
			} 
			$db->query($core,"DELETE FROM USERRIGHTS WHERE URI_USR_ID = ? AND URI_RIG_ID = ? ;",array($this->id, $rightId));
			if (ibase_errmsg() != false){
				throw new UserException("Revoking Right: Something went wrong in the Database");
			} 
		}
	}
	
	/**
	 * Get grantable rights
	 * 
	 * Get The rights, that are assignable to the User By the current sessionUser
	 * 
	 * @return Array A String-array of rights
	 */
	public function getGrantableRights(){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		$rightArray = $rightM->getGrantableRights($this);
		return $rightArray; 
	}
	
	/**
	 * Get Grantable Roles
	 * 
	 * Get the roles that are assignable to the User by the current sessionUser
	 * 
	 * @return Array An array of Roles represented as array {'name':string, 'granted':bool,'id':int  }
	 */	
	public function getGrantableRoles(){
		$core = Core::getInstance();
		$rightM = $core->getRightsManager();
		$roleArray = $rightM->getGrantableRoles($this);
		return $roleArray;
	}
	
	/**
	 * Assign Role
	 * 
	 * Assign a role to the user. Redirects to Role->assignTo
	 * 
	 * @param Role $role The role-object to assign
	 */
	public function assignRole($role,$checkRight=true){
		return $role->assignTo($this,$checkRight);
	}
	
	/**
	 * Revoke Role
	 * 
	 * Revoke a role  from the user. Redirects to Role->revokeFrom
	 * 
	 * @param Role $role The role-object to revoke
	 */
	public function revokeRole($role,$checkRight=true){
		return $role->revokeFrom($this,$checkRight);
	}
}

class UserManager extends Singleton {
	private static $instance = null;
	
	/**
	 * Get Instance of UserManager
	 * 
	 * Get the Singleton Instance of UserManager
	 * 
	 * @return UserManager the user manager
	 */
	public static function getInstance(){
		if (UserManager::$instance==null){
			UserManager::$instance = new UserManager();
			UserManager::$instance->init();
		}
		return UserManager::$instance;
	}
	
	protected function init(){}
	
	/**
	 * Get current Session user
	 * 
	 * Return the user, that is affiliated with the current Session
	 * 
	 * @return User The current session User
	 */
	public function getSessionUser(){
		if(isset($_SESSION['user'])){
			return $_SESSION['user'];
		}else{return null;}
	}

	/**
	 * Get Id of current Session user
	 * 
	 * Return the id of the User, that is affiliated with the current Session
	 * 
	 * @return int the current session users ID
	 */
	public function getSessionUserId(){
		if(isset($_SESSION['user']) and $_SESSION['user'] != null){
			return $_SESSION['user']->getId();
		}else{return -1;}
	}
	
	/**
	 * Get User by name
	 * 
	 * Returns A userobject of the USer with the given name. OTherwise throws an exception
	 * 
	 * @param string $username The name of the user
	 * @return User The user-object
	 */
	public function getUserByName($username){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$res = $db->query($core,"SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS WHERE USR_NAME= ? ;",array($username));
		$userset = $db->fetchObject($res);
		
		if(!$userset){
			throw new UserException("No User with Name $username");
		}
		
		$user = new User();
		$user->setId($userset->USR_ID);
		$user->setName($userset->USR_NAME);
		$user->setPassword($userset->USR_PASSWORD);
		$user->setSalt($userset->USR_SALT);
		return $user;
	}
	
	/**
	 * Get User by ID
	 * 
	 * Returns a userobject of the User with the given ID. Otherwise throws an exception
	 * 
	 * @param int $userId the Users ID
	 * @return User the returned User object
	 */
	public function getUserById($userId){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$res = $db->query($core,"SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS WHERE USR_ID= ? ;",array($userId));
		$userset = $db->fetchObject($res);
		
		if(!$userset){
			throw new UserException("No User with Id $userId");
		}
		
		$user = new User();
		$user->setId($userset->USR_ID);
		$user->setName($userset->USR_NAME);
		$user->setPassword($userset->USR_PASSWORD);
		$user->setSalt($userset->USR_SALT);
		return $user;
	}
	
	
	/**
	 * Get Users
	 * 
	 * Returns All users in an array. check right checks for 'scoville.users.view'
	 * 
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 * @return Array an array of User-Objects 
	 */
	public function getUsers($checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();

		if ($checkRight and !$sessionUser->checkRight('scoville.users.view'){
			throw new UserException("getUsers: This user is not allowed to view users!");
		}
		$res = $db->query($core,"SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS ;",array());
		$users = array();
		while($userset = $db->fetchObject($res)){
		    $user = new User();
			$user->setId($userset->USR_ID);
			$user->setName($userset->USR_NAME);
			$user->setPassword($userset->USR_PASSWORD);
			$user->setSalt($userset->USR_SALT);
			$users[] = $user;
		}
		
		return $users;
	}
	
	/**
	 * Create User
	 * 
	 * Creates a user of the given Data.
	 * 
	 * @param string $username The name of the user that is created
	 * @param string $password The plaintext password of the new user
	 * @param json $userinfo Not implemented yet
	 * @param bool $checkRight Set false to omit permissionchecks (testing and internal use)
	 */
	public function createUser($username, $password, $userinfo, $checkRight=true){
		$user = new User();
		$user->setName($username);
		$user->setPassword("");
		$user->store();
		$user->alterPassword($password, "", true);
		return true;
	}
	
	/**
	 * Get Users for admin Interface
	 * 
	 * Returns getUsers() in a json-like structure
	 * 
	 * @return json userlist
	 */
	public function getUsersForAdminInterface(){
		$users = $this->getUsers();
		$ret = array();
		foreach ($users as $user){
			$element = array("name"=>$user->getName(),"id"=>$user->getId());
			$ret[]=$element;
		}
		return $ret;
	}
}
?>
