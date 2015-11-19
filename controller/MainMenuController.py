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

from controller.RequirementsCheckController import RequirementsCheckController
from controller.ConnectWithGecosCCController import ConnectWithGecosCCController
from controller.UserAuthenticationMethodController import UserAuthenticationMethodController
from controller.LocalUserController import LocalUserController
from controller.SystemStatusController import SystemStatusController
from controller.AutoSetupController import AutoSetupController
from controller.NTPServerController import NTPServerController
from controller.NetworkInterfaceController import NetworkInterfaceController

from view.MainWindow import MainWindow
from view.MainMenuDialog import MainMenuDialog
from view.AutoconfDialog import AutoconfDialog
from view.NetworkSettingsDialog import NetworkSettingsDialog

from view.CommonDialog import showerror_gtk, showinfo_gtk, askyesno_gtk
from util.PackageManager import PackageManager 

import logging
import os, traceback

from inspect import getmembers
from pprint import pprint

import gettext
from gettext import gettext as _
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
        self.currentView = None
        
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
        
        # new pars
        self.mainScreen = MainMenuDialog(self)
        self.mainScreenGUIValues = {}
        self.autoconfDialog = AutoconfDialog(self)
        self.autoconfGUIValues = {}
        self.networkSettingsDialog = NetworkSettingsDialog(self)
        self.networkSettingsGUIValues = {}
        
        self.logger = logging.getLogger('MainMenuController')
        
    def show(self):
        self.window.buildUI()
        self.window.initGUIValues()
        self.window.loadCurrentState(None)
        
        self.currentView = self.mainScreen
        self.currentView.initGUIValues()
        self.currentView.loadCurrentState(None)
        centralMainFrame = self.currentView.getCentralFrame()
        
        self.window.putInCenterFrame(centralMainFrame)
        self.window.show()

    def hide(self):
        self.root.destroy()
    
    # common screen switch method
    def changeScreen(self, dialog):
        centralFrame = dialog.getCentralFrame()
        try:
            self.window.putInCenterFrame(centralFrame)
        except:
            tb = traceback.format_exc()
            self.logger.error(tb)
    
    # navigate thru screens
    def navigate(self, dialog):
        # retrieve values from previous window
        toSaveState = self.currentView.getCurrentState()
        
        if(type(self.currentView) is MainMenuDialog):
            self.mainScreenGUIValues = toSaveState
        elif(type(self.currentView) is AutoconfDialog):
            self.autoconfGUIValues = toSaveState
        elif(type(self.currentView) is NetworkSettingsDialog):
            self.networkSettingsGUIValues = toSaveState
        
        # load previous state
        currentState = {}
        if(type(self.currentView) is MainMenuDialog):
            currentState = self.mainScreenGUIValues
        elif(type(self.currentView) is AutoconfDialog):
            currentState = self.autoconfGUIValues
        elif(type(self.currentView) is NetworkSettingsDialog):
            currentState = self.networkSettingsGUIValues
        
        dialog.loadCurrentState(currentState)
        
        # change widgets
        self.changeScreen(dialog)
        # put a reference to the new window
        self.currentView = dialog
            
    # new show methods
    def showAutoconfDialog(self):
        #instantiate
        self.autoconfDialog = AutoconfDialog(self)
        self.navigate(self.autoconfDialog)
    
    def backToMainWindowDialog(self):
        # restore main window
        self.mainScreen = MainMenuDialog(self)
        self.navigate(self.mainScreen)
    
    def showNetworkSettingsDialog(self):
        # get network settings widgets
        self.networkSettingsDialog = NetworkSettingsDialog(self)
        self.navigate(self.networkSettingsDialog)
    
    def showRequirementsCheckDialog(self):
        self.requirementsCheck.show(self.currentView)

    def showConnectWithGecosCCDialog(self):
        self.connectWithGecosCC.show(self.currentView)

    def showUserAuthenticationMethod(self):
        self.userAuthenticationMethod.show(self.currentView)

    def showSoftwareManager(self):
        self.logger.debug("showSoftwareManager")
        cmd = '/usr/sbin/synaptic'
        os.spawnlp(os.P_NOWAIT, cmd, cmd)

    def showLocalUserListView(self):
        self.localUserList.showList(self.currentView)

    def updateConfigAsystant(self):
        if askyesno_gtk( _("Are you sure you want to update the GECOS Config Assistant?"), self.mainScreen.getMainWindow()):
            pm = PackageManager()
            if not pm.update_cache():
                showerror_gtk( _("An error occurred during the upgrade"), self.mainScreen.getMainWindow())
            else:
                try:
                    if not pm.upgrade_package('gecosws-config-assistant'):
                        showerror_gtk( _("CGA is already at the newest version!"), self.mainScreen.getMainWindow())
                    else:
                        showerror_gtk( _("GECOS Config Assistant has been udpated. Please restart GCA"), self.mainScreen.getMainWindow())
                except:
                    showerror_gtk( _("An error occurred during the upgrade"), self.mainScreen.getMainWindow())
                    
        

    def showSystemStatus(self):
        self.systemStatus.show()


