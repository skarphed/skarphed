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

	require_once('repository.php');
	
	class ProtocolHandler  {
		//Calls From Scoville to Repository
		const GET_ALL_MODULES = 1;
		const GET_VERSIONS_OF_MODULE = 2;
		const RESOLVE_DEPENDENCIES_DOWNWARDS = 3;
		const RESOLVE_DEPENDENCIES_UPWARDS = 4;
		const DOWNLOAD_MODULE = 5;
		const GET_PUBLICKEY = 6;
		const GET_LATEST_VERSION = 7;
		
		//Calls from AdminGUI to Repository
		const AUTHENTICATE = 100;
		const LOGOUT = 101;
		const CHANGE_PASSWORD = 102;
		const REGISTER_DEVELOPER = 103;
		const UNREGISTER_DEVELOPER = 104;
		const UPLOAD_MODULE = 105;
		const DELETE_MODULE = 106;
		const GET_DEVELOPERS = 107;
		
		public function __construct($json){
			$this->subject = json_decode($json);
			$this->result = null;
			if ($this->subject == null){
				throw new Exception('Invalid Json');
			}
		}
		
		private function verifyModule(){
			if (!isset($this->subject->m) or 
				!isset($this->subject->m->name) or
				!isset($this->subject->m->hrname) or
				!isset($this->subject->m->version_major) or 
				!isset($this->subject->m->version_minor) or
				!isset($this->subject->m->revision) or
				!isset($this->subject->m->signature) ){
				throw new Exception('Not a valid Module!');
			}
			
		}
		
		public function execute(){
			$repository = Repository::getInstance();
			switch($this->subject->c){
				case ProtocolHandler::GET_ALL_MODULES:
					$this->result = $repository->getAllModules();
					break;
				case ProtocolHandler::GET_VERSIONS_OF_MODULE:
					$this->verifyModule();
					$this->result =$repository->getVersionsOfModule($this->subject->m);
					break;
				case ProtocolHandler::RESOLVE_DEPENDENCIES_DOWNWARDS:
					$this->verifyModule();
					$this->result = $repository->resolveDependenciesDownwards($this->subject->m);
					break;
				case ProtocolHandler::RESOLVE_DEPENDENCIES_UPWARDS:
					$this->verifyModule();
					$this->result = $repository->resolveDependenciesUpwards($this->subject->m);
					break;
				case ProtocolHandler::DOWNLOAD_MODULE:
					$this->verifyModule();
					$this->result = $repository->downloadModule($this->subject->m);
					break;
				case ProtocolHandler::GET_PUBLICKEY:
					$this->result = json_encode(array("r"=>$repository->getPublicKeyForScoville()));
					break;
				case ProtocolHandler::GET_LATEST_VERSION:
					$this->result = json_encode($repository->getLatestVersion($this->subject->m));
					break;
				
				
				case ProtocolHandler::AUTHENTICATE:
					if (!isset($this->subject->dxd)){
						throw new Exception('Password not set');
					}
					$res = $repository->authenticate((string)$this->subject->dxd);
					$this->result = json_encode(array("r"=>$res));
					break;
					
				case ProtocolHandler::LOGOUT:
					$repository->logout();
					$this->result = json_encode(array("r"=>0));
					break;
					
				case ProtocolHandler::CHANGE_PASSWORD:
					if (!isset($this->subject->dxd)){
						throw new Exception('Password not set');
					}
					$repository->changePassword((string)$this->subject->dxd);
					$this->result = json_encode(array("r"=>0));
					break;
					
				case ProtocolHandler::REGISTER_DEVELOPER:
					if (!isset($this->subject->name) or 
					    !isset($this->subject->fullName) or 
						!isset($this->subject->publicKey)){
							throw new Exception ('Invalid Registrationdata');
						}
					$repository->registerDeveloper((string)$this->subject->name,
												   (string)$this->subject->fullName,
												   (string)$this->subject->publicKey);
					$this->result = json_encode(array("r"=>0));
					break;
					
				case ProtocolHandler::UNREGISTER_DEVELOPER:
					if (!isset($this->subject->devId)){
						throw new Exception('Need DeveloperId');
					}
					$repository->unregisterDeveloper((int)$this->subject->devId);
					$this->result = json_encode(array("r"=>0));
					break;
					
				case ProtocolHandler::UPLOAD_MODULE:
					if (!isset($this->subject->data) or 
					    !isset($this->subject->signature)){
					    	throw new Exception('Not valid data');
					    }
					$repository->uploadModule(base64_decode($this->subject->data),
											  base64_decode($this->subject->signature));
					$this->result = json_encode(array("r"=>0));
					break;
					
				case ProtocolHandler::DELETE_MODULE:
					if (!isset($this->subject->moduleIdentifier)){
						throw new Exception('Need module to delete');			
					}			
					$repository->deleteModule((string)$this->subject->moduleIdentifier);
					$this->result = json_encode(array("r"=>0));
					break;
	
				case ProtocolHandler::GET_DEVELOPERS:
					$res = $repository->getDevelopers();
					$this->result = json_encode(array("r"=>$res));
					break;
					
				default:
					throw new Exception('Unknown Commandidentifier: '.$this->subject->c);
			}
		}

		public function getResult(){
			if (isset($this->result))
				return $this->result;
		}
	}

?>