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
import traceback
import os
import hashlib
import socket
import fcntl
import struct

from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.dao.NetworkInterfaceDAO import (
    NetworkInterfaceDAO)
from gecosws_config_assistant.util.JSONUtil import JSONUtil
from gecosws_config_assistant.util.Template import Template
from gecosws_config_assistant.firstboot_lib.firstbootconfig import (
    get_data_file)
from gecosws_config_assistant.util.SSLUtil import SSLUtil

class GecosAccessDataDAO(object):
    '''
    DAO class to manipulate GecosAccessData DTO objects.
    '''

    # Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GecosAccessDataDAO, cls).__new__(
                                cls, *args, **kwargs)
            cls._instance.previous_saved_data = None
        return cls._instance


    def __init__(self):
        '''
        Constructor
        '''

        self.logger = logging.getLogger('GecosAccessDataDAO')
        self.data_file = '/etc/gcc.control'

    def previousDataExists(self):
        ''' Previous data exists '''
        ret = False
        if self.previous_saved_data != None:
            ret = True

        return ret

    def load(self):
        ''' Loading data '''
        self.logger.debug('load - BEGIN')
        data = GecosAccessData()

        # Check previous saved data (in memory cache)
        if self.previous_saved_data is not None:
            return self.previous_saved_data

        # Get data from data file
        jsonUtil = JSONUtil()
        json_data = jsonUtil.loadJSONFromFile(self.data_file)
        if json_data is not None:

            data.set_login(json_data['gcc_username'].encode('utf-8'))
            data.set_url(json_data['uri_gcc'].encode('utf-8'))

            # Password is not stored!
            data.set_password(None)

        if data.get_url() is None or data.get_url().strip()=='':
            data = None

        self.logger.debug('load - END')
        return data

    def _getHwAddr(self, ifname):
        ''' Getting hardware address '''
        self.logger.debug("Getting hardware address")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(
            s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )
        return ''.join(['%02x:' % char for char in info[18:24]])[:-1]

    def calculate_workstation_node_name(self):
        ''' Calculates workstation node name '''
        networkDao = NetworkInterfaceDAO()
        interfaces = networkDao.loadAll()
        no_localhost_name = None
        for inter in interfaces:
            if not inter.get_ip_address().startswith('127.0'):
                no_localhost_name = inter.get_name()
                break
        self.logger.debug("Selected interface name is: %s", no_localhost_name)
        mac = self._getHwAddr(no_localhost_name)
        gcc_nodename = hashlib.md5(mac.encode()).hexdigest()
        self.logger.debug("New node name is: %s", gcc_nodename)
        return gcc_nodename

    def save(self, data):
        ''' Saving data '''
        self.logger.debug('save - BEGIN')

        if data is None:
            raise ValueError('data is None')

        if not isinstance(data, GecosAccessData):
            raise ValueError('data is not a GecosAccessData instance')

        # Insert the data in cache memory
        self.previous_saved_data = data

        # Get gcc_nodename from data file
        try:
            jsonUtil = JSONUtil()
            json_data = jsonUtil.loadJSONFromFile(self.data_file)
            gcc_nodename = ''
            if json_data is not None:
                gcc_nodename = json_data['gcc_nodename']

            if gcc_nodename is None or gcc_nodename.strip() == '':
                gcc_nodename = self.calculate_workstation_node_name()
        except Exception:
            # Can't get gcc_nodename from file, calculate it
            gcc_nodename = self.calculate_workstation_node_name()

        # Save data to data file
        template = Template()
        template.source = get_data_file('templates/gcc.control')
        template.destination = self.data_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 0o00755
        url = data.get_url()
        if url.endswith('/'):
            url = url[0:-1]
        template.variables = {
            'uri_gcc':  url,
            'gcc_username':  data.get_login(),
            'gcc_nodename':  gcc_nodename,
            'ssl_verify': SSLUtil.isSSLCertificatesVerificationEnabled()
        }

        return template.save()

    def delete(self, data):
        ''' Deleting data '''
        self.logger.debug('delete - BEGIN')

        if data is None:
            raise ValueError('data is None')

        if not isinstance(data, GecosAccessData):
            raise ValueError('data is not a GecosAccessData instance')

        # Remove data from memory
        self.previous_saved_data = None

        # Remove data file
        try:
            if os.path.isfile(self.data_file):
                os.remove(self.data_file)

            return True
        except Exception:
            self.logger.error('Error removing file:' + self.data_file)
            self.logger.error(str(traceback.format_exc()))

        self.logger.debug('delete - END')
        return False
