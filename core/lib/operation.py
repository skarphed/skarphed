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

import os
from daemon import Daemon
from time import sleep
from StringIO import StringIO
from traceback import print_exc

from skarphedcore.configuration import Configuration
from skarphedcore.database import Database
from skarphedcore.core import Core
from skarphedcore.module import Module

from common.errors import OperationException

class Operation(object):
    """
    Contais everything necessary to Handle Operations
    """

    STATUS_PENDING = 0
    STATUS_ACTIVE = 1
    STATUS_FAILED = 2

    VALID_STORAGE_TYPES = ('int','bool','str','unicode')

    def __init__(self, parent_id = None):
        """

        """
        self._id = None
        self._parent = parent_id
        self._values = {}

    @classmethod
    def drop_operation(cls,operation_id):
        """
        Drops an Operation, identified by it's Operation Id and
        it's children recursively
        Drop deletes the Operations from Database
        """
        db = Database()

        stmnt = "SELECT OPE_ID FROM OPERATIONS WHERE OPE_OPE_PARENT = ? AND OPE_STATUS IN (0, 2) ;"
        cur = db.query(stmnt,(operation_id,))
        for row in cur.fetchallmap():
            cls.drop_operation(row["OPE_ID"])

        stmnt = "DELETE FROM OPERATIONS WHERE OPE_ID = ? AND OPE_STATUS IN (0, 2) ;"
        db.query(stmnt,(operation_id,),commit=True)

    @classmethod
    def retry_operation(cls,operation_id):
        """
        Resets the state of an operation and it's children recursively to 0 (PENDING)
        The operation is identified by a given operationId
        """
        db = Database()

        stmnt = "SELECT OPE_ID FROM OPERATIONS WHERE OPE_OPE_PARENT = ? AND OPE_STATUS = 2 ;"
        cur = db.query(stmnt,(operation_id,))
        for row in cur.fetchallmap():
            cls.retry_operation(row["OPE_ID"])

        stmnt = "UPDATE OPERATIONS SET OPE_STATUS = 0 WHERE OPE_ID = ? AND OPE_STATUS = 2 ;"
        db.query(stmnt,(operation_id,),commit=True)

    @classmethod
    def cancel_operation(cls,operation_id):
        """
        Cancels an Operation, identified by it's Operation Id and
        it's children recursively
        Cancel Deletes the Operation from Database
        """
        db = Database()

        stmnt = "SELECT OPE_ID FROM OPERATIONS WHERE OPE_OPE_PARENT = ? AND OPE_STATUS = 0 ;"
        cur = db.query(stmnt,(operation_id,))
        for row in cur.fetchallmap():
            cls.cancel_operation(row["OPE_ID"])

        stmnt = "DELETE FROM OPERATIONS WHERE OPE_ID = ? AND OPE_STATUS = 0 ;"
        db.query(stmnt,(operation_id,),commit=True)

    @classmethod
    def restore_operation(cls, operation_record):
        """
        Restore an Operationobject stored in the database by a Dataset consisting of
        the operation's ID and the operation's TYPE:
        For example:   {"OPE_ID": 100, "OPE_TYPE": "TestOperation"}
        Restores the Operationobject's _values-attribute by the data saved
        in the DB-Table OPERATIONDATA
        """
        classname = operation_record["OPE_TYPE"]
        module = "" #TODO Implement modulename from database if Operation belongs to Module
        is_operation_of_module = False
        exec """
try:
    type(%(class)s)
except NameError,e:
    is_operation_of_module = True"""%{'class':classname}

        if is_operation_of_module:
            exec """
from %(module)s import %(class)s
operation = %(class)s()"""%{'class':classname,'module':module}
        else:
            exec """
operation = %(class)s()"""%{'class':classname}

        operation.set_id(operation_record['OPE_ID'])
        db = Database()
        stmnt = "SELECT OPD_KEY, OPD_VALUE, OPD_TYPE FROM OPERATIONDATA WHERE OPD_OPE_ID = ? ;"
        cur = db.query(stmnt,(operation_record["OPE_ID"],))
        for row in cur.fetchallmap():
            val = row["OPD_VALUE"]
            exec """val = %s(val)"""%row["OPD_TYPE"]
            operation.set_value(row["OPD_KEY"], val)
        return operation

    @classmethod
    def process_children(cls, operation):
        """
        Recursively executes the workloads of Operation's Childoperations
        It hereby catches exceptions in the workloads, sets the OPE_STATUS
        to 2 (FAILED) if a catch occurs, then passes the exception on to the 
        higher layer.
        If an Operation succeeds, it's entry in DB gets deleted
        """
        db = Database()

        stmnt = "SELECT OPE_ID, OPE_TYPE FROM OPERATIONS WHERE OPE_OPE_PARENT = ? ORDER BY OPE_INVOKED ;"
        stmnt_lock = "UPDATE OPERATIONS SET OPE_STATUS = 1 WHERE OPE_ID = ? ;"
        cur = db.query(stmnt,(operation.get_id(),))
        for row in cur.fetchallmap():
            child_operation = cls.restore_operation(row)
            db.query(stmnt_lock,(child_operation.get_id(),),commit=True)
            try:
                cls.process_children(child_operation)
                child_operation.do_workload()
            except Exception,e:
                stmnt_err = "UPDATE OPERATIONS SET OPE_STATUS = 2 WHERE OPE_ID = ? ;"
                db.query(stmnt_err,(int(row["OPE_ID"]),),commit=True)
                #TODO GENERATE ERROR IN LOG
                raise e
            stmnt_delete = "DELETE FROM OPERATIONS WHERE OPE_ID = ?;"
            db.query(stmnt_delete,(child_operation.get_id(),),commit=True)

    @classmethod
    def process_next(cls):
        """
        Sets the status of the next toplevel operation to 1 (ACTIVE)
        Fetches the next toplevel-operation from the database, applies a FILESYSTEMLOCK!
        Which is /tmp/scv_operating.lck !!! 
        """
        db = Database()
        configuration = Configuration()
        if os.path.exists(configuration.get_entry("core.webpath")+"/scv_operating.lck"):
            return False
        lockfile = open(configuration.get_entry("core.webpath")+"/scv_operating.lck","w")
        lockfile.close()
        stmnt_lock = "UPDATE OPERATIONS SET OPE_STATUS = 1 \
                            WHERE OPE_ID IN ( \
                              SELECT OPE_ID FROM OPERATIONS \
                              WHERE OPE_OPE_PARENT IS NULL AND OPE_STATUS = 0 \
                              AND OPE_INVOKED = ( \
                                SELECT MIN(OPE_INVOKED) FROM OPERATIONS  \
                                WHERE OPE_OPE_PARENT IS NULL AND OPE_STATUS = 0) \
                            ) ;"
        stmnt = "SELECT OPE_ID, OPE_TYPE FROM OPERATIONS WHERE OPE_OPE_PARENT IS NULL AND OPE_STATUS = 1 ;"
        db.query(stmnt_lock,commit=True)
        cur = db.query(stmnt)
        res = cur.fetchallmap()
        if len(res) > 0:
            operation = cls.restore_operation(res[0])
            try:
                cls.process_children(operation)
                operation.do_workload()
            except Exception, e:
                stmnt_err = "UPDATE OPERATIONS SET OPE_STATUS = 2 WHERE OPE_ID = ? ;"
                db.query(stmnt_err,(operation.get_id(),),commit=True)
                error = StringIO()
                print_exc(None,error)
                Core().log(error.getvalue())
            ret = True
        else:
            ret = False
        stmnt_delete = "DELETE FROM OPERATIONS WHERE OPE_STATUS = 1 ;"
        db.query(stmnt_delete,commit=True)
        db.commit()
        try:
            os.unlink(configuration.get_entry("core.webpath")+"/scv_operating.lck")
        except OSError,e :
            raise OperationException(OperationException.get_msg(0))
        return ret

    @classmethod
    def get_current_operations_for_gui(cls, operation_types=None):
        """
        Returns all Operations in an associative array.
        The array's indices are the operationIDs
        The Objects contain all information about the operations,
        including the Data
        """
        db = Database()
        #TODO CHECK HOW LISTS ARE HANDLED IN FDB
        if operation_types is not None and type(operation_types) == list:
            stmnt = "SELECT OPE_ID, OPE_OPE_PARENT, OPE_INVOKED, OPE_TYPE, OPE_STATUS FROM OPERATIONS WHERE OPE_TYPE IN (?) ORDER BY OPE_INVOKED ;"
            cur = db.query(stmnt,(operation_types))
        else:
            stmnt = "SELECT OPE_ID, OPE_OPE_PARENT, OPE_INVOKED, OPE_TYPE, OPE_STATUS FROM OPERATIONS ORDER BY OPE_INVOKED ;"
            cur = db.query(stmnt)
        ret = {}
        for row in cur.fetchallmap():
            operation = cls.restore_operation(row)
            custom_values = operation.get_values()

            ret[row["OPE_ID"]] = {"id":row["OPE_ID"],
                                  "parent":row["OPE_OPE_PARENT"],
                                  "invoked":str(row["OPE_INVOKED"]),
                                  "type":row["OPE_TYPE"],
                                  "status":row["OPE_STATUS"],
                                  "data":custom_values}
        return ret

    def get_values(self):
        """
        trivial
        """
        return self._values

    def get_value(self,key):
        """
        trivial
        """
        return self._values(key)

    def set_value(self,key,value):
        """
        trivial
        """
        self._values[key] = value

    def set_parent(self,parent_id):
        """
        trivial
        """
        self._parent = parent_id

    def get_parent(self):
        """
        trivial
        """
        return self._parent

    def set_db_id(self):
        """
        Get a new Operation Id from the Database and assign it to this
        Operation if this Operation's id is null. Afterwards return the 
        new Id
        """
        if self._id is None:
            self._id = Database().get_seq_next('OPE_GEN')
        return self._id

    def set_id(self, nr):
        """
        trivial
        """
        self._id = nr

    def get_id(self):
        """
        trivial
        """
        return self._id

    def store(self):
        """
        Stores this Operation to database.
        Also saves every user defined value in $_values as 
        long as it is a valid type         
        """
        db = Database()

        self.set_db_id()

        stmnt = "UPDATE OR INSERT INTO OPERATIONS (OPE_ID, OPE_OPE_PARENT, OPE_INVOKED, OPE_TYPE) \
                      VALUES (?,?,CURRENT_TIMESTAMP,?) MATCHING (OPE_ID);"
        db.query(stmnt,(self._id,self._parent,self.__class__.__name__),commit=True)

        stmnt = "UPDATE OR INSERT INTO OPERATIONDATA (OPD_OPE_ID, OPD_KEY, OPD_VALUE, OPD_TYPE) \
                      VALUES ( ?, ?, ?, ?) MATCHING(OPD_OPE_ID,OPD_KEY);"
        for key, value in self._values.items():
            typ = str(type(value)).replace("<type '","",1).replace("'>","",1)
            if typ not in Operation.VALID_STORAGE_TYPES:
                continue
            db.query(stmnt,(self._id,key,value,typ),commit=True)

    def do_workload(self):
        """
        This method must be overridden by inheriting classes.
        The code inside this method will be executed when the
        Operation is processed by Operation.processNext or 
        Operation.processChild 
        """
        pass

