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

from dao.NTPServerDAO import NTPServerDAO
from dao.GecosAccessDataDAO import GecosAccessDataDAO
from dao.WorkstationDataDAO import WorkstationDataDAO
from dao.LocalUserDAO import LocalUserDAO
from dao.NetworkInterfaceDAO import NetworkInterfaceDAO
from dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO

import logging

class SystemStatusController(object):
    '''
    Controller class for the "show system status" functionality.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.view = None # TODO!
        self.gecosAccessDao = GecosAccessDataDAO()
        self.workstationDataDao = WorkstationDataDAO()
        self.localUserDao = LocalUserDAO()
        self.networkInterfaceDao = NetworkInterfaceDAO()
        self.ntpServerDao = NTPServerDAO()
        self.userAuthenticationMethodDao = UserAuthenticationMethodDAO()
        self.logger = logging.getLogger('SystemStatusController')

    def show(self):
        # TODO!
        pass

    def hide(self):
        # TODO!
        pass
    

