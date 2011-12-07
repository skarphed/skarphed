<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

class TestTemplate extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        $this->fixture = scv\Core::getInstance(); 
    }
	
	public function testInstallTemplate(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$templateM = $this->fixture->getTemplateManager();
		system("cp /var/lib/jenkins/jobs/Scoville\ -\ Core/scv_template.tar.gz /tmp/");
		$template = $templateM->createFromFile('scv_template.tar.gz');
		$template->install();
		$templateRes = $templateM->createCurrentInstalled();
		$manifest = $templateRes->getManifest();
		$this->assertEquals("Scoville Showcase",$manifest['name']);
	}
	
	public function testOverInstallTemplate(){
		$userM= $this->fixture->getUserManager();
		$userM->createUser("currentSessionUser","testpassword",null);
		$_SESSION['user'] = $userM->getUserByName("currentSessionUser");
		$_SESSION['loggedin'] = "true";
		
		$templateM = $this->fixture->getTemplateManager();
		system("cp /var/lib/jenkins/jobs/Scoville\ -\ Core/scv_template.tar.gz /tmp/");
		$template = $templateM->createFromFile('scv_template.tar.gz');
		$template->install();
		$templateRes = $templateM->createCurrentInstalled();
		$manifest = $templateRes->getManifest();
		$this->assertEquals("Scoville Showcase",$manifest['name']);
		system("cp /var/lib/jenkins/jobs/Scoville\ -\ Core/scv_template2.tar.gz /tmp/");
		$template2 = $templateM->createFromFile('scv_template2.tar.gz');
		$template2->install();
		$templateRes = $templateM->createCurrentInstalled();
		$manifest = $templateRes->getManifest();
		$this->assertEquals("Scoville Zwei",$manifest['name']);
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