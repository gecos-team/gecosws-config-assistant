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

from controller.RequirementsCheckController import RequirementsCheckController
from controller.ConnectWithGecosCCController import ConnectWithGecosCCController
from controller.UserAuthenticationMethodController import UserAuthenticationMethodController
from controller.LocalUserController import LocalUserController
from controller.SystemStatusController import SystemStatusController

from view.MainMenuDialog import MainMenuDialog

import logging
import traceback

from Tkinter import Tk
import tkMessageBox

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
        self.view = None
        self.requirementsCheck = RequirementsCheckController()
        self.connectWithGecosCC = ConnectWithGecosCCController()
        self.userAuthenticationMethod = UserAuthenticationMethodController()
        self.localUserList = LocalUserController()
        self.systemStatus = SystemStatusController()
        
        self.logger = logging.getLogger('MainMenuController')
        self.logger.setLevel(logging.DEBUG)
        

    def on_closing(self):
        if tkMessageBox.askokcancel(_("Quit"), _("Do you want to quit?")):
            self.root.destroy()

    def show(self):
        self.root = Tk()
        #root.geometry("800x400")
        self.view = MainMenuDialog(self.root)
        self.view.set_controller(self)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()          

        pass


    def hide(self):
        self.root.destroy()
    
    def showRequirementsCheckDialog(self):
        # TODO!
        pass

    def showConnectWithGecosCCDialog(self):
        # TODO!
        pass

    def showUserAuthenticationMethod(self):
        # TODO!
        pass

    def showSoftwareManager(self):
        # TODO!
        pass

    def showLocalUserListView(self):
        # TODO!
        pass

    def updateConfigAsystant(self):
        # TODO!
        pass

    def showSystemStatus(self):
        # TODO!
        pass


