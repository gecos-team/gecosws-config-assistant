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

import sys

if 'check' in sys.argv:
    # Mock view classes for testing purposses
    print "==> Loading mocks..."
    from view.ViewMocks import askyesno_gtk, showerror_gtl, UserAuthenticationMethodElemView, ADSetupDataElemView
else:
    # Use real view classes
    from view.CommonDialog import askyesno_gtk, showerror_gtk
    from view.UserAuthenticationMethodElemView import UserAuthenticationMethodElemView
    from view.ADSetupDataElemView import ADSetupDataElemView
    from view.UserAuthDialog import UserAuthDialog

from util.Validation import Validation


from dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO

from dto.NTPServer import NTPServer
from dto.LDAPSetupData import LDAPSetupData
from dto.LDAPAuthMethod import LDAPAuthMethod
from dto.ADSetupData import ADSetupData
from dto.ADAuthMethod import ADAuthMethod
from dto.LocalUsersAuthMethod import LocalUsersAuthMethod


import socket
import logging
import traceback


import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class UserAuthenticationMethodController(object):
    '''
    Controller class for the "set user authentication method" functionality.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.view = None 
        self.dao = UserAuthenticationMethodDAO()
        self.logger = logging.getLogger('UserAuthenticationMethodController')

    def getView(self, mainController):
        self.logger.debug('getView - BEGIN')
        self.view = UserAuthDialog(mainController)
        
        data = self.dao.load()
        self.logger.debug('data is of type %s'%(type(data).__name__))
        self.view.set_data(data)
        self.view.updateCombo()
        
        self.logger.debug('getView - END')
        
        return self.view

    def hide(self):
        self.logger.debug('hide')
        self.view.cancel()

    def _data_has_changed(self):
        oldData = self.dao.load()
        newData = self.view.get_data()
        
        # Check data types
        if type(oldData).__name__ != type(newData).__name__:
            self.logger.debug('Old data: %s New data:%s'%(type(oldData).__name__, type(newData).__name__))
            return True
        
        if isinstance(oldData, LDAPAuthMethod):
            # Check LDAP parameters
            oldAuthData = oldData.get_data()
            newAuthData = newData.get_data()
            
            if oldAuthData.get_uri() != newAuthData.get_uri():
                self.logger.debug('LDAP URIs are different')
                return True
        
            if oldAuthData.get_base() != newAuthData.get_base():
                self.logger.debug('LDAP user base DNs are different')
                return True
        
            if oldAuthData.get_base_group() != newAuthData.get_base_group():
                self.logger.debug('LDAP user base groups are different')
                return True
        
            if oldAuthData.get_bind_user_dn() != newAuthData.get_bind_user_dn():
                self.logger.debug('LDAP bind user DNs are different')
                return True
        
            if oldAuthData.get_bind_user_pwd() != newAuthData.get_bind_user_pwd():
                self.logger.debug('LDAP bind user passwords are different')
                return True

        if isinstance(oldData, ADAuthMethod):
            # Check AD parameters
            oldAuthData = oldData.get_data()
            newAuthData = newData.get_data()
            
            if oldAuthData.get_domain() != newAuthData.get_domain():
                self.logger.debug('AD domains are different')
                return True
        
            if oldAuthData.get_workgroup() != newAuthData.get_workgroup():
                self.logger.debug('AD workgroups are different')
                return True
        
        return False

    def accept(self):
        self.logger.debug('accept - BEGIN')
        if self._data_has_changed():
            if askyesno_gtk(_('The user authentication data has changed.\n'+
                    'Do you want to setup the user authentication method using this new data?'), self.view):
                # Test and save
                if self.test():
                    result = self.save()
                    self.hide()
                    return result
                else:
                    return False
            else:
                self.hide()
                return False
        else:
            self.hide()
            return False

    
    def save(self):
        self.logger.debug('save - BEGIN')
        oldData = self.dao.load()
        newData = self.view.get_data()        
        if newData is not None:
            # Return to local users authentication
            if isinstance(oldData, ADAuthMethod):
                # We need AD Administrator user credentials to return 
                # to local users authentication method
                
                # Ask the user for Active Directory administrator user and password
                askForActiveDirectoryCredentialsView = ADSetupDataElemView(self.view, self)
                askForActiveDirectoryCredentialsView.set_data(oldData.get_data())
                askForActiveDirectoryCredentialsView.show()
    
                data = askForActiveDirectoryCredentialsView.get_data()
                if data is None:
                    self.logger.error("Operation canceled by user!")
                    return False
                oldData.set_data(data)
            
            if self.dao.delete(oldData):
                # Set new authentication method
                return self.dao.save(newData)
            else:
                return False
        else:
            self.logger.debug("Empty data!")
            
        return False


    def test(self):
        self.logger.debug('test - BEGIN')
        
        if self.view.get_data() is None:
            self.logger.debug("Empty data!")
            return False
        
        newData = self.view.get_data()

        if isinstance(newData, LDAPAuthMethod):
            # Check LDAP parameters
            newAuthData = newData.get_data()
            
            if (newAuthData.get_uri() is None or
                newAuthData.get_uri().strip() == ''):
                self.logger.debug("Empty LDAP URI!")
                showerror_gtk(_("The URI field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                     self.view)
                self.view.focusLdapUriField()            
                return False            
            
            if not Validation().isLdapUri(newAuthData.get_uri()):
                self.logger.debug("Malformed LDAP URI! %s"%(newAuthData.get_uri()))
                showerror_gtk(_("Malformed LDAP URI!") + "\n" + _("Please check that the URI starts with 'ldap://' or 'ldaps://'."),
                     self.view)
                self.view.focusLdapUriField()            
                return False            

            if (newAuthData.get_base() is None or
                newAuthData.get_base().strip() == ''):
                self.logger.debug("Empty user base DN!")
                showerror_gtk(_("The users base DN field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                     self.view)
                self.view.focusUserBaseDNField()            
                return False    
            
            if not newAuthData.test():
                self.logger.debug("Can't connect to LDAP!")
                showerror_gtk(_("Can't connect to LDAP server!") + "\n" + _("Please check all the fields and your network connection."),
                     self.view)
                self.view.focusLdapUriField()            
                return False            
            

        if isinstance(newData, ADAuthMethod):
            # Check AD parameters
            newAuthData = newData.get_data()
            
            if (newAuthData.get_domain() is None or
                newAuthData.get_domain().strip() == ''):
                self.logger.debug("Empty AD domain field!")
                showerror_gtk(_("The Domain field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                     self.view)
                self.view.focusAdDomainField()            
                return False            

            # Check fqdn
            ipaddress = None
            try:
                ipaddress = socket.gethostbyname(newAuthData.get_domain())
            except:
                self.logger.error("Can't resolv domain name: %s"%(newAuthData.get_domain()))
                self.logger.error(str(traceback.format_exc()))
                
            if ipaddress is None:
                showerror_gtk(_("Can't resolv the Active Directory Domain name!") + "\n" 
                    + _("Please check the Domain field and your DNS configuration."),
                     self.view)
                self.view.focusAdDomainField() 
                return False

            if (newAuthData.get_workgroup() is None or
                newAuthData.get_workgroup().strip() == ''):
                self.logger.debug("Empty AD workgroup field!")
                showerror_gtk(_("The Workgroup field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                     self.view)
                self.view.focusAdWorkgroupField()            
                return False   

            if (newAuthData.get_ad_administrator_user() is None or
                newAuthData.get_ad_administrator_user().strip() == ''):
                self.logger.debug("Empty AD administrator user field!")
                showerror_gtk(_("The AD administrator user field is empty!") + "\n" 
                    + _("Please fill all the mandatory fields."),
                     self.view)
                self.view.focusAdUserField()            
                return False   

            if (newAuthData.get_ad_administrator_pass() is None or
                newAuthData.get_ad_administrator_pass().strip() == ''):
                self.logger.debug("Empty AD administrator password field!")
                showerro_gtk(_("The AD administrator password field is empty!") + "\n" 
                    + _("Please fill all the mandatory fields."),
                     self.view)
                self.view.focusAdPasswordField()            
                return False   
        
            if not newAuthData.test():
                self.logger.debug("Can't connect to Active Directory!")
                showerror_gtk(_("Can't connect to Active Directory server!") + "\n" 
                    + _("Please check all the fields and your network connection."),
                     self.view)
                self.view.focusAdDomainField()             
                return False         
        
        
        return True
        
