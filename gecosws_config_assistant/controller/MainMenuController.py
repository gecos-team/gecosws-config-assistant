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

from gecosws_config_assistant.controller.AutoSetupController import AutoSetupController
from gecosws_config_assistant.controller.ConnectWithGecosCCController import ConnectWithGecosCCController
from gecosws_config_assistant.controller.LocalUserController import LocalUserController
from gecosws_config_assistant.controller.NTPServerController import NTPServerController
from gecosws_config_assistant.controller.NetworkInterfaceController import NetworkInterfaceController
from gecosws_config_assistant.controller.RequirementsCheckController import RequirementsCheckController
from gecosws_config_assistant.controller.SystemStatusController import SystemStatusController
from gecosws_config_assistant.controller.UserAuthenticationMethodController import UserAuthenticationMethodController
from gecosws_config_assistant.util.PackageManager import PackageManager 
from gecosws_config_assistant.view.AutoconfDialog import AutoconfDialog
from gecosws_config_assistant.view.CommonDialog import showerror_gtk, showinfo_gtk, askyesno_gtk
from gecosws_config_assistant.view.MainWindow import MainWindow
from gecosws_config_assistant.view.UserAuthDialog import UserAuthDialog, LOCAL_USERS, LDAP_USERS, AD_USERS

gettext.textdomain('gecosws-config-assistant')

class MainMenuController(object):
    '''
    Controller class to show the main menu window.
    '''
    
