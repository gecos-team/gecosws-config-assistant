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
import time
import urllib
import urllib2
import urlparse


from gi.repository import Gtk, Gdk
from firstboot_lib import firstbootconfig
from ServerConf import ServerConf
from ChefSolo import ChefSolo

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
__CHEF_FLAG__ = '/etc/chef.control'
__LDAP_FLAG__ = '/etc/gca-sssd.control'
__AD_FLAG__ = __LDAP_FLAG__
__CHEF_CLIENT_PEM__ = '/etc/chef/client.pem'
__CHEF_PEM__ = '/etc/chef/validation.pem'
__AD_CONF_SCRIPT__ = 'firstboot-adconf.sh'

CREDENTIAL_CACHED = {}
ACTUAL_USER = ()


def validate_credentials(url, err_chef_solo=False):
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
            r = requests.get(url, auth=(user,password), headers=headers, verify=False)
            if r.ok:
                validate = True

    if not validate:
        if err_chef_solo:
            user, password = auth_dialog(_('Authentication Required'),
            _('You need to enter your GCC credentials to restoring the Workstation.'))
        else:
            user, password = auth_dialog(_('Authentication Required'),
            _('You need to enter your credentials to access the requested resource.'))
        r = requests.get(url, auth=(user,password), headers=headers, verify=False)
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
        if ACTUAL_USER != ():
            conf["gcc"]["gcc_pwd_user"] = ACTUAL_USER[1]
        if conf["chef"]["chef_server_uri"] == "https://localhost/":
            chef_uri = conf["gcc"]["uri_gcc"].split('//')[1].split(':')[0]
            conf["chef"]["chef_server_uri"] = "https://" + chef_uri + '/'

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
    if ACTUAL_USER != ():
        conf["gcc"]["gcc_pwd_user"] = ACTUAL_USER[1]
    if conf["chef"]["chef_server_uri"] == "https://localhost/":
        chef_uri = conf["gcc"]["uri_gcc"].split('//')[1].split(':')[0]
        conf["chef"]["chef_server_uri"] = "https://" + chef_uri + '/'
    return conf

def get_server_conf(content):
    server_conf = ServerConf.Instance()
    if content != None:
        server_conf.load_data(content)
    return server_conf

def create_pem(pem_string):
    content = pem_string
    if not os.path.exists('/etc/chef/'):
        os.makedirs('/etc/chef/')
    fp = open(__CHEF_PEM__, "w+b")
    if fp:
        fp.write(content.decode('base64'))
        fp.close()

    return __CHEF_PEM__


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


def ad_is_configured():

    try:
        if not os.path.exists(__AD_FLAG__):
            return False
        return True
    except Exception as e:
        raise e


