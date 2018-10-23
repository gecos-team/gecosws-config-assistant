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
import gettext
from gettext import gettext as _
from GladeWindow import GladeWindow
from gi.repository import Gtk

gettext.textdomain('gecosws-config-assistant')

class LocalUserListDialog(GladeWindow):
    '''
    Dialog class that shows the local users list, redone in glade.
    '''

    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('LocalUserListDialog')
        self.gladepath = 'localusers.glade'

        self.data = None

        self.selection_index = -1

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
        self.view = self.getElementById('treeview2')

        self.store.clear()

        column = Gtk.TreeViewColumn('Login', Gtk.CellRendererText(), text=0)
        column.set_clickable(True)
        column.set_resizable(True)
        self.view.append_column(column)

        column = Gtk.TreeViewColumn('Name', Gtk.CellRendererText(), text=1)
        column.set_clickable(True)
        column.set_resizable(True)
        self.view.append_column(column)

        # add selection handler
        select = self.view.get_selection()
        select.connect("changed", self.on_selection_changed)

        self.logger.debug('UI initiated')

    def extractGUIElements(self):
        ''' Extract GUI elements '''

        self.logger.debug('Extract GUI elements')

        self.dialog            = self.getElementById('window1')

        self.explanationLabel1 = self.getElementById('label1')
        self.explanationLabel2 = self.getElementById('label2')
        self.explanationLabel4 = self.getElementById('label3')

        self.newUserButton     = self.getElementById('button1')
        self.updateUserButton  = self.getElementById('button2')
        self.deleteUserButton  = self.getElementById('button3')
        self.closeButton       = self.getElementById('button4')

        self.ysb               = self.getElementById('adjustment1')
        self.xsb               = self.getElementById('adjustment2')

        self.treeview          = self.view

    def show(self):
        ''' Show '''

        self.logger.debug("Show")
        self.extractGUIElements()

        self.refresh()

        self.window.set_modal(True)
        self.window.set_transient_for(self.parent.window)
        self.window.show_all()

        x, y = self.parent.window.get_position()
        w, h = self.parent.window.get_size()
        sw, sh = self.window.get_size()
        self.logger.debug('x={} y={} w={} h={} sw={} sh={}'.format(
            x, y, w, h, sw, sh))
        self.window.move(x + w/2 - sw/2, y + h/2 - sh/2)

        while Gtk.events_pending():
            Gtk.main_iteration()

    def addHandlers(self):
        ''' Adding handlers '''

        self.handlers = self.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding new handler")
        self.handlers["onNeww"] = self.new
        self.logger.debug("Adding update handler")
        self.handlers["onUpdt"] = self.update
        self.logger.debug("Adding delete handler")
        self.handlers["onDelt"] = self.delete
        self.logger.debug("Adding go back handler")
        self.handlers["onBack"] = self.goBack

    def on_selection_changed(self, selection):
        ''' Event onchange '''

        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.my_model = model
            self.selection_index = treeiter

    def refresh(self):
        ''' Refresh '''

        self.store.clear()
        data = self.get_data()
        if data is not None:
            for user in data:
                self.store.append([user.get_login(), user.get_name()])

    def goBack(self, *args):
        ''' Go back '''

        self.logger.debug("Go Back")
        self.dialog.destroy()

    def new(self, *args):
        ''' New '''

        self.logger.debug("New")
        self.localUserController.newElement()

    def setLocalUserController(self, localUserController):
        ''' Setting local user controller '''

        self.localUserController = localUserController

    def _get_selected_user(self):
        if(
            self.selection_index != -1 and
            self.my_model[self.selection_index] != None
        ):
            login = self.my_model[self.selection_index][0]
            data = self.get_data()
            if data is not None:
                for user in data:
                    if user.get_login() == login:
                        return user

    def _get_selected_user_old(self):
        ''' Get selected user old '''

        if (
            self.treeview.selection() is not None and
            isinstance(self.treeview.selection(), tuple)
        ):
            selected = self.treeview.selection()[0]
            item = self.treeview.item(selected)
            login = item["values"][0]
            self.logger.debug("login = %s", login)

            data = self.get_data()
            if data is not None:
                for user in data:
                    if user.get_login() == login:
                        return user
        else:
            self.logger.debug("No user selected")

        return None

    def update(self, *args):
        ''' Update '''

        self.logger.debug("New")
        user = self._get_selected_user()
        if user is None:
            self.logger.error("Strange error: User is None!")
            return

        self.localUserController.updateElement(user)

    def delete(self, *args):
        ''' Delete '''

        self.logger.debug("Delete")
        user = self._get_selected_user()
        if user is None:
            self.logger.error("Strange error: User is None!")
            return

        self.localUserController.deleteElement(user)


    data = property(
        get_data,
        set_data,
        None,
        None)

        
