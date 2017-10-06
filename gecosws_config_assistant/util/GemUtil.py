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
from gecosws_config_assistant.util.PackageManager import PackageManager

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
        self.rubyEmbeddedInChef = True
        self.sys_gemrc = "/etc/gemrc"

        if not os.path.isfile(self.command):
            # Linux distribution Chef installation
            self.command = "/usr/bin/gem"
            self.rubyEmbeddedInChef = False

        self.commandUtil = CommandUtil()
        self.pm = PackageManager()

    def get_gem_sources_list(self):
        list = []

        output = self.commandUtil.get_command_output('%s source --list'%(self.command))

        for line in output:
            if line.startswith('http'):
                list.append(line.strip())

        return list
    def clear_cache_gem_sources(self):

        return self.commandUtil.execute_command('%s source -c --config-file "%s"'%(self.command, self.sys_gemrc))
        
    def remove_all_gem_sources(self):
        sources = self.get_gem_sources_list()
        for source in sources:
            print "removing %s", source
            self.commandUtil.execute_command('%s source -r "%s" --config-file "%s"'%(self.command, source, self.sys_gemrc))
        if os.path.exists(self.sys_gemrc):
            os.remove(self.sys_gemrc)

    # Adding only gecoscc.ini source ("gem_repo")
    # The gem add command adds https://rubygems.org source by default. We must manually delete it.
    def add_gem_only_one_source(self, url):

        res = self.add_gem_source(url)
        # Remove default source
        res &= self.commandUtil.execute_command('%s source -r "%s" --config-file "%s"'%(self.command,'https://rubygems.org/', self.sys_gemrc))

        if res and url == 'https://rubygems.org/':
            res = self.add_gem_source(url)

        return res
    def add_gem_source(self, url):
        return self.commandUtil.execute_command('%s source -a "%s" --config-file "%s"'%(self.command, url, self.sys_gemrc))

    def is_gem_intalled(self, gem_name):
        output = self.commandUtil.get_command_output('%s list'%(self.command))
        res = False
        if output != False:
            for line in output:
                if line.startswith(gem_name + ' '):
                    res = True

        return res

    def install_gem(self, gem_name):
        if not self.rubyEmbeddedInChef:
            # Try to install the GEM by using the package manager
            package_name = gem_name
            if not package_name.startswith('ruby-'):
                package_name = 'ruby-%s'%(package_name)
                
            if (self.pm.exists_package(package_name) and not self.pm.is_package_installed(package_name)):
                self.pm.install_package(package_name)
            
            if self.is_gem_intalled(gem_name):
                # GEM installed successfully by using the package manager
                return True
                
            # GEM is not installed successfully
            if not self.pm.is_package_installed('build-essential'):
                # We will need 'build-essential' package to build GEMs
                self.pm.install_package('build-essential')
            
        return self.commandUtil.execute_command('%s install "%s"'%(self.command, gem_name), os.environ)

    def uninstall_gem(self, gem_name):
        if not self.rubyEmbeddedInChef:
            # Try to uninstall the GEM by using the package manager
            package_name = gem_name
            if not package_name.startswith('ruby-'):
                package_name = 'ruby-%s'%(package_name)
                
            if (self.pm.exists_package(package_name) and self.pm.is_package_installed(package_name)):
                self.pm.remove_package(package_name)        
                
            if not self.is_gem_intalled(gem_name):
                # GEM uninstalled successfully by using the package manager
                return True    
    
        return self.commandUtil.execute_command('%s uninstall "%s"'%(self.command, gem_name))
