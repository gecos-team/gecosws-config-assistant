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

import gettext
from gettext import gettext as _

from gecosws_config_assistant.dto.UserAuthenticationMethod import (
    UserAuthenticationMethod)

gettext.textdomain('gecosws-config-assistant')

class LocalUsersAuthMethod(UserAuthenticationMethod):
    '''
    DTO object that represents the necessary data to setup the local users
    authentication method.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.data = None

    def get_name(self):
        ''' Getter name '''

        return _('Internal')

    def set_data(self, value):
        raise TypeError('No data defined for LocalUsersAuthMethod')
