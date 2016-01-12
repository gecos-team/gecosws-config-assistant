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

from gecosws_config_assistant.dao.LocalUserDAO import LocalUserDAO
from gecosws_config_assistant.dto.LocalUser import LocalUser


class LocalUserDAOTest(unittest.TestCase):
    '''
    Unit test that check LocalUserDAO class
    '''



    def runTest(self):
        dao = LocalUserDAO()
        
        test_user_name = u'Test user áéíóúüñ'
        test_user_login = 'tstuser'
        test_user_pass = 'tstuserpwd'
        
        # Create a test user 
        newUser = LocalUser()
        newUser.set_login(test_user_login)
        newUser.set_password(test_user_pass)
        newUser.set_name(test_user_name)
        dao.save(newUser)
        
        # Check the user list to verify that the user was created
        userlist = dao.loadAll()
        
        found = False
        for user in userlist:
            if user.get_login() == test_user_login:
                found = True
                self.assertEqual(user.get_name(), test_user_name)
        
        self.assertTrue(found, 'User not found!')

        # Modify the user
        newUser = LocalUser()
        newUser.set_login(test_user_login)
        newUser.set_password(test_user_pass+'_mod')
        newUser.set_name(test_user_name+'_mod')
        dao.save(newUser)        

        # Check the user list to verify that the user was modified
        userlist = dao.loadAll()
        
        found = False
        for user in userlist:
            if user.get_login() == test_user_login:
                found = True
                self.assertEqual(user.get_name(), test_user_name+'_mod')
        
        self.assertTrue(found, 'User not found!')

        # Delete the test user
        newUser = LocalUser()
        newUser.set_login(test_user_login)     
        dao.delete(newUser)   

        # Check the user list to verify that the user was modified
        userlist = dao.loadAll()
        
        found = False
        for user in userlist:
            if user.get_login() == test_user_login:
                found = True
        
        self.assertFalse(found, 'User found!')
