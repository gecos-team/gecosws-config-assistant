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
from gecosws_config_assistant.dto.ADAuthMethod import ADAuthMethod
from gecosws_config_assistant.dto.ADSetupData import ADSetupData

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class ADAuthMethodTest(unittest.TestCase):
    '''
    Unit test that check getters and setters
    '''


    def runTest(self):
        obj = ADAuthMethod()
        self.assertEqual(obj.get_name(), _('Active Directory'))
        self.assertEqual(obj.get_data(), None)
        
        value = ADSetupData()
        obj.set_data(value)
        self.assertEqual(obj.get_data(), value)
        self.assertEqual(obj.data, value)

        obj.set_data(None)
        self.assertEqual(obj.get_data(), None)

        
        with self.assertRaises(TypeError):
            obj.set_data('wrong data!')




