<?php
namespace scv;

include_once 'core.php';

class TemplateException extends \Exception{}

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
		$template = new Template();
		$manifestRaw = file_get_contents("../web/manifest.json");
		if ($manifestRaw == false){
			throw new ModuleException("InstallationError: $moduleId is not a valid Scoville Module");
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
			if (preg_match("/^[\w_-]*.html$/",$site->filename)){
				$siteString[] = $site->filename;
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
		
		if (!$tryToMap){
			$stmnt = "UPDATE WIDGETS SET WGT_SPACE = NULL WHERE WGT_SIT_ID IN (".join(",",$siteIds).") ;";
			$db->query($core,$stmnt);
		}
		$stmnt = "DELETE FROM SITES WHERE SIT_ID IN (".join(",",$siteIds).") ;";
		$db->query($core,$stmnt);
		$stmnt = "UPDATE WIDGETS SET WGT_SIT_ID = NULL WHERE WGT_SIT_ID IN (".join(",",$siteIds).") ;";
		$db->query($core,$stmnt);
		unlink("../web/manifest.json");
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
			if (1 == preg_match('<\s*div[^>]*id\s*=\s*"s'.$spaceId.'"[^>]*>',$sitedata)) {
				$spaceId++;
			}else{
				break;
			}
		}
		return $spaceId;
	}
	
	public function install($tryToMap=false, $checkRight=true){
		if ($this->installed){
			throw new TemplateException("Installation: This template is already installed!");
		}
		$currentTemplate = $this->createCurrentInstalled();
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
		return;
	}
	
	public function setManifest($manifest){
		if (is_object($manifest) and $this->validateManifest($manifest)){
			$this->manifest = $manifest;
		}
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
		if (count($manifest->sites < 1)){
			return false;
		}
		foreach ($manifest->sites as $site){
			if (!isset($site->name) or !isset($manifest->desc) or !isset($site->filename)){
				return false;
			}
		}
		return true;
	}
}
?>