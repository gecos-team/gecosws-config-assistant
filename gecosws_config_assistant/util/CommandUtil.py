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
__copyright__ = "Copyright (C) 2016, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

import subprocess
import logging
import traceback

class CommandUtil(object):
    '''
    Utility class to run commands.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('CommandUtil')


    def execute_command(self, cmd, my_env={}):
        try:
            p = subprocess.Popen(cmd, shell=True, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 env=my_env)
            for line in p.stdout.readlines():
                self.logger.debug(line)
                    
            retval = p.wait()
            if retval != 0:
                self.logger.error('Error running command: %s'%(cmd))
                return False     
            
        except:
            self.logger.error('Error running command: %s'%(cmd))
            self.logger.error(str(traceback.format_exc()))
            return False        
        
        
        return True   
        
