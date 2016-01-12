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
import traceback
from gecosws_config_assistant.util.JSONUtil import JSONUtil


class JSONUtilTest(unittest.TestCase):
    '''
    Unit test that check JSONUtil methods
    '''


    def runTest(self):
        # create a temp file with json
        
        # Save name to pclabel file
        try:
            data = '{"data_key": "data_value"}'
            fd = open('/tmp/jsonutil_test.json', 'w')
            if fd != None:
                fd.write(data)
                fd.close()
            
        except Exception:
            self.logger.error('Error writing file: /tmp/jsonutil_test.json')
            self.logger.error(str(traceback.format_exc()))                
        
        
        jsonutil = JSONUtil()
        json_data = jsonutil.loadJSONFromFile('/tmp/jsonutil_test.json')
        
        self.assertEqual(json_data['data_key'], 'data_value')

       
