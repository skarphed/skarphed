#!/usr/bin/python
#-*- coding: utf-8 -*-

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

class ActionException(Exception):
    """
    Exceptions for Database-Module
    """
    ERRORS = {
        0:"""Action Exception"""        
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "ACT_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class ActionManager(object):
    """
    Manages Exceptions. 
    """
    def __init__(self, core):
        self._core = core

        Action.set_core(core)
        ActionList.set_core(core)
        MenuItem.set_core(core)
        Menu.set_core(core)

        self.create_action = Action.create_action
        self.create_action_list = ActionList.create_action_list
        self.create_menu_item = MenuItem.create_menu_item
        self.create_menu = Menu.create_menu
        self.get_action_by_id = Action.get_action_by_id
        self.get_action_list_by_id = ActionList.get_action_list_by_id
        self.get_menu_item_by_id = MenuItem.get_menu_item_by_id
        self.get_menu_by_id = Menu.get_menu_by_id

class Action(object):
    """
    An Action represents anything that can happen when
    using Hyperlinks inside scoville. 
    An Action can refer to three different things:
    1. A combination of a Space and a Widget:
            The Widget will be load into the Space of the current site.
    2. A Site
            The Site will be load instead of the site currently shown
    3. An URL
            The User will leave the scoville-Site and navigate to the URL
    
    An Action has an execution Order. If an ActionList contains more 
    than one Action, the actions will be executed according to priority
    starting by low numbers, moving to higher numbers
    """

    @classmethod
    def set_core(cls,core):
        """
        trivial
        """
        cls._core = core

    @classmethod
    def create_action(cls, actionlist=None, page_id=None, url=None, widget_id = None, space_id = None):
        """
        This method creates a new Action and returns it.
        You can create an action based on either:
        1. A Page Id 
        2. An URL
        3. A widgetId combined with a SpaceId (Both applies to the site the menu is showed in)
        If the combination is not valid this function will return null and not do anything in db
        The action will be inserted with the lowest order (execution priority)
        """
        if actionlist is None:
            return None
        action = Action()
        action.set_action_list_id(actionlist.get_id())
        if page_id is not None:
            page =cls._core.get_composite_manager().get_page(page_id)
            if page is not None:
                action.set_page_id(page_id)
            else:
                return None
        elif url is not None:
            action.set_url(str(url),True)
        elif widget_id is not None and space_id is not None:
            widget = cls._core.get_module_manager().get_widget(widget_id)
            if widget is not None:
                action.set_widget_space_constellation(widget_id,space_id,True)
        else:
            return None

        action.set_name("new action",True)
        db = cls._core.get_db()
        new_id = db.get_seq_next("ACT_GEN")
        stmnt = "SELECT MAX(ACT_ORDER) AS MAXORDER FROM ACTIONS WHERE ACT_ATL_ID = ? ;"
        cur = db.query(cls._core, stmnt, (action.get_action_list_id(),))
        row = cur.fetchonemap()
        if row is not None:
            new_order = row["MAXORDER"]+1
        else:
            new_order = 0
        action.set_id(new_id)
        action.set_order(new_order)
        stmnt = "INSERT INTO ACTIONS VALUES (?,?,?,?,?,?,?,?) ;"
        db.query(cls._core , stmnt, (action.get_id(), action.get_name(), action.get_action_list_id(),
                                     action.get_page_id(), action.get_url(), action.get_space(), 
                                     action.get_widget_id(), action.get_order()),commit=True)
        return action

    @classmethod
    def get_action_by_id(cls, action_id):
        """
        This function looks for an Action with the given ID in the database
        and returns it
        If the action does not exist this returns null 
        """
        db = cls._core.get_db()
        stmnt = "SELECT ACT_NAME, ACT_ATL_ID, ACT_SIT_ID, \
                     ACT_SPACE, ACT_WGT_ID, ACT_URL, ACT_ORDER \
                 FROM ACTIONS WHERE ACT_ID = ?;"
        cur = db.query(cls._core,stmnt, (action_id,))
        row = cur.fetchonemap()
        if row is not None:
            action = Action()
            if row.has_key("ACT_SIT_ID"):
                action.set_page_id(row["ACT_SIT_ID"],True)
            if row.has_key("ACT_URL"):
                action.set_url(row["ACT_URL"], True)
            if row.has_key("ACT_WGT_ID") and row.has_key("ACT_SPACE"):
                action.set_widget_space_constellation(row["ACT_WGT_ID"], row["ACT_SPACE"], True)
            action.set_id(row["ACT_ID"])
            action.set_name(row["ACT_NAME"],True)
            action.set_action_list_id(row["ACT_ATL_ID"])
            action.set_order(row["ACT_ORDER"])

            return action

        return None

    def __init__(self,core):
        self._core = core

        self._id = None

        self._widget_id = None
        self._space_id = None

        self._page_id = None
        self._url = None

        self._name = None
        self._order = None
        self._action_list_id = None

    def set_order(self, order_number):
        """
        Sets the execution order of the Action
        Only for use to fetch Actions from Database
        Use increaseOrder() or decreaseOrder(), 
        moveToTopOrder() or moveToBottomOrder()
        to modify
        """
        self._order = int(order_number)

    def get_order(self):
        """
        Returns the current order number of the action
        """
        return self._order

    def increase_order(self):
        """
        Increases the order number of this action and
        decreases the order number of the higher-order action
        """
        db = self._core.get_db()
        stmnt = "SELECT MIN(ACT_ORDER) AS NEWORDER FROM ACTIONS WHERE ACT_ATL_ID = ? AND ACT_ORDER > ? ;"
        cur = db.query(self._core, stmnt, (self.get_action_list_id(),self.get_order()))
        row = cur.fetchonemap()
        if row is not None:
            if row["NEWORDER"] is None:
                return
            temp_order = self.get_order()
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ORDER = ? AND ACT_ATL_ID = ? ;"
            db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_action_list_id()),commit=True)
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ID = ? ;"
            db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
            db.commit()

    def decrease_order(self):
        """
        Decreases the order number of this action and
        increases the order number of the higher-order action
        """
        db = self._core.get_db()
        stmnt = "SELECT MAX(ACT_ORDER) AS NEWORDER FROM ACTIONS WHERE ACT_ATL_ID = ? AND ACT_ORDER < ? ;"
        cur = db.query(self._core,stmnt, (self.get_action_list_id(), self.get_order()))
        row = cur.fetchonemap()
        if row is not None:
            if row["NEWORDER"] is None:
                return
            temp_order = self.get_order()
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ORDER = ? AND ACT_ATL_ID = ? ;"
            db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_action_list_id()),commit=True)
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ID = ? ;"
            db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
            db.commit()

    def move_to_top_order(self):
        """
        moves this action to the top order in its actionlist
        """
        db = self._core.get_db()
        stmnt = "SELECT MAX(ACT_ORDER) AS NEWORDER FROM ACTIONS WHERE ACT_ATL_ID = ? ;"
        cur = db.query(self._core,stmnt, (self.get_action_list_id(),))
        row = cur.fetchonemap()
        if row is not None:
            if row["NEWORDER"] is None:
                return
            temp_order = self.get_order()
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ORDER = ? AND ACT_ATL_ID = ? ;"
            db.query(self._core, stmnt, (temp_order, row["NEWORDER"], self.get_action_list_id()),commit=True)
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ID = ? ;"
            db.query(self._core, stmnt, (row["NEWORDER"], self.get_id()),commit=True)
            db.commit()

    def move_to_bottom_order(self):
        """
        moves this action to the bottom order in its actionlist
        """
        db = self._core.get_db()
        stmnt = "SELECT MIN(ACT_ORDER) AS NEWORDER FROM ACTIONS WHERE ACT_ATL_ID = ? ;"
        cur = db.query(self._core,stmnt, (self.get_action_list_id(),))
        row = cur.fetchonemap()
        if row is not None:
            if row["NEWORDER"] is None:
                return
            temp_order = self.get_order()
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ORDER = ? AND ACT_ATL_ID = ? ;"
            db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_action_list_id()),commit=True)
            stmnt = "UPDATE ACTIONS SET ACT_ORDER = ? WHERE ACT_ID = ? ;"
            db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
            db.commit()

    def set_action_list_id(self, action_list_id):
        """
        Assigns an ActionListId to the Action
        Only for Internal Use while loading the Action from DB
        """
        self._action_list_id = action_list_id

    def set_name(self,name,ignore_db = True):
        """
        Sets the Name of the action
        """
        self._name = str(name)
        if not ignore_db:
            db = self._core.get_db()
            stmnt = "UPDATE ACTIONS SET ACT_NAME = ? WHERE ACT_ID = ? ;"
            db.query(self._core, stmnt, (self._name, self.get_id()),commit=True)

    def get_name(self):
        """
        returns the name of this action
        """
        return self._name

    def get_action_list(self):
        """
        returns the ActionList this Action is currently assigned to
        """
        action_manager = self._core.get_action_manager()
        action_list = action_manager.get_action_list_by_id(self.get_action_list_id())
        return action_list

    def get_action_list_id(self):
        """
        Returns the ID of the ActionList this Action is currently assigned To
        """
        return self._action_list_id

    def set_id(self,nr):
        """
        Sets the ID of this Action
        Dedicated for Internal Use (ID gets set via DB-Sequence)
        """
        self._id = int(nr)

    def get_id(self):
        """
        Returns the ID of this Action
        """
        return self._id

    def set_url(self, url, ignore_db=False):
        """
        Make this Action an URL-Operation
        Resets Widget/Space or Site-attributes of this Action
        """
        self._url = url
        self._widget_id = None
        self._space_id = None
        self._page_id = None

        if not ignore_db:
            db = self._core.get_db()
            stmnt = "UPDATE ACTIONS SET ACT_URL = ?, ACT_SIT_ID = NULL, \
                     ACT_WGT_ID = NULL, ACT_SPACE = NULL WHERE ACT_ID = ?;"
            db.query(self._core, stmnt, (self.get_url(),self.get_id()),commit=True)

    def delete(self):
        """
        Deletes this Action from the database
        """
        db = self._core.get_db()
        stmnt = "DELETE FROM ACTIONS WHERE ACT_ID = ? ;"
        db.query(self._core,stmnt, (self.get_id(),),commit=True)

    def set_widget_space_constellation(self, widget_id, space_id, ignore_db=False):
        """
        Make this Action a Widget/Space Action
        The Action will load the targetted widget into the given Space when
        executed.
        Resets Site- and URL-Link-attributes of this Action
        """
        if widget_id is not None and space_id is not None:
            #TODO : Check if space exists in the menu's site and widget exists
            self._widget_id = int(widget_id)
            self._space_id = int(space_id)
            self._url = None
            self._page_id = None

        if not ignore_db:
            db = self._core.get_db()
            stmnt = "UPDATE ACTIONS SET ACT_URL = NULL, ACT_SIT_ID = NULL, \
                     ACT_WGT_ID = ?, ACT_SPACE = ? WHERE ACT_ID = ? ;"
            db.query(self._core,stmnt, (self.get_widget_id(), self.get_space(), self.get_id()),commit=True)

    def set_page_id(self, page_id, ignore_db = False):
        """
        Make This action a Page-Link that links
        to another Scoville-Page.
        Resets Widget/Page- and URL-Linkattributes
        """
        if self._core.get_composite_manager().get_page(page_id) is not None:
            self._page_id = int(page_id)
            self._widget_id = None
            self._space_id = None
            self._url = None
        else:
            return

        if not ignore_db:
            db = self._core.get_db()
            stmnt = "UPDATE ACTIONS SET ACT_URL = NULL, ACT_SIT_ID = ?, \
                     ACT_WGT_ID = NULL, ACT_SPACE = NULL WHERE ACT_ID = ? ;"
            db.query(self._core,stmnt,(self.get_page_id(),self.get_id()),commit=True)

    def unset_links(self):
        """
        Resets all links that are represented by this Action
        """
        self._page_id = None
        self._widget_id = None
        self._space_id = None
        self._url = None

    def get_widget_id(self):
        """
        Returns The widgetId assigned to This Action (only set when in Widget/Space-Mode)
        otherwise null
        """
        return self._widget_id

    def get_space(self):
        """
        Returns The Space assigned to this Action (only set when in Widget/Space-Mode)
        otherwise null
        """
        return self._space_id

    def get_page_id(self):
        """
        Returns the Page-ID of the site assigned to this Action (only in Page-Mode)
        otherwise null
        """
        return self._page_id

    def get_url(self):
        """
        Returns the URL assigned to this action (only in URL-Mode)
        otherwise nul
        """
        return self._url

    def get_type(self):
        """
        Returns the type of this action wich may be
        'url', 'site' (for Page) or 'widgetSpaceConstellation'
        if incostistent, returns None
        """
        if self._url is not None:
            return 'url'
        elif self._widget_id is not None and self._space_id is not None:
            return 'widgetSpaceConstellation'
        elif self._page_id is not None:
            return 'site'
        else:
            return None

