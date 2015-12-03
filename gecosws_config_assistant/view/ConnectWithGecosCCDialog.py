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

__author__ = "Abraham Macias Paredes <amacias@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from GladeWindow import GladeWindow
from gi.repository import Gtk, Gdk
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.dto.WorkstationData import WorkstationData

class ConnectWithGecosCCDialog(GladeWindow):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('ConnectWithGecosCCDialog')
        self.gladepath = 'gecoscon.glade'
        
        self.gecos_access_data = None
        self.workstation_data = None
        
        self.initUI()        

    def get_gecos_access_data(self):
        return self.__gecos_access_data


    def get_workstation_data(self):
        return self.__workstation_data


    def set_gecos_access_data(self, value):
        self.__gecos_access_data = value


    def set_workstation_data(self, value):
        self.__workstation_data = value


    def initUI(self):
        self.buildUI(self.gladepath)
        
        #combo stuff
        self.lastComboValue = ''
        self.store = self.getElementById('liststore1')
        self.combo = self.getElementById('combobox1')
        
        renderer_text = Gtk.CellRendererText()
        self.combo.pack_start(renderer_text, True)
        self.combo.add_attribute(renderer_text, "text", 0)
        
        self.extractGUIElements()        
        self.logger.debug('UI initiated')
        
    def extractGUIElements(self):
        self.disconnectButton = self.getElementById("button2")
        self.connectButton = self.getElementById("button3")
        
        self.workstationNameEntry = self.getElementById('workstation_entry')
        self.gecosCCurlEntry = self.getElementById('url_entry')
        self.gecosCCuserEntry = self.getElementById('login_entry')
        self.gecosCCpassEntry = self.getElementById('password_entry')
        
        self.selectOUVar = self.getElementById("combobox1")
        self.searchFilterEntry = self.getElementById("entry5")        
        
    def addHandlers(self):
        self.handlers = self.parent.get_common_handlers()
        
        # add new handlers here
        self.logger.debug("Adding search handler")
        self.handlers["onSrch"] = self.patternSearch
        self.logger.debug("Adding connection handler")
        self.handlers["onConn"] = self.connect
        self.logger.debug("Adding accept handler")
        self.handlers["onAcpt"] = self.cancel
        self.logger.debug("Adding disconnect handler")
        self.handlers["onDcon"] = self.disconnect
        self.logger.debug("Adding on change combobox handler")
        self.handlers["onChng"] = self.onChangeComboBox      

    def show(self):
        self.logger.debug("Show")
        
        workstation_data = self.get_workstation_data()
        if workstation_data is not None:
            if (workstation_data.get_name() is not None
                and workstation_data.get_name().strip() != ''):
                self.workstationNameEntry.set_text(workstation_data.get_name())

        gecos_data = self.get_gecos_access_data()
        if gecos_data is not None:
            if (gecos_data.get_url() is not None
                and gecos_data.get_url().strip() != ''):
                self.gecosCCurlEntry.set_text(gecos_data.get_url())

            if (gecos_data.get_login() is not None
                and gecos_data.get_login().strip() != ''):
                self.gecosCCuserEntry.set_text(gecos_data.get_login())
            
            if (gecos_data.get_password() is not None
                and gecos_data.get_password().strip() != ''):
                self.gecosCCpassEntry.set_text(gecos_data.get_password())
        
        self.parent.navigate(self)

    def connect(self, *args):
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

    def disconnect(self, *args):
        self.logger.debug("disconnect")
        
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

        
        self.controller.disconnect()
        
    def onChangeComboBox(self, combo):
        self.logger.debug("This should show up each time the combobox is changed")
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            value = model[tree_iter][0]
            self.lastComboValue = value
        
        
    def getOUComboValue(self):
        return self.lastComboValue
    
    def loadOUCombo(self, values):
        if isinstance(values, (list, tuple)):
            for value in values:
                self.store.append([value[1]])        

    def patternSearch(self, *args):
        self.logger.debug("patternSearch")
        
        if self.get_gecos_access_data() is None:
            self.set_gecos_access_data(GecosAccessData())
        self.get_gecos_access_data().set_url(self.gecosCCurlEntry.get_text())
        self.get_gecos_access_data().set_login(self.gecosCCuserEntry.get_text())
        self.get_gecos_access_data().set_password(self.gecosCCpassEntry.get_text())
        
       
        res = self.controller.patternSearch(self.searchFilterEntry.get_text())
        self.loadOUCombo(res)
        
    def cancel(self, *args):
        self.logger.debug("cancel")
        self.controller.hide()
                
    def focusUrlField(self):
        self.gecosCCurlEntry.grab_focus()                

    def focusUsernameField(self):
        self.gecosCCuserEntry.grab_focus()                

    def focusPasswordField(self):
        self.gecosCCpassEntry.grab_focus()   
        
    def focusSeachFilterField(self):
        self.searchFilterEntry.grab_focus()   
              
    def focusWorkstationNameField(self):
        self.workstationNameEntry.grab_focus()   
                 
    gecos_access_data = property(get_gecos_access_data, set_gecos_access_data, None, None)
    workstation_data = property(get_workstation_data, set_workstation_data, None, None)
                



        
