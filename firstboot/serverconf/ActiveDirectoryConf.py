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

__author__ = "David Amian Valle <damian@emergya.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

import firstboot.validation as validation

class ActiveDirectoryProperties():
    def __init__(self):
        self._data = {}
        self._data['fqdn'] = ''
        self._data['workgroup'] = ''
        self._data['sssd_conf'] = ''
        self._data['krb5_conf'] = ''
        self._data['smb_conf'] = ''
        self._data['pam_conf'] = ''

    def load_data(self, conf, specific):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        if not specific:
            try:
                self.set_fqdn(conf['fqdn'])
            except KeyError as e:
                print msg % ('fqdn',)
            try:
                self.set_workgroup(conf['workgroup'])
            except KeyError as e:
                print msg % ('workgroup',)
            
        else:
            try:
                self.set_sssd_conf(conf['sssd_conf'])
            except KeyError as e:
                print msg % ('sssd_conf',)
            try:
                self.set_krb5_conf(conf['krb5_conf'])
            except KeyError as e:
                print msg % ('krb5_conf',)
            try:
                self.set_smb_conf(conf['smb_conf'])
            except KeyError as e:
                print msg % ('smb_conf',)
            try:
                self.set_pam_conf(conf['pam_conf'])
            except KeyError as e:
                print msg % ('pam_conf',)

    def get_fqdn(self):
        return self._data['fqdn'].encode('utf-8')
    
    def set_fqdn(self, fqdn):
        self._data['fqdn'] = fqdn
        return self

    def get_workgroup(self):
        return self._data['workgroup'].encode('utf-8')

    def set_workgroup(self, workgroup):
        self._data['workgroup'] = workgroup
        return self

    def get_sssd_conf(self):
        return self._data['sssd_conf']

    def set_sssd_conf(self, sssd_conf):
        self._data['sssd_conf'] = sssd_conf
        return self

    def get_krb5_conf(self):
        return self._data['krb5_conf']

    def set_krb5_conf(self, krb5_conf):
        self._data['krb5_conf'] = krb5_conf
        return self

    def get_smb_conf(self):
        return self._data['smb_conf']

    def set_smb_conf(self, smb_conf):
        self._data['smb_conf'] = smb_conf
        return self



class ActiveDirectoryConf():

    def __init__(self):
        self._data = {}
        self._data['specific_conf'] = ''
        self._ad_properties = ActiveDirectoryProperties()

    def load_data(self, conf):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        try:
            self.set_fqdn(conf['specific_conf'])
        except KeyError as e:
            print msg % ('specific_conf',)
        try:
            self.set_ad_properites.load_data(conf['auth_properties'])
        except KeyError as e:
            print msg % ('auth_properties',)

    def validate(self):
        return True

    def get_specific_conf(self):
        return self._data['specific_conf'].encode('utf-8')

    def set_specific_conf(self, specific_conf):
        self._data['specific_conf'] = specific_conf
        return self

    def get_auth_properties(self):
        return self._ad_properties

    def __str__(self):
        return str(self._data)
