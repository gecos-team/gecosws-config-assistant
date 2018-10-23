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
import os
import gettext
from gettext import gettext as _
from gecosws_config_assistant.view.GladeWindow import GladeWindow
from gi.repository import Gtk

gettext.textdomain('gecosws-config-assistant')

class NetworkInterfaceListView(GladeWindow):
    '''
    Dialog class that shows the "network interfaces" list.
    '''

    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('NetworkInterfaceListView')
        self.gladepath = 'network.glade'

        self.data = None

        self.initUI()

    def get_data(self):
        ''' Getter data '''

        return self.__data

    def set_data(self, value):
        ''' Setter data '''

        self.__data = value

    def initUI(self):
        ''' Initialize UI '''

        self.buildUI(self.gladepath)

        self.store = self.getElementById('liststore1')
        self.view = self.getElementById('treeview1')

        self.store.clear() 

        column = Gtk.TreeViewColumn('Interface', Gtk.CellRendererText(), text=0)   
        column.set_clickable(True)
        column.set_resizable(True)
        self.view.append_column(column)

        column = Gtk.TreeViewColumn('IP', Gtk.CellRendererText(), text=1)
        column.set_clickable(True)
        column.set_resizable(True)
        self.view.append_column(column)

        self.logger.debug('UI initiated')

    def addHandlers(self):
        ''' Adding handlers '''

        self.handlers = self.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding go back handler")
        self.handlers["onBack"] = self.close
        self.logger.debug("Adding setup network connection handler")
        self.handlers["onSetp"] = self.setupNetworkConnection

    def show(self):
        ''' Show '''

        self.logger.debug("Show")

        data = self.get_data()
        if data is not None:
            for ni in data:
                self.store.append([ni.get_name(), ni.get_ip_address()])

        self.parent.navigate(self)

    def close(self, *args):
        ''' Close '''

        self.logger.debug("Close")
        self.controller.hide()

    def setupNetworkConnection(self, *args):
        ''' Setting network connection '''

        self.logger.debug("setupNetworkConnection")
        cmd = 'nm-connection-editor'
        os.spawnlp(os.P_NOWAIT, cmd, cmd)

    data = property(
        get_data,
        set_data,
        None,
        None)

    def getHeight(self):
        return 250
