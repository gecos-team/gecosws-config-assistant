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

from dto.NTPServer import NTPServer

import tkMessageBox

class NTPServerElemView(Toplevel):
    '''
    Dialog class that shows the a NTP server element.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('NTPServerElemView')
        self.logger.setLevel(logging.DEBUG)
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
      
        self.title(_('Time synchronization'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Explanation
        explanationLabel1 =  Label(self.body, text=_("A precise time is mandatory to coordinate some services"))
        explanationLabel1.grid(column=0, row=1, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(self.body, text=_("Please set your NTP server address:"))
        explanationLabel2.grid(column=0, row=2, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)


        # NTP server address
        ntpServerLabel = Label(self.body, text=_("NTP server:"))
        ntpServerLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.ntpServerEntry = Entry(self.body)
        self.ntpServerEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.ntpServerEntry.delete(0, END)
        self.ntpServerEntry.insert(0, "hora.roa.es")
        
         
        # Setup network interface button
        testButton = Button(self.body, text=_("Test"),
            command=self.test)
        testButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Accept button
        acceptButton = Button(self.body, text=_("Accept"),
            command=self.accept)
        acceptButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            self.ntpServerEntry.delete(0, END)
            self.ntpServerEntry.insert(0, data.get_address())
        
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def accept(self):
        self.logger.debug("Accept")
        if self.get_data() is None:
            self.set_data(NTPServer())
        self.get_data().set_address(self.ntpServerEntry.get())
        
        if self.test(False):
            self.controller.save()


    def test(self, displaySuccess = True):
        self.logger.debug("test")
        if self.get_data() is None:
            self.set_data(NTPServer())
        self.get_data().set_address(self.ntpServerEntry.get())
        result = self.controller.test()
        
        if not result:
            tkMessageBox.showwarning(_("Can't synchronize time"), 
                _("Can't connect with NTP server.\nPlease double-check the NTP server address"), 
                parent=self)
        elif displaySuccess:
            tkMessageBox.showinfo(_("Success"), 
                _("NTP server connection successful"), parent=self)
            
        return result
        
    def cancel(self):
        self.logger.debug("cancel")
        self.destroy()
                
    data = property(get_data, set_data, None, None)



        
