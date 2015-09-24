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

from Tkinter import N, S, W, E, Toplevel, END
from ttk import Frame, Button, Style, Label, Entry
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from dto.GecosAccessData import GecosAccessData

class AutoSetupDialog(Toplevel):
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
        self.logger = logging.getLogger('AutoSetupDialog')
        self.logger.setLevel(logging.DEBUG)
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
      
        self.title(_('Auto setup'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Explanation
        explanationLabel1 =  Label(self.body, text=_("Some of the setup parameters can be filled automatically"))
        explanationLabel1.grid(column=0, row=1, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(self.body, text=_("if you have a setup file in your GECOS server."))
        explanationLabel2.grid(column=0, row=2, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)


        # Gecos CC URL
        gecosCCurlLabel = Label(self.body, text=_("Gecos Control Center URL:"))
        gecosCCurlLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.gecosCCurlEntry = Entry(self.body)
        self.gecosCCurlEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.gecosCCurlEntry.delete(0, END)
        self.gecosCCurlEntry.insert(0, "http://your.gecos.server.url")

        # Gecos CC user
        gecosCCuserLabel = Label(self.body, text=_("User:"))
        gecosCCuserLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.gecosCCuserEntry = Entry(self.body)
        self.gecosCCuserEntry.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.gecosCCuserEntry.delete(0, END)
        self.gecosCCuserEntry.insert(0, "<gecos_administrator_username>")

        # Gecos CC password
        gecosCCpassLabel = Label(self.body, text=_("Password:"))
        gecosCCpassLabel.grid(column=0, row=5, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.gecosCCpassEntry = Entry(self.body, show="*")
        self.gecosCCpassEntry.grid(column=1, row=5, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.gecosCCpassEntry.delete(0, END)
        
         
        # Setup Gecos CC
        testButton = Button(self.body, text=_("Setup"),
            command=self.setup)
        testButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Cancel button
        acceptButton = Button(self.body, text=_("Cancel"),
            command=self.cancel)
        acceptButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            if (data.get_url() is not None
                and data.get_url().strip() != ''):
                self.gecosCCurlEntry.delete(0, END)
                self.gecosCCurlEntry.insert(0, data.get_url())

            if (data.get_login() is not None
                and data.get_login().strip() != ''):
                self.gecosCCuserEntry.delete(0, END)
                self.gecosCCuserEntry.insert(0, data.get_login())
            
            if (data.get_password() is not None
                and data.get_password().strip() != ''):
                self.gecosCCpassEntry.delete(0, END)
                self.gecosCCpassEntry.insert(0, data.get_password())
        
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def setup(self):
        self.logger.debug("setup")
        if self.get_data() is None:
            self.set_data(GecosAccessData())
        self.get_data().set_url(self.gecosCCurlEntry.get())
        self.get_data().set_login(self.gecosCCuserEntry.get())
        self.get_data().set_password(self.gecosCCpassEntry.get())
        
        self.controller.setup()


    def cancel(self):
        self.logger.debug("cancel")
        self.destroy()
                
    def focusUrlField(self):
        self.gecosCCurlEntry.focus()                

    def focusUsernameField(self):
        self.gecosCCuserEntry.focus()                

    def focusPasswordField(self):
        self.gecosCCpassEntry.focus()                
                
    data = property(get_data, set_data, None, None)



        
