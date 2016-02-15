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

from Tkinter import N, S, W, E, NO, Tk
from ttk import Frame, Button, Style, Label, Treeview, Scrollbar
import logging
import json

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class LocalUserListView(Tk):
    '''
    Dialog class that shows the local users list.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        Tk.__init__(self, None, None, 'LocalUserListView', 1, 0, None)
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('LocalUserListView')
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
      
        self.title(_('Manage local users'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Explanation
        explanationLabel1 =  Label(self.body, text=_("You can create, update or delete local users in this workstation."))
        explanationLabel1.grid(column=0, row=1, columnspan=5, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(self.body, text=_("It isn't necessary to create here the users that are authenticated by external services (LDAP, AD, ...)"))
        explanationLabel2.grid(column=0, row=2, columnspan=5, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel3 =  Label(self.body, text=" ")
        explanationLabel3.grid(column=0, row=3, columnspan=5, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel4 =  Label(self.body, text=_("Please check default OEM users and change their passwords when needed:"))
        explanationLabel4.grid(column=0, row=4, columnspan=5, sticky=E+W, padx=padding_x, pady=padding_y)

        # Treeview
        self.treeview = Treeview(self.body, height="5")
        
        self.treeview['columns']=('Login', 'Name')
        
        self.treeview.heading('#1', text=_('Login'), anchor=W)
        self.treeview.heading('#2', text=_('Name'), anchor=W)
        self.treeview.column('#1', stretch=NO, minwidth=0, width=100)
        self.treeview.column('#2', stretch=NO, minwidth=0, width=300)
        
        self.treeview.column('#0', stretch=NO, minwidth=0, width=0) #width 0 to not display it        
        
   
        ysb = Scrollbar(self.body, orient='vertical', command=self.treeview.yview)
        xsb = Scrollbar(self.body, orient='horizontal', command=self.treeview.xview)
        self.treeview.configure(yscroll=ysb.set, xscroll=xsb.set)

        # Lay it out on a grid so that it'll fill the width of the containing window.
        self.treeview.grid(column=0, row=5, columnspan=6, sticky='nsew')
        self.treeview.columnconfigure(0, weight=1)
        ysb.grid(row=5, column=5, sticky='nse')
        xsb.grid(row=6, column=0, columnspan=6, sticky='sew')         
         
         
        # New user button
        newUserButton = Button(self.body, text=_("New"),
            command=self.new)
        newUserButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Update user button
        updateUserButton = Button(self.body, text=_("Update"),
            command=self.update)
        updateUserButton.grid(column=1, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Delete user button
        deleteUserButton = Button(self.body, text=_("Delete"),
            command=self.delete)
        deleteUserButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)


        # Accept button
        closeButton = Button(self.body, text=_("Go Back"),
            command=self.accept)
        closeButton.grid(column=5, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        self.refresh()
        
        self.grab_set()
        self.mainloop()

    def refresh(self):
        self.treeview.delete(*self.treeview.get_children())
        data = self.get_data()
        if data is not None:
            for user in data:
                self.treeview.insert("" , "end", "", values=(user.get_login(), user.get_name()))

    def accept(self):
        self.logger.debug("Accept")
        self.destroy()

    def cancel(self):
        self.logger.debug("Cancel")
        self.destroy()

    def new(self):
        self.logger.debug("New")
        self.localUserController.newElement()
    
    def setLocalUserController(self, localUserController):
        self.localUserController = localUserController

    def _get_selected_user(self):
        if (self.treeview.selection() is not None
            and isinstance(self.treeview.selection(), tuple)):
            selected = self.treeview.selection()[0]
            item = self.treeview.item(selected)
            login = item["values"][0]
            self.logger.debug("login = %s", login)
            
            data = self.get_data()
            if data is not None:
                for user in data:
                    if user.get_login() == login:
                        return user
        else:
            self.logger.debug("No user selected")
            
                
        return None

    def update(self):
        self.logger.debug("New")
        user = self._get_selected_user()
        if user is None:
            self.logger.error("Strange error: User is None!")
            return
        
        self.localUserController.updateElement(user)

    def delete(self):
        self.logger.debug("New")
        user = self._get_selected_user()
        if user is None:
            self.logger.error("Strange error: User is None!")
            return
        
        self.localUserController.deleteElement(user)
        
        
    data = property(get_data, set_data, None, None)



        
