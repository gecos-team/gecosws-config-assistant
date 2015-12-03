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
import traceback

from gi.repository import Gtk, Gdk
from gecosws_config_assistant.view import GLADE_PATH, CSS_PATH, CSS_COMMON
from gecosws_config_assistant.firstboot_lib.firstbootconfig import get_data_file

class MainWindow(object):
    
    def __init__(self, mainController):
        self.controller = mainController
        self.logger = logging.getLogger('MainWindow')
        
        self.currentView = None
        
        self.trafficlightsKey = "trafficlights"
        self.centerbuttonsKey = "centerbuttons"
        self.buttonsKey = "buttons"        
    
    def buildUI(self):
        self.logger.debug("Building UI")
        
        self.gladepath = 'window.glade'
        
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
        
    
    def show(self):
        self.window.show_all()
        Gtk.main()
        
    def getMainWindow(self):
        return self.window
        
    # common screen switch method
    def changeScreen(self, dialog):
        centralFrame = dialog.getCentralFrame()
        width = dialog.getWidth()
        height = dialog.getHeight()
        try:
            self.putInCenterFrame(centralFrame, width, height)
        except:
            tb = traceback.format_exc()
            self.logger.error(tb)
    
    # navigate thru screens
    def navigate(self, dialog):
        # change widgets
        self.changeScreen(dialog)
        # put a reference to the new window
        self.currentView = dialog
    
    def gotoConnectoWithGECOS(self, connectView):
        self.navigate(connectView)
    
    def gotoUserAuth(self, userAuthView):
        self.navigate(userAuthView)
    
    def getCentralFrame(self):
        return self.getElementById("frame2")
    
    def putInCenterFrame(self, newCentralFrame, width, height):
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
             
        self.logger.debug('Resize central frame')
        self.getCentralFrame().set_size_request(width, height)
    
    def addHandlers(self):
        self.logger.debug("Adding all handlers")
        self.handlers = {}
        # add new handlers here
        self.logger.debug("Adding auth management handler")
        self.handlers["onAuth"] = self.authManagementHandler
        self.logger.debug("Adding link/unlink handler")
        self.handlers["onLink"] = self.connectWithGECOSHandler
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
    
    def get_common_handlers(self):
        return self.handlers
    
    def bindHandlers(self):
        self.builder.connect_signals(self.handlers)
    
    def connectWithGECOSHandler(self, *args):
        self.logger.debug('This should display the gecos connection settings')
        self.controller.showConnectWithGecosCCDialog()
        
    def authManagementHandler(self, *args):
        self.logger.debug('This should display the auth settings')
        self.controller.showUserAuthenticationMethod()
    
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
    
    def getElementById(self, id_):
        elem = self.builder.get_object(id_)
        if elem is None and self.currentView is not None:
            elem = self.currentView.builder.get_object(id_)
        
        if elem is None:
            self.logger.warn("Can't find %s element"%(id_))
            
        return elem
    
    '''
    change the image of the traffic signal
    index: Between 1 and 5, if not it will raise and Exception
    state: Between 1 and 3: 1 green, 2 yellow, 3 grey
    '''
    def trafficSignalChange(self, id_, state):
        lightgreenimg  = get_data_file("media/i-status-18-ok.png")
        lightyellowimg = get_data_file("media/i-status-18-grey.png")
        lightgreyimg   = get_data_file("media/i-status-18-off.png")
        
        trafficwidget = self.getElementById(id_)
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
    
    def setStatus(self, calculatedStatus, calculatedButtons):
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
        
        guiValues = {}
        guiValues[self.trafficlightsKey] = trafficlights
        
        # center buttons
        centerbuttons = self.controller.calculateMainButtons(calculatedStatus)
        
        guiValues[self.centerbuttonsKey] = centerbuttons    
        
        guiValues[self.buttonsKey] = calculatedButtons

        self.loadCurrentState(guiValues)
            
        for buttonKey in guiValues[self.buttonsKey].keys():
            buttonValue = guiValues[self.buttonsKey][buttonKey]
            button = self.getElementById(buttonKey)
            button.set_sensitive(buttonValue)        
        
    
    def loadCurrentState(self, guiValues):
        
        self.texts = self.controller.getTexts()
        self.putTexts()
        
        # init streetlights 
        for trafficlightKey in guiValues[self.trafficlightsKey].keys():
            trafficlightValue = guiValues[self.trafficlightsKey][trafficlightKey]
            self.trafficSignalChange(trafficlightKey, trafficlightValue)
        
        
        # disable almost all
        for centerbuttonKey in guiValues[self.centerbuttonsKey].keys():
            centerbuttonValue = guiValues[self.centerbuttonsKey][centerbuttonKey]
            self.setCenterButton(centerbuttonKey, centerbuttonValue)
    
    def putTexts(self):
        networkText  = self.texts[self.controller.networkStatusKey ]
        autoconfText = self.texts[self.controller.autoconfStatusKey]
        ntpText      = self.texts[self.controller.ntpStatusKey     ]
        gecosText    = self.texts[self.controller.gecosStatusKey   ]
        userText     = self.texts[self.controller.usersStatusKey   ]
        
        self.getElementById("netlabel" ).set_text(networkText )
        self.getElementById("conflabel").set_text(autoconfText)
        self.getElementById("synclabel").set_text(ntpText     )
        self.getElementById("syslabel" ).set_text(gecosText   )
        self.getElementById("userlabel").set_text(userText    )
    
    '''
    change the state of one of the central buttons
    index: Between 1 and 7, if not it will raise and Exception
    '''
    def setCenterButton(self, id_, enabled):
        button = self.getElementById(id_)
        button.set_sensitive(enabled)
            