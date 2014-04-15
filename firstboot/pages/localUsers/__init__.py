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


import pwd
import os, Dialogs
from gi.repository import Gtk
import firstboot.pages
from firstboot_lib import PageWindow
from firstboot import serverconf
import firstboot.validation as validation

import gettext
from gettext import gettext as _
gettext.textdomain('firstboot')

import shlex
import subprocess

__REQUIRED__ = False

__TITLE__ = _('Manage local users')

__DUMMY_PASSWORD__ = '********'

def get_page(main_window):

    page = LocalUsersPage(main_window)
    return page

class LocalUsersPage(PageWindow.PageWindow):
    __gtype_name__ = "LocalUsersPage"

    def load_page(self, params=None):
     
        self.emit('status-changed', 'localUsers', not __REQUIRED__)
        content = serverconf.get_json_content()
        self.serverconf = serverconf.get_server_conf(content)
        self.init_treeview()
        self.reload_page()

        self.ui.lblGroups.set_visible(False)
        self.ui.txtGroups.set_visible(False)

    def reload_page(self):
        self._accept_changes = False
        self._active_user = None
        self.ui.btnApply.set_sensitive(False)
        self.ui.btnCancel.set_sensitive(False)
        self.ui.btnAdd.set_sensitive(True)
        self.ui.btnRemove.set_sensitive(False)
        self._accept_changes = False
        self.ui.txtName.set_text('')
        self.ui.txtName.set_sensitive(False)
        self.ui.txtPassword.set_text('')
        self.ui.txtPassword.set_sensitive(False)
        self.ui.txtConfirm.set_text('')
        self.ui.txtConfirm.set_sensitive(False)
        self.ui.txtGroups.set_text('')
        self.ui.txtGroups.set_sensitive(False)
        self._accept_changes = True
        try:
            self.load_users()
        except Exception as e:
            print e

    def translate(self):
        self.ui.lblDescription.set_text(_('You can create or delete local users on this\
workstation. \n\nUsers authenticated by external services (AD, LDAP...) directory do not need to be created here\
\n\nCheck default OEM users and change its passwords if needed.'))

        self.ui.lblName.set_text(_('Name'))
        self.ui.lblPassword.set_text(_('Password'))
        self.ui.lblConfirm.set_text(_('Confirm'))
        self.ui.lblGroups.set_text(_('Groups'))
        self.ui.btnAdd.set_label(_('Add'))
        self.ui.btnRemove.set_label(_('Remove'))
        self.ui.btnCancel.set_label(_('Cancel'))
        self.ui.btnApply.set_label(_('Apply'))

