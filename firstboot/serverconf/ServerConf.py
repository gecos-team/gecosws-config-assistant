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


import firstboot.serverconf
from ChefConf import ChefConf
from GCCConf import GCCConf
from AuthConf import AuthConf
from DateSyncConf import DateSyncConf
from UsersConf import UsersConf


class ServerConf():

    # Version of the configuration JSON file
    VERSION = '0.2.0'

    def __init__(self):
        self._data = {}
        self._data['version'] = ServerConf.VERSION
        self._data['organization'] = ''
        self._chef_conf = ChefConf()
        self._gcc_conf = GCCConf()
        self._auth_conf = AuthConf()
        self._ntp_conf = DateSyncConf()
        self._users_conf = UsersConf()

    def load_data(self, conf):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        try:
            v = conf['version']
            if v != ServerConf.VERSION:
                print 'WARNING: ServerConf and AUTOCONFIG_JSON version mismatch!'
        except KeyError as e:
            print msg % ('version',)
        try:
            self.set_organization(conf['organization'])
        except KeyError as e:
            print msg % ('organization',)
        try:
            self._chef_conf.load_data(conf['chef'])
        except KeyError as e:
            print msg % ('chef',)
        try:
            self._gcc_conf.load_data(conf['gcc'])
        except KeyError as e:
            print msg % ('gcc',)
        try:
            self._auth_conf.load_data(conf['auth'])
        except KeyError as e:
            print msg % ('auth',)
        try:
            self._ntp_conf.load_data(conf['uri_ntp'])
        except KeyError as e:
            print msg % ('ntp',)

    def validate(self):
        valid = len(self._data['version']) > 0 \
            and self._chef_conf.validate() \
            and self._auth_conf.validate() \
            and self._ntp_conf.validate() \
            and self._gcc_conf.validate()
        return valid

    def get_version(self):
        return self._data['version'].encode('utf-8')

    def set_version(self, version):
        self._data['version'] = version
        return self

    def get_organization(self):
        return self._data['organization'].encode('utf-8')

    def set_organization(self, organization):
        self._data['organization'] = organization
        return self

    def get_auth_conf(self):
        return self._auth_conf

    def get_chef_conf(self):
        return self._chef_conf

    def get_ntp_conf(self):
        return self._ntp_conf

    def get_gcc_conf(self):
        return self._gcc_conf

    def get_users_conf(self):
        return self._users_conf


