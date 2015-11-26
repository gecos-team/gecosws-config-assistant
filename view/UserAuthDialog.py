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
"""
UserAuthenticationMethodElemView redone in Glade
"""
LOCAL_USERS = _('Internal')
LDAP_USERS  = _('LDAP')
AD_USERS    = _('Active Directory')

class UserAuthDialog(GladeWindow):
    def __init__(self, mainController):
        self.controller = mainController
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
        
        self.extractGUIElements()
        self.selectComboValue(LOCAL_USERS)
        
    def get_data(self):
        self.logger.debug("get_data() --> %s"%(type(self.__data).__name__))
        return self.__data


    def set_data(self, value):
        self.__data = value
        self.logger.debug("set_data(%s)"%(type(self.__data).__name__))
        
    def extractGUIElements(self):
        self.authTypeOption = self.getElementById("combobox1")
        self.setupButton = self.getElementById("button1")
        self.acceptButton = self.getElementById("button2")
        # self.optionsFrame
    
    def addHandlers(self):
        super(UserAuthDialog, self).addHandlers()
        self.logger.info('Calling child specific handler')
    
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
        self.combo.set_active_id(index)
    
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
                
    def _show_active_directory_method(self):
        self.logger.debug("_show_active_directory_method")

#         # Options frame
#         self.optionsFrame['text'] = _('Active Directory authentication')
#         
#         # Delete previous content
#         for widget in self.optionsFrame.winfo_children():
#             widget.destroy()
#             
#         padding_x = 10
#         padding_y = 10
#                     
#         # Explanation
#         explanationLabel =  Label(self.optionsFrame, 
#             text=_("Please fill the data to setup the Active Directory authentication method."))
#         explanationLabel.grid(column=0, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         # Domain
#         adDomainLabel = Label(self.optionsFrame, text=_("Domain:"))
#         adDomainLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.adDomainEntry = Entry(self.optionsFrame)
#         self.adDomainEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         # Workgroup
#         adWorkgroupLabel = Label(self.optionsFrame, text=_("Workgroup:"))
#         adWorkgroupLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.adWorkgroupEntry = Entry(self.optionsFrame)
#         self.adWorkgroupEntry.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         # User
#         adUserLabel = Label(self.optionsFrame, text=_("User:"))
#         adUserLabel.grid(column=0, row=5, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.adUserEntry = Entry(self.optionsFrame)
#         self.adUserEntry.grid(column=1, row=5, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         self.adUserEntry.delete(0, END)
# 
#         # Password
#         adPasswordLabel = Label(self.optionsFrame, text=_("Password:"))
#         adPasswordLabel.grid(column=0, row=6, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.adPasswordEntry = Entry(self.optionsFrame, show="*")
#         self.adPasswordEntry.grid(column=1, row=6, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         self.adPasswordEntry.delete(0, END)
# 
#         # Fill data values
#         if self.get_data() is not None and isinstance(self.get_data(), ADAuthMethod):
#             data = self.get_data().get_data()
#             if data.get_domain() is not None and data.get_domain().strip()!='':
#                 self.adDomainEntry.delete(0, END)
#                 self.adDomainEntry.insert(0, data.get_domain())
# 
#             if data.get_workgroup() is not None and data.get_workgroup().strip()!='':
#                 self.adWorkgroupEntry.delete(0, END)
#                 self.adWorkgroupEntry.insert(0, data.get_workgroup())
# 
#             if data.get_ad_administrator_user() is not None and data.get_ad_administrator_user().strip()!='':
#                 self.adPasswordEntry.delete(0, END)
#                 self.adUserEntry.insert(0, data.get_ad_administrator_user())
# 
#             if data.get_ad_administrator_pass() is not None and data.get_ad_administrator_pass().strip()!='':
#                 self.adPasswordEntry.delete(0, END)
#                 self.adPasswordEntry.insert(0, data.get_ad_administrator_pass())
    def _show_ldap_method(self):
        self.logger.debug("_show_ldap_method")

