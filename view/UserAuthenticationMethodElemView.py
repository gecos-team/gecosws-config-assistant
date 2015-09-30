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
__copyright__ = "Copyright (C) 2015, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"

from Tkinter import N, S, W, E, Toplevel, END, StringVar
from ttk import Frame, Button, Style, Label, Entry, OptionMenu, LabelFrame
import logging

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

from dto.LocalUsersAuthMethod import LocalUsersAuthMethod
from dto.LDAPAuthMethod import LDAPAuthMethod
from dto.ADAuthMethod import ADAuthMethod
from dto.LDAPSetupData import LDAPSetupData
from dto.ADSetupData import ADSetupData

from view.CommonDialog import showerror

class UserAuthenticationMethodElemView(Toplevel):
    '''
    View class to setup the user authentication method.
    '''


    def __init__(self, parent, mainController):
        '''
        Constructor
        '''
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.body = Frame(self, padding="20 20 20 20")   
        self.controller = mainController
        self.logger = logging.getLogger('UserAuthenticationMethodElemView')
        
        self.data = None
        
        self.initUI()        

    def get_data(self):
        self.logger.debug("get_data() --> %s"%(type(self.__data).__name__))
        return self.__data


    def set_data(self, value):
        self.__data = value
        self.logger.debug("set_data(%s)"%(type(self.__data).__name__))



    def initUI(self):
      
        self.title(_('User authentication method'))
        self.body.style = Style()
        self.body.style.theme_use("default")        
        self.body.pack()
        
        self.body.grid(column=0, row=0, sticky=(N, W, E, S))
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)        
        
        padding_x = 10
        padding_y = 10

        # Explanation
        explanationLabel1 =  Label(self.body, text=_("The users of this workstation may authenticate by using"))
        explanationLabel1.grid(column=0, row=1, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(self.body, text=_("an external system like LDAP or Microsoft Active Directory."))
        explanationLabel2.grid(column=0, row=2, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        explanationLabel2 =  Label(self.body, text=_("Also, they can be authenticated by using local users of this O.S."))
        explanationLabel2.grid(column=0, row=3, columnspan=3, sticky=E+W, padx=padding_x, pady=padding_y)

        # Authentication Type
        authTypeLabel = Label(self.body, text=_("Authentication type:"))
        authTypeLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.authTypeVar = StringVar(self.body)
        self.authTypeVar.set(_('Internal'))
        
        self.authTypeOption = OptionMenu(self.body, self.authTypeVar, _('Internal'), _('Internal'), _('LDAP'), _('Active Directory') )
        self.authTypeOption.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # Options frame
        self.optionsFrame = LabelFrame(self.body)
        self.optionsFrame.grid(column=0, row=5, columnspan=3, sticky="nswe", padx=padding_x, pady=padding_y)
         
        # Setup button
        setupButton = Button(self.body, text=_("Setup"),
            command=self.setup)
        setupButton.grid(column=0, row=7, sticky=E, padx=padding_x, pady=padding_y)

        # Accept button
        acceptButton = Button(self.body, text=_("Accept"),
            command=self.accept)
        acceptButton.grid(column=2, row=7, sticky=E, padx=padding_x, pady=padding_y)
        
        self.logger.debug('UI initiated')
        

    def _show_active_directory_method(self):
        self.logger.debug("_show_active_directory_method")

        # Options frame
        self.optionsFrame['text'] = _('Active Directory authentication')
        
        # Delete previous content
        for widget in self.optionsFrame.winfo_children():
            widget.destroy()
            
        padding_x = 10
        padding_y = 10
                    
        # Explanation
        explanationLabel =  Label(self.optionsFrame, 
            text=_("Please fill the data to setup the Active Directory authentication method."))
        explanationLabel.grid(column=0, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)
        
        # Domain
        adDomainLabel = Label(self.optionsFrame, text=_("Domain:"))
        adDomainLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adDomainEntry = Entry(self.optionsFrame)
        self.adDomainEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # Workgroup
        adWorkgroupLabel = Label(self.optionsFrame, text=_("Workgroup:"))
        adWorkgroupLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adWorkgroupEntry = Entry(self.optionsFrame)
        self.adWorkgroupEntry.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # User
        adUserLabel = Label(self.optionsFrame, text=_("User:"))
        adUserLabel.grid(column=0, row=5, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adUserEntry = Entry(self.optionsFrame)
        self.adUserEntry.grid(column=1, row=5, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.adUserEntry.delete(0, END)

        # Password
        adPasswordLabel = Label(self.optionsFrame, text=_("Password:"))
        adPasswordLabel.grid(column=0, row=6, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.adPasswordEntry = Entry(self.optionsFrame, show="*")
        self.adPasswordEntry.grid(column=1, row=6, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        self.adPasswordEntry.delete(0, END)

        # Fill data values
        if self.get_data() is not None and isinstance(self.get_data(), ADAuthMethod):
            data = self.get_data().get_data()
            if data.get_domain() is not None and data.get_domain().strip()!='':
                self.adDomainEntry.delete(0, END)
                self.adDomainEntry.insert(0, data.get_domain())

            if data.get_workgroup() is not None and data.get_workgroup().strip()!='':
                self.adWorkgroupEntry.delete(0, END)
                self.adWorkgroupEntry.insert(0, data.get_workgroup())

            if data.get_ad_administrator_user() is not None and data.get_ad_administrator_user().strip()!='':
                self.adPasswordEntry.delete(0, END)
                self.adUserEntry.insert(0, data.get_ad_administrator_user())

            if data.get_ad_administrator_pass() is not None and data.get_ad_administrator_pass().strip()!='':
                self.adPasswordEntry.delete(0, END)
                self.adPasswordEntry.insert(0, data.get_ad_administrator_pass())

        
        
    def _show_ldap_method(self):
        self.logger.debug("_show_ldap_method")

        # Options frame
        self.optionsFrame['text'] = _('LDAP authentication')

        # Delete previous content
        for widget in self.optionsFrame.winfo_children():
            widget.destroy()
            
        padding_x = 10
        padding_y = 10
                    
        # Explanation
        explanationLabel =  Label(self.optionsFrame, 
            text=_("Please fill the data to setup the LDAP authentication method."))
        explanationLabel.grid(column=0, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        
        # URI
        ldapUriLabel = Label(self.optionsFrame, text=_("LDAP server URI:"))
        ldapUriLabel.grid(column=0, row=3, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.ldapUriEntry = Entry(self.optionsFrame)
        self.ldapUriEntry.grid(column=1, row=3, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # Users base DN
        ldapBaseLabel = Label(self.optionsFrame, text=_("Users base DN:"))
        ldapBaseLabel.grid(column=0, row=4, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.ldapBaseEntry = Entry(self.optionsFrame)
        self.ldapBaseEntry.grid(column=1, row=4, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # Groups base DN
        ldabBaseGroupLabel = Label(self.optionsFrame, text=_("Groups base DN (optional):"))
        ldabBaseGroupLabel.grid(column=0, row=5, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.ldabBaseGroupEntry = Entry(self.optionsFrame)
        self.ldabBaseGroupEntry.grid(column=1, row=5, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # Bind user DN
        ldabBindUserDNLabel = Label(self.optionsFrame, text=_("Bind user DN (optional):"))
        ldabBindUserDNLabel.grid(column=0, row=6, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.ldabBindUserDNEntry = Entry(self.optionsFrame)
        self.ldabBindUserDNEntry.grid(column=1, row=6, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)


        # Bind user password
        ldabBindUserPwdLabel = Label(self.optionsFrame, text=_("Bind user password (optional):"))
        ldabBindUserPwdLabel.grid(column=0, row=7, sticky=E+W, padx=padding_x, pady=padding_y)
        
        self.ldabBindUserPwdEntry = Entry(self.optionsFrame, show="*")
        self.ldabBindUserPwdEntry.grid(column=1, row=7, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)

        # Fill data values
        if self.get_data() is not None and isinstance(self.get_data(), LDAPAuthMethod):
            data = self.get_data().get_data()
            if data.get_uri() is not None and data.get_uri().strip()!='':
                self.ldapUriEntry.delete(0, END)
                self.ldapUriEntry.insert(0, data.get_uri())

            if data.get_base() is not None and data.get_base().strip()!='':
                self.ldapBaseEntry.delete(0, END)
                self.ldapBaseEntry.insert(0, data.get_base())

            if data.get_base_group() is not None and data.get_base_group().strip()!='':
                self.ldabBaseGroupEntry.delete(0, END)
                self.ldabBaseGroupEntry.insert(0, data.get_base_group())

            if data.get_bind_user_dn() is not None and data.get_bind_user_dn().strip()!='':
                self.ldabBindUserDNEntry.delete(0, END)
                self.ldabBindUserDNEntry.insert(0, data.get_bind_user_dn())

            if data.get_bind_user_pwd() is not None and data.get_bind_user_pwd().strip()!='':
                self.ldabBindUserPwdEntry.delete(0, END)
                self.ldabBindUserPwdEntry.insert(0, data.get_bind_user_pwd())

         

    def _show_local_users_method(self):
        self.logger.debug("_show_local_users_method")
        
        # Options frame
        self.optionsFrame['text'] = _('Local users authentication')

        # Delete previous content
        for widget in self.optionsFrame.winfo_children():
            widget.destroy()
            
        padding_x = 10
        padding_y = 10
                    
        # Explanation
        explanationLabel =  Label(self.optionsFrame, 
            text=_("There is no necessary data to setup the local users authentication method."))
        explanationLabel.grid(column=0, row=1, columnspan=2, sticky=E+W, padx=padding_x, pady=padding_y)



    def _update_options(self, *args):
        self.logger.debug("_update_options")
        self.logger.debug('authTypeVar=%s'%(self.authTypeVar.get()))
        
        if self.authTypeVar.get() == _('LDAP'):
            self._show_ldap_method()
        elif self.authTypeVar.get() == _('Active Directory'):
            self._show_active_directory_method()
        else:
            self._show_local_users_method()

    def show(self):
        self.logger.debug("Show")
        
        data = self.get_data()
        if data is not None:
            self.logger.debug("data is %s"%(type(data).__name__))
            if isinstance(data, ADAuthMethod):
                self._show_active_directory_method()
                self.authTypeVar.set(_('Active Directory'))
            elif isinstance(data, LDAPAuthMethod):
                self._show_ldap_method()
                self.authTypeVar.set(_('LDAP'))                
            else:
                self._show_local_users_method()
                self.authTypeVar.set(_('Internal'))
                
        else:
            # LocalUsersAuthMethod
            self.logger.debug("data is None")            
            self._show_local_users_method()
            self.authTypeVar.set(_('Internal'))
        
        self.authTypeVar.trace('w', self._update_options)
        
        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

    def _populate_data(self):
        self.logger.debug("_populate_data")
        
        if self.authTypeVar.get() == _('LDAP'):
            # Populate data from LDAP data
            self.set_data(LDAPAuthMethod())
            setupData = LDAPSetupData()
            setupData.set_base(self.ldapBaseEntry.get())
            setupData.set_uri(self.ldapUriEntry.get())
            setupData.set_base_group(self.ldabBaseGroupEntry.get())
            setupData.set_bind_user_dn(self.ldabBindUserDNEntry.get())
            setupData.set_bind_user_pwd(self.ldabBindUserPwdEntry.get())
            
            self.get_data().set_data(setupData)
        elif self.authTypeVar.get() == _('Active Directory'):
            # Populate data from AD data
            self.set_data(ADAuthMethod())
            setupData = ADSetupData()
            setupData.set_domain(self.adDomainEntry.get())
            setupData.set_workgroup(self.adWorkgroupEntry.get())
            setupData.set_ad_administrator_user(self.adUserEntry.get())
            setupData.set_ad_administrator_pass(self.adPasswordEntry.get())
            
            self.get_data().set_data(setupData)
            
        else:
            # Internal users
            self.set_data(LocalUsersAuthMethod())

    def accept(self):
        self.logger.debug("Accept")
        self._populate_data()
        self.controller.accept()


    def cancel(self):
        self.logger.debug("cancel")
        self.set_data(None)
        self.destroy()

    def setup(self):
        self.logger.debug("setup")
        self._populate_data()
        
        if self.controller.test():
            if not self.controller.save():
                showerror(_("Error saving authentication method"), 
                    _("An error happened while saving the users authentication method!") + "\n" + _("See log for more details."),
                     self.view)
                 


    def focusLdapUriField(self):
        self.ldapUriEntry.focus()               

    def focusUserBaseDNField(self):
        self.ldapBaseEntry.focus()               

    def focusAdDomainField(self):
        self.adDomainEntry.focus()               

    def focusAdWorkgroupField(self):
        self.adWorkgroupEntry.focus()         

    def focusAdUserField(self):
        self.adUserEntry.focus()         

    def focusAdPasswordField(self):
        self.adPasswordEntry.focus()


                
    data = property(get_data, set_data, None, None)



        
