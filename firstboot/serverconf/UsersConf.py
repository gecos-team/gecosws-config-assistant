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

__author__ = "David Amian Valle <damian@emergya.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

import firstboot.validation as validation

class Users():
    def __init__(self):
        self._data = {}
        self._data['actiontorun'] = ''
        self._data['groups'] =  []
        self._data['name'] = ''
        self._data['user'] = ''
        self._data['password'] = ''

    def get_actiontorun(self):
        return self._data['actiontorun'].encode('utf-8')
    
    def set_actiontorun(self, actiontorun):
        self._data['actiontorun'] = actiontorun
        return self

    def get_groups(self):
        return self._data['groups']

    def add_group(self, group):
        self._data['groups'].append(group)
        return self
    
    def add_groups(self, groups):
        [self.add_group(group) for group in groups]
        return self

    def remove_group(self, group):
        self._data['groups'].remove(group)
        return self

    def get_name(self):
        return self._data['name']

    def set_name(self, name):
        self._data['name'] = name
        return self

    def get_user(self):
        return self._data['user']

    def set_user(self, user):
        self._data['user'] = user
        return self

    def get_password(self):
        return self._data['password']

    def set_password(self, password):
        self._data['password'] = password
        return self
    
    def get_deletehome(self):
        return self._data['deletehome']

    def set_deletehome(self, deletehome):
        self._data['deletehome'] = deletehome
        return self

    def __str__(self):
        return str(self._data)


class UsersConf():

    def __init__(self):
        self._data = {}
        self._data['users_list'] = []

    def validate(self):
        return True

    def get_users_list(self):
        return self._data['users_list']

    def add_user_to_list(self, user):
        return self._data['users_list'].append(user)
    
    def add_users_to_list(self, users):
        return [self.add_user_to_list(user) for user in users]
    
    def clear(self):
        self._data['users_list'] = []
        return self
    
    def __str__(self):
        return str(self._data)
