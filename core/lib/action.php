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
		
		/**
		 * Create Action
		 * 
		 * This method creates a new Action and returns it.
		 * You can create an action based on either:
		 * 1. A Site Id 
		 * 2. An URL
		 * 3. A widgetId combined with a SpaceId (Both applies to the site the menu is showed in)
		 * If the combination is not valid this function will return null and not do anything in db
		 * The action will be inserted with the lowest order (execution priority)
		 * 
		 * @param ActionList $actionList = null The ActionList this action should be created in.
		 * @param int $siteId = null The Site the Action should link to
		 * @param string $url = null The SiteURL the Action should link to
		 * @param int $widgetId = null The Widget that should be loaded into a specific space (only valid with $spaceId)
		 * @param int $spaceId = null The Space id that the widget of $widgetId should be loaded into (only valid with $widgetId)
		 * @return Action The created Action
		 */
		public function createAction($actionList=null,$siteId=null, $url=null, $widgetId=null, $spaceId=null){
			if(!isset($actionList)){
				return null;
			}
			$core = Core::getInstance();
			$action = new Action();
			$action->setActionListId($actionList->getId());
			if (isset($siteId)){
				$compositeManager = $core->getCompositeManager();
				$site = $compositeManager->getSite($siteId);
				if ($site != null){
					$action->setSiteId($siteId,true);
				}else{
					return null;
				}
			}else if (isset($url)){
				$action->setUrl((string)$url,true);
			}else if (isset($widgetId) and isset($spaceId)){
				$compositeManager = $core->getCompositeManager();
				$widget = $compositeManager->getWidget($widgetId);
				if ($widget != null){
					$action->setWidgetSpaceConstellation($widgetId, $spaceId,true);
				}else{
					return null;
				}
			}else{
				return null;
			}
			$action->setName("new action",true);
			$db = $core->getDB();
			$newId = $db->getSeqNext('ACT_GEN');
			$orderres = $db->query($core,"SELECT MAX(ACT_ORDER) AS MAXORDER FROM ACTIONS WHERE ACT_ATL_ID = ? ;",array($action->getActionListId()));
			if ($orderset = $db->fetchObject($orderres)){
				$newOrder = $orderset->MAXORDER+1;
			}else{
				$newOrder = 0;
			}
			$action->setId($newId);
			$action->setOrder($newOrder);
			$db->query($core,"INSERT INTO ACTIONS VALUES (?,?,?,?,?,?,?,?)", 
						array($action->getId(),$action->getName(), $action->getActionListId(),
							  $action->getSiteId(), $action->getUrl(), $action->getSpace(),
							  $action->getWidgetId(), $action->getOrder()));
			return $action;
		}
		
		/**
		 * Create ActionList
		 * 
		 * This function creates a new ActionList
		 * 
		 * @param string $actionListName = "new actionlist" The name of the new ActionList
		 * @return ActionList The created ActionList
		 */
		public function createActionList($actionListName = "new actionlist"){
			$actionList = new ActionList();
			$actionList->setName($actionListName);
			$core = Core::getInstance();
			$db = $core->getDB();
			$actionList->setId($db->getSeqNext('ATL_GEN'));
			$db->query($core, "INSERT INTO ACTIONLISTS VALUES (?,?);",array($actionList->getId(),$actionList->getName()));
			return $actionList;
		}
		
		/**
		 * Create MenuItem
		 * 
		 * This function creates a new MenuItem based on either:
		 * 1. A parent Menu or
		 * 2. A parent MenuItem
		 * If none of those is set, the function will abort and return null
		 * The MenuItem will be spawned with the lowest display order
		 * 
		 * @param Menu $menu = null The parent Menu 
		 * @param MenuItem $menuItemParent = null The parent MenuItem
		 * @param string $name = "new item" The name the MenuItem is spwaned with
		 * @return MenuItem The created MenuItem
		 */
		
		public function createMenuItem($menu=null,$menuItemParent=null, $name="new item"){
			if (!isset($menu) and !isset($menuItemParent)){
				return null;
			}
			$core = Core::getInstance();
			$db = $core->getDB();
			$menuItem = new MenuItem();
			$menuItem->setName($name);
			if (isset($menu)){
				$menuItem->setMenuId($menu->getId());
				$orderres = $db->query($core, 
									   "SELECT MAX(MNI_ORDER) AS MAXORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? ;",
									   array($menu->getId()));
			}
			if (isset($menuItemParent)){
				$menuItem->setParentMenuItemId($menuItemParent->getId());
				$orderres = $db->query($core, 
									   "SELECT MAX(MNI_ORDER) AS MAXORDER FROM MENUITEMS WHERE MNI_MNI_ID = ? ;",
									   array($menuItemParent->getId()));
			}
			$menuItem->setId($db->getSeqNext('MNI_GEN'));
			if ($orderset = $db->fetchObject($orderres)){
				$newOrder = $orderset->MAXORDER+1;
			}else{
				$newOrder = 0;
			}
			$menuItem->setOrder($newOrder);
			$db->query($core ,"INSERT INTO MENUITEMS VALUES (?,?,?,?,?,?) ;",
						array($menuItem->getId(), $menuItem->getName(),
						$menuItem->getMenuId(), $menuItem->getParentMenuItemId(),
						null, $menuItem->getOrder()));
		    $db->commit();
			$actionList = $this->createActionList();
			$menuItem->assignActionList($actionList);
			return $menuItem;
		}

		/**
		 * Create Menu
		 * 
		 * This function creates a menu.
		 * 
		 * @param string $name = "new menu" The name of the new menu
		 * @return Menu The created Menu
		 */
		public function createMenu($site,$name="new menu"){
			$core = Core::getInstance();
			$db = $core->getDB();
			$menu = new Menu();
			$menu->setId($db->getSeqNext('MNU_GEN'));
			$menu->setName($name);
			$db->query($core,"INSERT INTO MENUS (MNU_ID,MNU_NAME, MNU_SIT_ID) VALUES (?,?, ?) ;",array($menu->getId(), $menu->getName(), $site->getId()));
			#$db->query($core,"UPDATE SITES SET SIT_MNU_ID = ? WHERE SIT_ID = ?;", array($menu->getId(), $site->getId()));
			return $menu;
		}
		
		/**
		 * Get Action By Id
		 * 
		 * This function looks for an Action with the given ID in the database
		 * and returns it
		 * If the action does not exist this returns null 
		 * 
		 * @param int $actionId The ID of the Action to look for
		 * @return Action The Action or null
		 */
		public function getActionById($actionId){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core, "SELECT ACT_NAME, ACT_ATL_ID, ACT_SIT_ID, 
												ACT_SPACE, ACT_WGT_ID, ACT_URL, ACT_ORDER
											 FROM ACTIONS WHERE ACT_ID = ?;", array($actionId));
			if ($set = $db->fetchObject($res)) {
				$action = new Action();
				if (isset($set->ACT_SIT_ID)){
					$action->setSiteId($set->ACT_SIT_ID,true);
				}
				if (isset($set->ACT_URL)){
					$action->setUrl($set->ACT_URL,true);
				}
				if (isset($set->ACT_WGT_ID) and isset($set->ACT_SPACE)){
					$action->setWidgetSpaceConstellation($set->ACT_WGT_ID, $set->ACT_SPACE,true);
				}
				$action->setId($actionId);
				$action->setName($set->ACT_NAME,true);
				$action->setActionListId($set->ACT_ATL_ID);
				$action->setOrder($set->ACT_ORDER);
				
				return $action;
			}
			return null;	
		}	
		
		/**
		 * Get ActionList By Id
		 * 
		 * This function looks for an ActionList with the given ID in the database
		 * and returns it
		 * If the action does not exist this returns null 
		 * 
		 * @param int $actionListId The ID of the ActionList to look for
		 * @return ActionList The ActionList or null
		 */
		public function getActionListById($actionListId){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core, "SELECT ATL_NAME FROM ACTIONLISTS WHERE ATL_ID = ?;", array($actionListId));
			if ($set = $db->fetchObject($res)){
				$actionList = new ActionList();
				$actionList->setId($actionListId);
				$actionList->setName($set->ATL_NAME,true);
				return $actionList;	
			}
			return null;
		}
		
		/**
		 * Get MenuItem By Id
		 * 
		 * This function looks for a MenuItem with the given ID in the database
		 * and returns it
		 * If the MenuItem does not exist this returns null 
		 * 
		 * @param int $menuItemId The ID of the MenuItem to look for
		 * @return MenuItem The MenuItem or null
		 */
		public function getMenuItemById($menuItemId){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core, "SELECT MNI_NAME, MNI_MNU_ID, MNI_MNI_ID, MNI_ATL_ID, MNI_ORDER FROM MENUITEMS WHERE MNI_ID = ?;",array($menuItemId));
			if ($set = $db->fetchObject($res)){
				$menuItem = new MenuItem();
				$menuItem->setId($menuItemId);
				$menuItem->setName($set->MNI_NAME, true);
				$menuItem->setOrder($set->MNI_ORDER);
				if (isset($set->MNI_MNU_ID)){
					$menuItem->setMenuId($set->MNI_MNU_ID,true);
				}
				if (isset($set->MNI_MNI_ID)){
					$menuItem->setParentMenuItemId($set->MNI_MNI_ID,true);
				}
				if (isset($set->MNI_ATL_ID)){
					$menuItem->setActionListId($set->MNI_ATL_ID);
				}
				return $menuItem;
			}				
			return null;
		}
		
		/**
		 * Get Menu By Id
		 * 
		 * This function looks for a Menu with the given ID in the database
		 * and returns it
		 * If the Menu does not exist this returns null 
		 * 
		 * @param int $menuId The ID of the Menu to look for
		 * @return Menu The Menu or null
		 */
		public function getMenuById($menuId){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core,"SELECT MNU_NAME FROM MENUS WHERE MNU_ID = ? ;",array($menuId));
			if ($set = $db->fetchObject($res)){
				$menu = new Menu();
				$menu->setId($menuId);
				$menu->setName($set->MNU_NAME,true);
				return $menu;
			}
			return null;
		}
	}
	
	/**
	 * Action
	 * 
	 * An Action represents anything that can happen when
	 * using Hyperlinks inside scoville. 
	 * An Action can refer to three different things:
	 * 1. A combination of a Space and a Widget:
	 * 		The Widget will be load into the Space of the current site.
	 * 2. A Site
	 * 		The Site will be load instead of the site currently shown
	 * 3. An URL
	 * 		The User will leave the scoville-Site and navigate to the URL
	 * 
	 * An Action has an execution Order. If an ActionList contains more 
	 * than one Action, the actions will be executed according to priority
	 * starting by low numbers, moving to higher numbers 
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
		
		/**
		 * Set Order
		 * 
		 * Sets the execution order of the Action
		 * Only for use to fetch Actions from Database
		 * Use increaseOrder() or decreaseOrder(), 
		 * moveToTopOrder() or moveToBottomOrder()
		 * to modify
		 * 
		 * @param int $orderNumber The order number coming from database
		 */
		public function setOrder($orderNumber){
			$this->order = $orderNumber;
		}
		
		/**
		 * Get Order
		 * 
		 * Returns the current order number of the action
		 * 
		 * @return int The order number
		 */
		public function getOrder(){
			return $this->order;
		}
		
		public function increaseOrder(){
			//TODO: implement
		}

		public function decreaseOrder(){
			//TODO: implement
		}
		
		public function moveToTopOrder(){
			//TODO: implement 
		}

		public function moveToBottomOrder(){
			//TODO: implement
		}
		
		/**
		 * Set ActionList Id
		 * 
		 * Assigns an ActionListId to the Action
		 * Only for Internal Use while loading the Action from DB
		 * 
		 * @param int $actionListId The Id of the ActionList
		 */
		public function setActionListId($actionListId){
			$this->actionListId =$actionListId;
		}
		
		/**
		 * Set Name
		 *
		 * Sets the Name of the action
		 * 
		 * @param string $name The new Name 
		 */
		public function setName($name, $ignoreDb=true){
			$this->name = (string)$name;
			if (!$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core,"UPDATE ACTIONS SET ACT_NAME = ? WHERE ACT_ID = ?;",array($this->name, $this->getId()));
			}
		}
		
		/**
		 * Get Name
		 *
		 * Returns the Name of the action
		 * 
		 * @return string The Name of the Action 
		 */
		public function getName(){
			return $this->name;
		}
		
		/**
		 * Get ActionList
		 * 
		 * Returns the ActionList this Action is currently assigned To
		 * 
		 * @return ActionList The ActionList of the Action or null
		 */
		public function getActionList(){
			$core = Core::getInstance();
			$am = $core->getActionManager();
			$actionList = $am->getActionListById($this->getActionListId()); 
			return $actionList;
		}
		
		/**
		 * Get ActionList-ID
		 * 
		 * Returns the ID of the ActionList this Action is currently assigned To
		 * 
		 * @return int The ActionListID of the Action or null
		 */
		public function getActionListId(){
			return $this->actionListId;
		}
		
		/**
		 * Set ID
		 * 
		 * Sets the ID of this Action
		 * Dedicated for Internal Use (ID gets set via DB-Sequence)
		 * 
		 * @param int $id The new ID 
		 */
		public function setId($id){
			$this->id = $id;
		}
		
		/**
		 * Get ID
		 * 
		 * Returns the ID of the Action
		 * 
		 * @return int The ActionId
		 */
		public function getId(){
			return $this->id;
		}
		
		/**
		 * Set URL
		 * 
		 * Make this Action an URL-Operation
		 * Resets Widget/Space or Site-attributes of this Action
		 * 
		 * @param string $url The URL to target with this Action
		 */
		public function setUrl($url,$ignoreDb=false){
			$this->url = $url;
			$this->widgetId = null;
			$this->spaceId = null;
			$this->siteId = null;
			
			if(!$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE ACTIONS SET ACT_URL = ?, ACT_SIT_ID = NULL, 
								   ACT_WGT_ID = NULL, ACT_SPACE = NULL WHERE ACT_ID = ?;",
								   array($this->getUrl(),$this->getId()));
			}
		}
		
		/**
		 * Delete
		 * 
		 * Deletes this action from Database
		 */
		public function delete(){
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core,"DELETE FROM ACTIONS WHERE ACT_ID = ?;",array($this->getId()));
		}
		
		/**
		 * Set Widget Space Constellation
		 * 
		 * Make this Action a Widget/Space Action
		 * The Action will load the targetted widget into the given Space when
		 * executed.
		 * Resets Site- and URL-Link-attributes of this Action
		 * 
		 * @param int $widgetId The ID of the targeted Widget
		 * @param int $spaceId The Space that the widget should be placed into
		 */
		public function setWidgetSpaceConstellation($widgetId, $spaceId, $ignoreDb = false){
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
			if (!$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE ACTIONS SET ACT_URL = NULL, ACT_SIT_ID = NULL,
								   ACT_WGT_ID = ?, ACT_SPACE = ? WHERE ACT_ID = ?",
								   array($this->getWidgetId(),$this->getSpace(),$this->getId()));
			}
		}
		
		/**
		 * Set Site ID
		 * 
		 * Make This action a Site-Link that links
		 * to another Scoville-Site.
		 * Resets Widget/Site- and URL-Linkattributes
		 * 
		 * @param int $siteId
		 */
		public function setSiteId($siteId,$ignoreDb=false){
			$core = Core::getInstance();
			if ($core->getCompositeManager()->getSite($siteId) != null){
				$this->siteId = $siteId;
				$this->widgetId = null;
				$this->spaceId = null;
				$this->url = null;	
			}
			
			if(!$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE ACTIONS SET ACT_URL = NULL, ACT_SIT_ID = ?, 
								   ACT_WGT_ID = NULL, ACT_SPACE = NULL WHERE ACT_ID = ?;",
								   array($this->getSiteId(),$this->getId()));
			}
		}
		
		/**
		 * Unset Links
		 * 
		 * Resets all links that are represented by this Action
		 */
		public function unsetLinks(){
			$this->siteId = null;
			$this->widgetId = null;
			$this->spaceId = null;
			$this->url = null;
		}
		
		/**
		 * Get WidgetId
		 * 
		 * Returns The widgetId assigned to This Action (only set when in Widget/Space-Mode)
		 * otherwise null
		 * 
		 * @return int The Widget ID
		 */
		public function getWidgetId(){
			return $this->widgetId;
		}
		
		/**
		 * Get Space
		 * 
		 * Returns The Space assigned to this Action (only set when in Widget/Space-Mode)
		 * otherwise null
		 * 
		 * @return int The Spacenumber
		 */
		public function getSpace(){
			return $this->spaceId;
		}
		
		/**
		 * Get SiteID
		 * 
		 * Returns the Site-ID of the site assigned to this Action (only in Site-Mode)
		 * otherwise null
		 * 
		 * @return int The SiteID
		 */
		public function getSiteId(){
			return $this->siteId;
		}
		
		/**
		 * Get URL
		 * 
		 * Returns the URL assigned to this action (only in URL-Mode)
		 * otherwise null
		 * 
		 * @return string The URL
		 */
		public function getUrl(){
			return $this->url;
		}
		
		/**
		 * Get Type
		 * 
		 * Returns the type of this action wich may be
		 * 'url', 'site' or 'widgetSpaceConstellation'
		 * if incostistent, returns null
		 * 
		 * @return string The Type
		 */
		public function getType(){
			if (isset($this->url)){
				return 'url';
			}elseif (isset($this->widgetId) and isset($this->spaceId)){
				return 'widgetSpaceConstellation';
			}elseif (isset($this->siteId)){
				return 'site';
			}else{
				return null;
			}
		}

	}

	/**
	 * ActionList
	 * 
	 * An ActionList Represents a bunch of actions That
	 * will be executed when the ActionList is invoked
	 * ActionLists can be assigned to MenuItems.
	 * If an ActionList is executed, the Actions are
	 * executed by a priority-order that can be set via
	 * functions in the Action-Objects
	 */
	class ActionList  {
		function __const(){
			$this->children = array();
			$this->id = null;
			$this->name = null;
		}
		
		/**
		 * Delete
		 * 
		 * Deletes the ActionList from the DB
		 */
		public function delete(){
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core, "DELETE FROM ACTIONLISTS WHERE ATL_ID = ?;", array($this->getId()));
		}
		
		/**
		 * Set Name
		 * 
		 * Sets the Name of the actionList
		 * 
		 * @param string $name The new Name
		 */
		public function setName($name, $ignoreDb = false){
			$this->name = (string)$name;
			if (isset($this->id) and !$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE ACTIONLISTS SET ATL_NAME = ? WHERE ATL_ID = ?;", array($this->name, $this->getId()));
			}
		}
		
		/**
		 * Get Name
		 * 
		 * Returns the current Name of the ActionList
		 * 
		 * @return string Name of the ActionList
		 */
		public function getName(){
			return $this->name;
		}
		
		/**
		 * Set ID
		 * 
		 * Sets the ID of the ActionList
		 * Internal use Only (ID gets set with DB-generator while creation)
		 * 
		 * @param int $id The new Id of the ActionList
		 */
		public function setId($id){
			$this->id = (int)$id;
		}
		
		/**
		 * Get ID
		 * 
		 * Returns the ID of the ActionList
		 * 
		 * @return int The ID of the actionList
		 */
		public function getId(){
			return $this->id;
		}
		
		/**
		 * Add Action
		 * 
		 * This function adds an Action to this ActionList
		 * if $action is an integer, it will be handled as actionId
		 * the action will only be added if it is not already a part
		 * of this ActionList
		 * 
		 * @param Action $action The Action or action Id to add
		 param */
		public function addAction($action){
			$core = Core::getInstance();
			if (is_int($action)){
				$action = $core->getActionManager()->getActionById($action);
			}
			//TODO: Klasse pruefen
			if (!in_array($action,$this->children)){
				$this->children[] = $action;	
				$db = $core->getDB();
				$db->query($core,"UPDATE ACTIONS SET ACT_ATL_ID = ? WHERE ACT_ID = ?;",
						   array($this->getId(),$action->getId()));
			}
		}
		
		/**
		 * Has Action?
		 * 
		 * Tests whether this ActionList has the given action by 
		 * comparing Action-IDs. Returns true if Action is present
		 * 
		 * @param Action $action The Action to Test for
		 * @return boolean The test result
		 */
		public function hasAction($action){
			foreach ($this->children as $child){
				if ($child->getId() == $action->getId()){
					return true;
				}
			}
			return false;
		}
		
		/**
		 * Remove Action
		 * 
		 * Removes the given action from the ActionList
		 * Only does something if the given action is present in 
		 * this ActionList
		 * 
		 * @param Action $action The action to remove
		 */
		public function removeAction($action){
			if ($this->hasAction($action)){
				foreach ($this->children as $child){
					if ($child->getId() == $action->getId()){
						unset($child);
					}
				}
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE ACTIONS SET ACT_ATL_ID = NULL WHERE ACT_ID = ?;",
						   array($action->getId()));
			}
		}
		
		/**
		 * Load Actions
		 * 
		 * Loads all Actions assigned to this ActionList into the Action
		 */
		
		public function loadActions(){
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core, "SELECT ACT_ID FROM ACTIONS WHERE ACT_ATL_ID = ?;",
					   array($this->getId()));
			$this->children = array();
			$actionManager = $core->getActionManager();
			while($set = $db->fetchObject($res)){
				$this->children[] = $actionManager->getActionById($set->ACT_ID);
			}
		}
		
		/**
		 * Get Actions
		 * 
		 * Returns all Actions assigned to this ActionList
		 * 
		 * @return array The Actions of this ActionList
		 */
		public function getActions(){
			$this->loadActions();
			return $this->children;
		}
		
		/**
		 * Get Action By ID
		 * 
		 * Get a specific action of this ActionList by it's ID
		 * Return null if action is not found
		 * 
		 * @param int $actionId The ID of the searched Action
		 * @return Action The action or null if not found
		 */
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
	 * A Menu Item is an item graphically displayed in a Menu
	 * A MenuItem may contain other MenuItems as children
	 * The order-number determines in which order the menuitems are
	 * displayed in their parent element which may be a Menu or another
	 * MenuItem order goes from low to higher numbers
	 * 
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
		
		/**
		 * Delete
		 * 
		 * Deletes this MenuItem from DB
		 */
		public function delete(){
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core, "DELETE FROM MENUITEMS WHERE MNI_ID = ?;", array($this->getId()));
		}
		
		/**
		 * Set Order
		 * 
		 * Sets the display-ordernumber of this MenuItem
		 * Internal use only. 
		 * 
		 * Use increaseOrder() decreaseOrder(),
		 * moveToTopOrder() or moveToBottomOrder()
		 * to modify Order.
		 * 
		 * @param int $order The order number
		 */
		public function setOrder($order){
			$this->order = (int)$order;
		}
		
		/**
		 * Get Order
		 * 
		 * Returns the current Order number of this MenuItem
		 * 
		 * @return int The Order number
		 */
		public function getOrder(){
			return $this->order;
		}
			
		public function increaseOrder(){
			//TODO: implement
			$core = Core::getInstance();
			$db = $core->getDB();
			if ($this->getMenuId()!=null){
				$res = $db->query($core, "SELECT MIN(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? AND MNI_ORDER > ? ;", 
								  array($this->getMenuId(),$this->getOrder()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ?", array($tempOrder, $set->NEWORDER, $this->getMenuId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
					$db->commit();
				}
			}else if ($this->getParentMenuItemId()!=null){
				$res = $db->query($core, "SELECT MIN(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNI_ID = ? AND MNI_ORDER > ? ;", 
								  array($this->getParentMenuItemId(),$this->getOrder()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ?", array($tempOrder, $set->NEWORDER, $this->getParentMenuItemId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
					$db->commit();
				}
			}
		}

		public function decreaseOrder(){
			//TODO: implement
			$core = Core::getInstance();
			$db = $core->getDB();
			if ($this->getMenuId()!=null){
				$res = $db->query($core, "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? AND MNI_ORDER < ? ;", 
								  array($this->getMenuId(),$this->getOrder()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ?", array($tempOrder, $set->NEWORDER,$this->getMenuId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
					$db->commit();
				}
			}else if ($this->getParentMenuItemId()!=null){
				$res = $db->query($core, "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNI_ID = ? AND MNI_ORDER < ? ;", 
								  array($this->getParentMenuItemId(),$this->getOrder()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ?", array($tempOrder, $set->NEWORDER,$this->getParentMenuItemId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
					$db->commit();
				}
			}else{
				return;
			}
			
		}
		
		public function moveToTopOrder(){
			//TODO: implement
			$core = Core::getInstance();
			$db = $core->getDB();
			if ($this->getMenuId()!=null){
				$res = $db->query($core, "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ?;", 
								  array($this->getMenuId()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ?", array($tempOrder, $set->NEWORDER, $this->getMenuId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
				}
			}else if ($this->getParentMenuItemId()!=null){
				$res = $db->query($core, "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNI_ID = ?;", 
								  array($this->getParentMenuItemId()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ?", array($tempOrder, $set->NEWORDER, $this->getParentMenuItemId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
				}
			}
		}

		public function moveToBottomOrder(){
			//TODO: implement
			$core = Core::getInstance();
			$db = $core->getDB();
			if ($this->getMenuId()!=null){
				$res = $db->query($core, "SELECT MIN(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ?;", 
								  array($this->getMenuId()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ?", array($tempOrder, $set->NEWORDER, $this->getMenuId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
				}
			}else if ($this->getParentMenuItemId()!=null){
				$res = $db->query($core, "SELECT MIN(MNI_ORDER) AS NEWORDER, MNI_ID FROM MENUITEMS WHERE MNI_MNI_ID = ?;", 
								  array($this->getParentMenuItemId()));
				if ($set = $db->fetchObject($res)){
					if(!isset($set->NEWORDER)){
						return;
					}
					$tempOrder = $this->getOrder();
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ?", array($tempOrder, $set->NEWORDER, $this->getParentMenuItemId()));
					$db->query($core, "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ?", array($set->NEWORDER, $this->getId()));
				}
			}
		}
		
		/**
		 * Set ActionList
		 * 
		 * Set the ActionList assigned to this MenuItem directly
		 * Internal Use only
		 * 
		 * Use assignActionList() to modify this MenuItem's actionlist
		 * 
		 * @param int $actionListId The ID of the ActionList to assign
		 */
		public function setActionListId($actionListId){
			$this->actionListId = (int)$actionListId;
		}
		
		/**
		 * Get Action List
		 * 
		 * Returns the ActionList that is currently assigned to this MenuItem
		 * if there is no Action list return null
		 * 
		 * @return ActionList The ActionList of this MenuItem
		 */
		public function getActionList(){
			
			if ($this->actionList == null or $this->actionList->getId() != $this->actionListId){
				$core = Core::getInstance();
				$am = $core->getActionManager();
				$this->actionList = $am->getActionListById($this->getActionListId());
			}
			return $this->actionList;
		}
		
		/**
		 * Get ActionList-ID
		 * 
		 * Return the id of the ActionList that is currently assigned to this MenuItem
		 * If there is no ActionList assigned, returns null
		 * 
		 * @return int The ActionList Id
		 */
		public function getActionListId(){
			return $this->actionListId;
		}
		
		/**
		 * Set Menu ID
		 * 
		 * Assign this MenuItem to a Menu
		 * Resets assignments to a parentMenuItem
		 * 
		 * @param int $menuId The menuId
		 */
		public function setMenuId($menuId,$ignoreDb = false){
			$this->menuId = (int)$menuId;
			$this->parentMenuItem = null;
			$this->parentMenuItemId = null;
			if($this->getId()!=null and !$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core,"UPDATE MENUITEMS SET MNI_MNU_ID = ?, MNI_MNI_ID = NULL WHERE MNI_ID = ?",
								 array($this->menuId, $this->getId()));
			}
			
		}
		
		/**
		 * Get Menu
		 * 
		 * Returns the Menu this MenuItem is assigned To
		 * Returns null if not assigned to a Menu but to a submenu
		 * 
		 * @return int The Menu this MenuItem is Assigned to
		 */
		public function getMenu(){
			if ($this->menu == null or $this->menu->getId() != $this->menuId){
				$core = Core::getInstance();
				$am = $core->getActionManager();
				$this->menu = $am->getMenuById($this->getMenuId());
			}
			return $this->menu;
		}
		
		/**
		 * Get Menu ID
		 * 
		 * Returns the ID of the Menu this MenuItem is assigned To
		 * Returns null if not assigned to a Menu but to another MenuItem
		 * 
		 * @return int The MenuId of the Menu this MenuItem is Assigned to
		 */
		public function getMenuId(){
			return $this->menuId;
		}
		
		/**
		 * Set Parent Menu Item Id
		 * 
		 * Assigns this MenuItem to a parent MenuItem
		 * Resets any relations this MenuItem has to a Menu
		 * 
		 * @param int $parentMenuItemId The Parent MenuItem for this MenuItem
		 */
		public function setParentMenuItemId($parentMenuItemId, $ignoreDb=false){
			$this->parentMenuItemId = $parentMenuItemId;
			$this->menu = null;
			$this->menuId = null;
			if($this->getId()!=null and !$ignoreDb){
			    $core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core,"UPDATE MENUITEMS SET MNI_MNI_ID = ?, MNI_MNU_ID = NULL WHERE MNI_ID = ?",
								 array($this->parentMenuItemId, $this->getId()));
			}
		}
		
		/**
		 * Get Parent Menu Item 
		 * 
		 * Returns the MenuItem this MenuItem is assigned to or null if not assigned
		 * 
		 * @return MenuItem The MenuItem this MenuItem is Assigned To
		 */
		public function getParentMenuItem(){
			if ($this->parentMenuItem == null or $this->parentMenuItem->getId() != $this->parentMenuItemId){
				$core = Core::getInstance();
				$am = $core->getActionManager();
				$this->parentMenuItem = $am->getMenuItemById($this->getParentMenuItemId());
			}
			return $this->parentMenuItem;
		}
		
		/**
		 * Get Parent Menu ItemID 
		 * 
		 * Returns the MenuItemID of the MenuItem this MenuItem is assigned to or null if not assigned
		 * 
		 * @return int The Id of the MenuItem this MenuItem is Assigned To
		 */
		public function getParentMenuItemId(){
			return $this->parentMenuItemId;
		}
		
		/**
		 * Set Name
		 * 
		 * Sets the name of this MenuItem
		 * 
		 * @param string $name The name of the MenuItem
		 */
		public function setName($name, $ignoreDb=false){
			$this->name = (string)$name;
			if ($this->getId()!=null and !$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE MENUITEMS SET MNI_NAME = ? WHERE MNI_ID = ?;",array($this->name,$this->getId()));
			}
		}
		
		/**
		 * Get Name
		 * 
		 * Gets the name of the MenuIem
		 * 
		 * @return string the Name of the MenuItem
		 */
		public function getName(){
			return $this->name;
		}
		
		/**
		 * Set ID
		 * 
		 * Sets The id of this MenuItem
		 * Internal use only (ID gets set via DB generator while creation)
		 * 
		 * @param int $id The ID to set
		 */
		public function setId($id){
			$this->id = (int)$id;
		}
		
		/**
		 * Get ID
		 * 
		 * Returns the ID of this MenuItem
		 * 
		 * @return int The ID of this MenuItem
		 */
		public function getId(){
			return $this->id;
		}
		
		/**
		 * Assign an ActionList
		 * 
		 * Assigns an ActionList to this MenuItem
		 * 
		 * @param ActionList $actionList The ActionList to Assign
		 */
		public function assignActionList($actionList){
			$actionListId = $actionList->getId();
			$this->setActionListId($actionListId);
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core, "UPDATE MENUITEMS SET MNI_ATL_ID = ? WHERE MNI_ID = ?;",
					   array($actionListId, $this->getId()));
		}
		
		/**
		 * Add MenuItem
		 * 
		 * Adds a MenuItem as SubMenu-Component to this MenuItem
		 * 
		 * @param MenuItem $menuItem The MenuItem to add
		 */
		public function addMenuItem($menuItem){
			$menuItemId = $menuItem->getId();
			$menuItem->setParentMenuItemId($this->getId());
			
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core, "UPDATE MENUITEMS SET MNI_MNI_ID = ? WHERE MNI_ID = ?; ",
					   array($this->getId(), $menuItemId));
		}
		
		/**
		 * Remove MenuItem
		 * 
		 * Removes a MenuItem (SubmenuItem) assigned to this MenuItem
		 * 
		 * @param MenuItem $menuItem The MenuItem to remove
		 */
		public function removeMenuItem($menuItem){
			$menuItemId = $menuItem->getId();
			$menuItem->setParentMenuItemId(null);
			
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core, "UPDATE MENUITEMS SET MNI_MNI_ID = NULL WHERE MNI_ID = ?; ",
					   array($this->getId(), $menuItemId));
		}
		
		/**
		 * Get MenuItems
		 * 
		 * Returns all (Sub-)MenuItems that are assigned to this MenuItem
		 * 
		 * @return array A array with all submenuItems assigned to this MenuItem
		 */
		public function getMenuItems(){
			//PERFORMANCE-ENHANCE POSSIBLE BY IMPLEMENTING FETCHING IN HERE
			$core = Core::getInstance();
			$actionManager = $core->getActionManager();
			$db = $core->getDB();
			$res = $db->query($core,"SELECT MNI_ID FROM MENUITEMS WHERE MNI_MNI_ID = ?;",array($this->getId()));
			$ret = array();
			while($set = $db->fetchObject($res)){
				$ret[] = $actionManager->getMenuItemById($set->MNI_ID);
			}
			return $ret;
		}
	}
	
	/**
	 * Menu
	 * 
	 * A Menu represents a structure that contains MenuItems
	 * It is the root-element of any navigation-structure
	 */
	class Menu  {
		private $children = array();
		
		function __const(){
			$this->id = null;
			$this->name = null;
			$this->siteId = null;
			$this->site = null;
			
			$this->menuItemsInitialized = false;
		}
		
		/**
		 * Set Site Id
		 * 
		 * Set the Id of the Site this menu belongs to
		 * 
		 * @param int $siteId The SiteID
		 */
		public function setSiteId($siteId){
			$this->siteId = (int)$siteId;
		}
		
		/**
		 * Get Site 
		 * 
		 * Returns the site this Menu belongs To
		 * 
		 * @return Site The Site
		 */
		public function getSite(){
			if ($this->site == null or $this->getSiteId() != $this->site->getId()){
				$core = Core::getInstance();
				$cm = $core->getCompositeManager();
				$this->site = $cm->getSite($this->siteId);
			}
			return $this->site;
		}
		
		/**
		 * Get SiteID
		 * 
		 * Returns The site ID of the site this menu belongs to
		 * 
		 * @return int The SiteID
		 */
		public function getSiteId(){
			return $this->siteId;
		}
		
		/**
		 * Set Name
		 * 
		 * Sets the name of this menu
		 * 
		 * @param string $name The Name of the Menu
		 */
		public function setName($name, $ignoreDb=false){
			$this->name = (string)$name;
			if ($this->getId() != null and !$ignoreDb){
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE MENUS SET MNU_NAME = ? WHERE MNU_ID = ?;", array($this->name, $this->getId()));
			}
		}
		
		/**
		 * Get Name
		 * 
		 * Returns the name of this Menu
		 * 
		 * @return string The name of this menu
		 */
		public function getName(){
			return $this->name;
		}
		
		/**
		 * Set ID
		 * 
		 * Sets the id of this Menu
		 * Internal use only (Id gets set via DB-Generator while creation)
		 * 
		 * @param int $id The ID to set
		 */
		public function setId($id){
			$this->id  = (int)$id;
		}
		
		/**
		 * Get ID
		 * 
		 * Returns the id of this Menu
		 * 
		 * @return int The ID
		 */
		public function getId(){
			return $this->id;
		}
		
		/**
		 * Add MenuItem
		 * 
		 * Adds a MenuItem to this Menu
		 * MenuItem only gets added if its not already assigned here
		 * 
		 * @param MenuItem $menuItem The menuItem to add
		 */
		public function addMenuItem($menuItem){
			//TODO: Class must be MenuItem
			if (!in_array($menuItem, $this->children)){
				$this->children[] = $menuItem;
				$core = Core::getInstance();
				$db = $core->getDB();
				$db->query($core, "UPDATE MENUITEMS SET MNI_MNU_ID = ? WHERE MNI_ID = ? ;",
						   array($this->getId(),$menuItem->getId()));
			}
		}
		
		/**
		 * Loads the menuItems from Database
		 */
		private function loadMenuItems(){
			$this->children = array();
			$core = Core::getInstance();
			$db = $core->getDB();
			$res = $db->query($core,"SELECT MNI_ID FROM MENUITEMS WHERE MNI_MNU_ID = ?;",
							  array($this->getId()));
			$actionManager = $core->getActionManager();
			while($set = $db->fetchObject($res)){
				$this->children[] = $actionManager->getMenuItemById($set->MNI_ID);
			}
			$this->menuItemsInitialized = true;
		}
		/**
		 * Get Menu Item By Id
		 * 
		 * Returns a MenuItem assigned to this menu by a given ID
		 * If this MenuItem does not exist, returns null
		 * 
		 * @return MenuItem The menuitem searched for or null
		 */
		public function getMenuItemById($menuItemId){
			if (!$this->menuItemsInitialized){
				$this->loadMenuItems();
			}
			foreach($this->children as $item){
				if ($item->getId() == $menuItemId){
					return $item;
				}
			}
			return null;
		}
		
		/**
		 * Get MenuItems
		 * 
		 * Returns all MenuItems assigned to this Menu
		 * 
		 * @return array An array of MenuItems
		 */
		public function getMenuItems(){
			//PERFORMANCE-ENHANCE POSSIBLE BY IMPLEMENTING FETCHING IN HERE
			if (!$this->menuItemsInitialized){
				$this->loadMenuItems();
			}
			
			return $this->children;
		}
		
		/**
		 * Remove Menu Item
		 * 
		 * Removes a MenuItem from this Menu
		 * 
		 * @param MenuItem $menuItem The MenuItem To remove
		 */
		public function removeMenuItem($menuItem){
			$menuItemId = $menuItem->getId();
			$menuItem->setParentMenuItemId(null);
			
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core, "UPDATE MENUITEMS SET MNI_MNU_ID = NULL WHERE MNI_ID = ?; ",
					   array($this->getId(), $menuItemId));
		}
		
		public function delete(){
			$core = Core::getInstance();
			$db = $core->getDB();
			$db->query($core, "DELETE FROM MENUS WHERE MNU_ID = ? ;", array($this->getId()));
			$db->commit();
		}
	}