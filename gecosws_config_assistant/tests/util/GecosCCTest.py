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
import json

from gecosws_config_assistant.util.GecosCC import GecosCC
from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData

class GecosCCTest(unittest.TestCase):
    '''
    Unit test that check GecosCC methods
    '''


    def runTest(self):
        gecosCC = GecosCC()

        # Test with valid Gecos CC credentials
        badCredentials = GecosAccessData()
        self.assertFalse(gecosCC.validate_credentials(badCredentials), 
                        'Error validating empty credentials')

        badCredentials.set_login('nonexistenuser')
        self.assertFalse(gecosCC.validate_credentials(badCredentials), 
                        'Error validating credentials without password')


        badCredentials.set_password('badpassword')
        self.assertFalse(gecosCC.validate_credentials(badCredentials), 
                        'Error validating credentials without URL')


        badCredentials.set_url('this is not a URL!')
        self.assertFalse(gecosCC.validate_credentials(badCredentials), 
                        'Error validating credentials with a malformed URL')

        badCredentials.set_url('http://www.google.es')
        self.assertFalse(gecosCC.validate_credentials(badCredentials), 
                        'Error validating credentials with a bad address')

        badCredentials.set_url('http://192.168.0.15/')
        self.assertFalse(gecosCC.validate_credentials(badCredentials), 
                        'Error validating credentials with a non existent user')

        badCredentials.set_login('superuser')
        self.assertFalse(gecosCC.validate_credentials(badCredentials), 
                        'Error validating credentials with a bad password')

        
        # Test with valid Gecos CC credentials
        validCredentials = GecosAccessData()
        validCredentials.set_url('http://192.168.0.15/')
        validCredentials.set_login('superuser')
        validCredentials.set_password('yzsrhysa')
        self.assertTrue(gecosCC.validate_credentials(validCredentials), 
                        'Error validating credentials')
        
        # Check autoconfiguration JSON
        conf = gecosCC.get_json_autoconf(validCredentials)
        self.assertNotEqual(conf, None, "None returned!")
        print "AutoSetup JSON:", json.dumps(conf)
       
        # Check ou search
        result = gecosCC.search_ou_by_text(validCredentials, '')
        self.assertTrue(isinstance(result, (list, tuple)), 'OUs must be a list!')
       
        for res in result:
            result2 = gecosCC.search_ou_by_text(validCredentials, res[1])
            self.assertTrue(isinstance(result2, (list, tuple)), 'OU: %s must exist!'%(res[1]))
       
        # Get all computer names
        result = gecosCC.get_computer_names(validCredentials)
        self.assertTrue(isinstance(result, (list, tuple)), 'Computer names must be a list!')

        # Chef node registration
        self.assertFalse(gecosCC.is_registered_chef_node(validCredentials, 'test'))
        
        private_key = gecosCC.register_chef_node(validCredentials, 'test')
        self.assertNotEqual(private_key, False, "No private key returned!")
        self.assertTrue(gecosCC.is_registered_chef_node(validCredentials, 'test'))

        # Chef node re-registering        
        private_key = gecosCC.reregister_chef_node(validCredentials, 'test')
        self.assertNotEqual(private_key, False, "No private key returned!")
        self.assertTrue(gecosCC.is_registered_chef_node(validCredentials, 'test'))
        
        # Chef node unregistering        
        self.assertTrue(gecosCC.unregister_chef_node(validCredentials, 'test'))
        self.assertFalse(gecosCC.is_registered_chef_node(validCredentials, 'test'))
        
