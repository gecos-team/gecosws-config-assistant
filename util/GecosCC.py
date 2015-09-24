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

import logging
import requests
import traceback
import json

from dto.GecosAccessData import GecosAccessData
from util.Validation import Validation


class GecosCC(object):
    '''
    Utility class to communicate with the Gecos Control Center.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('GecosCC')
        self.last_request_content = None
        
    def validate_credentials(self, data):
        self.logger.debug('Validating credentials...')
        
        if data is None:
            raise ValueError('data is None')
        
        if not isinstance(data, GecosAccessData):
            raise ValueError('data is not a GecosAccessData instance')    
            
        # login, password and URL are mandatory
        if data.get_login() is None or data.get_login().strip() == '':
            self.logger.warn('Empty login!')
            return False

        if data.get_password() is None or data.get_password().strip() == '':
            self.logger.warn('Empty password!')
            return False

        if data.get_url() is None or data.get_url().strip() == '':
            self.logger.warn('Empty url!')
            return False
                
        if not Validation().isUrl(data.get_url()):
            self.logger.warn('Malformed url!')
            return False
        
        # Check credentials
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "%s/auth/config/"%(url)
            self.logger.debug('Try to connect to: %s'%(url))
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            user = data.get_login()
            password = data.get_password()
            r = requests.get(url, auth=(user,password), headers=headers, verify=False)
            if r.ok:
                if hasattr(r,'text'):
                    self.last_request_content = r.text
                else:  
                    self.last_request_content = r.content                
                
                return True            
            
        except Exception:
            self.logger.warn('Error connecting to Gecos server: %s'%(data.get_url()))
            self.logger.warn(str(traceback.format_exc()))
            
        return False            



    def get_json_autoconf(self, data):
        self.logger.debug('Getting auto setup data...')
        
        if not self.validate_credentials(data):
            return False
        
        conf = json.loads(self.last_request_content)
        if conf["chef"]["chef_server_uri"] == "https://localhost/":
            chef_uri = conf["gcc"]["uri_gcc"].split('//')[1].split(':')[0]
            conf["chef"]["chef_server_uri"] = "https://" + chef_uri + '/'
        return conf


