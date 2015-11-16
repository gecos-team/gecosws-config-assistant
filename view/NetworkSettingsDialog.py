#!/usr/bin/env python
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
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from GladeWindow import GladeWindow
import logging
"""
Network settings redone in Glade
"""
class NetworkSettingsDialog(GladeWindow):
    def __init__(self, mainController):
        self.controller = mainController
        self.gladePath = 'network.glade'
        self.logger = logging.getLogger('NetworkSettingsDialog')
        
        self.buildUI(self.gladePath)
    
    def addTranslations(self):
        super(NetworkSettingsDialog, self).addTranslations()
    
    def addHandlers(self):
        super(NetworkSettingsDialog, self).addHandlers()
        self.logger.info('Calling child specific handler')
        # add new handlers here
        self.logger.debug("Adding go back handler")
        self.handlers["onBack"] = self.backToMainWindowHandler
    
    # Here comes the handlers
    def backToMainWindowHandler(self, *args):
        self.logger.debug('Back to the main window')
        self.controller.backToMainWindowDialog()
    
    def setToInitialState(self):
        pass
    
    def show(self):
        self.setToInitialState()
        # super method
        super(NetworkSettingsDialog, self).show()