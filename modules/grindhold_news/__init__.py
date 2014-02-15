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
from StringIO import StringIO

from module import AbstractModule

class ModuleException(Exception): 
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "DB_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class Module(AbstractModule):
    def __init__(self, core):
        AbstractModule.__init__(self,core)
        self._path = os.path.dirname(__file__)
        self._load_manifest()

    """
    BEGIN IMPLEMENTING YOUR MODULE HERE
    """

    def render_pure_html(self,widget_id,args={}):
        db = self._core.get_db()
        ret = StringIO()
        view_manager = self._core.get_view_manager()
        view = view_manager.get_currently_rendering_view()
        if args.has_key("n"): #if specific newsentry is wanted:
            if "author" in args.keys() and "text" in args.keys():
                new_comment_id = db.get_seq_next("${grindhold_news.comments}")
                #TODO: Escape incoming strings
                stmnt = "INSERT INTO ${comments} (COM_ID, COM_AUTHOR, COM_TEXT, COM_NWS_ID, COM_DATE, MOD_INSTANCE_ID) VALUES (?,?,?,?,CURRENT_TIMESTAMP,?);"
                db.query(self,stmnt, (new_comment_id, args["author"], args["text"], int(args["n"]),int(widget_id)),commit=True)
            stmnt = "SELECT NWS_TITLE, NWS_TEXT, USR_NAME, NWS_DATE FROM ${news} INNER JOIN USERS ON USR_ID = NWS_USR_AUTHOR WHERE NWS_ID = ? AND MOD_INSTANCE_ID = ? ;"
            cur = db.query(self, stmnt, (int(args["n"]), int(widget_id)))
            row = cur.fetchonemap()
            if row is None:
                return "<h2> Nothing... </h2><p> Seriously, there is nothing like that here</p><p> We're sorry</p>"
            ret.write("<h3> %s </h3>"%row["NWS_TITLE"])
            ret.write('<div class="newsauthor">%s</div><div class="newsdate">%s</div>'%(row["USR_NAME"],str(row["NWS_DATE"])))
            ret.write('<div class="newsseparator" style="height:1px; border-bottom:1px dotted silver;"></div>')
            ret.write('<p>%s</p>'%row["NWS_TEXT"])

            stmnt = "SELECT COM_AUTHOR, COM_DATE, COM_TEXT FROM ${comments} WHERE COM_NWS_ID = ? AND MOD_INSTANCE_ID = ?"
            cur = db.query(self, stmnt, (int(args["n"]),int(widget_id)))

            for row in cur.fetchallmap():
                ret.write('<div class="commentauthor">Comment by %s</div><div class="commentdate">%s</div>'%(row["COM_AUTHOR"],str(row["COM_DATE"])))
                ret.write('<blockquote>%s</blockquote>'%row["COM_TEXT"])

            target_view = {'p':widget_id, 'c':{widget_id:{"n":args["n"]}}}
            comment_link = view.generate_link_from_dict(target_view)

            ret.write("""
                <form action="%s" method="post">
                    <h4>Leave a Comment:</h4>
                    <p>Name: <input type="text" name="author"></p>
                    <p><textarea name="text" style="width:90%%; height:200px;"></textarea></p>
                    <p><input type="submit" value="Post"></p>
                </form>
                """%comment_link)

            return ret.getvalue()
        else: # Generic newspage requested
            skipstring = ""
            if args.has_key("p"):
                skipstring = " SKIP %d "%int(args["p"])
            stmnt = "SELECT FIRST 10 %s NWS_TITLE, NWS_ID, NWS_TEXT, USR_NAME, NWS_DATE FROM ${news} INNER JOIN USERS ON USR_ID = NWS_USR_AUTHOR WHERE MOD_INSTANCE_ID = ? ;"%skipstring
            cur = db.query(self, stmnt, (widget_id,))
            for row in cur.fetchallmap():
                text = self._shorten_newsentry(row["NWS_TEXT"][:200])

                target_view = {'c':{widget_id:{"n":row["NWS_ID"]}}}
                read_on_link = view.generate_link_from_dict(target_view)

                ret.write("<h3> %s </h3>"%row["NWS_TITLE"])
                ret.write('<div class="newsauthor">%s</div><div class="newsdate">%s</div>'%(row["USR_NAME"],str(row["NWS_DATE"])))
                ret.write('<div class="newsseparator" style="height:1px; border-bottom:1px dotted silver;"></div>')
                ret.write('<p>%s<a href="%s">[ Read on ... ]</a></p><p>&nbsp;</p>'%(text,read_on_link))
            return ret.getvalue()

    def render_html(self,widget_id,args={}):
        return "<h3>news! with js</h3>"

    def render_javascript(self,widget_id,args={}):
        return """<script type="text/javascript"> alert('LOL');</script>"""

    def _shorten_newsentry(self,newsentry):
        while len(newsentry) > 0 and not (newsentry[-1:] == " " or newsentry[-1:] == "\n"):
            newsentry = newsentry[:-1]
        return newsentry+"..."

    def get_news(self,widget_id):
        db = self._core.get_db()
        stmnt = "SELECT NWS_ID, USR_NAME, NWS_DATE, NWS_SHOW, NWS_TITLE FROM ${news} INNER JOIN USERS ON USR_ID = NWS_USR_AUTHOR WHERE MOD_INSTANCE_ID = ?;"
        cur = db.query(self, stmnt, (int(widget_id),))
        ret = {}
        for row in cur.fetchallmap():
            ret[row["NWS_ID"]] = {"author":row["USR_NAME"],
                                  "title":row["NWS_TITLE"],
                                  "date":str(row["NWS_DATE"]),
                                  "show":bool(row["NWS_SHOW"])}
        return ret 


    def get_news_entry(self,widget_id, entry_id):
        db = self._core.get_db()
        stmnt = "SELECT USR_NAME, NWS_DATE, NWS_SHOW, NWS_TITLE, NWS_TEXT FROM ${news} INNER JOIN USERS ON USR_ID = NWS_USR_AUTHOR WHERE NWS_ID = ? AND MOD_INSTANCE_ID = ? ;"
        stmnt_comment = "SELECT COM_AUTHOR, COM_DATE, COM_TEXT, COM_ID FROM ${comments} WHERE COM_NWS_ID = ? AND MOD_INSTANCE_ID = ? ;"

        cur = db.query(self,stmnt,(int(entry_id),int(widget_id)))
        row = cur.fetchonemap()
        ret = {}
        if row:
            ret["author"] = row["USR_NAME"]
            ret["date"] = str(row["NWS_DATE"])
            ret["title"] = row["NWS_TITLE"]
            ret["content"] = row["NWS_TEXT"]
            ret["id"] = int(entry_id)
            ret["show"] = bool(row["NWS_SHOW"])
            ret["comments"] = {}
            cur = db.query(self,stmnt_comment, (int(entry_id), int(widget_id)))
            for commentrow in cur.fetchallmap():
                ret["comments"][commentrow["COM_ID"]] = {
                        "date": str(commentrow["COM_DATE"]),
                        "author":commentrow["COM_AUTHOR"],
                        "content":commentrow["COM_TEXT"],
                    }
        return ret

    def save_news_entry(self, widget_id, entry_data):
        session_manager = self._core.get_session_manager()
        current_user = session_manager.get_current_session_user()
        
        if not current_user.check_permission("grindhold_news.edit"):
            return False

        db = self._core.get_db()

        stmnt = "UPDATE ${news} SET NWS_TITLE = ?, NWS_TEXT = ?, NWS_SHOW = ?  WHERE NWS_ID = ? AND MOD_INSTANCE_ID = ? ;"
        db.query(self, stmnt, (entry_data["title"], entry_data["content"], int(entry_data["show"]), int(entry_data["id"]), widget_id), commit=True)

        if not current_user.check_permission("grindhold_news.deletecomments"):
            return False

        stmnt = "DELETE FROM ${comments} WHERE COM_ID = ? AND MOD_INSTANCE_ID = ?;"
        for comment in entry_data["comments"].keys():
            if entry_data["comments"][comment].has_key("del") and entry_data["comments"][comment]["del"]:
                db.query(self, stmnt, (int(comment), int(widget_id)), commit=True)
        return True

    def create_news_entry(self, widget_id, title=""):
        session_manager = self._core.get_session_manager()
        current_user = session_manager.get_current_session_user()
        
        if not current_user.check_permission("grindhold_news.create"):
            return False

        db = self._core.get_db()
        new_id = db.get_seq_next("${grindhold_news.news}")

        self.generate_view(widget_id, unicode(title), {"n":new_id})

        stmnt = "INSERT INTO ${news} (NWS_ID, NWS_USR_AUTHOR, NWS_SHOW, NWS_DATE, MOD_INSTANCE_ID, NWS_TEXT, NWS_TITLE) VALUES (?, ?, 0, CURRENT_TIMESTAMP, ?, '',  ?) ;"
        db.query(self, stmnt, (new_id, current_user.get_id(), int(widget_id), unicode(title)), commit=True)
        return True

    def store_comment(self, author, comment):
        pass
