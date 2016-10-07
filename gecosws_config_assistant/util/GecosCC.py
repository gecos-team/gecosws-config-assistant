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

from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.util.Validation import Validation


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
        self.timeout = 120
        
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
            r = requests.get(url, auth=(user,password), headers=headers, 
                             verify=True, timeout=self.timeout)
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


    def get_computer_names(self, data):
        self.logger.debug('Get all computer names by text...')
        
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
        
        # Get the list of workstation names
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "%s/computers/list/"%(url)
            self.logger.debug('Try to connect to: %s'%(url))
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            user = data.get_login()
            password = data.get_password()
            r = requests.get(url, auth=(user,password), headers=headers, 
                verify=False, timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s'%(url))
                computer_names = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s'%(r.text))
                    computer_names = json.loads(r.text)['computers']
                else:  
                    self.logger.debug('Response: %s'%(r.content))
                    computer_names = json.loads(r.content)['computers']               
                
                
                return computer_names            

            self.logger.debug('Response: NOT OK')
                     
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



    def search_ou_by_text(self, data, searchFilter):
        self.logger.debug('Search ou by text...')
        
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
        
        if searchFilter is None:
            searchFilter = ''
        
        # Get the list of OUs
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "%s/ou/gca/?q=%s"%(url, searchFilter)
            self.logger.debug('Try to connect to: %s'%(url))
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            user = data.get_login()
            password = data.get_password()
            r = requests.get(url, auth=(user,password), headers=headers, 
                verify=False, timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s'%(url))
                arr_ou = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s'%(r.text))
                    arr_ou = json.loads(r.text)['ous']
                else:  
                    self.logger.debug('Response: %s'%(r.content))
                    arr_ou = json.loads(r.content)['ous']               
                
                return arr_ou            

            self.logger.debug('Response: NOT OK')
                     
        except Exception:
            self.logger.warn('Error connecting to Gecos server: %s'%(data.get_url()))
            self.logger.warn(str(traceback.format_exc()))
            
        return False  


    def unregister_computer(self, data, nodename):
        self.logger.debug('Unregister computer...')
        
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
        
        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False

        
        # Unregister the computer
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "%s/register/computer/?node_id=%s"%(url, nodename)
            self.logger.debug('Try to connect to: %s'%(url))
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            user = data.get_login()
            password = data.get_password()
            r = requests.delete(url, auth=(user,password), headers=headers, 
                verify=False, timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s'%(url))
                response_json = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s'%(r.text))
                    response_json = json.loads(r.text)
                else:  
                    self.logger.debug('Response: %s'%(r.content))
                    response_json = json.loads(r.content)               
                
                if response_json is None:
                    self.logger.error('Error unregistering computer: NO RESPONSE')
                    return False
                
                if not response_json["ok"]:
                    self.logger.error('Error unregistering computer: %s'%(response_json['message']))
                    return False
                
                return True                

            self.logger.debug('Response: NOT OK')
                     
        except Exception:
            self.logger.warn('Error connecting to Gecos server: %s'%(data.get_url()))
            self.logger.warn(str(traceback.format_exc()))
            
        return False  

    def register_computer(self, data, nodename, selected_ou):
        self.logger.debug('Register computer (%s, %s)...', nodename, selected_ou)
        
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
        
        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False

        if selected_ou is None or selected_ou.strip() == '':
            self.logger.warn('selected_ou is empty!')
            return False

        
        # Register in the server
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "%s/register/computer/"%(url)
            self.logger.debug('Try to connect to: %s'%(url))
            user = data.get_login()
            password = data.get_password()
            
            payload = {'node_id': nodename, 'ou_id': selected_ou}
            self.logger.debug('payload: %s'%(json.dumps(payload)))
            
            r = requests.post(url, auth=(user,password), 
                verify=False, timeout=self.timeout, data=payload)
            if r.ok:
                self.logger.debug('Response: %s'%(url))
                response_json = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s'%(r.text))
                    response_json = json.loads(r.text)
                else:  
                    self.logger.debug('Response: %s'%(r.content))
                    response_json = json.loads(r.content)               
                
                if response_json is None:
                    self.logger.error('Error registering computer: NO RESPONSE')
                    return False
                
                if not response_json["ok"]:
                    self.logger.error('Error registering computer: %s'%(response_json['message']))
                    return False
                
                return True            

            self.logger.debug('Response: NOT OK')
                     
        except Exception:
            self.logger.warn('Error connecting to Gecos server: %s'%(data.get_url()))
            self.logger.warn(str(traceback.format_exc()))
            
        return False          

    def get_file_content_from_url(self, url):
        if url is None or url.strip() == '':
            self.logger.warn('Empty url!')
            return None      
        
        # Get the file content
        try:
            url = str(url)
            self.logger.debug('Try to connect to: %s'%(url))
            r = requests.get(url, verify=False, timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s'%(url))
                if hasattr(r,'text'):
                    return r.text
                else:  
                    return r.content

            self.logger.debug('Response: NOT OK')
                     
        except Exception:
            self.logger.warn('Error getting content from url: %s'%(url))
            self.logger.warn(str(traceback.format_exc()))
            
        return None          
