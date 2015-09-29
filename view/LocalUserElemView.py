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

from dto.LocalUser import LocalUser
from view.CommonDialog import showerror

class LocalUserElemView(Toplevel):
    '''
    Dialog class that shows the a local user element.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('LocalUserElemView')
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
      
        self.title(_('Add local user'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10


        # Name
        nameLabel = Label(self.body, text=_("Name:"))
        nameLabel.grid(column=0, row=1, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.nameEntry = Entry(self.body)
        self.nameEntry.grid(column=1, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.nameEntry.delete(0, END)
        
        # Login
        loginLabel = Label(self.body, text=_("Login:"))
        loginLabel.grid(column=0, row=2, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.loginEntry = Entry(self.body)
        self.loginEntry.grid(column=1, row=2, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.loginEntry.delete(0, END)


        # Password
        passwordLabel = Label(self.body, text=_("Password:"))
        passwordLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.passwordEntry = Entry(self.body, show="*")
        self.passwordEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.passwordEntry.delete(0, END)
        
        # Password confirmation
        passwordConfirmationLabel = Label(self.body, text=_("Confirm:"))
        passwordConfirmationLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.passwordConfirmationEntry = Entry(self.body, show="*")
        self.passwordConfirmationEntry.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.passwordConfirmationEntry.delete(0, END)
         
        # Cancel button
        cancelButton = Button(self.body, text=_("Cancel"),
            command=self.cancel)
        cancelButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Accept button
        acceptButton = Button(self.body, text=_("Accept"),
            command=self.accept)
        acceptButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            self.title(_('Modifiy local user'))
            self.nameEntry.delete(0, END)
            self.nameEntry.insert(0, data.get_name())

            self.loginEntry.delete(0, END)
            self.loginEntry.insert(0, data.get_login())
            self.loginEntry.config(state='disabled')
        else:
            self.title(_('Add local user'))
        
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def _test(self):
        # Test confirm password
        password = self.passwordEntry.get()
        confirm = self.passwordConfirmationEntry.get()
        
        if password is not None and password.strip() != '':
            if confirm is None or confirm.strip() == '':
                self.logger.debug("Empty password confirmation!")
                showerror(_('Error in user data'), 
                     _("The password confirmation field is empty!") + "\n" 
                     + _("Please fill all the mandatory fields."),
                    self)
                self.passwordConfirmationEntry.focus()  
                return False
            
            if confirm != password:
                self.logger.debug("Password confirmation different from password!")
                showerror(_('Error in user data'), 
                     _("The password confirmation is different from password") ,
                    self)
                self.passwordConfirmationEntry.focus()  
                return False
            
        
        return True        

    def accept(self):
        self.logger.debug("Accept")
        
        user = LocalUser()
        user.set_login(self.loginEntry.get())
        user.set_name(self.nameEntry.get())
        user.set_password(self.passwordEntry.get())
        
        check_password = (self.get_data() is None)
        
        if self.controller.test(user, check_password) and self._test():
            self.set_data(user)
            self.destroy()

    def cancel(self):
        self.logger.debug("cancel")
        self.destroy()
                
                
    def focusLoginField(self):
        self.loginEntry.focus()                

    def focusNameField(self):
        self.nameEntry.focus()                

    def focusPasswordField(self):
        self.passwordEntry.focus()                     
                
    data = property(get_data, set_data, None, None)



        
