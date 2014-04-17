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
from gettext import gettext as _
gettext.textdomain('firstboot')


__URLOPEN_TIMEOUT__ = 15
__JSON_CACHE__ = '/tmp/json_cached'
__BIN_PATH__ = firstbootconfig.get_bin_path()
__LDAP_CONF_SCRIPT__ = 'firstboot-ldapconf.sh'
__CHEF_CONF_SCRIPT__ = 'firstboot-chefconf.sh'
__GCC_FLAG__ = '/etc/gcc.control'
__AD_CONF_SCRIPT__ = 'firstboot-adconf.sh'

CREDENTIAL_CACHED = {}


def validate_credentials(url):
    global CREDENTIAL_CACHED
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

        import ipdb; ipdb.set_trace()
        user, password = auth_dialog(_('Authentication Required'),
            _('You need to enter your credentials to access the requested resource.'))
        r = requests.get(url, auth=(user,password), headers=headers)
        if r.ok:
            if not CREDENTIAL_CACHED.has_key(hostname):
                CREDENTIAL_CACHED[hostname] = []
            credentials = CREDENTIAL_CACHED[hostname]
            credentials.append([user, password])
        else:
            raise ServerConfException(_('Authentication is failed.'))
    
    return r.text

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
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(content.decode('base64'))
        fp.close()

    return filepath


def create_conf_file(file_content):
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(file_content.decode('base64'))
        fp.close()

    return filepath

def get_chef_hostnames(chef_conf):

    chef_url = chef_conf.get_url()
    pem_file_path = create_chef_pem(chef_conf)

    cmd = 'knife node list -u chef-validator -k %s -s %s' % (pem_file_path, chef_url)
    args = shlex.split(cmd)

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exit_code = os.waitpid(process.pid, 0)
    output = process.communicate()[0]
    output = output.strip()

    names = []
    if exit_code[1] != 0:
        raise ServerConfException(_('Couldn\'t retrieve the host names list') + ': ' + output)

    else:
        try:
            names = json.loads(output)
        except ValueError as e:
            names = output.split('\n')

    hostnames = []
    for name in names:
        name = name.strip()
        if name.startswith('WARNING') or name.startswith('ERROR'):
            continue
        hostnames.append(name)

    os.remove(pem_file_path)
    return hostnames


def ad_is_configured():
    try:
        script = os.path.join(__BIN_PATH__, __AD_CONF_SCRIPT__)
        if not os.path.exists(script):
            raise LinkToADException(_("The Active Directory configuration script couldn't be found") + ': ' + script)
        cmd = '"%s" "--query"' % (script,)
        args = shlex.split(cmd)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]
        output = output.strip()
        if exit_code[1] == 0:
            ret = bool(int(output))
            return ret

        else:
            raise LinkToADException(_('Active Directory setup error') + ': ' + output)

    except Exception as e:
        raise e


def create_solo_json(server_conf):
    json_solo = {}
    json_solo['run_list'] = ["recipe[gecos_ws_mgmt::local]"]
    json_solo['gecos_ws_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['misc_mgmt'] = {}
    if server_conf.get_ntp_conf().get_uri_ntp() != '':
        json_solo['gecos_ws_mgmt']['misc_mgmt']['tz_date_res'] = {'server':server_conf.get_ntp_conf().get_uri_ntp()}
    if server_conf.get_chef_conf().get_url() != '':
        tmpfile = create_chef_pem(server_conf.get_chef_conf())
        chef_url = server_conf.get_chef_conf().get_url()
        chef_node_name = server_conf.get_chef_conf().get_node_name()
        chef_json = {'chef_server_url':chef_url, 'chef_node_name': chef_node_name, 'chef_validation_pem': tmpfile}
        json_solo['gecos_ws_mgmt']['misc_mgmt']['chef_conf_res'] = chef_json
    if server_conf.get_auth_conf().get_auth_type() != '':
        auth_type = server_conf.get_auth_conf().get_auth_type()
        if auth_type == 'ad':
            auth_prop = server_conf.get_auth_conf().get_auth_properties()
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
                sssd_ad_json = {'krb5_url': krb5_file, 'smb_url': smb_file, 'sssd_url': sssd_file, 'mkhimedir_url': pam_file}
                json_solo['gecos_ws_mgmt']['misc_mgmt']['sssd_ad_res'] = sssd_ad_json
            else:
                ad_prop = auth_prop.get_ad_properties()
                sssd_ad_json = {'fqdn':  ad_prop.get_fqdn(), 'workgroup' : ad_prop.get_workgroup()}
                json_solo['gecos_ws_mgmt']['misc_mgmt']['sssd_ad_res'] = sssd_ad_json
                
        else:
            auth_prop = server_conf.get_auth_conf().get_auth_properties()
            sssd_ldap_json = {'uri': auth_prop.get_url(), 'base': auth_prop.get_basedn(), 'basegroup': auth_prop.get_basedngroup(), 'binddn': auth_prop.get_binddn(), 'bindpwd': auth_prop.get_password()}
            json_solo['gecos_ws_mgmt']['misc_mgmt']['sssd_ldap_res'] = sssd_ldap_json
    if server_conf.get_gcc_conf().get_uri_gcc() != '':
        gcc_conf = server_conf.get_gcc_conf()
        gcc_json = {'uri_gcc': gcc_conf.get_uri_gcc(), 'gcc_username' : gcc_conf.get_gcc_username(), 'ou_username': gcc_conf.get_ou_username(), 'gcc_pwd_user': gcc_conf.get_gcc_pwd_user(),'gcc_nodename': gcc_conf.get_nodename(),'gcc_link': gcc_conf.get_link()}
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

        script = os.path.join(__BIN_PATH__, __LDAP_CONF_SCRIPT__)
        if not os.path.exists(script):
            raise LinkToLDAPException(_("The LDAP configuration script couldn't be found") + ': ' + script)

        cmd = '"%s" "--query"' % (script,)
        args = shlex.split(cmd)

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]
        output = output.strip()

        if exit_code[1] == 0:
            ret = bool(int(output))
            return ret

        else:
            raise LinkToLDAPException(_('LDAP setup error') + ': ' + output)

    except Exception as e:
        raise e


