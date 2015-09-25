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

from dto.ADSetupData import ADSetupData

import tkMessageBox

class ADSetupDataElemView(Toplevel):
    '''
    Dialog class to ask the user for the Active Directory administrator user and password.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('ADSetupDataElemView')
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
      
        self.title(_('Active Directory credentials needed'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Explanation
        explanationLabel1 =  Label(self.body, text=_("To setup or remove the Active Directory authentication method you"))
        explanationLabel1.grid(column=0, row=1, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(self.body, text=_("have to specify an AD administrator user and password:"))
        explanationLabel2.grid(column=0, row=2, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)


        # Domain
        adDomainLabel = Label(self.body, text=_("Domain:"))
        adDomainLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adDomainEntry = Entry(self.body)
        self.adDomainEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # Workgroup
        adWorkgroupLabel = Label(self.body, text=_("Workgroup:"))
        adWorkgroupLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adWorkgroupEntry = Entry(self.body)
        self.adWorkgroupEntry.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # User
        adUserLabel = Label(self.body, text=_("User:"))
        adUserLabel.grid(column=0, row=5, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adUserEntry = Entry(self.body)
        self.adUserEntry.grid(column=1, row=5, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.adUserEntry.delete(0, END)
        self.adUserEntry.insert(0, "<AD_user>")

        # Password
        adPasswordLabel = Label(self.body, text=_("Password:"))
        adPasswordLabel.grid(column=0, row=6, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adPasswordEntry = Entry(self.body, show="*")
        self.adPasswordEntry.grid(column=1, row=6, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.adPasswordEntry.delete(0, END)

        
         
        # Cancel button
        cancelButton = Button(self.body, text=_("Cancel"),
            command=self.cancel)
        cancelButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Accept button
        acceptButton = Button(self.body, text=_("Accept"),
            command=self.accept)
        acceptButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            self.adDomainEntry.delete(0, END)
            self.adDomainEntry.insert(0, data.get_domain())
            self.adDomainEntry.config(state='disabled')

            self.adWorkgroupEntry.delete(0, END)
            self.adWorkgroupEntry.insert(0, data.get_workgroup())
            self.adWorkgroupEntry.config(state='disabled')

        
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def accept(self):
        self.logger.debug("Accept")
        if self.get_data() is None:
            self.set_data(ADSetupData())
        self.get_data().set_domain(self.adDomainEntry.get())
        self.get_data().set_workgroup(self.adWorkgroupEntry.get())
        self.get_data().set_ad_administrator_user(self.adUserEntry.get())
        self.get_data().set_ad_administrator_pass(self.adPasswordEntry.get())
        
        if self.get_data().test():
            self.destroy()
        else:
            tkMessageBox.showwarning(_("Active Directory connection error"), 
                _("Can't connect to Active Directory.\nPlease double-check all the fields"), 
                parent=self)            


    def cancel(self):
        self.logger.debug("cancel")
        self.set_data(None)
        self.destroy()
                
    data = property(get_data, set_data, None, None)



        
