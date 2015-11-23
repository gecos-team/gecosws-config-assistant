#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# This file is part of Guadalinex
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__ = "Francisco Fuentes Barrera <ffuentes@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from GladeWindow import GladeWindow
import logging
"""
Autoconf redone in Glade
"""
class AutoconfDialog(GladeWindow):
    def __init__(self, mainController):
        self.controller = mainController
        self.gladePath = 'autoconf.glade'
        self.logger = logging.getLogger('AutoconfDialog')
        
        self.data = None
        self.entriesKey = "entries"
        self.visiblesKey= "visibles"
        self.labelsKey = "labels"
        self.trafficLightsKey = "trafficLights"
        
        self.buildUI(self.gladePath)
    
    def addTranslations(self):
        super(AutoconfDialog, self).addTranslations()
    
    def addHandlers(self):
        super(AutoconfDialog, self).addHandlers()
        self.logger.debug("Adding back handler")
        self.handlers["onBack"] = self.backtoMainWindow
        self.logger.debug("Adding connect handler")
        self.handlers["onConn"] = self.connectWithCurrentCreds
    
    # Here comes the handlers
    def backtoMainWindow(self, *args):
        self.logger.debug("Going back to the main window")
        self.controller.backToMainWindowDialog()
    
    def connectWithCurrentCreds(self, *args):
        self.logger.debug("This should connect and check if creds works")
        if self.get_data() is None:
            self.set_data(GecosAccessData())
            
        values = self.getURLUserPassValues()
        self.get_data().set_url(values["URL"])
        self.get_data().set_login(values["user"])
        self.get_data().set_password(values["pass"])
        
        self.controller.requirementsCheck.autoSetup.setup()
    
    def getURLUserPassValues(self):
        values = {}
        values["URL"] = self.builder.get_object("entry1").get_text()
        values["user"] = self.builder.get_object("entry2").get_text()
        values["pass"] = self.builder.get_object("entry3").get_text()
        
        return values
        
    def trafficSignalChange(self, state):
        datafolder = "/usr/local/share/gecosws-config-assistant/"
        
        lightgreenimg  = datafolder+"media/i-status-22-ok.png"
        lightyellowimg = datafolder+"media/i-status-22-grey.png"
        lightgreyimg   = datafolder+"media/i-status-22-off.png"
        
        trafficwidget = self.builder.get_object("image1")
        lightimg = ""
        
        if   (state == 1):
            lightimg = lightgreenimg
        elif (state == 2):
            lightimg = lightyellowimg
        elif (state == 3):
            lightimg = lightgreyimg
            
        trafficwidget.hide()
        trafficwidget.set_from_file(lightimg)
        trafficwidget.show()
    
    def setToInitialState(self):
        # clean
        self.builder.get_object('entry1').set_text('')
        self.builder.get_object('entry2').set_text('')
        self.builder.get_object('entry3').set_text('')
        
        # hide
        self.builder.get_object('label9').set_visible(false)
        self.builder.get_object('label7').set_visible(false)
        self.builder.get_object('entry4').set_visible(false)
        self.builder.get_object('entry5').set_visible(false)
        self.builder.get_object('button2').set_visible(false)
        
        # change
        self.trafficSignalChange(2)
        self.builder.get_object('label11').set_text('PENDIENTE')
    
    def initGUIValues(self):
        self.logger.debug("Initializing GUI values")
        # entries
        entries = {}
        entries["entry1"] = ''
        entries["entry2"] = ''
        entries["entry3"] = ''
        self.guiValues[self.entriesKey] = entries
        
        # visibles
        visibles = {}
#         visibles["entry1"] = True
#         visibles["entry2"] = True
#         visibles["entry3"] = True
        
        visibles["label9"] = False
        visibles["label7"] = False
        visibles["label8"] = False
        visibles["entry4"] = False
        visibles["entry5"] = False
        visibles["button2"] = False
        self.guiValues[self.visiblesKey] = visibles
        
        labels = {}
        labels["label11"] = "PENDIENTE"
        self.guiValues[self.labelsKey] = labels
        
        trafficLights = {}
        
        trafficLights["image1"] = 2
        self.guiValues[self.trafficLightsKey] = trafficLights
    
    def loadCurrentState(self, guiValues):
        super(AutoconfDialog, self).loadCurrentState(guiValues)
        # init entries texts
        for entryKey in self.guiValues[self.entriesKey].keys():
            entryValue = self.guiValues[self.entriesKey][entryKey]
            self.logger.error("Entry key "+entryKey)
            self.logger.error("Entry value "+entryValue)
            self.builder.get_object(entryKey).set_text(entryValue)
         
        # init visibles
        for visibleKey in self.guiValues[self.visiblesKey].keys():
            visibleValue = self.guiValues[self.visiblesKey][visibleKey]
            self.builder.get_object(visibleKey).set_visible(visibleValue)
            
        # init label value
        for labelKey in self.guiValues[self.labelsKey].keys():
            label11Value = self.guiValues[self.labelsKey][labelKey]
            self.builder.get_object(labelKey).set_text(label11Value)
            
        for trafficLightKey in self.guiValues[self.trafficLightsKey].keys():
            trafficLightValue = self.guiValues[self.trafficLightsKey][trafficLightKey]
            self.trafficSignalChange(trafficLightValue)
    
    def show(self):
        self.initGUIValues()
        self.loadCurrentState(self.guiValues)
        # super method
        super(AutoconfDialog, self).show()
    
    def set_data(self, dao_data):
        self.logger.debug("Setting data from DAO")
        self.data = dao_data
        self.handleData()
    
    def get_data(self):
        return self.data
    
    def handleData(self):
        self.initGUIValues()
        entries = {}
        entries["entry1"] = self.data.get_url() if self.data.get_url() is not None else ''
        entries["entry2"] = self.data.get_login() if self.data.get_login() is not None else ''
        entries["entry3"] = self.data.get_password() if self.data.get_password() is not None else ''
        
        self.guiValues[self.entriesKey] = entries
        self.loadCurrentState(self.guiValues)