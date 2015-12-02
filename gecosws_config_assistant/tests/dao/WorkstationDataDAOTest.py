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

from gecosws_config_assistant.dao.WorkstationDataDAO import WorkstationDataDAO
from gecosws_config_assistant.dto.WorkstationData import WorkstationData


class WorkstationDataDAOTest(unittest.TestCase):
    '''
    Unit test that check WorkstationDataDAO class
    '''


    def runTest(self):
        dao = WorkstationDataDAO()
        
        
        originalData = dao.load() 
        
        # Set a new name for this pc
        newData = WorkstationData()
        newData.set_name('test_name')
        newData.set_node_name('test_node_name')
        dao.save(newData)
        
        newData = dao.load()
        
        self.assertEqual(newData.get_name(), 'test_name')
        self.assertEqual(newData.get_node_name(), 'test_node_name')
        
        dao.delete(newData)
        self.assertFalse(os.path.isfile('/etc/pclabel'))
        
        if originalData is not None:
            dao.save(originalData)

