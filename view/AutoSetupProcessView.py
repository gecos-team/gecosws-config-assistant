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
from ttk import Frame, Button, Style, Label
import logging


import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class AutoSetupProcessView(Tk):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        Tk.__init__(self, None, None, 'AutoSetupProcessView', 1, 0, None)
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('AutoSetupProcessView')
        
        self.initUI()        

    def initUI(self):
      
        self.title(_('Auto setup process'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Auto setup data load 
        autoSetupDataLoadLabel =  Label(self.body, text=_("Auto setup data load:"))
        autoSetupDataLoadLabel.grid(column=0, row=1, sticky=E+W, padx=padding_x, pady=padding_y)

        self.autoSetupDataLoadStatusLabel =  Label(self.body, text=_("PENDING"))
        self.autoSetupDataLoadStatusLabel.grid(column=1, row=1, sticky=E+W, padx=padding_x, pady=padding_y)


        # NTP server setup
        ntpServerSetupLabel =  Label(self.body, text=_("NTP server setup:"))
        ntpServerSetupLabel.grid(column=0, row=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.ntpServerSetupStatusLabel =  Label(self.body, text=_("PENDING"))
        self.ntpServerSetupStatusLabel.grid(column=1, row=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # User authentication method setup
        userAuthenticationSetupLabel =  Label(self.body, text=_("User authentication method setup:"))
        userAuthenticationSetupLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)

        self.userAuthenticationSetupStatusLabel =  Label(self.body, text=_("PENDING"))
        self.userAuthenticationSetupStatusLabel.grid(column=1, row=3, sticky=E+W, padx=padding_x, pady=padding_y)

        # Accept button
        self.acceptButton = Button(self.body, text=_("Accept"),
            command=self.accept)
        self.acceptButton.grid(column=2, row=5, sticky=E, padx=padding_x, pady=padding_y)
        self.acceptButton.config(state='disabled')
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        self.grab_set()
        self.update()
        


    def accept(self):
        self.logger.debug("accept")
        self.controller.proccess_dialog_accept()
  
    def hide(self):
        self.logger.debug("hide")
        self.destroy()
                
    def setAutoSetupDataLoadStatus(self, status):
        self.autoSetupDataLoadStatusLabel['text'] = status
        self.update()

    def setNTPServerSetupStatus(self, status):
        self.ntpServerSetupStatusLabel['text'] = status
        self.update()

    def setUserAuthenticationSetupStatus(self, status):
        self.userAuthenticationSetupStatusLabel['text'] = status
        self.update()

    def enableAcceptButton(self):
        self.acceptButton.config(state='enabled')
        self.update()
    