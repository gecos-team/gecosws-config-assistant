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


class ADSetupData(object):
    '''
    DTO object that represents Active Directory authentication method data.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.domain = ''
        self.workgroup = ''

    def get_domain(self):
        return self.__domain


    def get_workgroup(self):
        return self.__workgroup


    def set_domain(self, value):
        self.__domain = value


    def set_workgroup(self, value):
        self.__workgroup = value

    domain = property(get_domain, set_domain, None, None)
    workgroup = property(get_workgroup, set_workgroup, None, None)





