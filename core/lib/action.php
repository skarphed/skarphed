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
	namespace scv;

	include_once("core.php");
	
	class ActionException extends \Exception{}

	/**
	 * ActionManager
	 * 
	 * Manages Exceptions. 
	 */
	class ActionManager extends Singleton  {
		private static $instance = null;
	
		public static function getInstance(){
			if (OperationManager::$instance==null){
				OperationManager::$instance = new OperationManager();
				OperationManager::$instance->init();
			}
			return OperationManager::$instance;
		}
		
		protected function init(){}

		private $currentParent = null;

		public function createAction(){
			
		}
		
		public function getActionById(){
			
		}	
	}

	
	
	/**
	 * Action
	 * 
	 * An action represents anything that can happen when
	 * using Hyperlinks inside scoville. 
	 */
	class Action  {
		function __const(){
			
		}
		
		public function render(){
			
		}

	}
