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
require_once 'core.php';

class TemplateException extends Exception{}

class TemplateManager extends Singleton{
	private static $instance = null;
	
	/**
	 * Get Singleton Instance
	 * 
	 * Returns the singleton Instance of the Rightsmanager
	 * 
	 * @return RightsManager The rights manager
	 */
	public static function getInstance(){
		if (TemplateManager::$instance==null){
			TemplateManager::$instance = new TemplateManager();
			TemplateManager::$instance->init();
		}
		return TemplateManager::$instance;
	}
	
	protected function init(){}
	
	public function createFromData($data){
		$template = new Template();
		$filename =hash('md5',time()+session_id()).".tar.gz";
		$template->setFilename($filename); 
		$handle = fopen("/tmp/".$filename,"w");
		fwrite($handle,$data);
		fclose();
		return $template;
	}
	
	public function createFromFile($filename){
		$template = new Template();
		$template->setFilename($filename);
		return $template;
	}
	
	public function createFromRemote($repository,$templatename){
		$template = $repository->downloadTemplate($templatename);
		$data = $template->data;
		return $this->createFromData($data);
	}
	
	public function createCurrentInstalled(){
		global $SCV_GLOBALCFG;
		$core = Core::getInstance();
		$template = new Template();
		$manifestWebPath = $SCV_GLOBALCFG['SCV_WEBPATH'].$SCV_GLOBALCFG['SCV_INSTANCE_SCOPE_ID']."/web/manifest.json";
		$manifestRaw = file_get_contents($manifestWebPath);
		if ($manifestRaw == false){
			throw new ModuleException("InstallationError: The manifest is not a valid Scoville Template");
			return;
		}
		$manifest = json_decode($manifestRaw);
		if ($manifest == null){
			throw new ModuleException("InstallationError: Manifest seems to be broken. Validate!");
			return;
		}
		$template->setManifest($manifest);
		$template->setInstalled(true);
		return $template;
	}
}

class Template {
	private $manifest = null;
	private $filename = null;
	private $installed = false;
	
	public function uninstall($tryToMap=false, $checkRight=true){
		if(!$this->installed){
			throw new TemplateException("Uninstall: Cannot uninstall a non-installed Template");
		}
		foreach($this->manifest->filenames as $filename){
			unlink("../web/".$filename);
		}
		
		$core = Core::getInstance();
		$db = $core->getDB();
		
		$sitesToSelect = array();
		
		foreach ($this->manifest->sites as $site){
			if (preg_match('/^[\w_-]*.html$/',$site->filename)){
				$sitesToSelect[] = $site->filename;
			}else{
				error_log("TemplateSystem//Warning: Site has been ignored due to suspicious filename: ".$site->filename);
			}
		}
		
		$stmnt = "SELECT SIT_ID FROM SITES WHERE SIT_FILENAME IN ( '".join("','",$sitesToSelect)."' ) ;";
	    $res = $db->query($core,$stmnt);
		
		$siteIds = array();
		while($set = $db->fetchArray($res)){
			$siteIds[] = $set['SIT_ID'];
		}
		if (count($siteIds)>0){
			if (!$tryToMap){
				$stmnt = "UPDATE WIDGETS SET WGT_SPACE = NULL WHERE WGT_SIT_ID IN (".join(",",$siteIds).") ;";
				$db->query($core,$stmnt);
			}
			$stmnt = "DELETE FROM SITES WHERE SIT_ID IN (".join(",",$siteIds).") ;";
			$db->query($core,$stmnt);
			$stmnt = "UPDATE WIDGETS SET WGT_SIT_ID = NULL WHERE WGT_SIT_ID IN (".join(",",$siteIds).") ;";
			$db->query($core,$stmnt);
		}
		$manifestWebPath = $SCV_GLOBALCFG['SCV_WEBPATH'].$SCV_GLOBALCFG['SCV_INSTANCE_SCOPE_ID']."/web/manifest.json";
		unlink($manifestWebPath);
	}
	
	
	public function validate(){
		//TODO: Eventuell noch nach im template vorhandenen ordnern ueberpruefen, die dort nicht sein sollten.
		
		if ($this->installed){
			throw new TemplateException("Validate: Cannot validate the installed template");
		}
		if (!isset($this->manifest)){
			throw new TemplateException("Validate: Cannot validate without a manifest");
		}
		if (!is_dir("/tmp/".$this->getTemporaryFolder())){
			throw new TemplateException("Validate: Cannot validate a Template that is not temporarily unpacked");
		}
		
		$foundDefault = false;
		
		foreach($this->manifest->sites as $site){
			if (isset($site->default)){
				$foundDefault = true;
			}
			if (!file_exists("/tmp/".$this->getTemporaryFolder()."/".$site->filename)){
				throw new TemplateException("Validate: File does not Exist: $site->filename");
			}
			$sitename = str_replace(".html","",$site->filename);
			if (!file_exists("/tmp/".$this->getTemporaryFolder()."/".$sitename.".css")){
				throw new TemplateException("Validate: Site is missing CSS: $site->filename");
			}
		}
		
		if(!file_exists("/tmp/".$this->getTemporaryFolder()."/general.css")){
			throw new TemplateException("Validate: Could not find general.css");
		}
		
		if (!$foundDefault){
			throw new TemplateException("Validate: Could not find Defaultsite");
		}
		
	}
	
