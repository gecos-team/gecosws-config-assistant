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

import logging
import os

from gecosws_config_assistant.util.CommandUtil import CommandUtil

class GemUtil(object):
    '''
    Utility class to configure Ruby GEMs.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('GemUtil')
        # Embebed Chef installation
        self.command = "/opt/chef/embedded/bin/gem"

        if not os.path.isfile(self.command):
            # Linux distribution Chef installation
            self.command = "/usr/bin/gem"

        self.commandUtil = CommandUtil()

    def get_gem_sources_list(self):
        list = []

        output = self.commandUtil.get_command_output('%s source --list'%(self.command))

        for line in output:
            if line.startswith('http'):
                list.append(line.strip())

        return list
        
    def remove_all_gem_sources(self):
        sources = self.get_gem_sources_list()
        for source in sources:
            print "removing %s", source
            self.commandUtil.execute_command('%s source -r "%s"'%(self.command, source))

    def add_gem_source(self, url):
        return self.commandUtil.execute_command('%s source -a "%s"'%(self.command, url))

    def is_gem_intalled(self, gem_name):
        output = self.commandUtil.get_command_output('%s list'%(self.command))
        res = False
        if output != False:
            for line in output:
                if line.startswith(gem_name + ' '):
                    res = True

        return res

    def install_gem(self, gem_name):
        return self.commandUtil.execute_command('%s install "%s"'%(self.command, gem_name))

    def uninstall_gem(self, gem_name):
        return self.commandUtil.execute_command('%s uninstall "%s"'%(self.command, gem_name))
