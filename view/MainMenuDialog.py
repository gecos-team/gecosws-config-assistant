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

"""
MainMenu redone in Glade
"""
class MainMenuDialog(GladeWindow):
    
    def __init__(self, mainController):
        self.controller = mainController
        self.gladePath = 'main.glade'
        self.logger = logging.getLogger('MainMenuDialog')
        
        self.trafficlightsKey = "trafficlights"
        self.centerbuttonsKey = "centerbuttons"
        
        self.buildUI(self.gladePath)
    
    def addTranslations(self):
        super(MainMenuDialog, self).addTranslations()
    
    def addHandlers(self):
        super(MainMenuDialog, self).addHandlers()
        self.logger.info('Calling child specific handler')
        # add new handlers here
        self.logger.debug("Adding link/unlink handler")
        self.handlers["onLink"] = self.connectWithGECOSHandler
        self.logger.debug("Adding auth management handler")
        self.handlers["onAuth"] = self.authManagementHandler
        self.logger.debug("Adding network management handler")
        self.handlers["onNetw"] = self.netManagementHandler
        self.logger.debug("Adding autoconf handler")
        self.handlers["onAuto"] = self.autoconfManagementHandler
        self.logger.debug("Adding NTP handler")
        self.handlers["onnNTP"] = self.ntpManagementHandler
    
    # Here comes the handlers
    def connectWithGECOSHandler(self, *args):
        self.logger.debug('This should display the gecos connection settings')
        
    def authManagementHandler(self, *args):
        self.logger.debug('This should display the auth settings')
    
    def netManagementHandler(self, *args):
        self.logger.debug('This should display the network settings')
        self.controller.showNetworkSettingsDialog()
    
    def autoconfManagementHandler(self, *args):
        self.logger.debug('This should call the autoconf method or whatever')
        self.controller.showAutoconfDialog()
    
    def ntpManagementHandler(self, *args):
        self.logger.debug('This should call the NTP manager')
        self.controller.showNTPSettingsDialog()
    
    '''
    change the image of the traffic signal
    index: Between 1 and 5, if not it will raise and Exception
    state: Between 1 and 3: 1 green, 2 yellow, 3 grey
    '''
    def trafficSignalChange(self, id, state):
        datafolder = "/usr/local/share/gecosws-config-assistant/"
        
        lightgreenimg  = datafolder+"media/i-status-18-ok.png"
        lightyellowimg = datafolder+"media/i-status-18-grey.png"
        lightgreyimg   = datafolder+"media/i-status-18-off.png" 
        
        trafficwidget = self.builder.get_object(id)
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
    
    '''
    change the state of one of the central buttons
    index: Between 1 and 7, if not it will raise and Exception
    '''
    def setCenterButton(self, id, enabled):
        button = self.builder.get_object(id)
        button.set_sensitive(enabled)
        
    def initGUIValues(self, calculatedStatus):
        trafficlights = {}
        centerbuttons = {}
        
        centerbuttons["netbutton"] = True
        centerbuttons["confbutton"]= False
        centerbuttons["syncbutton"]= False    
        centerbuttons["sysbutton"] = False
        centerbuttons["userbutton"]= False
        
        trafficlights["trafficlight1"] = 3
        trafficlights["trafficlight2"] = 3
        trafficlights["trafficlight3"] = 3
        trafficlights["trafficlight4"] = 3
        trafficlights["trafficlight5"] = 3
        
        networkTrafficLightValue = 2
        networkActivated = False
        
        try:
            networkTrafficLightValue = calculatedStatus[self.controller.networkStatusKey]
            networkActivated = True
        except:
            pass
        
        ntpActivated = False
        
        try:
            if(calculatedStatus[self.controller.ntpStatusKey] == 1):
                ntpActivated = True
        except:
            pass
        
        autoconfActivated = False
        
        try:
            if(calculatedStatus[self.controller.autoconfStatusKey] == 1):
                autoconfActivated = True
        except:
            pass
        
        gecosValue = 3
        gecosActivated = False
        
        try:
            gecosValue = calculatedStatus[self.controller.gecosStatusKey]
        except:
            pass
        
        usersValue = 3
        
        try:
            usersValue = calculatedStatus[self.controller.usersStatusKey]
        except:
            pass
            
        
        # traffic lights
        trafficlights["trafficlight1"] = networkTrafficLightValue
        
        if(networkActivated):
            trafficlights["trafficlight2"] = 2
            trafficlights["trafficlight3"] = 2
        
        if(autoconfActivated):
            trafficlights["trafficlight2"] = 1
        
        if(ntpActivated):
            trafficlights["trafficlight3"] = 1
        
        if(gecosActivated):
            trafficlights["trafficlight4"] = 1
        else:
            trafficlights["trafficlight4"] = gecosValue
        
        trafficlights["trafficlight5"] = usersValue
        
        self.guiValues[self.trafficlightsKey] = trafficlights
        
        # center buttons
        centerbuttons["netbutton"] = True
        
        if(networkActivated):
            centerbuttons["confbutton"]= True
            centerbuttons["syncbutton"]= True
        
        if(gecosValue != 1):
            centerbuttons["sysbutton"] = True
        
        if(gecosValue != 1):
            centerbuttons["sysbutton"] = True
        
        if(usersValue != 1):
            centerbuttons["userbutton"] = True
        
        self.guiValues[self.centerbuttonsKey] = centerbuttons
    
    def loadCurrentState(self, guiValues):
        super(MainMenuDialog, self).loadCurrentState(guiValues)
         # init streetlights 
        for trafficlightKey in self.guiValues[self.trafficlightsKey].keys():
            trafficlightValue = self.guiValues[self.trafficlightsKey][trafficlightKey]
            self.trafficSignalChange(trafficlightKey, trafficlightValue)
        
        
        # disable almost all
        for centerbuttonKey in self.guiValues[self.centerbuttonsKey].keys():
            centerbuttonValue = self.guiValues[self.centerbuttonsKey][centerbuttonKey]
            self.setCenterButton(centerbuttonKey, centerbuttonValue)
    
    '''
    Override of the show method, setting all to the initial state
    '''
    def show(self):
        # set to initial state
        self.initGUIValues(None)
        
        # super method
        super(MainMenuDialog, self).show()
    
    # New call-to-controller-methods
    def showAutoconfDialog(self):
        self.logger.debug("showAutoconfDialog")
        self.controller.showAutoconfDialog()
    
    # old methods, just pasted for copypaste sake
    def showRequirementsCheckDialog(self):
        self.logger.debug("showRequirementsCheckDialog")
        self.controller.showRequirementsCheckDialog()

    def showConnectWithGecosCCDialog(self):
        self.logger.debug("showConnectWithGecosCCDialog")
        self.controller.showConnectWithGecosCCDialog()

    def showUserAuthenticationMethod(self):
        self.logger.debug("showUserAuthenticationMethod")
        self.controller.showUserAuthenticationMethod()
        
    def showLocalUserListView(self):
        self.logger.debug("showLocalUserListView")
        self.controller.showLocalUserListView()