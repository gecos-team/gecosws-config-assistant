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
from dto.NTPServer import NTPServer
from view.CommonDialog import showerror_gtk, showinfo_gtk, askyesno_gtk
# from view.MainWindow import MainWindow
from gettext import gettext as _
import gettext
import logging

class NTPDialog(GladeWindow):
    
    def __init__(self, mainController):
        self.controller = mainController
        self.gladePath = 'ntp.glade'
        self.logger = logging.getLogger('NTPDialog')
        
        self.data = None
        self.ntpServerKey = "ntpKey"
#         self.mainWindow = MainWindow.getInstance(None)

        self.buildUI(self.gladePath)
        
    def get_data(self):
        return self.data

    def set_data(self, value):
        self.data = value
    
    def addTranslations(self):
        super(NTPDialog, self).addTranslations()
    
    def addHandlers(self):
        super(NTPDialog, self).addHandlers()
        self.logger.info('Calling child specific handler')
        # add new handlers here
        self.logger.debug("Adding check ntp connection")
        self.handlers["onChek"] = self.checkNTPCon
        self.logger.debug("Adding OK handler")
        self.handlers["onOOKK"] = self.okAndBack
    
    def checkNTPCon(self, *args):
        self.logger.debug("Checking NTP connection")
        return self.test(True)
    
    def test(self, display = False):
        text = self.getNTPServerInput()
        
        if self.get_data() is None:
            self.set_data(NTPServer())
        
        self.get_data().set_address(text)
        result = self.controller.getNTPController().test(self)
        
#         if not result:
#             showwarning_gtk(_("Can't synchronize time"), 
#                 _("Can't connect with NTP server.\nPlease double-check the NTP server address"), 
#                 self.mainWindow)
#         else:
#             showinfo_gtk(_("Success"), 
#                 _("NTP server connection successful"), self.mainWindow)
            
        return result
    
    def okAndBack(self, *args):
        self.logger.debug("Back to main screen")
        guiDir = self.getNTPServerInput()
        
        if self.get_data() is None:
            self.set_data(NTPServer())
        
        if guiDir is not None:
            self.guiValues[self.ntpServerKey] = self.getNTPServerInput()
            ntpServer = NTPServer()
            ntpServer.set_address(self.getNTPServerInput())
            self.set_data(ntpServer)
        
        if self.test(False):
            self.controller.getNTPController().save(self.get_data())
        self.controller.backToMainWindowDialog()
    
    def getNTPServerInput(self):
        entry = self.builder.get_object("entry1")
        text = entry.get_text()
        return text
    
    def initGUIValues(self, previousState):
        try:
            # access to key to check it exists
            foo = previousState[self.ntpServerKey]
            # if it does, we can safely pass the state
            self.guiValues = previousState
        except:
            # if it doesn't use default
            self.guiValues[self.ntpServerKey] = "hora.roa.es"
    
    def loadCurrentState(self, guiValues):
        entry = self.builder.get_object("entry1")
        entry.set_text(self.guiValues[self.ntpServerKey])
    
    def show(self):
        # set to initial state
        self.initGUIValues(None)
        
        # super method
        super(NTPDialog, self).show()