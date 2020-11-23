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

from gecosws_config_assistant.util.CommandUtil import CommandUtil

class CommandUtilTest(unittest.TestCase):
    '''
    Unit test that check CommandUtil methods
    '''


    def runTest(self):
        commandUtil = CommandUtil()
		
	self.assertFalse(commandUtil.execute_command('non existent command'))
	self.assertTrue(commandUtil.execute_command('ls'))
		
	self.assertFalse(commandUtil.get_command_output('non existent command'), [])
	self.assertNotEqual(commandUtil.get_command_output('ls'), [])
	self.assertTrue(commandUtil.execute_command('echo "Asking a yes no question (y/n)?" & read choice'))
	self.assertTrue(commandUtil.get_command_output('echo "Asking a yes no question (y/n)?" & read choice'))
        

