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

from dto.GecosAccessData import GecosAccessData
from util.JSONUtil import JSONUtil
from util.Template import Template

import logging
import traceback
import os

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class GecosAccessDataDAO(object):
    '''
    DAO class to manipulate GecosAccessData DTO objects.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.logger = logging.getLogger('GecosAccessDataDAO')
        self.data_file = '/etc/gcc.control'
            
           

    def load(self):
        self.logger.debug('load - BEGIN')
        data = GecosAccessData()
        

        # Get data from data file
        jsonUtil = JSONUtil()
        json_data = jsonUtil.loadJSONFromFile(self.data_file)
        if json_data is not None:
            
            data.set_login(json_data['gcc_username'])
            data.set_url(json_data['uri_gcc'])
            
            # Password is not stored!
            data.set_password(None)
            
        if (data.get_url() is None or data.get_url().strip()==''):
            data = None
            
        self.logger.debug('load - END')
        return data


    def save(self, data):
        self.logger.debug('save - BEGIN')
        
        if data is None:
            raise ValueError('data is None')
        
        if not isinstance(data, GecosAccessData):
            raise ValueError('data is not a GecosAccessData instance')        
        
        # Get data from data file
        jsonUtil = JSONUtil()
        json_data = jsonUtil.loadJSONFromFile(self.data_file)
        gcc_nodename = ''
        if json_data is not None:
            gcc_nodename = json_data['gcc_nodename']
                    
        # Save data to data file
        template = Template()
        template.source = 'templates/gcc.control'
        template.destination = self.data_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00755
        template.variables = { 
            'uri_gcc':  data.get_url(), 
            'gcc_username':  data.get_login(), 
            'gcc_nodename':  gcc_nodename, 
        }        
        
        template.save()

        self.logger.debug('save - END')

        
    def delete(self, data):
        self.logger.debug('delete - BEGIN')
        
        if data is None:
            raise ValueError('data is None')
        
        if not isinstance(data, GecosAccessData):
            raise ValueError('data is not a GecosAccessData instance')        
 
        
        # Remove data file
        try:
            if os.path.isfile(self.data_file):
                os.remove(self.data_file)
            
        except Exception:
            self.logger.error(_('Error removing file:') + self.data_file)
            self.logger.error(str(traceback.format_exc()))             
        
        self.logger.debug('delete - END')        








