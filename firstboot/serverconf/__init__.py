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


import json
import requests
import os
import subprocess
import shlex
import shutil
import tempfile
import urllib
import urllib2
import urlparse


from gi.repository import Gtk
from firstboot_lib import firstbootconfig
from ServerConf import ServerConf
from gi.repository import Gtk
import gettext
from firstboot_lib.firstbootconfig import get_prefix
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')


__URLOPEN_TIMEOUT__ = 15
__JSON_CACHE__ = '/tmp/json_cached'
__BIN_PATH__ = firstbootconfig.get_bin_path()
__LDAP_CONF_SCRIPT__ = 'firstboot-ldapconf.sh'
__CHEF_CONF_SCRIPT__ = 'firstboot-chefconf.sh'
__GCC_FLAG__ = '/etc/gcc.control'
__LDAP_FLAG__ = '/etc/ldap.control'
__AD_FLAG__ = '/etc/ad.control'
__CHEF_PEM__ = '/etc/chef/validation.pem'
__AD_CONF_SCRIPT__ = 'firstboot-adconf.sh'

CREDENTIAL_CACHED = {}
ACTUAL_USER = ()


def validate_credentials(url):
    global CREDENTIAL_CACHED
    global ACTUAL_USER
    url_parsed = urlparse.urlparse(url)
    user = ''
    password = ''
    hostname = url_parsed.hostname
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    validate = False
    if hostname in CREDENTIAL_CACHED:
        credentials = CREDENTIAL_CACHED[hostname]
        for cred in credentials:
            user, password = cred[0], cred[1]
            r = requests.get(url, auth=(user,password), headers=headers)
            if r.ok:
                validate = True

    if not validate:

        user, password = auth_dialog(_('Authentication Required'),
            _('You need to enter your credentials to access the requested resource.'))
        r = requests.get(url, auth=(user,password), headers=headers)
        if r.ok:
            if not CREDENTIAL_CACHED.has_key(hostname):
                CREDENTIAL_CACHED[hostname] = []
            credentials = CREDENTIAL_CACHED[hostname]
            credentials.append([user, password])
            ACTUAL_USER = (user, password)
        else:
            raise ServerConfException(_('Authentication is failed.'))
    if hasattr(r,'text'):
        return r.text
    else:  
        return r.content

def json_is_cached():
    return os.path.exists(__JSON_CACHE__)

def clean_json_cached():
    return os.remove(__JSON_CACHE__)

def get_json_content():
    if json_is_cached():
        fp = open(__JSON_CACHE__, 'r')
        content = fp.read()
        fp.close()
        conf = json.loads(content)
        return conf
    else:
        return None

def get_json_autoconf(url):
    try:
        content = validate_credentials(url)
    except Exception as e:
        raise e
    if json_is_cached():
        clean_json_cached()
    fp_cached = open(__JSON_CACHE__, 'w')
    fp_cached.write(content)
    fp_cached.close()
    
    conf = json.loads(content)
    return conf

def get_server_conf(content):
    server_conf = ServerConf.Instance()
    if content != None:
        server_conf.load_data(content)
    return server_conf



def create_chef_pem(chef_conf):
    content = chef_conf.get_pem()
    if not os.path.exists('/etc/chef/'):
        os.makedirs('/etc/chef/')
    fp = open(__CHEF_PEM__, "w+b")
    if fp:
        fp.write(content.decode('base64'))
        fp.close()

    return __CHEF_PEM__


def create_conf_file(file_content):
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(file_content.decode('base64'))
        fp.close()

    return filepath

# def get_chef_hostnames(chef_conf):

#     chef_url = chef_conf.get_url()
#     pem_file_path = create_chef_pem(chef_conf)

#     cmd = 'knife node list -u chef-validator -k %s -s %s' % (pem_file_path, chef_url)
#     args = shlex.split(cmd)

#     process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     exit_code = os.waitpid(process.pid, 0)
#     output = process.communicate()[0]
#     output = output.strip()