#    def on_btnLocalUsers_Clicked(self, button):
#        cmd = 'gnome-control-center'
#        param = 'user-accounts'
#        os.spawnlp(os.P_NOWAIT, cmd, cmd, param)

    def previous_page(self, load_page_callback):
        load_page_callback(firstboot.pages.linkToServer)

    def next_page(self, load_page_callback):
        load_page_callback(firstboot.pages.installSoftware)

    def init_treeview(self):

        tvcolumn = Gtk.TreeViewColumn(_('User'))

        cell = Gtk.CellRendererText()
        tvcolumn.pack_start(cell, False)
        tvcolumn.set_cell_data_func(cell, self._render_user_column)

        self.ui.tvUsers.append_column(tvcolumn)
        self.ui.tvUsers.set_enable_search(True)
        self.ui.tvUsers.set_search_column(1)
        self.ui.tvUsers.set_show_expanders(False)

    def _render_user_column(self, column, cell, model, iter, userdata):
        user = model.get_value(iter, 0)
        property = 'text'
        text = user['login']
        cell.set_property(property, text)

    def load_users(self):
        #read users to delete, to avoid to show them in the widget
        userstodelete = []
        for user in self.serverconf.get_users_conf().get_users_list():
            if user.get_actiontorun() == 'delete':
                userstodelete.append(user.get_user())
        
        #load users in the system, excluding those to be deleted
        #and load changes in parameters
        users = self.read_users()
        store = self.ui.tvUsers.get_model()
        store.clear()
        
        for user in users:
            if user['login'] not in userstodelete:
                for user2 in self.serverconf.get_users_conf().get_users_list():
                    if user2.get_user() == user['login']:
                        user['name'] = user2.get_name()
                store.append([user])
        
        #load users to create
        for user in self.serverconf.get_users_conf().get_users_list():
            if user.get_actiontorun() == 'create':
                userdict = {
                    'login': user.get_user(),
                    'uid': '',
                    'gid': '',
                    'name': user.get_name(),
                    'home': '',
                    'shell': '',
                    'groups': '',
                    'is_admin': False,
                    }
                store.append([userdict])
        
        self.ui.tvUsers.set_model(store)

    def _select_user(self):
        self.ui.tvUsers.get_selection().select_path(self._selected_path)
        self.on_tvUsersCursorChanged(self.ui.tvUsers)

    def on_tvUsersCursorChanged(self, widget):
        #if self._active_user and self._active_user['updated'] == True:
        #    return
        store, iter = widget.get_selected()
        user = store.get_value(iter, 0)
        self._selected_path = store.get_path(iter)
        self.set_active_user(user)

    def set_active_user(self, user):
        is_current_user = user['is_admin']
        self._active_user = user
        self._active_user['updated'] = False
        self._accept_changes = False
        self.ui.txtName.set_text(user['name'])
        self.ui.txtName.set_sensitive(True)
        self.ui.txtPassword.set_text(__DUMMY_PASSWORD__)
        self.ui.txtPassword.set_sensitive(True)
        self.ui.txtConfirm.set_text('')
        self.ui.txtConfirm.set_sensitive(True)
        self.ui.txtGroups.set_text(user['groups'])
        self.ui.txtGroups.set_sensitive(True)
        self.ui.btnRemove.set_sensitive(not is_current_user)
        self._accept_changes = True

    def on_userDataChanged(self, widget):
        if self._active_user != None:
            self._active_user['updated'] = self._accept_changes
        self.ui.btnApply.set_sensitive(self._accept_changes)
        self.ui.btnCancel.set_sensitive(self._accept_changes)

    def on_btnApplyClicked(self, widget):

        update_passwd = False

        if self.ui.txtPassword.get_text() != __DUMMY_PASSWORD__:
            update_passwd = True

        user = {
            'login': self._active_user['login'],
            'name': self.ui.txtName.get_text(),
            'password': self.ui.txtPassword.get_text(),
            'confirm': self.ui.txtConfirm.get_text(),
            'groups': self.ui.txtGroups.get_text()
        }
        if not self.validate_user(user):
            return
        
        #modify user
        try:
            changeuser = serverconf.UsersConf.Users()
            changeuser.set_actiontorun('modify')
            changeuser.set_user(user['login'])
            changeuser.set_name(user['name'])
            changeuser.set_password(user['password'])
            changeuser.add_group(user['groups'])
            
            #avoid to add 2 or more modify entries for the same user
            #add only the last one
            #if there is a create operation, rewrite the create with the modified parameters
            userlist = []
            modifiedbefore = False
            for user2 in self.serverconf.get_users_conf().get_users_list():
                if user2.get_user() == changeuser.get_user():
                    if user2.get_actiontorun() == 'create':
                        modifiedbefore = True
                        #rewrite the create operation with the new parameters
                        user2.set_name(changeuser.get_name())
                        user2.set_password(changeuser.get_password())
                        user2.add_groups(changeuser.get_groups())
                        userlist.append(user2)
                    elif user2.get_actiontorun() == 'modify':
                        modifiedbefore = True
                        userlist.append(changeuser) #add the new changes
                    elif user2.get_actiontorun() == 'delete':
                        userlist.append(user2)
                else:
                    userlist.append(user2)
            
            if not modifiedbefore:
                userlist.append(changeuser)
            
            self.serverconf.get_users_conf().clear()
            self.serverconf.get_users_conf().add_users_to_list(userlist)
            self.reload_page()
            self._select_user()

        except LocalUsersException as e:
            Dialogs.user_error_dialog(e.message)

    def on_btnCancelClicked(self, widget):
        self._accept_changes = False
        self.ui.txtName.set_text(self._active_user['name'])
        self.ui.txtPassword.set_text(__DUMMY_PASSWORD__)
        self.ui.txtConfirm.set_text('')
        self.ui.txtGroups.set_text(self._active_user['groups'])
        self._accept_changes = True

    def on_btnAddClicked(self, widget):
        login_info = Dialogs.new_user_dialog()

        if login_info == False:
            # Pressed 'Cancel' or dialog closed
            return

        if not self.validate_user(login_info):
            return
        
        #checking for duplicated users
        usedusers = set()
        for user in self.read_users():
            usedusers.add(user['login'])
        for user in self.serverconf.get_users_conf().get_users_list():
            if user.get_actiontorun() == 'create':
                usedusers.add(user.get_user())
            elif user.get_actiontorun() == 'delete':
                usedusers.remove(user.get_user())
        if login_info['login'] in usedusers:
            Dialogs.user_error_dialog(_('Duplicated user'))
            return
        
        #mark to add
        try:
            newuser = serverconf.UsersConf.Users()
            newuser.set_actiontorun('create')
            newuser.set_user(login_info['login'])
            newuser.set_name(login_info['name'])
            newuser.set_password(login_info['password'])
            newuser.add_group('') #groups not added
            self.serverconf.get_users_conf().add_user_to_list(newuser)
            self.reload_page()
            self._select_user()
            

        except LocalUsersException as e:
            Dialogs.user_error_dialog(e.message)

    def on_btnRemoveClicked(self, widget):
        action = Dialogs.remove_user_dialog(self._active_user)
        if action == False:
            return
        
        #mark user to delete
        try:
            deleteuser = serverconf.UsersConf.Users()
            deleteuser.set_actiontorun('delete')
            deleteuser.set_user(self._active_user['login'])
            deleteuser.set_deletehome(action[1])
            
            #remove any operation on the user we are going to delete
            userlist = []
            createdhere = False
            for user2 in self.serverconf.get_users_conf().get_users_list():
                if user2.get_user() != deleteuser.get_user(): #operation on a different user, ok
                    userlist.append(user2)
                elif user2.get_actiontorun() == 'create': #if user was created in this session, then, do not create+delete
                    createdhere = True
            
            if not createdhere:
                userlist.append(deleteuser)
            
            self.serverconf.get_users_conf().clear()
            self.serverconf.get_users_conf().add_users_to_list(userlist)
            
            self.reload_page()
            self._select_user()

        except LocalUsersException as e:
            Dialogs.user_error_dialog(e.message)

    def validate_user(self, user):

        valid = True
        messages = []

        if not validation.is_qname(user['login']):
            messages.append(_('User login is empty or contains invalid characters.'))
            valid = False

        if validation.is_empty(user['password']):
            messages.append(_('User password can not be empty.'))
            valid = False

        elif user['password'] != __DUMMY_PASSWORD__ and user['password'] != user['confirm']:
            messages.append(_('Passwords do not match.'))
            valid = False

        if not valid:
            msgs = '\n'.join(messages)
            Dialogs.user_error_dialog(msgs)

        return valid

    def read_users(self, min_uid=1000):

        users = []

        f = open('/etc/passwd')
        try:
            for line in f:
                line = line.strip()
                tokens = line.split(':')
                if int(tokens[2]) >= min_uid and tokens[0] != 'nobody':
                    cmd = 'groups %s' % (tokens[0],)
                    pid, exit_code, output = self._run_command(cmd)
                    groups = output.split(':')
                    groups = groups[1].strip()

                    user = {
                        'login': tokens[0],
                        'uid': tokens[2],
                        'gid': tokens[3],
                        'name': tokens[4].split(',')[0],
                        'home': tokens[5],
                        'shell': tokens[6],
                        'groups': groups,
                        'is_admin': ('sudo' in groups.split(' '))
                    }
                    users.append(user)

        finally:
            f.close()
        
        return users


    def _run_command(self, cmd):
        args = shlex.split(cmd)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]
        output = output.strip()

        #print cmd, exit_code
        #if exit_code[1] != 0:
        #    raise Exception(output)

        # PID, exit code, output
        return (exit_code[0], exit_code[1], output)


class LocalUsersException(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
