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

from dao.GecosAccessDataDAO import GecosAccessDataDAO
from dao.NTPServerDAO import NTPServerDAO
from dao.UserAuthenticationMethodDAO import UserAuthenticationMethodDAO
from dao.WorkstationDataDAO import WorkstationDataDAO

from view.AutoconfDialog import AutoconfDialog

import sys
import socket
import base64


if 'check' in sys.argv:
    # Mock view classes for testing purposses
    print "==> Loading mocks..."
    from view.ViewMocks import showerror_gtk, AutoSetupDialog, AutoSetupProcessView, ADSetupDataElemView, ConnectWithGecosCCDialog
    from util.UtilMocks import GecosCC
else:
    # Use real view classes
    from view.AutoSetupDialog import AutoSetupDialog
    from view.AutoSetupProcessView import AutoSetupProcessView
    from view.ADSetupDataElemView import ADSetupDataElemView
    from view.CommonDialog import showerror_gtk
    from util.GecosCC import GecosCC
    from view.ConnectWithGecosCCDialog import ConnectWithGecosCCDialog 


from util.Validation import Validation
from util.Template import Template

from dto.NTPServer import NTPServer
from dto.LDAPSetupData import LDAPSetupData
from dto.LDAPAuthMethod import LDAPAuthMethod
from dto.ADSetupData import ADSetupData
from dto.ADAuthMethod import ADAuthMethod

from firstboot_lib.firstbootconfig import get_data_file


import logging
import traceback
import subprocess 


