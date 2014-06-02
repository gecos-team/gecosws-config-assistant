#!/usr/bin/env python
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

__author__ = "Antonio Hernández <ahernandez@emergya.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys
import glob

try:
    import DistUtilsExtra.auto
    from distutils.core import setup, Command
    from DistUtilsExtra.command import *
except ImportError:
    print >> sys.stderr, 'To build gecos-config-assistant you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def get_datafiles(datadir):
    source = ''
    datafiles = []
    for root, dirs, files in os.walk(datadir):
        sources = []
        for f in files:
            sources.append(os.path.join(root,f))
        root_s = root.split('/')
        root_s.remove(datadir)
        root = str.join('/', root_s)
        datafiles.append(['share/gecosws-config-assistant/'+root, sources])
    return datafiles

datafiles = get_datafiles('data')
datafiles.append(('share/applications/', glob.glob('data/gecos-config-assistant.desktop')))

def update_config(values={}):

    oldvalues = {}
    try:
        fin = file('firstboot_lib/firstbootconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ')  # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find firstboot_lib/firstbootconfig.py")
        sys.exit(1)
    return oldvalues


def create_solo_rb(datadir):
    try:
        fout = file('data\solo.rb', 'w')
        line = "cookbook_path \"" + datadir + "cookbooks/\""
        fout.write(line)
        fout.close()
    except (OSError, IOError), e:
        print ("ERROR: Can't create data/solo.rb file")
        sys.exit(1)


def update_desktop_file(datadir):

    try:
        fin = file('gecos-config-assistant.desktop.in', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            if 'Icon=' in line:
                line = "Icon=%s\n" % (datadir + 'media/wizard1.png')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find gecos-config-assistant.desktop.in")
        sys.exit(1)


def copy_pages(pages_path):
    pass


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__firstboot_data_directory__': "'%s'" % (
                                        self.prefix + '/share/gecosws-config-assistant/'),
                  '__version__': "'%s'" % self.distribution.get_version(),
                  '__firstboot_prefix__': "'%s'" % self.prefix}
        previous_values = update_config(values)
        update_desktop_file(self.prefix + '/share/gecosws-config-assistant/')
        create_solo_rb(self.prefix + '/share/gecosws-config-assistant/')
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


class Clean(Command):
    description = "custom clean command that forcefully removes dist/build directories and update data directory"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./build ./dist')
        update_data_path(prefix, oldvalue)


##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='gecosws-config-assistant',
    version='0.5.1-0gecos1',
    license='GPL-2',
    author='David Amian',
    author_email='damian@emergya.com',
    description='First start assistant for helping to connect a GECOS \
workstation to different services',
    url='https://github.com/gecos-team/gecosws-config-assistant',

    keywords=['python', 'gnome', 'guadalinex', 'gecos'],

    packages=[
        'firstboot',
        'firstboot_lib',
        'firstboot.pages',
        'firstboot.serverconf',
        'firstboot.pages.installSoftware',
        'firstboot.pages.linkToChef',
        'firstboot.pages.linkToServer',
        'firstboot.pages.localUsers',
        'firstboot.pages.network',
        'firstboot.pages.pcLabel',
        'firstboot.pages.dateSync',
        'firstboot.pages.autoConfig',
    ],

    package_dir={
        'firstboot': 'firstboot',
        'firstboot_lib': 'firstboot_lib',
        'firstboot.pages': 'firstboot/pages',
        'firstboot.serverconf': 'firstboot/serverconf',
        'firstboot.pages.installSoftware': 'firstboot/pages/installSoftware',
        'firstboot.pages.linkToServer': 'firstboot/pages/linkToServer',
        'firstboot.pages.linkToChef': 'firstboot/pages/linkToChef',
        'firstboot.pages.localUsers': 'firstboot/pages/localUsers',
        'firstboot.pages.network': 'firstboot/pages/network',
        'firstboot.pages.pcLabel': 'firstboot/pages/pcLabel',
        'firstboot.pages.dateSync': 'firstboot/pages/dateSync',
        'firstboot.pages.autoConfig': 'firstboot/pages/autoConfig',
        },

    scripts=[
        'bin/gecos-config-assistant',
        'bin/gecos-config-assistant-launcher'
    ],
    data_files = datafiles,
  #  data_files=[
  #     ('share/gecosws-config-assistant/media', glob.glob('data/media/*')),
  #     ('share/gecosws-config-assistant/cookbooks', glob.glob('data/cookbooks/*')),
  #     ('share/gecosws-config-assistant/ui', glob.glob('data/ui/*')),
  #     #('/etc/xdg/autostart/', glob.glob('data/gecos-config-assistant.desktop')),
  #  ],

    cmdclass={
        'install': InstallAndUpdateDataDirectory,
        "build": build_extra.build_extra,
        "build_i18n":  build_i18n.build_i18n,
        "clean": [clean_i18n.clean_i18n, Clean],
    }
)
