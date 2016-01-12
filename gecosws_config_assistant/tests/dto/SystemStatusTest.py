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


import unittest
from gecosws_config_assistant.dto.SystemStatus import SystemStatus
from gecosws_config_assistant.dto.NetworkInterface import NetworkInterface
from gecosws_config_assistant.dto.NTPServer import NTPServer
from gecosws_config_assistant.dto.WorkstationData import WorkstationData
from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.dto.LocalUser import LocalUser
from gecosws_config_assistant.dto.LocalUsersAuthMethod import LocalUsersAuthMethod




class SystemStatusTest(unittest.TestCase):
    '''
    Unit test that check getters and setters
    '''


    def runTest(self):
        obj = SystemStatus()

        # Network interfaces
        obj.set_network_interfaces([])
        self.assertEqual(obj.get_network_interfaces(), [])
        self.assertEqual(obj.networkInterfaces, [])

        networkInterfaces = []
        networkInterfaces.append(NetworkInterface())
        obj.set_network_interfaces(networkInterfaces)
        self.assertEqual(obj.networkInterfaces, networkInterfaces)

        
        with self.assertRaises(TypeError):
            obj.set_network_interfaces('wrong data!')

        with self.assertRaises(TypeError):
            obj.set_network_interfaces(None)

        with self.assertRaises(TypeError):
            obj.set_network_interfaces(['wrong data!'])

        
        # Time server
        timeServer = NTPServer()
        obj.set_time_server(timeServer)
        self.assertEqual(obj.get_time_server(), timeServer)
        self.assertEqual(obj.timeServer, timeServer)

        obj.set_time_server(None)
        self.assertEqual(obj.get_time_server(), None)

        with self.assertRaises(TypeError):
            obj.set_time_server('wrong data!')

        # Workstation data
        workstationData = WorkstationData()
        obj.set_workstation_data(workstationData)
        self.assertEqual(obj.get_workstation_data(), workstationData)
        self.assertEqual(obj.workstationData, workstationData)

        obj.set_workstation_data(None)
        self.assertEqual(obj.get_workstation_data(), None)

        with self.assertRaises(TypeError):
            obj.set_workstation_data('wrong data!')


        # GECOS access data
        gecosAccessData = GecosAccessData()
        obj.set_gecos_access_data(gecosAccessData)
        self.assertEqual(obj.get_gecos_access_data(), gecosAccessData)
        self.assertEqual(obj.gecosAccessData, gecosAccessData)

        obj.set_gecos_access_data(None)
        self.assertEqual(obj.get_gecos_access_data(), None)

        with self.assertRaises(TypeError):
            obj.set_gecos_access_data('wrong data!')

        # Local users
        obj.set_local_users([])
        self.assertEqual(obj.get_local_users(), [])
        self.assertEqual(obj.localUsers, [])

        localUsers = []
        localUsers.append(LocalUser())
        obj.set_local_users(localUsers)
        self.assertEqual(obj.localUsers, localUsers)

        
        with self.assertRaises(TypeError):
            obj.set_local_users('wrong data!')

        with self.assertRaises(TypeError):
            obj.set_local_users(None)

        with self.assertRaises(TypeError):
            obj.set_local_users(['wrong data!'])

        # User authentication method
        userAuthenticationMethod = LocalUsersAuthMethod()
        obj.set_user_authentication_method(userAuthenticationMethod)
        self.assertEqual(obj.get_user_authentication_method(), userAuthenticationMethod)
        self.assertEqual(obj.userAuthenticationMethod, userAuthenticationMethod)

        obj.set_user_authentication_method(None)
        self.assertEqual(obj.get_user_authentication_method(), None)

        with self.assertRaises(TypeError):
            obj.set_user_authentication_method('wrong data!')



