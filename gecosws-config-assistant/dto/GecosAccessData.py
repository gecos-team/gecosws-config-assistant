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


class GecosAccessData(object):
    '''
    DTO object that represents the data to access a GECOS CC.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.url = ''
        self.login = ''
        self.password = ''

    def get_url(self):
        return self.__url


    def get_login(self):
        return self.__login


    def get_password(self):
        return self.__password


    def set_url(self, value):
        self.__url = value


    def set_login(self, value):
        self.__login = value


    def set_password(self, value):
        self.__password = value

    url = property(get_url, set_url, None, None)
    login = property(get_login, set_login, None, None)
    password = property(get_password, set_password, None, None)





