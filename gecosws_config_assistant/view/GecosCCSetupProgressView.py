#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from __builtin__ import True

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
from gi.repository import Gtk

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class GecosCCSetupProgressView(GladeWindow):
    
    def __init__(self, mainController, mainWindow):
        self.controller = mainController
        self.mainWindow = mainWindow
        self.gladePath = 'progress.glade'
        self.logger = logging.getLogger('GecosCCSetupProgressView')
        
        self.buildUI(self.gladePath)
        
        self.setElements()
        self.acceptButton.set_sensitive(False)
    
    def setElements(self):
        self.logger.debug("Setting elements")
        self.dialog                       = self.getElementById("window1")
        self.linkToChefLabel              = self.getElementById("label4")
        self.registerInGecosLabel         = self.getElementById("label5")
        
        # labels to be modified
        
        self.gecosCredentialsStatusLabel  = self.getElementById("label7")
        self.workstationDataStatusLabel   = self.getElementById("label8")
        self.chefCertificateStatusLabel   = self.getElementById("label9")
        self.linkToChefStatusLabel        = self.getElementById("label10")
        self.registerInGecosStatusLabel   = self.getElementById("label11")
        self.cleanStatusLabel             = self.getElementById("label12")
        
        self.acceptButton                 = self.getElementById("button1")
        self.progressBar                  = self.getElementById("progressbar1")
        self.error_status                 = ""
    
    def addHandlers(self):
        super(GecosCCSetupProgressView, self).addHandlers()
        self.logger.info('Calling child specific handler')
        # add new handlers here
        self.logger.debug("Adding link/unlink handler")
        self.handlers["onAcpt"] = self.accept
    
    def accept(self, *args):
        self.logger.debug("accept")
        self.controller.proccess_dialog_accept(self.error_status)
        self.hide(None)
    
    def hide(self, *args):
        self.dialog.destroy()
    
    def show(self):
        # super method
        self.logger.debug("Show this view")
        self.window.set_modal(True)
        self.window.set_transient_for(self.mainWindow.window)
        #self.window.present()
        self.window.show_all()
        
        x, y = self.mainWindow.window.get_position()
        w, h = self.mainWindow.window.get_size()
        sw, sh = self.window.get_size()
        self.logger.debug('x=%s y=%s w=%s h=%s sw=%s sh=%s'%(x, y, w, h, sw, sh))
        self.window.move(x + w/2 - sw/2, y + h/2 - sh/2)        
        
        while Gtk.events_pending():
            Gtk.main_iteration()
    
    def elementChangeText(self, element, text):
        self.logger.debug("Changing "+str(element)+" to text "+text)
        element.set_text(text)
        while Gtk.events_pending():
            Gtk.main_iteration()
        
    def setCheckGecosCredentialsStatus(self, status):
        self.logger.debug("Setting gecos cred status")
        self.elementChangeText(self.gecosCredentialsStatusLabel, status)
        self.error_status = (status == _('ERROR'))
    
    def setCheckWorkstationDataStatus(self, status):
        self.logger.debug("Setting workstation data status")
        self.elementChangeText(self.workstationDataStatusLabel, status)
        self.error_status = (status == _('ERROR'))

    def setChefCertificateRetrievalStatus(self, status):
        self.logger.debug("Setting chef certificate status")
        self.elementChangeText(self.chefCertificateStatusLabel, status)
        self.error_status = (status == _('ERROR'))

    def setLinkToChefLabel(self, status):
        self.logger.debug("Setting link to chef label")
        self.elementChangeText(self.linkToChefLabel, status)
        
    def setLinkToChefStatus(self, status):
        self.logger.debug("Setting link to chef status")
        self.elementChangeText(self.linkToChefStatusLabel, status)
        self.error_status = (status == _('ERROR'))
        
    def setRegisterInGecosLabel(self, status):
        self.logger.debug("Setting register in gecos label")
        self.elementChangeText(self.registerInGecosLabel, status)
        
    def setRegisterInGecosStatus(self, status):
        self.logger.debug("Setting register in gecos status")
        self.elementChangeText(self.registerInGecosStatusLabel, status)
        self.error_status = (status == _('ERROR'))
        
    def setCleanStatus(self, status):
        self.logger.debug("Setting clean status")
        self.elementChangeText(self.cleanStatusLabel, status)
        self.error_status = (status == _('ERROR'))
    
    def enableAcceptButton(self):
        self.logger.debug("Enable accept button")
        self.acceptButton.set_sensitive(True)
    
    def addProgressFraction(self, fraction):
        currentFraction = self.progressBar.get_fraction()
        self.progressBar.set_fraction(fraction + currentFraction)