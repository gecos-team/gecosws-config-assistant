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

from dao.NetworkInterfaceDAO import NetworkInterfaceDAO
from dto.NetworkInterface import NetworkInterface


class NetworkInterfaceDAOTest(unittest.TestCase):
    '''
    Unit test that check NetworkInterfaceDAO class
    '''


    def runTest(self):
        dao = NetworkInterfaceDAO()
        
        interfaces = dao.loadAll() 
        self.assertTrue(isinstance(interfaces, list))
        
        print 'Network interfaces: '
        for interface in interfaces:
            self.assertTrue(isinstance(interface, NetworkInterface))
            print 'NAME: ', interface.get_name(), ' IP: ', interface.get_ip_address()
            self.assertNotEqual(interface.get_name(), '')
            self.assertNotEqual(interface.get_ip_address(), '')
            