class ActionList(object):
    """
    An ActionList Represents a bunch of actions That
    will be executed when the ActionList is invoked
    ActionLists can be assigned to MenuItems.
    If an ActionList is executed, the Actions are
    executed by a priority-order that can be set via
    functions in the Action-Objects
    """

    @classmethod
    def set_core(cls,core):
        """
        trivial
        """
        cls._core = core

    @classmethod
    def create_action_list(cls, action_list_name = "new actionlist"):
        """
        This function creates a new ActionList
        """
        action_list = ActionList()
        action_list.set_name(action_list_name)
        db = cls._core.get_db()
        action_list.set_id(db.get_seq_next('ATL_GEN'))
        stmnt = "INSERT INTO ACTIONLISTS VALUES (?,?);"
        db.query(cls._core, smtnt, (action_list.get_id(), action_list.get_name()),commit=True)
        return action_list

    @classmethod 
    def get_action_list_by_id(cls, action_list_id):
        """
        This function looks for an ActionList with the given ID in the database
        and returns it
        If the action does not exist this returns null 
        """
        db = cls._core.get_db()
        stmnt = "SELECT ATL_NAME FROM ACTIONLISTS WHERE ATL_ID = ? ;"
        cur = db.query(cls._core,stmnt,(action_list_id,))
        row = cur.fetchonemap()
        if row is not None:
            action_list = ActionList()
            action_list.set_id(action_list_id)
            action_list.set_name(row["ATL_NAME"],True)
            return action_list

        return None

    def __init__(self,core):
        self._core = core

        self._children = []
        self._id = None
        self._name = None

    def delete(self):
        """
        Deletes the ActionList from the DB
        """
        db = self._core.get_db()
        stmnt = "DELETE FROM ACTIONLISTS WHERE ATL_ID = ? ;"
        db.query(self._core,stmnt, (self.get_id(),),commit=True)

    def set_name(self, name, ignore_db=False):
        """
        Sets the Name of the actionList
        """
        self._name = str(name)
        if self._id is not None and not ignore_db:
            db= self._core.get_db()
            stmnt= "UPDATE ACTIONLISTS SET ATL_NAME = ? WHERE ATL_ID = ? ;"
            db.query(self._core,stmnt, (self._name, self.get_id()),commit=True)

    def get_name(self):
        """
        Returns the current Name of the ActionList
        """
        return self._name

    def set_id(self, nr):
        """
        Sets the ID of the ActionList
        Internal use Only (ID gets set with DB-generator while creation)
        """
        self._id = int(nr)

    def get_id(self):
        """
        Returns the ID of the ActionList
        """
        return self._id

    def add_action(self,action):
        """
        This function adds an Action to this ActionList
        if $action is an integer, it will be handled as actionId
        the action will only be added if it is not already a part
        of this ActionList
        """
        if type(action) == int:
            action = self._core.get_action_manager().get_action_by_id(action)

        if action is not None and action not in self._children:
            self._children.append(action)
            db = self._core.get_db()
            stmnt = "UPDATE ACTIONS SET ACT_ATL_ID = ? WHERE ACT_ID = ? ;"
            db.query(self._core,stmnt, (self.get_id(),action.get_id()),commit=True)

    def has_action(self,action):
        """
        Tests whether this ActionList has the given action by 
        comparing Action-IDs. Returns true if Action is present
        """
        for child in self._children:
            if child.get_id() == action.get_id():
                return True
        return False

    def remove_action(self,action):
        """
        Removes the given action from the ActionList
        Only does something if the given action is present in 
        this ActionList
        """
        for child in self._children:
            if child.get_id() == action.get_id():
                self._children.remove(child)
                break
        db = self._core.get_db()
        stmnt = "UPDATE ACTIONS SET ACT_ATL_ID = NULL WHERE ACT_ID = ? ;"
        db.query(self._core,stmnt, (action.get_id(),),commit=True)

    def load_actions(self):
        """
        Loads all Actions assigned to this ActionList into the Action
        """
        db = self._core.get_db()
        stmnt = "SELECT ACT_ID FROM ACTIONS WHERE ACT_ATL_ID = ? ;"
        cur = db.query(self._core,stmnt, (self.get_id(),))
        self._children= []
        rows = cur.fetchallmap()
        action_manager = self._core.get_action_manager()
        for row in rows:
            self._children.append(action_manager.get_action_by_id(row["ACT_ID"]))

    def get_actions(self):
        """
        Returns all Actions assigned to this ActionList
        """
        self.load_actions()
        return self._children

    def get_action_by_id(self, action_id):
        """
        Get a specific action of this ActionList by it's ID
        Return null if action is not found
        """
        for child in self._children:
            if child.get_id() == action_id :
                return child
        return None

