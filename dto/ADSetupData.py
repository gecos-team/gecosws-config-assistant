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

class ADSetupData(object):
    '''
    DTO object that represents Active Directory authentication method data.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.domain = ''
        self.workgroup = ''
        self.ad_administrator_user = None
        self.ad_administrator_pass = None
        
        self.logger = logging.getLogger('ADSetupData')

    def get_ad_administrator_user(self):
        return self.__ad_administrator_user


    def get_ad_administrator_pass(self):
        return self.__ad_administrator_pass


    def set_ad_administrator_user(self, value):
        self.__ad_administrator_user = value


    def set_ad_administrator_pass(self, value):
        self.__ad_administrator_pass = value


    def get_domain(self):
        return self.__domain


    def get_workgroup(self):
        return self.__workgroup


    def set_domain(self, value):
        self.__domain = value


    def set_workgroup(self, value):
        self.__workgroup = value


    def test(self):
        # Test AD connection
        result = False
        
        if self.get_domain() is None or self.get_domain().strip() == '':
            self.logger.debug('Empty domain!')
            return False

        if self.get_workgroup() is None or self.get_workgroup().strip() == '':
            self.logger.debug('Empty workgroup!')
            return False

        if self.get_ad_administrator_user() is None or self.get_ad_administrator_user().strip() == '':
            self.logger.debug('Empty administrator username!')
            return False

        if self.get_ad_administrator_pass() is None or self.get_ad_administrator_pass().strip() == '':
            self.logger.debug('Empty administrator pass!')
            return False


        
        try:
            ld = ldap.initialize('ldap://%s'%(self.get_domain()))
            ld.protocol_version = 3
            ld.set_option(ldap.OPT_REFERRALS, 0)
            
            user = "%s@%s"%(self.get_ad_administrator_user(), self.get_domain())
            password = self.get_ad_administrator_pass()
            ld.simple_bind_s(user, password) 

            return True

        except:
            self.logger.warn('Error connecting to AD server: %s'%(self.get_domain()))
            self.logger.warn(str(traceback.format_exc()))          
            
        return result




    domain = property(get_domain, set_domain, None, None)
    workgroup = property(get_workgroup, set_workgroup, None, None)
    ad_administrator_user = property(get_ad_administrator_user, set_ad_administrator_user, None, None)
    ad_administrator_pass = property(get_ad_administrator_pass, set_ad_administrator_pass, None, None)





