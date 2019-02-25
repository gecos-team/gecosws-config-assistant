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

import subprocess
import re
import logging
from gecosws_config_assistant.util.Template import Template
from gecosws_config_assistant.util.Utils import Utils, System_Manager
from gecosws_config_assistant.firstboot_lib.firstbootconfig import (
    get_data_file)

class NTPServer(object):
    '''
    DTO object that represents a NTP server.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.address = ''
        self.logger = logging.getLogger('NTPServer')

    def syncrhonize(self):
        ''' Syncronizing time with systemd-timesyncd service '''

        if self.address is None or self.address.strip() == '':
            return False
        else:
            sysmanager = Utils.get_system_manager()
            if sysmanager == System_Manager.SYSV or sysmanager == System_Manager.UPSTART:
                p = subprocess.Popen(
                    'ntpdate-debian -u {}'.format(self.address),
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
                retval = p.wait()
                return retval == 0	

            elif sysmanager == System_Manager.SYSTEMD:
                template = Template()
                template.source = get_data_file('templates/timesyncd.conf')
                template.destination = '/etc/systemd/timesyncd.conf'
                template.owner = 'root'
                template.group = 'root'
                template.mode = 00644
                template.variables = { 'ntp_server':  self.address }
                template.save()

                subprocess.call(["systemctl", "enable", "systemd-timesyncd.service"])
                subprocess.call(["systemctl", "start", "systemd-timesyncd.service"])
                subprocess.call(["timedatectl", "set-local-rtc", "0"])
                subprocess.call(["timedatectl", "set-ntp", "true"])
                subprocess.call(["systemctl", "restart", "systemd-timesyncd.service"])
            
                p = subprocess.Popen(
                    "timedatectl status", 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)

                for line in p.stdout.readlines():
                    if re.match(r'NTP synchronized: yes', line):
                        self.logger.debug('NTP synchronized: %s', self.address)
                        return True

                self.logger.debug('NTP unsynchronized: %s', self.address)
                return False

    def get_address(self):
        ''' Getter address '''

        return self.__address

    def set_address(self, value):
        ''' Setter address '''

        self.__address = value

    address = property(
        get_address,
        set_address,
        None,
        None)
