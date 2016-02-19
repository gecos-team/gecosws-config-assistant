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

from gecosws_config_assistant.dao.NTPServerDAO import NTPServerDAO
from gecosws_config_assistant.dto.NTPServer import NTPServer
from gecosws_config_assistant.view.NTPServerElemView import NTPServerElemView
from gecosws_config_assistant.view.CommonDialog import showerror_gtk

import logging
import json

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class NTPServerController(object):
    '''
    Controller class for the NTP time synchronization functionality.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        self.view = None # TODO!
        self.mainWindowController = mainController
        self.dao = NTPServerDAO()
        self.logger = logging.getLogger('NTPServerController')


    def show(self, mainWindow):
        self.logger.debug('show - BEGIN')
        self.view = NTPServerElemView(mainWindow, self)
        
        ntpDto = self.dao.load()
        
        conf = self.mainWindowController.requirementsCheck.autoSetup.get_conf()
        ntpKey = 'uri_ntp'
        if conf:
            self.logger.debug('We got an autoconf response object')
            if conf.has_key(ntpKey) and conf[ntpKey].strip() != '':
                self.logger.debug('Ntp key is present in the autoconf object')
                ntpDto = NTPServer()
                ntpDto.set_address(conf[ntpKey])
            else:
                self.logger.debug('Something went wrong extractiong data from the json repsone')
        else:
            self.logger.debug('Autoconf is not done yet')
        
        self.view.set_data(ntpDto)
        
        self.view.show()   
        self.logger.debug('show - END')

    def hide(self):
        self.logger.debug('hide')
        self.mainWindowController.showRequirementsCheckDialog()
    
    def save(self):
        self.logger.debug('save')
        data = self.view.get_data()
        try:
            if self.dao.save(data):
                self.hide()
            else:
                # Show error message
                showerror_gtk(_("Error saving NTP server data.") + "\n" + _("See log for more details."),
                    self.view)
        except:
            # Show error message
            showerror_gtk(_("Error saving NTP server data.") + "\n" + _("See log for more details."),
                self.view)
            

    def test(self):
        self.logger.debug('test')
        data = self.view.get_data()
        return data.syncrhonize()
