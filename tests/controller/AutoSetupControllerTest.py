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

from controller.AutoSetupController import AutoSetupController
from util.UtilMocks import GecosCC
from view.ViewMocks import ViewMock


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
        
        print "End ;)"