def create_solo_json(server_conf):
    json_solo = {}
    json_solo_sssd = {}
    json_solo['run_list'] = ["recipe[ohai-gecos::default]", "recipe[chef-client::upstart_service]", "recipe[gecos_ws_mgmt::local]"]
    json_solo_sssd['run_list'] = ["recipe[ohai-gecos::default]", "recipe[chef-client::upstart_service]", "recipe[gecos_ws_mgmt::local]"]
    json_solo['gecos_ws_mgmt'] = {}
    json_solo_sssd['gecos_ws_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['misc_mgmt'] = {}
    json_solo_sssd['gecos_ws_mgmt']['network_mgmt'] = {}
    if server_conf.get_ntp_conf().get_uri_ntp() != '':
        json_solo['gecos_ws_mgmt']['misc_mgmt']['tz_date_res'] = {'server':server_conf.get_ntp_conf().get_uri_ntp()}
    if server_conf.get_chef_conf().get_url() != '' and not chef_is_configured():
        tmpfile = create_chef_pem(server_conf.get_chef_conf())
        chef_url = server_conf.get_chef_conf().get_url()
        chef_node_name = server_conf.get_chef_conf().get_node_name()
        chef_admin_name = server_conf.get_chef_conf().get_admin_name()
        if chef_admin_name == "":
            chef_admin_name = server_conf.get_chef_conf().toChefUsername(server_conf.get_gcc_conf().get_gcc_username())
        chef_link = server_conf.get_chef_conf().get_chef_link()
        chef_link_existing = server_conf.get_chef_conf().get_chef_link_existing()
        chef_json = {'chef_server_url':chef_url, 'chef_node_name': chef_node_name, 'chef_validation_pem': tmpfile, 'chef_link': chef_link, 'chef_admin_name': chef_admin_name, 'chef_link_existing': chef_link_existing}
        json_solo['gecos_ws_mgmt']['misc_mgmt']['chef_conf_res'] = chef_json
    if server_conf.get_auth_conf().get_auth_type() != '' and not ad_is_configured():
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
                sssd_ad_json = {'krb5_url': krb5_file, 'smb_url': smb_file, 'sssd_url': sssd_file, 'mkhomedir_url': pam_file, 'domain': {}}
            else:
                ad_prop = auth_prop.get_ad_properties()
                sssd_ad_json = {'domain': {}}
            sssd_ad_json['enabled'] = server_conf.get_auth_conf().get_auth_link()
            sssd_ad_json['domain']['ad_user'] = ad_prop.get_user_ad()
            sssd_ad_json['domain']['name'] = ad_prop.get_domain()
            sssd_ad_json['domain']['ad_passwd'] = ad_prop.get_passwd_ad()
            sssd_ad_json['domain']['type'] = auth_type
            sssd_ad_json['domain']['workgroup'] = ad_prop.get_workgroup()
            json_solo_sssd['gecos_ws_mgmt']['network_mgmt']['sssd_res'] = sssd_ad_json
            
        else:
            auth_prop = server_conf.get_auth_conf().get_auth_properties()
            sssd_ldap_json = {'domain':{}}
            sssd_ldap_json['enabled'] = server_conf.get_auth_conf().get_auth_link()
            sssd_ldap_json['domain']['name'] = 'ldap_gecos_conf'
            sssd_ldap_json['domain']['ldap_uri'] = auth_prop.get_url()
            sssd_ldap_json['domain']['type'] = auth_type
            sssd_ldap_json['domain']['search_base'] = auth_prop.get_basedn()
            sssd_ldap_json['domain']['base_group'] = auth_prop.get_basedngroup()
            sssd_ldap_json['domain']['bind_dn'] = auth_prop.get_binddn()
            sssd_ldap_json['domain']['bind_pass'] = auth_prop.get_password()
            json_solo_sssd['gecos_ws_mgmt']['network_mgmt']['sssd_res'] = sssd_ldap_json
    if server_conf.get_gcc_conf().get_uri_gcc() != '' and not gcc_is_configured():
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



    return json_solo ,json_solo_sssd



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

def chef_is_configured():
    try:
        if not os.path.exists(__CHEF_FLAG__):
            return False
        return True

    except Exception as e:
        raise e



def apply_changes():
#TODO implements save the json to run chef solo and run it
    server_conf = get_server_conf(None)
    messages = []
    json_solo, json_solo_sssd = create_solo_json(server_conf)
    resources = json_solo['gecos_ws_mgmt']['misc_mgmt'].keys()
    for res in resources:
        if res == 'tz_date_res':
            if not server_conf.get_ntp_conf().validate():
                messages.append(_("The Date/Time Syncronization parameters are incorrect, please got to Date/Time section or review your autconf file"))
        if res == 'gcc_res' and not gcc_is_configured():
            if not server_conf.get_gcc_conf().validate():
                messages.append(_("The GCC parameters are incorrect, please got to GCC section or review your autconf file"))
        if res == 'chef_conf_res' and not chef_is_configured():
            if not server_conf.get_chef_conf().validate():
                messages.append(_("The Chef parameters are incorrect, please got to GCC section or review your autconf file"))
        if res == 'local_users_res':
            if not server_conf.get_users_conf().validate():
                messages.append(_("The Local Users parameters are incorrect, please go to Users section"))

    resources = json_solo_sssd['gecos_ws_mgmt']['network_mgmt'].keys()
    for res in resources:
        if res == 'sssd_res':
            if not server_conf.get_auth_conf().validate():
                messages.append(_("The authentication parameters are incorrect, please go to Authentication section or review your autconf file"))

    if len(messages) > 0:
        display_errors(_("Configuration Error"),messages)
        return 0    
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo,indent=2))
        fp.close()
    print filepath
    run_chef_solo(filepath, _("Configuring the client to link with Gecos Control Center, this may take several minutes.\nPlease wait a moment"))
    os.unlink(filepath)

    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo_sssd,indent=2))
        fp.close()
    print filepath
    run_chef_solo(filepath, _("Configuring the client to link authentication method, this may take several minutes.\nPlease wait a moment"), False, True)
    os.unlink(filepath)



def destroy_pgbar(widget, response, dialog, thread):
    if dialog == None:
        dialog = widget
    if thread.isAlive():
        return True
    else:
        dialog.hide()

