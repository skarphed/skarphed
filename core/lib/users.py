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

from hashlib import sha512
from random import randrange

class UserException(Exception):
    """
    Exceptions for User-Module
    """
    ERRORS = {
        0:"""The password has not been assigned properly. This shouldnt happen""",
        1:"""Could not set Password: Old password is wrong""",
        2:"""Authentication failed: Wrong Password""",
        3:"""This user is not authorized to delete users""",
        4:"""Granting Permission: This user is not allowed to grant permissions!""",
        5:"""Granting Permission: There is no such permission as """,
        6:"""A User cannot assign a permission that he does not possess himself""",
        7:"""Revoking Permission: This Sessionuser is not allowed to grant or revoke Permissions!""",
        8:"""A User cannot revoke a permission that he does not possess himself""",
        9:"""There is no user with the name """,
        10:"""Get Users: This user is not allowed to view users"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "USR_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class User(object):
    """
    The User Object represents a user in the Scoville system
    """
    def __init__(self,core):
        """
        Initialize User
        """
        self._core = core

        self._id = None
        self._name = None
        self._password = None
        self._salt = None

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

    def set_password(self,password):
        """
        trivial
        """
        self._password = str(password)

    def set_salt(self,salt):
        """
        trivial
        """
        self._salt = str(salt)

    def get_name(self):
        """
        trivial
        """
        return self._name

    def get_id(self):
        """
        trivial
        """
        return self._id

    def check_permission(self,permission):
        """
        Checks if this user has a specific Permission
        """
        permissionmanager = self._core.get_permission_manager()
        return permissionmanager.check_permission(permission,self)

    def authenticate(self,password):
        """
        checks if the given password fits to this user
        """
        if sha512(password+self._salt).hexdigest() == self._password:
            return True
        else:
            raise UserException(UserException.get_msg(2))

    def alter_password(self,new_password,old_password,new_user=False):
        """
        Changes the password of a User
        """
        db = self._core.get_db()
        if (sha512(old_password+self._salt).hexdigest() == self._password ) \
                != new_user: # != substituts xor
            pw, salt = self._generateSaltedPassword(new_password)
            self.set_password(pw)
            self.set_salt(salt)
            self.store()

            stmnt = "SELECT USR_PASSWORD FROM USERS WHERE USR_ID = ?";
            cur = db.query(self._core,stmnt,(self._id,))
            res = cur.fetchone()
            if res[0] != self._password:
                raise UserException(UserException.get_msg(0))
        else:
            raise UserException(UserException.get_msg(1))

    def _generateSaltedPassword(self, password):
        """
        Creates a new Password consisting of pw-hash (sha512) and a 128bit salt
        """
        salt = self._generateRandomString(128)
        pw = sha512(password+salt).hexdigest()
        return (pw, salt)          

    def _generateRandomString(self,length=8):
        """
        generates a random string with a given length. printable chars only
        """
        ret = ""
        for i in range(length):
            x = -1
            while x in (-1,91,92,93,94,95,96,60,61,62,58,59,63,64):
                x = randrange(48,123)
            ret+=chr(x)
        return ret

    def delete(self):
        """
        deletes this user from database
        """
        db = self._core.get_db()

        stmnt_uri="DELETE FROM USERRIGHTS WHERE URI_USR_ID = ? ;"
        stmnt_uro="DELETE FROM USERROLES WHERE URO_USR_ID = ? ;"
        stmnt_usr="DELETE FROM USERS WHERE USR_ID = ? ;"
        res = db.query(self._core, stmnt_uri, (self._id,),commit=True)
        res = db.query(self._core, stmnt_uro, (self._id,),commit=True)
        res = db.query(self._core, stmnt_usr, (self._id,),commit=True)

    def store(self):
        """
        stores this user into database
        """
        db = self._core.get_db()
        if self._id == None:
            stmnt = "INSERT INTO USERS (USR_ID, USR_NAME, USR_PASSWORD, USR_SALT) \
                      VALUES (?,?,?,?);"
            self.set_id(db.get_seq_next('USR_GEN'))
            db.query(self._core,stmnt,(self._id, self._name, self._password, self._salt),commit=True)
        else:
            stmnt =  "UPDATE USERS SET \
                        USR_NAME = ?, \
                        USR_PASSWORD = ?, \
                        USR_SALT = ? \
                      WHERE USR_ID = ?"
            db.query(self._core,stmnt,(self._name, self._password, self._salt, self._id),commit=True)

    def has_role(self, role):
        """
        checks if this user has the given role
        """
        permissionmanager = self._core.get_permission_manager()
        return permissionmanager.has_role_user(role,self)

    def get_permissions(self):
        """
        returns the permissions of this user as list of strings
        """
        permissionmanager = self._core.get_permission_manager()
        return permissionmanager.get_permissions_for_user(self)        

    def get_roles(self):
        """
        returns roles this user is assigned to as list of strings
        """
        permissionmanager = self._core.get_permission_manager()
        return permissionmanager.get_roles_for_user(self)        

    def grant_permission(self, permission):
        """
        grants a permission to the user
        """
        db = self._core.get_db()
        permissionmanager = self._core.get_permission_manager()
        session_user = self._core.get_session_manager().get_current_session_user()

        permission_id = permissionmanager.get_id_for_permission(permission)
        if permission_id is None:
            raise UserException(UserException.get_msg(5, permission))
        if not session_user.check_permission(permission):
            raise UserException(UserException.get_msg(6))
        stmnt = "UPDATE OR INSERT INTO USERRIGHTS VALUES (?,?) MATCHING (URI_USR_ID,URI_RIG_ID) ;"
        db.query(self._core,stmnt,(self._id,permission_id),commit=True)

    def revoke_permission(self,permission):
        """
        revokes a permission from the user
        """
        db = self._core.get_db()
        permissionmanager = self._core.get_permission_manager()
        session_user = self._core.get_session_manager().get_current_session_user()

        permission_id = permissionmanager.get_id_for_permission(permission)
        if permission_id is None:
            raise UserException(UserException.get_msg(5, permission))
        if not session_user.check_permission(permission):
            raise UserException(UserException.get_msg(8))            
        stmnt = "DELETE FROM USERRIGHTS WHERE URI_USR_ID = ? AND URI_RIG_ID = ? ;"
        db.query(self._core,stmnt,(self._id,permission_id),commit=True)

    def get_grantable_permissions(self):
        """
        get the permissions that can be assigned to this user
        returns list of strings
        """
        permissionmanager = self._core.get_permission_manager()
        return permissionmanager.get_grantable_permissions(self)


    def get_grantable_roles(self):
        """
        get the roles that can be assigned to this user
        returns list of dict: 
        {'name':string, 'granted':bool,'id':int  }
        """
        permissionmanager = self._core.get_permission_manager()
        return permissionmanager.get_grantable_roles(self)

    def assign_role(self,role):
        """
        assign a role to this user
        needs role object
        """
        return role.assign_to(self)

    def revoke_role(self,role):
        """
        revoke a role from this user
        needs role object
        """
        return role.revoke_from(self)

    @classmethod
    def set_core(cls, core):
        """
        sets the core of User 
        """
        cls._core = core

    @classmethod
    def get_user_by_name(cls,username):
        """
        returns the user with the given name or raises exception
        """
        db = cls._core.get_db()

        stmnt = "SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS WHERE USR_NAME= ? ;"
        cur = db.query(cls._core, stmnt, (username,))
        res = cur.fetchonemap()

        if res is None:
            raise UserException(UserException.get_msg(9,username))
        user = User(cls._core)
        user.set_id(res['USR_ID'])
        user.set_name(res['USR_NAME'])
        user.set_password(res['USR_PASSWORD'])
        user.set_salt(res['USR_SALT'])
        return user

    @classmethod
    def get_user_by_id(cls,nr):
        """
        returns the user with the given id or raises exception
        """
        db = cls._core.get_db()

        stmnt = "SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS WHERE USR_ID= ? ;"
        cur = db.query(cls._core, stmnt, (nr,))
        res = cur.fetchonemap()

        if res is None:
            raise UserException(UserException.get_msg(9,username))
        user = User(cls._core)
        user.set_id(res['USR_ID'])
        user.set_name(res['USR_NAME'])
        user.set_password(res['USR_PASSWORD'])
        user.set_salt(res['USR_SALT'])
        return user

    @classmethod
    def get_users(cls):
        """
        returns all users as array of User-objects
        """
        db = cls._core.get_db()

        stmnt = "SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS ;"
        cur = db.query(cls._core, stmnt)
        users = []
        res = cur.fetchallmap()
        for row in res:
            user = User(cls._core)
            user.set_id(row['USR_ID'])
            user.set_name(row['USR_NAME'])
            user.set_password(row['USR_PASSWORD'])
            user.set_salt(row['USR_SALT'])
            users.append(user)
        return users

    @classmethod
    def create_user(cls, username, password):
        """
        creates a new user
        """
        user = User(cls._core)
        user.set_name(username)
        user.set_password("")
        user.set_salt("")
        user.store()
        user.alter_password(password, "", True)
        return user

    @classmethod
    def get_users_for_admin_interface(cls):
        """
        only returns data necesssary for getUsersForAdminInterface
        """
        users = cls.get_users()
        ret = []
        for user in users:
            ret.append({"name":user.get_name(),"id":user.get_id()})
        return ret

class UserManager(object):
    """
    UserManger wraps User's classmethods
    """
    def __init__(self,core):
        """
        Initialize UserManager
        """
        self._core = core
        User.set_core(core)

        self.get_user_by_id = User.get_user_by_id
        self.get_user_by_name = User.get_user_by_name
        self.get_users = User.get_users
        self.create_user = User.create_user
        self.get_users_for_admin_interface = User.get_users_for_admin_interface

    def get_parent(self):
        """
        returns Database's coreobject
        """
        return self._core

    def get_core(self):
        """
        returns Database's coreobject
        """
        return self._core