#     names = []
#     if exit_code[1] != 0:
#         raise ServerConfException(_('Couldn\'t retrieve the host names list') + ': ' + output)

#     else:
#         try:
#             names = json.loads(output)
#         except ValueError as e:
#             names = output.split('\n')

#     hostnames = []
#     for name in names:
#         name = name.strip()
#         if name.startswith('WARNING') or name.startswith('ERROR'):
#             continue
#         hostnames.append(name)

#     os.remove(pem_file_path)
#     return hostnames


def ad_is_configured():

    try:
        if not os.path.exists(__AD_FLAG__):
            return False
        return True
    except Exception as e:
        raise e


def create_solo_json(server_conf):
    json_solo = {}
    json_solo['run_list'] = ["recipe[ohai-gecos::default]", "recipe[chef-client::upstart_service]", "recipe[gecos_ws_mgmt::local]"]
    json_solo['gecos_ws_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['misc_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['network_mgmt'] = {}
    if server_conf.get_ntp_conf().get_uri_ntp() != '':
        json_solo['gecos_ws_mgmt']['misc_mgmt']['tz_date_res'] = {'server':server_conf.get_ntp_conf().get_uri_ntp()}
    if server_conf.get_chef_conf().get_url() != '':
        tmpfile = create_chef_pem(server_conf.get_chef_conf())
        chef_url = server_conf.get_chef_conf().get_url()
        chef_node_name = server_conf.get_chef_conf().get_node_name()
        chef_admin_name = server_conf.get_chef_conf().get_admin_name()
        if chef_admin_name == "":
            chef_admin_name = server_conf.get_gcc_conf().get_gcc_username()
        chef_link = server_conf.get_chef_conf().get_chef_link()
        chef_link_existing = server_conf.get_chef_conf().get_chef_link_existing()
        chef_json = {'chef_server_url':chef_url, 'chef_node_name': chef_node_name, 'chef_validation_pem': tmpfile, 'chef_link': chef_link, 'chef_admin_name': chef_admin_name, 'chef_link_existing': chef_link_existing}
        json_solo['gecos_ws_mgmt']['misc_mgmt']['chef_conf_res'] = chef_json
    if server_conf.get_auth_conf().get_auth_type() != '':
        auth_type = server_conf.get_auth_conf().get_auth_type()
        if auth_type == 'ad':
            auth_prop = server_conf.get_auth_conf().get_auth_properties()
            sssd_ad_json  = {}
            if auth_prop.get_specific_conf():
                ad_prop = auth_prop.get_ad_properties()
                krb5_file = create_conf_file(ad_prop.get_krb5_conf())
                krb5_file = 'file://' + krb5_file
                smb_file = create_conf_file(ad_prop.get_smb_conf())
                smb_file = 'file://' + smb_file
                sssd_file = create_conf_file(ad_prop.get_sssd_conf())
                sssd_file = 'file://' + sssd_file
                pam_file = create_conf_file(ad_prop.get_pam_conf())
                pam_file = 'file://' + pam_file
                sssd_ad_json = {'krb5_url': krb5_file, 'smb_url': smb_file, 'sssd_url': sssd_file, 'mkhomedir_url': pam_file}
            else:
                ad_prop = auth_prop.get_ad_properties()
                sssd_ad_json = {'domain_list': [ad_prop.get_domain()], 'workgroup' : ad_prop.get_workgroup()}
            sssd_ad_json['user_ad'] = ad_prop.get_user_ad()
            sssd_ad_json['passwd_ad'] = ad_prop.get_passwd_ad()
            sssd_ad_json['enabled'] = server_conf.get_auth_conf().get_auth_link()
            json_solo['gecos_ws_mgmt']['misc_mgmt']['sssd_res'] = sssd_ad_json
            
        else:
            auth_prop = server_conf.get_auth_conf().get_auth_properties()
            sssd_ldap_json = {'uri': auth_prop.get_url(), 'base': auth_prop.get_basedn(), 'basegroup': auth_prop.get_basedngroup(), 'binddn': auth_prop.get_binddn(), 'bindpwd': auth_prop.get_password()}
            sssd_ldap_json['auth_link'] = server_conf.get_auth_conf().get_auth_link()
            json_solo['gecos_ws_mgmt']['network_mgmt']['sssd_res'] = sssd_ldap_json
    if server_conf.get_gcc_conf().get_uri_gcc() != '':
        gcc_conf = server_conf.get_gcc_conf()
        gcc_json = {'uri_gcc': gcc_conf.get_uri_gcc(), 'gcc_username' : gcc_conf.get_gcc_username(),'gcc_pwd_user': gcc_conf.get_gcc_pwd_user(),'gcc_nodename': gcc_conf.get_gcc_nodename(),'gcc_link': gcc_conf.get_gcc_link(), 'gcc_selected_ou': gcc_conf.get_selected_ou(), 'run_attr': gcc_conf.get_run()}
        json_solo['gecos_ws_mgmt']['misc_mgmt']['gcc_res'] = gcc_json

    if server_conf.get_users_conf().get_users_list():
        users_conf = server_conf.get_users_conf().get_users_list()
        array_users = [] 
        for user in users_conf:
            user_json = {}
            if user.get_actiontorun() == 'delete':
                user_json = {'user': user.get_user(),'groups': user.get_groups(), 'actiontorun': user.get_actiontorun(),'deletehome':user.get_deletehome()}
            else:
                user_json = {'user': user.get_user(), 'password': user.get_password(), 'groups': user.get_groups(), 'actiontorun': user.get_actiontorun(),'name':user.get_name()}
            array_users.append(user_json)

        users_json = {'users_list': array_users}
        json_solo['gecos_ws_mgmt']['misc_mgmt']['local_users_res'] = users_json



    return json_solo



def ldap_is_configured():
    try:
        if not os.path.exists(__LDAP_FLAG__):
            return False
        return True
    except Exception as e:
        raise e


def gcc_is_configured():
    try:
        if not os.path.exists(__GCC_FLAG__):
            return False
        return True

    except Exception as e:
        raise e


def apply_changes():
#TODO implements save the json to run chef solo and run it
    server_conf = get_server_conf(None)
    messages = []
    json_solo = create_solo_json(server_conf)
    resources = json_solo['gecos_ws_mgmt']['misc_mgmt'].keys()
    for res in resources:
        if res == 'tz_date_res':
            if not server_conf.get_ntp_conf().validate():
                messages.append(_("The Date/Time Syncronization parameters are incorrect, please got to Date/Time section or review your autconf file"))
        if res == 'gcc_res':
            if not server_conf.get_gcc_conf().validate():
                messages.append(_("The GCC parameters are incorrect, please got to GCC section or review your autconf file"))
        if res == 'chef_conf_res':
            if not server_conf.get_chef_conf().validate():
                messages.append(_("The Chef parameters are incorrect, please got to GCC section or review your autconf file"))
        if res == 'sssd_res':
            if not server_conf.get_auth_conf().validate():
                messages.append(_("The authentication parameters are incorrect, please go to Authentication section or review your autconf file"))
        if res == 'local_users_res':
            if not server_conf.get_users_conf().validate():
                messages.append(_("The Local Users parameters are incorrect, please go to Users section"))
    if len(messages) > 0:
        display_errors(_("Configuration Error"),messages)
        return 0    
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo,indent=2))
        fp.close()
    print filepath
    run_chef_solo(filepath)

