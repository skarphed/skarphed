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

class TestOperation extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        $this->fixture = Core::getInstance(); 
    }
 
    public function testSingleOperation(){
    	$opM = $this->fixture->getOperationManager();
		$op = new TestOperation();
		$op->store();
		
		$this->assertEquals(1,count($opM->getCurrentOperationsForGUI()));
		
		while($opM->processNext()){}
		
		$this->assertEquals(0,count($opM->getCurrentOperationsForGUI()));
		
    }
	
	public function testSingleFailOperation(){
		$opM = $this->fixture->getOperationManager();
		$op = new FailOperation();
		$op->store();
		
		$this->assertEquals(1,count($opM->getCurrentOperationsForGUI()));
		while($opM->processNext()){}
		$this->assertEquals(1,count($opM->getCurrentOperationsForGUI()));
		$opM->retryOperation($op->getId());
		while($opM->processNext()){}		
		$this->assertEquals(1,count($opM->getCurrentOperationsForGUI()));
		$opM->dropOperation($op->getId());
		$this->assertEquals(0,count($opM->getCurrentOperationsForGUI()));
	}
	
	public function testNestedOperations(){
		$opM = $this->fixture->getOperationManager();
		$operation = new TestOperation();
		$operationId = $operation->setDBID();
		
		for ($i = 0; $i < 3; $i++){
	
			$subOp = new TestOperation();
			$subOp->setParent($operationId);
			$subOp->setValue("val",$i+100);
			$subOp->store();
			$suboperationId = $subOp->getId(); 
			for ($j = 0; $j < 3; $j++){
	
				$subOp = new TestOperation();
				$subOp->setParent($suboperationId);
				$subOp->setValue("val",$j+1000);
				$subOp->store();
			}  
		}  
		$operation->store();
		
		$this->assertEquals(13,count($opM->getCurrentOperationsForGUI()));
		while($opM->processNext()){}
		$this->assertEquals(0,count($opM->getCurrentOperationsForGUI()));
	}
	
	public function testNestedFailOperations(){
		$opM = $this->fixture->getOperationManager();
		$operation = new TestOperation();
		$operationId = $operation->setDBID();
		$i2ID = null;
		
		for ($i = 0; $i < 3; $i++){
	
			$subOp = new TestOperation();
			$subOp->setParent($operationId);
			$subOp->setValue("val",$i+100);
			$subOp->store();
			$suboperationId = $subOp->getId();
			if ($i == 2){
				$i2ID = $suboperationId;
			} 
			for ($j = 0; $j < 3; $j++){
				if ($i == 2){
					$subOp = new FailOperation();
				}else{
					$subOp = new TestOperation();	
				}
				
				$subOp->setParent($suboperationId);
				$subOp->setValue("val",$j+1000);
				$subOp->store();
			}  
		}  
		$operation->store();
		
		$this->assertEquals(13,count($opM->getCurrentOperationsForGUI()));
		while($opM->processNext()){}
		$this->assertEquals(5,count($opM->getCurrentOperationsForGUI()));
		$opM->retryOperation($operationId);
		while($opM->processNext()){}
		$this->assertEquals(5,count($opM->getCurrentOperationsForGUI()));
		$opM->dropOperation($i2ID);
		$this->assertEquals(1,count($opM->getCurrentOperationsForGUI()));
		$opM->retryOperation($operationId);
		while($opM->processNext()){}
		$this->assertEquals(0,count($opM->getCurrentOperationsForGUI()));
	}

	public function testCancelSingleOperation(){
		$opM = $this->fixture->getOperationManager();
		$op = new TestOperation();
		$op->store();
		
		$this->assertEquals(1,count($opM->getCurrentOperationsForGUI()));
		
		$opM->cancelOperation($op->getId());
		
		$this->assertEquals(0,count($opM->getCurrentOperationsForGUI()));
	}
	
	public function testCancelNestedOperation(){
		$opM = $this->fixture->getOperationManager();
		$operation = new TestOperation();
		$operationId = $operation->setDBID();
		$i2ID = null;
		
		for ($i = 0; $i < 3; $i++){
	
			$subOp = new TestOperation();
			$subOp->setParent($operationId);
			$subOp->setValue("val",$i+100);
			$subOp->store();
			$suboperationId = $subOp->getId();
			if ($i == 2){
				$i2ID = $suboperationId;
			} 
			for ($j = 0; $j < 3; $j++){
	
				$subOp = new TestOperation();
				$subOp->setParent($suboperationId);
				$subOp->setValue("val",$j+1000);
				$subOp->store();
			}  
		}  
		$operation->store();
		
		$this->assertEquals(13,count($opM->getCurrentOperationsForGUI()));
		$opM->cancelOperation($i2ID);
		$this->assertEquals(9,count($opM->getCurrentOperationsForGUI()));
		$opM->cancelOperation($operationId);
		$this->assertEquals(0,count($opM->getCurrentOperationsForGUI()));
	}
	
	public function testRestoreOperation(){
    	$opM = $this->fixture->getOperationManager();
		$op = new TestOperation();
		$op->store();
		
		$opRestored = $opM->restoreOperation(array("OPE_ID"=>$op->getId(),"OPE_TYPE"=>"TestOperation"));
		
		$this->assertEquals(true,is_int($opRestored->getValue("val")));
		$this->assertEquals(true,is_string($opRestored->getValue("st")));
		$this->assertEquals(true,is_bool($opRestored->getValue("bl")));
		
		$this->assertEquals("TestOperation",get_class($opRestored));
    }
	
	protected function tearDown(){
		$db = $this->fixture->getDB();
		$db->query($this->fixture,"DELETE FROM OPERATIONS;");
		$db->commit();
	}
	
}
?>
