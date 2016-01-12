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
from gecosws_config_assistant.dto.ADSetupData import ADSetupData

class ADSetupDataTest(unittest.TestCase):
    '''
    Unit test that check getters and setters
    '''


    def runTest(self):
        obj = ADSetupData()
        
        obj.set_domain('test_domain')
        self.assertEqual(obj.get_domain(), 'test_domain')
        self.assertEqual(obj.domain, 'test_domain')

        obj.set_workgroup('test_workgroup')
        self.assertEqual(obj.get_workgroup(), 'test_workgroup')
        self.assertEqual(obj.workgroup, 'test_workgroup')

        obj.set_ad_administrator_user('test_user')
        self.assertEqual(obj.get_ad_administrator_user(), 'test_user')
        self.assertEqual(obj.ad_administrator_user, 'test_user')

        obj.set_ad_administrator_pass('test_pass')
        self.assertEqual(obj.get_ad_administrator_pass(), 'test_pass')
        self.assertEqual(obj.ad_administrator_pass, 'test_pass')

        obj.set_specific(True)
        self.assertEqual(obj.get_specific(), True)
        self.assertEqual(obj.specific, True)

        obj.set_krb_5_conf('BASE64CONTENT')
        self.assertEqual(obj.get_krb_5_conf(), 'BASE64CONTENT')
        self.assertEqual(obj.krb5_conf, 'BASE64CONTENT')

        obj.set_sssd_conf('BASE64CONTENT')
        self.assertEqual(obj.get_sssd_conf(), 'BASE64CONTENT')
        self.assertEqual(obj.sssd_conf, 'BASE64CONTENT')

        obj.set_smb_conf('BASE64CONTENT')
        self.assertEqual(obj.get_smb_conf(), 'BASE64CONTENT')
        self.assertEqual(obj.smb_conf, 'BASE64CONTENT')

        obj.set_pam_conf('BASE64CONTENT')
        self.assertEqual(obj.get_pam_conf(), 'BASE64CONTENT')
        self.assertEqual(obj.pam_conf, 'BASE64CONTENT')

        # Test connection with wrong password
        obj.set_specific(False)
        obj.set_domain('evaos.local')
        obj.set_workgroup('evaos')
        obj.set_ad_administrator_user('Administrador')
        obj.set_ad_administrator_pass('wrongpass')
        self.assertFalse(obj.test())

        # Test connection with correct data
        obj.set_domain('evaos.local')
        obj.set_workgroup('evaos')
        obj.set_ad_administrator_user('Administrador')
        obj.set_ad_administrator_pass('Evaos.2014')
        self.assertTrue(obj.test())


