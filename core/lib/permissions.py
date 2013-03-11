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

class PermissionException(Exception):
    """
    Exceptions for Permission-Module
    """
    ERRORS = {
        0:"""Create Role: Can't save a role without Id""",
        1:"""Create Role: Can't save a role without a Name""",
        2:"""Create Role: This user is not allowed to create Roles""",
        3:"""Add Permission: This user is not allowed to modify Roles""",
        4:"""Add Permission: User Cannot edit a permission that he does not possess himself!""",
        5:"""Delete Role : This user is not allowed to delete Roles""",
        6:"""Grant Role: This user is not allowed to grant or revoke Roles""",
        7:"""Grant Role: You can only allow Roles you possess yourself OR roles, that can be made up of the permissions you own.""",
        8:"""This role does not seem to exist (Shouldnt happen)""",
        9:"""Permissions can only be checked of users or userIds""",
        10:"""Create Role: Cannot Create role without roleData""",
        11:"""Create Role: Cannot Create a role without a name""",
        12:"""Create Role: User is not permitted to create roles"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "PERM_"+str(nr)+": "+cls.ERRORS[nr]+" "+info


class Role(object):
    """
    A Role is a collection of Permissions
    to be assigned to a user at once
    """
    def __init__(self,core):
        """
        initializes a user
        """
        self._core = core

        self._id = None
        self._name = ""

    def get_id(self):
        """
        trivial
        """
        return self._id

    def get_name(self):
        """
        trivial
        """
        return self._name

    def set_id(self,nr):
        """
        trivial
        """
        self._id = int(nr)

    def set_name(self,name):
        """
        trivial
        """
        self._name = str(name)

    def store(self):
        """
        Stores the current state of the role into the database
        """
        sessionmanager = self._core.get_session_manager()

        if self._id is None:
            raise PermissionException(PermissionException.get_msg(0))

        if self._name == "":
            raise PermissionException(PermissionException.get_msg(1))


        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO ROLES (ROL_ID, ROL_NAME) VALUES (?,?) MATCHING (ROL_ID) ;"
        db.query(self._core,stmnt,(self._id,self._name),commit=True)

    def add_permission(self, permission):
        """
        adds a given permission to this role
        """
        sessionmanager = self._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()

        if not session_user.check_permission(permission):
            raise PermissionException(PermissionException.get_msg(3))

        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO ROLERIGHTS (RRI_ROL_ID, RRI_RIG_ID) \
                        VALUES (?, (SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME= ?)) \
                      MATCHING (RRI_ROL_ID, RRI_RIG_ID);";
        db.query(self._core,stmnt,(self._id, permission),commit=True)

    def remove_permission(self, permission):
        """
        removes a given permission from this role
        """
        sessionmanager = self._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()
        
        if not session_user.check_permission(permission):
            raise PermissionException(PermissionException.get_msg(3))

        db = self._core.get_db()
        stmnt = "DELETE FROM ROLERIGHTS WHERE RRI_ROL_ID = ? AND RRI_RIG_ID = (SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME = ?); "
        db.query(self._core,stmnt,(self._id,permission),commit=True)

    def get_permissions(self):
        """
        returns all permissions assigned to this role as an array of strings
        """
        sessionmanager = self._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()

        db = self._core.get_db()
        stmnt = "SELECT RIG_NAME, RIG_ID FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) \
                    WHERE RRI_ROL_ID = ? ;"         
        cur = db.query(self._core,stmnt,(self._id,))
        res = cur.fetchallmap()
        return [row["RIG_NAME"] for row in res]

    def has_permission(self,permission):
        """
        checks if this role has a specific permission
        """
        sessionmanager = self._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()
        
        db = self._core.get_db()
        stmnt = "SELECT RIG_ID FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) \
                    WHERE RRI_ROL_ID = ? AND RIG_NAME = ?;"
        cur = db.query(self._core,stmnt,(self._id,permission))
        res = cur.fetchone()
        return len(res) > 0

    def get_grantable_permissions(self):
        """
        returns the permissions that are grantable to this role
        """
        permissionmanager = self._core.get_permission_manager()
        return permissionmanager.get_grantable_permissions(self)

    def delete(self):
        """
        deletes this role from the database
        """
        sessionmanager = self._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()

        db = self._core.get_db()
        stmnt = "DELETE FROM ROLES WHERE ROL_ID = ? ;"
        db.query(self._core,stmnt,(self._id,),commit=True)

    def assign_to(self,user):
        """
        Assigns this role to a user
        """
        sessionmanager = self._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()

        db = self._core.get_db()
        
        #check if sessionuser has role
        
        has_role = session_user.has_role(self)

        stmnt = "SELECT COUNT(URI_RIG_ID) AS CNT FROM USERRIGHTS WHERE URI_RIG_ID IN \
            (SELECT RRI_RIG_ID FROM ROLERIGHTS WHERE RRI_ROL_ID = ? ) ;"
        cur = db.query(self._core,stmnt,(self._id,))
        res = cur.fetchone()[0]

        has_all_permissions_of_role = res == len(self.get_permissions())

        if not has_role and not has_all_permissions_of_role:
            raise PermissionException(PermissionException.get_msg(7))

        for role in user.get_grantable_roles():
            if role["name"] == self._name:
                stmnt = "UPDATE OR INSERT INTO USERROLES (URO_USR_ID, URO_ROL_ID) \
                    VALUES (?,?) MATCHING (URO_USR_ID, URO_ROL_ID) ;";
                db.query(self._core,stmnt, (user.get_id(),self._id),commit=True)
                return
        raise PermissionException(PermissionException.get_msg(8))

    def revoke_from(self, user):
        """
        Revokes a role from a user 
        """
        sessionmanager = self._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()

        db = self._core.get_db()
        stmnt = "DELETE FROM USERROLES WHERE URO_USR_ID = ? AND URO_ROL_ID = ? ;";
        db.query(self._core,stmnt,(user.get_id(),self._id),commit=True)

    @classmethod
    def set_core(cls, core):
        """
        sets the core of Role 
        """
        cls._core = core

    @classmethod
    def get_grantable_roles(cls,user):
        """
        Returns the Roles that can be granted to a User
        Basically returns all the roles that the sessionUser Owns and the ones that can be made up by the rights of 
        the sessionUser as associative arrays in this style:
        array('name'=>$role->getName(),'id'=>$role->getId(),'granted'=>true)
        """

        #HERE BE DRAGONS! Check algorithm

        sessionmanager = cls._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()
        session_permissions = session_user.get_permissions()

        ret = []

        roles = Role.get_roles()
        for role in roles:
            if session_user.has_role(role):
                ret.append({"name":role.get_name(),
                            "id":role.get_id(),
                            "granted": user.has_role(role)})
                continue
            role_permissions = role.get_permissions()
            for role_permission in role_permissions:
                if role_permission not in session_permissions:
                    break
                ret.append({"name":role.get_name(),
                            "id":role.get_id(),
                            "granted": user.has_role(role)})
                continue
        return ret

    @classmethod
    def has_role_user(cls,role,user):
        """
        Checks if a User has a role, specified by given user and role objects
        """
        db = cls._core.get_db()
        stmnt = "SELECT URO_ROL_ID FROM USERROLES WHERE URO_ROL_ID = ? AND URO_USR_ID = ? ;"
        cur = db.query(cls._core,stmnt,(role.get_id(),user.get_id()))
        res = cur.fetchall()
        return len(res) > 0

    @classmethod
    def get_roles(cls):
        """
        Returns all roles as an array of Objects
        """
        db = cls._core.get_db()
        stmnt = "SELECT ROL_ID, ROL_NAME FROM ROLES ;"
        cur = db.query(cls._core,stmnt)
        ret = []
        for row in cur.fetchallmap():
            role = Role(cls._core)
            role.set_id(row["ROL_ID"])
            role.set_name(row["ROL_NAME"])
            ret.append(role)
        return ret

    @classmethod
    def get_roles_for_user(cls,user):
        """
        Returns all roles that are assigned to a given user as Array of role objects
        """
        db = cls._core.get_db()
        stmnt = "SELECT ROL_ID, ROL_NAME FROM ROLES INNER JOIN USERROLES ON (ROL_ID = URO_ROL_ID) WHERE URO_USR_ID = ? ;"
        cur = db.query(cls._core,stmnt,(user.get_id()))
        ret = []
        for row in cur.fetchallmap():
            role = Role(cls._core)
            role.set_id(row["ROL_ID"])
            role.set_name(row["ROL_NAME"])
            ret.append(role)
        return ret

    @classmethod
    def get_role(cls, role_id):
        """
        Get a role from the database by a given roleId. returns a role object
        """
        db = cls._core.get_db()
        stmnt = "SELECT ROL_ID, ROL_NAME FROM ROLES WHERE ROL_ID = ? ;"
        cur = db.query(cls._core,stmnt,(role_id,))
        res = cur.fetchonemap()
        role = Role(cls._core)
        role.set_id(res["ROL_ID"])
        role.set_name(res["ROL_NAME"])
        return role 

    @classmethod
    def create_role(cls, data=None):
        if data is None:
            raise PermissionException(PermissionException.get_msg(10))
        if data["name"] is None:
            raise PermissionException(PermissionException.get_msg(11))

        db = cls._core.get_db()
        sessionmanager = cls._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()

        role_id = db.get_seq_next("ROL_GEN")
        role = Role(cls._core)
        role.set_id(role_id)
        role.set_name(data["name"])
        role.store()

        if data.has_key("rights"):
            for permission in data["rights"]:
                if permission["granted"]:
                    role.add_permission(permission["name"])
                else:
                    role.remove_permission(permission["name"])
            role.store()

        return role

class Permission(object):
    @classmethod
    def set_core(cls, core):
        """
        sets the core of Permission
        """
        cls._core = core

    @classmethod
    def check_permission(cls, permission, user):
        """
        checks whether a user has a specific permission
        """
        if user.__class__.__name__ == "User":
            user_id = user.get_id()
        elif type(user) != int:
            raise PermissionException(PermissionException.get_msg(9))

        db = cls._core.get_db()
        stmnt = "select 1 as RESULT from RDB$DATABASE  where CAST( ? AS VARCHAR(64)) in(select rig_name \
                from USERROLES \
                left join ROLES \
                  on rol_id = uro_rol_id \
                left join ROLERIGHTS \
                  on rri_rol_id = rol_id \
                left join RIGHTS \
                  on rig_id = rri_rig_id \
                where uro_usr_id = ? \
                union \
                select rig_name \
                from USERRIGHTS \
                left join RIGHTS \
                  on rig_id = uri_rig_id \
                where uri_usr_id = ?) ; " \
        
        cur = db.query(cls._core,stmnt,(permission,user_id,user_id))
        res = cur.fetchone()[0]
        return res == 1

    @classmethod #MODULEINVOLVED
    def create_permission(cls, permission, module=""):
        """
        Creates a new permission in database
        """
        db = cls._core.get_db()
        new_id = db.get_seq_next('RIG_GEN')
        stmnt = "INSERT INTO RIGHTS (RIG_ID, RIG_NAME) VALUES (?,?) ;"
        db.query(cls._core,stmnt,(new_id,module+"."+permission),commit=True)

    @classmethod
    def remove_permission(cls, permission, module=""):
        """
        removes a permission from the database
        """
        db = cls._core.get_db()
        stmnt = "DELETE FROM RIGHTS WHERE RIG_NAME = ? ;"
        db.query(cls._core, stmnt, (permission,),commit=True)

    @classmethod
    def get_permissions_for_user(cls, user):
        """
        Returns all permissions of the given user as a
        list of strings
        """
        if user.__class__.__name__ == "User":
            user_id = user.get_id()
        elif type(user) != int:
            raise PermissionException(PermissionException.get_msg(9))

        db = cls._core.get_db()
        stmnt = "SELECT RIG_NAME \
                  FROM USERRIGHTS \
                    INNER JOIN RIGHTS ON RIG_ID = URI_RIG_ID \
                  WHERE URI_USR_ID = ? \
                  UNION SELECT RIG_NAME \
                  FROM USERROLES \
                    INNER JOIN ROLERIGHTS ON URO_ROL_ID = RRI_ROL_ID \
                    INNER JOIN RIGHTS ON RRI_RIG_ID = RIG_ID \
                  WHERE URO_USR_ID = ?;"
        cur = db.query(cls._core, stmnt, (user.get_id(),user.get_id()))
        res = cur.fetchall()
        return [row[0] for row in res]

    @classmethod
    def get_grantable_permissions(cls,obj):
        """
        Gets the rights that are assignable to either a User or a Role
        The function basically delivers all rights that are assigned to the sessionUser and whether 
        the user to be edited has them granted or not.
        The return values are associative arrays that look like this:
        array('right'=>$sessionRight,'granted'=>true)
        """
        db = cls._core.get_db()
        sessionmanager = cls._core.get_session_manager()
        session_user = sessionmanager.get_current_session_user()
        session_permissions = Permission.get_permissions_for_user(session_user)

        result = []
        result_permissions = []
        skip_permissions = []

        res2 = None

        if obj.__class__.__name__ == "User":
            stmnt1 = "SELECT RIG_NAME FROM RIGHTS INNER JOIN USERRIGHTS ON (RIG_ID = URI_RIG_ID) WHERE URI_USR_ID = ? ;"
            stmnt2 = "SELECT RIG_NAME FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) INNER JOIN USERROLES ON (URO_ROL_ID = RRI_ROL_ID) WHERE URO_USR_ID = ? ;"
            cur = db.query(cls._core,stmnt1,(obj.get_id(),))
            res1 = list(set(cur.fetchallmap()))
            cur = db.query(cls._core,stmnt2,(obj.get_id(),))
            res2 = list(set(cur.fetchallmap()))
        elif obj.__class__.__name__ == "Role":
            stmnt = "SELECT RIG_NAME FROM RIGHTS INNER JOIN ROLERIGHTS ON (RIG_ID = RRI_RIG_ID) WHERE RRI_ROL_ID = ? ;"
            cur = db.query(cls._core,stmnt,(obj.get_id(),))
            res1 = list(set(cur.fetchallmap()))

        result_permissions = [row['RIG_NAME'] for row in res1]
        if res2 is not None:
            skip_permissions = [row['RIG_NAME'] for row in res2]

        for permission in session_permissions:
            if permission in skip_permissions:
                continue
            result.append({'right':permission,'granted':permission in result_permissions})

        return result 

    @classmethod
    def get_id_for_permission(cls,permission):
        """
        Returns the database Id for a given right string identifier
        returns None if not existing
        """
        db = cls._core.get_db()
        stmnt = "SELECT RIG_ID FROM RIGHTS WHERE RIG_NAME = ? ;"
        cur = db.query(cls._core,stmnt,(permission,))
        res = cur.fetchallmap()
        try:
            return res[0]["RIG_ID"]
        except IndexError:
            return None

    @classmethod
    def create_permissions_for_module(cls,module):
        """
        creates the permissions of a newly installed module
        """
        module_name = module.get_name()
        permissions = module.get_permissions()
        for permission in permissions:
            cls.create_permission(permission,module_name)

    @classmethod
    def update_permissions_for_module(cls,module):
        """
        updates the permissions of a module
        """
        module_name = module.get_name()
        permissions = module.get_permissions()
        current = cls.get_permissions_for_module(module)
        for permission in permissions:
            if permission not in current:
                cls.create_permission(permission, module_name)
        for permission in current:
            if permission not in permissions:
                cls.remove_permission(permission, module_name)

    @classmethod
    def remove_permissions_for_module(cls,module):
        """
        removes the permissions of a module
        """
        module_name = module.get_name()
        db = cls._core.get_db()
        stmnt = "DELETE FROM RIGHTS WHERE RIG_NAME LIKE ? ;"
        db.query(cls._core, stmnt, (module_name+"%",),commit=True)

    @classmethod
    def get_permissions_for_module(cls,module):
        """
        gets the permissions of a module
        """
        db = cls._core.get_db()
        stmnt = "SELECT RIG_NAME FROM RIGHTS WHERE RIG_NAME LIKE ? ;"
        cur = db.query(cls._core,stmnt,(module.get_name()+".",))
        rows = cur.fetchallmap()
        rows = rows.values()
        return rows


class PermissionManager(object):
    """
    Permission Manger wraps Role's and Permission's classmethods
    """
    def __init__(self,core):
        """
        Initialize PermissionManager
        """
        self._core = core
        Permission.set_core(core)
        Role.set_core(core)

        self.check_permission = Permission.check_permission
        self.create_permission = Permission.create_permission
        self.create_permissions_for_module = Permission.create_permissions_for_module
        self.remove_permissions_for_module = Permission.remove_permissions_for_module
        self.remove_permission = Permission.remove_permission
        self.get_permissions_for_user = Permission.get_permissions_for_user
        self.get_grantable_permissions = Permission.get_grantable_permissions
        self.get_grantable_roles = Role.get_grantable_roles
        self.has_role_user = Role.has_role_user
        self.get_id_for_permission = Permission.get_id_for_permission
        self.get_roles = Role.get_roles
        self.get_roles_for_user = Role.get_roles_for_user
        self.get_role = Role.get_role
        self.create_role = Role.create_role

    def get_parent(self):
        """
        returns PermissionManager's coreobject
        """
        return self._core

    def get_core(self):
        """
        returns PermissionManager's coreobject
        """
        return self._core