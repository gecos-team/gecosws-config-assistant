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
__copyright__ = "Copyright (C) 2011, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"


###############################################
# DO NOT TOUCH THIS (HEAD TO THE SECOND PART) #
###############################################

import os
import sys
import glob

try:
    import DistUtilsExtra.auto
    from distutils.core import Command
    from DistUtilsExtra.command import *
except ImportError:
    print >> sys.stderr, 'To build gecos-config-assistant you need' + \
                         'https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', \
    'needs DistUtilsExtra.auto >= 2.18'

def get_datafiles(datadir):

    dfiles = []
    for root, _, files in os.walk(datadir):
        sources = []
        for f in files:
            sources.append(os.path.join(root,f))
        root_s = root.split('/')
        root_s.remove(datadir)
        root = str.join('/', root_s)
        dfiles.append(['share/gecosws-config-assistant/'+root, sources])
    return dfiles

datafiles = get_datafiles('data')
datafiles.append(
    ('share/applications/',
     glob.glob('data/gecos-config-assistant.desktop')))
datafiles.append(
    ('share/polkit-1/actions/',
     glob.glob('polkit/com.ubuntu.pkexec.gecos-config-assistant.policy')))

def update_config(values={}):
    ''' Update configuration '''

    oldvalues = {}
    try:
        fin = file(
            'gecosws_config_assistant/firstboot_lib/firstbootconfig.py',
            'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ')  # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "{} = {}\n".format(fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print "ERROR: Can't find gecosws_config_assistant/firstboot " + \
            "lib/firstbootconfig.py"
        sys.exit(1)
    return oldvalues

def update_desktop_file(datadir):
    ''' Update desktop file '''

    try:
        fin = file('gecos-config-assistant.desktop.in', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            if 'Icon=' in line:
                line = "Icon={}\n".format(datadir + 'media/wizard1.png')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print "ERROR: Can't find gecos-config-assistant.desktop.in"
        sys.exit(1)

def copy_pages(pages_path):
    pass

class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):

    def run(self):
        values = {
            '__firstboot_data_directory__': "'{}'".format(
                self.prefix + '/share/gecosws-config-assistant/'),
            '__version__': "'{}'".format(self.distribution.get_version()),
            '__firstboot_prefix__': "'{}'".format(self.prefix)
        }

        previous_values = update_config(values)
        update_desktop_file(self.prefix + '/share/gecosws-config-assistant/')
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)
        return True

class Clean(Command):
    description = "custom clean command that forcefully removes " + \
                  "dist/build directories and update data directory"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: {}'.format(
            self.cwd)
        os.system('rm -rf ./build ./dist')
        update_data_path(prefix, oldvalue)

