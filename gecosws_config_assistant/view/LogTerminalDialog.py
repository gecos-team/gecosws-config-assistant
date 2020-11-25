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
import fcntl
import os
from subprocess import Popen, PIPE
from gi.repository import Gtk, Pango, GObject

from gecosws_config_assistant.view.GladeWindow import GladeWindow

gettext.textdomain('gecosws-config-assistant')

class LogTerminalDialog(GladeWindow):
    '''
    Dialog class that shows the system status.
    '''

    def __init__(self, controller, parent):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = controller
        self.logger = logging.getLogger('LogTerminalDialog')
        self.gladepath = 'logterminal.glade'

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
        self.logger.debug('UI initiated')

    def initTerminal(self):
        ''' Initialize terminal '''

        self.sub_proc = Popen(
            "tail -n 200 -f /tmp/gecos-config-assistant.log",
            shell=True,
            stdout=PIPE)
        self.sub_outp = ""

    def non_block_read(self, output):
        ''' Non block read '''

        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except:
            return ''

    def update_terminal(self):
        ''' Update terminal '''

        self.textBuffer.insert_at_cursor(
            self.non_block_read(self.sub_proc.stdout).decode("utf-8"))
        return self.sub_proc.poll() is None

    def extractGUIElements(self):
        ''' Extract GUI elements '''

        self.window       = self.getElementById('window1')
        self.acceptButton = self.getElementById('button1')
        self.statusText   = self.getElementById('textview1')

        self.statusText.set_editable(False)
        self.statusText.set_cursor_visible(False)
        self.statusText.set_justification(Gtk.Justification.LEFT)
        self.statusText.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

        self.textBuffer   = self.statusText.get_buffer()

        self.dialog       = self.window

    def modifyFont(self):
        ''' Modifying font '''

        fontdesc = Pango.FontDescription("monospace")
        self.statusText.modify_font(fontdesc)

    def addHandlers(self):
        ''' Adding handlers '''

        self.handlers = self.parent.get_common_handlers()

        # add new handlers here
        self.logger.debug("Adding back handler")
        self.handlers["onBack"] = self.goBack

    def show(self):
        ''' Show '''

        self.logger.debug("Show")
        self.extractGUIElements()
        self.modifyFont()
        self.initTerminal()
        self.window.set_title(_('Log terminal'))

        self.window.set_modal(True)
        self.window.set_transient_for(self.parent.window)

        GObject.timeout_add(100, self.update_terminal)

        self.window.show_all()

        x, y = self.parent.window.get_position()
        w, h = self.parent.window.get_size()
        sw, sh = self.window.get_size()
        self.logger.debug('x={} y={} w={} h={} sw={} sh={}'.format(
            x, y, w, h, sw, sh))
        self.window.move(x + w/2 - sw/2, y + h/2 - sh/2)

        while Gtk.events_pending():
            Gtk.main_iteration()

    def goBack(self, *args):
        ''' Go back '''

        self.logger.debug("Go back")
        self.dialog.destroy()

    data = property(
        get_data,
        set_data,
        None,
        None)
