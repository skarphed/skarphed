<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

use scv;

class TestBinary extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        $this->fixture = scv\Core::getInstance(); 
    }
    
    public function testCreateBinary() {
    	$userM= $this->fixture->getUserManager();
    	$userM->createUser("currentSessionUser","testpassword",null);
    	$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
    	$_SESSION['loggedin'] = "true";
    	
    	$bm = $this->fixture->getBinaryManager();
    	$bin = $bm->create('binary',"wertfuyhiertfvygbuhrtfvygbuhdcrtfvygbuhrtfvygbuhndcrfygbuhnjidcrfvuhndcrtfgvybuhnjitfvygbuhnjimcfyguhjifgvhnjtfvygbuhnjmictfvygbuhn",null);
    	$this->assertEquals(null,$bin->getId());
    	$bin->store();
    	$this->assertNotEquals(null,$bin->getId());
    	$temp = $bin->getId();
    	$bin = $bm->load($temp);
    	$this->assertEquals("wertfuyhiertfvygbuhrtfvygbuhdcrtfvygbuhrtfvygbuhndcrfygbuhnjidcrfvuhndcrtfgvybuhnjitfvygbuhnjimcfyguhjifgvhnjtfvygbuhnjmictfvygbuhn",$bin->getData());
    	
    	$_SESSION['user']->delete(false);
    	unset($_SESSION['user']);
    	unset($_SESSION['loggedin']);
    }
    
    public function testChangeBinary() {
    	$userM= $this->fixture->getUserManager();
    	$userM->createUser("currentSessionUser","testpassword",null);
    	$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
    	$_SESSION['loggedin'] = "true";
    	 
    	$bm = $this->fixture->getBinaryManager();
    	$bin = $bm->create('binary',"wertfuyhiertfvygbuhrtfvygbuhdcrtfvygbuhrtfvygbuhndcrfygbuhnjidcrfvuhndcrtfgvybuhnjitfvygbuhnjimcfyguhjifgvhnjtfvygbuhnjmictfvygbuhn",null);
    	$this->assertEquals(null,$bin->getId());
    	$bin->store();
    	$this->assertNotEquals(null,$bin->getId());
    	$temp = $bin->getId();
    	$bin = $bm->load($temp);
    	$this->assertEquals("wertfuyhiertfvygbuhrtfvygbuhdcrtfvygbuhrtfvygbuhndcrfygbuhnjidcrfvuhndcrtfgvybuhnjitfvygbuhnjimcfyguhjifgvhnjtfvygbuhnjmictfvygbuhn",$bin->getData());
    	$bin->setMime("text");
    	$bin->setData("bla bla bla text");
    	$bin->store();
    	$bin = $bm->load($temp);
    	$this->assertEquals("text",$bin->getMime());
    	$this->assertEquals("bla bla bla text",$bin->getData());
    	 
    	$_SESSION['user']->delete(false);
    	unset($_SESSION['user']);
    	unset($_SESSION['loggedin']);
    }
	
	protected function tearDown(){
		$db = $this->fixture->getDB();
		$db->query($this->fixture,"DELETE FROM binarys;");
		$db->commit();
		try{
			if (isset($_SESSION['user']) and $_SESSION['user'] != null and get_class($_SESSION['user']) == 'scv\User'){
				$_SESSION['user']->delete(false);
			}
		}catch(Exception $e){
		}
		try{
			if (isset($_SESSION['user'])){
				unset($_SESSION['user']);
			}
		}catch(Exception $e){
		}
		try{
			if (isset($_SESSION['loggedin'])){
				unset($_SESSION['loggedin']);
			}
		}catch(Exception $e){
		}
	}
	
}
?>
