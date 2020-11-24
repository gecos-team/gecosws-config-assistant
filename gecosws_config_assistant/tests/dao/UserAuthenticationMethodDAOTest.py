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
from gecosws_config_assistant.dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO
from gecosws_config_assistant.dto.LocalUser import LocalUser
from gecosws_config_assistant.dto.LocalUsersAuthMethod import LocalUsersAuthMethod
from gecosws_config_assistant.dto.LDAPAuthMethod import LDAPAuthMethod
from gecosws_config_assistant.dto.LDAPSetupData import LDAPSetupData
from gecosws_config_assistant.dto.ADAuthMethod import ADAuthMethod
from gecosws_config_assistant.dto.ADSetupData import ADSetupData

from gecosws_config_assistant.dao.NetworkInterfaceDAO import NetworkInterfaceDAO


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
        except PAM.error as resp:
            print ('Bad autentication! (%s)' % resp)
            return False
        except:
            print ('Internal error')
            return False
        else:
            return True


    def runTest(self):
        localUserDao = LocalUserDAO()
        authMethodDao = UserAuthenticationMethodDAO()
        
        # For Active Directory the hostname must be valid
        networkInterfaceDAO = NetworkInterfaceDAO()
        originalHostname = networkInterfaceDAO.get_hostname()
        self.assertIsNotNone(originalHostname)
        print ('Original host name is: %s'%(originalHostname))
        
        self.assertTrue(networkInterfaceDAO.set_hostname('mycomputer'))
        self.assertEqual(networkInterfaceDAO.get_hostname(), 'mycomputer')
        
        
        adMethod = ADAuthMethod()
        adData = ADSetupData()
        
        # Data of an Active Directory server used for tests 
        adData.set_domain('evaos.local')
        adData.set_workgroup('evaos')
        adData.set_ad_administrator_user('Administrador')
        adData.set_ad_administrator_pass('Evaos.2014')
        
        adMethod.set_data(adData)        
        
        # Data of a LDAP server used for tests
        ldapMethod = LDAPAuthMethod()
        ldapData = LDAPSetupData()
        
        # Data of a LDAP server used for tests 
        ldapData.set_uri('ldap://test.ldap.server')
        ldapData.set_base('ou=users,dc=example,dc=com')
        ldapData.set_base_group('ou=groups,dc=example,dc=com')
        ldapData.set_bind_user_dn('cn=admin,dc=example,dc=com')
        ldapData.set_bind_user_pwd('demoevaos')
        
        ldapMethod.set_data(ldapData)        
        
        # Test user data
        test_user_name = 'Test user'
        test_user_login = 'tstuser'
        test_user_pass = 'tstuserpwd'
        
        print ('Create a test user')
        tstuser = LocalUser()
        tstuser.set_login(test_user_login)
        tstuser.set_password(test_user_pass)
        tstuser.set_name(test_user_name)
        localUserDao.save(tstuser)
        
        print ('Ensure that the default authentication method is "LocalUsers"')
        method = authMethodDao.load()
        if isinstance(method, ADAuthMethod):
            self.assertTrue(authMethodDao.delete(adMethod))
        elif isinstance(method, LDAPAuthMethod):
            self.assertTrue(authMethodDao.delete(ldapMethod))
        
        print ('Check default authentication method')
        # By default the authentication method must be "local users"
        method = authMethodDao.load()
        self.assertTrue(isinstance(method, LocalUsersAuthMethod))
        
        print ('Check a local user login')
        self.assertTrue(self.check_pam_login('tstuser', 'tstuserpwd'))
        self.assertFalse(self.check_pam_login('tstuser', 'badpassword!'))

        print ('Set the authentication method to Active Directory')
        self.assertTrue(authMethodDao.save(adMethod))
        
        # Check if the changes has been done properly
        currentMethod = authMethodDao.load()
        self.assertEqual(currentMethod.get_name(), adMethod.get_name())
        self.assertEqual(currentMethod.get_data().get_domain(), adMethod.get_data().get_domain())
        self.assertEqual(currentMethod.get_data().get_workgroup(), adMethod.get_data().get_workgroup())

        print ('Check a active directory test user login')
        self.assertTrue(self.check_pam_login('amacias', 'Evaos.2014'))   
        
             
        print ('Set the authentication method back to local users')
        self.assertTrue(authMethodDao.delete(adMethod))

        currentMethod = authMethodDao.load()
        self.assertTrue(isinstance(currentMethod, LocalUsersAuthMethod))


        print ('Set the authentication method to Active Directory (Specific setup)')
        adData.set_domain('SPECIFIC')
        adData.set_workgroup('SPECIFIC')
        adData.set_ad_administrator_user('Administrador')
        adData.set_ad_administrator_pass('Evaos.2014')

        adData.set_specific(True)
        adData.set_krb_5_conf('W2xpYmRlZmF1bHRzXQogZGVmYXVsdF9yZWFsbSA9IEVWQU9TLkxPQ0FMCiBkbnNfbG9va3VwX3JlYWxtID0gdHJ1ZQogZG5zX2xvb2t1cF9rZGMgPSB0cnVlCiB0aWNrZXRfbGlmZXRpbWUgPSAyNGgKIHJlbmV3X2xpZmV0aW1lID0gN2QKIHJkbnMgPSBmYWxzZQogZm9yd2FyZGFibGUgPSB5ZXMKIGRlZmF1bHRfdGdzX2VuY3R5cGVzID0gcmM0LWhtYWMKIGRlZmF1bHRfdGt0X2VuY3R5cGVzID0gcmM0LWhtYWMKIHBlcm1pdHRlZF9lbmN0eXBlcyA9IHJjNC1obWFjCgpbcmVhbG1zXQojIERlZmluaXIgc29sbyBzaSBlbCBETlMgbm8gZnVuY2lvbmEgYmllbgojRVZBT1MuTE9DQUwgPSB7CiMga2RjID0gc3J2MS5ldmFvcy5sb2NhbAojIGFkbWluX3NlcnZlciA9IHNydjEuZXZhb3MubG9jYWwKI30KCltkb21haW5fcmVhbG1dCiMgRGVmaW5pciBzb2xvIHNpIGVsIEROUyBubyBmdW5jaW9uYSBiaWVuCiMgLmV2YW9zLmxvY2FsID0gRVZBT1MuTE9DQUwKIyBldmFvcy5sb2NhbCA9IEVWQU9TLkxPQ0FMCg==')
        adData.set_sssd_conf('W3Nzc2RdCmNvbmZpZ19maWxlX3ZlcnNpb24gPSAyCmRvbWFpbnMgPSBldmFvcy5sb2NhbApzZXJ2aWNlcyA9IG5zcywgcGFtLCBwYWMKZGVidWdfbGV2ZWwgPSAwCgpbbnNzXQoKW3BhbV0gCltkb21haW4vZXZhb3MubG9jYWxdCiMgTGEgZW51bWVyYWNpb24gbm8gZXN0YSByZWNvbWVuZGFkYSBlbiBlbnRvcm5vcyBjb24gbXVjaG9zIHVzdWFyaW9zCmNhY2hlX2NyZWRlbnRpYWxzPXRydWUKZW51bWVyYXRlID0gZmFsc2UKCmlkX3Byb3ZpZGVyID0gYWQKYXV0aF9wcm92aWRlciA9IGFkCmNocGFzc19wcm92aWRlciA9IGFkCmFjY2Vzc19wcm92aWRlciA9IGFkCgpvdmVycmlkZV9ob21lZGlyID0gL2hvbWUvJXU=')
        adData.set_smb_conf('W2dsb2JhbF0KICAgd29ya2dyb3VwID0gZXZhb3MKICAgY2xpZW50IHNpZ25pbmcgPSB5ZXMKICAgY2xpZW50IHVzZSBzcG5lZ28gPSB5ZXMKICAga2VyYmVyb3MgbWV0aG9kID0gc2VjcmV0cyBhbmQga2V5dGFiCiAgIGxvZyBmaWxlID0gL3Zhci9sb2cvc2FtYmEvJW0ubG9nCiAgIHJlYWxtID0gRVZBT1MuTE9DQUwKICAgc2VjdXJpdHkgPSBhZHMK')
        adData.set_pam_conf('IyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0jCiMgL2V0Yy9wYW0uY29uZgkJCQkJCQkJICAgICAjCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIwojCiMgTk9URQojIC0tLS0KIwojIE5PVEU6IE1vc3QgcHJvZ3JhbSB1c2UgYSBmaWxlIHVuZGVyIHRoZSAvZXRjL3BhbS5kLyBkaXJlY3RvcnkgdG8gc2V0dXAgdGhlaXIKIyBQQU0gc2VydmljZSBtb2R1bGVzLiBUaGlzIGZpbGUgaXMgdXNlZCBvbmx5IGlmIHRoYXQgZGlyZWN0b3J5IGRvZXMgbm90IGV4aXN0LgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSMKCiMgRm9ybWF0OgojIHNlcnYuCW1vZHVsZQkgICBjdHJsCSAgICAgIG1vZHVsZSBbcGF0aF0JLi4uW2FyZ3MuLl0JCSAgICAgIwojIG5hbWUJdHlwZQkgICBmbGFnCQkJCQkJCSAgICAgIwoK')
        
        adMethod.set_data(adData)  
        
        self.assertTrue(authMethodDao.save(adMethod))
        
        # Check if the changes has been done properly
        currentMethod = authMethodDao.load()
        self.assertEqual(currentMethod.get_name(), adMethod.get_name())
        self.assertEqual(currentMethod.get_data().get_domain(), 'evaos.local')
        self.assertEqual(currentMethod.get_data().get_workgroup(), 'evaos')

        print ('Check a active directory test user login')
        self.assertTrue(self.check_pam_login('amacias', 'Evaos.2014'))   
        
             
        print ('Set the authentication method back to local users')
        self.assertTrue(authMethodDao.delete(adMethod))

        currentMethod = authMethodDao.load()
        self.assertTrue(isinstance(currentMethod, LocalUsersAuthMethod))


        print ('Set the authentication method to LDAP')
        self.assertTrue(authMethodDao.save(ldapMethod))
        
        # Check if the changes has been done properly
        currentMethod = authMethodDao.load()
        self.assertEqual(currentMethod.get_name(), ldapMethod.get_name())
        self.assertEqual(currentMethod.get_data().get_uri(), ldapMethod.get_data().get_uri())
        self.assertEqual(currentMethod.get_data().get_base(), ldapMethod.get_data().get_base())
        self.assertEqual(currentMethod.get_data().get_base_group(), ldapMethod.get_data().get_base_group())
        self.assertEqual(currentMethod.get_data().get_bind_user_dn(), ldapMethod.get_data().get_bind_user_dn())
        self.assertEqual(currentMethod.get_data().get_bind_user_pwd(), ldapMethod.get_data().get_bind_user_pwd())

        print ('Check a LDAP test user login')
        self.assertTrue(self.check_pam_login('pperez', 'pperez'))   
        
             
        print ('Set the authentication method back to local users')
        self.assertTrue(authMethodDao.delete(ldapMethod))

        currentMethod = authMethodDao.load()
        self.assertTrue(isinstance(currentMethod, LocalUsersAuthMethod))


        print ('Delete the test user')
        localUserDao.delete(tstuser)   

        # Restore the original hostname
        self.assertTrue(networkInterfaceDAO.set_hostname(originalHostname))

      
