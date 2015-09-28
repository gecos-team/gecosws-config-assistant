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

class GecosCCSetupProcessView(Toplevel):
    '''
    Dialog class that shows the process of GECOS CC connection/disconnection.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('GecosCCSetupProcessView')
        
        self.initUI()        

    def initUI(self):
      
        self.title(_('GECOS CC connection process'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Checking GECOS credentials
        gecosCredentialsLabel =  Label(self.body, text=_("Check GECOS credentials"))
        gecosCredentialsLabel.grid(column=0, row=1, sticky=E+W, padx=padding_x, pady=padding_y)

        self.gecosCredentialsStatusLabel =  Label(self.body, text=_("PENDING"))
        self.gecosCredentialsStatusLabel.grid(column=1, row=1, sticky=E+W, padx=padding_x, pady=padding_y)
        
        # Checking workstation data
        workstationDataLabel =  Label(self.body, text=_("Check workstation data"))
        workstationDataLabel.grid(column=0, row=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.workstationDataStatusLabel =  Label(self.body, text=_("PENDING"))
        self.workstationDataStatusLabel.grid(column=1, row=2, sticky=E+W, padx=padding_x, pady=padding_y)
        
        # Obtaining Chef validation certificate
        chefCertificateLabel =  Label(self.body, text=_("Get chef certificate"))
        chefCertificateLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)

        self.chefCertificateStatusLabel =  Label(self.body, text=_("PENDING"))
        self.chefCertificateStatusLabel.grid(column=1, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        # Linking/unlinking to Chef server
        self.linkToChefLabel =  Label(self.body, text=_("Link to Chef"))
        self.linkToChefLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)

        self.linkToChefStatusLabel =  Label(self.body, text=_("PENDING"))
        self.linkToChefStatusLabel.grid(column=1, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
        
        # Registering computer in GECOS CC
        self.registerInGecosLabel =  Label(self.body, text=_("Register in GECOS"))
        self.registerInGecosLabel.grid(column=0, row=5, sticky=E+W, padx=padding_x, pady=padding_y)

        self.registerInGecosStatusLabel =  Label(self.body, text=_("PENDING"))
        self.registerInGecosStatusLabel.grid(column=1, row=5, sticky=E+W, padx=padding_x, pady=padding_y)
        
        # Removing old configuration files
        cleanLabel =  Label(self.body, text=_("Clean setup data"))
        cleanLabel.grid(column=0, row=6, sticky=E+W, padx=padding_x, pady=padding_y)

        self.cleanStatusLabel =  Label(self.body, text=_("PENDING"))
        self.cleanStatusLabel.grid(column=1, row=6, sticky=E+W, padx=padding_x, pady=padding_y)
         



        # Accept button
        self.acceptButton = Button(self.body, text=_("Accept"),
            command=self.accept)
        self.acceptButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)
        self.acceptButton.config(state='disabled')
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        self.transient(self.parent)
        self.grab_set()
        self.update()
        


    def accept(self):
        self.logger.debug("accept")
        self.controller.proccess_dialog_accept()
  
    def hide(self):
        self.logger.debug("hide")
        self.destroy()
                
    def setCheckGecosCredentialsStatus(self, status):
        self.gecosCredentialsStatusLabel['text'] = status
        self.update()

    def setCheckWorkstationDataStatus(self, status):
        self.workstationDataStatusLabel['text'] = status
        self.update()

    def setChefCertificateRetrievalStatus(self, status):
        self.chefCertificateStatusLabel['text'] = status
        self.update()

    def setLinkToChefLabel(self, text):
        self.linkToChefLabel['text'] = text
        self.update()
        
    def setLinkToChefStatus(self, status):
        self.linkToChefStatusLabel['text'] = status
        self.update()
        
    def setRegisterInGecosLabel(self, text):
        self.registerInGecosLabel['text'] = text
        self.update()
        
        
    def setRegisterInGecosStatus(self, status):
        self.registerInGecosStatusLabel['text'] = status
        self.update()
        
    def setCleanStatus(self, status):
        self.cleanStatusLabel['text'] = status
        self.update()
        
        
    def enableAcceptButton(self):
        self.acceptButton.config(state='enabled')
        self.update()
    