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
MainMenu redone in Glade
"""
class MainMenuDialog(GladeWindow):
    
    def __init__(self, mainController):
        self.controller = mainController
        self.gladePath = 'main.glade'
        self.logger = logging.getLogger('MainMenuDialog')
        
        self.buildUI(self.gladePath)
    
    def addTranslations(self):
        super(MainMenuDialog, self).addTranslations()
    
    def addHandlers(self):
        super(MainMenuDialog, self).addHandlers()
        self.logger.info('Calling child specific handler')
        # add new handlers here
        self.logger.debug("Adding link/unlink handler")
        self.handlers["onLink"] = self.connectWithGECOSHandler
        self.logger.debug("Adding auth management handler")
        self.handlers["onAuth"] = self.authManagementHandler
        self.logger.debug("Adding network management handler")
        self.handlers["onNetw"] = self.netManagementHandler
        self.logger.debug("Adding autoconf handler")
        self.handlers["onAuto"] = self.autoconfManagementHandler
        self.logger.debug("Adding help1 handler")
        self.handlers["onHlp1"] = self.help1ManagementHandler
        self.logger.debug("Adding help2 handler")
        self.handlers["onHlp2"] = self.help2ManagementHandler
    
    # Here comes the handlers
    def connectWithGECOSHandler(self, *args):
        self.logger.info('This should display the gecos connection settings')
        
    def authManagementHandler(self, *args):
        self.logger.info('This should display the auth settings')
    
    def netManagementHandler(self, *args):
        self.logger.info('This should display the network settings')
    
    def autoconfManagementHandler(self, *args):
        self.logger.info('This should call the autoconf method or whatever')
    
    def help1ManagementHandler(self, *args):
        self.logger.info('This should show a brief help about GECOS linking')
    
    def help2ManagementHandler(self, *args):
        self.logger.info('This should show a brief help about auth modes')
    
    
    # old methods, just pasted for copypaste sake
    def showRequirementsCheckDialog(self):
        self.logger.debug("showRequirementsCheckDialog")
        self.controller.showRequirementsCheckDialog()

    def showConnectWithGecosCCDialog(self):
        self.logger.debug("showConnectWithGecosCCDialog")
        self.controller.showConnectWithGecosCCDialog()

    def showUserAuthenticationMethod(self):
        self.logger.debug("showUserAuthenticationMethod")
        self.controller.showUserAuthenticationMethod()
        
    def showSoftwareManager(self):
        self.logger.debug("showSoftwareManager")
        self.controller.showSoftwareManager()
        
    def showLocalUserListView(self):
        self.logger.debug("showLocalUserListView")
        self.controller.showLocalUserListView()
        
    def updateConfigAssistant(self):
        self.logger.debug("updateConfigAssistant")
        self.controller.updateConfigAsystant()
        
    def showSystemStatus(self):
        self.logger.debug("showSystemStatus")
        self.controller.showSystemStatus()