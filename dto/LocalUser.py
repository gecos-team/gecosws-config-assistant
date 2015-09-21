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

__author__ = "Abraham Macias Paredes <amacias@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


class LocalUser(object):
    '''
    DTO object that represents a local user account.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.login = ''
        self.password = ''
        self.name = ''

    def get_login(self):
        return self.__login


    def get_password(self):
        return self.__password


    def get_name(self):
        return self.__name


    def set_login(self, value):
        self.__login = value


    def set_password(self, value):
        self.__password = value


    def set_name(self, value):
        self.__name = value

    login = property(get_login, set_login, None, None)
    password = property(get_password, set_password, None, None)
    name = property(get_name, set_name, None, None)




