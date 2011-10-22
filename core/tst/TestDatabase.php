<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

use scv;

class TestDatabase extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        // Array-Fixture erzeugen.
        $this->fixture = scv\Core::getInstance();
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