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

from gecosws_config_assistant.controller.AutoSetupController import AutoSetupController
from gecosws_config_assistant.controller.NTPServerController import NTPServerController
from gecosws_config_assistant.controller.NetworkInterfaceController import NetworkInterfaceController

from gecosws_config_assistant.view.RequirementsCheckDialog import RequirementsCheckDialog

from gecosws_config_assistant.dao.NetworkInterfaceDAO import NetworkInterfaceDAO
from gecosws_config_assistant.dao.NTPServerDAO import NTPServerDAO
from gecosws_config_assistant.dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO
from gecosws_config_assistant.dto.LocalUsersAuthMethod import LocalUsersAuthMethod 

import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class RequirementsCheckController(object):
    '''
    Controller class for the requirements check functionality.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        self.view = None
        self.mainWindowController = mainController 
        self.ntpServer = NTPServerController(self.mainWindowController)
        self.networkInterface = NetworkInterfaceController(self.mainWindowController)
        self.autoSetup = AutoSetupController(self.mainWindowController)
        self.logger = logging.getLogger('RequirementsCheckController')
        
        #self.window = MainWindow.getInstance(None)
    
    def getNetworkStatus(self):
        self.logger.debug('Check network interfaces')
        ret = False
        networkInterfacesDao = NetworkInterfaceDAO()
        interfaces = networkInterfacesDao.loadAll()
        if interfaces is not None:
            for ni in interfaces:
                if ni.get_name() != 'lo':
                    self.logger.debug('Network interfaces OK')
                    ret = True
        return ret
    
    def getNetworkInterfaces(self):
        networkInterfacesDao = NetworkInterfaceDAO()
        interfaces = networkInterfacesDao.loadAll()
        return interfaces
    
    def getNTPStatus(self):
        self.logger.debug('Check NTP server')
        ret = False
        ntpServerDao = NTPServerDAO()
        if ntpServerDao.load() is not None:
            self.logger.debug('NTP Server OK')
            ret = True
        
        return ret
    
    def getAutoconfStatus(self):
        self.logger.debug('Check auto setup status')
        ret = self.autoSetup.get_conf()
        return ret
    
    def show(self, mainWindow):
        self.logger.debug('show - BEGIN')
        self.view = RequirementsCheckDialog(mainWindow, self)

        self.view.show()   
        self.logger.debug('show - END')

    def hide(self):
        self.view.quit()
    
    def showNetworkInterfaces(self):
        self.networkInterface.show(self.view.parent)

    def showAutoSetup(self):
        self.autoSetup.show(self.view.parent)

    def showNTPServer(self):
        self.ntpServer.show(self.view.parent)

