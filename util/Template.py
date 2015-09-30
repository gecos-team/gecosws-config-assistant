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
import grp
import pwd
import os

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')


class Template(object):
    '''
    Utility class to manipulate templates.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('Template')
        
        self.source = None
        self.destination = None
        self.owner = None
        self.group = None
        self.mode = None
        self.variables = {}
        

    def save(self):
        if self.source is None:
            raise ValueError('source is None')
        if self.destination is None:
            raise ValueError('destination is None')
        
        try:
            contents = ''
            # Read the template
            with open(self.source, 'r+') as f:
                contents = f.read()
        
            # Replace the variables
            for key, value in self.variables.items():
                contents = contents.replace('${%s}'%(key), value)
                
            # Eliminate non existing IF blocks
            lines = contents.splitlines()
            keeplines = []
            inIfBlock = False
            existKey = False
            lineno = 0
            for line in lines:
                lineno = lineno + 1
                if line.strip() == '#{ENDIF}':
                    if inIfBlock:
                        inIfBlock = False
                        existKey = False
                        continue
                    else:
                        self.logger.warn('Detected ENDIF without IF in line %s'%(lineno))
                
                if line.strip().startswith('#{IF '):
                    key = line.replace('#{IF ', '').replace('}','').strip()
                    inIfBlock = True
                    existKey = (key in self.variables.keys())
                    continue
                
                if inIfBlock and not existKey:
                    continue
                
                keeplines.append(line)
            
            contents = "\n".join(keeplines)
                
            # Save the file
            with open(self.destination, 'w') as f:
                f.write(contents)
                
            # Check the owner and permissions
            stat_info = os.stat(self.destination)
            uid = stat_info.st_uid
            gid = stat_info.st_gid

            current_usr = pwd.getpwuid(uid)[0]
            current_grp = grp.getgrgid(gid)[0]
            
            if self.owner is not None and current_usr != self.owner:
                uid = pwd.getpwnam(self.owner).pw_uid
                if uid is None:
                    self.logger.error(_('Can not find user to be used as owner: ') + self.owner)
                else:
                    os.chown(self.destination, uid, gid)  
                
            if self.group is not None and current_grp != self.group:
                gid = grp.getgrnam(self.group).gr_gid
                if gid is None:
                    self.logger.error(_('Can not find group to be used as owner: ') + self.group)
                else:
                    os.chown(self.destination, uid, gid)  
                
            m = stat_info.st_mode & 00777
            if self.mode is not None and m != self.mode:
                os.chmod(self.destination, self.mode)
                 
            return True
        
        except:
            self.logger.error(_('Error saving template:') + self.source)
            self.logger.error(str(traceback.format_exc()))

       
        
        return False


