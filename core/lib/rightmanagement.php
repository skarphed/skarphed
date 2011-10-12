<?php
namespace scv;

include_once 'core.php';

class RightsException extends \Exception{}

class RightsManager extends Singleton{
	private static $instance = null;
	
	public static function getInstance(){
		if (RightsManager::$instance==null){
			RightsManager::$instance = new RightsManager();
			RightsManager::$instance->init();
		}
		return RightsManager::$instance;
	}
	
	protected function init(){}
	
	public function checkRight($right,$user){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT AVAILABLE FROM CHECK_RIGHT(? , ?);";
		$res = $db->query($core,$stmnt,array($user->getId(),$right));
		$set = $db->fetchArray($res);
		return $set['AVAILABLE']; 
	}
	
	public function createRight($right, $moduleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$newRightId = $db->getSeqNext("RIG_GEN");
		$stmnt = "INSERT INTO RIGHTS (RIG_ID, RIG_NAME) VALUES (?,?);";
		$db->query($core, $stmnt, array($newRightId,$moduleId.".".$right));
		return;
	}
	
	public function removeRight($right, $moduleId){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "DELETE FROM RIGHTS WHERE RIG_NAME = ?;";
		$db->query($core, $stmnt, array($moduleId.".".$right));
		return;
	}
	
	public function getRightsForUser($user){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT RIG_NAME 
		          FROM USERRIGHTS 
		            INNER JOIN RIGHTS ON RIG_ID = URI_RIG_ID
		          WHERE URI_USR_ID = ?
		          UNION SELECT RIG_NAME
		          FROM USERROLES
		            INNER JOIN ROLERIGHTS ON URO_ROL_ID = RRI_ROL_ID
		            INNER JOIN RIGHTS ON RRI_RIG_ID = RIG_ID
		          WHERE URO_USR_ID = ?;";
		$result = $db->query($core, $stmnt, array($user->getId(),$user->getId()));
		$retval = array();
		while($set = $db->fetchArray($result)){
			$retval[] = $set['RIG_NAME'];
		}
		return $retval;
		
	}
	
	public function getGrantableRights($user){
		$core = Core::getInstance();
		$db = $core->getDB();
		$userM = $core->getUserManager();
		$sessionUser = $userM->getSessionUser();
		$sessionRights = $this->getRightsForUser($sessionUser);
		$stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN USERRIGHTS ON (RIG_ID = URI_RIG_ID) WHERE URI_USR_ID = ? ;";
		$res = $db->query($core,$stmnt,array($user->getId()));
		$resrights = array();
		while($set = $db->fetchArray($res)){
			$resrights[] = $set['RIG_NAME'];
		}
		$result = array();
		foreach ($sessionRights as $sessionRight){
			if (in_array($sessionRight,$resrights)){
				$result[] = array('right'=>$sessionRight,'granted'=>true);
			}else{
				$result[] = array('right'=>$sessionRight,'granted'=>false);
			}
		}
		return $result;
	}
	
	public function getIdForRight($right){
		$core = Core::getInstance();
		$db = $core->getDB();
		$stmnt = "SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME = ? ;";
		$res = $db->query($core,$stmnt, array($right));
		while($set = $db->fetchArray($res)){
			return $set['RIG_ID'];
		}
		return null;
	}
	
}