def run_chef_solo(fp):
    try:
        envs = os.environ
        envs['LANG'] = 'es_ES.UTF-8'
        solo_rb = get_prefix() + '/share/gecosws-config-assistant/solo.rb'
        cmd = '"chef-solo" "-c" "%s" "-j" "%s"' % (solo_rb, fp)
        args = shlex.split(cmd)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=envs)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]

        if exit_code[1] != 0:
            messages = [(_('An error has ocurred running chef-solo'))]
            display_errors(_("Configuration Error"), messages)

    except Exception as e:
        display_errors(_("Configuration Error"), [e.message])
         

def unlink_from_sssd():
#TODO implement unlink from ldap calling chef-solo
    server_conf = get_server_conf(None)
    json_solo = {}
    json_solo['run_list'] = ["recipe[gecos_ws_mgmt::unlink_from_sssd]"]
    json_solo['gecos_ws_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['network_mgmt'] = {}
    sssd_json = {}
    sssd_json['enabled'] = server_conf.get_auth_conf().get_auth_link()
    json_solo['gecos_ws_mgmt']['network_mgmt']['sssd_res'] = sssd_json
    return []


def unlink_from_gcc(password):
#TODO Implement unlink from gcc server
    server_conf = get_server_conf(None)
    json_solo = {}
    json_solo['run_list'] = ["recipe[gecos_ws_mgmt::unlink_from_gcc]"]
    json_solo['gecos_ws_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['misc_mgmt'] = {}
    gcc_conf = server_conf.get_gcc_conf()
    gcc_json = {}
    gcc_json = {'uri_gcc': gcc_conf.get_uri_gcc(), 'gcc_username' : gcc_conf.get_gcc_username(), 'gcc_pwd_user': password,'gcc_nodename': gcc_conf.get_gcc_nodename(),'gcc_link': gcc_conf.get_gcc_link(), 'gcc_selected_ou': 'without ou'}
    json_solo['gecos_ws_mgmt']['misc_mgmt']['gcc_res'] = gcc_json
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo,indent=2))
        fp.close()
    run_chef_solo(filepath)
    return []

