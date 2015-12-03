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

from gecosws_config_assistant.dto.GecosAccessData import GecosAccessData
from gecosws_config_assistant.dto.ADSetupData import ADSetupData


def showerror(title, message, parent_window):
    logger = logging.getLogger('tkMessageBox')
    logger.debug("showerror('%s', '%s')"%(title, message))

def askyesno(title, message, parent_window):
    logger = logging.getLogger('tkMessageBox')
    logger.debug("askyesno('%s', '%s')"%(title, message))
    return True

def showerror_gtk(title, message, parent_window):
    showerror("", message, parent_window)

def askyesno_gtk(title, message, parent_window):
    return aksyesno("", message, parent_window)

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



        
class ConnectWithGecosCCDialog(ViewMock):
    '''
    Dialog class that shows the Auto setup Dialog.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('ConnectWithGecosCCDialog')
        
        self.gecos_access_data = None
        self.workstation_data = None
        
   

    def get_gecos_access_data(self):
        return self.__gecos_access_data


    def get_workstation_data(self):
        return self.__workstation_data


    def set_gecos_access_data(self, value):
        self.__gecos_access_data = value


    def set_workstation_data(self, value):
        self.__workstation_data = value
       

    def show(self):
        self.logger.debug("Show")


    def connect(self):
        self.logger.debug("connect")

    def disconnect(self):
        self.logger.debug("disconnect")


    def patternSearch(self):
        self.logger.debug("patternSearch")
        
    def cancel(self):
        self.logger.debug("cancel")
                
    def focusUrlField(self):
        self.logger.debug("focusUrlField")               

    def focusUsernameField(self):
        self.logger.debug("focusUsernameField")                 

    def focusPasswordField(self):
        self.logger.debug("focusPasswordField")   
        
    def focusSeachFilterField(self):
        self.logger.debug("focusSeachFilterField")     
              
    def focusWorkstationNameField(self):
        self.logger.debug("focusWorkstationNameField")   

    gecos_access_data = property(get_gecos_access_data, set_gecos_access_data, None, None)
    workstation_data = property(get_workstation_data, set_workstation_data, None, None)
                
        
class GecosCCSetupProcessView(ViewMock):
    '''
    Dialog class that shows the process of GECOS CC connection/disconnection.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('GecosCCSetupProcessView')
        

    def show(self):
        self.logger.debug("Show")


    def accept(self):
        self.logger.debug("accept")
  
    def hide(self):
        self.logger.debug("hide")
                
    def setCheckGecosCredentialsStatus(self, status):
        self.logger.debug("setCheckGecosCredentialsStatus")

    def setCheckWorkstationDataStatus(self, status):
        self.logger.debug("setCheckWorkstationDataStatus")

    def setChefCertificateRetrievalStatus(self, status):
        self.logger.debug("setChefCertificateRetrievalStatus")

    def setLinkToChefLabel(self, text):
        self.logger.debug("setLinkToChefLabel")
        
    def setLinkToChefStatus(self, status):
        self.logger.debug("setLinkToChefStatus")
        
    def setRegisterInGecosLabel(self, text):
        self.logger.debug("setRegisterInGecosLabel")
        
        
    def setRegisterInGecosStatus(self, status):
        self.logger.debug("setRegisterInGecosStatus")
        
    def setCleanStatus(self, status):
        self.logger.debug("setCleanStatus")
        
        
    def enableAcceptButton(self):
        self.logger.debug("enableAcceptButton")


class ChefValidationCertificateDialog(ViewMock):
    '''
    Dialog class to ask the user for the Active Directory administrator user and password.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        self.parent = parent
        self.controller = mainController
        self.logger = logging.getLogger('ChefValidationCertificateDialog')
        
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
                
    data = property(get_data, set_data, None, None)



        

           