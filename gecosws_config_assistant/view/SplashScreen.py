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

import logging
import gettext
from gettext import gettext as _
from gecosws_config_assistant.view.GladeWindow import GladeWindow

gettext.textdomain('gecosws-config-assistant')

class SplashScreen(GladeWindow):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('SplashScreen')
        self.gladepath = 'splash.glade'
        self.initUI()


    def initUI(self):
        ''' Initialize UI '''

        self.buildUI(self.gladepath)
        label = self.getElementById('label1')
        label.set_label(_('Loading ...'))
        self.logger.debug('UI initiated')

    def show(self):
        ''' Show '''

        width = self.getWidth()
        height = self.getHeight()
        self.window.set_size_request(width, height)
        self.window.show_all()
        #Gtk.main()

    def hide(self):
        ''' Hide '''

        self.window.destroy()

    def getWidth(self):
        ''' Override parent method. Splash window width adjusted '''

        return 350

    def getHeight(self):
        ''' Override parent method. Splash window height adjusted'''

        return 100
