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
            subprocess.call(["systemctl", "enable", "systemd-timesyncd.service"])
            subprocess.call(["systemctl", "start", "systemd-timesyncd.service"])
            subprocess.call(["timedatectl", "set-ntp", "true"])
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
