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

import logging

from dto.GecosAccessData import GecosAccessData
from dto.ADSetupData import ADSetupData


def showerror(title, message, parent_window):
    logger = logging.getLogger('tkMessageBox')
    logger.debug("showerror('%s', '%s')"%(title, message))

def askyesno(title, message, parent_window):
    logger = logging.getLogger('tkMessageBox')
    logger.debug("askyesno('%s', '%s')"%(title, message))
    return True

class ViewMock(object):
    def wait_window(self, window):
        pass

class ADSetupDataElemView(ViewMock):
    '''
    Dialog class to ask the user for the Active Directory administrator user and password.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.data = None
        
        self.logger = logging.getLogger('ADSetupDataElemView')
        

    def get_data(self):
        self.logger.debug("Return test AD access data")
        self.__data = ADSetupData()
        self.__data.set_domain('evaos.local')
        self.__data.set_workgroup('evaos')
        self.__data.set_ad_administrator_user('Administrador')            
        self.__data.set_ad_administrator_pass('Evaos.2014')            
        return self.__data


    def set_data(self, value):
        self.__data = value
        
    def show(self):
        self.logger.debug("Show")           
        
    def accept(self):
        self.logger.debug("Accept")

    def cancel(self):
        self.logger.debug("cancel")

                
    data = property(get_data, set_data, None, None)           
    
    
class AutoSetupDialog(ViewMock):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('AutoSetupDialog')
        
        self.data = None
        

    def get_data(self):
        self.logger.debug("Return test Gecos access data")
        self.__data = GecosAccessData()
        self.__data.set_url('http://192.168.1.139/')
        self.__data.set_login('amacias')
        self.__data.set_password('console')        
        
        return self.__data


    def set_data(self, value):
        self.__data = value



    def show(self):
        self.logger.debug("Show")

    def setup(self):
        self.logger.debug("setup")

    def cancel(self):
        self.logger.debug("cancel")
                
    def focusUrlField(self):
        self.logger.debug("focusUrlField")

    def focusUsernameField(self):
        self.logger.debug("focusUsernameField")

    def focusPasswordField(self):
        self.logger.debug("focusPasswordField")
                
    data = property(get_data, set_data, None, None)


class AutoSetupProcessView(ViewMock):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('AutoSetupProcessView')
        
        

    def show(self):
        self.logger.debug("Show")


    def accept(self):
        self.logger.debug("accept")
  
    def hide(self):
        self.logger.debug("hide")
                
    def setAutoSetupDataLoadStatus(self, status):
        self.logger.debug("setAutoSetupDataLoadStatus")

    def setNTPServerSetupStatus(self, status):
        self.logger.debug("setNTPServerSetupStatus")

    def setUserAuthenticationSetupStatus(self, status):
        self.logger.debug("setUserAuthenticationSetupStatus")

    def setGecosCCConnectionSetupStatus(self, status):
        self.logger.debug("setGecosCCConnectionSetupStatus")
        
    def enableAcceptButton(self):
        self.logger.debug("enableAcceptButton")
    
        
class UserAuthenticationMethodElemView(ViewMock):
    '''
    View class to setup the user authentication method.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('UserAuthenticationMethodElemView')
        
        self.data = None
        

    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value


    def show(self):
        self.logger.debug("Show")
 
    def accept(self):
        self.logger.debug("Accept")


    def cancel(self):
        self.logger.debug("cancel")

    def setup(self):
        self.logger.debug("setup")
       
    def focusLdapUriField(self):
        self.logger.debug("focusLdapUriField")              

    def focusUserBaseDNField(self):
        self.logger.debug("focusUserBaseDNField")               

    def focusAdDomainField(self):
        self.logger.debug("focusAdDomainField")               

    def focusAdWorkgroupField(self):
        self.logger.debug("focusAdWorkgroupField")         

    def focusAdUserField(self):
        self.logger.debug("focusAdUserField")          

    def focusAdPasswordField(self):
        self.logger.debug("focusAdPasswordField")        
               
    data = property(get_data, set_data, None, None)



        

       