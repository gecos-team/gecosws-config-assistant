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

from gecosws_config_assistant.util.Validation import Validation

class ValidationTest(unittest.TestCase):
    '''
    Unit test that check Validation methods
    '''


    def runTest(self):
        validation = Validation()

        self.assertFalse(validation.isUrl(None))
        self.assertFalse(validation.isUrl(''))
        self.assertFalse(validation.isUrl('malformed url'))
        self.assertFalse(validation.isUrl('httpQ://www.google.es'))
        self.assertFalse(validation.isUrl('http:/www.google.es'))
        self.assertFalse(validation.isUrl('http://es'))
        self.assertTrue(validation.isUrl('http://www.google.es'))
        self.assertTrue(validation.isUrl('https://www.google.es/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=caca'))
        self.assertTrue(validation.isUrl('http://192.168.10.20:8080/'))


        self.assertFalse(validation.isLdapUri(None))
        self.assertFalse(validation.isLdapUri(''))
        self.assertFalse(validation.isLdapUri('malformed url'))
        self.assertFalse(validation.isLdapUri('ldapQ://www.google.es'))
        self.assertFalse(validation.isLdapUri('ldap:/www.google.es'))
        self.assertFalse(validation.isLdapUri('ldap://es'))
        self.assertTrue(validation.isLdapUri('ldap://www.google.es'))
        self.assertTrue(validation.isLdapUri('ldaps://www.google.es:1234/'))
        self.assertTrue(validation.isLdapUri('ldaps://192.168.10.20:1234/'))
        self.assertTrue(validation.isLdapUri('ldap://test.ldap.server'))
        

        self.assertFalse(validation.isLogin(None))
        self.assertFalse(validation.isLogin(''))
        self.assertFalse(validation.isLogin('Contains Space'))
        self.assertFalse(validation.isLogin('Contains + Symbol'))
        self.assertFalse(validation.isLogin('Contains Ñ character'))
        self.assertTrue(validation.isLogin('amacias'))
        
        self.assertFalse(validation.isAscii(None))
        self.assertFalse(validation.isAscii('áéíóú'))
        self.assertTrue(validation.isAscii(''))
        self.assertTrue(validation.isAscii('ascii'))
        self.assertTrue(validation.isAscii('ascii with spaces'))
        self.assertTrue(validation.isAscii('ascii symbols: + . ; _ -'))
        