#MODULEINVOLVED
class ModuleOperation(Operation):
    """
    Abstracts Operations that have to do with modules
    """
    def __init__(self):
        """
        trivial
        """
        Operation.__init__(self)

    def set_values(self,module):
        """
        Sets this operations values from module metadata
        """
        if type(module) == dict:
            self.set_value("name",module["name"])
            self.set_value("hrname",module["hrname"])
            self.set_value("version_major",module["version_major"])
            self.set_value("version_minor",module["version_minor"])
            self.set_value("revision",module["revision"])
            if module.has_key("signature"):
                self.set_value("signature",module["signature"])
        elif module.__class__.__name__ == "Module":
            pass #TODO IMPLEMENT / DISCUSS AFTER IMPLEMENTING MODULE-SUBSYSTEM

    def get_meta(self):
        """
        trivial
        """
        return self._values
    
    @classmethod
    def get_currently_processed_modules(cls):
        """
        Returns an Array of ModuleOperation-Objects that are
        currently listedin the queue 
        """
        db = Database()
        stmnt = "SELECT OPE_ID, OPE_OPE_PARENT, OPE_TYPE FROM OPERATIONS \
                   WHERE OPE_TYPE = 'ModuleInstallOperation' \
                   or OPE_TYPE = 'ModuleUninstallOperation' ;"
        cur = db.query(stmnt);
        ret = []
        for row in cur.fetchallmap():
            ret.append(Operation.restore_operation(row).get_meta())
        return ret

    def optimize_queue(self):
        """
        abtract
        """
        pass

