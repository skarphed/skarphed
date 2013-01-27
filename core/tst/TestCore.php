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

class TestCore extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        // Array-Fixture erzeugen.
        $this->fixture = Core::getInstance();
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
}
?>