def unlink_from_chef():
#TODO Implement unlink from chef server
    server_conf = get_server_conf(None)
    json_solo = {}
    json_solo['run_list'] = ["recipe[gecos_ws_mgmt::unlink_from_chef]"]
    json_solo['gecos_ws_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['misc_mgmt'] = {}
    chef_url = server_conf.get_chef_conf().get_url()
    chef_node_name = server_conf.get_chef_conf().get_node_name()
    chef_admin_name = server_conf.get_chef_conf().get_admin_name()
    if chef_admin_name == "":
        chef_admin_name = server_conf.get_gcc_conf().get_gcc_username()
    chef_link = server_conf.get_chef_conf().get_chef_link()
    chef_json = {}
    chef_json = {'chef_server_url':chef_url, 'chef_node_name': chef_node_name, 'chef_validation_pem': __CHEF_PEM__, 'chef_link': chef_link, 'chef_admin_name': chef_admin_name}
    chef_json['chef_link'] = server_conf.get_chef_conf().get_chef_link()
    json_solo['gecos_ws_mgmt']['misc_mgmt']['chef_conf_res'] = chef_json
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo,indent=2))
        fp.close()
    run_chef_solo(filepath)
    return []
#    try:
#
#        script = os.path.join(__BIN_PATH__, __CHEF_CONF_SCRIPT__)
#        if not os.path.exists(script):
#            raise LinkToChefException("The file could not be found: " + script)
#
#        cmd = '"%s" "--restore"' % (script,)
#        args = shlex.split(cmd)
#
#        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#        exit_code = os.waitpid(process.pid, 0)
#        output = process.communicate()[0]
#
#        if exit_code[1] != 0:
#            raise LinkToChefException(_('An error has ocurred unlinking from Chef') + ': ' + output)
#
#    except Exception as e:
#        raise e
#
#    return True

