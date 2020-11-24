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
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"

import logging
import gettext

from gecosws_config_assistant.view.GladeWindow import GladeWindow


from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
gettext.textdomain('gecosws-config-assistant')

class AutoSetupDialog(GladeWindow):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''

    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('AutoSetupDialog')
        self.gladepath = 'autoconf.glade'

        self.data = None

        self.initUI()

    def get_data(self):
        ''' Getter data '''

        return self.__data

    def set_data(self, value):
        ''' Setter data '''

        self.__data = value

    def initUI(self):
        ''' Initilize UI '''

        self.buildUI(self.gladepath)

        self.logger.debug('UI initiated')

    def addHandlers(self):
        ''' Adding handlers '''

        self.logger.debug("Adding all handlers")
        self.handlers = self.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding back handler")
        self.handlers["onBack"] = self.cancel
        self.logger.debug("Adding connect handler")
        self.handlers["onConn"] = self.setup

    def show(self):
        ''' Showing view '''

        self.logger.debug("Show")

        data = self.get_data()
        if data is not None:
            if (data.get_url() is not None
                and data.get_url().strip() != ''):
                self.getElementById('url_entry').set_text(data.get_url(),)

            if (data.get_login() is not None
                and data.get_login().strip() != ''):
                self.getElementById('login_entry').set_text(data.get_login())

            if (data.get_password() is not None
                and data.get_password().strip() != ''):
                self.getElementById('password_entry') \
                .set_text(data.get_password())

        self.parent.navigate(self)

    def setup(self, *args):
        ''' Setup action '''

        self.logger.debug("setup")
        if self.get_data() is None:
            self.set_data(GecosAccessData())
        self.get_data() \
            .set_url(self.getElementById('url_entry').get_text())
        self.get_data() \
            .set_login(self.getElementById('login_entry').get_text())
        self.get_data() \
            .set_password(self.getElementById('password_entry').get_text())

        self.controller.setup()

    def cancel(self, *args):
        ''' Cancel action '''

        self.logger.debug("cancel")
        self.controller.cancel()

    def focusUrlField(self):
        ''' Focus url field '''

        self.getElementById('url_entry').grab_focus()

    def focusUsernameField(self):
        ''' Focus username field '''

        self.logger.debug("focusUsernamefield")
        self.getElementById('login_entry').grab_focus()

    def focusPasswordField(self):
        ''' Focus password field '''

        self.logger.debug("focusPasswordfield")
        self.getElementById('password_entry').grab_focus()

    def setAutoSetupDataLoadStatus(self, text):
        ''' Set auto data load status '''

        self.logger.debug("setAutoSetupDataLoadStatus")
        self.getElementById('status').set_text(text)

    data = property(
        get_data,
        set_data,
        None,
        None)
