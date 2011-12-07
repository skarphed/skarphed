<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

class TestCss extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        $this->fixture = scv\Core::getInstance(); 
    }
	
	public function testInstallTemplate(){
		$templateM = $this->fixture->getTempateManager();
		system("cp /var/lib/jenkins/jobs/Scoville\ -\ Core/scv_template.tar.gz /tmp/");
		$template = $templateM->createFromFile('scv_template.tar.gz');
		$template->install();
		$templateRes = $templateM->createCurrentInstalled();
		$manifest = $templateRes->getManifest();
		$this->assertEquals("Scoville Showcase",$manifest['name']);
	}
	
	public function testOverInstallTemplate(){
		$templateM = $this->fixture->getTempateManager();
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
		
	}
	
}
?>