	public function getSiteSpaces($sitedata){
		$spaceId = 1;
		while(true){
			if (1 == preg_match('/<\s*div[^>]*id\s*=\s*"s'.$spaceId.'"[^>]*>/',$sitedata)) {
				$spaceId++;
			}else{
				break;
			}
		}
		return $spaceId-1;
	}
	
	public function install($tryToMap=false, $checkRight=true){
		global $SCV_GLOBALCFG;

		if ($this->installed){
			throw new TemplateException("Installation: This template is already installed!");
		}
		
		$core = Core::getInstance();
		$templateM = $core->getTemplateManager();
		$currentTemplate = $templateM->createCurrentInstalled();
		$currentTemplate->uninstall($tryToMap, $checkRight);
		
		$this->temporaryUnpack();
		
		$manifestRaw = file_get_contents("/tmp/".$this->getTemporaryFolder()."/manifest.json");
		if ($manifestRaw == false){
			throw new ModuleException("InstallationError: $moduleId is not a valid Scoville Module");
		}
		$manifest = json_decode($manifestRaw);
		if ($manifest == null){
			throw new ModuleException("InstallationError: Manifest seems to be broken. Validate!");
		}
		$this->setManifest($manifest);
		
		$this->validate();
		
		foreach($this->manifest->filenames as $file){
			copy("/tmp/".$this->getTemporaryFolder()."/".$file, "../web/".$file);
		}
		
		$cssParser = new CssParser(file_get_contents("/tmp/".$this->getTemporaryFolder()."/general.css"));
		$core = Core::getInstance();
		$cssM = $core->getCssManager();
		$serverPropertySet = $cssM->getCssPropertySet();
		$serverPropertySet->setFromParser($cssParser);
		$serverPropertySet->store();
		
		$db = $core->getDB();
		$stmnt = "INSERT INTO SITES (SIT_ID, SIT_NAME, SIT_DESCRIPTION, SIT_FILENAME, SIT_HTML, SIT_SPACES, SIT_DEFAULT ) VALUES (GEN_ID(SIT_GEN,1),?,?,?,?,?,?) ;";
		foreach($this->manifest->sites as $site){
			$sitedata = file_get_contents("../web/".$site->filename);
			$spaces = $this->getSiteSpaces($sitedata);
			$name = isset($site->name)?"(unnamed)":$site->name;
			$htmlBlob = $db->createBlob($sitedata);
			$db->query($core,$stmnt,array($site->name, $site->desc, $site->filename, $htmlBlob, $spaces, isset($site->default)?1:0));
		}
		$manifestWebPath = $SCV_GLOBALCFG['SCV_WEBPATH'].$SCV_GLOBALCFG['SCV_INSTANCE_SCOPE_ID']."/web/manifest.json";
		copy("/tmp/".$this->getTemporaryFolder()."/manifest.json", $manifestWebPath);
		return;
	}
	
	public function setManifest($manifest){
		if (is_object($manifest) and $this->validateManifest($manifest)){
			$this->manifest = $manifest;
		}else{
			throw new TemplateException("Set Manifest: The manifest does not match specification!");
		}
	}
	
	public function getManifest(){
		return $this->manifest;
	}
	
	public function setFilename($filename){
		$this->filename = $filename;
	}
	
	public function setInstalled($installed){
		$this->installed = $installed;
	}
	
	public function temporaryUnpack(){
		if (!is_dir("/tmp/".$this->getTemporaryFolder())){
			mkdir("/tmp/".$this->getTemporaryFolder());
			system('tar xfz /tmp/'.escapeshellarg($this->filename).' -C /tmp/'.escapeshellarg($this->getTemporaryFolder()).'/ > /dev/null');
		}
	}
	
	private function getTemporaryFolder(){
		if (!isset($this->filename)){
			throw new TemplateException("GetTemporaryFolder: Cannot get Filename (Is this template the installed one? ;> )");
		}
		return str_replace(".tar.gz","",$this->filename);
	}
	
	public function __destruct(){
		if (isset($this->filename)){
			if (file_exists("/tmp/".$this->filename)){
				unlink("/tmp/".$this->filename);
			}
			if (is_dir("/tmp/".$this->getTemporaryFolder())){
				$core = Core::getInstance();
				$core->recursiveDelete("/tmp/".$this->getTemporaryFolder());
			}
		}
		
	}
	
	private function validateManifest($manifest){
		if (!isset($manifest->name) or !isset($manifest->description) or !isset($manifest->author)
		       or !isset($manifest->sites) or !isset($manifest->filenames)){
       		return false;
		}
		if (count($manifest->sites) < 1){
			return false;
		}
		foreach ($manifest->sites as $site){
			if (!isset($site->name) or !isset($site->desc) or !isset($site->filename)){
				return false;
			}
		}
		return true;
	}
}
?>