def run_chef_solo(fp, message, unlink=False, jsssd=False):
    try:
        server_conf = get_server_conf(None)
        status = Gtk.Label()
        log = Gtk.TextView()
        log.set_editable(False)
        thread = ChefSolo(fp, server_conf, unlink, gcc_is_configured(), chef_is_configured(), status, log)
        dialog = Gtk.Dialog(_('Configuring the client'), None,
                Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_default_size(600, 400)
        description = Gtk.Label()
        progressbar = Gtk.ProgressBar()
        description.set_text(message)
        box = Gtk.VBox()
        content_area = dialog.get_content_area()
        content_area.set_spacing(10)
        content_area.pack_start(Gtk.Fixed(),False,False,0)
        content_area.pack_start(box,False,False,0)
        content_area.pack_start(Gtk.Fixed(),False,False,0)
        box.pack_start(description,False,False,10)
        box.pack_start(progressbar, False, False, 10)
        box.pack_start(status, False, False, 10)

        sw = Gtk.ScrolledWindow()
        sw.set_hexpand(True)
        sw.set_vexpand(True)
        sw.set_size_request(300, 200)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.add(log)
        box.pack_start(sw, False, False, 10)
        
        dialog.connect("delete-event", destroy_pgbar, None, thread)
        dialog.show_all()  
        dialog.get_children()[0].set_spacing(10)
        dialog.get_children()[0].get_children()[0].set_margin_right(10)
        dialog.get_children()[0].get_children()[1].set_spacing(10)
        dialog.get_children()[0].get_children()[2].set_margin_right(10)
        
        button = dialog.get_children()[0].get_children()[3].get_children()[0]
        button.set_sensitive(False)
        button.connect("clicked", destroy_pgbar, None, dialog, thread )
        
        thread.daemon = True 
        thread.start()
        while thread.isAlive():
            time.sleep(0.09)
            progressbar.pulse() 
            while Gtk.events_pending():
                Gtk.main_iteration()
        button.set_sensitive(True)
        progressbar.set_fraction(1.0)
        exit_code = thread.get_exit_code()
        description.set_text(_("The client has been configured"))
        status.set_text("")
        if exit_code[1] != 0 and not unlink:
            description.set_text(_('An error has ocurred running chef-solo'))
            messages = [(_('An error has ocurred running chef-solo'))]
            display_errors(_("Configuration Error"), messages)

            server_conf = get_server_conf(None)
            ## TODO Implement unlink GCC an Chef into serverconf Class
            if not jsssd:
                if chef_is_configured():
                    pem = ''
                    if not server_conf.get_chef_conf().validate():
                        chef_flag = open(__CHEF_FLAG__, 'r')
                        content = chef_flag.read()
                        chef_flag.close()
                        chef_flag_json = json.loads(content)
                        server_conf.get_chef_conf().set_url(chef_flag_json['chef_server_url'])
                        server_conf.get_chef_conf().set_node_name(chef_flag_json['chef_node_name'])
                        json_server = validate_credentials(chef_flag_json['chef_server_url'])
                        json_server = json.loads(json_server)
                        pem = json_server['chef']['chef_validation']
                        server_conf.get_chef_conf().set_admin_name(json_server['gcc']['gcc_username'])
                    else:
                        pem = server_conf.get_chef_conf().get_pem()
                    create_pem(pem)
                    unlink_from_chef()
                            
                if gcc_is_configured():
                    
                    if not server_conf.get_gcc_conf().validate():
                        gcc_flag = open(__GCC_FLAG__, 'r')
                        content = gcc_flag.read()
                        gcc_flag.close()
                        gcc_flag_json = json.loads(content)
                        server_conf.get_gcc_conf().set_uri_gcc(gcc_flag_json['uri_gcc'])
                        server_conf.get_gcc_conf().set_gcc_nodename(gcc_flag_json['gcc_nodename'])
                        server_conf.get_gcc_conf().set_run(True)
                        json_server = validate_credentials(gcc_flag_json['uri_gcc'] + '/auth/config/')
                        json_server = json.loads(json_server)
                        server_conf.get_gcc_conf().set_gcc_username(json_server['gcc']['gcc_username'])
                    unlink_from_gcc(server_conf.get_gcc_conf().get_gcc_username())
            else:
                if ad_is_configured():
                    unlink_from_sssd(False)

                
        if exit_code[1] != 0 and unlink:
            if chef_is_configured():
                clean_conf_chef()
            if gcc_is_configured():
                clean_conf_gcc()
            messages = [(_('No connection to the server. It will unlink locally'))]
            display_errors(_("Configuration Error"), messages)  

    except Exception as e:
        display_errors(_("Configuration Error"), [e.message])


def clean_conf_gcc():
    try:
        if os.path.exists(__GCC_FLAG__):
            os.remove(__GCC_FLAG__)
    except Exception as e:
        raise e


def clean_conf_chef():
    try:
        if os.path.exists(__CHEF_FLAG__):
            os.remove(__CHEF_FLAG__)
        if os.path.exists(__CHEF_PEM__):
            os.remove(__CHEF_PEM__)
        if os.path.exists(__CHEF_CLIENT_PEM__):
            os.remove(__CHEF_CLIENT_PEM__)
    except Exception as e:
        raise e

def unlink_from_sssd(leave=True):
#TODO implement unlink from ldap calling chef-solo
    server_conf = get_server_conf(None)
    json_solo = {}
    json_solo['run_list'] = ["recipe[gecos_ws_mgmt::unlink_from_sssd]"]
    json_solo['gecos_ws_mgmt'] = {}
    json_solo['gecos_ws_mgmt']['network_mgmt'] = {}
    sssd_json = {}
    auth_type = server_conf.get_auth_conf().get_auth_type()
    auth_prop = server_conf.get_auth_conf().get_auth_properties()
    sssd_json['enabled'] = False
    if auth_type == 'ad':
        ad_prop = auth_prop.get_ad_properties()
        sssd_json['domain'] = {}
        sssd_json['domain']['type'] = auth_type
        sssd_json['domain']['ad_user'] = ad_prop.get_user_ad()
        sssd_json['domain']['ad_passwd'] = ad_prop.get_passwd_ad()
        sssd_json['domain']['workgroup'] = 'default'
        sssd_json['domain']['name'] = 'default'

    else:
        sssd_json['domain'] = {}
        sssd_json['domain']['type'] = auth_type

    if leave:
        sssd_json['domain']['leave'] = True
    else:
        sssd_json['domain']['leave'] = False
    
    json_solo['gecos_ws_mgmt']['network_mgmt']['sssd_res'] = sssd_json
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo,indent=2))
        fp.close()
    run_chef_solo(filepath, _("Restoring authentication configuration"), True)
    os.unlink(filepath)
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
    gcc_json = {'uri_gcc': gcc_conf.get_uri_gcc(), 'gcc_username' : gcc_conf.get_gcc_username(), 'gcc_pwd_user': password,'gcc_nodename': gcc_conf.get_gcc_nodename(),'gcc_link': False, 'gcc_selected_ou': 'without ou'}
    json_solo['gecos_ws_mgmt']['misc_mgmt']['gcc_res'] = gcc_json
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo,indent=2))
        fp.close()
    run_chef_solo(filepath, _("Unlink from GCC"), True)
    os.unlink(filepath)
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
    chef_json = {'chef_server_url':chef_url, 'chef_node_name': chef_node_name, 'chef_validation_pem': __CHEF_PEM__, 'chef_link': False, 'chef_admin_name': chef_admin_name}
    chef_json['chef_link'] = False
    json_solo['gecos_ws_mgmt']['misc_mgmt']['chef_conf_res'] = chef_json
    (fd, filepath) = tempfile.mkstemp(dir='/tmp')
    fp = os.fdopen(fd, "w+b")
    if fp:
        fp.write(json.dumps(json_solo,indent=2))
        fp.close()
    run_chef_solo(filepath, _("Unlink from Server"), True)
    os.unlink(filepath)
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


