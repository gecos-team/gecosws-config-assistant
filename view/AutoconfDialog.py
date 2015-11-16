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

from GladeWindow import GladeWindow
import logging
"""
Autoconf redone in Glade
"""
class AutoconfDialog(GladeWindow):
    def __init__(self, mainController):
        self.controller = mainController
        self.gladePath = 'autoconf.glade'
        self.logger = logging.getLogger('AutoconfDialog')
        
        self.buildUI(self.gladePath)
    
    def addTranslations(self):
        super(AutoconfDialog, self).addTranslations()
    
    def addHandlers(self):
        super(AutoconfDialog, self).addHandlers()
    
    # Here comes the handlers
    def trafficSignalChange(self, state):
        datafolder = "/usr/local/share/gecosws-config-assistant/"
        
        lightgreenimg  = datafolder+"media/i-status-22-ok.png"
        lightyellowimg = datafolder+"media/i-status-22-grey.png"
        lightgreyimg   = datafolder+"media/i-status-22-off.png"
        
        trafficwidget = self.builder.get_object("image1")
        lightimg = ""
        
        if   (state == 1):
            lightimg = lightgreenimg
        elif (state == 2):
            lightimg = lightyellowimg
        elif (state == 3):
            lightimg = lightgreyimg
            
        trafficwidget.hide()
        trafficwidget.set_from_file(lightimg)
        trafficwidget.show()
    
    def setToInitialState(self):
        # clean
        self.builder.get_object('entry1').set_text('')
        self.builder.get_object('entry2').set_text('')
        self.builder.get_object('entry3').set_text('')
        
        # hide
        self.builder.get_object('label9').set_visible(false)
        self.builder.get_object('label7').set_visible(false)
        self.builder.get_object('entry4').set_visible(false)
        self.builder.get_object('entry5').set_visible(false)
        self.builder.get_object('button2').set_visible(false)
        
        # change
        self.trafficSignalChange(2)
        self.builder.get_object('label11').set_text('PENDIENTE')
    
    def show(self):
        self.setToInitialState()
        # super method
        super(AutoconfDialog, self).show()