def url_chef(title, text):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_icon_name('dialog-password')
    dialog.set_markup(text)

    hboxurl = Gtk.HBox()
    lblurl = Gtk.Label(_('Url Certificate'))
    lblurl.set_visible(True)
    hboxurl.pack_start(lblurl, False, False, False)
    url = Gtk.Entry()
    url.set_activates_default(True)
    url.show()
    hboxurl.pack_end(url, False, False, False)
    hboxurl.show()

    dialog.get_message_area().pack_start(hboxurl, False, False, False)
    result = dialog.run()
    retval = None
    if result == Gtk.ResponseType.OK:
        retval = url.get_text()
    dialog.destroy()
    return retval



def entry_ou(title, text):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_icon_name('dialog-password')
    dialog.set_markup(text)

    hboxou = Gtk.HBox()
    lblou = Gtk.Label(_('OU Name'))
    lblou.set_visible(True)
    hboxou.pack_start(lblou, False, False, False)
    ou = Gtk.Entry()
    ou.set_activates_default(True)
    ou.show()
    hboxou.pack_end(ou, False, False, False)
    hboxou.show()

    dialog.get_message_area().pack_start(hboxou, False, False, False)
    result = dialog.run()
    retval = None
    if result == Gtk.ResponseType.OK:
        retval = ou.get_text()
    dialog.destroy()
    return retval

def get_hostnames(uri_gcc, username_gcc, password_gcc):
    #Implements code to call API rest to get node list
    global CREDENTIAL_CACHED
    global ACTUAL_USER
    uri_gcc = uri_gcc + '/node/list/'
    url_parsed = urlparse.urlparse(uri_gcc)
    user = username_gcc
    password = password_gcc
    hostname = url_parsed.hostname
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    content = '' 
    validate = False
    if hostname in CREDENTIAL_CACHED:
        credentials = CREDENTIAL_CACHED[hostname]
        for cred in credentials:
            user, password = cred[0], cred[1]
            r = requests.get(url, auth=(user,password), headers=headers)
            if r.ok:
                validate = True

    if not validate:

        r = requests.get(url, auth=(user,password), headers=headers)
        if r.ok:
            if not CREDENTIAL_CACHED.has_key(hostname):
                CREDENTIAL_CACHED[hostname] = []
            credentials = CREDENTIAL_CACHED[hostname]
            credentials.append([user, password])
            ACTUAL_USER = (user, password)
        else:
            raise ServerConfException(_('Authentication is failed.'))
    if hasattr(r,'text'):
        content = r.text
    else:  
        content = r.content

    arr_hostname = json.loads(content)

    #Testing lines
    # arr_hostname = []
    # hostname = {'chef_id': '23c3cd0e88b5df0e9fe29a5200723cda', 'pclabel': 'test1'}
    # arr_hostname.append(hostname)
    # hostname = {'chef_id': 'cf5ecbd267b6c6558884edc9e023cf8b', 'pclabel': 'test2'}
    # arr_hostname.append(hostname)
    return arr_hostname

def select_node(title, text, hostnames):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_icon_name('dialog-password')
    dialog.set_markup(text)

    hboxws = Gtk.HBox()
    lblws = Gtk.Label(_('Select Workstation'))
    lblws.set_visible(True)
    hboxws.pack_start(lblws, False, False, False)
    ws_store = Gtk.ListStore(str, str)
    for ws in hostnames:
        ws_store.append([ws['pclabel'], ws['chef_id']])

    ws_combo = Gtk.ComboBox.new_with_model(ws_store)
    renderer_text = Gtk.CellRendererText()
    ws_combo.pack_start(renderer_text, True)
    ws_combo.add_attribute(renderer_text, "text", 0)    

    ws_combo.show()
    hboxws.pack_end(ws_combo, False, False, False)
    hboxws.show()

    dialog.get_message_area().pack_start(hboxws, False, False, False)
    result = dialog.run()
    retval = None
    if result == Gtk.ResponseType.OK:
        model = ws_combo.get_model()
        retval = model[ws_combo.get_active()][1]
    dialog.destroy()
    return retval

