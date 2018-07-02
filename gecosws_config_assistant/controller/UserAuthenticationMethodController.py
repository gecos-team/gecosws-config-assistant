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

from gecosws_config_assistant.view.CommonDialog import askyesno_gtk, showerror_gtk, showinfo_gtk
from gecosws_config_assistant.view.ADSetupDataElemView import ADSetupDataElemView
from gecosws_config_assistant.view.UserAuthDialog import UserAuthDialog, LOCAL_USERS, LDAP_USERS, AD_USERS

from gecosws_config_assistant.util.Validation import Validation


from gecosws_config_assistant.dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO
from gecosws_config_assistant.dao.NetworkInterfaceDAO import NetworkInterfaceDAO

from gecosws_config_assistant.dto.NTPServer import NTPServer
from gecosws_config_assistant.dto.LDAPSetupData import LDAPSetupData
from gecosws_config_assistant.dto.LDAPAuthMethod import LDAPAuthMethod
from gecosws_config_assistant.dto.ADSetupData import ADSetupData
from gecosws_config_assistant.dto.ADAuthMethod import ADAuthMethod
from gecosws_config_assistant.dto.LocalUsersAuthMethod import LocalUsersAuthMethod


import socket
import logging
import traceback
import types

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class UserAuthenticationMethodController(object):
    '''
    Controller class for the "set user authentication method" functionality.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        self.view = None 
        self.mainController = mainController
        self.dao = UserAuthenticationMethodDAO()
        self.logger = logging.getLogger('UserAuthenticationMethodController')

    def getView(self, mainController):
        self.logger.debug('getView - BEGIN')
        self.mainWindow = mainController.window
        self.view = UserAuthDialog(mainController)
        
        data = self.dao.load()
        self.logger.debug('data from dao is of type %s'%(type(data).__name__))
        if self.mainController.requirementsCheck.autoSetup.view is not None:
            conf = self.mainController.requirementsCheck.autoSetup.get_conf()
            if conf is not None:
                new_data = self.get_auth_data_from_conf(conf)
                if type(new_data) != types.BooleanType:
                    data = new_data
                 
        
        self.logger.debug('data is of type %s'%(type(data).__name__))
        self.view.set_data(data)
        self.view.updateCombo()
        
        self.logger.debug('getView - END')
        
        return self.view
    
    def get_auth_data_from_conf(self, conf):
        if conf is None or conf is False or not isinstance(conf, dict):
            return False
        
        if not conf.has_key("auth") or not conf["auth"].has_key("auth_type"):
            self.logger.error("Authentication method values aren't in auto setup data!")
            return False
        
        if conf["auth"]["auth_type"] != 'AD' and conf["auth"]["auth_type"] != 'LDAP':
            self.logger.error("Unknown user authentication method: "+conf["auth"]["auth_type"])
            return False
        
        # --> LDAP authentication method
        if conf["auth"]["auth_type"] == 'LDAP':
            return self._setup_ldap_authentication_method(conf)
            

        # --> Active Directory authentication method
        if conf["auth"]["auth_type"] == 'AD':
            return self._setup_ad_authentication_method(conf)
        
        return False
        
    def _setup_ad_authentication_method(self, conf):
        self.logger.debug("_setup_ad_authentication_method")
        adSetupData = ADSetupData()

        if not conf["auth"].has_key("auth_properties"):
            self.logger.error("AD authentication method needs data!")
            return False             

        if not conf["auth"]["auth_properties"].has_key("specific_conf"):
            self.logger.error("AD authentication method needs 'specific_conf' parameter!")
            return False              

        specific_conf = conf["auth"]["auth_properties"]["specific_conf"]
        if specific_conf:
            if not conf["auth"]["auth_properties"].has_key("ad_properties"):
                self.logger.error("AD authentication method needs 'ad_properties' parameter!")
                return False

            ad_properties = conf["auth"]["auth_properties"]["ad_properties"]
            
            if not ad_properties.has_key("krb5_conf"):
                self.logger.error("AD authentication method needs krb5.conf file!")
                return False          

            if not ad_properties.has_key("sssd_conf"):
                self.logger.error("AD authentication method needs sssd.conf file!")
                return False          

            if not ad_properties.has_key("smb_conf"):
                self.logger.error("AD authentication method needs smb.conf file!")
                return False          

            if not ad_properties.has_key("pam_conf"):
                self.logger.error("AD authentication method needs pam.conf file!")
                return False          

            
            # Add files to ADSetupData
            adSetupData.set_specific(True)
            adSetupData.set_krb_5_conf(ad_properties["krb5_conf"])
            adSetupData.set_sssd_conf(ad_properties["sssd_conf"])
            adSetupData.set_smb_conf(ad_properties["smb_conf"])
            adSetupData.set_pam_conf(ad_properties["pam_conf"])
            
            
            
        else:              
            if not conf["auth"]["auth_properties"].has_key("ad_properties"):
                self.logger.error("AD authentication method needs 'ad_properties' parameter!")
                return False

            ad_properties = conf["auth"]["auth_properties"]["ad_properties"]
            
            if not ad_properties.has_key("fqdn"):
                self.logger.error("AD authentication method needs FQDN!")
                return False          

            if not ad_properties.has_key("workgroup"):
                self.logger.error("AD authentication method needs workgroup!")
                return False          

            adSetupData.set_workgroup(ad_properties["workgroup"])
            adSetupData.set_domain(ad_properties["fqdn"])
            
        method = ADAuthMethod()
        method.set_data(adSetupData)        
        
        return method
        
        
    def _setup_ldap_authentication_method(self, conf):
        self.logger.debug("_setup_ldap_authentication_method")
        
        ldapSetupData = LDAPSetupData()
        if not conf["auth"].has_key("auth_properties"):
            self.logger.error("LDAP authentication method needs data!")
            return False              

        if not conf["auth"]["auth_properties"].has_key("uri"):
            self.logger.error("LDAP authentication method needs LDAP server URI!")
            return False

        if not conf["auth"]["auth_properties"].has_key("base"):
            self.logger.error("LDAP authentication method needs LDAP users base DN!")
            return False           

        # If default parameters, skip user authentication
        if conf["auth"]["auth_properties"]["uri"] == 'URL_LDAP':
            self.logger.info('Default LDAP URI detected. Skip user authentication setup!')
            return True
        
        
        ldapSetupData.set_uri(conf["auth"]["auth_properties"]["uri"])
        ldapSetupData.set_base(conf["auth"]["auth_properties"]["base"])
        if conf["auth"]["auth_properties"].has_key("basegroup"):
            ldapSetupData.set_base_group(conf["auth"]["auth_properties"]["basegroup"])

        if conf["auth"]["auth_properties"].has_key("binddn"):
            ldapSetupData.set_bind_user_dn(conf["auth"]["auth_properties"]["binddn"])

        if conf["auth"]["auth_properties"].has_key("bindpwd"):
            ldapSetupData.set_bind_user_pwd(conf["auth"]["auth_properties"]["bindpwd"])

        method = LDAPAuthMethod()
        method.set_data(ldapSetupData)
        
        return method        
        
    
    
    
    def getStatus(self):
        data = self.dao.load()
        name = data.get_name()
        
        if(name == _('Internal')):
            value = LOCAL_USERS
        elif(name == _('LDAP')):
            value = LDAP_USERS
        elif(name == _('Active Directory')):
            value = AD_USERS
        
        return value
    
    def areNotInternal(self):
        status = self.getStatus()
        ret = False
        
        if(status != LOCAL_USERS):
            ret = True
        
        return ret

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
                askForActiveDirectoryCredentialsView = ADSetupDataElemView(self.mainWindow, self)
                askForActiveDirectoryCredentialsView.set_data(oldData.get_data())
                askForActiveDirectoryCredentialsView.show()
    
                data = askForActiveDirectoryCredentialsView.get_data()
                if data is None:
                    self.logger.error("Operation canceled by user!")
                    return False
                oldData.set_data(data)
            
            if self.dao.delete(oldData):
                # Set new authentication method
                if self.dao.save(newData)
                    self.logger.debug("Authentication method saved!")
                    showinfo_gtk(_("Authentication method saved!"),self.view)
                    return True
                else:
                    self.logger.error("Authentication method failed!")
                    showerror_gtk(_("Authentication method failed!"),self.view)
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
            
            networkInterfaceDAO = NetworkInterfaceDAO()
            hostname = networkInterfaceDAO.get_hostname()
            
            if not Validation().isValidNetbiosHostname(hostname):
                self.logger.debug("Bad hostname: %s"%(hostname))
                showerror_gtk(_("Bad netbios hostname!") + ": " +hostname + "\n" + _("Please change the hostname of this computer."),
                     self.view)
                self.view.focusAdDomainField()
                return False                          
            
            if (newAuthData.get_domain() is None or
                newAuthData.get_domain().strip() == ''):
                self.logger.debug("Empty AD domain field!")
                showerror_gtk(_("The Domain field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                     self.view)
                self.view.focusAdDomainField()            
                return False            

            self.logger.debug('Specific: %s'%(newAuthData.get_specific()))

            if not newAuthData.get_specific():
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
                showerror_gtk(_("The AD administrator password field is empty!") + "\n" 
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
        
