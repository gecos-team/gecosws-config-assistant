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

__author__ = "David Amian <damian@emergya.com>"
__copyright__ = "Copyright (C) 2014, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"




from firstboot_lib import PageWindow
from firstboot import serverconf
import firstboot.pages.autoConfig
import firstboot.validation as validation

from gi.repository import Gtk
import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

import firstboot.pages


__REQUIRED__ = False


def get_page(main_window):

    page = AutoConfigResult(main_window)
    return page


class AutoConfigResult(PageWindow.PageWindow):
    __gtype_name__ = "AutoConfigResult"

	def finish_initializing(self):
        self.set_status(None)

	def load_page(self, params=None):
        self.server_conf = serverconf.get_server_conf(None)
        self.ui.lblVersionValue.set_label(self.server_conf.get_version())
        self.ui.lblOrganizationValue.set_label(self.server_conf.get_organization())
#           self.ui.lblNotesValue.set_label(self.server_conf.get_notes())
		


    def translate(self):
        desc = _("This is the information about autoconfig file")

        self.ui.lblDescription.set_text(desc)

        self.ui.lblVersion.set_label(_('Version'))
        self.ui.lblOrganization.set_label(_('Organization'))
        self.ui.lblNotes.set_label(_('Notes'))

	def set_status(self, code, description=''):

        self.ui.imgStatus.set_visible(code != None)
        self.ui.lblStatus.set_visible(code != None)

        if code == None:
            return

        if code == 0:
            icon = Gtk.STOCK_YES

        else:
            icon = Gtk.STOCK_DIALOG_ERROR

        self.ui.imgStatus.set_from_stock(icon, Gtk.IconSize.MENU)
        self.ui.lblStatus.set_label(description)
    
    def previous_page(self, load_page_callback):    
        load_page_callback(firstboot.pages.autoConfig)

    def next_page(self, load_page_callback):
        load_page_callback(firstboot.pages.dateSync)
