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

__author__ = "Antonio Hernández <ahernandez@emergya.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


import os
from gi.repository import Gtk
import socket



import firstboot.pages
import LinkToServerConfEditorPage
from firstboot_lib import PageWindow
from firstboot import serverconf
from firstboot.serverconf import AuthConf

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')


__REQUIRED__ = True

__TITLE__ = _('Select authentication method')

__STATUS_TEST_PASSED__ = 0
__STATUS_CONFIG_CHANGED__ = 1
__STATUS_CONNECTING__ = 2
__STATUS_ERROR__ = 3

__LDAP__ = 'ldap'
__AD__ = 'ad'

__AD_FLAG__ = '/etc/gca-sssd.control'
__LDAP_FLAG__ = __AD_FLAG__


def get_page(main_window):

    page = LinkToServerPage(main_window)
    return page


class LinkToServerPage(PageWindow.PageWindow):
    __gtype_name__ = "LinkToServerPage"

    def finish_initializing(self):

        self.show_status()

        self.json_cached = serverconf.json_is_cached()
        self.unlink_ldap = False
        self.unlink_ad = False

        self.ldap_is_configured = serverconf.ldap_is_configured()
        self.ad_is_configured = serverconf.ad_is_configured()
        is_configured = self.ldap_is_configured or self.ad_is_configured

        self.ui.radioNone.set_active(True)
        self.ui.boxUnlinkOptions.set_visible(is_configured)
        self.ui.boxAuthSection.set_visible(not is_configured)
        self.main_window.btnNext.set_sensitive(True)

        self.ui.chkUnlinkLDAP.set_visible(self.ldap_is_configured)
        self.ui.chkUnlinkAD.set_visible(False)


    def translate(self):
        desc = _('Users in this workstation can be authenticated against a external system.\n\n')

        if self.ldap_is_configured:
            desc1 = _('This workstation currently uses an authentication user method.')
        elif self.ad_is_configured:
            desc1 = _('This workstation currently uses an authentication user method.')
        else:
            desc1 = _('No authentication system is currently configured.')

        desc2 = _('Select the authentication method you would like to use:')

        self.ui.lblDescription.set_text(desc)
        self.ui.lblDescription1.set_text(desc1)
        self.ui.lblDescription2.set_text(desc2)
        self.ui.chkUnlinkLDAP.set_label(_('Unlink from authentication method'))
        self.ui.chkUnlinkAD.set_label(_('Unlink from authentication method'))
        self.ui.radioLDAP.set_label(_('LDAP'))
        self.ui.radioAD.set_label(_('Active Directory'))
        self.ui.radioNone.set_label(_('None'))

    def on_chkUnlinkLDAP_toggle(self, button):
        active = button.get_active()
        self.unlink_ldap = active
        self.main_window.btnNext.set_sensitive(active)

    def on_chkUnlinkAD_toggle(self, button):
        active = button.get_active()
        self.unlink_ad = active
        self.main_window.btnNext.set_sensitive(active)

    def get_auth_method(self):
        if self.ui.radioLDAP.get_active():
            return __LDAP__

        elif self.ui.radioAD.get_active():
            return __AD__

    def show_status(self, status=None, exception=None):

        icon_size = Gtk.IconSize.BUTTON

        if status == None:
            self.ui.imgStatus.set_visible(False)
            self.ui.lblStatus.set_visible(False)

        elif status == __STATUS_TEST_PASSED__:
            self.ui.imgStatus.set_from_stock(Gtk.STOCK_APPLY, icon_size)
            self.ui.imgStatus.set_visible(True)
            self.ui.lblStatus.set_label(_('The configuration file is valid.'))
            self.ui.lblStatus.set_visible(True)

        elif status == __STATUS_CONFIG_CHANGED__:
            self.ui.imgStatus.set_from_stock(Gtk.STOCK_APPLY, icon_size)
            self.ui.imgStatus.set_visible(True)
            self.ui.lblStatus.set_label(_('The configuration was updated successfully.'))
            self.ui.lblStatus.set_visible(True)

        elif status == __STATUS_ERROR__:
            self.ui.imgStatus.set_from_stock(Gtk.STOCK_DIALOG_ERROR, icon_size)
            self.ui.imgStatus.set_visible(True)
            self.ui.lblStatus.set_label(str(exception))
            self.ui.lblStatus.set_visible(True)

        elif status == __STATUS_CONNECTING__:
            self.ui.imgStatus.set_from_stock(Gtk.STOCK_CONNECT, icon_size)
            self.ui.imgStatus.set_visible(True)
            self.ui.lblStatus.set_label(_('Trying to connect...'))
            self.ui.lblStatus.set_visible(True)

    def previous_page(self, load_page_callback):
        load_page_callback(firstboot.pages.linkToChef)

    def next_page(self, load_page_callback):

        if self.unlink_ldap == True or self.unlink_ad == True:
            messages = []
            if self.unlink_ldap:
                messages += serverconf.unlink_from_sssd()
            else:
                messages += serverconf.unlink_from_sssd()
            result = len(messages) == 0
            if result:
                server_conf = serverconf.get_server_conf(None)
                auth_conf = server_conf.get_auth_conf()
                content = serverconf.get_json_content()
                if content != None:
                    auth_conf_cached = AuthConf.AuthConf()
                    auth_conf_cached.load_data(content['auth'])
                    server_conf.set_auth_conf(auth_conf_cached)
                else:
                    server_conf.set_auth_conf(AuthConf.AuthConf())

                if self.unlink_ldap:
                    auth_conf.set_auth_type('ldap')
                    #os.remove(__LDAP_FLAG__)
                else:
                    auth_conf.set_auth_type('ad')
                    #os.remove(__AD_FLAG__)

            auth_conf.set_auth_link(False)
            load_page_callback(LinkToServerResultsPage, {
                'result': True,
                'messages': None
            })
            return
        
        if self.ui.radioNone.get_active() or (self.ldap_is_configured or self.ad_is_configured):
            if self.ui.radioNone.get_active():
                server_conf = serverconf.get_server_conf(None)
                server_conf.set_auth_conf(AuthConf.AuthConf())
            self.emit('status-changed', 'linkToServer', True)
            load_page_callback(firstboot.pages.localUsers)
            return

        self.show_status()

        try:
            if len(socket.gethostname()) > 19:
                raise Exception(_("The hostname can't not be longer than 19 characters"))
            server_conf = serverconf.get_server_conf(None)

            load_page_callback(LinkToServerConfEditorPage, {
                'ldap_is_configured': self.ldap_is_configured,
                'auth_method': self.get_auth_method(),
                'ad_is_configured': self.ad_is_configured,
            })

        except serverconf.ServerConfException as e:
            self.show_status(__STATUS_ERROR__, e)

        except Exception as e:
            self.show_status(__STATUS_ERROR__, e)
