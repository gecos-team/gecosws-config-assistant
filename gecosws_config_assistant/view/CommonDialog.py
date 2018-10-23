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

from gi.repository import Gtk

def showwarning_gtk(message, parent_window):
    ''' Showing warning gtk '''

    parent_window = None
    dialog = Gtk.MessageDialog(parent_window, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, message)
    dialog.run()
    dialog.destroy()

def showinfo_gtk(message, parent_window):
    ''' Showing info gtk '''

    parent_window = None
    dialog = Gtk.MessageDialog(parent_window, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, message)
    dialog.run()
    dialog.destroy()

def showerror_gtk(message, parent_window):
    ''' Showing error gtk '''

    parent_window = None
    dialog = Gtk.MessageDialog(parent_window, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, message)
    dialog.run()
    dialog.destroy()

def askyesno_gtk(message, parent_window):
    ''' Asking yes/no gtk '''

    msgtype = Gtk.MessageType.QUESTION
    if msgtype == 'warning':
        msgtype = Gtk.MessageType.WARNING
    parent_window = None
    dialog = Gtk.MessageDialog(parent_window, 0, msgtype,
            Gtk.ButtonsType.YES_NO, message)
    response = dialog.run()

    ret = None
    if response == Gtk.ResponseType.YES:
        ret = True
    elif response == Gtk.ResponseType.NO:
        ret = False

    dialog.destroy()

    return ret
