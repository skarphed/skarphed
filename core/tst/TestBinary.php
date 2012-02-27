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
    	$this->assertEquals(null,$bin->getRight());
    	$bin->setMime("text");
    	$bin->setData("bla bla bla text");
    	$bin->store();
    	$bin = $bm->load($temp);
    	$this->assertEquals("text",$bin->getMime());
    	$this->assertEquals("bla bla bla text",$bin->getData());
    	$bin->store();
    	$bin = $bm->load($temp);
    	$bin->setRight(1);
    	$bin->store();
    	$bin = $bm->load($temp);
    	$this->assertEquals(1,$bin->getRight());
    	$bin->setRight(2);
    	$bin->store();
    	 
    	$_SESSION['user']->delete(false);
    	unset($_SESSION['user']);
    	unset($_SESSION['loggedin']);
    }
    
    public function testBinaryMeta() {
    	$userM= $this->fixture->getUserManager();
    	$userM->createUser("currentSessionUser","testpassword",null);
    	$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
    	$_SESSION['loggedin'] = "true";
    	 
    	$bm = $this->fixture->getBinaryManager();
    	$bin = $bm->create("binary","abc",null);
    	$this->assertEquals(null,$bin->getId());
    	$bin->store();
    	$this->assertNotEquals(null,$bin->getId());
    	$temp = $bin->getId();
    	$bin = $bm->load($temp);
    	$this->assertEquals("abc",$bin->getData());
    	$this->assertEquals(3,$bin->getSize());
    	$this->assertEquals(null,$bin->getRight());
    	$this->assertEquals($temp,$bin->getId());
    	 
    	$_SESSION['user']->delete(false);
    	unset($_SESSION['user']);
    	unset($_SESSION['loggedin']);
    }
    
    public function testLoadMD5() {
    	$userM= $this->fixture->getUserManager();
    	$userM->createUser("currentSessionUser","testpassword",null);
    	$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
    	$_SESSION['loggedin'] = "true";
    	 
    	$bm = $this->fixture->getBinaryManager();
    	$bin = $bm->create("binary","abc",null);
    	$this->assertEquals(null,$bin->getId());
    	$bin->store();
    	
    	$bin = $bm->loadmd5("900150983cd24fb0d6963f7d28e17f72");
    	$this->assertEquals("abc",$bin->getData());
    	 
    	$_SESSION['user']->delete(false);
    	unset($_SESSION['user']);
    	unset($_SESSION['loggedin']);
    }
    
    public function testFailLoad() {
    	$this->setExpectedException('scv\BinaryException','Data ID not found!');
    	$bm = $this->fixture->getBinarymanager();
    	$bin = $bm->load(123);
    }
    
    public function testFailLoadMD5() {
    	$this->setExpectedException('scv\BinaryException','Data ID not found!');
    	$bm = $this->fixture->getBinarymanager();
    	$bin = $bm->loadmd5("abcabcabcabcabcabcabcabcabcabcab");
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
