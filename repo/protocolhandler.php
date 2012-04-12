<?php
	include_once('repository.php');
	
	class ProtocolHandler  {
		const GET_ALL_MODULES = 1;
		const GET_VERSIONS_OF_MODULE = 2;
		const RESOLVE_DEPENDENCIES_DOWNWARDS = 3;
		const RESOLVE_DEPENDENCIES_UPWARDS = 4;
		const DOWNLOAD_MODULE = 5;
		
		const AUTHENTICATE = 100;
		const LOGOUT = 101;
		const CHANGE_PASSWORD = 102;
		const REGISTER_DEVELOPER = 103;
		const UNREGISTER_DEVELOPER = 104;
		const UPLOAD_MODULE = 105;
		const DELETE_MODULE = 106;
		
		public function __construct($json){
			$this->subject = json_decode($json);
			$this->result = null;
			if ($this->subject == null){
				throw Exception('Invalid Json');
			}
		}
		
		private function verifyModule(){
			if (!isset($this->subject->m) or 
				!isset($this->subject->m->name) or
				!isset($this->subject->m->hrname) or
				!isset($this->subject->m->version_major) or 
				!isset($this->subject->m->version_minor) or
				!isset($this->subject->m->revision) or
				!isset($this->subject->m->md5) ){
				throw Exception('Not a valid Module!');
			}
			
		}
		
		public function execute(){
			$repository = Repository::getInstance();
			switch($this->subject->c){
				case ProtocolHandler::GET_ALL_MODULES:
					$repository->getAllModules();
					break;
				case ProtocolHandler::GET_VERSIONS_OF_MODULE:
					$this->verifyModule();
					$repository->getVersionsOfModule($this->subject->m);
					break;
				case ProtocolHandler::RESOLVE_DEPENDENCIES_DOWNWARDS:
					$this->verifyModule();
					$repository->resolveDependenciesDownwards($this->subject->m);
					break;
				case ProtocolHandler::RESOLVE_DEPENDENCIES_UPWARDS:
					$this->verifyModule();
					$repository->resolveDependenciesUpwards($this->subject->m);
					break;
				case ProtocolHandler::DOWNLOAD_MODULE:
					$this->verifyModule();
					$repository->downloadModule($this->subject->m);
					break;
					
					
				case ProtocolHandler::AUTHENTICATE:
					if (!isset($this->subject->dxd)){
						throw Exception('Password not set');
					}
					$repository->authenticate($this->subject->dxd);
					break;
				case ProtocolHandler::LOGOUT:
					$repository->logout();
					break;
				case ProtocolHandler::CHANGE_PASSWORD:
					$repository->changePassword();
					break;
				case ProtocolHandler::REGISTER_DEVELOPER:
					$repository->registerDeveloper();
					break;
				case ProtocolHandler::UNREGISTER_DEVELOPER:
					$repository->unregisterDeveloper();
					break;
				case ProtocolHandler::UPLOAD_MODULE:
					$repository->registerDeveloper();
					break;
				case ProtocolHandler::DELETE_MODULE:
					$repository->registerDeveloper();
					break;
				case ProtocolHandler::REGISTER_DEVELOPER:
					$repository->registerDeveloper();
					break;
				default:
					throw Exception('Unknown Commandidentifier: '.$this->subject->c);
			}
		}

		public function getResult(){
			if (isset($this->result))
				return $this->result;
		}
	}

?>