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

from dto.NTPServer import NTPServer
from util.PackageManager import PackageManager
from util.Template import Template

import logging
import traceback

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class NTPServerDAO(object):
    '''
    DAO class to manipulate NTPServer DTO objects.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.logger = logging.getLogger('NTPServerDAO')
        self.initiated = False
        
        # Check if 'ntpdate' package exists
        self.pm = PackageManager()
        if not self.pm.is_package_installed('ntpdate'):
            # Try to install the package
            try:
                self.pm.install_package('ntpdate')
                self.initiated = True
            except Exception:
                self.logger.error(_('Package installation failed:'), 'ntpdate')
                self.logger.error(str(traceback.format_exc())) 
        else:
            self.initiated = True               
        

    def load(self):
        ntpServer = None
        
        if self.initiated:
            # Get server from /etc/default/ntpdate
            try:
                address = None
                with open('/etc/default/ntpdate') as fp:
                    for line in fp:
                        if line.startswith('NTPSERVERS='):
                            address = line[len('NTPSERVERS='):]
                            break
                
                if address is not None:
                    address = address.replace('"', '')
                    address = address.strip()
                    ntpServer = NTPServer()
                    ntpServer.set_address(address)     
                
            except Exception:
                self.logger.error(_('Error reading file:'), '/etc/default/ntpdate')
                self.logger.error(str(traceback.format_exc()))             
            
        else:
            self.logger.warn(_('NTPServerDAO used without a proper initialization!'))
        
        
        return ntpServer


    def save(self, ntp_server):
        if ntp_server is None:
            raise ValueError('ntp_server is None')
        
        if not isinstance(ntp_server, NTPServer):
            raise ValueError('ntp_server is not a NTPServer instance')
            
        if self.initiated:
            # Check the previous value
            previous = self.load()
            if previous is not None and previous.get_address() == ntp_server.get_address():
                return
            
            # Save the value to /etc/default/ntpdate
            template = Template()
            template.source = 'templates/ntpdate'
            template.destination = '/etc/default/ntpdate'
            template.owner = 'root'
            template.group = 'root'
            template.mode = 00644
            template.variables = { 'ntp_server':  ntp_server.get_address()}
            
            template.save()
            
        else:
            self.logger.warn(_('NTPServerDAO used without a proper initialization!'))
        
        

    def delete(self, ntp_server):
        raise TypeError('Can not delete the NTP server configuration!')