class MenuItem(object):
    """
    A Menu Item is an item graphically displayed in a Menu
    A MenuItem may contain other MenuItems as children
    The order-number determines in which order the menuitems are
    displayed in their parent element which may be a Menu or another
    MenuItem order goes from low to higher numbers
    """

    @classmethod
    def set_core(cls,core):
        """
        trivial
        """
        cls._core = core

    @classmethod 
    def create_menu_item(cls, menu=None, menu_item_parent=None, name="new item"):
        """
        This function creates a new MenuItem based on either:
        1. A parent Menu or
        2. A parent MenuItem
        If none of those is set, the function will abort and return null
        The MenuItem will be spawned with the lowest display order
        """
        if menu is None and menu_item_parent is None:
            return None
        db = cls._core.get_db()
        menu_item = MenuItem()
        menu_item.set_name(name)
        if menu is not None:
            menu_item.set_menu_id(menu.get_id())
            stmnt = "SELECT MAX(MNI_ORDER) AS MAXORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? ;"
            cur = db.query(cls._core, stmnt, (menu.get_id(),))
        if menu_item_parent is not None:
            menu_item.set_parent_menu_item_id(menu_item_parent.get_id())
            stmnt = "SELECT MAX(MNI_ORDER) AS MAXORDER FROM MENUITEMS WHERE MNI_MNI_ID = ? ;"
            cur = db.query(cls._core, stmnt, (menu_item_parent.get_id(),))
        menu_item.set_id(db.get_seq_next('MNI_GEN'))
        row = cur.fetchonemap()
        if row is not None:
            new_order = row["MAXORDER"]+1
        else:
            new_order = 0
        menu_item.set_order(new_order)
        stmnt = "INSERT INTO MENUITEMS VALUES (?,?,?,?,?,?) ;"
        db.query(cls._core,stmnt,(menu_item.get_id(), menu_item.get_name(),
                                  menu_item.get_menu_id(), menu_item.get_parent_menu_item_id(),
                                  None, menu_item.get_order()),commit=True)
        db.commit()
        actionlist = cls.create_action_list()
        menu_item.assign_action_list(action_list)
        return menu_item

    @classmethod
    def get_menu_item_by_id(cls, menu_item_id):
        """
        This function looks for a MenuItem with the given ID in the database
        and returns it
        If the MenuItem does not exist this returns null
        """
        db = cls._core.get_db()
        stmnt = "SELECT MNI_NAME, MNI_MNU_ID, MNI_MNI_ID, MNI_ATL_ID, MNI_ORDER \
                 FROM MENUITEMS WHERE MNI_ID = ? ;"
        cur = db.query(cls._core,stmnt,(menu_item_id,))
        row = cur.fetchonemap()
        if row is not None:
            menu_item = MenuItem()
            menu_item.set_id(menu_item_id)
            menu_item.set_name(row["MNI_NAME"],True)
            menu_item.set_order(row["MNI_ORDER"])
            if row.has_key("MNI_MNU_ID"):
                menu_item.set_menu_id(row["MNI_MNU_ID"],True)
            if row.has_key("MNI_MNI_ID"):
                menu_item.set_parent_menu_item_id(row["MNI_MNI_ID"],True)
            if row.has_key("MNI_ATL_ID"):
                menu_item.set_action_list_id(row["MNI_ATL_ID"])

            return menu_item
        return None

    def __init__(self, core):
        self._core = core

        self._id = None
        self._name = None
        self._action_list_id = None
        self._action_list = None
        self._menu_id = None
        self._manu = None
        self._parent_menu_item_id = None
        self._parent_menu_item = None
        self._order = None

    def delete(self):
        """
        Deletes this MenuItem from DB
        """        
        db = self._core.get_db()
        stmnt = "DELETE FROM MENUITEMS WHERE MNI_ID = ? ;"
        db.query(self._core,stmnt, (self.get_id(),),commit=True)

    def set_order(self, order):
        """
        Sets the display-ordernumber of this MenuItem
        Internal use only. 
        
        Use increaseOrder() decreaseOrder(),
        moveToTopOrder() or moveToBottomOrder()
        to modify Order.
        """
        self._order = int(order)

    def get_order(self):
        """
        Returns the current Order number of this MenuItem
        """
        return self._order

    def increase_order(self):
        """
        Increases the order of this MenuItem
        """
        db = self._core.get_db()
        if self.get_menu_id() is not None:
            stmnt = "SELECT MIN(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? AND MNI_ORDER > ? ;"
            cur = db.query(self._core,stmnt, (self.get_menu_id(), self.get_order()))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ? ;"
                db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_menu_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()
        elif self.get_parent_menu_item_id() is not None:
            stmnt = "SELECT MIN(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNI_ID = ? AND MNI_ORDER > ? ;"
            cur = db.query(self._core,stmnt, (self.get_parent_menu_item_id(), self.get_order()))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ? ;"
                db.query(self._core, stmnt, (temp_order, row["NEWORDER"], self.get_parent_menu_item_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core, stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()

    def decrease_order(self):
        """
        Decreases the order of this MenuItem
        """
        db = self._core.get_db()
        if self.get_menu_id() is not None:
            stmnt = "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? AND MNI_ORDER < ? ;"
            cur = db.query(self._core,stmnt, (self.get_menu_id(), self.get_order()))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ? ;"
                db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_menu_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()
        elif self.get_parent_menu_item_id() is not None:
            stmnt = "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNI_ID = ? AND MNI_ORDER < ? ;"
            cur = db.query(self._core,stmnt, (self.get_parent_menu_item_id(), self.get_order()))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ? ;"
                db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_parent_menu_item_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()
    
    def move_to_top_order(self):
        """
        Moves this menuitem to the top-order
        """
        db = self._core.get_db()
        if self.get_menu_id() is not None:
            stmnt = "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? ;"
            cur = db.query(self._core,stmnt, (self.get_menu_id(),))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ? ;"
                db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_menu_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()
        elif self.get_parent_menu_item_id() is not None:
            stmnt = "SELECT MAX(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNI_ID = ? ;"
            cur = db.query(self._core,stmnt, (self.get_parent_menu_item_id(),))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ? ;"
                db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_parent_menu_item_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()

    def move_to_bottom_order(self):
        """
        Moves this menuitem to the bottom-order
        """
        db = self._core.get_db()
        if self.get_menu_id() is not None:
            stmnt = "SELECT MIN(MNI_ORDER) AS NEWORDER FROM MENUITEMS WHERE MNI_MNU_ID = ? ;"
            cur = db.query(self._core,stmnt, (self.get_menu_id(),))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNU_ID = ? ;"
                db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_menu_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()
        elif self.get_parent_menu_item_id() is not None:
            stmnt = "SELECT MIN(MNI_ORDER) AS NEWORDER, MNI_ID FROM MENUITEMS WHERE MNI_MNI_ID = ? ;"
            cur = db.query(self._core,stmnt, (self.get_parent_menu_item_id(),))
            row = cur.fetchonemap()
            if row is not None:
                if row["NEWORDER"] is None:
                    return
                temp_order = self.get_order()
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ORDER = ? AND MNI_MNI_ID = ? ;"
                db.query(self._core,stmnt, (temp_order, row["NEWORDER"], self.get_parent_menu_item_id()),commit=True)
                stmnt = "UPDATE MENUITEMS SET MNI_ORDER = ? WHERE MNI_ID = ? ;"
                db.query(self._core,stmnt, (row["NEWORDER"], self.get_id()),commit=True)
                db.commit()

    def set_action_list_id(self,action_list_id):
        """
        Set the ActionList assigned to this MenuItem directly
        Internal Use only
        
        Use assignActionList() to modify this MenuItem's actionlist
        """
        self._action_list_id = int(action_list_id)

    def get_action_list(self):
        """
        Returns the ActionList that is currently assigned to this MenuItem
        if there is no Action list return null
        """
        if self._action_list is None or self._action_list.get_id() != self._action_list_id:
            action_manager = self._core.get_action_manager()
            self._action_list = action_manager.get_action_list_by_id(self.get_action_list_id())
        return self._action_list

    def get_action_list_id(self):
        """
        Return the id of the ActionList that is currently assigned to this MenuItem
        If there is no ActionList assigned, returns null
        """
        return self._action_list_id

    def get_menu(self):
        """
        Returns the Menu this MenuItem is assigned To
        Returns null if not assigned to a Menu but to a submenu
        """
        if self._menu is None or self._menu.get_id() != self._menu_id:
            action_manager = self._core.get_action_manager()
            self._menu = action_manager.get_menu_by_id(self.get_menu_id())
        return self._menu

    def get_menu_id(self):
        """
        Returns the ID of the Menu this MenuItem is assigned To
        Returns null if not assigned to a Menu but to another MenuItem
        """
        return self._menu_id

    def set_parent_menu_item_id(self, parent_menu_item_id, ignore_db=False):
        """
        Assigns this MenuItem to a parent MenuItem
        Resets any relations this MenuItem has to a Menu
        """
        self._parent_menu_item_id = parent_menu_item_id
        self._menu = None
        self._menu_id = None
        if self._get_id() is not None and not ignore_db:
            db = self._core.get_db()
            stmnt = "UPDATE MENUITEMS SET MNI_MNI_ID = ?, MNI_MNU_ID = NULL WHERE MNI_ID = ? ;"
            db.query(self._core,stmnt, (self._parent_menu_item_id, self.get_id()),commit=True)

    def get_parent_menu_item(self):
        """
        Returns the MenuItem this MenuItem is assigned to or null if not assigned
        """
        if self._parent_menu_item is None or self._parent_menu_item.get_id() != self._parent_menu_item_id:
            action_manager = self._core.get_action_manager()
            self._parent_menu_item = action_manager.get_menu_item_by_id(self.get_parent_menu_item_id())
        return self._parent_menu_item

    def get_parent_menu_item_id(self):
        """
        Returns the MenuItemID of the MenuItem this MenuItem is assigned to or null if not assigned
        """

        return self._parent_menu_item_id

    def set_name(self,name, ignore_db=False):
        """
        Sets the name of this MenuItem
        """
        self._name = str(name)
        if self.get_id() is None and not ignore_db:
            db = self._core.get_db()
            stmnt = "UPDATE MENUITEMS SET MNI_NAME = ? WHERE MNI_ID = ? ;"
            db.query(self._core,stmnt, (self._name, self.get_id()),commit=True)

    def get_name(self):
        """
        Gets the name of this MenuItem
        """
        return self._name

    def set_id(self, nr):
        """
        Sets The id of this MenuItem
        Internal use only (ID gets set via DB generator while creation)
        """
        self._id = int(nr)

    def get_id(self):
        """
        Returns the ID of this MenuItem
        """
        return self._id

    def assign_action_list(self, action_list):
        """
        Assigns an ActionList to this MenuItem
        """
        action_list_id = action_list.get_id()
        self.set_action_list_id(action_list_id)
        db = self._core.get_db()
        stmnt = "UPDATE MENUITEMS SET MNI_ATL_ID = ? WHERE MNI_ID = ? ;"
        db.query(self._core,stmnt, (action_list_id, self.get_id()),commit=True)

    def add_menu_item(self, menu_item):
        """
        Adds a MenuItem as SubMenu-Component to this MenuItem
        """
        menu_item_id = menu_item.get_id()
        menu_item.set_parent_menu_item_id(self.get_id())
        db = self._core.get_db()
        stmnt = "UPDATE MENUITEMS SET MNI_MNI_ID = ? WHERE MNI_ID = ? ;"
        db.query(self._core,stmnt, (self.get_id(), menu_item_id),commit=True)

    def remove_menu_item(self, menu_item):
        """
        Removes a MenuItem (SubmenuItem) assigned to this MenuItem
        """
        menu_item_id = menu_item.get_id()
        menu_item.set_parent_menu_item_id(None)
        db = self._core.get_db()
        stmnt = "UPDATE MENUITEMS SET MNI_MNI_ID = NULL WHERE MNI_ID = ? ;"
        db.query(self._core,stmnt, (self.get_id(), menu_item_id),commit=True)

    def get_menu_items(self):
        """
        Returns all (Sub-)MenuItems that are assigned to this MenuItem
        """
        action_manager = self._core.get_action_manager()
        db = self._core.get_db()
        stmnt = "SELECT MNI_ID FROM MENUITEMS WHERE MNI_MNI_ID = ? ;"
        cur = db.query(self._core,stmnt, (self.get_id()))
        ret = []
        rows = cur.fetchallmap()
        for row in rows:
            ret.append(action_manager.get_menu_item_by_id(row["MNI_ID"]))
        return ret

class Menu(object):
    """
    A Menu represents a structure that contains MenuItems
    It is the root-element of any navigation-structure
    """

    @classmethod
    def set_core(cls,core):
        """
        trivial
        """
        cls._core = core

    @classmethod 
    def create_menu(cls, page, name="new menu"):
        """
        This function creates a menu.
        """
        db = cls._core.get_db()
        menu = Menu()
        menu.set_id(db.get_seq_next('MNU_GEN'))
        menu.set_name(name)
        stmnt = "INSERT INTO MENUS (MNU_ID,MNU_NAME, MNU_SIT_ID) VALUES (?,?, ?) ;"
        db.query(cls._core,stmnt, (menu.get_id(), menu.get_name(), page.get_id()),commit=True)
        return menu 

    @classmethod
    def get_menu_by_id(cls, menu_id):
        """
        This function looks for a Menu with the given ID in the database
        and returns it
        If the Menu does not exist this returns null 
        """
        db = cls._core.get_db()
        stmnt = "SELECT MNU_NAME FROM MENUS WHERE MNU_ID = ? ;"
        cur = db.query(cls._core,stmnt, (menu_id,))
        row = cur.fetchonemap()
        if row is not None:
            menu = Menu()
            menu.set_id(menu_id)
            menu.set_name(row["MNU_NAME"],True)
            return menu
        return None

    def __init__(self, core):
        self._core = core

        self._children = []
        self._id = None
        self._name = None
        self._page_id = None
        self._page = None

    def set_page_id(self, page_id):
        """
        Set the Id of the Page this menu belongs to
        """
        self._page_id = int(page_id)

    def get_page(self):
        """
        Returns the page this Menu belongs To
        """
        if self._page is None or self._page.get_id() != self._page_id:
            composite_manager = self._core.get_composite_manager()
            self._page = composite_manager.get_page(self._page_id)
        return self._page

    def get_page_id(self):
        """
        Returns The page ID of the page this menu belongs to
        """
        return self._page_id

    def set_name(self,name, ignore_db = False):
        """
        Sets the name of this menu
        """
        self._name = str(name)
        if self.get_id() is None and not ignore_db:
            db = self._core.get_db()
            stmnt = "UPDATE MENUS SET MNU_NAME = ? WHERE MNU_ID = ? ;"
            db.query(self._core,stmnt, (self._name, self.get_id()),commit=True)

    def get_name(self):
        """
        Returns the name of this Menu
        """
        return self._name

    def set_id(self, nr):
        """
        Sets the id of this Menu
        Internal use only (Id gets set via DB-Generator while creation)
        """
        self._id = int(nr)

    def get_id(self):
        """
        Returns the id of this Menu
        """
        return self._id

    def add_menu_item(self, menu_item):
        """
        Adds a MenuItem to this Menu
        MenuItem only gets added if its not already assigned here
        """
        if menu_item not in self._children:
            self._chilren.append(menu_item)
            db = self._core.get_db()
            stmnt = "UPDATE MENUITEMS SET MNI_MNU_ID = ? WHERE MNI_ID = ? ;"
            db.query(self._core,stmnt, (self.get_id(),menu_item.get_id()),commit=True)

    def load_menu_items(self):
        """
        Loads the menuItems from Database
        """
        self._children = []
        db = self._core.get_db()
        stmnt = "SELECT MNI_ID FROM MENUITEMS WHERE MNI_MNU_ID = ? ;"
        cur = db.query(self._core, stmnt, (self.get_id(),))
        action_manager = self._core.get_action_manager()
        rows = cur.fetchallmap()
        for row in rows:
            self._children.append(action_manager.get_menu_item_by_id(row["MNI_ID"]))
        self._menu_items_initialized = True

    def get_menu_item_by_id(self, menu_item_id):
        """
        Returns a MenuItem assigned to this menu by a given ID
        If this MenuItem does not exist, returns null
        """
        if not self._menu_items_initialized:
            self.load_menu_items()
        for child in self._children:
            if child.get_id() == menu_item_id:
                return child
        return None

    def get_menu_items(self):
        """
        Returns all MenuItems assigned to this Menu
        """
        if not self._menu_items_initialized:
            self.load_menu_items()
        return self._children

    def remove_menu_item(self, menu_item):
        """
        Removes a MenuItem from this Menu
        """
        menu_item_id = menu_item.get_id()
        menu_item.set_parent_menu_item_id(None)

        db = self._core.get_db()
        stmnt = "UPDATE MENUITEMS SET MNI_MNU_ID = NULL WHERE MNI_ID = ? ;"
        db.query(self._core,stmnt, (self.get_id(), menu_item_id),commit=True)

    def delete(self):
        """
        Deletes this menu from the database
        """
        db = self._core.get_db()
        stmnt = "DELETE FROM MENUS WHERE MNU_ID = ? ;"
        db.query(self._core,stmnt, (self.get_id(),),commit=True)
        db.commit()






