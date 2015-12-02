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

from gecosws_config_assistant.controller.AutoSetupController import AutoSetupController
from gecosws_config_assistant.util.UtilMocks import GecosCC
from gecosws_config_assistant.view.ViewMocks import ViewMock
from gecosws_config_assistant.dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO
from gecosws_config_assistant.dto.ADAuthMethod import ADAuthMethod
from gecosws_config_assistant.dto.ADSetupData import ADSetupData


class AutoSetupControllerTest(unittest.TestCase):
    '''
    Unit test that check AutoSetupController class
    '''


    def runTest(self):
        print "Create the controller"
        controller = AutoSetupController()
        
        print "Show the window"
        mainWindow = ViewMock()
        controller.show(mainWindow)

        print "Prepare Gecos CC Mock with default LDAP parameters"
        gecosCC = GecosCC()
        gecosCC.set_last_request_content(
         '{ ' + "\n" +
         '  "uri_ntp": "0.centos.pool.ntp.org", ' +  "\n" +
         '  "gem_repo": "http://v2.gecos.guadalinex.org/gems/", ' + "\n" +
         '  "gcc": { '+ "\n" +
         '       "gcc_username": "amacias", ' + "\n" +
         '       "gcc_link": true, ' + "\n" +
         '       "uri_gcc": "http://192.168.1.139"}, ' + "\n" +
         '  "auth": { '+ "\n" +
         '       "auth_type": "LDAP", '+ "\n" +
         '       "auth_properties": { '+ "\n" +
         '             "basegroup": "OU_BASE_GROUP", ' + "\n" +
         '             "binddn": "USER_WITH_BIND_PRIVILEGES", ' + "\n" +
         '             "base": "OU_BASE_USER", '+ "\n" +
         '             "bindpwd": "PASSWORD_USER_BIND", '+ "\n" +
         '             "uri": "URL_LDAP"} '+ "\n" +
         '       }, '+ "\n" +
         '  "chef": { '+ "\n" +
         '       "chef_server_uri": "https://192.168.1.139/", ' + "\n" +
         '       "chef_link": true, '+ "\n" +
         '       "chef_validation": "VALIDATION_DATA"}, ' + "\n" +
         '  "version": "0.2.0", ' + "\n" +
         '  "organization": "Junta de Andaluc\u00eda" '+ "\n" +
         '}')
        
        print "Simulate setup"        
        self.assertTrue(controller.setup())

        print "Prepare Gecos CC Mock with LDAP user authentication"
        gecosCC = GecosCC()
        gecosCC.set_last_request_content(
         '{ ' + "\n" +
         '  "uri_ntp": "0.centos.pool.ntp.org", ' +  "\n" +
         '  "gem_repo": "http://v2.gecos.guadalinex.org/gems/", ' + "\n" +
         '  "gcc": { '+ "\n" +
         '       "gcc_username": "amacias", ' + "\n" +
         '       "gcc_link": true, ' + "\n" +
         '       "uri_gcc": "http://192.168.1.139"}, ' + "\n" +
         '  "auth": { '+ "\n" +
         '       "auth_type": "LDAP", '+ "\n" +
         '       "auth_properties": { '+ "\n" +
         '             "basegroup": "ou=groups,dc=us,dc=es", ' + "\n" +
         '             "binddn": "cn=admin,dc=us,dc=es", ' + "\n" +
         '             "base": "ou=users,dc=us,dc=es", '+ "\n" +
         '             "bindpwd": "demoevaos", '+ "\n" +
         '             "uri": "ldap://test.ldap.server"} '+ "\n" +
         '       }, '+ "\n" +
         '  "chef": { '+ "\n" +
         '       "chef_server_uri": "https://192.168.1.139/", ' + "\n" +
         '       "chef_link": true, '+ "\n" +
         '       "chef_validation": "VALIDATION_DATA"}, ' + "\n" +
         '  "version": "0.2.0", ' + "\n" +
         '  "organization": "Junta de Andaluc\u00eda" '+ "\n" +
         '}')
        
        
        print "Simulate setup"        
        self.assertTrue(controller.setup())


        print "Prepare Gecos CC Mock with AD user authentication"
        gecosCC = GecosCC()
        gecosCC.set_last_request_content(
         '{ ' + "\n" +
         '  "uri_ntp": "0.centos.pool.ntp.org", ' +  "\n" +
         '  "gem_repo": "http://v2.gecos.guadalinex.org/gems/", ' + "\n" +
         '  "gcc": { '+ "\n" +
         '       "gcc_username": "amacias", ' + "\n" +
         '       "gcc_link": true, ' + "\n" +
         '       "uri_gcc": "http://192.168.1.139"}, ' + "\n" +
         '  "auth": { '+ "\n" +
         '       "auth_type": "AD", '+ "\n" +
         '       "auth_properties": { '+ "\n" +
         '             "specific_conf": false, ' + "\n" +
         '             "ad_properties": { ' + "\n" +
         '                 "fqdn": "evaos.local", '+ "\n" +
         '                 "workgroup": "evaos"}} '+ "\n" +
         '       }, '+ "\n" +
         '  "chef": { '+ "\n" +
         '       "chef_server_uri": "https://192.168.1.139/", ' + "\n" +
         '       "chef_link": true, '+ "\n" +
         '       "chef_validation": "VALIDATION_DATA"}, ' + "\n" +
         '  "version": "0.2.0", ' + "\n" +
         '  "organization": "Junta de Andaluc\u00eda" '+ "\n" +
         '}')
        
        print "Simulate setup"        
        self.assertTrue(controller.setup())

        print "Return user authentication to local users"
        authMethodDao = UserAuthenticationMethodDAO()
        method = ADAuthMethod()
        data = ADSetupData()
                
        # Data of an Active Directory server used for tests 
        data.set_domain('evaos.local')
        data.set_workgroup('evaos')
        data.set_ad_administrator_user('Administrador')
        data.set_ad_administrator_pass('Evaos.2014')
        
        method.set_data(data)
        self.assertTrue(authMethodDao.delete(method))        
        
        
        
        print "Prepare Gecos CC Mock with AD user authentication (specific setup)"
        gecosCC = GecosCC()
        gecosCC.set_last_request_content(
         '{ ' + "\n" +
         '  "uri_ntp": "0.centos.pool.ntp.org", ' +  "\n" +
         '  "gem_repo": "http://v2.gecos.guadalinex.org/gems/", ' + "\n" +
         '  "gcc": { '+ "\n" +
         '       "gcc_username": "amacias", ' + "\n" +
         '       "gcc_link": true, ' + "\n" +
         '       "uri_gcc": "http://192.168.1.139"}, ' + "\n" +
         '  "auth": { '+ "\n" +
         '       "auth_type": "AD", '+ "\n" +
         '       "auth_properties": { '+ "\n" +
         '             "specific_conf": true, ' + "\n" +
         '             "ad_properties": { ' + "\n" +
         '             "krb5_conf": "W2xpYmRlZmF1bHRzXQogZGVmYXVsdF9yZWFsbSA9IEVWQU9TLkxPQ0FMCiBkbnNfbG9va3VwX3Jl\\nYWxtID0gdHJ1ZQogZG5zX2xvb2t1cF9rZGMgPSB0cnVlCiB0aWNrZXRfbGlmZXRpbWUgPSAyNGgK\\nIHJlbmV3X2xpZmV0aW1lID0gN2QKIHJkbnMgPSBmYWxzZQogZm9yd2FyZGFibGUgPSB5ZXMKIGRl\\nZmF1bHRfdGdzX2VuY3R5cGVzID0gcmM0LWhtYWMKIGRlZmF1bHRfdGt0X2VuY3R5cGVzID0gcmM0\\nLWhtYWMKIHBlcm1pdHRlZF9lbmN0eXBlcyA9IHJjNC1obWFjCgpbcmVhbG1zXQojIERlZmluaXIg\\nc29sbyBzaSBlbCBETlMgbm8gZnVuY2lvbmEgYmllbgojRVZBT1MuTE9DQUwgPSB7CiMga2RjID0g\\nc3J2MS5ldmFvcy5sb2NhbAojIGFkbWluX3NlcnZlciA9IHNydjEuZXZhb3MubG9jYWwKI30KCltk\\nb21haW5fcmVhbG1dCiMgRGVmaW5pciBzb2xvIHNpIGVsIEROUyBubyBmdW5jaW9uYSBiaWVuCiMg\\nLmV2YW9zLmxvY2FsID0gRVZBT1MuTE9DQUwKIyBldmFvcy5sb2NhbCA9IEVWQU9TLkxPQ0FMCg==\\n", ' +"\n" +
         '             "sssd_conf": "W3Nzc2RdCmNvbmZpZ19maWxlX3ZlcnNpb24gPSAyCmRvbWFpbnMgPSBldmFvcy5sb2NhbApzZXJ2\\naWNlcyA9IG5zcywgcGFtLCBwYWMKZGVidWdfbGV2ZWwgPSAwCgpbbnNzXQoKW3BhbV0gCltkb21h\\naW4vZXZhb3MubG9jYWxdCiMgTGEgZW51bWVyYWNpb24gbm8gZXN0YSByZWNvbWVuZGFkYSBlbiBl\\nbnRvcm5vcyBjb24gbXVjaG9zIHVzdWFyaW9zCmNhY2hlX2NyZWRlbnRpYWxzPXRydWUKZW51bWVy\\nYXRlID0gZmFsc2UKCmlkX3Byb3ZpZGVyID0gYWQKYXV0aF9wcm92aWRlciA9IGFkCmNocGFzc19w\\ncm92aWRlciA9IGFkCmFjY2Vzc19wcm92aWRlciA9IGFkCgpvdmVycmlkZV9ob21lZGlyID0gL2hv\\nbWUvJXU=\\n",  ' +"\n" +
         '             "smb_conf": "W2dsb2JhbF0KICAgd29ya2dyb3VwID0gZXZhb3MKICAgY2xpZW50IHNpZ25pbmcgPSB5ZXMKICAg\\nY2xpZW50IHVzZSBzcG5lZ28gPSB5ZXMKICAga2VyYmVyb3MgbWV0aG9kID0gc2VjcmV0cyBhbmQg\\na2V5dGFiCiAgIGxvZyBmaWxlID0gL3Zhci9sb2cvc2FtYmEvJW0ubG9nCiAgIHJlYWxtID0gRVZB\\nT1MuTE9DQUwKICAgc2VjdXJpdHkgPSBhZHMK\\n",  ' +"\n" +
         '             "pam_conf": "IyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t\\nLS0tLS0tLS0tLS0tLS0tLS0tLS0jCiMgL2V0Yy9wYW0uY29uZgkJCQkJCQkJICAgICAjCiMgLS0t\\nLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t\\nLS0tLS0tLS0tLS0tLS0tIwojCiMgTk9URQojIC0tLS0KIwojIE5PVEU6IE1vc3QgcHJvZ3JhbSB1\\nc2UgYSBmaWxlIHVuZGVyIHRoZSAvZXRjL3BhbS5kLyBkaXJlY3RvcnkgdG8gc2V0dXAgdGhlaXIK\\nIyBQQU0gc2VydmljZSBtb2R1bGVzLiBUaGlzIGZpbGUgaXMgdXNlZCBvbmx5IGlmIHRoYXQgZGly\\nZWN0b3J5IGRvZXMgbm90IGV4aXN0LgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t\\nLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSMKCiMgRm9ybWF0Ogoj\\nIHNlcnYuCW1vZHVsZQkgICBjdHJsCSAgICAgIG1vZHVsZSBbcGF0aF0JLi4uW2FyZ3MuLl0JCSAg\\nICAgIwojIG5hbWUJdHlwZQkgICBmbGFnCQkJCQkJCSAgICAgIwoK\\n"  ' +"\n" +
         '       }}}, '+ "\n" +
         '  "chef": { '+ "\n" +
         '       "chef_server_uri": "https://192.168.1.139/", ' + "\n" +
         '       "chef_link": true, '+ "\n" +
         '       "chef_validation": "VALIDATION_DATA"}, ' + "\n" +
         '  "version": "0.2.0", ' + "\n" +
         '  "organization": "Junta de Andaluc\u00eda" '+ "\n" +
         '}')
        
        print "Simulate setup"        
        self.assertTrue(controller.setup())

        print "Return user authentication to local users"
        authMethodDao = UserAuthenticationMethodDAO()
        method = ADAuthMethod()
        data = ADSetupData()
                
        # Data of an Active Directory server used for tests 
        data.set_domain('evaos.local')
        data.set_workgroup('evaos')
        data.set_ad_administrator_user('Administrador')
        data.set_ad_administrator_pass('Evaos.2014')
        
        method.set_data(data)
        self.assertTrue(authMethodDao.delete(method))        
        
        
        print "End ;)"
