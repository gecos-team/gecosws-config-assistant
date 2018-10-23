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

import logging
import json

class GecosCC(object):
    '''
    Utility class to communicate with the Gecos Control Center.
    '''

    # Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GecosCC, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('GecosCC')
        #self.last_request_content = ''

    def get_last_request_content(self):
        ''' Getting last request content '''

        return self.__last_request_content

    def set_last_request_content(self, value):
        ''' Setting last request content '''

        self.logger.debug('set_last_request_content(%s)', value)
        self.__last_request_content = value

    def validate_credentials(self, data):
        ''' Validating credentials '''

        self.logger.debug('Validating credentials...')
        return True            

    def get_json_autoconf(self, data):
        ''' Getting auto setup data '''

        self.logger.debug('Getting auto setup data...')
        self.logger.debug(
            "last request content: %s", self.get_last_request_content())
        return json.loads(self.get_last_request_content())

    def get_computer_names(self, data):
        ''' Get all computer names by text '''

        self.logger.debug('Get all computer names by text...')
        return [
            {
                "node_chef_id": "a48b2f532c009e1d328cfa83c923ee58",
                "name": "testgecos3"
            }
        ]

    def search_ou_by_text(self, data, searchFilter):
        ''' Search OU by text '''

        self.logger.debug('Search ou by text...')
        return [
            ["5566df5f1d5e265de2047434", "users"],
            ["5566df6d1d5e265de2047436", "computers"],
            ["5566df7b1d5e265ddcb59a63", "groups"],
            ["5566df4f1d5e265ddcb59a61", "pruebas.es"]
        ]

    def unregister_computer(self, data, nodename):
        ''' Unregister computer '''

        self.logger.debug('Unregister computer...')
        return True

    def register_computer(self, data, nodename, selected_ou):
        ''' Register computer '''

        self.logger.debug('Register computer (%s, %s)...',
                          nodename, selected_ou)
        return True

    def get_file_content_from_url(self, url):
        ''' Getting file content from url '''

        self.logger.debug('get_file_content_from_url (%s)...', url)
        return None


    last_request_content = property(
        get_last_request_content,
        set_last_request_content,
        None,
        None)
