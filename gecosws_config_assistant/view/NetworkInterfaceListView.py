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

from Tkinter import N, S, W, E, Toplevel, NO
from ttk import Frame, Button, Style, Label, Treeview, Scrollbar
import logging
import os

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class NetworkInterfaceListView(Toplevel):
    '''
    Dialog class that shows the "network interfaces" list.
    '''

    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('NetworkInterfaceListView')
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
      
        self.title(_('Network setup'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Explanation
        explanationLabel1 =  Label(self.body, text=_("This workstations needs a network connection to authenticate"))
        explanationLabel1.grid(column=0, row=1, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(self.body, text=_("the users, link with the GECOS server and install software"))
        explanationLabel2.grid(column=0, row=2, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel3 =  Label(self.body, text=" ")
        explanationLabel3.grid(column=0, row=3, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel4 =  Label(self.body, text=_("Available network connections are:"))
        explanationLabel4.grid(column=0, row=4, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        # Treeview
        self.treeview = Treeview(self.body, height="5")
        
        self.treeview['columns']=('Interface', 'IP')
        
        self.treeview.heading('#1', text=_('Interface'), anchor=W)
        self.treeview.heading('#2', text=_('IP'), anchor=W)
        self.treeview.column('#1', stretch=NO, minwidth=0, width=100)
        self.treeview.column('#2', stretch=NO, minwidth=0, width=300)
        
        self.treeview.column('#0', stretch=NO, minwidth=0, width=0) #width 0 to not display it        
        
   
        ysb = Scrollbar(self.body, orient='vertical', command=self.treeview.yview)
        xsb = Scrollbar(self.body, orient='horizontal', command=self.treeview.xview)
        self.treeview.configure(yscroll=ysb.set, xscroll=xsb.set)

        # Lay it out on a grid so that it'll fill the width of the containing window.
        self.treeview.grid(column=0, row=5, columnspan=3, sticky='nsew')
        self.treeview.columnconfigure(0, weight=1)
        ysb.grid(row=5, column=3, sticky='nse')
        xsb.grid(row=6, column=0, columnspan=3, sticky='sew')         
         
         
        # Setup network interface button
        setupNetworkButton = Button(self.body, text=_("Setup network interface"),
            command=self.setupNetworkConnection)
        setupNetworkButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Accept button
        closeButton = Button(self.body, text=_("Accept"),
            command=self.close)
        closeButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            for ni in data:
                self.treeview.insert("" , "end", "", values=(ni.get_name(), ni.get_ip_address()))
        
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def close(self):
        self.logger.debug("Close")
        self.destroy()


    def setupNetworkConnection(self):
        self.logger.debug("setupNetworkConnection")
        cmd = 'nm-connection-editor'
        os.spawnlp(os.P_NOWAIT, cmd, cmd)
        
        
    data = property(get_data, set_data, None, None)



        
