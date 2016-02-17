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
import traceback
import ldap

class LDAPSetupData(object):
    '''
    DTO object that represents the necessary data to setup LDAP user 
    authentication method.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.uri = ''
        self.base = ''
        self.baseGroup = ''
        self.bindUserDN = ''
        self.bindUserPWD = ''
        self.logger = logging.getLogger('LDAPSetupData')

    def get_uri(self):
        return self.__uri


    def get_base(self):
        return self.__base


    def get_base_group(self):
        return self.__baseGroup


    def get_bind_user_dn(self):
        return self.__bindUserDN


    def get_bind_user_pwd(self):
        return self.__bindUserPWD


    def set_uri(self, value):
        self.__uri = value


    def set_base(self, value):
        self.__base = value


    def set_base_group(self, value):
        self.__baseGroup = value


    def set_bind_user_dn(self, value):
        self.__bindUserDN = value


    def set_bind_user_pwd(self, value):
        self.__bindUserPWD = value
        
    def test(self):
        # Test LDAP connection
        result = False
        
        if self.get_uri() is None or self.get_uri().strip() == '':
            self.logger.debug('Empty URI!')
            return False

        if self.get_base() is None or self.get_base().strip() == '':
            self.logger.debug('Empty base DN!')
            return False

        if (self.get_bind_user_dn() is not None and self.get_bind_user_dn().strip() != ''
            and (self.get_bind_user_pwd() is None or self.get_bind_user_pwd().strip() == '')):
            self.logger.debug('Empty bind user password!')
            return False

        
        try:
            ld = ldap.initialize(self.get_uri())
            
            if self.get_bind_user_dn() is None or self.get_bind_user_dn().strip() == '':
                #  Bind anonymously
                ld.simple_bind_s()
            else:
                ld.simple_bind_s(self.get_bind_user_dn(), self.get_bind_user_pwd())

            # Check user DN
            ldapfilter = "(objectclass=*)"
            results = ld.search_ext_s(self.get_base(), ldap.SCOPE_ONELEVEL, ldapfilter, None, 0, None, None, -1, 1)
            if results is None:
                return False
            else:
                self.logger.debug('LDAP user DN check was successful')            


            # Check user groups DN
            if self.get_base_group() is not None and self.get_base_group().strip() != '':
                results = ld.search_ext_s(self.get_base(), ldap.SCOPE_ONELEVEL, ldapfilter, None, 0, None, None, -1, 1)
                if results is None:
                    return False
                else:
                    self.logger.trace('LDAP group check was successful')

            return True

        except:
            self.logger.warn('Error connecting to LDAP server: %s'%(self.get_uri()))
            self.logger.warn(str(traceback.format_exc()))          
            
        return result
            
    uri = property(get_uri, set_uri, None, None)
    base = property(get_base, set_base, None, None)
    baseGroup = property(get_base_group, set_base_group, None, None)
    bindUserDN = property(get_bind_user_dn, set_bind_user_dn, None, None)
    bindUserPWD = property(get_bind_user_pwd, set_bind_user_pwd, None, None)




