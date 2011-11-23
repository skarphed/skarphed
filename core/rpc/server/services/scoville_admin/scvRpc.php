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
	try{
		$user = $usermanager->getUserByName($username);
	}catch(scv\UserException $e){
		session_destroy();
		return false;
	}
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
	
  }

  function method_getUsers($params,$error){
  	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$userM = $core->getUserManager();
	$users = $userM->getUsersForAdminInterface();
	return $users;
	
  }
  
  function method_getRoles($params,$error){
  	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$roles = $rightM->getRoles();
	$ret = array();
	foreach ($roles as $role){
		$ret[] = array("id"=>$role->getId(),"name"=>$role->getName());
	}
	return json_encode($ret);
  }
  
  function method_createUser($params,$error){
  	$username = $params[0];
	$password = $params[1];
  	$core = scv\Core::getInstance();
	$userM = $core->getUserManager();
	$userM->createUser($username,$password,null);
	return true;
  }
  
  function method_grantRightToUser($params,$error){
  	$userId = $params[0];
	$rightName = $params[1];
	
	$core = scv\Core::getInstance();
	
	$user = $core->getUserManager()->getUserByName($userId);
	$user->grantRight($rightName);
	return true;
  }
  
  function method_revokeRightFromUser($params, $error){
  	$userId = $params[0];
	$rightName = $params[1];
	
	$core = scv\Core::getInstance();	
	
	$user = $core->getUserManager()->getUserByName($userId);
	$user->revokeRight($rightName);
	return true;  	
  }
  
  function method_getRightsForUserPage($params,$error){
  	$userId = $params[0];
	$core = scv\Core::getInstance();
	$user = $core->getUserManager()->getUserByName($userId);	
	return json_encode($user->getGrantableRights());	
  }
  
  function method_grantRightToRole($params,$error){
  	$roleId = $params[0];
	$rightName = $params[1];
	
	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$role = $rightM->getRole($roleId);
	$role->addRight($rightName);
	//$role->store();
	return;
  }
  
  function method_revokeRightFromRole($params,$error){
  	$roleId = $params[0];
	$rightName = $params[1];
	
	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$role = $rightM->getRole($roleId);
	$role->removeRight($rightName);
	//$role->store();
	return;
  }
  
  function method_getRightsForRolePage($params,$error){
  	$roleId = $params[0];
	$core = scv\Core::getInstance();
	$role = $core->getRightsManager()->getRole($roleId);	
	return json_encode($role->getGrantableRights());	
  }
  
  function method_createRole($params,$error){
  	$data = $params[0];
  	
	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$role = $rightM->createRole($data);
	return $role->getId();
	
  }
  
  function method_deleteRole($params,$error){
  	$roleId = $params[0];
	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$rightM->getRole($roleId)->delete();
  }
  
  function method_getRolesForUserPage($params,$error){
  	$userName = $params[0];
	$core = scv\Core::getInstance();
	$user = $core->getUserManager()->getUserByName($userName);	
	return json_encode($user->getGrantableRoles());
  }
  
  function method_assignRoleToUser($params,$error){
  	$userName = $params[0];
	$roleId = $params[1];
	
	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$role = $rightM->getRole($roleId);
	$core->getUserManager()->getUserByName($userName)->assignRole($role);
	return;
  }
  
  function method_revokeRoleFromUser($params,$error){
  	$userName = $params[0];
	$roleId = $params[1];
	
	$core = scv\Core::getInstance();
	$rightM = $core->getRightsManager();
	$role = $rightM->getRole($roleId);
	$core->getUserManager()->getUserByName($userName)->revokeRole($role);
	return;
  }
  
  function method_getCssPropertySet($params,$error){
  	$moduleId = $params[0];
	$widgetId = $params[1];
	$session =  $params[2];
	
	$core = scv\Core::getInstance();
	$cssM = $core->getCssManager();
	$cssPropertySet = $cssM->getCssPropertySet($moduleId,$widgetId,$session);
	$data = $cssPropertySet->serializeSet();
	return json_encode($data);
  }
  
  function method_setCssPropertySet($params,$error){
  	$data = $params[0];
	
	$core = scv\Core::getInstance();	
	$cssM = $core->getCssManager();
	$cssPropertySet = $cssM->createCssPropertySetFromSerial($data);
	$cssPropertySet->store();
	return;
  }
  
  function method_getModules($params,$error){
  	$getInstalledOnly = $params[0];
	
	$core = scv\Core::getInstance();
	$moduleM = $core->getModuleManager();
	$modules = $moduleM->getModules($getInstalledOnly);
	
	return json_encode($modules);
  }
  
  function method_setRepository($params,$error){
  	$ip = $params[0];
	$port = (int)$params[1];
	
	$core = scv\Core::getInstance();
	$moduleM = $core->getModuleManager();
	foreach ($moduleM->getRepositories() as $repo){
		$repo->delete();
	}
	$moduleM->addRepository($ip,$port,'(default)');
	return;
  }
  
  function method_getRepository($params,$error){
  	$core = scv\Core::getInstance();
	$moduleM = $core->getModuleManager();
	$repos = $moduleM->getRepositories();
	if (count($repos) > 0){
		$repo = $repos[0];
		return json_encode(array('id'=>$repo->getId(),'ip'=>$repo->getIp(),'port'=>$repo->getPort(),'name'=>$repo->getName()));
	}else{
		return null;
	}
  }
  
  function method_uninstallModule($params,$error){
  	$module = $params[0];
	$operationId = $params[1];
	
	$core = scv\Core::getInstance();
	$moduleM = $core->getModuleManager();
	$moduleM->uninstallModuleRemote(null,$module,$operationId);
  	return true;  //TODO:implement
  }
  
  function method_installModule($params,$error){
  	$module = $params[0];
	$operationId = $params[1];
	
	$core = scv\Core::getInstance();
	$moduleM = $core->getModuleManager();
	$modulemeta = array("name"=>$module->name,
						"hrname"=>$module->hrname,
						"version_major"=>$module->version_major,
						"version_minor"=>$module->version_minor,
						"revision"=>$module->revision,
						"md5"=>$module->md5);
	$moduleM->installModuleFromRepository(null, $modulemeta,$operationId);
  	return true;  //TODO:implement
  }
  
  function method_dropOperation($params,$error){
  	$operationId = (int)$params[0];
	
	$core = scv\Core::getInstance();
	$opM = $core->getOperationManager();
	$opM->dropOperation($operationId);
	
  }
  
  function method_retryOperation($params,$error){
  	$operationId = (int)$params[0];
	
	$core = scv\Core::getInstance();
	$opM = $core->getOperationManager();
	$opM->retryOperation($operationId);
  }
  
  function method_cancelOperation($params,$error){
  	$operationId = (int)$params[0];
	
	$core = scv\Core::getInstance();
	$opM = $core->getOperationManager();
	$opM->cancelOperation($operationId);
  }
  
  function method_getOperations($params,$error){
  	$operationtypes = null;
  	if (isset($params[0])){
  		$operationtypes = $params[0];
  	}
	
  	$core = scv\Core::getInstance();
	$opM = $core->getOperationManager();
	$operations = $opM->getCurrentOperationsForGUI($operationtypes);
	
	return $operations;
  }
  
  function method_getSites($params,$error){
  	$core = scv\Core::getInstance();
  	$compositeM = $core->getCompositeManager();	
	
  	return json_encode($compositeM->getSitesMeta());
  }
  
  function method_getSite($params,$error){
  	$siteId = $params[0];
	
	$core = scv\Core::getInstance();
	$compositeM = $core->getCompositeManager();	
	$site = $compositeM->getSite($siteId);
	
	return json_encode($site->getMeta());
  }
  
  function assignWidgetToSpace($params,$error){
  	$siteId = $params[0];
	$space = $params[1];
	$widgetId = $params[2];
	
	$core = scv\Core::getInstance();
	$compositeM = $core->getCompositeManager();	
	$site = $compositeM->getSite($siteId);
	$widget = $compositeM->($widgetId);
	$site->assignWidget($space,$widget);
	return;
  }
  
  function removeWidgetFromSpace($params,$error){
  	$siteId = $params[0];
	$space = $params[1];
	
	$core = scv\Core::getInstance();
	$compositeM = $core->getCompositeManager();
	$site = $compositeM->getSite($siteId);
	$site->removeWidget($space);
	return;
  }
}
?>