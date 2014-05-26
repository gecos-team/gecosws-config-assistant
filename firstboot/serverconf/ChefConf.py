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

import firstboot.validation as validation


class ChefConf():

    def __init__(self):
        self._data = {}
        self._data['chef_server_uri'] = ''
        self._data['chef_validation'] = ''
        self._data['chef_link'] = False
        self._data['chef_link_existing'] = False


    def load_data(self, conf):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        try:
            self.set_url(conf['chef_server_uri'])
        except KeyError as e:
            print msg % ('chef_server_uri',)
        try:
            self.set_pem(conf['chef_validation'])
        except KeyError as e:
            print msg % ('chef_validation',)
        try:
            self.set_chef_link(conf['chef_link'])
        except KeyError as e:
            print msg % ('chef_link',)

    def validate(self):
        valid = validation.is_url(self._data['chef_server_uri']) and self._data['chef_validation'] != '' and self._data['chef_link'] != None and self._data['chef_link_existing'] != None
        return valid

    def get_url(self):
        return self._data['chef_server_uri'].encode('utf-8')

    def set_url(self, url):
        self._data['chef_server_uri'] = url
        return self

    def get_pem(self):
        return self._data['chef_validation'].encode('utf-8')

    def set_pem(self, pem):
        self._data['chef_validation'] = pem
        return self


    # --- Next fields are not present in the JSON file but are
    # setted on runtime by Firstboot ---
    def set_chef_link_existing(self, link_existing):
        self._data['chef_link_existing'] = link_existing
        return self

    def get_chef_link_existing(self):
        return self._data['chef_link_existing']

    def set_chef_link(self, chef_link):
        self._data['chef_link'] = chef_link
        return self

    def get_chef_link(self):
        return self._data['chef_link']
        
    def get_node_name(self):
        if not 'node_name' in self._data:
            self._data['node_name'] = ''
        return self._data['node_name'].encode('utf-8')

    def set_node_name(self, node_name):
        self._data['node_name'] = node_name
        return self

    def get_admin_name(self):
        if not 'chef_admin_name' in self._data:
            self._data['chef_admin_name'] = ''
        return self._data['chef_admin_name'].encode('utf-8')

    def set_admin_name(self, admin_name):
        self._data['chef_admin_name'] = admin_name
        return self