#MODULEINVOLVED
class ModuleInstallOperation(ModuleOperation):
    """
    Manages the process to install a module to this server
    """
    def __init__(self):
        """
        trivial
        """
        ModuleOperation.__init__(self)

    def do_workload(self):
        """
        tell the module manager to install a specific module.
        """
        Module.install_module(self.get_meta())

    def optimize_queue(self):
        """
        optimizes the queue. 
        """
        pass    #TODO Implement

#MODULEINVOLVED
class ModuleUninstallOperation(ModuleOperation):
    """
    Manages the process to uninstall a module to this server
    """
    def __init__(self):
        """
        trivial
        """
        ModuleOperation.__init__(self)

    def do_workload(self):
        """
        tell the module manager to install a specific module.
        """
        module = Module.get_module_by_name(self._values["name"])
        module_manager.uninstall_module(module)

    def optimize_queue(self):
        """
        optimizes the queue. 
        """
        pass    #TODO Implement

#MODULEINVOLVED
class ModuleUpdateOperation(ModuleOperation):
    """
    Manages the process to uninstall a module to this server
    """
    def __init__(self):
        """
        trivial
        """
        ModuleOperation.__init__(self)

    def do_workload(self):
        """
        tell the module manager to install a specific module.
        """
        module = Module.get_module_by_name(self._values["name"])
        module_manager.update_module(module)
        
    def optimize_queue(self):
        """
        optimizes the queue. 
        """
        pass    #TODO Implement

class FailOperation(Operation):
    """
    For unittest purposes: An Operation that always fails
    """
    def __init__(self):
        """
        trivial
        """
        Operation.__init__(self)

    def do_workload(self):
        """
        simply fail
        """
        raise Exception("Failoperation failed")

class TestOperation(Operation):
    """
    For unittest purposes: An Operation that always succeds
    """
    def __init__(self):
        """
        trivial
        """
        Operation.__init__(self)

    def do_workload(self):
        """
        simply succeed
        """
        pass

class OperationDaemon(Daemon):
    """
    This is the deamon that runs to actually execute the scheduled operations
    """
    def __init__(self, pidfile):
        """
        Initialize the deamon
        """
        Daemon.__init__(self,pidfile)

    def stop(self):
        configuration = Configuration()
        if os.path.exists(configuration.get_entry("core.webpath")+"/scv_operating.lck"):
            os.remove(configuration.get_entry("core.webpath")+"/scv_operating.lck") 
        Daemon.stop(self)

    def run(self):
        """
        Do work if there is work to do, otherwise check every two seconds for new work.
        """
        while True:
            while Operation.process_next():
                pass
            sleep(2)

