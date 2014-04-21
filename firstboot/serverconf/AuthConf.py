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

import firstboot.validation as validation
from LdapConf import LdapConf
from ActiveDirectoryConf import ActiveDirectoryConf
from LdapConf import LdapConf

class AuthConf():

    def __init__(self):
        self._data = {}
        self._data['auth_type'] = ''
        self._data['auth_properties'] = ''
        self._data['auth_link'] = True
        self._ad_conf = ActiveDirectoryConf()
        self._ldap_conf = LdapConf()

    def load_data(self, conf):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        try:
            self.set_auth_type(conf['auth_type'].lower())
        except KeyError as e:
            print msg % ('auth_type',)
        try:
            if conf['auth_type'].lower() == 'ldap':
                self._ldap_conf.load_data(conf['auth_properties'])
            else:
                self._ad_conf.load_data(conf['auth_properties'])

        except KeyError as e:
            print msg % ('auth_properties',)

    def validate(self):
        valid = validation.is_auth_type(self._data['auth_type']) 
        return valid

    def get_auth_type(self):
        return self._data['auth_type'].encode('utf-8')

    def set_auth_type(self, auth_type):
        self._data['auth_type'] = auth_type
        return self

    def set_auth_link(self, auth_link):
        self._data['auth_link'] = auth_link
        return self

    def get_auth_link(self):
        return self._data['auth_link']

    def get_auth_properties(self):
        if self._data['auth_type'] == 'ldap':
            return self._ldap_conf
        else:
            return self._ad_conf

