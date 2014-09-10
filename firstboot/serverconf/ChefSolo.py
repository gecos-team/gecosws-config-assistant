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

__author__ = "David Amian <damian@emergya.com>"
__copyright__ = "Copyright (C) 2014, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

import os
import subprocess
import shlex
import threading

from gi.repository import Gtk
from firstboot_lib import firstbootconfig
from gi.repository import Gtk
import gettext
import firstboot.serverconf as serverconf
from firstboot_lib.firstbootconfig import get_prefix
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class ChefSolo(threading.Thread):
    def __init__(self, filepath):
        self.filepath = filepath
        self.exit_code = 0
        threading.Thread.__init__(self)

    def get_exit_code(self):
		return self.exit_code

    def run(self):
        server_conf = serverconf.get_server_conf(None)
        gem_repo = server_conf.get_gem_repo()
        envs = os.environ
        envs['LANG'] = 'es_ES.UTF-8'
        log_chef_solo = open('/tmp/chef-solo', "w", 1)
        log_chef_solo_err = open('/tmp/chef-solo-err', "w", 1)

        cmd = '"/opt/chef/embedded/bin/gem" "source" "-c"'
        cmd_split = shlex.split(cmd)
        process = subprocess.Popen(cmd_split, stdout=log_chef_solo, stderr=log_chef_solo_err, env=envs)

        cmd = '"/opt/chef/embedded/bin/gem" "source" "-a" "%s"' % (gem_repo)
        cmd_split = shlex.split(cmd)
        process = subprocess.Popen(cmd_split, stdout=log_chef_solo, stderr=log_chef_solo_err, env=envs)
        

        solo_rb = get_prefix() + '/share/gecosws-config-assistant/solo.rb'
        cmd = '"chef-solo" "-c" "%s" "-j" "%s"' % (solo_rb, self.filepath)
        cmd_split = shlex.split(cmd)
        process = subprocess.Popen(cmd_split, stdout=log_chef_solo, stderr=log_chef_solo_err, env=envs)
        self.exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]
	
	
	        