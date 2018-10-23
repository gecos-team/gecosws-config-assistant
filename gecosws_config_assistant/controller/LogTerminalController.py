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

__author__ = "Francisco Fuentes Barrera <ffuentes@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"

import logging
from gecosws_config_assistant.view.LogTerminalDialog import LogTerminalDialog


class LogTerminalController(object):
    '''
    Controller class for the "show system status" functionality.
    '''

    def __init__(self, mainController):
        '''
        Constructor
        '''
        self.controller = mainController
        self.view = None
        self.logger = logging.getLogger('LogTerminalController')


    def show(self):
        ''' Show log '''
        self.view = LogTerminalDialog(self, self.controller.window)
        self.view.show()

    def hide(self):
        ''' Hide log '''
        # TODO implement this method
        pass
