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

from GladeWindow import GladeWindow
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class RequirementsCheckDialog(GladeWindow):
    '''
    Dialog class that shows the "requirements check" menu.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('RequirementsCheckDialog')
        self.gladepath = 'requirements.glade'
        
        self.initUI()        


    def initUI(self):
        self.logger.debug('Initiating UI')
        self.buildUI(self.gladepath)
        
        self.logger.debug('UI initiated')
        
    def addHandlers(self):
        self.logger.debug("Adding all handlers")
        self.handlers = self.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding network management handler")
        self.handlers["onNetw"] = self.showNetworkInterfaces
        self.logger.debug("Adding autoconf handler")
        self.handlers["onAuto"] = self.showAutoSetup
        self.logger.debug("Adding NTP handler")
        self.handlers["onnNTP"] = self.showNTPServer
        
    def show(self):
        self.logger.debug("Show")
        self.parent.navigate(self)

    def close(self):
        self.logger.debug("Close")
        self.destroy()


    def showNetworkInterfaces(self, *args):
        self.logger.debug("showNetworkInterfaces")
        self.controller.showNetworkInterfaces()

    def showAutoSetup(self, *args):
        self.logger.debug("showAutoSetup")
        self.controller.showAutoSetup()

    def showNTPServer(self, *args):
        self.logger.debug("showNTPServer")
        self.controller.showNTPServer()

        