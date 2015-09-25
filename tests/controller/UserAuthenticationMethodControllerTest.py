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

from controller.UserAuthenticationMethodController import UserAuthenticationMethodController
from view.ViewMocks import ViewMock
from dto.ADAuthMethod import ADAuthMethod
from dto.ADSetupData import ADSetupData
from dto.LDAPAuthMethod import LDAPAuthMethod
from dto.LDAPSetupData import LDAPSetupData
from dto.LocalUsersAuthMethod import LocalUsersAuthMethod



class UserAuthenticationMethodControllerTest(unittest.TestCase):
    '''
    Unit test that check UserAuthenticationMethodController class
    '''


    def runTest(self):
        print "Create the controller"
        controller = UserAuthenticationMethodController()

        ldapMethod = LDAPAuthMethod()
        ldapData = LDAPSetupData()
        ldapData.set_uri('ldap://test.ldap.server')
        ldapData.set_base('ou=users,dc=us,dc=es')
        ldapData.set_base_group('ou=groups,dc=us,dc=es')
        ldapData.set_bind_user_dn('cn=admin,dc=us,dc=es')
        ldapData.set_bind_user_pwd('demoevaos')            
        ldapMethod.set_data(ldapData)
        
        adMethod = ADAuthMethod()
        adData = ADSetupData()
        adData.set_domain('evaos.local')
        adData.set_workgroup('evaos')
        adData.set_ad_administrator_user('Administrador')
        adData.set_ad_administrator_pass('Evaos.2014')        
        adMethod.set_data(adData)

        internalMethod = LocalUsersAuthMethod()
        
        print "Show the window"
        mainWindow = ViewMock()
        controller.show(mainWindow)

        print "Simulate Internal to LDAP setup"
        controller.view.set_data(ldapMethod)
        self.assertTrue(controller.accept())

        print "Simulate LDAP to Internal setup"
        controller.view.set_data(internalMethod)
        self.assertTrue(controller.accept())

        print "Simulate Internal to AD setup"
        controller.view.set_data(adMethod)
        self.assertTrue(controller.accept())
        
        print "Simulate AD to LDAP setup"
        controller.view.set_data(ldapMethod)
        self.assertTrue(controller.accept())

        print "Simulate LDAP to AD setup"
        controller.view.set_data(adMethod)
        self.assertTrue(controller.accept())

        print "Simulate AD to Internal setup"
        controller.view.set_data(internalMethod)
        self.assertTrue(controller.accept())

        print "End ;)"
