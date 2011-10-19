<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

use scv;

class ArrayTest extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        // Array-Fixture erzeugen.
        $this->fixture = scv\Core::getInstance();
		$userM= $this->fixture->getUserManager();
		$userM->createUser("genericTestUser", "testpassword", null);
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
	
	public function testCreateUser(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("testCreateAndDeleteUser", "testpassword", null);
		$user = $userM->getUserByName("testCreateAndDeleteUser");
		$this->assertEquals('scv\User', get_class($user));
		$this->assertTrue($user->authenticate("testpassword"));
	}
	
	public function testAlterPassword(){
		$userM = $this->fixture->getUserManager();
		$user = $userM->getUserByName("genericTestUser");
		$this->assertFalse($user->authenticate("tochangepassword"));
		$user->alterPassword("tochangepassword", "testpassword");
		$this->assertTrue( $user->authenticate("tochangepassword"));
		$user->alterPassword("testpassword", "tochangepassword");
		$this->assertFalse($user->authenticate("tochangepassword"));
	}
	
	public function testCannotSetPasswordWithoutOldPasssword(){
		$userM = $this->fixture->getUserManager();
		$user = $userM->getUserByName("genericTestUser");
		try{
			$user->alterPassword("tochangepassword","falsepassword");
			$this->assertTrue(false);
		}catch (UserException $e ){}
	}
	
	
}
?>