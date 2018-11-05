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

from gecosws_config_assistant.view.GladeWindow import GladeWindow
from gi.repository import Gtk
import logging
import gettext
from gettext import gettext as _

from gecosws_config_assistant.dto.ADSetupData import ADSetupData
from gecosws_config_assistant.view.CommonDialog import showerror_gtk

gettext.textdomain('gecosws-config-assistant')

class ADSetupDataElemView(GladeWindow):
    '''
    Dialog class to ask the user for the
    Active Directory administrator user and password.
    '''

    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('ADSetupDataElemView')
        self.gladePath = 'adsetupdata.glade'

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

        self.buildUI(self.gladePath)
        self.adDomainEntry = self.getElementById("ad_domain")
        self.adWorkgroupEntry = self.getElementById("ad_workgroup")
        self.adUserEntry = self.getElementById("ad_admin_login")
        self.adPasswordEntry = self.getElementById("ad_admin_pass")

    def addHandlers(self):
        ''' Add Handlers '''

        self.handlers = {}
        # add new handlers here
        self.logger.debug("Adding link/unlink handler")
        self.handlers["onAccept"] = self.accept
        self.handlers["onCancel"] = self.cancel

    def show(self):
        self.logger.debug("Show")

        data = self.get_data()
        if data is not None:
            self.adDomainEntry.set_text(data.get_domain())
            self.adDomainEntry.set_editable(False)

            self.adWorkgroupEntry.set_text(data.get_workgroup())
            self.adWorkgroupEntry.set_editable(False)

        self.window.set_modal(True)
        self.window.set_transient_for(self.parent.window)
        self.window.show_all()

        x, y = self.parent.window.get_position()
        w, h = self.parent.window.get_size()
        sw, sh = self.window.get_size()
        self.logger.debug('x={} y={} w= {} h={} sw={} sh={}' \
                          .format(x, y, w, h, sw, sh))
        self.window.move(x + w / 2 - sw / 2, y + h / 2 - sh / 2)

        # while Gtk.events_pending():
        #    Gtk.main_iteration()
        Gtk.main()

    def accept(self, *args):
        ''' Accept action '''

        self.logger.debug("Accept")
        if self.get_data() is None:
            self.set_data(ADSetupData())
        self.get_data().set_domain(self.adDomainEntry.get_text())
        self.get_data().set_workgroup(self.adWorkgroupEntry.get_text())
        self.get_data().set_ad_administrator_user(self.adUserEntry.get_text())
        self.get_data().set_ad_administrator_pass(
            self.adPasswordEntry.get_text())

        if self.get_data().test():
            self.window.hide()
            Gtk.main_quit()
        else:
            showerror_gtk(
                _("Can't connect to Active Directory.\n" +
                  "Please double-check all the fields"),
                None)

    def cancel(self, *args):
        ''' Cancel action '''

        self.logger.debug("cancel")
        self.set_data(None)
        self.window.hide()
        Gtk.main_quit()

    data = property(
        get_data,
        set_data,
        None,
        None)
