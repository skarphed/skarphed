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

from hashlib import sha512
from random import randrange

ROOT_USER_ID = 1

from skarphedcore.database import Database
from skarphedcore.permission import Permission
from skarphedcore.poke import PokeManager
from skarphedcore.session import Session

from common.enums import ActivityType
from common.errors import UserException

class User(object):
    """
    The User Object represents a user in the Skarphed system
    """
    def __init__(self):
        """
        Initialize User
        """
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
        self._name = unicode(name)

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
        if self.get_id() == ROOT_USER_ID and self.get_name() == "root":
            return True
        return Permission.check_permission(permission,self)

    def authenticate(self,password):
        """
        checks if the given password fits to this user
        """
        if sha512(password.encode('utf-8')+self._salt).hexdigest() == self._password:
            return True
        else:
            raise UserException(UserException.get_msg(2))

    def alter_password(self,new_password,old_password,new_user=False):
        """
        Changes the password of a User
        """
        db = Database()
        if (sha512(old_password.encode('utf-8')+self._salt).hexdigest() == self._password ) \
                != new_user: # != substituts xor
            pw, salt = self._generateSaltedPassword(new_password)
            self.set_password(pw)
            self.set_salt(salt)
            self.store()

            stmnt = "SELECT USR_PASSWORD FROM USERS WHERE USR_ID = ?";
            cur = db.query(stmnt,(self._id,))
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
        pw = sha512(password.encode('utf-8')+salt).hexdigest()
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
        if self.get_id() == ROOT_USER_ID:
            raise UserException(UserException.get_msg(14))

        db = Database()

        stmnt_uri="DELETE FROM USERRIGHTS WHERE URI_USR_ID = ? ;"
        stmnt_uro="DELETE FROM USERROLES WHERE URO_USR_ID = ? ;"
        stmnt_usr="DELETE FROM USERS WHERE USR_ID = ? ;"
        res = db.query(stmnt_uri, (self._id,),commit=True)
        res = db.query(stmnt_uro, (self._id,),commit=True)
        res = db.query(stmnt_usr, (self._id,),commit=True)
        PokeManager.add_activity(ActivityType.USER)

    def store(self):
        """
        stores this user into database
        """
        db = Database()()
        if self._id == None:
            stmnt = "INSERT INTO USERS (USR_ID, USR_NAME, USR_PASSWORD, USR_SALT) \
                      VALUES (?,?,?,?);"
            self.set_id(db.get_seq_next('USR_GEN'))
            db.query(stmnt,(self._id, self._name, self._password, self._salt),commit=True)
        else:
            stmnt =  "UPDATE USERS SET \
                        USR_NAME = ?, \
                        USR_PASSWORD = ?, \
                        USR_SALT = ? \
                      WHERE USR_ID = ?"
            db.query(stmnt,(self._name, self._password, self._salt, self._id),commit=True)
        PokeManager.add_activity(ActivityType.USER)

    def has_role(self, role):
        """
        checks if this user has the given role
        """
        return Permission.has_role_user(role,self)

    def get_permissions(self):
        """
        returns the permissions of this user as list of strings
        """
        return Permission.get_permissions_for_user(self)        

    def get_roles(self):
        """
        returns roles this user is assigned to as list of strings
        """
        return Permission.get_roles_for_user(self)        

    def grant_permission(self, permission, ignore_check=False):
        """
        grants a permission to the user
        """
        db = Database()
        session_user = None
        if not ignore_check:
            session_user = self._core.get_session_manager().get_current_session_user()

        permission_id = Permission.get_id_for_permission(permission)
        if permission_id is None:
            raise UserException(UserException.get_msg(5, permission))
        if not ignore_check and not session_user.check_permission(permission):
            raise UserException(UserException.get_msg(6))
        stmnt = "UPDATE OR INSERT INTO USERRIGHTS VALUES (?,?) MATCHING (URI_USR_ID,URI_RIG_ID) ;"
        db.query(stmnt,(self._id,permission_id),commit=True)
        PokeManager().add_activity(ActivityType.USER)

    def revoke_permission(self,permission, ignore_check=False):
        """
        revokes a permission from the user
        """
        db = Database()
        session_user = None

        if self.get_id() == ROOT_USER_ID and self.get_name() == "root":
            raise UserException(UserException.get_msg(16))

        if not ignore_check:
            session_user = Session.get_current_session_user()

        permission_id = Permission.get_id_for_permission(permission)
        if permission_id is None:
            raise UserException(UserException.get_msg(5, permission))
        if not ignore_check and not session_user.check_permission(permission):
            raise UserException(UserException.get_msg(8))            
        stmnt = "DELETE FROM USERRIGHTS WHERE URI_USR_ID = ? AND URI_RIG_ID = ? ;"
        db.query(stmnt,(self._id,permission_id),commit=True)
        PokeManager().add_activity(ActivityType.USER)

    def get_grantable_permissions(self):
        """
        get the permissions that can be assigned to this user
        returns list of strings
        """
        return Permission.get_grantable_permissions(self)


    def get_grantable_roles(self):
        """
        get the roles that can be assigned to this user
        returns list of dict: 
        {'name':string, 'granted':bool,'id':int  }
        """
        return Permission.get_grantable_roles(self)

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
    def get_user_by_name(cls,username):
        """
        returns the user with the given name or raises exception
        """
        db = Database()

        stmnt = "SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS WHERE USR_NAME= ? ;"
        cur = db.query(stmnt, (username,))
        res = cur.fetchonemap()

        if res is None:
            raise UserException(UserException.get_msg(9,username))
        user = User()
        user.set_id(res['USR_ID'])
        user.set_name(res['USR_NAME'])
        user.set_password(res['USR_PASSWORD'])
        user.set_salt(res['USR_SALT'])
        return user

    @classmethod
    def get_root_user(cls):
        return cls.get_user_by_id(ROOT_USER_ID)

    @classmethod
    def get_user_by_id(cls,nr):
        """
        returns the user with the given id or raises exception
        """
        db = Database()

        stmnt = "SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS WHERE USR_ID= ? ;"
        cur = db.query(stmnt, (nr,))
        res = cur.fetchonemap()

        if res is None:
            raise UserException(UserException.get_msg(11,nr))
        user = User()
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
        db = Database()

        stmnt = "SELECT USR_ID, USR_NAME, USR_PASSWORD, USR_SALT FROM USERS ;"
        cur = db.query(stmnt)
        users = []
        res = cur.fetchallmap()
        for row in res:
            user = User()
            user.set_id(row['USR_ID'])
            user.set_name(row['USR_NAME'])
            user.set_password(row['USR_PASSWORD'])
            user.set_salt(row['USR_SALT'])
            users.append(user)
        return users

    @classmethod
    def _check_password(cls, password):
        if password == "":
            raise UserException(UserException.get_msg(13))
        return True

    @classmethod
    def create_user(cls, username, password):
        """
        creates a new user
        """
        if username == "":
            raise UserException(UserException.get_msg(12))
        try:
            cls.get_user_by_name(username)
        except UserException:
            pass
        else:
            raise UserException(UserException.get_msg(15, username))
        cls._check_password(password)
        user = User()
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

