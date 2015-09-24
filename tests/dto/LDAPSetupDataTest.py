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
from dto.LDAPSetupData import LDAPSetupData

class LDAPSetupDataTest(unittest.TestCase):
    '''
    Unit test that check getters and setters
    '''


    def runTest(self):
        obj = LDAPSetupData()
        
        obj.set_uri('test_uri')
        self.assertEqual(obj.get_uri(), 'test_uri')
        self.assertEqual(obj.uri, 'test_uri')

        obj.set_base('test_base')
        self.assertEqual(obj.get_base(), 'test_base')
        self.assertEqual(obj.base, 'test_base')

        obj.set_base_group('test_base_group')
        self.assertEqual(obj.get_base_group(), 'test_base_group')
        self.assertEqual(obj.baseGroup, 'test_base_group')

        obj.set_bind_user_dn('test_bind_user_dn')
        self.assertEqual(obj.get_bind_user_dn(), 'test_bind_user_dn')
        self.assertEqual(obj.bindUserDN, 'test_bind_user_dn')

        obj.set_bind_user_pwd('test_bind_user_pwd')
        self.assertEqual(obj.get_bind_user_pwd(), 'test_bind_user_pwd')
        self.assertEqual(obj.bindUserPWD, 'test_bind_user_pwd')

        # Check LDAP connection
        obj.set_uri('ldap://test.ldap.server')
        obj.set_base('ou=users,dc=us,dc=es')
        obj.set_base_group('ou=groups,dc=us,dc=es')
        obj.set_bind_user_dn('cn=admin,dc=us,dc=es')
        obj.set_bind_user_pwd('demoevaos')       
        
        self.assertTrue(obj.test()) 

        obj.set_bind_user_pwd('badpassword')       
        self.assertFalse(obj.test()) 

