<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

use scv;

class TestBinary extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        $this->fixture = scv\Core::getInstance(); 
    }
    
    protected function testCreateBinary() {
    	$bm = $this->fixture->getBinaryManager();
    	$bin = $bm->create('binary',"wertfuyhiertfvygbuhrtfvygbuhdcrtfvygbuhrtfvygbuhndcrfygbuhnjidcrfvuhndcrtfgvybuhnjitfvygbuhnjimcfyguhjifgvhnjtfvygbuhnjmictfvygbuhn",null);
    	$this->assertEquals(null,$bin->getId());
    	$bin->store();
    	$this->assertNotEquals(null,$bin->getId());
    	$temp = $bin->getId();
    	$bin = $bm->load($temp);
    	$this->assertEquals("wertfuyhiertfvygbuhrtfvygbuhdcrtfvygbuhrtfvygbuhndcrfygbuhnjidcrfvuhndcrtfgvybuhnjitfvygbuhnjimcfyguhjifgvhnjtfvygbuhnjmictfvygbuhn",$bin->getData());
    }
	
	protected function tearDown(){
		$db = $this->fixture->getDB();
		$db->query($this->fixture,"DELETE FROM binarys;");
		$db->commit();
	}
	
}
?>
