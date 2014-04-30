#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

from json import JSONDecoder, JSONEncoder
from traceback import print_exc
from StringIO import StringIO
from operation import OperationDaemon
import base64
import os
import subprocess

from skarphedcore.configuration import Configuration
from skarphedcore.core import Core
from skarphedcore.operation import Operation
from skarphedcore.permission import Permission, Role
from skarphedcore.user import User
from skarphedcore.module import ModuleManager
from skarphedcore.session import Session
from skarphedcore.binary import Binary
from skarphedcore.template import Template
from skarphedcore.action import Action, ActionList, Menu, MenuItem
from skarphedcore.view import Page, View
from skarphedcore.css import CSSManager
from skarphedcore.pki import Pki
from skarphedcore.poke import PokeManager

class Rpc(object):
    def __call__(self, instructions):
        jd = JSONDecoder()
        je = JSONEncoder()
        answer = {}
        try:
            instructions = jd.decode(instructions)
        except ValueError, e:
            answer['error'] = "could not decode instructions"
            Core().response_body.append(je.encode(answer))
            return

        method = instructions['method']
        params = instructions['params']

        if not hasattr(self,method):
            answer['error'] = {}
            answer['error']['message'] = "The Rpc-backed does not support this method %s"%method
            answer['error']['class'] = "RpcException"
            Core().response_body.append(je.encode(answer))
            return
        try:
            exec "res = self.%s(params)"%method
        except Exception, e:
            error = StringIO()
            print_exc(None,error)
            answer['error'] = {}
            answer['error']['traceback'] = error.getvalue()
            answer['error']['class'] = e.__class__.__name__
            answer['error']['message'] = str(e)
            Core().response_body.append(je.encode(answer))
            return
        else:
            answer['result'] = res
            Core().response_body.append(je.encode(answer))
    
    # RPC - Method-Implementations____________________________

    def executeModuleMethod(self, params):
        module_id = params[0]
        method_name = params[1]
        parameter = params[2]

        module = ModuleManager.get_module(module_id)
        exec "res = module.%s(*parameter)"%method_name
        return res

    def getServerInfo(self,params):
        return Configuration().get_entry("core.name")

    def getInstanceId(self, params):
        session_user = Session.get_current_session_user()

        if session_user.check_permission('skarphed.manageserverdata'):
            config = Configuration()
            return config.get_entry('core.instance_id')
        else:
            return None

    def authenticateUser(self,params):
        username = unicode(params[0])
        password = unicode(params[1])
        
        try:
            user = User.get_user_by_name(username)
        except UserException , e:
            session = Session.get_current_session()
            if session is not None:
                session.delete()
            return False


        if user.authenticate(password):
            session = Session.create_session(user)
            return user.get_permissions()
        else:
            session = Session.get_current_session()
            if session is not None:
                session.delete()
            return False

    def alterPassword(self, params):
        user_id = int(params[0])
        new_password = unicode(params[1])
        old_password = unicode(params[2])

        session_user = Session.get_current_session_user()

        if user_id == session_user.get_id():
            session_user.alter_password(new_password,old_password)
        else:
            if session_user.check_permission("skarphed.users.alter_password"):
                user = User.get_user_by_id(user_id)
                user.alter_password(new_password,"",True)
        return True

    def getPublicKey(self, params):
        return Pki.get_public_key(as_string=True)


    def getUsers(self,params):
        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.users.view'):
            users = User.get_users_for_admin_interface()
            return users
        return False

    def getRoles(self,params):
        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.roles.view'):
            ret = []
            for role in Permission.get_roles():
                ret.append({"id":role.get_id(), "name": role.get_name()})
            return ret
        return False

    def createUser(self,params):
        username = unicode(params[0])
        password = unicode(params[1])

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.users.create'):
            User.create_user(username,password)
        return True

    def grantRightToUser(self,params):
        user_id = int(params[0])
        permission_name  = str(params[1])

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.users.grant_revoke'):
            user = User.get_user_by_id(user_id)
            user.grant_permission(permission_name)
            return True

    def revokeRightFromUser(self,params):
        user_id = int(params[0])
        permission_name = str(params[1])

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.users.grant_revoke'):
            user = User.get_user_by_id(user_id)
            user.revoke_permission(permission_name)
            return True

    def getRightsForUserPage(self,params):
        user_id = int(params[0])
        user = User.get_user_by_id(user_id)
        return user.get_grantable_permissions()

    def grantRightToRole(self,params):
        role_id = int(params[0])
        permission_name = str(params[1])

        role = Role.get_role(role_id)
        role.add_permission(permission_name)
        role.store()

    def revokeRightFromRole(self,params):
        role_id = int(params[0])
        permission_name = str(params[1])

        role = Role.get_role(role_id)
        role.remove_permission(permission_name)
        role.store()

    def getRightsForRolePage(self,params):
        role_id = int(params[0])

        role = Role.get_role(role_id)
        return role.get_grantable_permissions()

    def createRole(self,params):
        data = params[0]

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.roles.create'):
            role = Role.create_role(data)
        return role.get_id()

    def deleteRole(self, params):
        role_id = int(params[0])

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.roles.delete'):
            role = Role.get_role(role_id)
            role.delete()

    def getRolesForUserPage(self, params):
        user_name = params[0] # TODO get user by id instead of name
        user = User.get_user_by_name(user_name)
        return user.get_grantable_roles()

    def assignRoleToUser(self, params):
        user_name = params[0] # TODO get user by id instead of name
        role_id = params[1]

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.users.grant_revoke'):
            role = Role.get_role(role_id)
            User.get_user_by_name(user_name).assign_role(role)

    def revokeRoleFromUser(self, params):
        user_name = params[0] # TODO get user by id instead of name
        role_id = params[1]

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.users.grant_revoke'):
            role = Role.get_role(role_id)
            User.get_user_by_name(user_name).revoke_role(role)

    def getCssPropertySet(self,params):
        try:
            module_id = int(params[0])
        except TypeError:
            module_id = None

        try:
            widget_id = int(params[1])
        except TypeError:
            widget_id = None

        if params[2] is not None:
            session = str(params[2])
        else:
            session = None

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.css.edit'):
            css_manager = CSSManager()
            if module_id == None and widget_id == None and session == None:
                css_propertyset = css_manager.get_csspropertyset()
            else:
                css_propertyset = css_manager.get_csspropertyset(module_id,widget_id,session)
            data = css_propertyset.serialize_set()
            return data

    def setCssPropertySet(self, params):
        data = params[0]

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.css.edit'):
            css_propertyset = CSSManager().create_csspropertyset_from_serial(data)
            css_propertyset.store()

    def getModules(self,params):
        get_installed_only = bool(params[0])

        repo_state = True
        repo_state = module_manager.get_repository().ping()
        
        modules = ModuleManager.get_module_info(get_installed_only or not repo_state)
        return {'modules':modules,'repostate':repo_state}

    def getGuiForModule(self, params):
        module_id = int(params[0])

        module = ModuleManager.get_module(module_id)
        moduleguidata = base64.b64encode(module.get_guidata())
        signature = Pki.sign(moduleguidata)

        return {'data':moduleguidata,
                'signature':base64.b64encode(signature),
                'libstring':Configuration.get_entry('global.modpath')}

    def changeRepository(self, params):
        ip = str(params[0])
        port = int(params[1])

        ModuleManager.set_repository(ip, port, '(default)')

    def retrieveRepository(self, params):
        repo = ModuleManager.get_repository()
        return {"id":repo.get_id(), "ip":repo.get_ip(), 
                "port":repo.get_port(), "name": repo.get_name()}

    def updateModule(self, params):
        nr = str(params[0])

        module = ModuleManager.get_module(nr)
        module_meta = ModuleManager.get_meta_from_module(module)
        ModuleManager.invoke_update(module_meta)
        return True

    def invokeUpdateModules(self, params):
        ModuleManager.updateModules()
        return 0

    def uninstallModule(self, params):
        module_meta = params[0]

        ModuleManager.invoke_uninstall(module_meta)
        return 0

    def installModule(self, params):
        module_meta = params[0]

        ModuleManager.invoke_install(module_meta)
        return 0        

    def dropOperation(self, params):
        operation_id = int(params[0])

        Operation.drop_operation(operation_id)

    def retryOperation(self, params):
        operation_id = int(params[0])

        Operation.retry_operation(operation_id)

    def cancelOperation(self, params):
        operation_id = int(params[0])

        Operation.cancel_operation(operation_id)

    def deleteUser(self, params):
        user_id = int(params[0])

        session_user = Session.get_current_session_user()
        if session_user.check_permission('skarphed.users.delete'):
            user = User.get_user_by_id(user_id)
            user.delete()

    def getOperations(self, params):
        operationtypes = None
        if len(params) == 1:
            operationtypes = params[0]

        operations = Operation.get_current_operations_for_gui(operationtypes)

        return operations

    def retrieveSites(self, params):
        pages = Page.get_pages()
        ret = []
        for page in pages:
            spaces = page.get_space_names()
            boxes = page.get_box_info()
            ret.append({
                    'id':page.get_id(),
                    'name':page.get_name(),
                    'description':page.get_description(),
                    'spaces':spaces,
                    'boxes':boxes
                })
        return ret

    def getSite(self, params):
        page_id = int(params[0])
        
        page = Page.get_page(page_id)
        spaces = page.get_space_names()
        boxes = page.get_box_info()
        ret = {
            'id':page.get_id(),
            'name':page.get_name(),
            'description':page.get_description(),
            'spaces':spaces,
            'boxes':boxes
        }
        return ret

    def assignWidgetToSpace(self,params):
        view_id = int(params[0])
        space_id = int(params[1])
        widget_id = int(params[2])

        view = View.get_from_id(view_id)
        view.place_widget_in_space(space_id, widget_id)
        view.store()

    def removeWidgetFromSpace(self, params):
        view_id = int(params[0])
        space_id = int(params[1])

        view = View.get_from_id(view_id)
        view.remove_widget_from_space(space_id)
        view.store()

    def getCurrentTemplate(self, params):
        if Template.is_template_installed():
            current_template = Template.get_current_template()
            return {'name': current_template.get_name(),
                    'description': current_template.get_description(),
                    'author': current_template.get_author()}
        else:
            return {'name': '(No Template)',
                    'description': '(Currently no Template Installed)',
                    'author': '(No Author)',}

    def installTemplate(self, params):
        templatedata = base64.b64decode(params[0])

        #TODO check for permission

        errorlog = Template.install_from_data(templatedata)
        return errorlog

    def installTemplateFromRepo(self, params):
        repo_template_id = int(params[0])
        errorlog = Template.install_from_repo(repo_template_id)
        return errorlog

    def refreshAvailableTemplates(self, params):
        templates = Template.fetch_templates_for_gui()
        ret = [{
                'id':t['id'],
                'name':t['name'],
                'description':t['description'],
                'author':t['author']
              } for t in templates]
        return ret

    def createWidget(self,params):
        module_id = int(params[0])
        new_widget_name = unicode(params[1])

        module = ModuleManager.get_module(module_id)
        module.create_widget(new_widget_name)
        return

    def deleteWidget(self, params):
        widget_id = int(params[0])

        widget = ModuleManager.get_widget(widget_id)
        widget.delete()
        return

    def getWidgetsOfModule(self, params):
        module_id = int(params[0])

        module = ModuleManager.get_module(module_id)
        widgets = module.get_widgets()

        return [{'id':widget.get_id(), 'name':widget.get_name(), 'gviews':widget.is_generating_views(), 'baseview':widget.get_baseview_id(), 'basespace':widget.get_baseview_space_id()} for widget in widgets]

    def getMenusOfSite(self,params):
        page_id = int(params[0])

        page = Page.get_page(page_id)
        menus = page.get_menus()
        ret = []
        for menu in menus:
            ret.append({
                    'id':menu.get_id(),
                    'name':menu.get_name()
                })
        return ret

    def getMenuItemsOfMenu(self, params):
        menu_id = int(params[0])

        menu_items = Menu.get_menu_by_id(menu_id).get_menu_items()

        ret = []
        for menu_item in menu_items:
            ret.append({"name":  menu_item.get_name(),
                        "id":    menu_item.get_id(),
                        "order": menu_item.get_order()})
        return ret

    def getMenuItemsOfMenuItem(self, params):
        menu_item_id = int(params[0])

        menu_items = MenuItem.get_menu_item_by_id(menu_item_id).get_menu_items()

        ret = []
        for menu_item in menu_items:
            ret.append({"name":  menu_item.get_name(),
                        "id":    menu_item.get_id(),
                        "order": menu_item.get_order()})
        return ret

    def increaseMenuItemOrder(self, params):
        menu_item_id = int(params[0])

        menu_item = MenuItem.get_menu_item_by_id(menu_item_id)
        menu_item.increase_order()
        return 0

    def decreaseMenuItemOrder(self, params):
        menu_item_id = int(params[0])

        menu_item = MenuItem.get_menu_item_by_id(menu_item_id)
        menu_item.decrease_order()
        return 0

    def moveToBottomMenuItemOrder(self, params):
        menu_item_id = int(params[0])

        menu_item = MenuItem.get_menu_item_by_id(menu_item_id)
        menu_item.move_to_bottom_order()
        return 0

    def moveToTopMenuItemOrder(self, params):
        menu_item_id = int(params[0])

        menu_item = MenuItem.get_menu_item_by_id(menu_item_id)
        menu_item.move_to_top_order()
        return 0

    def createMenuForSite(self, params):
        page_id = int(params[0])

        page = Page.get_page(page_id)

        Menu.create_menu(page)

    def deleteMenu(self, params):
        menu_id = int(params[0])

        menu = Menu.get_menu_by_id(menu_id)
        menu.delete()

    def createMenuItem(self, params):
        parent_id = int(params[0])
        parent_type = unicode(params[1])

        if parent_type == "menu":
            menu = Menu.get_menu_by_id(parent_id)
            Menu.create_menu_item(menu)
            return 0
        elif parent_type == "menuItem":
            menu_item = MenuItem.get_menu_item_by_id(parent_id)
            MenuItem.create_menu_item(None,menu_item)
            return 0
        else:
            return 1

    def deleteMenuItem(self, params):
        menu_item_id = int(params[0])

        menu_item = MenuItem.get_menu_item_by_id(menu_item_id)
        menu_item.delete()
        return 0

    def renameMenuItem(self, params):
        menu_item_id = int(params[0])
        new_name = unicode(params[1])

        menu_item = MenuItem.get_menu_item_by_id(menu_item_id)
        menu_item.set_name(new_name)
        return 0

    def getActionsOfActionList(self, params):
        action_list_id = int(params[0])

        action_list = ActionList.get_action_list_by_id(action_list_id)
        actions = action_list.get_actions()

        ret = []
        for action in actions:
            ret.append({"id":action.get_id(),
                        "name":action.get_name(),
                        "url":action.get_url(),
                        "widgetId":action.get_widget_id(),
                        "space":action.get_space(),
                        "viewId":action.get_view_id(),
                        "order":action.get_order(),
                        "type":action.get_type()})
        return ret

    def addActionToActionList(self, params):
        action_list_id = int(params[0])

        action_list = ActionList.get_action_list_by_id(action_list_id)
        Action.create_action(action_list, None, "")
        return 0

    def deleteAction(self, params):
        action_id = int(params[0])

        action = Action.get_action_by_id(action_id)
        action.delete()
        return 0

    def increaseActionOrder(self, params):
        action_id = int(params[0])

        action = Action.get_action_by_id(action_id)
        action.increase_order()
        return 0

    def decreaseActionOrder(self, params):
        action_id = int(params[0])

        action = Action.get_action_by_id(action_id)
        action.decrease_order()
        return 0

    def moveToTopActionOrder(self, params):
        action_id = int(params[0])

        action = Action.get_action_by_id(action_id)
        action.move_to_top_order()
        return 0

    def moveToBottomActionOrder(self, params):
        action_id = int(params[0])

        action = Action.get_action_by_id(action_id)
        action.move_to_bottom_order()
        return 0

    def getActionListForMenuItem(self, params):
        menu_item_id = int(params[0])

        menu_item = MenuItem.get_menu_item_by_id(menu_item_id)
        action_list = menu_item.get_action_list()
        return {"id":action_list.get_id()}

    def setActionUrl(self, params):
        action_id = int(params[0])
        url = str(params[1])

        action = Action.get_action_by_id(action_id)
        action.set_url(url)
        return 0

    def setActionWidgetSpaceConstellation(self, params):
        action_id = int(params[0])
        widget_id = int(params[1])
        space = int(params[2])

        action = Action.get_action_by_id(action_id)
        action.set_widget_space_constellation(widget_id, space)
        return 0

    def setActionView(self, params):
        action_id = int(params[0])
        view_id = int(params[1])

        action = Action.get_action_by_id(action_id)
        action.set_view_id(view_id)
        return 0

    def renameMenu(self, params):
        menu_id = int(params[0])
        new_name = unicode(params[1])

        menu = Menu.get_menu_by_id(menu_id)
        menu.set_name(new_name)
        return 0

    def startOperationDaemon(self,params):
        session_user = Session.get_current_session_user()
        if not session_user.check_permission("skarphed.manageserverdata"):
            return False

        configuration = Configuration()
        os.system("python "+configuration.get_entry("core.webpath")+\
                  "/operation_daemon.py start "+ configuration.get_entry("core.instance_id"))

    def stopOperationDaemon(self,params):
        session_user = Session.get_current_session_user()
        if not session_user.check_permission("skarphed.manageserverdata"):
            return False

        configuration = Configuration()
        os.system("python "+configuration.get_entry("core.webpath")+\
                  "/operation_daemon.py stop "+ configuration.get_entry("core.instance_id"))

    def restartOperationDaemon(self,params):
        session_user = Session.get_current_session_user()
        if not session_user.check_permission("skarphed.manageserverdata"):
            return False

        configuration = Configuration()
        os.system("python "+configuration.get_entry("core.webpath")+\
                  "/operation_daemon.py restart "+ configuration.get_entry("core.instance_id"))

    def getOperationDaemonStatus(self,params):
        configuration = Configuration()
        res = os.system("python "+configuration.get_entry("core.webpath")+\
                  "/operation_daemon.py status "+ configuration.get_entry("core.instance_id"))

        if res == 0:
            running = True
        else:
            running = False
        return running

    def retrieveViews(self, params):
        return View.get_viewlist()
    
    def getView(self, params):
        view_id = int(params[0])

        view = View.get_from_id(view_id)
        ret = {
            'id' : view.get_id(),
            'name' : view.get_name(),
            'site' : view.get_page(),
            'default' : view.get_default(),
            'space_widget_mapping' : view.get_space_widget_mapping(),
            'box_mapping': view.get_box_mapping(),
            'widget_param_mapping' : view.get_widget_param_mapping()
        }
        return ret

    def setSpaceWidgetMapping(self, params):
        view_id = int(params[0])
        mapping = dict(params[1])

        view = View.get_from_id(view_id)
        view.set_space_widget_mapping(mapping)
        view.store(onlySpaceWidgetMapping=True)
        return True

    def setBoxMapping(self, params):
        view_id = int(params[0])
        mapping = dict(params[1])

        view = View.get_from_id(view_id)
        view.set_box_mapping(mapping)
        view.store(onlyBoxMapping=True)
        return True

    def setWidgetParamMapping(self, params):
        view_id = int(params[0])
        widget_id = int(params[1])
        mapping = int(params[2])

        view = View.get_from_id(view_id)
        view.set_params_for_widget(widget_id, mapping)
        view.store(onlyWidgetParamMapping=True)

    def storeBinary(self, params):
        data = base64.b64decode(params[0])
        filename = str(params[1])

        #TODO: Care about mimetype recognition
        binary = Binary.create(data, "benis/unknown", filename)
        binary.store()
        return binary.get_id()

    def loadMedia(self, params):
        return Binary.get_binaries_for_gui()

    def deleteBinaries(self, params):
        binary_ids = params[0]
        
        Binary.delete_binaries(binary_ids)
        return None

    def changeMaintenanceMode(self, params):
        state = bool(params[0])

        session_user = Session.get_current_session_user()
        if not session_user.check_permission('skarphed.manageserverdata'):
            return False

        if state:
            Core().activate_maintenance_mode()
        else:
            Core().deactivate_maintenance_mode()

        return True

    def retrieveMaintenanceMode(self, params):
        return Core().is_maintenance_mode()

    def changeRendermode(self,params):
        mode = str(params[0])

        session_user = Session.get_current_session_user()
        if not session_user.check_permission('skarphed.manageserverdata'):
            return False

        return Core().set_rendermode(mode)

    def retrieveRendermode(self,params):
        return Core().get_rendermode()

    def widgetActivateViewGeneration(self, params):
        widget_id = int(params[0])
        view_id = int(params[1])
        space_id = int(params[2])

        view = View.get_from_id(view_id)
        widget = ModuleManager.get_widget(widget_id)
        widget.activate_viewgeneration(view, space_id)
        return

    def widgetDeactivateViewGeneration(self, params):
        widget_id = int(params[0])

        widget = ModuleManager.get_widget(widget_id)
        widget.deactivate_viewgeneration()
        return

    def poke(self, params):
        return PokeManager.poke()
