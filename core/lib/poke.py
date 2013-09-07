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

import json

from common.errors import PokeException
from common.enums import ActivityType

class PokeManager(object):
    """
    The PokeManager manages pokes

    The poke system is a polling system that keeps skarphed clients up to 
    date and informed about changes that happen on the server.

    Pokes are messages that are sent from skarphed-admin to skarphed-core
    and get an answer that contains in which groups of datasets the admin must
    refresh it's data.

    The pokes happen periodically, but the period is increasing if previous pokes
    resulted in more activity, on the other hand decreasing when there is no activity
    on the skarphed-core. There is a maxvalue for the highest pokerate and a minvalue
    for the slowest pokerate.
    """

    @classmethod
    def __init__(cls, core):
        """
        trivial
        """
        cls._core = core
        ActivityReport.set_core(core)

    @classmethod
    def add_activity(cls, activity_type):
        """
        Registers an activity to the Pokesystem
        """
        session_manager = cls._core.get_session_manager()
        session = session_manager.get_current_session()

        activity = Activity(cls._core)
        if session is not None:
            activity.set_session_id(session.get_id())
        
        activity.set_activity_type(activity_type)
        activity.store()


    @classmethod
    def poke(cls):
        """
        Pulls together poke-response information for the current client
        """
        activity_report = ActivityReport.generate()
        session_manager = cls._core.get_session_manager()
        session = session_manager.get_current_session()
        db = cls._core.get_db()
        stmnt = "UPDATE OR INSERT INTO SESSIONPOKE (SPO_SES_ID, SPO_ATV_ID) VALUES (?, \
                MAXVALUE(COALESCE((SELECT SPO_ATV_ID FROM SESSIONPOKE WHERE SPO_SES_ID = ?), 0) ,?)) MATCHING (SPO_SES_ID) ;"
        db.query(cls._core, stmnt, (session.get_id(), session.get_id(), activity_report._latest_id+1), commit=True)
        cls.cleanup()
        return activity_report.to_dict()

    @classmethod
    def cleanup(cls):
        """
        Remove activities that are no longer needed
        """
        session_manager = cls._core.get_session_manager()
        session = session_manager.get_current_session()

        db = cls._core.get_db()
        stmnt = "DELETE FROM SESSIONPOKE WHERE SPO_SES_ID IN (SELECT SES_ID FROM SESSIONS WHERE SES_EXPIRES < NOW()) ;"
        db.query(cls._core, stmnt, (session.get_id(),), commit=True)
        stmnt = "DELETE FROM ACTIVITIES WHERE ATV_ID < COALESCE ((SELECT MIN(SPO_ATV_ID) FROM SESSIONPOKE WHERE SPO_SES_ID != ?),0) ;"
        db.query(cls._core, stmnt, (session.get_id(),), commit=True)


class Activity(object):
    """
    An activity is a change that occurs on a skarphed core
    """
    def __init__(self, core):
        self._core = core

        self._id = None
        self._activity_type = None
        self._session_id = None
        self._target = None # For later use for a more specific 

    def get_id(self):
        return self._id

    def set_id(self, nr):
        self._id = int(nr)

    def get_activity_type(self):
        return self._activity_type

    def set_activity_type(self, activity_type):
        if not ActivityType.is_valid_value(activity_type):
            raise PokeException(PokeException.get_msg(0, activity_type))
        self._activity_type = int(activity_type)

    def get_session_id(self):
        return self._session_id

    def set_session_id(self, session_id):
        self._session_id = session_id

    def store(self):
        db = self._core.get_db()
        if self._id is None:
            self.set_id(db.get_seq_next("ATV_GEN"))
        stmnt = "UPDATE OR INSERT INTO ACTIVITIES (ATV_ID, ATV_TYPE, ATV_SES_ID) VALUES (?,?,?) MATCHING (ATV_ID) ;"
        db.query(self._core, stmnt, (self.get_id(), self.get_activity_type(), self.get_session_id()), commit=True)

    def delete(self):
        db = self._core.get_db()
        stmnt = "DELETE FROM ACTIVITIES WHERE ATV_ID = ? ;"
        db.query(self._core, stmnt, (self.get_id(),), commit=True)

class ActivityReport(object):
    """
    Generates packed information about Activities that happened
    since the user checked for activities last time
    """
    @classmethod
    def set_core(cls, core):
        cls._core = core

    def __init__(self):
        self._activities = []
        self._latest_id = 0
        self._amount = 0

    def to_dict(self):
        """
        Returns a dictionary report in the form of:
        {"amount":<int>,"activity_types":[(<int>),(<int>),(<int>),...]}
        """
        ret = {}
        ret["amount"] = self._amount
        ret["activity_types"] = [a.get_activity_type() for a in self._activities]
        return ret

    @classmethod
    def generate(cls):
        """
        Generates an Activity Report. This report contains,
        how many activities have happened since the last poke
        further it contains the activity types.
        """
        session_manager = cls._core.get_session_manager()
        session  = session_manager.get_current_session()

        db = cls._core.get_db()
        stmnt = "SELECT ATV_TYPE, MAX(ATV_ID) AS LATEST_ID, COUNT(ATV_ID) AS AMOUNT FROM ACTIVITIES WHERE ATV_SES_ID != ? OR ATV_SES_ID IS NULL AND ATV_ID >= \
                COALESCE((SELECT SPO_ATV_ID FROM SESSIONPOKE WHERE SPO_SES_ID = ?),0) GROUP BY ATV_TYPE;"
        cur = db.query(cls._core, stmnt, (session.get_id(), session.get_id()))

        activity_report = ActivityReport()

        res = cur.fetchallmap()
        for row in res:
            activity = Activity(cls._core)
            activity.set_id(row["LATEST_ID"])
            activity.set_activity_type(row["ATV_TYPE"])

            activity_report._activities.append(activity)

            if activity_report._latest_id < row["LATEST_ID"]:
                activity_report._latest_id = row["LATEST_ID"]

            activity_report._amount += row["AMOUNT"]
        
        return activity_report
