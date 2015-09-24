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
        return self.__last_request_content


    def set_last_request_content(self, value):
        self.logger.debug('set_last_request_content(%s)'%(value))
        self.__last_request_content = value

        
    def validate_credentials(self, data):
        self.logger.debug('Validating credentials...')
        return True            



    def get_json_autoconf(self, data):
        self.logger.debug('Getting auto setup data...')
        self.logger.debug("last request content: %s"%(self.get_last_request_content()))
        return json.loads(self.get_last_request_content())
    
    last_request_content = property(get_last_request_content, set_last_request_content, None, None)


