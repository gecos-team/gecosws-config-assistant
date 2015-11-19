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

import logging
from gi.repository import Gtk, Gdk
from view import GLADE_PATH, CSS_PATH, CSS_COMMON 

class MainWindow(object):
    def __init__(self, mainController):
        self.controller = mainController
        self.logger = logging.getLogger('MainWindow')
    
    def buildUI(self):
        self.logger.debug("Building UI")
        
        self.gladepath = 'main.glade'
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_PATH+self.gladepath)
        
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path(CSS_PATH+CSS_COMMON)
        
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(
            Gdk.Screen.get_default(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        # main window
        self.window = self.builder.get_object("window1")
        # center frame, here we'll do the transformations to keep all in the same window
        self.frame = self.getCentralFrame()
        
        self.addHandlers()
        self.bindHandlers()
    
    def show(self):
        self.window.show_all()
        Gtk.main()
    
    def getCentralFrame(self):
        return self.builder.get_object("frame2")
    
    def putInCenterFrame(self, newCentralFrame):
        self.logger.debug("Enter putInCenterFrame()")
        children = self.getCentralFrame().get_children()
        self.logger.debug("destroy previous children")
        # destroy previous children
        for child in children:
            self.getCentralFrame().remove(child)
        
        self.logger.debug("append the other children")
        # add other children
        otherChildren = newCentralFrame.get_children()
        for otherChild in otherChildren:
            newCentralFrame.remove(otherChild)
            self.getCentralFrame().add(otherChild)
    
    def addHandlers(self):
        self.logger.debug("Adding all handlers")
        self.handlers = {}
        # add new handlers here
        self.logger.debug("Adding help1 handler")
        self.handlers["onHlp1"] = self.help1ManagementHandler
        self.logger.debug("Adding help2 handler")
        self.handlers["onHlp2"] = self.help2ManagementHandler
        self.logger.debug("Adding onSyst handler")
        self.handlers["onSyst"] = self.statusManagementHandler
        self.logger.debug("Adding onUsrs handler")
        self.handlers["onUsrs"] = self.localUsersManagementHandler
        self.logger.debug("Adding onMana handler")
        self.handlers["onMana"] = self.softwareManagementHandler
        self.logger.debug("Adding onUpdt handler")
        self.handlers["onUpdt"] = self.updateManagementHandler
        self.logger.debug("Adding close handlers")
        self.handlers['onDeleteWindow'] = Gtk.main_quit
    
    def bindHandlers(self):
        self.builder.connect_signals(self.handlers)        
    
    def help1ManagementHandler(self, *args):
        self.logger.debug('This should show a brief help about GECOS linking')
    
    def help2ManagementHandler(self, *args):
        self.logger.debug('This should show a brief help about auth modes')
        
    def statusManagementHandler(self, *args):
        self.logger.debug('This should show the system status')
        self.controller.showSystemStatus()
    
    def localUsersManagementHandler(self, *args): 
        self.logger.debug('Show local users management')
        self.controller.showLocalUserListView()
    
    def softwareManagementHandler(self, *args):
        self.logger.debug('Open the software manager')
        self.controller.showSoftwareManager()
    
    def updateManagementHandler(self, *args):
        self.logger.debug('Update config assistant')
        self.controller.updateConfigAsystant()