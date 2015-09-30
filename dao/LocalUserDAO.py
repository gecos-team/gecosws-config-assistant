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

from dto.LocalUser import LocalUser

import logging

import pwd
import subprocess

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')


class LocalUserDAO(object):
    '''
    DAO class to manipulate LocalUser DTO objects.
    '''

    # Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LocalUserDAO, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance



    def __init__(self):
        '''
        Constructor
        '''
        
        self.logger = logging.getLogger('LocalUserDAO')
        self.min_uid = 1000
     
        

    def loadAll(self):
        self.logger.debug('loadAll - BEGIN')
        users = []
        
        
        for user in pwd.getpwall():
            if user.pw_uid < self.min_uid or user.pw_name == 'nobody':
                continue
            
            lu = LocalUser()
            lu.set_login(user.pw_name) 
            lu.set_name(unicode(user.pw_gecos.split(',')[0], 'utf-8', 'replace'))
            
            # For security reasons can't get raw user password
            lu.set_password(None)
            
            users.append(lu)        
      
        return users

    def existsUser(self, local_user):
        if local_user is None:
            return False
        
        if not isinstance(local_user, LocalUser):
            return False
        
        if local_user.get_login() is None:
            return False
               
        try:
            pwd.getpwnam(local_user.get_login())
            return True
        except KeyError:
            return False        

    def save(self, local_user):
        self.logger.debug('save - BEGIN')
        if local_user is None:
            raise ValueError('local_user is None')
        
        if not isinstance(local_user, LocalUser):
            raise ValueError('local_user is not a LocalUser instance')
        
        if not self.existsUser(local_user):
            # Create a new user
            self.logger.debug('creating new user: %s'%(local_user.get_login()))
            p = subprocess.Popen('LC_ALL=C adduser --gecos "%s" %s'%(local_user.get_name(), local_user.get_login()), shell=True, 
                                 stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            p.stdin.write("%s\n"%(local_user.get_password()))
            p.stdin.write("%s\n"%(local_user.get_password()))
            
            for line in p.stdout.readlines():
                line = line.strip()
                self.logger.debug(line)
            
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error creating user: ')+local_user.get_login())
            
        else:   
            # Modify an existent user
            self.logger.debug('setting information for user: %s'%(local_user.get_login()))
            p = subprocess.Popen('usermod -c "%s" %s'%(local_user.get_name(), local_user.get_login()), shell=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                self.logger.debug(line)
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error modifying user name: ')+local_user.get_login())

            # Change password            
            self.logger.debug('setting password for user: %s'%(local_user.get_login()))
            p = subprocess.Popen('LC_ALL=C passwd %s'%(local_user.get_login()), shell=True, 
                                 stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.stdin.write("%s\n"%(local_user.get_password()))
            p.stdin.write("%s\n"%(local_user.get_password()))
            for line in p.stdout.readlines():
                self.logger.debug(line)
                line = line.strip()
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error modifying user password: ')+local_user.get_login())
            
        self.logger.debug('save - END')


    def delete(self, local_user):
        self.logger.debug('delete - BEGIN')
        if local_user is None:
            raise ValueError('local_user is None')
        
        if not isinstance(local_user, LocalUser):
            raise ValueError('local_user is not a LocalUser instance')
        
        if not self.existsUser(local_user):
            raise ValueError('Trying to delete a non existent user: %s'%(local_user.get_login()))
        else:
            self.logger.debug('Deleting user: %s'%(local_user.get_login()))
            p = subprocess.Popen('userdel %s'%(local_user.get_login()), shell=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                self.logger.debug(line)
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error deleting user: ')+local_user.get_login())

            self.logger.debug('Deleting folder user: %s'%(local_user.get_login()))
            p = subprocess.Popen('rm -rf /home/%s'%(local_user.get_login()), shell=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                self.logger.debug(line)
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error(_('Error deleting user home: ')+local_user.get_login())
                
                