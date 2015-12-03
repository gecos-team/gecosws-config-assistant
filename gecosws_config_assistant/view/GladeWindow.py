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

from gi.repository import Gtk, Gdk
from gecosws_config_assistant.view import GLADE_PATH, CSS_PATH, CSS_COMMON 
"""
Abstract parent class for any Gtk window used in GECOS
"""
class GladeWindow(object):
    def __init__(self, mainController):
        raise NotImplementedError( "This is an abstract class that cannot be instantiated" )
        
    def buildUI(self, gladepath):
        self.logger.debug("Building UI")
        
        self.gladepath = gladepath
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain('gecosws-config-assistant')
        self.builder.add_from_file(GLADE_PATH+self.gladepath)
        
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path(CSS_PATH+CSS_COMMON)
        
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(
            Gdk.Screen.get_default(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        # main window
        self.window = self.getElementById("window1")
        # center frame, here we'll do the transformations to keep all in the same window
        self.frame = self.getCentralFrame()
        
        self.addHandlers()
        self.bindHandlers()
    
    def getMainWindow(self):
        return self.window
    
    def show(self):
        self.window.show_all()
        Gtk.main()
    
    def addHandlers(self):
        self.logger.debug("Adding all handlers")
        self.handlers = {}
        # handling common hooks
        self.addCloseHandler()
        
    def addCloseHandler(self):
        self.logger.debug("Adding close handlers")
        self.handlers['onDeleteWindow'] = Gtk.main_quit
    
    def bindHandlers(self):
        self.logger.debug("Binding handlers")
        self.builder.connect_signals(self.handlers)
    
    def getCentralFrame(self):
        return self.getElementById("frame2")
    
    def getElementById(self, id_):
        return self.builder.get_object(id_)
    
    def getWidth(self):
        # Default width
        return 600
        
    def getHeight(self):
        # Default height
        return 300    