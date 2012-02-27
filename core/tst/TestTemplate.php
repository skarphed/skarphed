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
		$this->assertEquals("Scoville Showcase",$manifest->name);
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
		$this->assertEquals("Scoville Showcase",$manifest->name);
		system("cp /var/lib/jenkins/jobs/Scoville\ -\ Core/scv_template2.tar.gz /tmp/");
		$template2 = $templateM->createFromFile('scv_template2.tar.gz');
		$template2->install();
		$templateRes = $templateM->createCurrentInstalled();
		$manifest = $templateRes->getManifest();
		$this->assertEquals("Scoville Zwei",$manifest->name);
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