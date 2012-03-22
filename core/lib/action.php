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
		
		public function createAction($siteId, $url, $widgetId, $spaceId){
			
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
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core, "SELECT ACT_NAME, ACT_ATL_ID, ACT_SIT_ID, 
												ACT_SPACE, ACT_WGT_ID, ACT_URL, ACT_ORDER
											 FROM ACTIONS WHERE ACT_ID = ?;", array($actionId));
			if ($set = $db->fetchObject($res)) {
				$action = new Action();
				if (isset($set->ACT_SIT_ID)){
					$action->setSiteId($set->ACT_SIT_ID);
				}
				if (isset($set->ACT_URL)){
					$action->setUrl($set->ACT_URL);
				}
				if (isset($set->ACT_WGT_ID) and isset($set->ACT_SPACE)){
					$action->setWidgetSpaceConstellation($set->ACT_WGT_ID, $set->ACT_SPACE);
				}
				$action->setId($actionId);
				$action->setName($set->ACT_NAME);
				$action->setActionListId($set->ACT_ATL_ID);
				$action->setOrder($set->ACT_ORDER);
				
				return $action;
			}
			return null;	
		}	
		
		public function getActionListById($actionListId){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core, "SELECT ATL_NAME FROM ACTIONLISTS WHERE ATL_ID = ?;", array($actionListId));
			if ($set = $db->fetchObject($res)){
				$actionList = new ActionList();
				$actionList->setId($actionListId);
				$actionList->setName($set->ATL_NAME);
				return $actionList;	
			}
			return null;
		}
		
		public function getMenuItemById($menuItemId){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core, "SELECT MNI_NAME, MNI_MNU_ID, MNI_MNI_ID, MNI_ATL_ID, MNI_ORDER WHERE MNI_ID = ?;",array($menuItemId));
			if ($set = $db->fetchObject($res)){
				$menuItem = new MenuItem();
				$menuItem->setId($menuItemId);
				$menuItem->setName($set->MNI_NAME);
				$menuItem->setOrder($set->MNI_ORDER);
				if (isset($set->MNI_MNU_ID)){
					$menuItem->setMenuId($set->MNI_MNU_ID);
				}
				if (isset($set->MNI_MNI_ID)){
					$menuItem->setParentMenuItemId($set->MNI_MNI_ID);
				}
				if (isset($set->MNI_ATL_ID)){
					$menuItem->setActionListId($set->MNI_ATL_ID);
				}
			}				
			return null;
		}
		
		public function getMenuById($menuId){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core,"SELECT MNU_NAME FROM MENU WHERE MNU_ID = ? ;",array($menuId));
			if ($set = $db->fetchObject($res)){
				$menu = new Menu();
				$menu->setId($menuId);
				$menu->setName($set->MNU_NAME);
				return $menu;
			}
			return null;
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
			
			$this->name = null;
			$this->order = null;
			$this->actionListId = null;
			$this->order = null;
		}
		
		public function setOrder($orderNumber){
			$this->order = $orderNumber;
		}
		
		public function getOrder(){
			return $this->order;
		}
		
		public function setActionListId($actionListId){
			$this->actionListId =$actionListId;
		}
		
		public function setName($name){
			$this->name = $name;
		}
		
		public function getName(){
			return $this->name;
		}
		
		public function getActionList(){
			$core = Core::getInstance();
			$am = $core->getActionManager();
			$actionList = $am->getActionListById($this->getActionListId()); 
			return $actionList;
		}
		
		public function getActionListId(){
			return $this->actionListId;
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
			$this->siteId = null;
			$this->widgetId = null;
			$this->spaceId = null;
			$this->url = null;
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
			$this->id = null;
			$this->name = null;
		}
		
		public function delete(){
			//TODO: Implement
		}
		
		public function setName($name){
			$this->name = $name;
		}
		
		public function getName(){
			return $this->name;
		}
		
		public function setId($id){
			$this->id = $id;
		}
		
		public function getId(){
			return $this->id;
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
			$this->id = null;
			$this->name =null;
			$this->actionListId = null;
			$this->actionList = null;
			$this->menuId = null;
			$this->menu = null;
			$this->parentMenuItemId = null;
			$this->parentMenuItem = null;
			$this->order = null;
		}
		
		public function render(){
			//TODO: Implement
		}
		
		public function delete(){
			//TODO: Implement
		}
		
		public function setOrder($order){
			$this->order = (int)$order;
		}
		
		public function getOrder(){
			return $this->order;
		}
		
		public function setActionListId($actionListId){
			$this->actionListId = (int)$actionListId;
		}
		
		public function getActionList(){
			
			if ($this->actionList == null or $this->actionList->getId() != $this->actionListId){
				$core = Core::getInstance();
				$am = $core->getActionManager();
				$this->actionList = $am->getActionListById($this->getActionListId());
			}
			return $this->actionList;
		}
		
		public function getActionListId(){
			return $this->actionListId;
		}
		
		public function setMenuId($menuId){
			$this->menuId = $menuId;
		}
		
		public function getMenu(){
			if ($this->menu == null or $this->menu->getId() != $this->menuId){
				$core = Core::getInstance();
				$am = $core->getActionManager();
				$this->menu = $am->getMenuById($this->getMenuId());
			}
			return $this->menu;
		}
		
		public function getMenuId(){
			return $this->menuId;
		}
		
		public function setParentMenuItemId($parentMenuItemId){
			$this->parentMenuItemId = $parentMenuItemId;
		}
		
		public function getParentMenuItem(){
			if ($this->parentMenuItem == null or $this->parentMenuItem->getId() != $this->parentMenuItemId){
				$core = Core::getInstance();
				$am = $core->getActionManager();
				$this->parentMenuItem = $am->getMenuItemById($this->getParentMenuItemId());
			}
			return $this->parentMenuItem;
		}
		
		public function getParentMenuItemId(){
			return $this->parentMenuItemId;
		}
		
		public function setName($name){
			$this->name = $name;
		}
		
		public function getName(){
			return $this->name;
		}
		
		public function setId($id){
			$this->id = $id;
		}
		
		public function getId($id){
			return $this->id;
		}
		
		public function assignActionList($actionList){
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
			$this->id = null;
			$this->name = null;
		}
		
		public function setName($name){
			$this->name = (string)$name;
		}
		
		public function getName(){
			return $this->name;
		}
		
		public function setId($id){
			$this->id  = (int)$id;
		}
		
		public function getId($id){
			return $this->id;
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