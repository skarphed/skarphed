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

from data.Generic import GenericScovilleObject
from Widget import Widget

import tarfile
import shutil
import glob
import base64

import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5

class Module(GenericScovilleObject):
    def __init__(self,parent, data = {}):
        GenericScovilleObject.__init__(self)
        self.par = parent
        self.data = data
        self.updated()
        self.loadWidgets()

        if not os.path.exists(os.path.expanduser("~/.scovilleadmin/modulegui")):
            os.mkdir(os.path.expanduser("~/.scovilleadmin/modulegui"))
            open(os.path.expanduser("~/.scovilleadmin/modulegui")+"/__init__.py","w").close()

    def getName(self):
        if self.data.has_key('hrname'):
            return self.data['hrname']+" ["+self.getPrintableVersion()+"]"
        else:
            return "Unknown Module"
    
    def getId(self):
        if self.data.has_key('serverModuleId'):
            return self.data['serverModuleId']
        else:
            return None
    
    def getPrintableVersion(self):
        return str(self.data['version_major'])+"."+str(self.data['version_minor'])+"."+str(self.data['revision'])
    
    def getVersionFolderString(self):
        return "v"+str(self.data['version_major'])+"_"+str(self.data['version_minor'])+"_"+str(self.data['revision'])

    def getModuleName(self):
        if self.data.has_key('name'):
            return self.data['name']
        else:
            return None
    
    def refresh(self,data):
        self.data = data
        self.updated()
    
    def loadCssPropertySetCallback(self,result):
        self.cssPropertySet = result
        self.updated()
    
    def loadCssPropertySet(self):
        obj_id = self.getId()
        if obj_id is not None:
            self.getApplication().doRPCCall(self.getModules().getScoville(),self.loadCssPropertySetCallback, "getCssPropertySet", [obj_id,None,None])
    
    def getCssPropertySet(self):
        return self.cssPropertySet
    
    def setCssPropertySet(self,cssPropertySet):
        self.cssPropertySet['properties'] = cssPropertySet
    
    def saveCssPropertySetCallback(self,json):
        self.loadCssPropertySet()
    
    def saveCssPropertySet(self):
        self.getApplication().doRPCCall(self.getModules().getScoville(),self.saveCssPropertySetCallback, "setCssPropertySet", [self.cssPropertySet])
    
    def loadWidgetsCallback(self,data):
        widgetIds = [w.getId() for w in self.children]
        for widget in data:
            if widget['id'] not in widgetIds:
                self.addChild(Widget(self,widget))
            else:
                self.getWidgetById(widget['id']).refresh(widget)
                widgetIds.remove(widget['id'])
        for wgt in self.children:
            if wgt.getId() in widgetIds:
                self.children.remove(wgt)
                wgt.destroy()
        self.updated()
        self.getModules().updated()
        
    def loadWidgets(self):
        self.getApplication().doRPCCall(self.getModules().getScoville(),self.loadWidgetsCallback, "getWidgetsOfModule", [self.getId()])
    
    def loadGuiCallback(self, result):
        modulepath = os.path.expanduser("~/.scovilleadmin/modulegui/")
        if not os.path.exists(modulepath+self.getModuleName()):
            os.mkdir(modulepath+self.getModuleName())

        open(modulepath+self.getModuleName()+"/__init__.py","w").close()

        if not os.path.exists(modulepath+self.getModuleName()+"/"+self.getVersionFolderString()):
            os.mkdir(modulepath+self.getModuleName()+"/"+self.getVersionFolderString())

        data = result['data']
        signature = base64.b64decode(result['signature'])
        libstring = result['libstring']

        publickeyraw = self.getModules().getScoville().getPublicKey()
        publickey = RSA.importKey(publickeyraw)
        hashed = SHA256.new(data)
        verifier = PKCS1_v1_5.new(publickey)
        if verifier.verify(hashed, signature):
            f = open(modulepath+self.getModuleName()+"/"+self.getVersionFolderString()+"/gui.tar.gz","w")
            f.write(base64.b64decode(data))
            f.close()
            tar = tarfile.open(modulepath+self.getModuleName()+"/"+self.getVersionFolderString()+"/gui.tar.gz","r:gz")
            tar.extractall(modulepath+self.getModuleName()+"/"+self.getVersionFolderString())
            tar.close()
            os.unlink(modulepath+self.getModuleName()+"/"+self.getVersionFolderString()+"/gui.tar.gz")
            for filename in glob.glob(modulepath+self.getModuleName()+"/"+self.getVersionFolderString()+libstring+"/"+self.getModuleName()+"/"+self.getVersionFolderString()+"/gui/*"):
                shutil.move(filename, modulepath+self.getModuleName()+"/"+self.getVersionFolderString()+"/")
            shutil.rmtree(modulepath+self.getModuleName()+"/"+self.getVersionFolderString()+"/"+libstring.split("/")[1])
            self.updated()
        else:
            raise Exception("GuiData did not validate against Signature!")
            

    def loadGui(self):
        self.getApplication().doRPCCall(self.getModules().getScoville(),self.loadGuiCallback, "getGuiForModule", [self.getId()])

    def isGuiAvailable(self):
        return os.path.exists(os.path.expanduser("~/.scovilleadmin/modulegui/"+self.getModuleName()+\
                                                 "/"+self.getVersionFolderString()))

    def createWidgetCallback(self, json):
        self.loadWidgets()
    
    def createWidget(self,name):
        self.getApplication().doRPCCall(self.getModules().getScoville(),self.createWidgetCallback, "createWidget", [self.getId(),name])
    
    def getWidgetById(self,obj_id):
        for widget in self.children:
            if widget.getId() == obj_id:
                return widget
        return None
    
    def getAllWidgets(self):
        return self.children
    
    def getPar(self):
        return self.par
    
    def getModules(self):
        return self.getPar()
    