#     _singleton = None
#     
#     @classmethod
#     def getInstance(cls):
#         if not isinstance(cls._singleton,cls):
#             cls._singleton = cls()
#         return cls._singleton

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('MainMenuController')
        self.window = MainWindow(self)
        self.logger.error(self.window)
        
        # controllers
        self.connectWithGecosCC = ConnectWithGecosCCController()
        self.userAuthenticationMethod = UserAuthenticationMethodController()
        self.localUserList = LocalUserController()
        self.systemStatus = SystemStatusController()
        self.requirementsCheck = RequirementsCheckController()
        
        #keys
        self.networkStatusKey = "networkStatus"
        self.ntpStatusKey = "ntpStatus"
        self.autoconfStatusKey = "autoconf"
        self.gecosStatusKey = "gecos"
        self.usersStatusKey = "users"
    def show(self):
        
        calculatedStatus = self.calculateStatus()
        calculatedButtons = self.calculateTopButtons(calculatedStatus)
        
        self.window.buildUI()
        self.window.initGUIValues()
        self.window.loadCurrentState(calculatedStatus, calculatedButtons)
        
        self.window.initFrame(calculatedStatus)
        
        self.window.show()

    def hide(self):
        self.root.destroy()
    
    def calculateStatus(self):
        ret = {}
        
        ret[self.networkStatusKey] = 3
        ret[self.ntpStatusKey] = 3
        ret[self.autoconfStatusKey] = 3 
        ret[self.gecosStatusKey] = 3
        ret[self.usersStatusKey] = 3
        
        checkNetwork = self.checkNetwork()
        checkNTP = self.checkNTP()
        
        if(checkNetwork):
            ret[self.networkStatusKey] = 1
            if(checkNTP):
                ret[self.ntpStatusKey] = 1
            if(self.checkAutoconf()):
                ret[self.autoconfStatusKey] = 1
            
            if(checkNetwork and checkNTP):
                ret[self.gecosStatusKey] = 2
                ret[self.usersStatusKey] = 2
            
            if(self.checkGECOS()):
                ret[self.gecosStatusKey] = 1
            
            if(self.checkUsers()):
                ret[self.usersStatusKey] = 1
        
        return ret
    
    def calculateMainButtons(self, calculatedStatus):
        ret = {}
        
        ret["netbutton" ] = True
        ret["confbutton"] = False
        ret["syncbutton"] = False 
        ret["sysbutton" ] = False
        ret["userbutton"] = False
        
        if(calculatedStatus[self.ntpStatusKey] != 3):
            ret["confbutton"] = True
        
        if(calculatedStatus[self.autoconfStatusKey] != 3):
            ret["syncbutton"] = True
        
        if(calculatedStatus[self.gecosStatusKey] != 3):
            ret["sysbutton" ] = True
        
        if(calculatedStatus[self.usersStatusKey] != 3):
            ret["userbutton"] = True
        
        return ret
    
    def calculateTopButtons(self, calculatedStatus):
        buttons = {}
        
        if(calculatedStatus[self.gecosStatusKey] != 3): 
            buttons["linkbutton"]= True
        else:
            buttons["linkbutton"]= False
            
        if(calculatedStatus[self.autoconfStatusKey] != 3):
            buttons["authbutton"]= True
        else:
            buttons["authbutton"]= False
        
        return buttons
    
    def getTexts(self):
        self.logger.debug("Calculating texts")
        text = {}
        
        if(self.checkNetwork()):
            text[self.networkStatusKey]  = _("El sistema tiene conexión a Red (Datos de conexión)")
        else:
            text[self.networkStatusKey]  = _("El sistema NO tiene conexión a Red")
        
        text[self.autoconfStatusKey]     = _("Puede autoconfigurar el sistema con los valores predeterminados")
            
        if(self.checkNTP()):
            text[self.ntpStatusKey]      = _("El sistema está sincronizado con un servidor NTP")
        else:
            text[self.ntpStatusKey]      = _("El sistema NO está sincronizado con un servidor NTP")
        
        if(self.checkGECOS()):
            text[self.gecosStatusKey]    = _("El sistema está vinculado a GECOS")
        else:
            text[self.gecosStatusKey]    = _("El sistema NO está vinculado a GECOS")
        
        basetext = "Los usuarios se autentican por el método "
        
        status = self.userAuthenticationMethod.getStatus()
        
        if(status == LDAP_USERS):
            text[self.usersStatusKey]    = _(basetext+"LDAP")
        elif(status == AD_USERS):
            text[self.usersStatusKey]    = _(basetext+"Active Directory")
        else:
            text[self.usersStatusKey]    = _(basetext+"INTERNO")
        
        return text
    
    def checkNetwork(self):
        self.logger.debug("Checking network status")
        ret = self.requirementsCheck.getNetworkStatus()
        return ret
    
    def getNetworkInterfaces(self):
        return self.requirementsCheck.getNetworkInterfaces()
    
    def checkNTP(self):
        self.logger.debug("Checking NTP status")
        ret = self.requirementsCheck.getNTPStatus()
        return ret
    
    def checkAutoconf(self):
        self.logger.debug("Checking Autoconf")
        ret = self.requirementsCheck.getAutoconfStatus()
        return ret
    
    def checkGECOS(self):
        self.logger.debug("Checking GECOS")
        ret = self.connectWithGecosCC.getStatus()
        return ret
    
    def checkUsers(self):
        self.logger.debug("Checking Users")
        ret = self.userAuthenticationMethod.areNotInternal()
        return ret
    
    # new show methods
    def showAutoconfDialog(self):
        view = self.requirementsCheck.autoSetup.getView(self)
        self.window.gotoAutoconf(view)
    
    def backToMainWindowDialog(self):
        # restore main window
        self.window.gotoMainWindow()
    
    def showNetworkSettingsDialog(self):
        # get network settings widgets
        view = self.requirementsCheck.networkInterface.getView(self)
        self.window.gotoNetworkSettings(view)
    
    def showNTPSettingsDialog(self):
        view = self.requirementsCheck.ntpServer.getView(self)
        self.window.gotoNTPSettings(view)
    
    def showRequirementsCheckDialog(self):
        self.requirementsCheck.show(self.window.currentView)

    def showConnectWithGecosCCDialog(self):
        view = self.connectWithGecosCC.getView(self)
        self.window.gotoConnectoWithGECOS(view)

    def showUserAuthenticationMethod(self):
        view = self.userAuthenticationMethod.getView(self)
        self.window.gotoUserAuth(view)

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


    def getNTPController(self):
        return self.requirementsCheck.ntpServer