#         # Options frame
#         self.optionsFrame['text'] = _('LDAP authentication')
# 
#         # Delete previous content
#         for widget in self.optionsFrame.winfo_children():
#             widget.destroy()
#             
#         padding_x = 10
#         padding_y = 10
#                     
#         # Explanation
#         explanationLabel =  Label(self.optionsFrame, 
#             text=_("Please fill the data to setup the LDAP authentication method."))
#         explanationLabel.grid(column=0, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         
#         # URI
#         ldapUriLabel = Label(self.optionsFrame, text=_("LDAP server URI:"))
#         ldapUriLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.ldapUriEntry = Entry(self.optionsFrame)
#         self.ldapUriEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         # Users base DN
#         ldapBaseLabel = Label(self.optionsFrame, text=_("Users base DN:"))
#         ldapBaseLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.ldapBaseEntry = Entry(self.optionsFrame)
#         self.ldapBaseEntry.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         # Groups base DN
#         ldabBaseGroupLabel = Label(self.optionsFrame, text=_("Groups base DN (optional):"))
#         ldabBaseGroupLabel.grid(column=0, row=5, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.ldabBaseGroupEntry = Entry(self.optionsFrame)
#         self.ldabBaseGroupEntry.grid(column=1, row=5, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         # Bind user DN
#         ldabBindUserDNLabel = Label(self.optionsFrame, text=_("Bind user DN (optional):"))
#         ldabBindUserDNLabel.grid(column=0, row=6, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.ldabBindUserDNEntry = Entry(self.optionsFrame)
#         self.ldabBindUserDNEntry.grid(column=1, row=6, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
# 
#         # Bind user password
#         ldabBindUserPwdLabel = Label(self.optionsFrame, text=_("Bind user password (optional):"))
#         ldabBindUserPwdLabel.grid(column=0, row=7, sticky=E+W, padx=padding_x, pady=padding_y)
#         
#         self.ldabBindUserPwdEntry = Entry(self.optionsFrame, show="*")
#         self.ldabBindUserPwdEntry.grid(column=1, row=7, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
# 
#         # Fill data values
#         if self.get_data() is not None and isinstance(self.get_data(), LDAPAuthMethod):
#             data = self.get_data().get_data()
#             if data.get_uri() is not None and data.get_uri().strip()!='':
#                 self.ldapUriEntry.delete(0, END)
#                 self.ldapUriEntry.insert(0, data.get_uri())
# 
#             if data.get_base() is not None and data.get_base().strip()!='':
#                 self.ldapBaseEntry.delete(0, END)
#                 self.ldapBaseEntry.insert(0, data.get_base())
# 
#             if data.get_base_group() is not None and data.get_base_group().strip()!='':
#                 self.ldabBaseGroupEntry.delete(0, END)
#                 self.ldabBaseGroupEntry.insert(0, data.get_base_group())
# 
#             if data.get_bind_user_dn() is not None and data.get_bind_user_dn().strip()!='':
#                 self.ldabBindUserDNEntry.delete(0, END)
#                 self.ldabBindUserDNEntry.insert(0, data.get_bind_user_dn())
# 
#             if data.get_bind_user_pwd() is not None and data.get_bind_user_pwd().strip()!='':
#                 self.ldabBindUserPwdEntry.delete(0, END)
#                 self.ldabBindUserPwdEntry.insert(0, data.get_bind_user_pwd())
    def _show_local_users_method(self):
        self.logger.debug("_show_local_users_method")
#         
#         # Options frame
#         self.optionsFrame['text'] = _('Local users authentication')
# 
#         # Delete previous content
#         for widget in self.optionsFrame.winfo_children():
#             widget.destroy()
#             
#         padding_x = 10
#         padding_y = 10
#                     
#         # Explanation
#         explanationLabel =  Label(self.optionsFrame, 
#             text=_("There is no necessary data to setup the local users authentication method."))
#         explanationLabel.grid(column=0, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
    
    def focusLdapUriField(self):
        pass               

    def focusUserBaseDNField(self):
        pass               

    def focusAdDomainField(self):
        pass               

    def focusAdWorkgroupField(self):
        pass         

    def focusAdUserField(self):
        pass 

    def focusAdPasswordField(self):
        pass