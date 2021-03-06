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
import tarfile
import shutil
from StringIO import StringIO
from json import JSONDecoder

from skarphedcore.configuration import Configuration
from skarphedcore.database import Database
from skarphedcore.core import Core
from skarphedcore.module import ModuleManager
from skarphedcore.binary import Binary
from skarphedcore.css import CSSManager
from skarphedcore.view import Page, View
from skarphedcore.poke import PokeManager

from common.enums import ActivityType
from common.errors import TemplateException


class Template(object):
    """
    The template class manages the Data that has to be handled with
    template-packages and represents the template to the 

    Furthermore it hold the template-data in RAM to deliver it faster
    to the clients.
    """
    @classmethod
    def get_current_template(cls):
        """
        Receives .tar.gz'ed data and generates templatedata from it
        """
        db = Database()
        stmnt = "SELECT TPL_NAME, TPL_DESC, TPL_AUTHOR FROM TEMPLATE_INFO ;"

        cur = db.query(stmnt)
        tpldata = cur.fetchonemap()
        if tpldata is None:
            raise TemplateException(TemplateException.get_msg(1))

        tpl = Template()
        tpl.set_name(tpldata['TPL_NAME'])
        tpl.set_description(tpldata['TPL_DESC'])
        tpl.set_author(tpldata['TPL_AUTHOR'])

        stmnt = "SELECT TPB_BIN_ID FROM TEMPLATE_BINARIES WHERE TPB_TPL_ID = 0 ;"
        cur = db.query(stmnt)
        rows = cur.fetchallmap()
        for row in rows:
            tpl.add_binary(row['TPB_BIN_ID'])

        return tpl

    @classmethod
    def fetch_templates_for_gui(cls):
        repository = ModuleManager.get_repository()
        data = repository.get_all_templates()
        return data

    @classmethod
    def install_from_repo(cls, nr):
        repository = ModuleManager.get_repository()
        data = repository.download_template(nr)
        return cls.install_from_data(data)

    @classmethod
    def install_from_data(cls, data):
        """
        Receives .tar.gz'ed data and generates templatedata from it
        First validates the data. While validating it tracks all occuring
        errors in the errorlog. If one severe error happens during validation,
        the method stops before actually doing write-operations and returns
        the errorlog to the client
        Otherwise, it executes the installation and returns all 
        non-severe errors (warnings).
        """
        def cleanup(path):
            shutil.rmtree(path)

        #TODO: Mutex this operation

        errorlog = []

        configuration = Configuration()
        webpath = configuration.get_entry("core.webpath")
        temp_installpath = webpath+"/tpl_install"
        os.mkdir(temp_installpath)

        tar = open(temp_installpath+"/tpl.tar.gz","w")
        tar.write(data)
        tar.close()

        tar = tarfile.open(temp_installpath+"/tpl.tar.gz","r:gz")
        tar.extractall(temp_installpath)
        tar.close()

        os.unlink(temp_installpath+"/tpl.tar.gz")

        manifest_file = open(temp_installpath+"/manifest.json","r")
        try:
            manifest = JSONDecoder().decode(manifest_file.read())
        except ValueError,e:
            errorlog.append({'severity':1,
                           'type':'PackageFile',
                           'msg':'JSON seems to be corrupt'})
            cleanup(temp_installpath)
            return errorlog
        manifest_file.close()

        #BEGIN TO VALIDATE DATA

        try:
            f = open(temp_installpath+"/general.css")
            general_css = f.read()
            f.close()
        except IOError,e:
            errorlog.append({'severity':1,
                           'type':'PackageFile',
                           'msg':'File not in Package general.css'})
        
        css_manager = CSSManager()
        general_csspropertyset = None
        try:
            general_csspropertyset = css_manager.create_csspropertyset_from_css(general_css)
            general_csspropertyset.set_type_general()
        except Exception, e:
            errorlog.append({'severity':1,
                           'type':'CSS-Data',
                           'msg':'General CSS File does not Contain Valid CSS '+str(e)})
        
        pagedata = [] # Prepared filedata for execution into Database

        for page in manifest['pages']:
            if page['filename'].endswith(".html"):
                name = page['filename'].replace(".html","",1)
            elif page['filename'].endswith(".htm"):
                name = page['filename'].replace(".htm","",1)
            else:
                errorlog.append({'severity':1,
                               'type':'PageData',
                               'msg':'Invalid format (allowed is .html and .htm: '+page['filename']})

            try:
                f = open(temp_installpath+"/"+page['filename'])
                html = f.read()
                f.close()
            except IOError,e:
                errorlog.append({'severity':1,
                               'type':'PageFile',
                               'msg':'File not in Package '+page['filename']})
                continue

            try:
                f = open(temp_installpath+"/"+name+"_head.html","r")
                html_head = f.read()
                f.close()
            except IOError,e:
                errorlog.append({'severity':0,
                               'type':'PageFile',
                               'msg':'File not in Package '+name+"_head.html"})
                html_head = ""

            try:
                f = open(temp_installpath+"/static/"+name+".css")
                css = f.read()
                f.close()
            except IOError,e:
                errorlog.append({'severity':1,
                               'type':'PageFile',
                               'msg':'File not in Package static/'+name+".css"})
                continue

            try:
                f = open(temp_installpath+"/static/"+name+"_minimap.png","rb")
                minimap = f.read()
                f.close()
                os.unlink(temp_installpath+"/static/"+name+"_minimap.png")
            except IOError,e:
                errorlog.append({'severity':0,
                               'type':'PageFile',
                               'msg':'File not in Package static/'+name+"_minimap.png"})
                minimap = None

            pagedata.append({'name':page['name'],
                             'desc':page['desc'],
                             'html_body':html,
                             'html_head':html_head,
                             'css':css,
                             'minimap':minimap,
                             'internal_name':name})
        
        if len(errorlog) > 0:
            is_severe_error = False
            for error in errorlog:
                if error['severity'] >= 1:
                    is_severe_error = True
                    break
            if is_severe_error:
                cleanup(temp_installpath)
                return errorlog

        # BEGIN TO WRITE DATA

        #release maintenance mode at the end?
        release_maintenance_mode = not cls.is_template_installed()

        #uninstall old template
        if cls.is_template_installed():
            old_template = cls.get_current_template()
            old_template.uninstall()

        new_template = Template()
        new_template.set_name(manifest['name'])
        new_template.set_description(manifest['description'])
        new_template.set_author(manifest['author'])

        #create pages
        for page in pagedata:
            Page.create(page['name'],
                                page['internal_name'],
                                page['desc'],
                                page['html_body'],
                                page['html_head'],
                                page['css'],
                                page['minimap'])    

        #put binary into database
        for bin_filename in os.listdir(temp_installpath+"/static"):
            binary=None
            try:
                bin_file = open(temp_installpath+"/static/"+bin_filename,"rb")
                bin_data = bin_file.read()
                bin_file.close()
                # TODO: Find more generic way to determine mimetype
                if bin_filename.endswith(".png"):
                    binary = Binary.create("image/png", bin_data)
                if bin_filename.endswith(".jpeg") or bin_filename.endswith(".jpg"):
                    binary = Binary.create("image/jpeg", bin_data)
                else:
                    binary = Binary.create("application/octet-stream", bin_data)
                if binary is not None:
                    binary.set_filename(bin_filename)
                    binary.store()

                    new_template.add_binary(binary.get_id())

            except IOError, e:
                errorlog.append({'severity':0,
                               'type':'PageFile',
                               'msg':'File seems broken static/'+bin_filename})


        #read general.css into CSSPropertysets
        general_csspropertyset.store()

        new_template.store()
        cleanup(temp_installpath)

        #create a defaultview if there isnt
        View.create_default_view()

        if release_maintenance_mode:
            Core().deactivate_maintenance_mode()

        return errorlog


    @classmethod
    def is_template_installed(cls):
        """
        checks whether there is a template installed
        """
        db = Database()
        stmnt = "SELECT COUNT(*) AS AMNT FROM TEMPLATE_INFO ;"
        cur = db.query(stmnt)
        row = cur.fetchonemap()
        return bool(row['AMNT'])

    def __init__(self):
        self._name = None
        self._description = None
        self._author = None

        self._binaries = [] #binaries that belong to this template

    def get_id(self):
        """
        everything in skarphed should have a get_id()
        """
        return 0

    def set_name(self, name):
        self._name = unicode(name)

    def get_name(self):
        return self._name 

    def set_description(self, desc):
        self._description = unicode(desc)

    def get_description(self):
        return self._description

    def set_author(self, author):
        self._author = unicode(author)

    def get_author(self):
        return self._author

    def add_binary(self, bin_id):
        if bin_id not in self._binaries:
            self._binaries.append(bin_id)

    def remove_binary(self, bin_id):
        self._binaries.remove(bin_id)

    def store(self):
        """
        stores the template information in the database
        """
        db = Database()
        stmnt = "UPDATE OR INSERT INTO TEMPLATE_INFO (TPL_ID, TPL_NAME, TPL_DESC, TPL_AUTHOR) \
                 VALUES (0, ?, ?, ? ) MATCHING (TPL_ID) ;"
        db.query(stmnt, (self._name, self._description, self._author), commit=True)

        stmnt = "INSERT INTO TEMPLATE_BINARIES (TPB_TPL_ID, TPB_BIN_ID) VALUES (?,?) ;"
        for bin_id in self._binaries:
            db.query(stmnt, (0, bin_id), commit=True)
        PokeManager.add_activity(ActivityType.TEMPLATE)

    def uninstall(self):
        """
        Uninstalls this template
        """
        db = Database()

        for bin_id in self._binaries:
            bin = Binary.get_by_id(bin_id)
            bin.delete()
        stmnt = "DELETE FROM TEMPLATE_BINARIES ;"
        db.query(stmnt, commit=True)
        
        #Destroy Pages
        Page.delete_all_pages()

        #Set Page ID-Generator to 1
        db.set_seq_to('SIT_GEN',1)

        stmnt = "DELETE FROM TEMPLATE_INFO ;"
        db.query(stmnt, commit=True)

        PokeManager.add_activity(ActivityType.TEMPLATE)
