<?php
require_once '/usr/share/php/PHPUnit/Framework/TestCase.php';
require_once '../lib/core.php';

use scv;

class TestOperation extends PHPUnit_Framework_TestCase {
    protected $fixture;
 
    protected function setUp() {
        $this->fixture = scv\Core::getInstance(); 
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
		$operation = new scv\TestOperation();
		$operationId = $operation->setDBID();
		
		for ($i = 0; $i < 3; $i++){
	
			$subOp = new scv\TestOperation();
			$subOp->setParent($operationId);
			$subOp->setValue("val",$i+100);
			$subOp->store();
			$suboperationId = $subOp->getId(); 
			for ($j = 0; $j < 3; $j++){
	
				$subOp = new scv\TestOperation();
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
		$operation = new scv\TestOperation();
		$operationId = $operation->setDBID();
		$i2ID = null;
		
		for ($i = 0; $i < 3; $i++){
	
			$subOp = new scv\TestOperation();
			$subOp->setParent($operationId);
			$subOp->setValue("val",$i+100);
			$subOp->store();
			$suboperationId = $subOp->getId();
			if ($i == 2){
				$i2ID = $subOperationId;
			} 
			for ($j = 0; $j < 3; $j++){
				if ($i == 2){
					$subOp = new scv\FailOperation();
				}else{
					$subOp = new scv\TestOperation();	
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
		$operation = new scv\TestOperation();
		$operationId = $operation->setDBID();
		$i2ID = null;
		
		for ($i = 0; $i < 3; $i++){
	
			$subOp = new scv\TestOperation();
			$subOp->setParent($operationId);
			$subOp->setValue("val",$i+100);
			$subOp->store();
			if ($i == 2){
				$i2ID = $subOperationId;
			} 
			$suboperationId = $subOp->getId(); 
			for ($j = 0; $j < 3; $j++){
	
				$subOp = new scv\TestOperation();
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
		
		$opRestored = $opM->restoreOperation(array("OPE_ID"=>$op->getId(),"OPE_TYPE"=>"scv\\TestOperation"));
		
		$this->assertEquals(true,is_int($opRestored->getValue("val")));
		$this->assertEquals(true,is_string($opRestored->getValue("st")));
		$this->assertEquals(true,is_bool($opRestored->getValue("bl")));
		
		$this->assertEquals("scv\\TestOperation",get_class($opRestored));
    }
	
	protected function tearDown(){
		
	}
	
}
?>
