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
import json
import gettext
from gettext import gettext as _
from gecosws_config_assistant.view.GladeWindow import GladeWindow
from gi.repository import Gtk

from gecosws_config_assistant.dto.LocalUser import LocalUser
from gecosws_config_assistant.view.CommonDialog import showerror_gtk

gettext.textdomain('gecosws-config-assistant')

class LocalUserElemDialog(GladeWindow):
    '''
    Dialog class that shows the a local user element, redone in glade
    '''

    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('LocalUserElemDialog')
        self.gladepath = 'localuserpopup.glade'

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

        self.window                    = self.getElementById("window1")
        self.dialog                    = self.window

        self.nameLabel                 = self.getElementById("label1")
        self.loginLabel                = self.getElementById("label2")
        self.passwordLabel             = self.getElementById("label3")
        self.passwordConfirmationLabel = self.getElementById("label4")

        self.nameEntry                 = self.getElementById("entry1")
        self.loginEntry                = self.getElementById("entry2")
        self.passwordEntry             = self.getElementById("entry3")
        self.passwordConfirmationEntry = self.getElementById("entry4")

    def show(self):
        ''' Show '''

        self.logger.debug("Show")
        self.extractGUIElements()

        data = self.get_data()
        if data is not None:
            self.window.set_title(_('Modifiy local user'))
            self.nameEntry.set_text(data.get_name())

            self.loginEntry.set_text(data.get_login())
            self.loginEntry.set_editable(False)
        else:
            self.window.set_title(_('Add local user'))

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

    def addHandlers(self):
        ''' Adding handlers '''

        self.handlers = self.parent.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding new handler")
        self.handlers["onAcpt"] = self.accept
        self.logger.debug("Adding update handler")
        self.handlers["onBack"] = self.cancel

    def _test(self):
        # Test confirm password
        password = self.passwordEntry.get_text()
        confirm = self.passwordConfirmationEntry.get_text()

        if password is not None and password.strip() != '':
            if confirm is None or confirm.strip() == '':
                self.logger.debug("Empty password confirmation!")
                showerror_gtk(
                    _("The password confirmation field is empty!") + "\n" +
                    _("Please fill all the mandatory fields."),
                    self)
                self.passwordConfirmationEntry.grab_focus()
                return False

            if confirm != password:
                self.logger.debug(
                    "Password confirmation different from password!")
                showerror_gtk(
                    _("The password confirmation is different from password"),
                    self)
                self.passwordConfirmationEntry.grab_focus()
                return False

        return True

    def accept(self, *args):
        ''' Accept '''

        self.logger.debug("Accept")

        user = LocalUser()
        user.set_login(self.loginEntry.get_text())
        user.set_name(self.nameEntry.get_text())
        user.set_password(self.passwordEntry.get_text())

        check_password = (self.get_data() is None)

        if self.controller.test(user, check_password) and self._test():
            self.logger.debug("Test is ok")
            self.set_data(user)
            self.controller.createNewElement()
            self.dialog.destroy()

    def cancel(self, *args):
        ''' Cancel '''

        self.logger.debug("cancel")
        self.dialog.destroy()

    def focusLoginField(self):
        ''' Focus the login field '''
        self.loginEntry.grab_focus()

    def focusNameField(self):
        ''' Focus the name field '''
        self.nameEntry.grab_focus()

    def focusPasswordField(self):
        ''' Focus the password field '''
        self.passwordEntry.grab_focus()

    data = property(
        get_data,
        set_data,
        None,
        None)
