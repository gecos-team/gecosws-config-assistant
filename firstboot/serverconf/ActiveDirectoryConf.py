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

    def load_data(self, conf, specific):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        if not specific:
            try:
                self.set_domain(conf['fqdn'])
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

    def get_domain(self):
        if not 'domain' in self._data:
            self._data['domain'] = ''
        return self._data['domain'].encode('utf-8')
    
    def set_domain(self, domain):
        self._data['domain'] = domain
        return self

    def get_workgroup(self):
        if not 'workgroup' in self._data:
            self._data['workgroup'] = ''
        return self._data['workgroup'].encode('utf-8')

    def set_workgroup(self, workgroup):
        self._data['workgroup'] = workgroup
        return self

    def get_sssd_conf(self):
        if not 'sssd_conf' in self._data:
            self._data['sssd_conf'] = ''
        return self._data['sssd_conf']

    def set_sssd_conf(self, sssd_conf):
        self._data['sssd_conf'] = sssd_conf
        return self

    def get_krb5_conf(self):
        if not 'krb5_conf' in self._data:
            self._data['krb5_conf'] = ''
        return self._data['krb5_conf']

    def set_krb5_conf(self, krb5_conf):
        self._data['krb5_conf'] = krb5_conf
        return self

    def get_smb_conf(self):
        if not 'smb_conf' in self._data:
            self._data['smb_conf'] = ''
        return self._data['smb_conf']

    def set_smb_conf(self, smb_conf):
        self._data['smb_conf'] = smb_conf
        return self

    def get_pam_conf(self):
        if not 'pam_conf' in self._data:
            self._data['pam_conf'] = ''
        return self._data['pam_conf']

    def set_pam_conf(self, pam_conf):
        self._data['pam_conf'] = pam_conf
        return self

    def set_user_ad(self, user_ad):
        self._data['user_ad'] = user_ad
        return self

    def set_passwd_ad(self, passwd_ad):
        self._data['passwd_ad'] = passwd_ad
        return self

    def get_user_ad(self):
        if not 'user_ad' in self._data:
            self._data['user_ad'] = ''
        return self._data['user_ad']

    def get_passwd_ad(self):
        if not 'passwd_ad' in self._data:
            self._data['passwd_ad'] = ''
        return self._data['passwd_ad']


    def validate(self, specific):
        if specific:
            return self.get_pam_conf() != '' and self.get_smb_conf() != '' and self.get_krb5_conf() != '' and self.get_sssd_conf() != '' and get_user_ad() != '' and get_passwd_ad() != ''
        else:
            return self.get_domain() != '' and self.get_workgroup() != '' and get_user_ad() != '' and get_passwd_ad() != ''


    def __str__(self):
        return str(self._data)


class ActiveDirectoryConf():

    def __init__(self):
        self._data = {}
        self._data['specific_conf'] = False
        self._ad_properties = ActiveDirectoryProperties()

    def load_data(self, conf):
        msg = 'ServerConf: Key "%s" not found in the configuration file.'
        try:
            self.set_specific_conf(conf['specific_conf'])
        except KeyError as e:
            print msg % ('specific_conf',)
        try:
            self._ad_properties.load_data(conf['ad_properties'], self.get_specific_conf())
        except KeyError as e:
            print msg % ('ad_properties',)

    def validate(self):
        return self._ad_properties.validate(self.get_specific_conf())

    def get_specific_conf(self):
        return self._data['specific_conf']

    def set_specific_conf(self, specific_conf):
        self._data['specific_conf'] = specific_conf
        return self

    def get_ad_properties(self):
        return self._ad_properties
    
    def __str__(self):
        return str(self._data)
