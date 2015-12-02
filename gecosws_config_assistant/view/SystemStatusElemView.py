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

from Tkinter import N, S, W, E, END, Tk
from ScrolledText import ScrolledText
from ttk import Frame, Button, Style
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from gecosws_config_assistant.dto.LDAPAuthMethod import LDAPAuthMethod
from gecosws_config_assistant.dto.ADAuthMethod import ADAuthMethod

class SystemStatusElemView(Tk):
    '''
    Dialog class that shows the system status.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        Tk.__init__(self, None, None, 'SystemStatusElemView', 1, 0, None)
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('SystemStatusElemView')
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
      
        self.title(_('System status'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10


        # Status text
        self.statusText = ScrolledText(self.body, height=10, width=50)
        self.statusText.grid(column=0, row=0, sticky=E, padx=padding_x, pady=padding_y)
        
        # Accept button
        acceptButton = Button(self.body, text=_("Accept"),
            command=self.accept)
        acceptButton.grid(column=0, row=1, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            if data.get_cga_version() is not None:
                statusText = _('Assistant version: ') + data.get_cga_version() + "\n"
            else:
                statusText = _('Assistant version: ') + _("UNKNOWN VERSION")+ "\n"
            
            if data.get_workstation_data() is not None:
                d = data.get_workstation_data()
                if d.get_name() is not None:
                    statusText += _('Workstation name: ') + d.get_name() + "\n"

            if data.get_time_server() is not None:
                d = data.get_time_server()
                if d.get_address() is not None:
                    statusText += _('Time server: ') + d.get_address() + "\n"

            if data.get_network_interfaces() is not None:
                statusText += "\n" + _('Network interfaces: ')  + "\n"
                statusText += "=====================================\n"
                for d in data.get_network_interfaces():
                    statusText += d.get_name() +"\t" + d.get_ip_address() + "\n"
            
            if data.get_gecos_access_data() is not None:
                statusText += "\n" + _('GECOS Control Center connection data: ')  + "\n"
                statusText += "=====================================\n"
                d = data.get_gecos_access_data() 
                statusText += _('Server URL:') + d.get_url() + "\n"
                statusText += _('Login:') + d.get_login() + "\n"

            if data.get_local_users() is not None:
                statusText += "\n" + _('Local users: ')  + "\n"
                statusText += "=====================================\n"
                for d in data.get_local_users():
                    statusText += d.get_login() + "\t\t" + d.get_name().encode('utf-8') + "\n"


            if data.get_user_authentication_method() is not None:
                statusText += "\n" + _('User authentication method: ')  + "\n"
                statusText += "=====================================\n"
                d = data.get_user_authentication_method() 
                statusText += _('Method:') + d.get_name() + "\n"
                
                if isinstance(d, ADAuthMethod):
                    statusText += _('Domain:') + d.get_data().get_domain() + "\n"
                    statusText += _('Workgroup:') + d.get_data().get_workgroup() + "\n"
                    
                if isinstance(d, LDAPAuthMethod):
                    statusText += _('Server URI:') + d.get_data().get_uri() + "\n"
                    statusText += _('Users base DN:') + d.get_data().get_base() + "\n"
                    statusText += _('Groups base DN:') + d.get_data().get_base_group() + "\n"
                
            
            self.statusText.insert(END, statusText)
        else:
            self.statusText.insert(END, _('No status data!'))
        
        self.grab_set()
        self.mainloop()


    def accept(self):
        self.logger.debug("Accept")
        self.destroy()

    data = property(get_data, set_data, None, None)