def select_ou(title, text, ous):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_icon_name('dialog-password')
    dialog.set_markup(text)

    hboxou = Gtk.HBox()
    lblou = Gtk.Label(_('Select OU'))
    lblou.set_visible(True)
    hboxou.pack_start(lblou, False, False, False)
    ou_store = Gtk.ListStore(str, str)
    for ou in ous:
        ou_store.append([ou[1], ou[0]])

    ou_combo = Gtk.ComboBox.new_with_model(ou_store)
    renderer_text = Gtk.CellRendererText()
    ou_combo.pack_start(renderer_text, True)
    ou_combo.add_attribute(renderer_text, "text", 0)    

    ou_combo.show()
    hboxou.pack_end(ou_combo, False, False, False)
    hboxou.show()

    dialog.get_message_area().pack_start(hboxou, False, False, False)
    result = dialog.run()
    retval = None
    if result == Gtk.ResponseType.OK:
        model = ou_combo.get_model()
        retval = model[ou_combo.get_active()][1]
    dialog.destroy()
    return retval


def display_errors(title, messages):
    text = ''
    for message in messages:
        text += message + '\n'
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,text)
    dialog.set_title(title)
    result = dialog.run()
    dialog.destroy()
    return result 

def get_passwd_gcc(username):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(_('GCC Password'))
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_icon_name('dialog-password')
    dialog.set_markup(_('Please insert GCC password for user ') + username )
    hboxpwd = Gtk.HBox()
    lblpwd = Gtk.Label(_('password'))
    lblpwd.set_visible(True)
    hboxpwd.pack_start(lblpwd, False, False, False)
    pwd = Gtk.Entry()
    pwd.set_activates_default(True)
    pwd.set_visibility(False)
    pwd.show()
    hboxpwd.pack_end(pwd, False, False, False)
    hboxpwd.show()
    dialog.get_message_area().pack_start(hboxpwd, False, False, False)
    result = dialog.run()

    retval = None
    if result == Gtk.ResponseType.OK:
        retval = pwd.get_text()

    dialog.destroy()
    return retval
    

def auth_dialog(title, text):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_icon_name('dialog-password')
    dialog.set_markup(text)

    hboxuser = Gtk.HBox()
    lbluser = Gtk.Label(_('user'))
    lbluser.set_visible(True)
    hboxuser.pack_start(lbluser, False, False, False)
    user = Gtk.Entry()
    user.set_activates_default(True)
    user.show()
    hboxuser.pack_end(user, False, False, False)
    hboxuser.show()

    hboxpwd = Gtk.HBox()
    lblpwd = Gtk.Label(_('password'))
    lblpwd.set_visible(True)
    hboxpwd.pack_start(lblpwd, False, False, False)
    pwd = Gtk.Entry()
    pwd.set_activates_default(True)
    pwd.set_visibility(False)
    pwd.show()
    hboxpwd.pack_end(pwd, False, False, False)
    hboxpwd.show()

    dialog.get_message_area().pack_start(hboxuser, False, False, False)
    dialog.get_message_area().pack_end(hboxpwd, False, False, False)
    result = dialog.run()

    retval = [None, None]
    if result == Gtk.ResponseType.OK:
        retval = [user.get_text(), pwd.get_text()]

    dialog.destroy()
    return retval


class ServerConfException(Exception):
    '''
    Raised when there are errors retrieving the remote configuration.
    '''

    def __init__(self, msg):
        Exception.__init__(self, msg)


class LinkToLDAPException(Exception):
    '''
    Raised when there are errors trying to link the client to a LDAP server.
    '''

    def __init__(self, msg):
        Exception.__init__(self, msg)


class LinkToADException(Exception):
    '''
    Raised when there are errors trying to link the client to a LDAP server.
    '''

    def __init__(self, msg):
        Exception.__init__(self, msg)


class LinkToChefException(Exception):
    '''
    Raised when there are errors trying to link the client to a Chef server.
    '''

    def __init__(self, msg):
        Exception.__init__(self, msg)