def gcc_is_configured():
    try:

        gcc_flag = os.path.join(__GCC_FLAG__)
        if not os.path.exists(gcc_flag):
            return False
        return True

    except Exception as e:
        raise e


def setup_server(server_conf, link_ldap=False, unlink_ldap=False,
                link_chef=False, unlink_chef=False, link_ad=False, unlink_ad=False):

    result = True
    messages = []

    if unlink_ldap == True:
        try:
            ret = unlink_from_ldap()
            if ret == True:
                messages.append({'type': 'info', 'message': _('Workstation has been unlinked from LDAP.')})
            else:
                messages += ret
        except Exception as e:
            messages.append({'type': 'error', 'message': str(e)})

    elif link_ldap == True:
        try:
            ret = link_to_ldap(server_conf.get_ldap_conf())
            if ret == True:
                messages.append({'type': 'info', 'message': _('The LDAP has been configured successfully.')})
            else:
                messages += ret
        except Exception as e:
            messages.append({'type': 'error', 'message': str(e)})

    if unlink_ad == True:
        try:
            ret = unlink_from_ad()
            if ret == True:
                messages.append({'type': 'info', 'message': _('Workstation has been unlinked from the Active Directory.')})
            else:
                messages += ret
        except Exception as e:
            messages.append({'type': 'error', 'message': str(e)})

    elif link_ad == True:
        try:
            ret = link_to_ad(server_conf.get_ad_conf())
            if ret == True:
                messages.append({'type': 'info', 'message': _('The Active Directory has been configured successfully.')})
            else:
                messages += ret
        except Exception as e:
            messages.append({'type': 'error', 'message': str(e)})

    if unlink_chef == True:
        try:
            ret = unlink_from_chef()
            if ret == True:
                messages.append({'type': 'info', 'message': _('Workstation has been unlinked from Chef.')})
            else:
                messages += ret
        except Exception as e:
            messages.append({'type': 'error', 'message': str(e)})

    elif link_chef == True:
        try:
            ret = link_to_chef(server_conf.get_chef_conf())
            if ret == True:
                messages.append({'type': 'info', 'message': _('The Chef client has been configured successfully.')})
            else:
                messages += ret
        except Exception as e:
            messages.append({'type': 'error', 'message': str(e)})

    for msg in messages:
        if msg['type'] == 'error':
            result = False
            break

    return result, messages