import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class AutoSetupController(object):
    '''
    Controller class for the auto setup functionality.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.view = None
        self.processView = None
        self.dao = GecosAccessDataDAO()
        
        self.ntpServerDao = NTPServerDAO()
        self.userAuthenticationMethodDao = UserAuthenticationMethodDAO()
        self.workstationDataDao = WorkstationDataDAO()
        
        self.logger = logging.getLogger('AutoSetupController')
        
        self.auto_setup_success = False

    def getView(self, mainController):
        self.logger.debug('show - BEGIN')
        self.view = AutoconfDialog(mainController)
        self.view.set_data(self.dao.load())   
        self.logger.debug('show - END')
        
        return self.view

    def cancel(self):
        self.logger.debug("cancel")
        self.view.cancel()
    
    def accept(self):
        self.logger.debug("accept")
        self.view.cancel()


    def _setup_validate_data(self, gecosAccessData):
        self.logger.debug("_setup_validate_data")
        # Validate Gecos access data
        if (gecosAccessData.get_url() is None or
            gecosAccessData.get_url().strip() == ''):
            self.logger.debug("Empty URL!")
            showerror_gtk(_("The URL field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                 None)
            self.view.focusUrlField()            
            return False

        if not Validation().isUrl(gecosAccessData.get_url()):
            self.logger.debug("Malformed URL!")
            showerror_gtk(_("Malformed URL in URL field!") + "\n" + _("Please double-check it."),
                 None)            
            self.view.focusUrlField()            
            return False

        if (gecosAccessData.get_login() is None or
            gecosAccessData.get_login().strip() == ''):
            self.logger.debug("Empty login!")
            showerror_gtk(_("The Username field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                 None)
            self.view.focusUsernameField()            
            return False

        if (gecosAccessData.get_password() is None or
            gecosAccessData.get_password().strip() == ''):
            self.logger.debug("Empty password!")
            showerror_gtk(_("The Password field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                 None)
            self.view.focusPasswordField()            
            return False

        gecosCC = GecosCC()
        if not gecosCC.validate_credentials(gecosAccessData):
            self.logger.debug("Bad access data!")
            showerror_gtk(_("Can't connect to GECOS CC!") + "\n" +  _("Please double-check all the data and your network setup."),
                 None)
            self.view.focusPasswordField()            
            return False
        
        return True

    def _setup_ntp_server(self, conf):
        self.logger.debug("_setup_ntp_server")
        if conf["uri_ntp"] is None:
            self.processView.setNTPServerSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("NTP server URI value isn't in auto setup data!"),
                 self.processView)            
            return False
        
        ntpServer = NTPServer()
        ntpServer.set_address(conf["uri_ntp"])
        
        if not ntpServer.syncrhonize():
            self.processView.setNTPServerSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't synchronize with NTP server!"),
                 self.processView)            
            return False
            
        if not self.ntpServerDao.save(ntpServer):
            self.processView.setNTPServerSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Error saving NTP server data!"),
                 self.processView)            
            return False
        
        return True

    def _setup_ldap_authentication_method(self, conf):
        self.logger.debug("_setup_ldap_authentication_method")
        
        ldapSetupData = LDAPSetupData()
        if not conf["auth"].has_key("auth_properties"):
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("LDAP authentication method needs data!"),
                 self.processView)              
            return False              

        if not conf["auth"]["auth_properties"].has_key("uri"):
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("LDAP authentication method needs LDAP server URI!"),
                 self.processView)              
            return                

        if not conf["auth"]["auth_properties"].has_key("base"):
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("LDAP authentication method needs LDAP users base DN!"),
                 self.processView)              
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

        if not ldapSetupData.test():
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Auto setup error"), 
                _("Can't synchronize with LDAP server!"),
                 self.processView)            
            return False
    
        method = LDAPAuthMethod()
        method.set_data(ldapSetupData)
        if not self.userAuthenticationMethodDao.save(method):
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't save LDAP server information!"),
                 self.processView)
            self.userAuthenticationMethodDao.delete(method)
            return False
        
        
        return True

    def _save_base64_file(self, filename, data):
        self.logger.debug("_save_base64_file BEGIN")

        if filename is None:
            self.logger.error("Filename is None")
            return False
        
        if data is None:
            self.logger.error("Data is None")
            return False
        
        try:
            fd = open(filename, 'w');
            fd.write(base64.decodestring(data))
            fd.close()

            
            return True
        except:
            self.logger.error("Error saving %s file"%(filename))
            self.logger.error(str(traceback.format_exc()))
            
        return False

            


    def _setup_ad_authentication_method(self, conf):
        self.logger.debug("_setup_ad_authentication_method")
        adSetupData = ADSetupData()

        if not conf["auth"].has_key("auth_properties"):
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("AD authentication method needs data!"),
                 self.processView)              
            return False             

        if not conf["auth"]["auth_properties"].has_key("specific_conf"):
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("AD authentication method needs 'specific_conf' parameter!"),
                 self.processView)              
            return False              

        specific_conf = conf["auth"]["auth_properties"]["specific_conf"]
        if specific_conf:
            if not conf["auth"]["auth_properties"].has_key("ad_properties"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs 'ad_properties' parameter!"),
                     self.processView)              
                return False

            ad_properties = conf["auth"]["auth_properties"]["ad_properties"]
            
            if not ad_properties.has_key("krb5_conf"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs krb5.conf file!"),
                     self.processView)              
                return False          

            if not ad_properties.has_key("sssd_conf"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs sssd.conf file!"),
                     self.processView)              
                return False          

            if not ad_properties.has_key("smb_conf"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs smb.conf file!"),
                     self.processView)              
                return False          

            if not ad_properties.has_key("pam_conf"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs pam.conf file!"),
                     self.processView)              
                return False          

            
            # Save files
            if not self._save_base64_file(
                self.userAuthenticationMethodDao.main_data_file, 
                    ad_properties["sssd_conf"]):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error saving sssd.conf file!"),
                     self.processView)              
                return False          
                
            if not self._save_base64_file(
                self.userAuthenticationMethodDao.samba_conf_file, 
                    ad_properties["smb_conf"]):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error saving smb.conf file!"),
                     self.processView)              
                return False          
                
            if not self._save_base64_file(
                self.userAuthenticationMethodDao.krb_conf_file, 
                    ad_properties["krb5_conf"]):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error saving krb5.conf file!"),
                     self.processView)              
                return False          
                
            if not self._save_base64_file(
                    '/etc/pam.conf', 
                    ad_properties["pam_conf"]):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error saving pam.conf file!"),
                     self.processView)              
                return False          
            
            adSetupData = ADSetupData()
            if isinstance(self.userAuthenticationMethodDao.load(), ADAuthMethod):
                adSetupData = self.userAuthenticationMethodDao.load().get_data()
            
            # Ask the user for Active Directory administrator user and password
            askForActiveDirectoryCredentialsView = ADSetupDataElemView(self.processView, self)
            askForActiveDirectoryCredentialsView.set_data(adSetupData)
            askForActiveDirectoryCredentialsView.show()

            adSetupData = askForActiveDirectoryCredentialsView.get_data()
            if adSetupData is None:
                self.logger.error("Operation canceled by user!")
                self.processView.setUserAuthenticationSetupStatus(_('CANCELED'))
                self.processView.enableAcceptButton()
                return False
            
            # Run "net ads join" command
            command = 'net ads join -U {0}%{1}'.format(
                    adSetupData.get_ad_administrator_user(), 
                    adSetupData.get_ad_administrator_pass())
            self.logger.debug('running: %s'%(command))
            p = subprocess.Popen(command, shell=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                self.logger.debug(line)
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error running command: ')+command)
                self.processView.setUserAuthenticationSetupStatus(_('CANCELED'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error executing net ads join"),
                     self.processView)              
                return False
                  
                  
            # Restart SSSD service
            self.logger.debug('Restart SSSD service')
            p = subprocess.Popen('service sssd restart', shell=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                self.logger.debug(line)
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error running command: ')+'service sssd restart')
                self.processView.setUserAuthenticationSetupStatus(_('CANCELED'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error restarting sssd service"),
                     self.processView)              
                return False        
            
            self.logger.debug('Save /usr/share/pam-configs/my_mkhomedir file')
            # Save /usr/share/pam-configs/my_mkhomedir file
            template = Template()
            template.source = get_data_file('templates/my_mkhomedir')
            template.destination = '/usr/share/pam-configs/my_mkhomedir'
            template.owner = 'root'
            template.group = 'root'
            template.mode = 00644
            template.variables = { }
            
            if not template.save():
                self.logger.error('Error saving /usr/share/pam-configs/my_mkhomedir file')
                self.processView.setUserAuthenticationSetupStatus(_('CANCELED'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error saving my_mkhomedir file"),
                     self.processView)              
                return False        
            
            # Execute command pam-auth-update
            self.logger.debug('Execute command pam-auth-update')
            p = subprocess.Popen('pam-auth-update --package', shell=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                self.logger.debug(line)
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error running command: ')+'pam-auth-update')
                self.processView.setUserAuthenticationSetupStatus(_('CANCELED'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error executing pam-auth-update"),
                     self.processView)              
                return False           
            
            
            self.logger.debug('Save /etc/gca-sssd.control file')
            # Save /etc/gca-sssd.control file
            template = Template()
            template.source = get_data_file('templates/gca-sssd.control')
            template.destination = '/etc/gca-sssd.control'
            template.owner = 'root'
            template.group = 'root'
            template.mode = 00644
            template.variables = { 'auth_type':  'ad' }
            
            if not template.save():
                self.logger.error('Error saving /etc/gca-sssd.control file')
                self.processView.setUserAuthenticationSetupStatus(_('CANCELED'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Error saving /etc/gca-sssd.control file"),
                     self.processView)              
                return False           
            
            
        else:              
            if not conf["auth"]["auth_properties"].has_key("ad_properties"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs 'ad_properties' parameter!"),
                     self.processView)              
                return False

            ad_properties = conf["auth"]["auth_properties"]["ad_properties"]
            
            if not ad_properties.has_key("fqdn"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs FQDN!"),
                     self.processView)              
                return False          

            if not ad_properties.has_key("workgroup"):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("AD authentication method needs workgroup!"),
                     self.processView)              
                return False          

        
            # Check fqdn
            ipaddress = None
            try:
                ipaddress = socket.gethostbyname(ad_properties["fqdn"])
            except:
                self.logger.error("Can't resolv fqdn: %s"%(ad_properties["fqdn"]))
                self.logger.error(str(traceback.format_exc()))
                
            if ipaddress is None:
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Can't resolv FQDN!\nPlease check your DNS configuration."),
                     self.processView)  
                return False

        
            adSetupData.set_workgroup(ad_properties["workgroup"])
            adSetupData.set_domain(ad_properties["fqdn"])
            
            # Ask the user for Active Directory administrator user and password
            askForActiveDirectoryCredentialsView = ADSetupDataElemView(self.processView, self)
            askForActiveDirectoryCredentialsView.set_data(adSetupData)
            askForActiveDirectoryCredentialsView.show()

            adSetupData = askForActiveDirectoryCredentialsView.get_data()
            if adSetupData is None:
                self.logger.error("Operation canceled by user!")
                self.processView.setUserAuthenticationSetupStatus(_('CANCELED'))
                self.processView.enableAcceptButton()
                return False
            

            # Save AD auth method                
            method = ADAuthMethod()
            method.set_data(adSetupData)
            if not self.userAuthenticationMethodDao.save(method):
                self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("Can't save AD server information!"),
                     self.processView)
                self.userAuthenticationMethodDao.delete(method)
                return False                
        
        
        
        return True

    def proccess_dialog_accept(self):
        self.logger.debug("proccess_dialog_accept")
        self.processView.hide()
        
        if self.auto_setup_success:
            self.view.cancel()
        

    def setup(self):
        self.logger.debug("setup")
        self.auto_setup_success = False
        gecosAccessData = self.view.get_data()
        
        # Validate Gecos access data
        if not self._setup_validate_data(gecosAccessData):
            return False


        # Show process view
        self.processView = AutoSetupProcessView(self)
        self.processView.show()

        # Get auto setup JSON
        self.processView.setAutoSetupDataLoadStatus(_('IN PROCESS'))
        conf = False
        gecosCC = GecosCC()
        try:
            conf = gecosCC.get_json_autoconf(gecosAccessData)
        except:
            self.logger.error('Error loading auto setup data from GECOS')
            self.logger.error(str(traceback.format_exc()))
            
        if not conf:
            self.processView.setAutoSetupDataLoadStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't read auto setup configuration data from GECOS Control Center!"),
                 self.processView)            
            return False
            
        
        self.processView.setAutoSetupDataLoadStatus(_('DONE'))
        
        # Setup NTP server
        self.processView.setNTPServerSetupStatus(_('IN PROCESS'))
        
        if not self._setup_ntp_server(conf):
            return False
        
            
        self.processView.setNTPServerSetupStatus(_('DONE'))
        
        # Setup user authentication method
        self.processView.setUserAuthenticationSetupStatus(_('IN PROCESS'))
        
        if not conf.has_key("auth") or not conf["auth"].has_key("auth_type"):
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Authentication method values aren't in auto setup data!"),
                 self.processView)              
            return False
        
        if conf["auth"]["auth_type"] != 'AD' and conf["auth"]["auth_type"] != 'LDAP':
            self.processView.setUserAuthenticationSetupStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Unknown user authentication method: "+conf["auth"]["auth_type"]),
                 self.processView)              
            return False
        
        # --> LDAP authentication method
        if conf["auth"]["auth_type"] == 'LDAP':
            if not self._setup_ldap_authentication_method(conf):
                return False
            

        # --> Active Directory authentication method
        if conf["auth"]["auth_type"] == 'AD':
            if not self._setup_ad_authentication_method(conf):
                return False      
            
        self.processView.setUserAuthenticationSetupStatus(_('DONE'))

        # Auto setup success
        self.auto_setup_success = True
        self.processView.enableAcceptButton()
        
        return True
