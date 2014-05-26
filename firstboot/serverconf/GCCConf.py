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


class GCCConf():

    def __init__(self):
        self._data = {}
        self._data['uri_gcc'] = ''
        self._data['gcc_username'] = ''
        self._data['gcc_nodename'] = ''
        self._data['gcc_link'] = False
        self._data['gcc_pwd_user'] = ''
        self._data['selected_ou'] = ''
        self._data['run'] = True
        self._data['ou_username'] = []

    def load_data(self, conf):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        try:
            self.set_uri_gcc(conf['uri_gcc'])
        except KeyError as e:
            print msg % ('uri_gcc',)
        try:
            self.set_gcc_username(conf['gcc_username'])
        except KeyError as e:
            print msg % ('gcc_username',)
        try:
            self.set_ou_username(conf['ou_username'])
        except KeyError as e:
            print msg % ('ou_username',)
        try:
            self.set_gcc_link(conf['gcc_link'])
        except KeyError as e:
            print msg % ('gcc_link',)

    def validate(self):
        valid = self._data['run'] == False or (validation.is_url(self._data['uri_gcc']) and self._data['gcc_username'] != '' and self._data['gcc_nodename'] != '' and self._data['gcc_link'] != None and self._data['gcc_pwd_user'] != '' and self._data['ou_username'] != None and self._data['selected_ou'] != '')
        return valid

    def get_uri_gcc(self):
        return self._data['uri_gcc'].encode('utf-8')

    def set_uri_gcc(self, uri):
        self._data['uri_gcc'] = uri
        return self

    def get_gcc_username(self):
        return self._data['gcc_username'].encode('utf-8')

    def set_gcc_username(self, gcc_username):
        self._data['gcc_username'] = gcc_username
        return self

    def get_gcc_nodename(self):
        return self._data['gcc_nodename'].encode('utf-8')

    def set_gcc_nodename(self, gcc_nodename):
        self._data['gcc_nodename'] = gcc_nodename
        return self

    def set_selected_ou(self, selected_ou):
        self._data['selected_ou'] = selected_ou
        return self

    def get_selected_ou(self):
        return self._data['selected_ou']

    def get_gcc_link(self):
        return self._data['gcc_link']

    def set_gcc_link(self, gcc_link):
        self._data['gcc_link'] = gcc_link
        return self

    def get_gcc_pwd_user(self):
        return self._data['gcc_pwd_user'].encode('utf-8')

    def set_gcc_pwd_user(self, gcc_pwd_user):
        self._data['gcc_pwd_user'] = gcc_pwd_user
        return self

    def get_ou_username(self):
        return self._data['ou_username']

    def set_run(self, run_action):
        self._data['run'] = run_action
        return self

    def get_run(self):
        return self._data['run']
    
    def add_ou_username(self, ou_username):
        self._data['ou_username'].append(ou_username)
        return self

    def set_ou_username(self, ou_username):
        self._data['ou_username'] = ou_username
        return self