def search_ou_by_text(uri_gcc, username_gcc, password_gcc, text):
    #Implements code to call API rest to get node list
    global CREDENTIAL_CACHED
    global ACTUAL_USER
    uri_gcc = uri_gcc + '/ou/gca/?q=' + text
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
            r = requests.get(uri_gcc, auth=(user,password), headers=headers, verify=False)
            if r.ok:
                validate = True

    if not validate:

        r = requests.get(uri_gcc, auth=(user,password), headers=headers, verify=False)
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

    arr_ou = json.loads(content)['ous']
    return arr_ou

def get_hostnames(uri_gcc, username_gcc, password_gcc):
    #Implements code to call API rest to get node list
    global CREDENTIAL_CACHED
    global ACTUAL_USER
    uri_gcc = uri_gcc + '/computers/list/'
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
            r = requests.get(uri_gcc, auth=(user,password), headers=headers, verify=False)
            if r.ok:
                validate = True

    if not validate:

        r = requests.get(uri_gcc, auth=(user,password), headers=headers, verify=False)
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

    arr_hostname = json.loads(content)['computers']

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

    hbosearch = Gtk.HBox()
    lblsearch = Gtk.Label(_('Pattern search'))
    lblsearch.set_visible(True)
    hbosearch.pack_start(lblsearch, False, False, 10)

    hboxws = Gtk.HBox()
    lblws = Gtk.Label(_('Select Workstation'))
    lblws.set_visible(True)
    hboxws.pack_start(lblws, False, False, False)
    ws_store = Gtk.ListStore(str, str)
    for ws in hostnames:
        ws_store.append([ws['name'], ws['node_chef_id']])

    ws_combo = Gtk.ComboBox.new_with_model(ws_store)
    renderer_text = Gtk.CellRendererText()
    ws_combo.pack_start(renderer_text, True)
    ws_combo.add_attribute(renderer_text, "text", 0)    

    search = Gtk.Entry()
    search.set_activates_default(True)
    search.show()
    hbosearch.pack_start(search, False, False, False)
    hbosearch.show()
    dialog.get_message_area().pack_start(hbosearch, False, False, False)
    
    search.connect('changed', search_ws, ws_combo, hostnames)

    ws_combo.show()
    hboxws.pack_end(ws_combo, False, False, False)
    hboxws.show()

    dialog.get_message_area().pack_start(hboxws, False, False, False)
    result = dialog.run()
    retval = None
    if result == Gtk.ResponseType.OK:
        model = ws_combo.get_model()
        retval = hostnames[0]['node_chef_id']
        if not ws_combo.get_active() == -1:
            retval = model[ws_combo.get_active()][1]
    dialog.destroy()
    return retval

