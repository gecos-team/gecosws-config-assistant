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

__author__ = "Abraham Macias Paredes <amacias@solutia-it.es> Francisco Fuentes Barrera <ffuentes@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from gettext import gettext as _
import gettext
from inspect import getmembers
import logging
import os, traceback
from pprint import pprint

from controller.AutoSetupController import AutoSetupController
from controller.ConnectWithGecosCCController import ConnectWithGecosCCController
from controller.LocalUserController import LocalUserController
from controller.NTPServerController import NTPServerController
from controller.NetworkInterfaceController import NetworkInterfaceController
from controller.RequirementsCheckController import RequirementsCheckController
from controller.SystemStatusController import SystemStatusController
from controller.UserAuthenticationMethodController import UserAuthenticationMethodController
from util.PackageManager import PackageManager 
from view.AutoconfDialog import AutoconfDialog
from view.CommonDialog import showerror_gtk, showinfo_gtk, askyesno_gtk
from view.MainWindow import MainWindow

gettext.textdomain('gecosws-config-assistant')

class MainMenuController(object):
    '''
    Controller class to show the main menu window.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.window = MainWindow(self)
        
        # controllers
        self.connectWithGecosCC = ConnectWithGecosCCController()
        self.userAuthenticationMethod = UserAuthenticationMethodController()
        self.localUserList = LocalUserController()
        self.systemStatus = SystemStatusController()
        self.networkInterface = NetworkInterfaceController()
        self.ntpServer = NTPServerController()
        self.autoSetup = AutoSetupController()
        # almost deprecated
        self.requirementsCheck = RequirementsCheckController()
        
        self.logger = logging.getLogger('MainMenuController')
        
    def show(self):
        self.window.buildUI()
        self.window.initGUIValues()
        self.window.loadCurrentState(None)
        
        self.window.initFrame()
        
        self.window.show()

    def hide(self):
        self.root.destroy()
            
    # new show methods
    def showAutoconfDialog(self):
        self.window.gotoAutoconf()
    
    def backToMainWindowDialog(self):
        # restore main window
        self.window.gotoMainWindow()
    
    def showNetworkSettingsDialog(self):
        # get network settings widgets
        self.window.gotoSettings()
    
    def showRequirementsCheckDialog(self):
        self.requirementsCheck.show(self.window.currentView)

    def showConnectWithGecosCCDialog(self):
        self.connectWithGecosCC.show(self.window.currentView)

    def showUserAuthenticationMethod(self):
        self.userAuthenticationMethod.show(self.window.currentView)

    def showSoftwareManager(self):
        self.logger.debug("showSoftwareManager")
        cmd = '/usr/sbin/synaptic'
        os.spawnlp(os.P_NOWAIT, cmd, cmd)

    def showLocalUserListView(self):
        self.localUserList.showList(self.window.currentView)

    def updateConfigAsystant(self):
        if askyesno_gtk( _("Are you sure you want to update the GECOS Config Assistant?"), self.window.getMainWindow()):
            pm = PackageManager()
            if not pm.update_cache():
                showerror_gtk( _("An error occurred during the upgrade"), self.window.getMainWindow())
            else:
                try:
                    if not pm.upgrade_package('gecosws-config-assistant'):
                        showerror_gtk( _("CGA is already at the newest version!"), self.window.getMainWindow())
                    else:
                        showerror_gtk( _("GECOS Config Assistant has been udpated. Please restart GCA"), self.window.getMainWindow())
                except:
                    showerror_gtk( _("An error occurred during the upgrade"), self.window.getMainWindow())
                    
        

    def showSystemStatus(self):
        self.systemStatus.show()


