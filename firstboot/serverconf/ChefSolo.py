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
import time
import re
from firstboot_lib.firstbootconfig import get_prefix
from gettext import gettext as _
import gettext
gettext.textdomain('gecosws-config-assistant')

def handle_data(source, condition):
    print "handle data!"
    data = source.recv(12)
    print len(data)
    if len(data) > 0:
        return True #run forever
    else:
        print 'closed'
        return False # stop looping

class ChefSolo(threading.Thread):
    def __init__(self, filepath, server_conf, unlink, gcc_conf, chef_conf, status_label, log):
        self.filepath = filepath
        self.unlink = unlink
        self.gcc_conf = gcc_conf
        self.chef_conf = chef_conf
        self.server_conf = server_conf
        self.exit_code = 0
        self.status_label = status_label
        self.log = log
        threading.Thread.__init__(self)

    def get_exit_code(self):
        return self.exit_code

    def run(self):
        gem_repo = self.server_conf.get_gem_repo()
        envs = os.environ
#TODO: do not use this forced localization
#        envs['LANG'] = 'es_ES.UTF-8'
        log_timestamp = time.strftime("%Y%m%d%H%M%S")
        log_chef_solo = open("/tmp/chef-solo-%s"%(log_timestamp), "w", 1)
        log_chef_solo_err = open("/tmp/chef-solo-err-%s"%(log_timestamp), "w", 1)

        self.status_label.set_text(_("Preparing GEMs..."))
        cmd = '"/opt/chef/embedded/bin/gem" "source" "--list"'
        cmd_split = shlex.split(cmd)
        process = subprocess.Popen(cmd_split, stdout=subprocess.PIPE, env=envs)
        os.waitpid(process.pid, 0)
        output = process.communicate()[0]

        sources = output.split('\n')
        sources.pop(0)
        sources.pop(0)
        sources.pop(len(sources) - 1)

        for source in sources:
            cmd = '"/opt/chef/embedded/bin/gem" "source" "-r" "%s"' % (source)
            cmd_split = shlex.split(cmd)
            log_chef_solo.write(cmd)
            log_chef_solo.write("\n---------------------------------------\n")
            log_chef_solo.flush()
            log_chef_solo_err.write(cmd)
            log_chef_solo_err.write("\n---------------------------------------\n")
            log_chef_solo_err.flush()
            process = subprocess.Popen(cmd_split, stdout=log_chef_solo, stderr=log_chef_solo_err, env=envs)
            os.waitpid(process.pid, 0)
            log_chef_solo.flush()
            log_chef_solo_err.flush()


        cmd = '"/opt/chef/embedded/bin/gem" "source" "-a" "%s"' % (gem_repo)
        cmd_split = shlex.split(cmd)
        log_chef_solo.write(cmd)
        log_chef_solo.write("\n---------------------------------------\n")
        log_chef_solo.flush()
        log_chef_solo_err.write(cmd)
        log_chef_solo_err.write("\n---------------------------------------\n")
        log_chef_solo_err.flush()
        process = subprocess.Popen(cmd_split, stdout=log_chef_solo, stderr=log_chef_solo_err, env=envs)
        os.waitpid(process.pid, 0)
        log_chef_solo.flush()
        log_chef_solo_err.flush()

        self.status_label.set_text(_("Running chef-solo..."))
        solo_rb = get_prefix() + '/share/gecosws-config-assistant/solo.rb'
        cmd = '"chef-solo" "-c" "%s" "-j" "%s"' % (solo_rb, self.filepath)
        cmd_split = shlex.split(cmd)
        log_chef_solo.write(cmd)
        log_chef_solo.write("\n---------------------------------------\n")
        log_chef_solo.flush()
        log_chef_solo_err.write(cmd)
        log_chef_solo_err.write("\n---------------------------------------\n")
        log_chef_solo_err.flush()

        process = subprocess.Popen(cmd_split, stdout=subprocess.PIPE, env=envs)
        p = re.compile( '\\[[^\\[]+\\]')
        for line in process.stdout:
            buf = self.log.get_buffer()
            buf.insert_at_cursor(p.sub('', line.decode())) 
            log_chef_solo.write(line.decode())
            self.log.scroll_to_mark(buf.get_insert(), 0, False, 0, 0)

        self.exit_code = os.waitpid(process.pid, 0)
        log_chef_solo.flush()
        log_chef_solo_err.flush()

        output = process.communicate()[0]
        if not self.unlink and self.gcc_conf and self.chef_conf and os.path.exists("/usr/bin/gecos-chef-client-wrapper"):
            self.status_label.set_text(_("Running chef-client-wrapper..."))
            cmd = '"gecos-chef-client-wrapper"'
            cmd_split = shlex.split(cmd)
            process = subprocess.Popen(cmd_split, env=envs)
            self.exit_code = os.waitpid(process.pid, 0)
            output = process.communicate()[0]

        
            