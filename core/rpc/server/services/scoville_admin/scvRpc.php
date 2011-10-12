<?php
require_once ("../lib/core.php");


class class_scvRpc {


	
  function method_test($params, $error)	{
  	$core = scv\Core::getInstance();
	$db = $core->getDB();
	$dbip = $core->getConfig()->getEntry('db.ip');
	
  	
  	return "HALLO WELT: $dbip";
  }
  
  function method_getServerInfo($params,$error){
  	$core = scv\Core::getInstance();
	  
	return $core->getConfig()->getEntry('core.name');
  }
  
  function method_getServerUsers($params,$error){
  	$core = scv\Core::getInstance();
	return "test";
  }
  
  function method_authenticateUser($params,$error){
  	$core = scv\Core::getInstance();
	$username = $params[0];
	$password = $params[1];
	
	$usermanager = $core->getUserManager();
	$user = $usermanager->getUserByName($username);
	if($user->authenticate($password)){
		$_SESSION['loggedin'] = "true";
		$_SESSION['user'] = $user;
		
		//Send the user the rights he has
		$rightM = $core->getRightsManager();	
	    $rights = $rightM->getRightsForUser($user);
	    return $rights;
	}else{
		session_destroy();
		return false;
	}
	
  }/*TEST*/

  function method_getUsers($params,$error){
  	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$userM = $core->getUserManager();
	$users = $userM->getUsersForAdminInterface();
	return $users;
	
  }
  
  function method_createUser($params,$error){
  	$username = $params[0];
	$password = $params[1];
  	$core = scv\Core::getInstance();
	$userM = $core->getUserManager();
	$userM->createUser($username,$password,null);
	return true;
  }
  
  function method_getRightlistGranted($params,$error){
  	
  }
}
?>