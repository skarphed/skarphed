<?php
namespace scv;

include_once 'core.php';



class UserException extends \Exception{}

class User {
	const SALT = 'ooj1nahMeeP4bohzJa2ied6eeir1IchijeyeiSh6zeG5TaiEang6peeiu0ohZie2';
	private $id = null;
	private $name = null;
	private $password = null;
	
	public function setId($id){
		$this->id = (int)$id;
	}
	
	public function setName($name){
		$this->name = (string)$name;
	}
	
	public function setPassword($pwd){
		$this->password = (string)$pwd;
	}
	
	public function alterPassword($newpassword,$oldpassword,$newuser=false){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		if ((hash('ripemd160',$oldpassword.User::SALT) == $this->password) xor $newuser){
			$this->password = hash('ripemd160',$newpassword.User::SALT);
			$this->store();
			$passwordqry = "SELECT USR_PASSWORD FROM USERS WHERE USR_ID = ?";
			$res = $db->query($core,$passwordqry,array($this->id));
			$set = $db->fetchObject($res);
			if ($this->password != $set->USR_PASSWORD){
				throw new UserException("Could not set Password: Some Error in Database");
			}else{
				$this->password = $newpassword;
			}
		}else{
			throw new UserException("Could not set Password: Old password is wrong");
		}
	}
	
	public function getName(){
		return $this->name;
	}
	
	public function getId(){
		return $this->id;
	}
	
	public function authenticate($password){
		$core = Core::getInstance();
		$core->debugGrindlog(hash('ripemd160',$password.User::SALT)."<-->".$this->password );
		if (hash('ripemd160',$password.User::SALT) == $this->password){
			return true;
		}
		return false;
	}
	
	public function store( $checkRight = true){
		$core = Core::getInstance();
		$db = $core->getDB();
		if ($this->id == null){
			$query = "INSERT INTO USERS (USR_ID, USR_NAME, USR_PASSWORD)
			          VALUES (?,?,?);";
		    $this->setId($db->getSeqNext('USR_GEN'));
		    $db->query($core,$query,array($this->id,$this->name,$this->password));
		}else{
			$query = "UPDATE USERS SET 
						USR_NAME = ?,
						USR_PASSWORD = ?
					  WHERE USR_ID = ?";
					  
		    $db->query($core,$query,array($this->name,$this->password,$this->id));
			if (ibase_errmsg() != false){
				throw new UserException("Storing User: Something went wrong in the Database");
			} 
		}
	}
	
}

class UserManager extends Singleton {
	private static $instance = null;
	
	public static function getInstance(){
		if (UserManager::$instance==null){
			UserManager::$instance = new UserManager();
			UserManager::$instance->init();
		}
		return UserManager::$instance;
	}
	
	protected function init(){}
	
	public function getSessionUser(){
		if(isset($_SESSION['user'])){
			return $_SESSION['user'];
		}else{return null;}
	}
	
	public function getSessionUserId(){
		if(isset($_SESSION['user']) and $_SESSION['user'] != null){
			return $_SESSION['user']->getId();
		}else{return -1;}
	}
	
	public function getUserByName($username){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$res = $db->query($core,"SELECT USR_ID, USR_NAME, USR_PASSWORD FROM USERS WHERE USR_NAME= ? ;",array($username));
		$userset = $db->fetchObject($res);
		
		$user = new User();
		$user->setId($userset->USR_ID);
		$user->setName($userset->USR_NAME);
		$user->setPassword($userset->USR_PASSWORD);
		return $user;
	}
	
	public function getUserById($username){
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$res = $db->query($core,"SELECT USR_ID, USR_NAME, USR_PASSWORD FROM USERS WHERE USR_NAME= ? ;",array($username));
		$userset = $db->fetchObject($res);
		
		$user = new User();
		$user->setId($userset->USR_ID);
		$user->setName($userset->USR_NAME);
		$user->setPassword($userset->USR_PASSWORD);
		return $user;
	}
	
	public function getUsers($checkRight=true){
		$core = Core::getInstance();
		$db = $core->getDB();
		$checkstring = "";
		system($this->getSessionUserId(). ">> GRINDLOG.log");
		if ($checkRight){
			$checkstring = " WHERE 1 = (SELECT AVAILABLE FROM CHECK_RIGHT(". $this->getSessionUserId().",'scoville.users.view')) ";
		}
		$res = $db->query($core,"SELECT USR_ID, USR_NAME, USR_PASSWORD FROM USERS $checkstring ;",array());
		$users = array();
		while($userset = $db->fetchObject($res)){
		    $user = new User();
			$user->setId($userset->USR_ID);
			$user->setName($userset->USR_NAME);
			$user->setPassword($userset->USR_PASSWORD);
			$users[] = $user;
		}
		
		return $users;
	}
	
	public function createUser($username, $password, $userinfo, $checkRight=true){
		$user = new User();
		$user->setName($username);
		$user->setPassword("");
		$user->store();
		$user->alterPassword($password, "", true);
		return true;
	}
	
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
