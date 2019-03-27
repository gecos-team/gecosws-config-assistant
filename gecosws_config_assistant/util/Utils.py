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

__author__ = "Jose M. Rodriguez Caro <jmrodriguez@gruposolutia.com"
__copyright__ = "Copyright (C) 2019, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"

from enum import Enum
from gecosws_config_assistant.util.CommandUtil import CommandUtil

import logging
logger = logging.getLogger('Utils')

class System_Manager(Enum):
    SYSV = 1
    UPSTART = 2
    SYSTEMD = 3

class Utils(object):
    '''
    Miscelanea utilities
    '''
    
    @staticmethod
    def get_system_manager():
        '''
        Detecting which system manager is running
        ''' 
        sysmanager = None
        commandUtil = CommandUtil()

        output = commandUtil.get_command_output('ls -l /proc/1/exe')
        line = output[0]

        if line.endswith('/sbin/init'):
            sysmanager = System_Manager.SYSV
        elif line.endswith('/sbin/upstart'):
            sysmanager = System_Manager.UPSTART
        elif line.endswith('/lib/systemd/systemd'):
            sysmanager = System_Manager.SYSTEMD

        return sysmanager
 
