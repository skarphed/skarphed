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
			if (ActionManager::$instance==null){
				ActionManager::$instance = new ActionManager();
				ActionManager::$instance->init();
			}
			return ActionManager::$instance;
		}
		
		protected function init(){}

		private $currentParent = null;

		public function createAction(){
			//TODO: Implement
		}
		
		public function createActionList(){
			//TODO: Implement
		}
		
		public function createMenuItem(){
			//TODO: Implement
		}
		
		public function createMenu(){
			//TODO: Implement
		}
		
		
		
		public function getActionById($actionId){
			//TODO: Implement	
		}	
		
		public function getActionListById($actionListId){
			//TODO: Implement
		}
		
		public function getMenuItemById($menuItemId){
			//TODO: Implement
		}
		
		public function getMenuById($menuId){
			//TODO: Implement
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
			$this->id = null;
			
			$this->widgetId = null;
			$this->spaceId =null;
			
			$this->siteId = null;
			$this->url = null;
		}
		
		public function setId($id){
			$this->id = $id;
		}
		
		public function getId(){
			return $this->id;
		}
		
		public function setUrl($url){
			$this->url = $url;
			//TODO: Implement SQL-shit
		}
		
		public function delete(){
			//TODO: Implement
		}
		
		public function setWidgetSpaceConstellation($widgetId, $spaceId){
			if (isset($widgetId) and isset($spaceId)){
				$core = Core::getInstance();
				//if ($core->getCompositeManager()->getWidget($widgetId) and
				//	)
				//TODO: Ueberpreufung nach widget- und spaceexistenz
				$this->widgetId = $widgetId;
				$this->spaceId = $spaceId;
				$this->url = null;
				$this->siteId = null;
			}
			//TODO: Implement Sql-shit
		}
		
		public function setSiteId($siteId){
			$core = Core::getInstance();
			if ($core->getCompositeManager()->getSite($siteId) != null){
				$this->siteId = $siteId;
				$this->widgetId = null;
				$this->spaceId = null;
				$this->url = null;	
			}
			//TODO: Implement
		}
		
		public function unsetLinks(){
			//TODO: Implement
		}

	}

	/**
	 * ActionList
	 * 
	 * An action represents anything that can happen when
	 * using Hyperlinks inside scoville. 
	 */
	class ActionList  {
		function __const(){
			//TODO: Implement
			$this->children = array();
		}
		
		public function delete(){
			//TODO: Implement
		}
		
		public function addAction($action){
			if (is_int($action)){
				$core = Core::getInstance();
				$action = $core->getActionManager()->getActionById($action);
			}
			//TODO: Klasse pruefen
			if (!in_array($action,$this->children)){
				$this->children[] = $action;	
				//TODO SQL-Krempel	
			}
		}
		
		public function removeAction($action){
			//TODO: Implement
			
		}
		
		public function getActions(){
			return $this->children;
		}
		
		public function getActionById($actionId){
			foreach ($this->children as $child){
				if ($child->getId() == $actionId){
					return $child;
				}
			}
			return null;
		}

	}
	
	/**
	 * MenuItem
	 * 
	 * An action represents anything that can happen when
	 * using Hyperlinks inside scoville. 
	 */
	class MenuItem  {
		function __const(){
			//TODO: Implement
		}
		
		public function render(){
			//TODO: Implement
		}
		
		public function delete(){
			//TODO: Implement
		}
		
		public function setActionList($actionList){
			//TODO: Implement
		}
		
		public function getActionList(){
			//TODO: Implement
		}
		
		public function addMenuItem(){
			//TODO: Implement
		}
		

	}
	
	/**
	 * Menu
	 * 
	 * An action represents anything that can happen when
	 * using Hyperlinks inside scoville. 
	 */
	class Menu  {
		private $children = array();
		
		function __const(){
		}
		
		
		public function addMenuItem($menuItem){
			//TODO: Class must be MenuItem
			if (!in_array($menuItem, $this->children)){
				$this->children[] = $menuItem;
			}
		}
		
		public function getMenuItemById($menuItemId){
			foreach($this->children as $item){
				if ($item->getId() == $menuItemId){
					return $item;
				}
			}
			return null;
		}
		
		public function getMenuItems(){
			//TODO: Implement
		}

	}