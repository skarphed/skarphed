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

import os
import tarfile
import shutil
from StringIO import StringIO
from json import JSONDecoder

class TemplateException(Exception):
    """
    Exceptions for Database-Module
    """
    ERRORS = {
        0:"""At least one Parameter for the Connection is missing"""
        
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "TPL_"+str(nr)+": "+cls.ERRORS[nr]+" "+info


class TemplateManager(object):
    def __init__(self, core):
        self._core = core 
        Template.set_core(self._core)
        
        self.get_current_template = Template.get_current_template
        self.install_from_data = Template.install_from_data
        self.is_template_installed = Template.is_template_installed



class Template(object):
    """
    The template class manages the Data that has to be handled with
    template-packages and represents the template to the 

    Furthermore it hold the template-data in RAM to deliver it faster
    to the clients.
    """

    @classmethod
    def set_core(cls, core):
        cls._core = core

    @classmethod
    def get_current_template(cls):
        """
        Receives .tar.gz'ed data and generates templatedata from it
        """
        db = cls._core.get_db()
        stmnt = "SELECT TPL_NAME, TPL_DESC, TPL_AUTHOR FROM TEMPLATE_INFO ;"

        cur = db.query(cls._core, stmnt)
        tpldata = cur.fetchonemap()

        tpl = Template(cls._core)
        tpl.set_name(tpldata['TPL_NAME'])
        tpl.set_description(tpldata['TPL_DESC'])
        tpl.set_author(tpldata['TPL_AUTHOR'])

        stmnt = "SELECT TPB_BIN_ID FROM TEMPLATE_BINARIES WHERE TPB_TPL_ID = 0 ;"
        cur = db.query(cls._core, stmnt)
        rows = cur.fetchallmap()
        for row in rows:
            tpl.add_binary(row['TPB_BIN_ID'])

        return tpl

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

        configuration = cls._core.get_configuration()
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
        manifest = JSONDecoder().decode(manifest_file.read())
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
        
        css_manager = cls._core.get_css_manager()
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

        #uninstall old template
        if cls.is_template_installed():
            old_template = cls.get_current_template()
            old_template.uninstall()

        new_template = Template(cls._core)
        new_template.set_name(manifest['name'])
        new_template.set_description(manifest['description'])
        new_template.set_author(manifest['author'])

        #create pages
        page_manager = cls._core.get_page_manager()
        binary_manager = cls._core.get_binary_manager()
        for page in pagedata:
            page_manager.create(page['name'],
                                page['internal_name'],
                                page['desc'],
                                page['html_body'],
                                page['html_head'],
                                page['css'],
                                page['minimap'])    

        #put binary into database
        for bin_filename in os.listdir(temp_installpath+"/static"):
            cls._core.log(bin_filename)
            binary=None
            try:
                bin_file = open(temp_installpath+"/static/"+bin_filename,"rb")
                bin_data = bin_file.read()
                bin_file.close()
                if bin_filename.endswith(".png"):
                    binary = binary_manager.create("image/png", bin_data)
                if bin_filename.endswith(".jpeg") or bin_filename.endswith(".jpg"):
                    binary = binary_manager.create("image/jpeg", bin_data)
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
        view_manager = cls._core.get_view_manager()
        view_manager.create_default_view()

        return errorlog


    @classmethod
    def is_template_installed(cls):
        """
        checks whether there is a template installed
        """
        db = cls._core.get_db()
        stmnt = "SELECT COUNT(*) AS AMNT FROM TEMPLATE_INFO ;"
        cur = db.query(cls._core, stmnt)
        row = cur.fetchonemap()
        return bool(row['AMNT'])

    def __init__(self, core):
        self._core = core

        self._name = None
        self._description = None
        self._author = None

        self._binaries = [] #binaries that belong to this template

    def get_id(self):
        """
        everything in scoville should have a get_id()
        """
        return 0

    def set_name(self, name):
        self._name = str(name)

    def get_name(self):
        return self._name 

    def set_description(self, desc):
        self._description = str(desc)

    def get_description(self):
        return self._description

    def set_author(self, author):
        self._author = str(author)

    def get_author(self):
        return self._author

    def add_binary(self, bin_id):
        if bin_id not in self._binaries:
            self._binaries.append(bin_id)

    def remove_binary(self, bin_id):
        self._binaries.remove(bin_id)

    def store(self):
        """
        strors the template information in the database
        """
        db = self._core.get_db()
        stmnt = "UPDATE OR INSERT INTO TEMPLATE_INFO (TPL_ID, TPL_NAME, TPL_DESC, TPL_AUTHOR) \
                 VALUES (0, ?, ?, ? ) MATCHING (TPL_ID) ;"
        db.query(self._core, stmnt, (self._name, self._description, self._author), commit=True)

        stmnt = "INSERT INTO TEMPLATE_BINARIES (TPB_TPL_ID, TPB_BIN_ID) VALUES (?,?) ;"
        for bin_id in self._binaries:
            db.query(self._core, stmnt, (0, bin_id), commit=True)

    def uninstall(self):
        """
        Uninstalls this template
        """
        db = self._core.get_db()

        binary_manager = self._core.get_binary_manager()
        for bin_id in self._binaries:
            bin = binary_manager.get_by_id(bin_id)
            bin.delete()
        stmnt = "DELETE FROM TEMPLATE_BINARIES ;"
        db.query(self._core, stmnt, commit=True)
        
        #Destroy Pages
        page_manager = self._core.get_page_manager()
        page_manager.delete_all_pages()

        #Set Page ID-Generator to 1
        db.set_seq_to('SIT_GEN',1)

        stmnt = "DELETE FROM TEMPLATE_INFO ;"
        db.query(self._core, stmnt, commit=True)
