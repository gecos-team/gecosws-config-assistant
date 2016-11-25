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

__author__ = "Abraham Macias Paredes <amacias@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


from gecosws_config_assistant.view.LocalUserListDialog import LocalUserListDialog
from gecosws_config_assistant.view.LocalUserElemDialog import LocalUserElemDialog
from gecosws_config_assistant.view.CommonDialog import showerror_gtk, askyesno_gtk

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from gecosws_config_assistant.dao.LocalUserDAO import LocalUserDAO
from gecosws_config_assistant.util.Validation import Validation

import logging

class LocalUserController(object):
    '''
    Controller class for the "manage local users" functionality.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        self.listView = None
        self.elemView = None
        self.dao = LocalUserDAO()
        self.controller = mainController
        self.logger = logging.getLogger('LocalUserController')

    def showList(self, mainWindow):
        self.logger.debug('show - BEGIN')
        self.listView = LocalUserListDialog(mainWindow, self.controller)
        self.listView.setLocalUserController(self)
        self.listView.set_data(self.dao.loadAll())
        
        self.listView.show()   
        self.logger.debug('show - END')

    def refreshList(self):
        self.logger.debug('refreshList')
        self.listView.set_data(self.dao.loadAll())
        self.listView.refresh()   
        

    def hideList(self):
        self.logger.debug('hideList - BEGIN')
        self.listView.cancel()

    def test(self, obj, check_password):
        self.logger.debug('test - BEGIN')
        
        # Test login
        if obj.get_login() is None or obj.get_login().strip() == '':
            self.logger.debug("Empty login!")
            showerror_gtk(_("The login field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                self.elemView)
            self.elemView.focusLoginField() 
            return False

        if not Validation().isLogin(obj.get_login()):
            self.logger.debug("Bad login!")
            showerror_gtk(_("The login field contains not allowed characters!"),
                self.elemView)
            self.elemView.focusLoginField() 
            return False


        # Test name
        if obj.get_name() is None or obj.get_name().strip() == '':
            self.logger.debug("Empty name!")
            showerror_gtk(_("The name field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                self.elemView)
            self.elemView.focusNameField() 
            return False

        # Test password
        if check_password:
            if obj.get_password() is None or obj.get_password().strip() == '':
                self.logger.debug("Empty password!")
                showerror_gtk(_("The password field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                    self.elemView)
                self.elemView.focusPasswordField() 
                return False

        if obj.get_password() is not None or obj.get_password().strip() != '':
            if not Validation().isAscii(obj.get_password()):
                self.logger.debug("Bad password!")
                showerror_gtk(_("The password field contains not allowed characters."),
                    self.elemView)
                self.elemView.focusPasswordField() 
                return False


        return True

    
    def newElement(self):
        self.logger.debug('newElement - BEGIN')

        self.elemView = LocalUserElemDialog(self.listView, self)
        self.elemView.set_data(None)
        self.elemView.show()  

    def createNewElement(self):
        localUser = self.elemView.get_data()
        if localUser is not None:
            self.logger.debug("Saving new user")
            self.dao.save(localUser)
        self.refreshList()

    def hideElementView(self):
        self.logger.debug('hideElementView - BEGIN')
        self.elemView.cancel()

    def updateElement(self, obj):
        self.logger.debug('updateElement - BEGIN')

        self.elemView = LocalUserElemDialog(self.listView, self)
        self.elemView.set_data(obj)
        self.elemView.show()          
        
        localUser = self.elemView.get_data()
        
        if (localUser is not None and 
            not localUser.isEqual(obj) 
            or (localUser.get_password() is not None 
                and localUser.get_password().strip() != '')):
            self.dao.save(localUser)
        
        self.refreshList()


    def deleteElement(self, obj):
        self.logger.debug('deleteElement - BEGIN')
        self.logger.debug(self.listView.controller)
        
        if askyesno_gtk(_('Do you really want to delete this user? '+ obj.get_login())
                        , self.listView.controller) :
            self.dao.delete(obj)
            
        self.refreshList()
            