#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from __builtin__ import True

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
__copyright__ = "Copyright (C) 2015, Junta de Andaluc�a <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from GladeWindow import GladeWindow
from gi.repository import Gtk, Gdk
import logging
import gettext
from gettext import gettext as _
"""
ConnectWithGecosCC redone in Glade
"""
class ConnectWithGecosDialog(GladeWindow):
    
    def __init__(self, mainController):
        self.mainController = mainController
        self.controller = self.mainController.connectWithGecosCC
        self.gladePath = 'gecoscon.glade'
        self.logger = logging.getLogger('ConnectWithGecosDialog')
        
        self.gecos_access_data = None
        self.workstation_data = None
        
        self.buildUI(self.gladePath)
        
        #combo stuff
        self.lastComboValue = -1
        self.store = self.getElementById('liststore1')
        self.combo = self.getElementById('combobox1')
        
        renderer_text = Gtk.CellRendererText()
        self.combo.pack_start(renderer_text, True)
        self.combo.add_attribute(renderer_text, "text", 0)
        
        self.extractGUIElements()
    
    def get_gecos_access_data(self):
        return self.__gecos_access_data

    def get_workstation_data(self):
        return self.__workstation_data

    def set_gecos_access_data(self, value):
        self.__gecos_access_data = value

    def set_workstation_data(self, value):
        self.__workstation_data = value
    
    def addTranslations(self):
        super(ConnectWithGecosDialog, self).addTranslations()
    
    def addHandlers(self):
        super(ConnectWithGecosDialog, self).addHandlers()
        self.logger.info('Calling child specific handler')
        # add new handlers here
        self.logger.debug("Adding search handler")
        self.handlers["onSrch"] = self.searchOUHandler
        self.logger.debug("Adding connection handler")
        self.handlers["onConn"] = self.connectToHandler
        self.logger.debug("Adding accept handler")
        self.handlers["onAcpt"] = self.acceptHandler
        self.logger.debug("Adding disconnect handler")
        self.handlers["onDcon"] = self.disconnectHandler
        self.logger.debug("Adding on change combobox handler")
        self.handlers["onChng"] = self.onChangeComboBox
    
    def searchOUHandler(self, *args):
        self.logger.debug("This should search OUs and call patternSearch")
        self.patternSearch()
        
    def connectToHandler(self, *args):
        self.logger.debug("This should connecto to GECOS CC")
        self.connect()
    
    def acceptHandler(self, *args):
        self.logger.debug("This should accept and cancel the action")
        self.cancel()
    
    def disconnectHandler(self, *args):
        self.logger.debug("This should disconnect from GECOS CC")
        self.disconnect()
        
    def onChangeComboBox(self, combo):
        self.logger.debug("This should show up each time the combobox is changed")
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            value = model[tree_iter][0]
            self.lastComboValue = value
    
    def initGUIValues(self, calculatedStatus):
        pass
        
    def loadCurrentState(self, guiValues):
        self.preShow()
        super(ConnectWithGecosDialog, self).loadCurrentState(guiValues)
    
    def extractGUIElements(self):
        self.workstationNameEntry = self.getElementById("entry1") 
        self.disconnectButton = self.getElementById("button2")
        self.connectButton = self.getElementById("button3")
        
        self.gecosCCurlEntry = self.getElementById("entry2")
        self.gecosCCuserEntry = self.getElementById("entry3")
        self.gecosCCpassEntry = self.getElementById("entry4")
        
        self.selectOUVar = self.getElementById("combobox1")
        self.searchFilterEntry = self.getElementById("entry5")
    
    def preShow(self):
        self.logger.debug("Pre show method")
        
        workstation_data = self.get_workstation_data()
        if workstation_data is not None:
            if (workstation_data.get_name() is not None
                and workstation_data.get_name().strip() != ''):
                self.workstationNameEntry.set_text(workstation_data.get_name())

        gecos_data = self.get_gecos_access_data()
        if gecos_data is not None:
            self.disconnectButton.set_label(_("Disconnect from GECOS CC"))
            
            if (gecos_data.get_url() is not None
                and gecos_data.get_url().strip() != ''):
                self.gecosCCurlEntry.set_text(gecos_data.get_url())

            if (gecos_data.get_login() is not None
                and gecos_data.get_login().strip() != ''):
                self.gecosCCuserEntry.set_text(gecos_data.get_login())
            
            if (gecos_data.get_password() is not None
                and gecos_data.get_password().strip() != ''):
                self.gecosCCpassEntry.set_text(gecos_data.get_password())
            
        else:
            #elem
            self.connectButton.set_label(_("Connect to GECOS CC"))
    
    def getOUComboValue(self):
        return self.lastComboValue
    
    def loadOUCombo(self, values):
        for value in values:
            self.store.append([value])

    def connect(self):
        self.logger.debug("connect")
        
        if self.get_gecos_access_data() is None:
            self.set_gecos_access_data(GecosAccessData())
        self.get_gecos_access_data().set_url(self.gecosCCurlEntry.get_text())
        self.get_gecos_access_data().set_login(self.gecosCCuserEntry.get_text())
        self.get_gecos_access_data().set_password(self.gecosCCpassEntry.get_text())
        
        self.get_workstation_data()
        if self.get_workstation_data() is None:
            self.set_workstation_data(WorkstationData())
        self.get_workstation_data().set_name(self.workstationNameEntry.get_text())
        self.get_workstation_data().set_ou(self.getOUComboValue())
  
        
        self.controller.connect()

    def disconnect(self):
        self.logger.debug("disconnect")
        
        if self.get_gecos_access_data() is None:
            self.get_gecos_access_data(GecosAccessData())
        self.get_gecos_access_data().set_url(self.gecosCCurlEntry.get_text())
        self.get_gecos_access_data().set_login(self.gecosCCuserEntry.get_text())
        self.get_gecos_access_data().set_password(self.gecosCCpassEntry.get_text())
        
        self.get_workstation_data()
        if self.get_workstation_data() is None:
            self.set_workstation_data(WorkstationData())
        self.get_workstation_data().set_name(self.workstationNameEntry.get_text())
        self.get_workstation_data().set_ou(self.getOUComboValue())

        
        self.controller.disconnect()

    def patternSearch(self):
        self.logger.debug("patternSearch")
        
        if self.get_gecos_access_data() is None:
            self.set_gecos_access_data(GecosAccessData())
        self.get_gecos_access_data().set_url(self.gecosCCurlEntry.get_text())
        self.get_gecos_access_data().set_login(self.gecosCCuserEntry.get_text())
        self.get_gecos_access_data().set_password(self.gecosCCpassEntry.get_text())
        
        
        res = self.controller.patternSearch(self.searchFilterEntry.get_text())
        if isinstance(res, (list, tuple)):
            for r in res:
                self.selectOUSelection['menu'].add_command(label=r[1], command=tk._setit(self.selectOUVar, r[1]))
            self.selectOUVar.set(res[0][1])
        
    def cancel(self):
        self.logger.debug("cancel")
        self.mainController.backToMainWindowDialog()
    
    '''
    Override of the show method, setting all to the initial state
    '''
    def show(self):
        # set to initial state
        self.initGUIValues(None)
        
        # super method
        super(MainMenuDialog, self).show()