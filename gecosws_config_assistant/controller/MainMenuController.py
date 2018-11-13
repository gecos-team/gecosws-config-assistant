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

__author__ = "Abraham Macias Paredes <amacias@solutia-it.es>" + \
     "Francisco Fuentes Barrera <ffuentes@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"

from gettext import gettext as _
import gettext
from inspect import getmembers
import logging
import os
import sys

from gecosws_config_assistant.controller.ConnectWithGecosCCController import (
    ConnectWithGecosCCController)
from gecosws_config_assistant.controller.LocalUserController import (
    LocalUserController)
from gecosws_config_assistant.controller.RequirementsCheckController import (
    RequirementsCheckController)
from gecosws_config_assistant.controller.SystemStatusController import (
    SystemStatusController)
from gecosws_config_assistant.controller.UserAuthenticationMethodController \
    import UserAuthenticationMethodController
from gecosws_config_assistant.controller.LogTerminalController import (
    LogTerminalController)
from gecosws_config_assistant.view.CommonDialog import (
    showerror_gtk, showinfo_gtk)
from gecosws_config_assistant.view.SplashScreen import SplashScreen
from gecosws_config_assistant.view.MainWindow import MainWindow
from gecosws_config_assistant.util.GtkAptProgress import GtkAptProgress
from gecosws_config_assistant.view.UserAuthDialog import (
    LDAP_USERS, AD_USERS)

gettext.textdomain('gecosws-config-assistant')

