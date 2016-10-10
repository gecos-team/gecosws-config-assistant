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
import os

from gecosws_config_assistant.util.GemUtil import GemUtil

class GemUtilTest(unittest.TestCase):
    '''
    Unit test that check GemUtil methods
    '''


    def runTest(self):
        gemUtil = GemUtil()
		
        # Reset the test
        gemUtil.remove_all_gem_sources()
        gemUtil.add_gem_source('https://rubygems.org/')
        gemUtil.uninstall_gem('a1425bt')
        
        # Start the test
        self.assertNotEqual(gemUtil.get_gem_sources_list(), [])
        print("INITIAL LIST: ", gemUtil.get_gem_sources_list())
        gemUtil.remove_all_gem_sources()
        self.assertEqual(gemUtil.get_gem_sources_list(), [])

        self.assertTrue(gemUtil.add_gem_source('https://rubygems.org/'))
        self.assertNotEqual(gemUtil.get_gem_sources_list(), [])

        self.assertFalse(gemUtil.add_gem_source('http://nonexistentdomain.org/'))


        self.assertFalse(gemUtil.is_gem_intalled('a1425bt'))
        self.assertTrue(gemUtil.install_gem('a1425bt'))
        self.assertTrue(gemUtil.is_gem_intalled('a1425bt'))
        self.assertTrue(gemUtil.uninstall_gem('a1425bt'))
        self.assertFalse(gemUtil.is_gem_intalled('a1425bt'))
