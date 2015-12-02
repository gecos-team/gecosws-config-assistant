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
import grp
import pwd
import os
from util.Template import Template


class TemplateTest(unittest.TestCase):
    '''
    Unit test that check getters and setters
    '''

    def findInFile(self, filepath, value):
        with open(filepath) as fp:
            for line in fp:
                if value in line:
                    return True        
        
        return False


    def runTest(self):
        template = Template()
        template.source = 'tests/test.tmpl'
        template.destination = '/tmp/test1/test2/test3/test.file'
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        template.variables = { 'test_value':  'TEST_VALUE_1',
                              'test_2_value':  'TEST_2_VALUE_1'}        
        

        # Delete the file is exist
        if os.path.isfile(template.destination):
            os.remove(template.destination)
        
        
        # Create the file
        template.save()
        self.assertTrue(self.findInFile(template.destination, 'TEST_VALUE_1'), 
                        'Can not find TEST_VALUE_1!')
        self.assertTrue(self.findInFile(template.destination, 'TEST_2_VALUE_1'), 
                        'Can not find TEST_2_VALUE_1!')
        self.assertFalse(self.findInFile(template.destination, 'test_3_value'), 
                        'Found test_3_value!')
        
        # update the file
        template.variables = { 'test_value':  'TEST_VALUE_2',
                              'test_3_value':  'TEST_3_VALUE_1'}  
        template.save()
        self.assertTrue(self.findInFile(template.destination, 'TEST_VALUE_2'), 
                        'Can not find TEST_VALUE_2!')
        self.assertTrue(self.findInFile(template.destination, 'TEST_3_VALUE_1'), 
                        'Can not find TEST_3_VALUE_1!')
        self.assertFalse(self.findInFile(template.destination, 'test_2_value'), 
                        'Found test_2_value!')
        

        # Change mode and owner
        os.chmod(template.destination, 00666)
        uid = pwd.getpwnam('nobody').pw_uid
        gid = grp.getgrnam('nogroup').gr_gid
        os.chown(template.destination, uid, gid)
        
        # Test mode and owner
        template.save()
        
        stat_info = os.stat(template.destination)
        uid = stat_info.st_uid
        gid = stat_info.st_gid   
        current_usr = pwd.getpwuid(uid)[0]
        current_grp = grp.getgrgid(gid)[0]        
        m = stat_info.st_mode & 00777
        self.assertEqual(template.mode, m)     
        self.assertEqual(current_usr, template.owner)     
        self.assertEqual(current_grp, template.group)     
        
        os.remove('/tmp/test1/test2/test3/test.file')
        os.rmdir('/tmp/test1/test2/test3')
        os.rmdir('/tmp/test1/test2')
        os.rmdir('/tmp/test1')
