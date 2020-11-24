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

__author__ = "Francisco Fuentes Barrera <ffuentes@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"

import logging
import gettext
from gettext import gettext as _
from gecosws_config_assistant.view.GladeWindow import GladeWindow
from gi.repository import Gtk

from gecosws_config_assistant.dto.LDAPAuthMethod import LDAPAuthMethod
from gecosws_config_assistant.dto.ADAuthMethod import ADAuthMethod

gettext.textdomain('gecosws-config-assistant')

class SystemStatusElemDialog(GladeWindow):
    '''
    Dialog class that shows the system status.
    '''


    def __init__(self, controller, parent):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = controller
        self.logger = logging.getLogger('SystemStatusElemDialog')
        self.gladepath = 'systemstatus.glade'

        self.data = None

        self.initUI()

    def get_data(self):
        ''' Getter data '''

        return self.__data

    def set_data(self, value):
        ''' Setter data '''

        self.__data = value

    def initUI(self):
        ''' Initialize UI '''

        self.buildUI(self.gladepath)
        self.logger.debug('UI initiated')

    def extractGUIElements(self):
        ''' Extract GUI elements '''

        self.window       = self.getElementById('window1')
        self.acceptButton = self.getElementById('button1')
        self.statusText   = self.getElementById('textview1')

        self.statusText.set_editable(False)
        self.statusText.set_cursor_visible(False)
        self.statusText.set_justification(Gtk.Justification.LEFT)
        self.statusText.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

        self.textBuffer   = self.statusText.get_buffer()

        self.dialog       = self.window

    def addHandlers(self):
        ''' Adding handlers '''

        self.handlers = self.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding back handler")
        self.handlers["onBack"] = self.goBack

    def show(self):
        ''' Show '''

        self.logger.debug("Show")
        self.extractGUIElements()
        self.window.set_title(_('System status'))

        data = self.get_data()
        if data is not None:
            if data.get_cga_version() is not None:
                statusText = _('Assistant version: ') + \
                             data.get_cga_version() + "\n"
            else:
                statusText = _('Assistant version: ') + \
                             _("UNKNOWN VERSION")+ "\n"

            if data.get_workstation_data() is not None:
                d = data.get_workstation_data()
                if d.get_name() is not None:
                    statusText += _('Workstation name: ') + \
                                  d.get_name() + "\n"

            if data.get_time_server() is not None:
                d = data.get_time_server()
                if d.get_address() is not None:
                    statusText += _('Time server: ') + d.get_address()+ "\n"

            if data.get_network_interfaces() is not None:
                statusText += "\n" + _('Network interfaces: ')  + "\n"
                statusText += "=====================================\n"
                for d in data.get_network_interfaces():
                    statusText += d.get_name() + "\t" + \
                                  d.get_ip_address() + "\n"

            if data.get_gecos_access_data() is not None:
                statusText += "\n" + \
                              _('GECOS Control Center connection data: ') + \
                               "\n"
                statusText += "=====================================\n"
                d = data.get_gecos_access_data()
                statusText += _('Server URL:') + d.get_url() + "\n"
                statusText += _('Login:') + d.get_login() + "\n"

            if data.get_local_users() is not None:
                statusText += "\n" + _('Local users: ')  + "\n"
                statusText += "=====================================\n"
                for user in data.get_local_users():
                    statusText += user.get_login() + "\t\t" + \
                                  user.get_name() + "\n"

            if data.get_user_authentication_method() is not None:
                statusText += "\n" + _('User authentication method: ')  + "\n"
                statusText += "=====================================\n"
                d = data.get_user_authentication_method()
                statusText += _('Method:') + d.get_name() + "\n"

                if isinstance(d, ADAuthMethod):
                    statusText += _('Domain:') + \
                                  d.get_data().get_domain() + "\n"
                    statusText += _('Workgroup:') + \
                                  d.get_data().get_workgroup() + "\n"

                if isinstance(d, LDAPAuthMethod):
                    statusText += _('Server URI:') + \
                                  d.get_data().get_uri() + "\n"
                    statusText += _('Users base DN:') + \
                                  d.get_data().get_base() + "\n"
                    statusText += _('Groups base DN:') + \
                                  d.get_data().get_base_group() + "\n"

            self.textBuffer.set_text(statusText)
        else:
            self.textBuffer.set_text(_('No status data!'))

        self.window.set_modal(True)
        self.window.set_transient_for(self.parent.window)
        self.window.show_all()

        x, y = self.parent.window.get_position()
        w, h = self.parent.window.get_size()
        sw, sh = self.window.get_size()
        self.logger.debug('x={} y={} w={} h={} sw={} sh={}'.format(
            x, y, w, h, sw, sh))
        self.window.move(x + w/2 - sw/2, y + h/2 - sh/2)

        while Gtk.events_pending():
            Gtk.main_iteration()

    def goBack(self, *args):
        ''' Go back '''

        self.logger.debug("Go back")
        self.dialog.destroy()

    data = property(
        get_data,
        set_data,
        None,
        None)
