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

from Tkinter import N, S, W, E, Tk
from ttk import Frame, Button, Style
import tkMessageBox
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class MainMenuDialog(Tk):
    '''
    Dialog class that shows the main menu.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        Tk.__init__(self, None, None, 'MainMenuDialog', 1, 0, None)
        self.body = Frame(self, padding="20 20 20 20")    
        self.controller = mainController
        self.logger = logging.getLogger('MainMenuDialog')
        
        self.initUI()        

    def initUI(self):
      
        self.title(_('Gecos config assistant'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10
        
        requirementsCheckButton = Button(self.body, text=_("Check setup requirements"),
            command=self.showRequirementsCheckDialog)
        requirementsCheckButton.grid(column=1, row=1, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        connectWithGecosCCButton = Button(self.body, text=_("Connect / disconnect to GECOS Control Center"),
            command=self.showConnectWithGecosCCDialog)
        connectWithGecosCCButton.grid(column=1, row=2, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        userAuthenticationMethodButton = Button(self.body, text=_("Setup user authentication method"),
            command=self.showUserAuthenticationMethod)
        userAuthenticationMethodButton.grid(column=1, row=3, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        softwareManagerButton = Button(self.body, text=_("Software manager"),
            command=self.showSoftwareManager)
        softwareManagerButton.grid(column=1, row=4, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        localUserManagerButton = Button(self.body, text=_("Local user manager"),
            command=self.showLocalUserListView)
        localUserManagerButton.grid(column=1, row=5, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        updateAssistantButton = Button(self.body, text=_("Update this assistant"),
            command=self.updateConfigAssistant)
        updateAssistantButton.grid(column=1, row=6, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        
        statusButton = Button(self.body, text=_("View status"),
            command=self.showSystemStatus)
        statusButton.grid(column=1, row=7, sticky=W, padx=padding_x, pady=padding_y)

        closeButton = Button(self.body, text=_("Close"),
            command=self.close)
        closeButton.grid(column=3, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.mainloop()           

    def close(self):
        self.logger.debug("Close")
        if tkMessageBox.askokcancel(_("Quit"), _("Do you want to quit?")):
            self.body.quit()


    def showRequirementsCheckDialog(self):
        self.logger.debug("showRequirementsCheckDialog")
        self.controller.showRequirementsCheckDialog()

    def showConnectWithGecosCCDialog(self):
        self.logger.debug("showConnectWithGecosCCDialog")
        self.controller.showConnectWithGecosCCDialog()

    def showUserAuthenticationMethod(self):
        self.logger.debug("showUserAuthenticationMethod")
        self.controller.showUserAuthenticationMethod()
        
        
    def showSoftwareManager(self):
        self.logger.debug("showSoftwareManager")
        
    def showLocalUserListView(self):
        self.logger.debug("showLocalUserListView")
        
    def updateConfigAssistant(self):
        self.logger.debug("updateConfigAssistant")
        
    def showSystemStatus(self):
        self.logger.debug("showSystemStatus")
        
    