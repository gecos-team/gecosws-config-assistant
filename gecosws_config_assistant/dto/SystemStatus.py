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

from gecosws_config_assistant.dto.NetworkInterface import NetworkInterface
from gecosws_config_assistant.dto.NTPServer import NTPServer
from gecosws_config_assistant.dto.WorkstationData import WorkstationData
from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.dto.LocalUser import LocalUser
from gecosws_config_assistant.dto.UserAuthenticationMethod import (
    UserAuthenticationMethod)


class SystemStatus(object):
    '''
    DTO object that represents the current status of the system.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.networkInterfaces = []
        self.timeServer = None
        self.workstationData = None
        self.gecosAccessData = None
        self.localUsers = []
        self.userAuthenticationMethod = None
        self.cgaVersion = None

    def get_cga_version(self):
        ''' Getter CGA version '''

        return self.__cgaVersion

    def set_cga_version(self, value):
        ''' Setter CGA version '''

        self.__cgaVersion = value

    def get_network_interfaces(self):
        ''' Getter network interfaces '''

        return self.__networkInterfaces

    def get_time_server(self):
        ''' Getter time server '''

        return self.__timeServer

    def get_workstation_data(self):
        ''' Getter workstation data '''

        return self.__workstationData

    def get_gecos_access_data(self):
        ''' Getter gecos access data '''

        return self.__gecosAccessData

    def get_local_users(self):
        ''' Getter local users '''

        return self.__localUsers

    def get_user_authentication_method(self):
        ''' Getter user authentication method '''

        return self.__userAuthenticationMethod

    def set_network_interfaces(self, value):
        ''' Setter network interfaces '''

        if not isinstance(value, list):
            raise TypeError('"Network interfaces" must be a list')

        for item in value:
            if not isinstance(item, NetworkInterface):
                raise TypeError(
                    '"Network interfaces" must be a list of NetworkInterface'
                )

        self.__networkInterfaces = value

    def set_time_server(self, value):
        ''' Setter time server '''

        if value is not None and not isinstance(value, NTPServer):
            raise TypeError(
                '"Time server" must be an object of class NTPServer'
            )
        self.__timeServer = value

    def set_workstation_data(self, value):
        ''' Setter workstation data '''

        if value is not None and not isinstance(value, WorkstationData):
            raise TypeError(
                '"Workstation data" must be an object of class WorkstationData'
            )
        self.__workstationData = value

    def set_gecos_access_data(self, value):
        ''' Setter gecos access data '''

        if value is not None and not isinstance(value, GecosAccessData):
            raise TypeError(
                '"GECOS access data" must be an object of ' +
                'class GecosAccessData'
            )
        self.__gecosAccessData = value

    def set_local_users(self, value):
        ''' Setter local users '''

        if not isinstance(value, list):
            raise TypeError('"Local users" must be a list')

        for item in value:
            if not isinstance(item, LocalUser):
                raise TypeError('"Local users" must be a list of LocalUser')

        self.__localUsers = value

    def set_user_authentication_method(self, value):
        ''' Setter user authentication method '''

        if (
            value is not None and
            not isinstance(value, UserAuthenticationMethod)
        ):
            raise TypeError(
                '"user authentication method" data must be an object ' +
                'of class UserAuthenticationMethod'
            )
        self.__userAuthenticationMethod = value


    networkInterfaces = property(
        get_network_interfaces,
        set_network_interfaces,
        None,
        None)
    timeServer = property(
        get_time_server,
        set_time_server,
        None,
        None)
    workstationData = property(
        get_workstation_data,
        set_workstation_data,
        None,
        None)
    gecosAccessData = property(
        get_gecos_access_data,
        set_gecos_access_data,
        None,
        None)
    localUsers = property(
        get_local_users,
        set_local_users,
        None,
        None)
    userAuthenticationMethod = property(
        get_user_authentication_method,
        set_user_authentication_method,
        None,
        None)
    cgaVersion = property(
        get_cga_version,
        set_cga_version,
        None,
        None)
