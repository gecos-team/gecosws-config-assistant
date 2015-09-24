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

from Tkinter import N, S, W, E, Toplevel
from ttk import Frame, Button, Style, Label
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class RequirementsCheckDialog(Toplevel):
    '''
    Dialog class that shows the "requirements check" menu.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('RequirementsCheckDialog')
        self.logger.setLevel(logging.DEBUG)
        
        self.initUI()        


    def initUI(self):
      
        self.title(_('Check basic setup requirements'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Network interfaces        
        networkInterfacesLabel =  Label(self.body, text=_("The system is connected to a network"))
        networkInterfacesLabel.grid(column=1, row=1, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.networkInterfacesStatusLabel =  Label(self.body, text=_("PENDING"))
        self.networkInterfacesStatusLabel.grid(column=2, row=1, sticky=E+W, padx=padding_x, pady=padding_y)

        networkInterfacesButton = Button(self.body, text=_("Setup"),
            command=self.showNetworkInterfaces)
        networkInterfacesButton.grid(column=3, row=1, sticky=E+W, padx=padding_x, pady=padding_y)


        # Auto setup        
        autoSetupLabel =  Label(self.body, text=_("The system has obtained automatic setup parameters from a Gecos server"))
        autoSetupLabel.grid(column=1, row=2, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.autoSetupStatusLabel =  Label(self.body, text=_("PENDING"))
        self.autoSetupStatusLabel.grid(column=2, row=2, sticky=E+W, padx=padding_x, pady=padding_y)

        autoSetupButton = Button(self.body, text=_("Setup"),
            command=self.showAutoSetup)
        autoSetupButton.grid(column=3, row=2, sticky=E+W, padx=padding_x, pady=padding_y)


        # NTP Server        
        ntpServerLabel =  Label(self.body, text=_("The system has synchronized the time with a NTP server"))
        ntpServerLabel.grid(column=1, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.ntpServerStatusLabel =  Label(self.body, text=_("PENDING"))
        self.ntpServerStatusLabel.grid(column=2, row=3, sticky=E+W, padx=padding_x, pady=padding_y)

        ntpServerButton = Button(self.body, text=_("Setup"),
            command=self.showNTPServer)
        ntpServerButton.grid(column=3, row=3, sticky=E+W, padx=padding_x, pady=padding_y)

        closeButton = Button(self.body, text=_("Accept"),
            command=self.close)
        closeButton.grid(column=3, row=4, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def close(self):
        self.logger.debug("Close")
        self.destroy()


    def showNetworkInterfaces(self):
        self.logger.debug("showNetworkInterfaces")
        self.controller.showNetworkInterfaces()

    def showAutoSetup(self):
        self.logger.debug("showAutoSetup")
        self.controller.showAutoSetup()

    def showNTPServer(self):
        self.logger.debug("showNTPServer")
        self.controller.showNTPServer()

    def setAutoSetupStatus(self, status):
        self.autoSetupStatusLabel['text'] = status
        
    def setNetworkInterfacesStatus(self, status):
        self.networkInterfacesStatusLabel['text'] = status

    def setNTPServerStatusLabel(self, status):
        self.ntpServerStatusLabel['text'] = status
        