class MainMenuController(object):
    '''
    Controller class to show the main menu window.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('MainMenuController')
        self.window = MainWindow(self)
        self.logger.error(self.window)

        # controllers
        self.connectWithGecosCC = ConnectWithGecosCCController(self)
        self.userAuthenticationMethod = UserAuthenticationMethodController(
            self)
        self.localUserList = LocalUserController(self)
        self.systemStatus = SystemStatusController(self)
        self.logController = LogTerminalController(self)
        self.requirementsCheck = RequirementsCheckController(self)

        #keys
        self.networkStatusKey = "networkStatus"
        self.ntpStatusKey = "ntpStatus"
        self.autoconfStatusKey = "autoconf"
        self.gecosStatusKey = "gecos"
        self.usersStatusKey = "users"

        self.window.buildUI()
        self.showRequirementsCheckDialog()

    def show(self):
        ''' Show main window '''

        # Checking updates for GCA
        self.checkForUpdates()

        self.window.show()

    def hide(self):
        ''' Hide main window '''

        self.root.destroy()

    def calculateStatus(self):
        ''' Calculates status of system '''

        ret = {}

        ret[self.networkStatusKey] = 3
        ret[self.ntpStatusKey] = 3
        ret[self.autoconfStatusKey] = 3
        ret[self.gecosStatusKey] = 3
        ret[self.usersStatusKey] = 3

        checkNetwork = self.checkNetwork()
        checkNTP = self.checkNTP()

        self.logger.debug('calculateStatus - network is: %s', checkNetwork)
        self.logger.debug('calculateStatus - NTP is: %s', checkNTP)

        if checkNetwork:
            # Network is green
            ret[self.networkStatusKey] = 1

            if checkNTP:
                # NTP is green
                ret[self.ntpStatusKey] = 1

            if self.checkAutoconf():
                # Auto configuration is green
                ret[self.autoconfStatusKey] = 1
            else:
                # Auto configuration is yellow
                ret[self.autoconfStatusKey] = 2

            if checkNetwork and checkNTP:
                ret[self.gecosStatusKey] = 2
                ret[self.usersStatusKey] = 2

            self.logger.debug(
                'calculateStatus - GECOS is: %s',
                self.checkGECOS())
            if self.checkGECOS():
                ret[self.gecosStatusKey] = 1

            self.logger.debug(
                'calculateStatus - Authentication is: %s',
                self.checkUsers())
            if self.checkUsers():
                ret[self.usersStatusKey] = 1

        return ret

    def calculateMainButtons(self, calculatedStatus):
        ''' Calculates main buttons '''

        ret = {
            'netbutton': True,
            'confbutton': False,
            'userbutton': False,
            'syncbutton': False,
            'sysbutton': False
        }

        if calculatedStatus[self.autoconfStatusKey] != 3:
            ret["confbutton"] = True

        if calculatedStatus[self.ntpStatusKey] != 3:
            ret["syncbutton"] = True

        if calculatedStatus[self.gecosStatusKey] != 3:
            ret["sysbutton" ] = True

        if calculatedStatus[self.usersStatusKey] != 3:
            ret["userbutton"] = True

        return ret

    def calculateTopButtons(self, calculatedStatus):
        ''' Calculates top buttons '''

        buttons = {}

        buttons["linkbutton"] = False \
            if calculatedStatus[self.gecosStatusKey] == 3 \
            else True

        buttons["authbutton"] = False \
            if calculatedStatus[self.autoconfStatusKey] == 3 \
            else True

        return buttons

    def getTexts(self):
        ''' Getting text '''

        self.logger.debug("Calculating texts")
        text = {}

        if self.checkNetwork():
            text[self.networkStatusKey] = \
                _("This workstation has got a network connection configured")
        else:
            text[self.networkStatusKey] = \
                _("This workstation has NO network connection")

        if self.checkAutoconf():
            text[self.autoconfStatusKey] = \
                _("This worstation has loaded setup data values from Control Center")
        else:
            text[self.autoconfStatusKey] = \
                _("This workstation can load setup data values from Control Center")

        if self.checkNTP():
            text[self.ntpStatusKey] = \
                _("This workstation is synchronized with a time server (NTP)")
        else:
            text[self.ntpStatusKey] = \
                _("This workstation is NOT synchronized with a time server (NTP)")

        if self.checkGECOS():
            text[self.gecosStatusKey] = \
                _("This workstation is linked to a Control Center")
        else:
            text[self.gecosStatusKey] = \
                _("This workstation is NOT linked to a Control Center")

        basetext = _("Users authenticate themselves with %s")

        status = self.userAuthenticationMethod.getStatus()

        if status == LDAP_USERS:
            text[self.usersStatusKey]    = _(basetext)%( _("LDAP") )
        elif status == AD_USERS:
            text[self.usersStatusKey]    = _(basetext)%( _("Active Directory"))
        else:
            text[self.usersStatusKey]    =  _(basetext)%( _("Internal"))

        return text

    def checkNetwork(self):
        ''' Checking network '''

        self.logger.debug("Checking network status")
        ret = self.requirementsCheck.getNetworkStatus()
        return ret

    def getNetworkInterfaces(self):
        ''' Checking network interfaces '''
        return self.requirementsCheck.getNetworkInterfaces()

    def checkNTP(self):
        ''' Checking NTP server '''

        self.logger.debug("Checking NTP status")
        ret = self.requirementsCheck.getNTPStatus()
        return ret

    def checkAutoconf(self):
        ''' Checking autoconf '''

        self.logger.debug("Checking Autoconf")
        ret = self.requirementsCheck.getAutoconfStatus()
        return ret

    def checkGECOS(self):
        ''' Checking GECOS '''

        self.logger.debug("Checking GECOS")
        ret = self.connectWithGecosCC.getStatus()
        return ret

    def checkUsers(self):
        ''' Checking users '''

        self.logger.debug("Checking Users")
        ret = self.userAuthenticationMethod.areNotInternal()
        return ret

    # new show methods
    def backToMainWindowDialog(self):
        ''' Restore main window '''

        self.showRequirementsCheckDialog()

    def showRequirementsCheckDialog(self):
        ''' Show requirements '''

        self.requirementsCheck.show(self.window)

        # Check status
        calculatedStatus = self.calculateStatus()
        calculatedButtons = self.calculateTopButtons(calculatedStatus)

        self.window.setStatus(calculatedStatus, calculatedButtons)

    def showConnectWithGecosCCDialog(self):
        ''' Show connection with GEcos Control Center '''

        self.connectWithGecosCC.show(self.window)

    def showUserAuthenticationMethod(self):
        ''' Show user authentication methods '''

        view = self.userAuthenticationMethod.getView(self)
        self.window.gotoUserAuth(view)

    def showSoftwareManager(self):
        ''' Show software manager '''

        self.logger.debug("showSoftwareManager")
        cmd = '/usr/sbin/synaptic'
        os.spawnlp(os.P_NOWAIT, cmd, cmd)

    def showLocalUserListView(self):
        ''' Show local user view '''

        self.localUserList.showList(self.window)

    def checkForUpdates(self):
        ''' Checking for update gecos config assistant '''

        import apt

        apt_progress = GtkAptProgress()
        cache = apt.cache.Cache(apt_progress.open)
        pkg = cache['gecosws-config-assistant'] if cache.has_key('gecosws-config-assistant') else None

        if pkg is not None and pkg.is_installed and pkg.is_upgradable:

            pkg.mark_upgrade()

            splash = SplashScreen()
            hbox2 = splash.getElementById('hbox2')
            hbox2.pack_start(apt_progress, True, True, 0)
            apt_progress.show()
            splash.show()

            button = splash.getElementById('label1')
            button.set_label(_('Upgrading ...'))

            apt_progress.show_terminal(True)

            upgrade = True

            try:
                cache.commit(apt_progress.acquire, apt_progress.install)
            except FetchFailedException, e:
                upgrade = False
                self.logger.debug("Exception happened: %s", e)
                showerror_gtk(
                    _("Unable to connect to software repository"),
                    self.window.getMainWindow())
            except Exception, e:
                upgrade = False
                self.logger.debug("Exception happened: %s", e)
                showerror_gtk(
                    _("An error occurred during the upgrade"),
                    self.window.getMainWindow())

            splash.hide()

            if upgrade:
                showinfo_gtk(
                    _("GECOS Config Assistant has been udpated. Restarting ..."),
                      self.window.getMainWindow())
                args = sys.argv[:]
                os.execvp(sys.executable, [sys.executable] + args)



    def showSystemStatus(self):
        ''' Show system status '''

        self.systemStatus.show()

    def showTerminalWindow(self):
        ''' Show Terminal window '''

        self.logController.show()

    def getNTPController(self):
        ''' Getting NTP controller '''

        return self.requirementsCheck.ntpServer
