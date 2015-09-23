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

from dao.LocalUserDAO import LocalUserDAO
from dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO
from dto.LocalUser import LocalUser
from dto.LocalUsersAuthMethod import LocalUsersAuthMethod
from dto.UserAuthenticationMethod import UserAuthenticationMethod
from dto.LDAPAuthMethod import LDAPAuthMethod
from dto.ADAuthMethod import ADAuthMethod
from dto.ADSetupData import ADSetupData

import PAM

pam_password = 'none'

def pam_conv(auth, query_list, userData):
    global pam_password
    return [(pam_password,0)]

class UserAuthenticationMethodDAOTest(unittest.TestCase):
    '''
    Unit test that check UserAuthenticationMethodDAO class
    '''

    def check_pam_login(self, user, password):
        global pam_password
        pam_password = password
        
        auth = PAM.pam()
        auth.start('sssd')
        auth.set_item(PAM.PAM_USER, user)
        auth.set_item(PAM.PAM_CONV, pam_conv)
        try:
            auth.authenticate()
            auth.acct_mgmt()
        except PAM.error, resp:
            print 'Bad autentication! (%s)' % resp
            return False
        except:
            print 'Internal error'
            return False
        else:
            return True


    def runTest(self):
        localUserDao = LocalUserDAO()
        authMethodDao = UserAuthenticationMethodDAO()
        
        test_user_name = 'Test user'
        test_user_login = 'tstuser'
        test_user_pass = 'tstuserpwd'
        
        print 'Create a test user'
        tstuser = LocalUser()
        tstuser.set_login(test_user_login)
        tstuser.set_password(test_user_pass)
        tstuser.set_name(test_user_name)
        localUserDao.save(tstuser)
        
        print 'Check default authentication method'
        # By default the authentication method must be "local users"
        method = authMethodDao.load()
        self.assertTrue(isinstance(method, LocalUsersAuthMethod))
        
        print 'Check a local user login'
        self.assertTrue(self.check_pam_login('tstuser', 'tstuserpwd'))

        print 'Set the authentication method to Active Directory'
        method = ADAuthMethod()
        data = ADSetupData()
        
        # Data of an Active Directory server used for tests 
        data.set_domain('evaos.local')
        data.set_workgroup('evaos')
        data.set_ad_administrator_user('Administrador')
        data.set_ad_administrator_pass('Evaos.2014')
        
        method.set_data(data)
        self.assertTrue(authMethodDao.save(method))
        
        # Check if the changes has been done properly
        currentMethod = authMethodDao.load()
        self.assertEqual(currentMethod.get_name(), method.get_name())
        self.assertEqual(currentMethod.get_data().get_domain(), method.get_data().get_domain())
        self.assertEqual(currentMethod.get_data().get_workgroup(), method.get_data().get_workgroup())

        print 'Check a active directory test user login'
        self.assertTrue(self.check_pam_login('amacias', 'Evaos.2014'))   
        
             
        print 'Set the authentication method back to local users'
        self.assertTrue(authMethodDao.delete(method))

        currentMethod = authMethodDao.load()
        self.assertTrue(isinstance(currentMethod, LocalUsersAuthMethod))

        print 'Delete the test user'
        localUserDao.delete(tstuser)   

      