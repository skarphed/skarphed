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
require_once '../lib/css.php';

use scv;

/*TODO:
 * Rechteueberpreufung in die Tests integrieren
 * Tests fuer Widget- und Sessionbasierende Propertysets bauen
 */

class TestCss extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        $this->fixture = scv\Core::getInstance(); 
    }
	
	public function testServerPropertySet(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		$_SESSION['user']->grantRight('scoville.css.edit',false);
		
		$propertyset = new scv\CssPropertySet();
		$propertyset->setTypeGeneral();
		$this->assertEquals(null,$propertyset->getModuleId());
		$this->assertEquals(null,$propertyset->getWidgetId());
		$this->assertEquals(null,$propertyset->getSessionId());
		$this->assertEquals(scv\CssPropertySet::GENERAL,$propertyset->getType());
		
		$propertyset->editValue("div","color","#fff");
		$this->assertEquals("#fff", $propertyset->getValue("div","color"));
		$this->assertEquals(null, $propertyset->getValue("div","notsetvalue"));
		$propertyset->store();
		
		$cssM = $this->fixture->getCssManager();
		$fetchedset = $cssM->getCssPropertySet();
		
		$this->assertEquals(null,$fetchedset->getModuleId());
		$this->assertEquals(null,$fetchedset->getWidgetId());
		$this->assertEquals(null,$fetchedset->getSessionId());
		$this->assertEquals(scv\CssPropertySet::GENERAL,$fetchedset->getType());
		$this->assertEquals("#fff", $fetchedset->getValue("div","color"));
		$this->assertEquals(null, $fetchedset->getValue("div","notsetvalue"));
		$fetchedset->delete();
	}

	public function testModulePropertySet(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		$_SESSION['user']->grantRight('scoville.css.edit',false);
		$moduleId = 1; // de.zigapeda.scoville.text
		
		$propertyset = new scv\CssPropertySet();
		$propertyset->setModuleId($moduleId);
		$this->assertEquals($moduleId,$propertyset->getModuleId());
		$this->assertEquals(null,$propertyset->getWidgetId());
		$this->assertEquals(null,$propertyset->getSessionId());
		$this->assertEquals(scv\CssPropertySet::MODULE,$propertyset->getType());
		
		$propertyset->editValue("div","color","#fff");
		$this->assertEquals("#fff", $propertyset->getValue("div","color"));
		$this->assertEquals(null, $propertyset->getValue("div","notsetvalue"));
		$propertyset->store();
		
		$cssM = $this->fixture->getCssManager();
		$fetchedset = $cssM->getCssPropertySet($moduleId,null,null);
		
		$this->assertEquals($moduleId,$fetchedset->getModuleId());
		$this->assertEquals(null,$fetchedset->getWidgetId());
		$this->assertEquals(null,$fetchedset->getSessionId());
		$this->assertEquals(scv\CssPropertySet::MODULE,$fetchedset->getType());
		$this->assertEquals("#fff", $fetchedset->getValue("div","color"));
		$this->assertEquals(null, $fetchedset->getValue("div","notsetvalue"));
		$fetchedset->delete();
	}
	
	public function testCssParser(){
		$DATA = " .adsf { font-size:1px;\r\n
						color:#af0;
						border : 1px solid silver ;}
				  #blub { font-family: Verdana ; }";
	    $RESULTDATA = array(
			array("s"=>".adsf","k"=>"font-size","v"=>"1px"),
			array("s"=>".adsf","k"=>"color","v"=>"#af0"),
			array("s"=>".adsf","k"=>"border","v"=>"1px solid silver"),
			array("s"=>"#blub","k"=>"font-family","v"=>"Verdana")
		);
		$parser = new scv\CssParser($DATA);
		$this->assertEquals("1px",$parser->getValue(".adsf","font-size"));
		$this->assertEquals("#af0",$parser->getValue(".adsf","color"));
		$this->assertEquals("1px solid silver",$parser->getValue(".adsf","border"));
		$this->assertEquals("Verdana",$parser->getValue("#blub","font-family"));
		$parser2 = new scv\CssParser();
		$parser2->parseData($DATA);
		$this->assertEquals("1px",$parser2->getValue(".adsf","font-size"));
		$this->assertEquals("#af0",$parser2->getValue(".adsf","color"));
		$this->assertEquals("1px solid silver",$parser2->getValue(".adsf","border"));
		$this->assertEquals("Verdana",$parser2->getValue("#blub","font-family"));
		foreach($parser2 as $parserSet){
			$this->assertContains($parserSet,$RESULTDATA);
		}
		
	}
	
	protected function tearDown(){
		if (isset($_SESSION['user']) and get_class($_SESSION['user']) == 'scv\User'){
			$_SESSION['user']->delete(false);
			unset($_SESSION['user']);
		}
		if (isset($_SESSION['login'])){
			unset($_SESSION['loggedin']);
		}
		
	}
	
}
?>
