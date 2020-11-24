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

from gecosws_config_assistant.dto.WorkstationData import WorkstationData
from gecosws_config_assistant.util.JSONUtil import JSONUtil
from gecosws_config_assistant.util.Template import Template
from gecosws_config_assistant.dao.NetworkInterfaceDAO import (
    NetworkInterfaceDAO)
from gecosws_config_assistant.firstboot_lib.firstbootconfig import (
    get_data_file)
from gecosws_config_assistant.util.SSLUtil import SSLUtil

class WorkstationDataDAO(object):
    '''
    DAO class to manipulate WorkstationData DTO objects.
    '''

    # Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WorkstationDataDAO, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        '''
        Constructor
        '''

        self.logger = logging.getLogger('WorkstationDataDAO')
        self.pclabel_file = '/etc/pclabel'
        self.gcc_control_file = '/etc/gcc.control'


    def load(self):
        ''' Loading '''

        self.logger.debug('load - BEGIN')
        data = WorkstationData()

        # Get name from pclabel file
        try:
            name = None
            with open(self.pclabel_file) as fp:
                for line in fp:
                    name = line

            if name is not None:
                name = name.replace('"', '')
                name = name.strip()
                data.set_name(name)

        except Exception:
            self.logger.error('Error reading file:'+ self.pclabel_file)
            self.logger.error(str(traceback.format_exc()))

        if name is None:
            # Get hostname as default name
            networkInterfaceDAO = NetworkInterfaceDAO()
            name = networkInterfaceDAO.get_hostname()

            if name is not None:
                name = name.replace("\"".encode(), "".encode())
                data.set_name(name)

        # Can't get OU from GECOS CC!!!

        # Get node name from gcc.control file
        jsonUtil = JSONUtil()
        json_data = jsonUtil.loadJSONFromFile(self.gcc_control_file)
        if json_data is not None:
            data.set_node_name(json_data['gcc_nodename'])

        if (
            (data.get_ou() is None or data.get_ou().strip()=='')  and
            (data.get_name() is None or data.get_name().strip()=='')
        ):
            data = None

        self.logger.debug('load - END')
        return data

    def save(self, data):
        ''' Saving '''

        self.logger.debug('save - BEGIN')

        if data is None:
            raise ValueError('data is None')

        if not isinstance(data, WorkstationData):
            raise ValueError('data is not a WorkstationData instance')

        if data is None:
            raise ValueError('data is None')

        # Save name to pclabel file
        try:
            fd = open(self.pclabel_file, 'w')
            if fd != None:
                fd.write(data.get_name())
                fd.close()

        except Exception:
            self.logger.error('Error writing file: %s', self.pclabel_file)
            self.logger.error(str(traceback.format_exc()))

        # Do not save OU in GECOS CC at this point!!

        # save node_name to gcc.control file
        jsonUtil = JSONUtil()
        json_data = jsonUtil.loadJSONFromFile(self.gcc_control_file)
        uri_gcc = ''
        gcc_username = ''
        if json_data is not None:
            uri_gcc = json_data['uri_gcc']
            gcc_username = json_data['gcc_username']

        template = Template()
        template.source = get_data_file('templates/gcc.control')
        template.destination = self.gcc_control_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 0o00755
        template.variables = {
            'uri_gcc':  uri_gcc,
            'gcc_username':  gcc_username,
            'gcc_nodename':  data.get_node_name(),
            'ssl_verify': SSLUtil.isSSLCertificatesVerificationEnabled()
        }

        template.save()

        self.logger.debug('save - END')

    def delete(self, data):
        ''' Deleting '''

        self.logger.debug('delete - BEGIN')

        if data is None:
            raise ValueError('data is None')

        if not isinstance(data, WorkstationData):
            raise ValueError('data is not a WorkstationData instance')

        if data.get_name() is None:
            raise ValueError('data.name is None')

        # Remove pclabel_file
        try:
            if os.path.isfile(self.pclabel_file):
                os.remove(self.pclabel_file)

        except Exception:
            self.logger.error('Error removing file: %s', self.pclabel_file)
            self.logger.error(str(traceback.format_exc()))

        # Eliminate node_name from gcc.control file
        jsonUtil = JSONUtil()
        json_data = jsonUtil.loadJSONFromFile(self.gcc_control_file)
        uri_gcc = ''
        gcc_username = ''
        if json_data is not None:
            uri_gcc = json_data['uri_gcc']
            gcc_username = json_data['gcc_username']

        template = Template()
        template.source = get_data_file('templates/gcc.control')
        template.destination = self.gcc_control_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 0o00755
        template.variables = {
            'uri_gcc':  uri_gcc,
            'gcc_username':  gcc_username,
            'gcc_nodename':  '',
            'ssl_verify': SSLUtil.isSSLCertificatesVerificationEnabled()
        }

        template.save()

        self.logger.debug('delete - END')
