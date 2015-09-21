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


class LDAPSetupData(object):
    '''
    DTO object that represents the necessary data to setup LDAP user 
    authentication method.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.uri = ''
        self.base = ''
        self.baseGroup = ''
        self.bindUserDN = ''
        self.bindUserPWD = ''

    def get_uri(self):
        return self.__uri


    def get_base(self):
        return self.__base


    def get_base_group(self):
        return self.__baseGroup


    def get_bind_user_dn(self):
        return self.__bindUserDN


    def get_bind_user_pwd(self):
        return self.__bindUserPWD


    def set_uri(self, value):
        self.__uri = value


    def set_base(self, value):
        self.__base = value


    def set_base_group(self, value):
        self.__baseGroup = value


    def set_bind_user_dn(self, value):
        self.__bindUserDN = value


    def set_bind_user_pwd(self, value):
        self.__bindUserPWD = value

    uri = property(get_uri, set_uri, None, None)
    base = property(get_base, set_base, None, None)
    baseGroup = property(get_base_group, set_base_group, None, None)
    bindUserDN = property(get_bind_user_dn, set_bind_user_dn, None, None)
    bindUserPWD = property(get_bind_user_pwd, set_bind_user_pwd, None, None)




