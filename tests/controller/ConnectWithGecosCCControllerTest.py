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

from controller.ConnectWithGecosCCController import ConnectWithGecosCCController
from util.UtilMocks import GecosCC
from view.ViewMocks import ViewMock
from dto.GecosAccessData import GecosAccessData
from dto.WorkstationData import WorkstationData


class ConnectWithGecosCCControllerTest(unittest.TestCase):
    '''
    Unit test that check ConnectWithGecosCCController class
    '''


    def runTest(self):
        print "Create the controller"
        controller = ConnectWithGecosCCController()
        
        print "Show the window"
        mainWindow = ViewMock()
        controller.show(mainWindow)
        
        print "Prepare the data"
        gecosAccessData = GecosAccessData()
        gecosAccessData.set_url('http://192.168.1.139/')
        gecosAccessData.set_login('amacias')
        gecosAccessData.set_password('console')        
        
        workstationData = WorkstationData()
        workstationData.set_name("testpc")
        workstationData.set_ou("computers")
        workstationData.set_node_name("d8d0aac2b47abdc9e221eb0ff583d0f9")
        
        controller.view.set_gecos_access_data(gecosAccessData)
        controller.view.set_workstation_data(workstationData)
        
        

        print "Prepare Gecos CC Mock with default LDAP parameters"
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
         '       "chef_link": true, ' + "\n" +
         '       "chef_validation": "' +
         'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBM3BCWFd0RGZM' +
         'UVo5ZldHaFBQR0ZrQ3Q1OXJJTytPandVcXhISmZyTmZSQW1sS01xCks0cy94c3RKL09zMnFlWisy' + 
         'MWhuZUIvWk14OWR4dFlWTzZoR2paU2FDZWRaQnVnSWhEendocFFsREFBVVZYMEIKbjZ6MEQxa1kv' + 
         'bVZrM05DQkVnbXV3S2xoeHFBMVhVS0NhM1FiYk5nenMvaWFMRVU0ZWw0K3MxWEpSMkxPbGpJcgpj' + 
         'Rko0TUxnQUdNZ08yWXlJa2MvVzI3WC9uZG94Z0NnZ0svMGRDNU9Ib01teXZySkRpS2lIYkE2WUNl' + 
         'YmtLVjFFClIxQWxDVk1vRDN1cGxRT3J4NUtoREVpbWFVZEtJWnZEWjZJK2J3bW9tLzVFVDM3eTRR' + 
         'SXgwdHZqRFkzdUR1R0IKckw5ekFjVTduMVpjTW90RkJzMyt4aXB4endLMmRHRnBuM1dOa3dJREFR' + 
         'QUJBb0lCQVFDZXhmZ2JpSUI5M1hCdQpudFJvNXAveTNxRXVkWTRxMGZxSDcvRDl6ak1EOGg2ajBO' + 
         'YkhvNXBHMWtXZEVhdTRmdittdVNWdlU4RWVNRlUxCkFRcTZ1V3hEbW14ZGZsWkxrQUpyWEJIMjMv' + 
         'NmgxZmlybC9jdGt6TzFNMG1hU25rdThldnlFMGhBbDFWeVhsNVQKZnB3TnpoRzJqM0lyQk1IdnJS' + 
         'NENaZk55K2xNU0FiMVBnNWE1aFpWWnZnV09aOFdPeFJRbUhkV3JqUnhmZHdsYwpGb2FZQTBKcGhP' + 
         'bGhmbGdjTVArSXNKbzUyZjdqUkZNZGRTRXZvUEJva1VuaGVpWDBTQjczTWRWMXlraVdCOWUxCmcy' + 
         'MllNRjVkVjRvMmpBM1l4M3F0UTNsdVpWTHhpRERKVE8yWlhKMXNzOXN4RkhWQUZGbnBkYnRWSmU2' + 
         'L1J2S08KSkhaTmt3NmhBb0dCQVBVeHcxVDVkMTVjcUF6R2ZsTE12eGVOdzBFQ1RKRkRkRWMrdm9L' + 
         'bXN3dVJiSHROMlNpYQphRDB6azhLMzcrcjZtTEhxVEJUUFA2V0kzcG9oZkgwdTlWYms3eEhaaXNh' + 
         'blBualg4QU9XeE9VczhTa1ZiN1BtCnRDTFRQcHJ4QUtVUUNkM1lpVC9hQzN2c2FKRk5JM2ZvaEFO' + 
         'UzhTa2ZlOFk2dWJNTWpkT0Q4VmFqQW9HQkFPaGYKUTdvbnA4TXo3VUxSc1M5YmZSZmJGaDZZS24x' +
         'WSs3Q1BBSkZtZG14MGlHWXJybUZiVHFjeUhtZm1vWUZ0eStSRwpkVFJUd1ZJbWRHdW94amJMWURO' + 
         'L3VxS25yMlpvQk5ySk5SdjBwRzZ5V2VhbGxlZWFmS0tpbklvSUlkQ3FZb00vCkE2Q0ZqbW92R0g2' + 
         'dnZ0K09LY2tsemxlQ3ZwMmU3bkZNMExzcjZJeFJBb0dCQU5nMjFKZVhFSEx1WStZNEZ1YnUKMDhk' + 
         'eVkrNXNsNVkxRkZGSysvWDhCOEM0c1IrZVMxTnByV2ZpbG5iTGVrNE1ReUFJaXFTRENRM3d2dExO' + 
         'bXBoTgpFMTFYclpWZzd1WTBUbnVEZDR2Q3BNZXV0TTVVcjliRkpxM2E5OGJycEhUcHlybU5HNkpw' + 
         'cFZ6VzRITFl3ZUVYCjhXbDQ5MTRhL0N1V1YzQ1RMbkdKVlFUZkFvR0FVNytoNVVITmtPanlKaGIx' + 
         'U1NBc0lhRHdnKzVMd2dtRURNbzkKWmlvTG5HTVRsZDlBWmc1R2RyUDFpWFR4MkhmOStEUDhvZk5k' + 
         'eFlIZWk3NjBVYU5TOUx5Z1EyYzBMREJwTDRFOQpCdXBSS1NSV2ltNDdiTkdkQWZDaGdvNFR3ZVRt' + 
         'eEc2OW0ra0d2dlppV2FaMW9KVFlNb3JScDNDVHlyTXhOTngrCmpqYnhCVUVDZ1lCUXVoMU1ubkF3' + 
         'TzVmRXkrRFdueTFERXYxeFhHcUtBU0Q5TUhxM1NjbVlncGpiZTJOZWYrMDkKeTB6TW4wTW1rU2Qy' + 
         'ekV6V0xHNW1Cbm5SbDlxV1ZLbmRzakNoT1J3UnZLYzhhUGE3N0hYMnQ1QzBZUmxqcnZCcgppdUI4' + 
         'bXErYXNNSFp0MlJjWWxIU3poNngxUUMrT0tGU2hIOU9qNFZrUUhMS3FMa1RlMkVwL3c9PQotLS0t' + 
         'LUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo="}}, ' + "\n" +
         '  "version": "0.2.0", ' + "\n" +
         '  "organization": "Junta de Andaluc\u00eda" '+ "\n" +
         '}')
        
        print "Simulate link to GECOS CC"        
        self.assertTrue(controller.connect())
        
      

        print "Simulate unlink from GECOS CC"
        self.assertTrue(controller.disconnect())
        
        
        
        print "End ;)"
