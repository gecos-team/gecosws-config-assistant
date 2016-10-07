#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from __builtin__ import True

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

__author__ = "Francisco Fuentes Barrera <ffuentes@solutia-it.es>"
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from GladeWindow import GladeWindow
from gi.repository import Gtk, Gdk
import logging
import gettext
from gettext import gettext as _

from gecosws_config_assistant.dto.LocalUsersAuthMethod import LocalUsersAuthMethod
from gecosws_config_assistant.dto.LDAPAuthMethod import LDAPAuthMethod
from gecosws_config_assistant.dto.ADAuthMethod import ADAuthMethod
from gecosws_config_assistant.dto.LDAPSetupData import LDAPSetupData
from gecosws_config_assistant.dto.ADSetupData import ADSetupData

from gecosws_config_assistant.view.CommonDialog import showerror_gtk

"""
UserAuthenticationMethodElemView redone in Glade
"""
LOCAL_USERS = 0
LDAP_USERS  = 1
AD_USERS    = 2

class UserAuthDialog(GladeWindow):
    def __init__(self, mainController):
        self.mainController = mainController
        self.controller = mainController.userAuthenticationMethod
        self.gladePath = 'users.glade'
        self.logger = logging.getLogger('UserAuthDialog')
        
        self.buildUI(self.gladePath)
        
        self.data = None
        
        #combo stuff
        self.lastComboValue = ''
        self.store = self.getElementById('liststore1')
        self.combo = self.getElementById('combobox1')
        
        renderer_text = Gtk.CellRendererText()
        self.combo.pack_start(renderer_text, True)
        self.combo.add_attribute(renderer_text, "text", 0)
        
        self.loadOUCombo([_('Internal'), _('LDAP'), _('Active Directory')])
        
        self.logger.debug(self.get_data())
        
        self.extractGUIElements()
        
    def get_data(self):
        self.logger.debug("get_data() --> %s"%(type(self.data).__name__))
        return self.data


    def set_data(self, value):
        self.data = value
        self.logger.debug("set_data(%s)"%(type(self.data).__name__))
        
    def extractGUIElements(self):
        self.biglabel = self.getElementById("label2")
        
        # labels
        self.label1 = self.getElementById("label3")
        self.label2 = self.getElementById("label4")
        self.label3 = self.getElementById("label5")
        self.label4 = self.getElementById("label6")
        self.label5 = self.getElementById("label7")
        
        # entries
        self.entry1 = self.getElementById("entry1")
        self.entry2 = self.getElementById("entry2")
        self.entry3 = self.getElementById("entry3")
        self.entry4 = self.getElementById("entry4")
        self.entry5 = self.getElementById("entry5")
        
        # buttons and combo
        self.authTypeOption = self.getElementById("combobox1")
        self.setupButton = self.getElementById("button1")
        self.acceptButton = self.getElementById("button2")
    
    def addHandlers(self):
        super(UserAuthDialog, self).addHandlers()
        self.logger.info('Calling child specific handler')
        self.logger.debug("Adding on change combobox handler")
        self.handlers["onChng"] = self.onChangeComboBox
        self.logger.debug("Adding on config handler")
        self.handlers["onCnfg"] = self.setup
        self.logger.debug("Adding on accept handler")
        self.handlers["onAcpt"] = self.accept
    
    def initGUIValues(self, calculatedStatus):
        pass
        
    def loadCurrentState(self, guiValues):
        pass
    
    def loadOUCombo(self, values):
        if isinstance(values, (list, tuple)):
            for value in values:
                self.store.append([value])
    
    '''
    0: Local users
    1: LDAP
    2: Active Directory
    '''
    def selectComboValue(self, index):
        self.logger.debug("Setting combo to index "+str(index))
        self.combo.set_active(index)
        if(index == LOCAL_USERS):
            self._show_local_users_method()
        elif(index == LDAP_USERS):
            self._show_ldap_method()
        elif(index == AD_USERS):
            self._show_active_directory_method()
    
    def updateCombo(self):
        self.logger.debug("Updating combo")
        name = self.get_data().get_name()
        
        value = -1
        
        if(name == _('Internal')):
            value = LOCAL_USERS
        elif(name == _('LDAP')):
            value = LDAP_USERS
        elif(name == _('Active Directory')):
            value = AD_USERS
        
        if(value != -1):
            self.selectComboValue(value)
    
    def preShow(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            self.logger.debug("data is %s"%(type(data).__name__))
            if isinstance(data, ADAuthMethod):
                self._show_active_directory_method()
                self.selectComboValue(AD_USERS)
            elif isinstance(data, LDAPAuthMethod):
                self._show_ldap_method()
                self.selectComboValue(LDAP_USERS)          
            else:
                self._show_local_users_method()
                self.selectComboValue(LOCAL_USERS)
                
        else:
            # LocalUsersAuthMethod
            self.logger.debug("data is None")
            self._show_local_users_method()
            self.selectComboValue(LOCAL_USERS)
        
        self.authTypeVar.trace('w', self._update_options)
    
    def onChangeComboBox(self, combo):
        self.logger.debug("This should show up each time the combobox is changed")
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            value = model[tree_iter][0]
            self.lastComboValue = value
            index = -1
            if(value == _('Internal')):
                index = LOCAL_USERS
            elif(value == _('LDAP')):
                index = LDAP_USERS
            elif(value == _('Active Directory')):
                index = AD_USERS
            if index != -1: self.selectComboValue(index)
    
    def ldapWidgetAlias(self):
        self.ldapBaseEntry = self.entry2
        self.ldapUriEntry = self.entry1
        self.ldabBaseGroupEntry = self.entry3
        self.ldabBindUserDNEntry = self.entry4
        self.ldabBindUserPwdEntry = self.entry5
    
    def adWidgetAlias(self):
        self.adDomainEntry = self.entry1
        self.adWorkgroupEntry = self.entry2
        self.adUserEntry = self.entry3
        self.adPasswordEntry = self.entry4
    
    def setFormForLDAP(self):
        self.logger.debug("Setting form for LDAP")
        
        self.biglabel.set_text(_("Please fill the data to setup the LDAP authentication method."))
        
        # text
        self.label1.set_text(_("LDAP server URI:"))
        self.label2.set_text(_("Users base DN:"))
        self.label3.set_text(_("Groups base DN (optional):"))
        self.label4.set_text(_("Bind user DN (optional):"))
        self.label5.set_text(_("Bind user password (optional):"))
        
        # visibility
        self.label1.set_visible(True)
        self.label2.set_visible(True)
        self.label3.set_visible(True)
        self.label4.set_visible(True)
        self.label5.set_visible(True)
        
        self.entry1.set_visible(True)
        self.entry2.set_visible(True)
        self.entry3.set_visible(True)
        self.entry4.set_visible(True)
        self.entry5.set_visible(True)
        
        # visibility
        self.entry1.set_visibility(True)
        self.entry2.set_visibility(True)
        self.entry3.set_visibility(True)
        self.entry4.set_visibility(True)
        self.entry5.set_visibility(False)
    
    def setFormForAD(self):
        self.logger.debug("Setting form for Active Directory")
        
        self.biglabel.set_text(_("Please fill the data to setup the Active Directory authentication method."))
        
        # text
        self.label1.set_text(_("Domain:"))
        self.label2.set_text(_("Workgroup:"))
        self.label3.set_text(_("(Active Directory) User:"))
        self.label4.set_text(_("(Active Directory) Password:"))
        
        # show or hide
        self.label1.set_visible(True)
        self.label2.set_visible(True)
        self.label3.set_visible(True)
        self.label4.set_visible(True)
        self.label5.set_visible(False)
        
        self.entry1.set_visible(True)
        self.entry2.set_visible(True)
        self.entry3.set_visible(True)
        self.entry4.set_visible(True)
        self.entry5.set_visible(False)
        
        # visibility
        self.entry1.set_visibility(True)
        self.entry2.set_visibility(True)
        self.entry3.set_visibility(True)
        self.entry4.set_visibility(False)
        self.entry5.set_visibility(True)

    def setFormForSpecificAD(self):
        self.logger.debug("Setting form for specific Active Directory setup")
        
        self.biglabel.set_text(_("Specific configuration data was loaded from GECOS server\n (sssd.conf, krb5.conf, smb.conf and pam.conf)"))
        
        
        # text
        self.label1.set_text(_("Domain:"))
        self.label2.set_text(_("Workgroup:"))
        self.label3.set_text(_("User:"))
        self.label4.set_text(_("Password:"))
        
        # show or hide
        self.label1.set_visible(False)
        self.label2.set_visible(False)
        self.label3.set_visible(True)
        self.label4.set_visible(True)
        self.label5.set_visible(False)
        
        self.entry1.set_visible(False)
        self.entry2.set_visible(False)
        self.entry3.set_visible(True)
        self.entry4.set_visible(True)
        self.entry5.set_visible(False)
        
        # visibility
        self.entry1.set_visibility(True)
        self.entry2.set_visibility(True)
        self.entry3.set_visibility(True)
        self.entry4.set_visibility(False)
        self.entry5.set_visibility(True)

    
    def setFormForInternal(self):
        self.logger.debug("Setting form for Internal")
        
        self.biglabel.set_text(_("There is no necessary data to setup the local users authentication method."))
        
        # visibility
        self.label1.set_visible(False)
        self.label2.set_visible(False)
        self.label3.set_visible(False)
        self.label4.set_visible(False)
        self.label5.set_visible(False)
        
        self.entry1.set_visible(False)
        self.entry2.set_visible(False)
        self.entry3.set_visible(False)
        self.entry4.set_visible(False)
        self.entry5.set_visible(False)
        
        # visibility
        self.entry1.set_visibility(True)
        self.entry2.set_visibility(True)
        self.entry3.set_visibility(True)
        self.entry4.set_visibility(True)
        self.entry5.set_visibility(True)
    
    def _show_active_directory_method(self):
        self.logger.debug("_show_active_directory_method")
        self.setFormForAD()

        # Fill data values
        if self.get_data() is not None and isinstance(self.get_data(), ADAuthMethod):
            data = self.get_data().get_data()
            
            if data.get_specific():
                # Specific setup
                self.setFormForSpecificAD()
                self.entry1.set_text('SPECIFIC')
                self.entry2.set_text('SPECIFIC')
                
            else:
                # Normal setup
                if data.get_domain() is not None and data.get_domain().strip()!='':
                    self.entry1.set_text(data.get_domain())
     
                if data.get_workgroup() is not None and data.get_workgroup().strip()!='':
                    self.entry2.set_text(data.get_workgroup())
     
                if data.get_ad_administrator_user() is not None and data.get_ad_administrator_user().strip()!='':
                    self.entry3.set_text(data.get_ad_administrator_user())
     
                if data.get_ad_administrator_pass() is not None and data.get_ad_administrator_pass().strip()!='':
                    self.entry4.set_text(data.get_ad_administrator_pass())
                    self.entry4.set_visibility(False)
                
    def _show_ldap_method(self):
        self.logger.debug("_show_ldap_method")
        self.setFormForLDAP()
 
        # Fill data values
        if self.get_data() is not None and isinstance(self.get_data(), LDAPAuthMethod):
            data = self.get_data().get_data()
            if data.get_uri() is not None and data.get_uri().strip()!='':
                self.entry1.set_text(data.get_uri())
 
            if data.get_base() is not None and data.get_base().strip()!='':
                self.entry2.set_text(data.get_base())
 
            if data.get_base_group() is not None and data.get_base_group().strip()!='':
                self.entry3.set_text(data.get_base_group())
 
            if data.get_bind_user_dn() is not None and data.get_bind_user_dn().strip()!='':
                self.entry4.set_text(data.get_bind_user_dn())
 
            if data.get_bind_user_pwd() is not None and data.get_bind_user_pwd().strip()!='':
                self.entry5.set_text(data.get_bind_user_pwd())
    
    def _show_local_users_method(self):
        self.logger.debug("_show_local_users_method")
        self.setFormForInternal()
    
    def focusLdapUriField(self):
        self.entry1.grab_focus()               

    def focusUserBaseDNField(self):
        self.entry2.grab_focus()

    def focusAdDomainField(self):
        self.entry1.grab_focus()                

    def focusAdWorkgroupField(self):
        self.entry2.grab_focus()         

    def focusAdUserField(self):
        self.entry3.grab_focus()  

    def focusAdPasswordField(self):
        self.entry4.grab_focus()
    
    def setup(self, *args):
        self.logger.debug("setup")
        self._populate_data()
        
        if self.controller.test():
            if not self.controller.save():
                showerror_gtk(_("An error happened while saving the users authentication method!") + "\n" + _("See log for more details."),
                     None)
    
    def accept(self, *args):
        self.logger.debug("Accept")
        self._populate_data()
        self.controller.accept()

    def cancel(self):
        self.logger.debug("cancel")
        self.set_data(None)
        self.mainController.backToMainWindowDialog()
            
    def _populate_data(self):
        index = self.combo.get_active()

        self.logger.debug("_populate_data: %s"%(index))        
        
        if index == LDAP_USERS:
            # Populate data from LDAP data
            self.ldapWidgetAlias()
            self.set_data(LDAPAuthMethod())
            setupData = LDAPSetupData()
            setupData.set_base(self.ldapBaseEntry.get_text())
            setupData.set_uri(self.ldapUriEntry.get_text())
            setupData.set_base_group(self.ldabBaseGroupEntry.get_text())
            setupData.set_bind_user_dn(self.ldabBindUserDNEntry.get_text())
            setupData.set_bind_user_pwd(self.ldabBindUserPwdEntry.get_text())
            
            self.get_data().set_data(setupData)
        elif index == AD_USERS:
            # Populate data from AD data
            self.adWidgetAlias()
            if (self.get_data() is not None 
                and isinstance(self.get_data(), ADAuthMethod) 
                and self.get_data().get_data().get_specific()):
                # Specific AD setup
                setupData = self.get_data().get_data()
            else:
                # Normal AD Setup
                self.set_data(ADAuthMethod())
                setupData = ADSetupData()
                
            setupData.set_domain(self.adDomainEntry.get_text())
            setupData.set_workgroup(self.adWorkgroupEntry.get_text())
            setupData.set_ad_administrator_user(self.adUserEntry.get_text())
            setupData.set_ad_administrator_pass(self.adPasswordEntry.get_text())
            
            self.get_data().set_data(setupData)
            
        else:
            # Internal users
            self.set_data(LocalUsersAuthMethod())