def select_ou(title, text, uri_gcc, gcc_username, gcc_pwd_user):#, ous):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_icon_name('dialog-password')
    dialog.set_markup(text)

    hbosearch = Gtk.HBox()
    lblsearch = Gtk.Label(_('Pattern search'))
    lblsearch.set_visible(True)
    hbosearch.pack_start(lblsearch, False, False, 10)

    hboxou = Gtk.HBox()
    lblou = Gtk.Label(_('Select OU'))
    lblou.set_visible(True)
    hboxou.pack_start(lblou, False, False, 10)
    ou_store = Gtk.ListStore(str, str)
    

    ou_combo = Gtk.ComboBox.new_with_model(ou_store)
    renderer_text = Gtk.CellRendererText()
    ou_combo.pack_start(renderer_text, True)
    ou_combo.add_attribute(renderer_text, "text", 0)    

    search = Gtk.Entry()
    search.set_activates_default(True)
    search.show()
    hbosearch.pack_start(search, False, False, False)
    #hbosearch.show()
    

    search_btn = Gtk.Button()
    search_btn.set_label(_('Search'))
    search_btn.show()
    hbosearch.pack_start(search_btn, False, False, False)
    hbosearch.show()
    dialog.get_message_area().pack_start(hbosearch, False, False, False)
   
    search_btn.connect('clicked', search_ou, search, ou_combo, uri_gcc, gcc_username, gcc_pwd_user)#, ous)

    ou_combo.show()
    hboxou.pack_end(ou_combo, False, False, False)
    hboxou.show()

    dialog.get_message_area().pack_start(hboxou, False, False, False)
    result = dialog.run()
    retval = ''
    if result == Gtk.ResponseType.OK:
        model = ou_combo.get_model()
        #retval = ous[0][0]
        if not ou_combo.get_active() == -1:
            retval = model[ou_combo.get_active()][1]
    #else:
    #    retval = ous[0][0]
    dialog.destroy()
    return retval

def search_ws(widget, combo, hostnames):
    hostnames_search = hostnames
    text = widget.get_text()
    if len(text) >= 3:
        hostnames_search = []
        for base_ws  in hostnames:
            if text.lower() in base_ws['name'].lower():
                hostnames_search.append(base_ws)

    ws_store = Gtk.ListStore(str, str)
    for ws in hostnames_search:
        ws_store.append([ws['name'], ws['node_chef_id']])

    combo.set_model(ws_store)
    combo.show_all()


def search_ou(widget,search, combo, uri_gcc, gcc_username, gcc_pwd_user):#, ous):
    ous_search = []
    text = search.get_text()
    #if len(text) >= 3:
    ous_search = search_ou_by_text(uri_gcc, gcc_username, gcc_pwd_user, text)
        #for base_ou  in ous:
        #    if text.lower() in base_ou[1].lower():
        #        ous_search.append(base_ou)

    ou_store = Gtk.ListStore(str, str)
    for ou in ous_search:
        ou_store.append([ou[1], ou[0]])

    combo.set_model(ou_store)
    combo.show_all()

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
    

def message_box(title, text):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL)
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_markup(text)
    result = dialog.run()

    retval = 0
    if result == Gtk.ResponseType.OK:
        retval = 1

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
