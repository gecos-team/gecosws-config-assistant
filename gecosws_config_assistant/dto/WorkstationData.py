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
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"


class WorkstationData(object):
    '''
    DTO object that represents a the data of a GECOS CC associated workstation.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = ''
        self.ou = ''
        self.node_name = ''

    def get_node_name(self):
        ''' Getter node name '''

        return self.__node_name

    def set_node_name(self, value):
        ''' Setter node name '''
        if isinstance(value, bytes):
            value = str(value, "utf-8")
        self.__node_name = value

    def get_name(self):
        ''' Getter name workstation '''

        return self.__name

    def get_ou(self):
        ''' Getter OU belong to workstation '''

        return self.__ou

    def set_name(self, value):
        ''' Setter name workstation '''
        if isinstance(value, bytes):
            value = str(value, "utf-8")
        self.__name = value

    def set_ou(self, value):
        ''' Setter OU '''
        if isinstance(value, bytes):
            value = str(value, "utf-8")
        self.__ou = value 


    name = property(
        get_name,
        set_name,
        None,
        None)
    ou = property(
        get_ou,
        set_ou,
        None,
        None)
    node_name = property(
        get_node_name,
        set_node_name,
        None,
        None)
