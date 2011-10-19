<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

use scv;

class ArrayTest extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
    	/*try{
		  session_destroy();
		}catch(Exception $e){}*/
        // Array-Fixture erzeugen.
        $this->fixture = scv\Core::getInstance();
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
		$this->assertEquals('scv\User', get_class($user));
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
		
		$this->assertEquals('scv\User', get_class($user));
		$this->assertTrue($user->authenticate("testpassword"));
		$user->delete(false);
		$this->assertTrue(true);
		
	}
	
	public function testCannotSetPasswordWithoutOldPasssword(){
		$this->setExpectedException('scv\UserException','Could not set Password: Old password is wrong');
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
		$this->setExpectedException('scv\UserException', 'Granting Right: This user is not allowed to grant rights!');
        try {
			$user->grantRight('scoville.manageserverdata',true);
		}catch(scv\UserException $e){
			$user->delete(false);
			$_SESSION['user']->delete(false);		
			unset($_SESSION['user']);
			unset($_SESSION['loggedin']);
			throw $e;
		}
		
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
	
	/*public function testGetGrantableRightsUser(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testAlterPasswordUser", "testpassword", null);
		$userM->createUser("currentSession", "testpassword", null);
		$user = $userM->getUserByName("testAlterPasswordUser");
		
		
	}
	
	public function testGetGrantableRightsRole(){
		
	}*/
	
	/*protected function tearDown(){
		try{
		  session_destroy();
		}catch(Exception $e){}
	}*/
	
}
?>