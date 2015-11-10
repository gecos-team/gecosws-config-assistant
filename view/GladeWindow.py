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

from gi import Gtk, Gdk
import time
import view 

class GladeWindow(object):
    def __init__(self, gladepath):
        self.gladepath = gladepath
        self.builder = Gtk.Builder(GLADE_PATH+gladepath)
        self.builder.connect_signals({"closeApplication": Gtk.main_quit})
        
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path(CSS_PATH+CSS_COMMON)
        
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        showUI()
        
    def showUI(self):
        self.window = self.builder.get_object("window1")
        self.window.show_all()
        Gtk.main()