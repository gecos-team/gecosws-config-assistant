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
        self._data['user'] = ''
        self._data['password'] = ''

    def get_actiontorun(self):
        return self._data['actiontorun'].encode('utf-8')
    
    def set_actiontorun(self, fqdn):
        self._data['actiontorun'] = actiontorun
        return self

    def get_groups(self):
        return self._data['groups'].encode('utf-8')

    def add_groups(self, group):
        self._data['groups'].append = group
        return self

    def remove_groups(self, group):
        self._data['groups'].remove(group)
        return self

    def get_user(self):
        return self._data['user']

    def set_user(self, user):
        self._data['user'] = user
        return self

    def get_passwd(self):
        return self._data['passwd']

    def set_passwd(self, passwd):
        self._data['passwd'] = passwd
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

    def __str__(self):
        return str(self._data)
