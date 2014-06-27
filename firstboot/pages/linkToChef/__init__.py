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

import firstboot.pages
import LinkToChefConfEditorPage
from firstboot_lib import PageWindow
from firstboot import serverconf, FirstbootWindow
from firstboot.serverconf import GCCConf, ChefConf

import requests
import json
import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')


__REQUIRED__ = True

__TITLE__ = _('Link workstation to GECOS Control Center')

__STATUS_TEST_PASSED__ = 0
__STATUS_CONFIG_CHANGED__ = 1
__STATUS_CONNECTING__ = 2
__STATUS_ERROR__ = 3

__GCC_FLAG__ = '/etc/gcc.control'
__CHEF_FLAG__ = '/etc/chef.control'


def get_page(main_window):

    page = LinkToChefPage(main_window)
    return page


class LinkToChefPage(PageWindow.PageWindow):
    __gtype_name__ = "LinkToChefPage"
    
    def load_page(self, params=None):
        self.gcc_is_configured = serverconf.gcc_is_configured()
        server_conf = serverconf.get_server_conf(None)
        if server_conf.get_gcc_conf().get_gcc_link() and not self.gcc_is_configured:
            self.emit('page-changed',LinkToChefConfEditorPage, {})



    def finish_initializing(self):
        self.gcc_is_configured = serverconf.gcc_is_configured()
        server_conf = serverconf.get_server_conf(None)
        self.show_status()
        self.ui.chkUnlinkChef.set_visible(self.gcc_is_configured)
        self.ui.chkLinkChef.set_visible(not self.gcc_is_configured)


    def translate(self):
        desc = _('When a workstation is linked to a Control Center can be \
easily managed remotely.\n\n')

        self.ui.lblDescription.set_text(desc)
        self.ui.chkUnlinkChef.set_label(_('Unlink from Control Center'))
        self.ui.chkLinkChef.set_label(_('Link to Control Center server?'))

    def on_chkUnlinkChef_toggle(self, button):
        #self.main_window.btnNext.set_sensitive(button.get_active())
        pass


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
        load_page_callback(firstboot.pages.pcLabel)

    def next_page(self, load_page_callback):
        if (self.ui.chkLinkChef.get_visible() and not self.ui.chkLinkChef.get_active()) or \
            (self.gcc_is_configured and not self.ui.chkUnlinkChef.get_active()):
            self.emit('status-changed', 'linkToChef', True)
            load_page_callback(firstboot.pages.linkToServer)
            return
        self.show_status()
        try:
            server_conf = None

            if not self.gcc_is_configured:
                load_page_callback(LinkToChefConfEditorPage)

            elif self.ui.chkUnlinkChef.get_active():
                server_conf = serverconf.get_server_conf(None)
                ## TODO Implement unlink GCC an Chef into serverconf Class
                gcc_flag = open(__GCC_FLAG__, 'r')
                content = gcc_flag.read()
                gcc_flag.close()
                gcc_flag_json = json.loads(content)
                server_conf.get_gcc_conf().set_uri_gcc(gcc_flag_json['uri_gcc'])
                server_conf.get_gcc_conf().set_gcc_nodename(gcc_flag_json['gcc_nodename'])
                server_conf.get_gcc_conf().set_gcc_link(False)
                server_conf.get_gcc_conf().set_run(True)
                json_server = serverconf.validate_credentials(gcc_flag_json['uri_gcc']+'/auth/config/')
                json_server = json.loads(json_server)
                pem = json_server['chef']['chef_validation']
                server_conf.get_gcc_conf().set_gcc_username(json_server['gcc']['gcc_username'])
                serverconf.create_pem(pem)
 
                chef_flag = open(__CHEF_FLAG__, 'r')
                content = chef_flag.read()
                chef_flag.close()
                chef_flag_json = json.loads(content)
                server_conf.get_chef_conf().set_url(chef_flag_json['chef_server_url'])
                server_conf.get_chef_conf().set_node_name(chef_flag_json['chef_node_name'])
                server_conf.get_chef_conf().set_admin_name(json_server['gcc']['gcc_username'])
                server_conf.get_chef_conf().set_chef_link(False)
                password = serverconf.ACTUAL_USER[1]
                if password == None:
                   raise Exception(_('Error in user and password'))
                messages = []
                messages += serverconf.unlink_from_gcc(password)
                messages += serverconf.unlink_from_chef()
                result = len(messages) == 0
                if result:
                    content = serverconf.get_json_content()
                    if content != None:
                        gcc_conf_cached = GCCConf.GCCConf()
                        gcc_conf_cached.load_data(content['gcc'])
                        chef_conf_cached = ChefConf.ChefConf()
                        chef_conf_cached.load_data(content['chef'])
                        server_conf.set_chef_conf(chef_conf_cached)
                        server_conf.set_gcc_conf(gcc_conf_cached)
                    else:
                        server_conf.set_chef_conf(ChefConf.ChefConf())
                        server_conf.set_gcc_conf(GCCConf.GCCConf())
                load_page_callback(LinkToChefResultsPage, {
                    'result': True,
                    'messages': messages
                })

        except serverconf.ServerConfException as e:
            self.show_status(__STATUS_ERROR__, e)

        except Exception as e:
            self.show_status(__STATUS_ERROR__, e)
