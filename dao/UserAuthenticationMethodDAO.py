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

from dto.LocalUsersAuthMethod import LocalUsersAuthMethod
from dto.UserAuthenticationMethod import UserAuthenticationMethod
from dto.LDAPAuthMethod import LDAPAuthMethod
from dto.LDAPSetupData import LDAPSetupData
from dto.ADAuthMethod import ADAuthMethod
from dto.ADSetupData import ADSetupData
from util.Template import Template
from util.PackageManager import PackageManager

import logging
import traceback
import subprocess
import os

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class UserAuthenticationMethodDAO(object):
    '''
    DAO class to manipulate UserAuthenticationMethod DTO objects.
    '''

    # Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UserAuthenticationMethodDAO, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        '''
        Constructor
        '''
        
        self.logger = logging.getLogger('UserAuthenticationMethodDAO')
        
        self.main_data_file = '/etc/sssd/sssd.conf'
        self.samba_conf_file = '/etc/samba/smb.conf'
        self.krb_conf_file = '/etc/krb5.conf'
        
        self.initiated = False
        # Check if 'sssd' package exists
        self.pm = PackageManager()
        if not self.pm.is_package_installed('sssd'):
            # Try to install the package
            self.logger.debug('Try to install "sssd" package')
            try:
                self.pm.install_package('sssd')
                self.initiated = True
            except Exception:
                self.logger.error(_('Package installation failed:') + 'sssd')
                self.logger.error(str(traceback.format_exc())) 
        else:
            self.logger.debug('Already installed "sssd" package')
            self.initiated = True            
      
    def _load_ldap(self):
        data = LDAPSetupData()
        
        # Get the data from /etc/sssd/sssd.conf
        with open(self.main_data_file) as fp:
            for line in fp:
                if line.strip().startswith('ldap_uri'):
                    parts = line.split('=')
                    del parts[0]
                    data.set_uri('='.join(parts).strip())
                    continue      

                if line.strip().startswith('ldap_search_base'):
                    parts = line.split('=')
                    del parts[0]
                    data.set_base('='.join(parts).strip())
                    continue      

                if line.strip().startswith('ldap_group_search_base'):
                    parts = line.split('=')
                    del parts[0]
                    data.set_base_group('='.join(parts).strip())
                    continue      

                if line.strip().startswith('ldap_default_bind_dn'):
                    parts = line.split('=')
                    del parts[0]
                    data.set_bind_user_dn('='.join(parts).strip())
                    continue      

                if line.strip().startswith('ldap_default_authtok') and not line.strip().startswith('ldap_default_authtok_type'):
                    parts = line.split('=')
                    del parts[0]
                    data.set_bind_user_pwd('='.join(parts).strip())
                    continue      
                
                
        method = LDAPAuthMethod();
        method.set_data(data)
         
        return method
    
    def _save_ldap(self, method):
        self.logger.debug('Saving LDAP user authentication method')
        data = method.get_data()
        
        # Check data values
        if data.get_uri() is None or data.get_uri().strip() == '':
            raise ValueError('LDAP URI is empty!')
        
        if data.get_base() is None or data.get_base().strip() == '':
            raise ValueError('LDAP base is empty!')

              
        self.logger.debug('Save /etc/sssd/sssd.conf file')
        # Save /etc/samba/sssd.conf file
        template = Template()
        template.source = 'templates/sssd.conf.ldap'
        template.destination = self.main_data_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00600
        template.variables = { 'ldap_uri':  data.get_uri(), 
                              'ldap_search_base': data.get_base()}
        
        if (data.get_bind_user_dn() is not None and 
            data.get_bind_user_dn().strip() != '' and
            data.get_bind_user_pwd() is not None and 
            data.get_bind_user_pwd().strip() != ''):
            template.variables['bind_dn'] = data.get_bind_user_dn()
            template.variables['bind_password'] = data.get_bind_user_pwd()

        if (data.get_base_group() is not None and 
            data.get_base_group().strip() != ''):
            template.variables['base_group'] = data.get_base_group()

        
        if not template.save():
            self.logger.error('Error saving /etc/sssd/sssd.conf file')
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
            return False        
        
        self.logger.debug('Save /usr/share/pam-configs/my_mkhomedir file')
        # Save /usr/share/pam-configs/my_mkhomedir file
        template = Template()
        template.source = 'templates/my_mkhomedir'
        template.destination = '/usr/share/pam-configs/my_mkhomedir'
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        template.variables = { }
        
        if not template.save():
            self.logger.error('Error saving /usr/share/pam-configs/my_mkhomedir file')
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
            return False           
        
        
        self.logger.debug('Save /etc/gca-sssd.control file')
        # Save /etc/gca-sssd.control file
        template = Template()
        template.source = 'templates/gca-sssd.control'
        template.destination = '/etc/gca-sssd.control'
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        template.variables = { 'auth_type':  'ldap' }
        
        if not template.save():
            self.logger.error('Error saving /etc/gca-sssd.control file')
            return False           
        
        return True
        
        
        
    def _delete_ldap(self, method):
        self.logger.debug('Deleting LDAP user authentication method')

        self.logger.debug('Save /etc/sssd/sssd.conf file')
        # Save /etc/samba/sssd.conf file
        template = Template()
        template.source = 'templates/sssd.conf.local'
        template.destination = self.main_data_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00600
        template.variables = { }
        
        if not template.save():
            self.logger.error('Error saving /etc/sssd/sssd.conf file')
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
            return False        
        
        self.logger.debug('Delete %s file'%('/etc/gca-sssd.control'))
        if os.path.isfile('/etc/gca-sssd.control'):
            os.remove('/etc/gca-sssd.control')        

        return True


          

    def _load_active_directory(self):
        data = ADSetupData()
        
        # Get domain from /etc/sssd/sssd.conf
        domain = None
        with open(self.main_data_file) as fp:
            for line in fp:
                if line.strip().startswith('domains'):
                    parts = line.split('=')
                    domain = parts[1].strip()
                    break        
        
        # Get workgroup from /etc/samba/smb.conf
        workgroup = None
        with open(self.samba_conf_file) as fp:
            for line in fp:
                if line.strip().startswith('workgroup'):
                    parts = line.split('=')
                    workgroup = parts[1].strip()
                    break          
        
        if domain is None:
            self.logger.error('Can not find Active Directory domain name in configuration files!')
            return None
        
        if workgroup is None:
            self.logger.error('Can not find Active Directory workgroup name in configuration files!')
            return None
        
        data.set_domain(domain)
        data.set_workgroup(workgroup)
        
        method = ADAuthMethod()
        method.set_data(data)
        
        return method


    def _save_active_directory(self, method):
        self.logger.debug('Saving active directory user authentication method')
        data = method.get_data()
        
        # Check data values
        if data.get_ad_administrator_user() is None or data.get_ad_administrator_user().strip() == '':
            raise ValueError('Active directory administrator user is empty!')
        
        if data.get_ad_administrator_pass() is None or data.get_ad_administrator_pass().strip() == '':
            raise ValueError('Active directory administrator password is empty!')

        if data.get_domain() is None or data.get_domain().strip() == '':
            raise ValueError('Active directory domain name is empty!')

        if data.get_workgroup() is None or data.get_workgroup().strip() == '':
            raise ValueError('Active directory workgroup is empty!')

        
        self.logger.debug('Save /etc/samba/smb.conf file')
        # Save /etc/samba/smb.conf file
        template = Template()
        template.source = 'templates/smb.conf'
        template.destination = self.samba_conf_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        template.variables = { 'ad_domain':  data.get_domain().upper(), 
                              'ad_workgroup': data.get_workgroup()}
        
        if not template.save():
            self.logger.error('Error saving /etc/samba/smb.conf file')
            return False


        self.logger.debug('Save /etc/krb5.conf file')
        # Save /etc/krb5.conf file
        template = Template()
        template.source = 'templates/krb5.conf'
        template.destination = self.krb_conf_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        template.variables = { 'ad_domain':  data.get_domain(), 
                              'ad_domain_upper':  data.get_domain().upper()}
        
        if not template.save():
            self.logger.error('Error saving /etc/krb5.conf file')
            return False
              
        # Run "net ads join" command
        command = 'net ads join -U {0}%{1}'.format(data.get_ad_administrator_user(), data.get_ad_administrator_pass())
        self.logger.debug('running: %s'%(command))
        p = subprocess.Popen(command, shell=True, 
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            self.logger.debug(line)
                
        retval = p.wait()
        if retval != 0:
            self.logger.error(_('Error running command: ')+command)
            return False
              
              
        self.logger.debug('Save /etc/sssd/sssd.conf file')
        # Save /etc/samba/sssd.conf file
        template = Template()
        template.source = 'templates/sssd.conf.ad'
        template.destination = self.main_data_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00600
        template.variables = { 'ad_domain':  data.get_domain()}
        
        if not template.save():
            self.logger.error('Error saving /etc/sssd/sssd.conf file')
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
            return False        
        
        self.logger.debug('Save /usr/share/pam-configs/my_mkhomedir file')
        # Save /usr/share/pam-configs/my_mkhomedir file
        template = Template()
        template.source = 'templates/my_mkhomedir'
        template.destination = '/usr/share/pam-configs/my_mkhomedir'
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        template.variables = { }
        
        if not template.save():
            self.logger.error('Error saving /usr/share/pam-configs/my_mkhomedir file')
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
            return False           
        
        
        self.logger.debug('Save /etc/gca-sssd.control file')
        # Save /etc/gca-sssd.control file
        template = Template()
        template.source = 'templates/gca-sssd.control'
        template.destination = '/etc/gca-sssd.control'
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        template.variables = { 'auth_type':  'ad' }
        
        if not template.save():
            self.logger.error('Error saving /etc/gca-sssd.control file')
            return False           
        
        return True
        
    def _delete_active_directory(self, method):
        self.logger.debug('Deleting active directory user authentication method')
        data = method.get_data()


        # Run "net ads leave" command
        command = 'net ads leave -U {0}%{1}'.format(data.get_ad_administrator_user(), data.get_ad_administrator_pass())
        self.logger.debug('running: %s'%(command))
        p = subprocess.Popen(command, shell=True, 
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            self.logger.debug(line)
                
        retval = p.wait()
        if retval != 0:
            self.logger.error(_('Error running command: ')+command)
            return False

        # Delete configuration files
        self.logger.debug('Delete %s file'%(self.samba_conf_file))
        if os.path.isfile(self.samba_conf_file):
            os.remove(self.samba_conf_file)

        self.logger.debug('Delete %s file'%(self.krb_conf_file))
        if os.path.isfile(self.krb_conf_file):
            os.remove(self.krb_conf_file)
        
     
        self.logger.debug('Save /etc/sssd/sssd.conf file')
        # Save /etc/samba/sssd.conf file
        template = Template()
        template.source = 'templates/sssd.conf.local'
        template.destination = self.main_data_file
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00600
        template.variables = { }
        
        if not template.save():
            self.logger.error('Error saving /etc/sssd/sssd.conf file')
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
            return False        
        
        self.logger.debug('Delete %s file'%('/etc/gca-sssd.control'))
        if os.path.isfile('/etc/gca-sssd.control'):
            os.remove('/etc/gca-sssd.control')        

        return True


    def load(self):
        self.logger.debug('load - BEGIN')
      
        if not self.initiated:
            self.logger.warn(_('UserAuthenticationMethodDAO used without a proper initialization!'))
            # Return default method
            return LocalUsersAuthMethod()
      
        # Get authType of authentication method
        authType = None
        try:
            with open(self.main_data_file) as fp:
                for line in fp:
                    if line.strip() == 'domains = DEFAULT':
                        self.logger.debug('Detected authentication method: Internal')
                        authType = 'Internal'
                        break
                     
                    if line.strip() == 'id_provider = ad':
                        self.logger.debug('Detected authentication method: Active Directory')
                        authType = 'AD'
                        break
            
                    if line.strip() == 'id_provider = ldap':
                        self.logger.debug('Detected authentication method: LDAP')
                        authType = 'LDAP'
                        break
                
        except Exception:
            self.logger.error(_('Error reading file:')+ self.main_data_file)
            self.logger.error(str(traceback.format_exc()))            
        
        if authType is None:
            return LocalUsersAuthMethod()
        elif authType == 'AD':
            return self._load_active_directory()
        elif authType == 'LDAP':
            return self._load_ldap()
        else:
            return LocalUsersAuthMethod()
        
        
    def save(self, method):
        self.logger.debug('save - BEGIN')        
        
        if not self.initiated:
            self.logger.warn(_('UserAuthenticationMethodDAO used without a proper initialization!'))
            # Do nothing
            return
        
        
        if method is None:
            raise ValueError('method is None')
        
        if not isinstance(method, UserAuthenticationMethod):
            raise ValueError('method is not an instance of UserAuthenticationMethod')        
        
        if isinstance(method, LocalUsersAuthMethod):
            # Do nothing
            return True
        elif isinstance(method, ADAuthMethod):
            return self._save_active_directory(method)
        elif isinstance(method, LDAPAuthMethod):
            return self._save_ldap(method)
        else:
            raise ValueError('method is an instance of an unknown class')
        
        
    def delete(self, method):
        self.logger.debug('delete - BEGIN')        
        
        if not self.initiated:
            self.logger.warn(_('UserAuthenticationMethodDAO used without a proper initialization!'))
            # Do nothing
            return
        
        
        if method is None:
            raise ValueError('method is None')
        
        if not isinstance(method, UserAuthenticationMethod):
            raise ValueError('method is not an instance of UserAuthenticationMethod')        
        
        if isinstance(method, LocalUsersAuthMethod):
            # Do nothing
            return True
        elif isinstance(method, ADAuthMethod):
            return self._delete_active_directory(method)
        elif isinstance(method, LDAPAuthMethod):
            return self._delete_ldap(method)
        else:
            raise ValueError('method is an instance of an unknown class')        