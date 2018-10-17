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
from gi.repository import GLib, Gtk, GObject
import logging
import threading
import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData

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
        self.buildUI(self.gladepath)
        label = self.getElementById('label1')
        label.set_label(_('Loading ...'))
        self.logger.debug('UI initiated')

    def show(self):
        width = super(SplashScreen, self).getWidth()
        height = super(SplashScreen, self).getHeight()
        self.window.set_size_request(width, height)
        self.window.show_all()
        #Gtk.main()

    def hide(self):
        self.window.destroy()
