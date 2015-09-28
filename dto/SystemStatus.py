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

from NetworkInterface import NetworkInterface
from NTPServer import NTPServer
from WorkstationData import WorkstationData
from GecosAccessData import GecosAccessData
from LocalUser import LocalUser
from UserAuthenticationMethod import UserAuthenticationMethod


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

    def get_network_interfaces(self):
        return self.__networkInterfaces


    def get_time_server(self):
        return self.__timeServer


    def get_workstation_data(self):
        return self.__workstationData


    def get_gecos_access_data(self):
        return self.__gecosAccessData


    def get_local_users(self):
        return self.__localUsers


    def get_user_authentication_method(self):
        return self.__userAuthenticationMethod


    def set_network_interfaces(self, value):
        if not isinstance(value, list):
            raise TypeError('"Network interfaces" must be a list')
        
        for item in value:
            if not isinstance(item, NetworkInterface):
                raise TypeError('"Network interfaces" must be a list of NetworkInterface')
        
        self.__networkInterfaces = value


    def set_time_server(self, value):
        if value is not None and not isinstance(value, NTPServer):
            raise TypeError('"Time server" must be an object of class NTPServer')        
        self.__timeServer = value


    def set_workstation_data(self, value):
        if value is not None and not isinstance(value, WorkstationData):
            raise TypeError('"Workstation data" must be an object of class WorkstationData')        
        self.__workstationData = value


    def set_gecos_access_data(self, value):
        if value is not None and not isinstance(value, GecosAccessData):
            raise TypeError('"GECOS access data" must be an object of class GecosAccessData')        
        self.__gecosAccessData = value


    def set_local_users(self, value):
        if not isinstance(value, list):
            raise TypeError('"Local users" must be a list')
        
        for item in value:
            if not isinstance(item, LocalUser):
                raise TypeError('"Local users" must be a list of LocalUser')
                    
        self.__localUsers = value


    def set_user_authentication_method(self, value):
        if value is not None and not isinstance(value, UserAuthenticationMethod):
            raise TypeError('"user authentication method" data must be an object of class UserAuthenticationMethod')        
        self.__userAuthenticationMethod = value

    networkInterfaces = property(get_network_interfaces, set_network_interfaces, None, None)
    timeServer = property(get_time_server, set_time_server, None, None)
    workstationData = property(get_workstation_data, set_workstation_data, None, None)
    gecosAccessData = property(get_gecos_access_data, set_gecos_access_data, None, None)
    localUsers = property(get_local_users, set_local_users, None, None)
    userAuthenticationMethod = property(get_user_authentication_method, set_user_authentication_method, None, None)
        





