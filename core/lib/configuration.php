<?php
namespace scv;

class ConfigException extends \Exception{}

class Config {
    const CONF_NOT_LOAD = 0;
	const CONF_LOAD_LOCAL = 1;
	const CONF_LOAD_DB = 2;
	
	private $configuration = null;
	private $config_state = self::CONF_NOT_LOAD;
	
	public function __construct(){
		$this->configuration = json_decode(file_get_contents('../lib/config.json'),true);
		$this->config_state = self::CONF_LOAD_LOCAL;
	}
	
	public function initFromDb($database){
		//TODO: Implement
		$this->config_state = self::CONF_LOAD_DB;
		return;
	}
	
	public function getConfigState(){
		return $this->config_state;
	}
	
	public function getEntry ($id){
		if (isset($this->configuration[$id])){
			return $this->configuration[$id];
		}else{
			throw new ConfigException('This Configuration-Entry does not exist: '.$id);
		}
	}
		
}
