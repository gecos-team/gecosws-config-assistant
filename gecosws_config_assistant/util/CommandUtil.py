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
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"

import subprocess
import logging
import traceback
import sys
import time
import select

from gecosws_config_assistant.util.PasswordMaskingFilter import (
    PasswordMaskingFilter)

if 'check' in sys.argv:
    # Mock view classes for testing purposses
    print ("==> Loading mocks...")
    from gecosws_config_assistant.view.ViewMocks import askyesno_gtk
else:
    # Use real view classes
    from gecosws_config_assistant.view.CommonDialog import askyesno_gtk

class CommandUtil(object):
    '''
    Utility class to run commands.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('CommandUtil')
        self.logger.addFilter(PasswordMaskingFilter())

        # Timeout is 2000 milliseconds
        self.timeout = 2000


    def execute_command(self, cmd, my_env=None):
        ''' Execute a command '''

        if my_env is None:
            my_env = {}

        output = self.get_command_output(cmd, my_env)
        return output != False

    def get_command_output(self, cmd, my_env=None):
        ''' Getting command output '''

        if my_env is None:
            my_env = {}

        output = []
        self.logger.debug('CMD: %s',cmd)
        try:
            p = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                env=my_env)

            # Read the process output with a timeout
            line = ''
            previous_line = ''
            c = p.stdout.read(1).decode("utf-8")
            lastread = int(round(time.time() * 1000))
            read = True
            
            while c:
                if read:
                    read = False
                    line += c

                    if c == '\n':
                        self.logger.debug(line)
                        output.append(line.strip())
                        previous_line = line
                        line = ''

                r, _, _ = select.select([ p.stdout ], [], [], 0.050)
                if p.stdout in r:
                    c = p.stdout.read(1).decode("utf-8")
                    lastread = int(round(time.time() * 1000))
                    read = True
                
                # Try to detect when the command waits for a yes/no question
                if (
                    (int(round(time.time() * 1000)) - lastread > self.timeout
                    and (line.find('?') > 0 or
                    previous_line.find('?') > 0))
                ):
                    self.logger.debug('QUESTION DETECTED: %s', line)
                    response =  askyesno_gtk(cmd, "\n".join(output), None)

                    if response:
                        p.stdin.write('y\n')
                    else:
                        p.stdin.write('n\n')

            retval = p.wait()
            if retval != 0:
                self.logger.error('Error running command: %s',cmd)
                return False

        except Exception as ex:
            self.logger.error("AMI:" + str(ex))
            self.logger.error('Error running command: %s',cmd)
            self.logger.error(str(traceback.format_exc()))
            return False

        return output
