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
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

class TestUsersAndRights extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
    	/*try{
		  session_destroy();
		}catch(Exception $e){}*/
        // Array-Fixture erzeugen.
        $this->fixture = Core::getInstance(); 
    }
 
    public function testNameIsRight() {
        // Der erwartete Wert von sizeof($this->fixture) ist 0.
        $this->assertEquals('de.masterprogs.scoville.core', $this->fixture->getName());
    }
 
    public function testNameIsWrong() {
        // Ein Element dem Array hinzufügen
 
        // Der erwartete Wert von sizeof($this->fixture) ist 1.
        $this->assertEquals('de.masterprogs.scoville.core',$this->fixture->getName());
    }
	
	public function testCreateAndDeleteUser(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testCreateAndDeleteUser", "testpassword", null);
		$user = $userM->getUserByName("testCreateAndDeleteUser");
		$this->assertEquals('User', get_class($user));
		$this->assertTrue($user->authenticate("testpassword"));
		$user->delete(false);
		$this->assertTrue(true);
	}
	
	public function testAlterPassword(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testAlterPasswordUser", "testpassword", null);
		$user = $userM->getUserByName("testAlterPasswordUser");
		
		$this->assertFalse($user->authenticate("tochangepassword"));
		$user->alterPassword("tochangepassword", "testpassword");
		$this->assertTrue( $user->authenticate("tochangepassword"));
		$user->alterPassword("testpassword", "tochangepassword");
		$this->assertFalse($user->authenticate("tochangepassword"));
		
		$this->assertEquals('User', get_class($user));
		$this->assertTrue($user->authenticate("testpassword"));
		$user->delete(false);
		$this->assertTrue(true);
		
	}
	
	public function testCannotSetPasswordWithoutOldPasssword(){
		$this->setExpectedException('UserException','Could not set Password: Old password is wrong');
		$userM = $this->fixture->getUserManager();
		$user = $userM->getUserByName("genericTestUser");
		$user->alterPassword("tochangepassword","falsepassword");
	}
	
	public function testGrantAndRevokeRightUserWithoutCheck(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testGrantAndRevokeRightUserWithoutCheckUser", "testpassword", null);
		$user = $userM->getUserByName("testGrantAndRevokeRightUserWithoutCheckUser");
		$this->assertNotContains('scoville.manageserverdata',$user->getRights());
		
		$user->grantRight('scoville.manageserverdata',false);
		$this->assertContains('scoville.manageserverdata',$user->getRights());
		
		$user->revokeRight('scoville.manageserverdata',false);
		$this->assertNotContains('scoville.manageserverdata',$user->getRights());
		
		$user->delete(false);		
	}
	
	public function testGrantAndRevokeRightUserWithCheck_S(){
		
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testGrantAndRevokeRightUserWithCheckUser_S", "testpassword", null);
		$userM->createUser("currentSessionUser","testpassword",null);
		$user = $userM->getUserByName("testGrantAndRevokeRightUserWithCheckUser_S");
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$_SESSION['user']->grantRight('scoville.manageserverdata',false);
		$_SESSION['user']->grantRight('scoville.users.grant_revoke',false);
		
		$this->assertNotContains('scoville.manageserverdata',$user->getRights());
		
		$user->grantRight('scoville.manageserverdata',true);
		$this->assertContains('scoville.manageserverdata',$user->getRights());
		
		$user->revokeRight('scoville.manageserverdata',true);
		$this->assertNotContains('scoville.manageserverdata',$user->getRights());
		
		$user->delete(false);
		$_SESSION['user']->delete(false);		
		unset($_SESSION['user']);
		unset($_SESSION['loggedin']);
	}

    public function testGrantAndRevokeRightUserWithCheck_NotAllowed(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testGrantAndRevokeRightUserWithCheckUser_NotAllowed", "testpassword", null);
		$userM->createUser("currentSessionUser","testpassword",null);
		$user = $userM->getUserByName("testGrantAndRevokeRightUserWithCheckUser_NotAllowed");
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		
		$this->assertNotContains('scoville.manageserverdata',$user->getRights());
		$this->setExpectedException('UserException', 'Granting Right: This user is not allowed to grant rights!');
        try {
			$user->grantRight('scoville.manageserverdata',true);
		}catch(UserException $e){
			$user->delete(false);
			$_SESSION['user']->delete(false);		
			unset($_SESSION['user']);
			unset($_SESSION['loggedin']);
			throw $e;
		}
		$user->delete(false);
		$_SESSION['user']->delete(false);		
		unset($_SESSION['user']);
		unset($_SESSION['loggedin']);
	}
	
	public function testGrantAndRevokeRightUserWithCheck_MissingRight(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testGrantAndRevokeRightUserWithCheckUser_MissingRight", "testpassword", null);
		$userM->createUser("currentSessionUser","testpassword",null);
		$user = $userM->getUserByName("testGrantAndRevokeRightUserWithCheckUser_MissingRight");
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$_SESSION['user']->grantRight('scoville.users.grant_revoke',false);
		
		$this->assertNotContains('scoville.manageserverdata',$user->getRights());
		$user->grantRight('scoville.manageserverdata',true);
		$this->assertNotContains('scoville.manageserverdata',$user->getRights());
		
		$user->delete(false);
		$_SESSION['user']->delete(false);
		unset($_SESSION['user']);		
		unset($_SESSION['loggedin']);
	}
	
	public function testCreateDeleteRoleWithCheck(){
		$roleData = json_decode('{"name":"testCreateDeleteRoleWithCheck"}');
		$rightM = $this->fixture->getRightsManager();
		$role = $rightM->createRole($roleData,false); 
		$this->assertEquals('Role',get_class($role));
		$role->delete(false);
		//TODO: getRole Should return null or throw exception
		
	}
	
	
	public function testGrantAndRevokeRightRoleWithoutCheck(){
		$roleData = json_decode('{"name":"testGrantAndRevokeRightRoleWithoutCheck"}');
		$rightM = $this->fixture->getRightsManager();
		$role = $rightM->createRole($roleData,false); 
		$this->assertNotContains('scoville.manageserverdata',$role->getRights(false));
		$role->addRight('scoville.manageserverdata',false);
		$this->assertContains('scoville.manageserverdata',$role->getRights(false));
		$role->removeRight('scoville.manageserverdata',false);
		$this->assertNotContains('scoville.manageserverdata',$role->getRights(false));
		$role->delete(false);		
	}
	
	public function testGrantAndRevokeRightRoleWithCheck_S(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$_SESSION['user']->grantRight('scoville.manageserverdata',false);
		
		$_SESSION['user']->grantRight('scoville.roles.create',false);
		$_SESSION['user']->grantRight('scoville.roles.modify',false);
		$_SESSION['user']->grantRight('scoville.roles.delete',false);
		
		$roleData = json_decode('{"name":"testGrantAndRevokeRightRoleWithCheck"}');
		$rightM = $this->fixture->getRightsManager();
		$role = $rightM->createRole($roleData); 
		$this->assertNotContains('scoville.manageserverdata',$role->getRights());
		$role->addRight('scoville.manageserverdata');
		$this->assertContains('scoville.manageserverdata',$role->getRights());
		$role->removeRight('scoville.manageserverdata');
		$this->assertNotContains('scoville.manageserverdata',$role->getRights());
		$role->delete();
		
		$_SESSION['user']->delete(false);
		unset($_SESSION['user']);		
		unset($_SESSION['loggedin']);		
	}
	
	public function testGrantAndRevokeRightRoleWithCheck_MissingRight(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$this->setExpectedException('RightsException','Add Right: User Cannot edit a Roleright that he does not possess himself!');
		
		$_SESSION['user']->grantRight('scoville.roles.create',false);
		$_SESSION['user']->grantRight('scoville.roles.modify',false);
		$_SESSION['user']->grantRight('scoville.roles.delete',false);
		
		try{
			$roleData = json_decode('{"name":"testGrantAndRevokeRightRoleWithCheck"}');
			$rightM = $this->fixture->getRightsManager();
			$role = $rightM->createRole($roleData); 
			$this->assertNotContains('scoville.manageserverdata',$role->getRights());
			$role->addRight('scoville.manageserverdata');
			$this->assertContains('scoville.manageserverdata',$role->getRights());
			$role->removeRight('scoville.manageserverdata');
			$this->assertNotContains('scoville.manageserverdata',$role->getRights());
		}catch(RightsException $e){
			$role->delete(false);
			$_SESSION['user']->delete(false);
			unset($_SESSION['user']);		
			unset($_SESSION['loggedin']);	
			throw $e;
		}
		
			
	}
	
	public function testGetGrantableRightsUserWithoutRole(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testGetGrantableRightsUserWithoutRole", "testpassword", null);
		$user = $userM->getUserByName("testGetGrantableRightsUserWithoutRole");
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$_SESSION['user']->grantRight('scoville.users.grant_revoke',false);
		$_SESSION['user']->grantRight('scoville.manageserverdata',false);
		$_SESSION['user']->grantRight('scoville.roles.create',false);
		
		$grantableRights = $user->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == false){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == false){$foundRolesCreate = true;}}
		$this->assertTrue($foundGrantRevoke and $foundRolesCreate and $foundServerData);
		
		$user->grantRight('scoville.roles.create');
		
		$grantableRights = $user->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == false){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == true){$foundRolesCreate = true;}}
		$this->assertTrue($foundGrantRevoke and $foundRolesCreate and $foundServerData);
		
		$_SESSION['user']->revokeRight('scoville.users.grant_revoke',false);
		
		$grantableRights = $user->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == false){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == true){$foundRolesCreate = true;}}
		$this->assertTrue(!$foundGrantRevoke and $foundRolesCreate and $foundServerData);
		
		$user->delete(false);
		$_SESSION['user']->delete(false);
		unset($_SESSION['user']);		
		unset($_SESSION['loggedin']);
	}
	
	public function testGetGrantableRightsUserWithRole(){
		$roleData = json_decode('{"name":"testGetGrantableRightsUserWithRole","rights":[{"name":"scoville.manageserverdata","granted":true}]}');
		$userM= $this->fixture->getUserManager();
		$rightM = $this->fixture->getRightsManager();
		$userM->createUser("testGetGrantableRightsUserWithRole", "testpassword", null);
		$user = $userM->getUserByName("testGetGrantableRightsUserWithRole");
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$_SESSION['user']->grantRight('scoville.users.grant_revoke',false);
		$_SESSION['user']->grantRight('scoville.manageserverdata',false);
		$_SESSION['user']->grantRight('scoville.roles.create',false);
		
		$role = $rightM->createRole($roleData,false);
		
		$grantableRights = $user->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == false){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == false){$foundRolesCreate = true;}}
		$this->assertTrue($foundGrantRevoke and $foundRolesCreate and $foundServerData);
		
		$user->assignRole($role,false);
		
		$grantableRights = $user->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == false){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == false){$foundRolesCreate = true;}}
		$this->assertTrue($foundGrantRevoke and $foundRolesCreate and !$foundServerData);
		
		$_SESSION['user']->revokeRight('scoville.users.grant_revoke',false);
		
		$grantableRights = $user->getGrantableRights();
		
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == false){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == false){$foundRolesCreate = true;}}
		$this->assertTrue(!$foundGrantRevoke and $foundRolesCreate and !$foundServerData);
		
		
		$role->delete(false);
		$user->delete(false);
		$_SESSION['user']->delete(false);
		unset($_SESSION['user']);		
		unset($_SESSION['loggedin']);
	}
	
	public function testGetGrantableRightsRole(){
		$roleData = json_decode('{"name":"testGetGrantableRightsRole"}');
		$userM= $this->fixture->getUserManager();
		$rightM = $this->fixture->getRightsManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$_SESSION['user']->grantRight('scoville.users.grant_revoke',false);
		$_SESSION['user']->grantRight('scoville.manageserverdata',false);
		$_SESSION['user']->grantRight('scoville.roles.create',false);
		$role = $rightM->createRole($roleData);
		$grantableRights = $role->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == false){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == false){$foundRolesCreate = true;}}
		$this->assertTrue($foundGrantRevoke and $foundRolesCreate and $foundServerData);
		
		$role->addRight('scoville.manageserverdata',false);
		
		$grantableRights = $role->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == true){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == false){$foundRolesCreate = true;}}
		$this->assertTrue($foundGrantRevoke and $foundRolesCreate and $foundServerData);
		
		$_SESSION['user']->revokeRight('scoville.manageserverdata',false);
		
		$grantableRights = $role->getGrantableRights();
		$foundGrantRevoke = false;
		$foundServerData = false;
		$foundRolesCreate = false;
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.users.grant_revoke' and $r['granted'] == false){$foundGrantRevoke = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.manageserverdata' and $r['granted'] == true){$foundServerData = true;}}
		foreach($grantableRights as $r){if ($r['right'] == 'scoville.roles.create' and $r['granted'] == false){$foundRolesCreate = true;}}
		$this->assertTrue($foundGrantRevoke and $foundRolesCreate and !$foundServerData);
		
		$role->delete(false);
		$_SESSION['user']->delete(false);
		unset($_SESSION['user']);		
		unset($_SESSION['loggedin']);
		
	}
	
	protected function tearDown(){
		try{
		    if (isset($role) and $role != null and get_class($role) == 'Role'){
		    	$role->delete(false);
		    }
		}catch(Exception $e){}
		try{
		    if (isset($user) and $user != null and get_class($user) == 'User'){
		    	$user->delete(false);
		    }
		}catch(Exception $e){}
		try{
		    if (isset($_SESSION['user']) and $_SESSION['user'] != null and get_class($_SESSION['user']) == 'User'){
		  		$_SESSION['user']->delete(false);
		  	}
		}catch(Exception $e){}
		try{
		  	if (isset($_SESSION['user'])){
		  		unset($_SESSION['user']);
		  	}
		}catch(Exception $e){}
		try{
			if (isset($_SESSION['loggedin'])){
		  		unset($_SESSION['loggedin']);
		  	}
		}catch(Exception $e){}
	}
	
}
?>
