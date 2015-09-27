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

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class ServerConf():

    # Version of the configuration JSON file

    def __init__(self):
        self._data = {}
        self.VERSION = '0.2.0'
        self._data['gem_repo'] = 'http://rubygems.org'
        self._data['version'] = self.VERSION
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
            if v != self.VERSION:
                print 'WARNING: ServerConf and AUTOCONFIG_JSON version mismatch!'
        except KeyError as e:
            print msg % ('version',)
        try:
            self.set_organization(conf['organization'])
        except KeyError as e:
            print msg % ('organization',)

        try:
            self.set_notes(conf['notes'])
        except KeyError as e:
            print msg % ('notes',)

        try:
            self.set_gem_repo(conf['gem_repo'])
        except KeyError as e:
            print msg % ('gem_repo',)

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


    def set_gem_repo(self, repo):
        self._data['gem_repo'] = repo
        return self

    def get_gem_repo(self):
        return self._data['gem_repo'].encode('utf-8')

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

    def get_notes(self):
        return self._data['notes'].encode('utf-8')

    def set_notes(self, notes):
        self._data['notes'] = notes
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

    def set_auth_conf(self, auth_conf):
        self._auth_conf = auth_conf
        return self

    def set_chef_conf(self, chef_conf):
        self._chef_conf = chef_conf
        return self

    def set_ntp_conf(self, ntp_conf):
        self._ntp_conf = ntp_conf
        return self

    def set_gcc_conf(self, gcc_conf):
        self._gcc_conf = gcc_conf
        return gcc_conf

    def set_users_conf(self, user_conf):
        self._users_conf = user_conf
        return self
