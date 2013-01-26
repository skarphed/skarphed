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
require_once('core.php');

class ConfigException extends Exception{}

class Config {
    const CONF_NOT_LOAD = 0;
	const CONF_LOAD_LOCAL = 1;
	const CONF_LOAD_DB = 2;
	
	private $configuration = null;
	private $config_state = self::CONF_NOT_LOAD;
	
	public function __construct(){
		global $SCV_GLOBALCFG;
		$configfilepath = $SCV_GLOBALCFG['SCV_WEBPATH'].$SCV_GLOBALCFG['SCV_INSTANCE_SCOPE_ID'].'/web/config.json';
		$this->configuration = json_decode(file_get_contents($configfilepath),true);
		$this->config_state = self::CONF_LOAD_LOCAL;
	}
	
	public function initFromDb(){
		$core = Core::getInstance();
		$con = $core->getDB();
		$res = $con->query($core,"SELECT PARAM,VAL FROM CONFIG");
		while($set = $con->fetchObject($res)){
			$this->configuration[$set->PARAM] = $set->VAL;
		}
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
?>