def link_to_ldap(ldap_conf):

    url = ldap_conf.get_url()
    basedn = ldap_conf.get_basedn()
    basedngroup = ldap_conf.get_basedngroup()
    binddn = ldap_conf.get_binddn()
    password = ldap_conf.get_password()
    errors = []

    if len(url) == 0:
        errors.append({'type': 'error', 'message': _('The LDAP URL cannot be empty.')})

    if len(basedn) == 0:
        errors.append({'type': 'error', 'message': _('The LDAP BaseDN cannot be empty.')})

    if len(binddn) == 0:
        errors.append({'type': 'error', 'message': _('The LDAP BindDN cannot be empty.')})

    if len(errors) > 0:
        return errors

    try:

        script = os.path.join(__BIN_PATH__, __LDAP_CONF_SCRIPT__)
        if not os.path.exists(script):
            raise LinkToLDAPException(_("The LDAP configuration script couldn't be found") + ': ' + script)

        cmd = '"%s" "%s" "%s" "%s" "%s" "%s"' % (script, url, basedn, basedngroup, binddn, password)
        args = shlex.split(cmd)

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]

        if exit_code[1] != 0:
            raise LinkToLDAPException(_('LDAP setup error') + ': ' + output)

    except Exception as e:
        raise e

    return True


def link_to_ad(ad_conf):

    fqdn = ad_conf.get_fqdn()
    dns_domain = ad_conf.get_dns_domain()
    user = ad_conf.get_user()
    passwd = ad_conf.get_passwd()
    errors = []

    if len(fqdn) == 0:
        errors.append({'type': 'error', 'message': _('The Active Directory URL cannot be empty.')})

    if len(dns_domain) == 0:
        errors.append({'type': 'error', 'message': _('The DNS Domain cannot be empty.')})
    if len(user) == 0:
        errors.append({'type': 'error', 'message': _('The administrator user cannot be empty.')})
    if len(passwd) == 0:
        errors.append({'type': 'error', 'message': _('The administrator password cannot be empty.')})

    if len(errors) > 0:
        return errors

    try:

        script = os.path.join(__BIN_PATH__, __AD_CONF_SCRIPT__)
        if not os.path.exists(script):
            raise LinkToADException(_("The Active Directory configuration script couldn't be found") + ': ' + script)

        cmd = '"%s" "%s" "%s" "%s" "%s"' % (script, fqdn, dns_domain, user, passwd)
        args = shlex.split(cmd)

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]

        if exit_code[1] != 0:
            raise LinkToADException(_('Active Directory setup error') + ': ' + output)

    except Exception as e:
        raise e

    return True


def unlink_from_ldap():

    try:

        script = os.path.join(__BIN_PATH__, __LDAP_CONF_SCRIPT__)
        if not os.path.exists(script):
            raise LinkToLDAPException("The file could not be found: " + script)

        cmd = '"%s" "--restore"' % (script,)
        args = shlex.split(cmd)

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]

        if exit_code[1] != 0:
            raise LinkToLDAPException(_('An error has ocurred unlinking from LDAP') + ': ' + output)

    except Exception as e:
        raise e

    return True


def unlink_from_ad():

    try:

        script = os.path.join(__BIN_PATH__, __AD_CONF_SCRIPT__)
        if not os.path.exists(script):
            raise LinkToADException("The file could not be found: " + script)

        cmd = '"%s" "--restore"' % (script,)
        args = shlex.split(cmd)

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]

        if exit_code[1] != 0:
            raise LinkToADException(_('An error has ocurred unlinking from Active Directory') + ': ' + output)

    except Exception as e:
        raise e

    return True


def link_to_chef(chef_conf):

    url = chef_conf.get_url()
    pemurl = chef_conf.get_pem_url()
    role = chef_conf.get_default_role()
    hostname = chef_conf.get_hostname()
    user = chef_conf.get_user()
    password = chef_conf.get_password()
    errors = []

    if len(url) == 0:
        errors.append({'type': 'error', 'message': _('The Chef URL cannot be empty.')})

    if len(pemurl) == 0:
        errors.append({'type': 'error', 'message': _('The Chef certificate URL cannot be empty.')})

    if len(hostname) == 0:
        errors.append({'type': 'error', 'message': _('The Chef host name cannot be empty.')})

    if len(errors) > 0:
        return errors

    try:

        script = os.path.join(__BIN_PATH__, __CHEF_CONF_SCRIPT__)
        if not os.path.exists(script):
            raise LinkToChefException(_("The Chef configuration script couldn't be found") + ': ' + script)

        cmd = '"%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (script, url, pemurl, hostname, user, password, role)
        args = shlex.split(cmd)

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = os.waitpid(process.pid, 0)
        output = process.communicate()[0]

        if exit_code[1] != 0:
            raise LinkToChefException(_('Chef setup error') + ': ' + output)

    except Exception as e:
        raise e

    return True

def unlink_from_gcc():
#TODO Implement unlink from gcc server
    return []

def unlink_from_chef():
#TODO Implement unlink from chef server
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
    retval = [None, None]
    if result == Gtk.ResponseType.OK:
        retval = url.get_text()
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
