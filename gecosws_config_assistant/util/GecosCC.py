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
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"


import traceback
import json
import logging
from urllib.parse import urlparse
import requests

from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.util.Validation import Validation
from gecosws_config_assistant.util.SSLUtil import SSLUtil

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

    def _check_credentials(self, data):
        ''' Checking credentials '''

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

        return True

    def validate_credentials(self, data):
        ''' Validating credentials '''

        self.logger.debug('Validating credentials...')

        if not self._check_credentials(data):
            return False

        # Check credentials
        try:
            url = str(data.get_url())
            if urlparse(url).path in ['','/']:
                url = "{}/auth/config/".format(
                    url[0:-1] if url.endswith('/') else url)

            self.logger.debug('Try to connect to: %s', url)
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }
            user = data.get_login()
            password = data.get_password()
            r = requests.get(
                url,
                auth=(user,password),
                headers=headers,
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout)
            if r.ok:
                if hasattr(r,'text'):
                    self.last_request_content = r.text
                else:
                    self.last_request_content = r.content

                return True

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s', data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def get_computer_names(self, data):
        ''' Get all computer names by text '''

        self.logger.debug('Get all computer names by text...')

        if not self._check_credentials(data):
            return False

        # Get the list of workstation names
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/computers/list/".format(url)
            self.logger.debug('Try to connect to: %s', url)
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }
            user = data.get_login()
            password = data.get_password()
            r = requests.get(
                url,
                auth=(user,password),
                headers=headers,
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s', url)
                computer_names = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s', r.text)
                    computer_names = json.loads(r.text)['computers']
                else:
                    self.logger.debug('Response: %s', r.content)
                    computer_names = json.loads(r.content)['computers']

                return computer_names

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s', data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def get_json_autoconf(self, data):
        ''' Getting auto setup data '''

        self.logger.debug('Getting auto setup data...')

        if not self.validate_credentials(data):
            return False

        conf = json.loads(self.last_request_content)
        if conf["chef"]["chef_server_uri"] == "https://localhost/":
            chef_uri = conf["gcc"]["uri_gcc"].split('//')[1].split(':')[0]
            conf["chef"]["chef_server_uri"] = "https://" + chef_uri + '/'

        return conf

    def search_ou_by_text(self, data, searchFilter):
        ''' Search ou by text '''

        self.logger.debug('Search ou by text...')

        if not self._check_credentials(data):
            return False

        if searchFilter is None:
            searchFilter = ''

        # Get the list of OUs
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/ou/gca/?q={}".format(url, searchFilter)
            self.logger.debug('Try to connect to: %s', url)
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }
            user = data.get_login()
            password = data.get_password()
            r = requests.get(
                url,
                auth=(user,password),
                headers=headers,
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s', url)
                arr_ou = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s', r.text)
                    arr_ou = json.loads(r.text)['ous']
                else:
                    self.logger.debug('Response: %s', r.content)
                    arr_ou = json.loads(r.content)['ous']

                return arr_ou

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s', data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def unregister_computer(self, data, nodename):
        ''' Unregistering computer '''

        self.logger.debug('Unregister computer...')

        if not self._check_credentials(data):
            return False

        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False

        # Unregister the computer
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/register/computer/?node_id={}".format(url, nodename)
            self.logger.debug('Try to connect to: %s', url)
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }
            user = data.get_login()
            password = data.get_password()
            r = requests.delete(
                url,
                auth=(user,password),
                headers=headers,
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s', url)
                response_json = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s', r.text)
                    response_json = json.loads(r.text)
                else:
                    self.logger.debug('Response: %s', r.content)
                    response_json = json.loads(r.content)

                if response_json is None:
                    self.logger.error(
                        'Error unregistering computer: NO RESPONSE')
                    return False

                if not response_json["ok"]:
                    self.logger.error(
                        'Error unregistering computer: %s',
                        response_json['message'])
                    return False

                return True

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s', data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def register_computer(self, data, nodename, selected_ou):
        ''' Registering computer '''

        self.logger.debug(
            'Register computer (%s, %s)...', nodename, selected_ou)

        reason = ''

        if not self._check_credentials(data):
            return False, reason

        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False, reason

        if selected_ou is None or selected_ou.strip() == '':
            self.logger.warn('selected_ou is empty!')
            return False, reason

        # Register in the server
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/register/computer/".format(url)
            self.logger.debug('Try to connect to: %s', url)
            user = data.get_login()
            password = data.get_password()

            payload = {
                'node_id': nodename,
                'ou_id': selected_ou
            }

            self.logger.debug('payload: %s', json.dumps(payload))

            r = requests.post(
                url,
                auth=(user,password),
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout,
                data=payload)
            if r.ok:
                self.logger.debug('Response: %s', url)
                response_json = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s', r.text)
                    response_json = json.loads(r.text)
                else:
                    self.logger.debug('Response: %s', r.content)
                    response_json = json.loads(r.content)

                if response_json is None:
                    self.logger.error(
                        'Error registering computer: NO RESPONSE')
                    return False, reason

                if not response_json["ok"]:
                    self.logger.error(
                        'Error registering computer: %s',
                        response_json['message'])
                    return False, response_json["reason"]

                return True, reason

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s', data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def register_chef_node(self, data, nodename):
        ''' Registering chef node '''

        self.logger.debug('Register computer (%s)...', nodename)

        if not self._check_credentials(data):
            return False

        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False

        # Register in the Chef Node
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/register/node/".format(url)
            self.logger.debug('Try to connect to: %s', url)
            user = data.get_login()
            password = data.get_password()

            payload = {'node_id': nodename}
            self.logger.debug('payload: %s', json.dumps(payload))
            rq = requests.post(
                url,
                auth=(user,password),
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout,
                data=payload)
            if rq.ok:
                self.logger.debug('Response: %s', url)
                response_json = False
                if hasattr(rq,'text'):
                    self.logger.debug('Response: %s', rq.text)
                    response_json = json.loads(rq.text)
                else:
                    self.logger.debug('Response: %s', rq.content)
                    response_json = json.loads(rq.content)

                if response_json is None:
                    self.logger.error(
                        'Error registering computer: NO RESPONSE')
                    return False

                if not response_json["ok"]:
                    self.logger.error(
                        'Error registering computer: %s',
                        response_json['message'])
                    return False

                return response_json["client_private_key"]

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s', data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def reregister_chef_node(self, data, nodename):
        ''' Re-registering computer '''

        self.logger.debug('Re-Register computer (%s)...', nodename)

        if not self._check_credentials(data):
            return False

        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False

        # Register in the Chef Node
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/register/node/".format(url)
            self.logger.debug('Try to connect to: %s', url)
            user = data.get_login()
            password = data.get_password()

            payload = {'node_id': nodename}
            self.logger.debug('payload: %s', json.dumps(payload))
            r = requests.put(
                url,
                auth=(user,password),
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout,
                data=payload)
            
            if r.ok:
                self.logger.debug('Response: %s', url)
                response_json = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s', r.text)
                    response_json = json.loads(r.text)
                else:
                    self.logger.debug('Response: %s', r.content)
                    response_json = json.loads(r.content)

                if response_json is None:
                    self.logger.error(
                        'Error registering computer: NO RESPONSE')
                    return False

                if not response_json["ok"]:
                    self.logger.error(
                        'Error registering computer: %s',
                        response_json['message'])
                    return False

                return response_json["client_private_key"]

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s', data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def unregister_chef_node(self, data, nodename):
        ''' Unregistering Chef node '''

        self.logger.debug('Unregister Chef node (%s)...', nodename)

        if not self._check_credentials(data):
            return False

        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False

        # Unregister the Chef Node
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/register/node/?node_id={}".format(url, nodename)
            self.logger.debug('Try to connect to: %s', url)
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }
            user = data.get_login()
            password = data.get_password()
            r = requests.delete(
                url,
                auth=(user,password),
                headers=headers,
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s', url)
                response_json = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s', r.text)
                    response_json = json.loads(r.text)
                else:
                    self.logger.debug('Response: %s', r.content)
                    response_json = json.loads(r.content)

                if response_json is None:
                    self.logger.error(
                        'Error unregistering computer: NO RESPONSE')
                    return False

                if not response_json["ok"]:
                    self.logger.error(
                        'Error unregistering computer: %s',
                        response_json['message'])
                    return False

                return True

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s',
                data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False

    def is_registered_chef_node(self, data, nodename):
        ''' Is registered Chef node ? '''

        self.logger.debug('IsRegistered? Chef node (%s)...', nodename)

        if not self._check_credentials(data):
            return False

        if nodename is None or nodename.strip() == '':
            self.logger.warn('nodename is empty!')
            return False

        # Unregister the Chef Node
        try:
            url = str(data.get_url())
            if url.endswith('/'):
                url = url[0:-1]
            url = "{}/register/node/?node_id={}".format(url, nodename)
            self.logger.debug('Try to connect to: %s', url)
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }
            user = data.get_login()
            password = data.get_password()
            r = requests.get(
                url,
                auth=(user,password),
                headers=headers,
                verify=SSLUtil.isSSLCertificatesVerificationEnabled(),
                timeout=self.timeout)
            if r.ok:
                self.logger.debug('Response: %s', url)
                response_json = False
                if hasattr(r,'text'):
                    self.logger.debug('Response: %s', r.text)
                    response_json = json.loads(r.text)
                else:
                    self.logger.debug('Response: %s', r.content)
                    response_json = json.loads(r.content)

                if response_json is None:
                    self.logger.error(
                        'Error unregistering computer: NO RESPONSE')
                    return False

                if not response_json["ok"]:
                    self.logger.error(
                        'Error unregistering computer: %s',
                        response_json['message'])
                    return False

                return True

            self.logger.debug('Response: NOT OK')

        except Exception:
            self.logger.warn(
                'Error connecting to Gecos server: %s',
                data.get_url())
            self.logger.warn(str(traceback.format_exc()))

        return False
