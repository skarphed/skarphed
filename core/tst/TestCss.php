<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

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
		
		$_SESSION['user']->delete(false);
		unset($_SESSION['user']);		
		unset($_SESSION['loggedin']);
	}

	public function testModulePropertySet(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
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
		$fetchedset = $cssM->getCssPropertySet();
		
		$this->assertEquals($moduleId,$fetchedset->getModuleId());
		$this->assertEquals(null,$fetchedset->getWidgetId());
		$this->assertEquals(null,$fetchedset->getSessionId());
		$this->assertEquals(scv\CssPropertySet::MODULE,$fetchedset->getType());
		$this->assertEquals("#fff", $fetchedset->getValue("div","color"));
		$this->assertEquals(null, $fetchedset->getValue("div","notsetvalue"));
		$fetchedset->delete();
		
		$_SESSION['user']->delete(false);
		unset($_SESSION['user']);		
		unset($_SESSION['loggedin']);
	}

	protected function tearDown(){

	}
	
}
?>
