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


import LinkToServerResultsPage
import firstboot.pages.linkToServer
from firstboot_lib import PageWindow
from firstboot import serverconf
import os
import gettext
from gettext import gettext as _
gettext.textdomain('firstboot')

__REQUIRED__ = False


def get_page(main_window):

    page = LinkToServerConfEditorPage(main_window)
    return page


class LinkToServerConfEditorPage(PageWindow.PageWindow):
    __gtype_name__ = "LinkToServerConfEditorPage"

    def finish_initializing(self):

        self.update_server_conf = False
        self.link_ldap = False
        self.link_ad = False

    def load_page(self, params=None):
        self.server_conf = serverconf.get_server_conf(None)
        self.ui.lblVersionValue.set_label(self.server_conf.get_version())
        self.ui.lblOrganizationValue.set_label(self.server_conf.get_organization())
#           self.ui.lblNotesValue.set_label(self.server_conf.get_notes())
        self.method = params['auth_method']
        if self.method == 'ldap':
            self.ui.checkSpecific.hide()
            if self.server_conf.get_auth_conf().get_auth_type() == 'ldap':
                ldap_conf = self.server_conf.get_auth_conf().get_auth_properties()
                self.ui.txtUrlLDAP.set_text(ldap_conf.get_url())
                self.ui.txtBaseDN.set_text(ldap_conf.get_basedn())
                self.ui.txtBaseDNGroup.set_text(ldap_conf.get_basedngroup())
                self.ui.txtBindDN.set_text(ldap_conf.get_binddn())
                self.ui.txtPassword.set_text(ldap_conf.get_password())
            self.ui.adBox.set_visible(False)
            self.ui.ldapBox.set_visible(True)
            self.link_ldap = True
        else:
            #os.system('DEBCONF_PRIORITY=critical DEBIAN_FRONTEND=noninteractive dpkg-reconfigure resolvconf')
            self.ui.ldapBox.set_visible(False)
            self.ui.adBox.set_visible(True)
            self.link_ad = True
            if self.server_conf.get_auth_conf().get_auth_type() == 'ad':
                if self.server_conf.get_auth_conf().get_auth_properties().get_specific_conf():
                    self.ui.checkSpecific.set_active(True)
                    self.ui.txtWorkgroup.set_editable(False)
                    self.ui.txtFqdnAD.set_editable(False)
                else:
                    ad_conf = self.server_conf.get_auth_conf().get_auth_properites().get_ad_properties()
                    self.ui.txtFqdnAD.set_text(ad_conf.get_fqdn())
                    self.ui.checkSpecific.hide()
                    self.ui.txtWorkgroup.set_text(ad_conf.get_workgroup())
            else:
                self.ui.checkSpecific.hide()


            

        self.update_server_conf = True


        if params['ldap_is_configured'] or params['ad_is_configured']:
            self.ui.lblDescription.set_visible(False)

    def _bold(self, str):
        return '<b>%s</b>' % str

    def translate(self):
        desc = _('These parameters are required in order to join an authentication server:')

        self.ui.lblDescription.set_text(desc)

        self.ui.lblVersion.set_label(_('Version'))
        self.ui.lblOrganization.set_label(_('Organization'))
        self.ui.lblNotes.set_label(_('Notes'))
        self.ui.lblUrlLDAP.set_label('URL')
        self.ui.lblBaseDN.set_label(_('Base DN for users'))
        self.ui.lblBaseDNGroup.set_label(_('Base DN for groups'))
        self.ui.lblBindDN.set_label('Bind DN')
        self.ui.lblPassword.set_label(_('Password'))
        self.ui.lblFqdnAD.set_label('FQDN')
        self.ui.lblWorkgroup.set_label(_('Workgroup'))
        self.ui.checkSpecific.set_label(_('Change specific configuration from server?'))

    def on_checkSpecific_toggled(self, widget):
        if not self.ui.checkSpecific.get_active():
            self.ui.txtFqdnAD.set_editable(False)
            self.ui.txtWorkgroup.set_editable(False)
        else:
            self.ui.txtFqdnAD.set_editable(True)
            self.ui.txtWorkgroup.set_editable(True)


    def previous_page(self, load_page_callback):
        load_page_callback(firstboot.pages.linkToServer)

    def next_page(self, load_page_callback):
        auth_conf = self.server_conf.get_auth_conf()
        auth_conf.set_auth_type(self.method)
        auth_conf.set_auth_link(True)
        messages = []
        result = True
        if self.method == 'ad':
            retval = serverconf.auth_dialog(_('Authentication Required'),
                _('Please, provide administration credentials for the Active Directory.'))
            
            if self.server_conf.get_auth_conf().get_auth_type() == 'ldap':
                self.server_conf.get_auth_conf().set_auth_type('ad')
            ad_conf = self.server_conf.get_auth_conf().get_auth_properties()
            ad_conf.get_ad_properties().set_user_ad(retval[0])
            ad_conf.get_ad_properties().set_passwd_ad(retval[1])
            ad_conf.set_specific_conf(False)
            ad_conf.get_ad_properties().set_fqdn(self.ui.txtFqdnAD.get_text())
            ad_conf.get_ad_properties().set_workgroup(self.ui.txtWorkgroup.get_text())
            if not auth_conf.get_auth_properties().validate():
                messages.append({'type': 'error', 'message': 'Please, check the Active Directory parameters.'})
                result = False
            
        else:
            if self.server_conf.get_auth_conf().get_auth_type() == 'ad':
                self.server_conf.get_auth_conf().set_auth_typei('ldap')

            ldap_conf = self.server_conf.get_auth_conf().get_auth_properties()
            ldap_conf.set_url(self.ui.txtUrlLDAP.get_text())
            ldap_conf.set_basedn(self.ui.txtBaseDN.get_text())
            ldap_conf.set_basedngroup(self.ui.txtBaseDNGroup.get_text())
            ldap_conf.set_binddn(self.ui.txtBindDN.get_text())
            ldap_conf.set_password(self.ui.txtPassword.get_text())

            if not ldap_conf.validate():
                messages.append({'type': 'error', 'message': 'Please, check the LDAP parameters.'})
                result = False

        load_page_callback(LinkToServerResultsPage, {
            'result': result,
            'messages': messages
         })

    def on_serverConf_changed(self, entry):
        pass