class Check(Command):
    description = "Run unit tests"

    user_options = [
        ('module=', 'm', 'The test module to run'),
        ]

    def initialize_options(self):
        self.module = None

    def finalize_options(self):
        pass

    def get_command_name(self):
        return 'test'

    def run(self):
        import unittest

        import logging
        logging.basicConfig(level=logging.DEBUG)

        from gecosws_config_assistant.tests.dto.NTPServerTest import (
            NTPServerTest)
        from gecosws_config_assistant.tests.dto.NetworkInterfaceTest import (
            NetworkInterfaceTest)
        from gecosws_config_assistant.tests.dto.WorkstationDataTest import (
            WorkstationDataTest)
        from gecosws_config_assistant.tests.dto.GecosAccessDataTest import (
            GecosAccessDataTest)
        from gecosws_config_assistant.tests.dto.LocalUserTest import (
            LocalUserTest)
        from gecosws_config_assistant.tests.dto.UserAuthenticationMethodTest \
            import UserAuthenticationMethodTest
        from gecosws_config_assistant.tests.dto.LocalUsersAuthMethodTest \
            import LocalUsersAuthMethodTest
        from gecosws_config_assistant.tests.dto.ADSetupDataTest import (
            ADSetupDataTest)
        from gecosws_config_assistant.tests.dto.LDAPSetupDataTest import (
            LDAPSetupDataTest)
        from gecosws_config_assistant.tests.dto.ADAuthMethodTest import (
            ADAuthMethodTest)
        from gecosws_config_assistant.tests.dto.LDAPAuthMethodTest import (
            LDAPAuthMethodTest)
        from gecosws_config_assistant.tests.dto.SystemStatusTest import (
            SystemStatusTest)

        suite = unittest.TestSuite()
        # suite.addTest(NTPServerTest())
        # suite.addTest(NetworkInterfaceTest())
        # suite.addTest(WorkstationDataTest())
        # suite.addTest(GecosAccessDataTest())
        # suite.addTest(LocalUserTest())
        # suite.addTest(UserAuthenticationMethodTest())
        # suite.addTest(LocalUsersAuthMethodTest())
        # suite.addTest(ADSetupDataTest())
        # suite.addTest(LDAPSetupDataTest())
        # suite.addTest(ADAuthMethodTest())
        # suite.addTest(LDAPAuthMethodTest())
        # suite.addTest(SystemStatusTest())


        from gecosws_config_assistant.tests.util.PackageManagerTest import (
            PackageManagerTest)
        from gecosws_config_assistant.tests.util.TemplateTest import (
            TemplateTest)
        from gecosws_config_assistant.tests.util.JSONUtilTest import (
            JSONUtilTest)
        from gecosws_config_assistant.tests.util.ValidationTest import (
            ValidationTest)
        from gecosws_config_assistant.tests.util.GecosCCTest import (
            GecosCCTest)
        from gecosws_config_assistant.tests.util.CommandUtilTest import (
            CommandUtilTest)
        from gecosws_config_assistant.tests.util.SSLUtilTest import (
            SSLUtilTest)
        from gecosws_config_assistant.tests.util.GemUtilTest import (
            GemUtilTest)

        # suite.addTest(PackageManagerTest())
        # suite.addTest(TemplateTest())
        # suite.addTest(JSONUtilTest())
        # suite.addTest(ValidationTest())
        # suite.addTest(GecosCCTest())
        # suite.addTest(CommandUtilTest())
        suite.addTest(SSLUtilTest())
        # suite.addTest(GemUtilTest())

        from gecosws_config_assistant.tests.dao.NTPServerDAOTest import (
            NTPServerDAOTest)
        from gecosws_config_assistant.tests.dao.NetworkInterfaceDAOTest import (
            NetworkInterfaceDAOTest)
        from gecosws_config_assistant.tests.dao.WorkstationDataDAOTest import (
            WorkstationDataDAOTest)
        from gecosws_config_assistant.tests.dao.GecosAccessDataDAOTest import (
            GecosAccessDataDAOTest)
        from gecosws_config_assistant.tests.dao.LocalUserDAOTest import (
            LocalUserDAOTest)
        from gecosws_config_assistant.tests.dao.UserAuthenticationMethodDAOTest \
            import UserAuthenticationMethodDAOTest

        # suite.addTest(NTPServerDAOTest())
        # suite.addTest(NetworkInterfaceDAOTest())
        # suite.addTest(WorkstationDataDAOTest())
        # suite.addTest(GecosAccessDataDAOTest())
        # suite.addTest(LocalUserDAOTest())
        # suite.addTest(UserAuthenticationMethodDAOTest())


        return unittest.TextTestRunner(verbosity=2).run(suite)


##############################################################################
#################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ####################
##############################################################################

DistUtilsExtra.auto.setup(
    name='gecosws-config-assistant',
    version='2.1.7',
    license='GPL-2',
    author='GECOS Team',
    author_email='gecos@guadalinex.org',
    description='Configuration assistant for helping to connect a GECOS' \
                'workstation to different services',
    url='https://github.com/gecos-team/gecosws-config-assistant',

    keywords=['python', 'gnome', 'guadalinex', 'gecos'],

    packages=[
        'gecosws_config_assistant',
        'gecosws_config_assistant.view',
        'gecosws_config_assistant.dao',
        'gecosws_config_assistant.dto',
        'gecosws_config_assistant.util',
        'gecosws_config_assistant.controller',
        'gecosws_config_assistant.firstboot_lib',
    ],

    package_dir={
        'gecosws_config_assistant': 'gecosws_config_assistant',
        },

    scripts=[
        'bin/gecos-config-assistant',
        'bin/gecos-config-assistant-launcher'
    ],
    data_files = datafiles,
    cmdclass={
        'install': InstallAndUpdateDataDirectory,
        "build": build_extra.build_extra,
        "build_i18n":  build_i18n.build_i18n,
        'check': Check,
    }
)
