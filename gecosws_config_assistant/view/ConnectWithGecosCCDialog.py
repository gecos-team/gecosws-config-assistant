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

from Tkinter import N, S, W, E, Toplevel, END, StringVar
from ttk import Frame, Button, Style, Label, Entry, LabelFrame, OptionMenu
import Tkinter as tk
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.dto.WorkstationData import WorkstationData

class ConnectWithGecosCCDialog(Toplevel):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('ConnectWithGecosCCDialog')
        
        self.gecos_access_data = None
        self.workstation_data = None
        
        self.initUI()        

    def get_gecos_access_data(self):
        return self.__gecos_access_data


    def get_workstation_data(self):
        return self.__workstation_data


    def set_gecos_access_data(self, value):
        self.__gecos_access_data = value


    def set_workstation_data(self, value):
        self.__workstation_data = value




    def initUI(self):
      
        self.title(_('Connect with GECOS Control Center'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10
        
        
        # Workstation name frame
        workstationFrame = LabelFrame(self.body)
        workstationFrame.grid(column=0, row=1, columnspan=3, sticky="nswe", padx=padding_x, pady=padding_y)        
        workstationFrame['text'] = _('Workstation name')
        

        # Explanation
        explanationLabel1 =  Label(workstationFrame, 
            text=_("Workstation name must be unique. Spaces and symbols may be used."))
        explanationLabel1.grid(column=0, row=1, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(workstationFrame, 
            text=_("This description apperars in the GECOS control center reports."))
        explanationLabel2.grid(column=0, row=2, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        # Workstation name field
        workstationNameLabel = Label(workstationFrame, text=_("Workstation name:"))
        workstationNameLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.workstationNameEntry = Entry(workstationFrame)
        self.workstationNameEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.workstationNameEntry.delete(0, END)



        # GECOS CC connection credentials
        gecosCCCredentialsFrame = LabelFrame(self.body)
        gecosCCCredentialsFrame.grid(column=0, row=2, columnspan=3, sticky="nswe", padx=padding_x, pady=padding_y)        
        gecosCCCredentialsFrame['text'] = _('GECOS Control Center Connection parameters')


        # Gecos CC URL
        gecosCCurlLabel = Label(gecosCCCredentialsFrame, text=_("GECOS Control Center URL:"))
        gecosCCurlLabel.grid(column=0, row=1, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.gecosCCurlEntry = Entry(gecosCCCredentialsFrame)
        self.gecosCCurlEntry.grid(column=1, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.gecosCCurlEntry.delete(0, END)
        self.gecosCCurlEntry.insert(0, "http://your.gecos.server.url")

        # Gecos CC user
        gecosCCuserLabel = Label(gecosCCCredentialsFrame, text=_("User:"))
        gecosCCuserLabel.grid(column=0, row=2, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.gecosCCuserEntry = Entry(gecosCCCredentialsFrame)
        self.gecosCCuserEntry.grid(column=1, row=2, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.gecosCCuserEntry.delete(0, END)
        self.gecosCCuserEntry.insert(0, "<gecos_administrator_username>")

        # Gecos CC password
        gecosCCpassLabel = Label(gecosCCCredentialsFrame, text=_("Password:"))
        gecosCCpassLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.gecosCCpassEntry = Entry(gecosCCCredentialsFrame, show="*")
        self.gecosCCpassEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.gecosCCpassEntry.delete(0, END)
        
        

        # OU selecction
        ouSelectionFrame = LabelFrame(self.body)
        ouSelectionFrame.grid(column=0, row=3, columnspan=3, sticky="nswe", padx=padding_x, pady=padding_y)        
        ouSelectionFrame['text'] = _('Select OU to connect to GECOS Control Center')


        # Search filter
        searchFilterLabel = Label(ouSelectionFrame, text=_("Search filter:"))
        searchFilterLabel.grid(column=0, row=1, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.searchFilterEntry = Entry(ouSelectionFrame)
        self.searchFilterEntry.grid(column=1, row=1, sticky=E+W, padx=padding_x, pady=padding_y)

        self.searchFilterEntry.delete(0, END)

        self.searchButton = Button(ouSelectionFrame, text=_("Search"),
            command=self.patternSearch)
        self.searchButton.grid(column=3, row=1, sticky=E, padx=padding_x, pady=padding_y)

        # Select OU
        selectOULabel = Label(ouSelectionFrame, text=_("Select OU:"))
        selectOULabel.grid(column=0, row=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.selectOUVar = StringVar(self.body)
        
        self.selectOUSelection = OptionMenu(ouSelectionFrame, self.selectOUVar)
        self.selectOUSelection.grid(column=1, row=2, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)



        
         
        # Connect/disconnect to Gecos CC
        self.connectButton = Button(self.body, text=_("Connect to GECOS CC"),
            command=self.connect)
        self.connectButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Cancel button
        acceptButton = Button(self.body, text=_("Accept"),
            command=self.cancel)
        acceptButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        workstation_data = self.get_workstation_data()
        if workstation_data is not None:
            if (workstation_data.get_name() is not None
                and workstation_data.get_name().strip() != ''):
                self.workstationNameEntry.delete(0, END)
                self.workstationNameEntry.insert(0, workstation_data.get_name())

        gecos_data = self.get_gecos_access_data()
        if gecos_data is not None:
            self.connectButton['text'] = _("Disconnect from GECOS CC")
            self.connectButton['command'] = self.disconnect
            
            if (gecos_data.get_url() is not None
                and gecos_data.get_url().strip() != ''):
                self.gecosCCurlEntry.delete(0, END)
                self.gecosCCurlEntry.insert(0, gecos_data.get_url())

            if (gecos_data.get_login() is not None
                and gecos_data.get_login().strip() != ''):
                self.gecosCCuserEntry.delete(0, END)
                self.gecosCCuserEntry.insert(0, gecos_data.get_login())
            
            if (gecos_data.get_password() is not None
                and gecos_data.get_password().strip() != ''):
                self.gecosCCpassEntry.delete(0, END)
                self.gecosCCpassEntry.insert(0, gecos_data.get_password())
            
        else:
            self.connectButton['text'] = _("Connect to GECOS CC")
            self.connectButton['command'] = self.connect
            

        
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def connect(self):
        self.logger.debug("connect")
        
        if self.get_gecos_access_data() is None:
            self.set_gecos_access_data(GecosAccessData())
        self.get_gecos_access_data().set_url(self.gecosCCurlEntry.get())
        self.get_gecos_access_data().set_login(self.gecosCCuserEntry.get())
        self.get_gecos_access_data().set_password(self.gecosCCpassEntry.get())
        
        self.get_workstation_data()
        if self.get_workstation_data() is None:
            self.set_workstation_data(WorkstationData())
        self.get_workstation_data().set_name(self.workstationNameEntry.get())
        self.get_workstation_data().set_ou(self.selectOUVar.get())
  
        
        self.controller.connect()

    def disconnect(self):
        self.logger.debug("disconnect")
        
        if self.get_gecos_access_data() is None:
            self.get_gecos_access_data(GecosAccessData())
        self.get_gecos_access_data().set_url(self.gecosCCurlEntry.get())
        self.get_gecos_access_data().set_login(self.gecosCCuserEntry.get())
        self.get_gecos_access_data().set_password(self.gecosCCpassEntry.get())
        
        self.get_workstation_data()
        if self.get_workstation_data() is None:
            self.set_workstation_data(WorkstationData())
        self.get_workstation_data().set_name(self.workstationNameEntry.get())
        self.get_workstation_data().set_ou(self.selectOUVar.get())

        
        self.controller.disconnect()

    def patternSearch(self):
        self.logger.debug("patternSearch")
        
        if self.get_gecos_access_data() is None:
            self.set_gecos_access_data(GecosAccessData())
        self.get_gecos_access_data().set_url(self.gecosCCurlEntry.get())
        self.get_gecos_access_data().set_login(self.gecosCCuserEntry.get())
        self.get_gecos_access_data().set_password(self.gecosCCpassEntry.get())
        
       
        res = self.controller.patternSearch(self.searchFilterEntry.get())
        if isinstance(res, (list, tuple)):
            for r in res:
                self.selectOUSelection['menu'].add_command(label=r[1], command=tk._setit(self.selectOUVar, r[1]))
            self.selectOUVar.set(res[0][1])
        
    def cancel(self):
        self.logger.debug("cancel")
        self.destroy()
                
    def focusUrlField(self):
        self.gecosCCurlEntry.focus()                

    def focusUsernameField(self):
        self.gecosCCuserEntry.focus()                

    def focusPasswordField(self):
        self.gecosCCpassEntry.focus()   
        
    def focusSeachFilterField(self):
        self.searchFilterEntry.focus()   
              
    def focusWorkstationNameField(self):
        self.workstationNameEntry.focus()   
                 
    gecos_access_data = property(get_gecos_access_data, set_gecos_access_data, None, None)
    workstation_data = property(get_workstation_data, set_workstation_data, None, None)
                



        
