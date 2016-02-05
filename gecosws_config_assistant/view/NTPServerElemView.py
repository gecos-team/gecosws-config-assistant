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

from GladeWindow import GladeWindow
from gi.repository import Gtk, Gdk
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from gecosws_config_assistant.dto.NTPServer import NTPServer

from gecosws_config_assistant.view.CommonDialog import showwarning_gtk, showinfo_gtk

class NTPServerElemView(GladeWindow):
    '''
    Dialog class that shows the a NTP server element.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('NTPServerElemView')
        self.gladepath = 'ntp.glade'
        
        self.data = None
        self.displaySuccess = True
        
        self.initUI()        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value



    def initUI(self):
        self.buildUI(self.gladepath)
        

    def addHandlers(self):
        self.logger.debug("Adding all handlers")
        self.handlers = self.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding check ntp connection")
        self.handlers["onChek"] = self.test
        self.logger.debug("Adding OK handler")
        self.handlers["onOOKK"] = self.accept
        self.logger.debug("Adding back handler")
        self.handlers["onBack"] = self.goBack

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            self.getElementById('ntp_server_entry').set_text(data.get_address())
        
        self.parent.navigate(self)
        
    def goBack(self, *args):
        self.logger.debug("Go back")
        self.controller.mainWindowController.backToMainWindowDialog()

    def accept(self, *args):
        self.logger.debug("Accept")
        if self.get_data() is None:
            self.set_data(NTPServer())
        self.get_data().set_address(self.getElementById('ntp_server_entry').get_text())
        
        self.displaySuccess = False
        if self.test(False):
            self.displaySuccess = True
            self.controller.save()
        self.displaySuccess = True


    def test(self, *args):
        self.logger.debug("test")
        if self.get_data() is None:
            self.set_data(NTPServer())
        self.get_data().set_address(self.getElementById('ntp_server_entry').get_text())
        self.logger.debug("test: %s"%(self.get_data().get_address()))
        result = self.controller.test()
        
        if not result:
            showwarning_gtk(_("Can't connect with NTP server.\nPlease double-check the NTP server address"), 
                self)
        elif self.displaySuccess:
            showinfo_gtk(_("NTP server connection successful"), self)
            
        return result
        
    def cancel(self, *args):
        self.logger.debug("cancel")
        self.controller.hide()
                
    data = property(get_data, set_data, None, None)



        
