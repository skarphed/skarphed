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

	require_once('repo_database.php');
	#require_once('Crypt_RSA');
	
	
	abstract class Singleton {
		abstract public static function getInstance();
	
		abstract protected function init();
	}
	
	class Repository extends Singleton{
		private static $instance = null;
		private $config = null;
	
		public static function getInstance(){
			if (Repository::$instance==null){
				Repository::$instance = new Repository();
				Repository::$instance->init();
			}
			return Repository::$instance;
		}
		
		protected function init(){
			$cfg_file = file_get_contents("config.json");
			$this->config = json_decode($cfg_file,true);
		}
		
		private function rrmdir($dir) {
			if (is_dir($dir)) {
				$objects = scandir($dir);
				foreach ($objects as $object) {
					if ($object != "." && $object != "..") {
						if (filetype($dir."/".$object) == "dir") $this->rrmdir($dir."/".$object); else unlink($dir."/".$object);
					}
				}
				reset($objects);
				rmdir($dir);
			}
		}
		
		private function establishConection(){
			$con = new repo_database();
			$con->set_all($this->config['db.user'],
						  $this->config['db.ip'],
						  $this->config['db.name'],
						  $this->config['db.password']);
			$con->connect();
			return $con;
		}
		
		public function getAllModules(){
			$con = $this->establishConection();
			$resultset = $con->query("select mod_displayname, mod_md5, mod_signature, mod_name, mod_versionmajor, mod_versionminor, mod_versionrev
				from modules join (select mod_name vername 
				,max(mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_versionrev) ver 
				from modules 
				group by mod_name) 
				on vername = mod_name 
				and ver = mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_versionrev");
			$modules = array();
			while($result = $con->fetchArray($resultset)){
				$modules[] = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_DISPLAYNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_VERSIONREV"],
					        		 'signature'=>$result["MOD_SIGNATURE"]);		
			}
			return json_encode(array("r"=>$modules));
		}
		
		public function getLatestVersion($module){
			$con = $this->establishConection();
			$resultset = $con->query("select mod_displayname, mod_signature, mod_name, mod_versionmajor, mod_versionminor, mod_versionrev
				from modules join (select mod_name vername 
				,max(mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_versionrev) ver 
				from modules 
				group by mod_name) 
				on vername = mod_name 
				and ver = mod_versionmajor*10000000 
				+mod_versionminor*100000 
				+mod_versionrev
				where mod_name = ?", array($module->name));
			
			if($result = $con->fetchArray($resultset)){
				$module = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_DISPLAYNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_VERSIONREV"],
					        		 'signature'=>$result["MOD_SIGNATURE"]);		
			}else{
				throw new Exception('Module does not Exist: '.$module->name);
			}
			return array("r"=>$module);
		}
		
		public function getVersionsOfModule($module){
			$con = $this->establishConection();
			$resultset = $con->query("select mod_name, mod_displayname, mod_signature, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev from modules 
										where mod_name = ? ;",array($module->name));
			$modules = array();
			while($result = $con->fetchArray($resultset)){
				$modules[] = array('name'=>$result["MOD_NAME"],
									 'hrname'=>$result["MOD_DISPLAYNAME"],
									 'version_major'=>$result["MOD_VERSIONMAJOR"],
									 'version_minor'=>$result["MOD_VERSIONMINOR"],
									 'revision'=>$result["MOD_VERSIONREV"],
							    	 'signature'=>$result["MOD_SIGNATURE"]);			
			}
			return json_encode(array("r"=>$modules));
		}
		
		public function resolveDependenciesDownwards($module){
			$con = $this->establishConection();
			$resultset = $con->query("select mod_id from modules
										where mod_name = ? and mod_versionmajor = ? and mod_versionminor = ? and mod_versionrev = ? and mod_signature = ? ;",
										array($module->name, $module->version_major,$module->version_minor,$module->revision,$module->signature));
			if($result = $con->fetchArray($resultset)) {
				$modid = $result['MOD_ID'];
				$resultset = $con->query("select distinct dep_mod_dependson from dependencies where dep_mod_id = ?", array($modid));
				$moduleids = $modid;
				while($result = $con->fetchArray($resultset)) {
					do {
						$moduleids = $moduleids.",".$result["DEP_MOD_DEPENDSON"];
					} while ($result = $con->fetchArray($resultset));
					$resultset = $con->query("select dep_mod_dependson from dependencies where dep_mod_id in (" . $moduleids . ") and dep_mod_dependson not in (" . $moduleids . ")");
				}
				$resultset = $con->query("select mod_name, mod_displayname, mod_signature, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev from modules where mod_id in (".$moduleids.") and mod_id != ".$modid);
				$modules = array();
				while($result = $con->fetchArray($resultset)){
					$modules[] = array('name'=>$result["MOD_NAME"],
										 'hrname'=>$result["MOD_DISPLAYNAME"],
										 'version_major'=>$result["MOD_VERSIONMAJOR"],
										 'version_minor'=>$result["MOD_VERSIONMINOR"],
										 'revision'=>$result["MOD_VERSIONREV"],
							   			 'signature'=>$result["MOD_SIGNATURE"]);	
				}
				return json_encode(array("r"=>$modules));
			}else{
				throw new Exception('Module does not Exist: '.$module->name);
			}
		}

		public function resolveDependenciesUpwards($module){
			$con = $this->establishConection();
			$resultset = $con->query("select mod_id from modules
										where mod_name = ? and mod_versionmajor = ? and mod_versionminor = ? and mod_versionrev = ? and mod_signature = ? ;",
										array($module->name, $module->version_major,$module->version_minor,$module->revision,$module->signature));
			if($result = $con->fetchArray($resultset)) {
				$modid = $result['MOD_ID'];
				$resultset = $con->query("select distinct dep_mod_id from dependencies where dep_mod_dependson = ?", array($modid));
				$moduleids = $modid;
				while($result = $con->fetchArray($resultset)) {
					do {
						$moduleids = $moduleids.",".$result["DEP_MOD_ID"];
					} while ($result = $con->fetchArray($resultset));
					$resultset = $con->query("select dep_mod_id from dependencies where dep_mod_dependson in (" . $moduleids . ") and dep_mod_id not in (" . $moduleids . ")");
				}
				$resultset = $con->query("select mod_name, mod_displayname, mod_signature, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev from modules where mod_id in (".$moduleids.") and mod_id != ".$modid);
				$modules = array();
				while($result = $con->fetchArray($resultset)){
					$modules[] = array('name'=>$result["MOD_NAME"],
										 'hrname'=>$result["MOD_DISPLAYNAME"],
										 'version_major'=>$result["MOD_VERSIONMAJOR"],
										 'version_minor'=>$result["MOD_VERSIONMINOR"],
										 'revision'=>$result["MOD_VERSIONREV"],
							    		 'signature'=>$result["MOD_SIGNATURE"]);	
				}
				return json_encode(array("r"=>$modules));
			}else{
				throw new Exception('Module does not Exist: '.$module->name);
			}
		}

		public function downloadModule($module){
			$con = $this->establishConection();
			$resultset = $con->query("select mod_name, mod_data, mod_displayname, mod_id, mod_versionmajor, mod_versionminor, mod_versionrev, mod_signature from modules 
									where mod_name = ? and mod_versionmajor = ? and mod_versionminor = ? and mod_versionrev = ? and mod_signature = ? ;",
									array($module->name, $module->version_major,$module->version_minor,$module->revision,$module->signature));
			if($result = $con->fetchArray($resultset)) {
				$module = array('name'=>$result["MOD_NAME"],
							    'hrname'=>$result["MOD_DISPLAYNAME"],
						 	    'version_major'=>$result["MOD_VERSIONMAJOR"],
							    'version_minor'=>$result["MOD_VERSIONMINOR"],
							    'revision'=>$result["MOD_VERSIONREV"],
							    'signature'=>$result["MOD_SIGNATURE"]);
				return json_encode(array("r"=>$module,"data"=>base64_encode($result["MOD_DATA"])));
			}else{
				throw new Exception('Module does not Exist: '.$module->name);
			}
		}

		public function authenticate($password){
			$con = $this->establishConection();
			$res = $con->query("SELECT VAL FROM CONFIG WHERE PARAM = 'password' OR PARAM = 'salt' ORDER BY PARAM ASC;");
			$set = $con->fetchObject($res);
			$db_hash = $set->VAL;
			$set = $con->fetchObject($res);
			$salt = base64_decode($set->VAL);
			$hash = hash('sha512', $password.$salt);
			
			$isValid = $db_hash == $hash;
			$_SESSION['privileged'] = $isValid;
			return $isValid;
		}
		
		public function logout(){
			$this->checkAdmin();
			$_SESSION['privileged'] = false;
		}
		
		private function generateSalt(){
			$salt = "";
			$length = rand(128,255);
			for ($i = 0; $i < $length; $i++){
				$salt .= chr(rand(0,255));
			}
			return $salt;
		}
		
		private function checkAdmin(){
			if (!isset($_SESSION['privileged']) or !$_SESSION['privileged'])
				throw new Exception('Only admin may perform this Operation (forgot to log on ?)');
		}
		
		public function changePassword($password){
			$this->checkAdmin();
				
			$con = $this->establishConection();
			$salt = $this->generateSalt();
			$hash = hash('sha512',$password.$salt);
			$salt = base64_encode($salt);
			$con->query("UPDATE CONFIG SET VAL = ? WHERE PARAM = ?", array($hash,'password'));
			$con->query("UPDATE CONFIG SET VAL = ? WHERE PARAM = ?", array($salt,'salt'));
			return true;
		}
		
		public function uploadModule($data,$signature){
			require_once('Crypt/RSA.php');
			$con = $this->establishConection();
			
			$rsa = new Crypt_RSA();
			$rsa->setSignatureMode(CRYPT_RSA_SIGNATURE_PKCS1);
			$rsa->setHash('sha256');
			$rsa->setMGFHash('sha256');
			
			$res = $con->query("SELECT DEV_ID, DEV_NAME, DEV_PUBLICKEY FROM DEVELOPER;");
			$valid = false;
			$developerId = null;
			while($set = $con->fetchObject($res)){
				$rsa->loadKey($set->DEV_PUBLICKEY);
				$valid = $rsa->verify($data,$signature);
				if ($valid)
					$developerId = $set->DEV_ID;
					break;
			}
			if(!$valid)
				throw new Exception('Signature verification Failed. Data has been manipulated.');
			try {
				mkdir("/tmp/scv_repo");
			} catch (Exception $e){}
			$filename_temp = "/tmp/scv_repo/".hash('md5',$signature);
			mkdir($filename_temp);
			$file = fopen($filename_temp.'.tar.gz','w');
			fwrite($file,$data);
			fclose($file);
			system('tar xfz '.$filename_temp.'.tar.gz -C '.$filename_temp.' > /dev/null');
			$manifestRaw = file_get_contents($filename_temp."/manifest.json");
			if ($manifestRaw == false){
				throw new Exception('Error while reading manifest');				
			}
			$manifest = json_decode($manifestRaw);
			if ($manifest == null){
				throw new Exception('Manifest is not valid JSON');
			}
			$res = $con->query("SELECT MAX(MOD_VERSIONREV) AS MAXREVISION FROM MODULES WHERE MOD_NAME = ? ;",array($manifest->name));
			if ($set = $con->fetchObject($res)){
				$revision = ++$set->MAXREVISION;
			}else{
				$revision = 0;
			}
			$mod_id = $con->getSeqNext("MOD_GEN");
			$md5 = hash('md5',$data);

			$rsa = new Crypt_RSA();
			$rsa->loadKey($this->getPrivateKey());
			$rsa->setSignatureMode(CRYPT_RSA_SIGNATURE_PKCS1);
			$rsa->setHash('sha256');
			$rsa->setMGFHash('sha256');
			$repo_signature = base64_encode($rsa->sign($data));
			
			
			$blobid = $con->createBlob($data);
			$con->query("INSERT INTO MODULES (MOD_ID, MOD_NAME, 
											MOD_DISPLAYNAME, 
											MOD_VERSIONMAJOR, 
											MOD_VERSIONMINOR,
											MOD_VERSIONREV,
											MOD_MD5,
											MOD_SIGNATURE,
											MOD_DATA)
									VALUES (?,?,?,?,?,?,?,?,?)",
									array($mod_id, $manifest->name,
										  $manifest->hrname, $manifest->version_major,
										  $manifest->version_minor, $revision, $md5,
										  $repo_signature, $blobid));
			$this->rrmdir($filename_temp);
			unlink($filename_temp.'.tar.gz');
			return true;
		}
		
		public function deleteModule($identifier,$major=null,$minor=null,$revision=null){
			$this->checkAdmin();
			$con = $this->establishConection();
			if (isset($major)){
				if (isset($minor)){
					if (isset($revision)){
						$con->query("DELETE FROM MODULES WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? AND MOD_VERSIONREV = ? ;"
									, array($identifier,$major,$minor,$revision));
					}else{
						$con->query("DELETE FROM MODULES WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? AND MOD_VERSIONMINOR = ? ;"
									, array($identifier,$major,$minor));	
					}
				}else{
				    $con->query("DELETE FROM MODULES WHERE MOD_NAME = ? AND MOD_VERSIONMAJOR = ? ;"
				    			, array($identifier,$major));
				}
			}else{
				$con->query("DELETE FROM MODULES WHERE MOD_NAME = ? ;"
				    			, array($identifier));
			}
			return true;
		}
		
		public function registerDeveloper($name, $fullname, $publickey){
			$this->checkAdmin();
			
			$con = $this->establishConection();
			$devId = $con->getSeqNext("DEV_GEN");
			
			$con = $this->establishConection();
			$con->query("INSERT INTO DEVELOPER (DEV_ID, DEV_NAME, DEV_FULLNAME, DEV_PUBLICKEY)
						 VALUES (?,?,?,?) ;", array($devId, $name, $fullname, $publickey));
			return true;
		}
		
		public function deleteDeveloper($devId){
			$this->checkAdmin();
			
			$con = $this->establishConection();
			$con->query("UPDATE DEVELOPER SET DEV_PUBLICKEY = '' WHERE DEV_ID = ? ;");
			
			return true;	
		}
		
		public function getDevelopers(){
			$this->checkAdmin();
			
			$con = $this->establishConection();
			$res = $con->query("SELECT DEV_ID, DEV_NAME, DEV_FULLNAME FROM DEVELOPER ;");
			$ret = array();
			while($set = $con->fetchObject($res)){
				$ret[] = array('devId'=>$set->DEV_ID,
							   'name'=>$set->DEV_NAME,
							   'fullName'=>$set->DEV_FULLNAME);
			}
			return $ret;
		}
		
		public function createOwnKeypair(){
			require_once('Crypt/RSA.php');
			
			$rsa = new Crypt_RSA();
			$keys  = $rsa->createKey(1024);
			
			$con = $this->establishConection();
			$con->query("INSERT INTO CONFIG (VAL,PARAM) VALUES (?,?);", array($keys['publickey'],'publickey'));
			$con->query("INSERT INTO CONFIG (VAL,PARAM) VALUES (?,?);", array($keys['privatekey'],'privatekey'));
			return true;
		}
		
		private function getPublicKey(){
			$con = $this->establishConection();
			$res = $con->query("SELECT VAL FROM CONFIG WHERE PARAM = 'publickey';");
			if ($set = $con->fetchObject($res)){
				return $set->VAL;
			}
			return null;
		}
		
		private function getPrivateKey(){
			$con = $this->establishConection();
			$res = $con->query("SELECT VAL FROM CONFIG WHERE PARAM = 'privatekey';");
			if ($set = $con->fetchObject($res)){
				return $set->VAL;
			}
			return null;
		}
		
		public function getPublicKeyForPage(){
			return $this->getPublicKey();
		}
		
		public function getPublicKeyForScoville(){
			return $this->getPublicKey();
		}
	}
?>