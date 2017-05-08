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

import sys

from gecosws_config_assistant.view.ConnectWithGecosCCDialog import ConnectWithGecosCCDialog
from gecosws_config_assistant.view.GecosCCSetupProgressView import GecosCCSetupProgressView
from gecosws_config_assistant.view.CommonDialog import showerror_gtk, showwarning_gtk
from gecosws_config_assistant.view.CommonDialog import askyesno_gtk

from gecosws_config_assistant.util.GecosCC import GecosCC
from gecosws_config_assistant.util.Validation import Validation
from gecosws_config_assistant.util.Template import Template
from gecosws_config_assistant.util.CommandUtil import CommandUtil
from gecosws_config_assistant.util.SSLUtil import SSLUtil, SSL_R_CERTIFICATE_VERIFY_FAILED
from gecosws_config_assistant.util.GemUtil import GemUtil

from gecosws_config_assistant.dao.GecosAccessDataDAO import GecosAccessDataDAO
from gecosws_config_assistant.dao.WorkstationDataDAO import WorkstationDataDAO

from gecosws_config_assistant.firstboot_lib.firstbootconfig import get_data_file



import logging
import traceback
import os
import pwd
import grp
import subprocess
import base64
import json

import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')


class ConnectWithGecosCCController(object):
    '''
    Controller class for the "connect/disconnect with GECOS CC" functionality.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        self.view = None
        self.mainController = mainController 
        self.accessDataDao = GecosAccessDataDAO()
        self.workstationDataDao = WorkstationDataDAO()
        self.logger = logging.getLogger('ConnectWithGecosCCController')

        # List of GEMS required to run GECOS 
        self.necessary_gems = ['json', 'rest-client', 'activesupport', 'sqlite3', 'netaddr']

    def show(self, mainWindow):
        self.logger.debug('show - BEGIN')
        self.view = ConnectWithGecosCCDialog(mainWindow, self)

        gecosData = None
        if self.mainController.requirementsCheck.autoSetup.view is not None:
            gecosData = self.mainController.requirementsCheck.autoSetup.view.get_data()
            
        if gecosData is None:        
            gecosData = self.accessDataDao.load()
        
        self.view.set_gecos_access_data(gecosData)
        self.view.set_workstation_data(self.workstationDataDao.load())
        
        self.view.show()   
        self.logger.debug('show - END')
    
    def getStatus(self):
        return ((self.accessDataDao.load() is not None) 
                and (self.workstationDataDao.load() is not None))

    def hide(self):
        self.logger.debug("hide")
        self.mainController.showRequirementsCheckDialog()
    
    def _check_gecosConnectionParameters(self, gecosAccessData):
        self.logger.debug("_check_gecosConnectionParameters")
        # Validate Gecos access data
        if (gecosAccessData.get_url() is None or
            gecosAccessData.get_url().strip() == ''):
            self.logger.debug("Empty URL!")
            showerror_gtk(_("The URL field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                 None)
            self.view.focusUrlField()            
            return False

        if not Validation().isUrl(gecosAccessData.get_url()):
            self.logger.debug("Malformed URL!")
            showerror_gtk(_("Malformed URL in URL field!") + "\n" + _("Please double-check it."),
                 None)            
            self.view.focusUrlField()            
            return False

        if (gecosAccessData.get_login() is None or
            gecosAccessData.get_login().strip() == ''):
            self.logger.debug("Empty login!")
            showerror_gtk(_("The Username field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                 None)
            self.view.focusUsernameField()            
            return False

        if (gecosAccessData.get_password() is None or
            gecosAccessData.get_password().strip() == ''):
            self.logger.debug("Empty password!")
            showerror_gtk(_("The Password field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                 None)
            self.view.focusPasswordField()            
            return False

        if gecosAccessData.get_url().startswith('https://'):
            # Check server certificate
            sslUtil = SSLUtil()
            if not sslUtil.isServerCertificateTrusted(gecosAccessData.get_url()):
                if sslUtil.getUntrustedCertificateErrorCode(gecosAccessData.get_url()) == SSL_R_CERTIFICATE_VERIFY_FAILED :
                    # Error code SSL_R_CERTIFICATE_VERIFY_FAILED means that the certificate is not trusted
                    
                    errorcode = sslUtil.getUntrustedCertificateErrorCode( gecosAccessData.get_url() )
                    certificate = sslUtil.getServerCertificate(gecosAccessData.get_url())
                    info = sslUtil.getCertificateInfo(certificate)                

                    # Ask to the user if he want to trust this certificate
                    if info is not None:
                        if info.has_expired():
                            message = unicode(_("The certificate of this server is expired!"), 'utf-8')
                        else:
                            message = unicode(_("The certificate of this server is not trusted!"), 'utf-8')

                        response =  askyesno_gtk((message  + "\n" 
                            + unicode(_("Do you want to disable the SSL certificate verification?"), 'utf-8') + "\n" 
                            + "\n" 
                            + unicode(_("Subject:"), 'utf-8') + " " + (sslUtil.formatX509Name(info.get_subject())) + "\n" 
                            + unicode(_("Issuer:"), 'utf-8') + " " + (sslUtil.formatX509Name(info.get_issuer())) + "\n" 
                            + unicode(_("Serial Number:"), 'utf-8') + " " + str(info.get_serial_number()) + "\n" 
                            + unicode(_("Not before:"), 'utf-8') + " " + str(info.get_notBefore()) + " " + unicode(_("Not after:"), 'utf-8') + " " + str(info.get_notAfter()) + "\n" 
                            ), self.view, 'warning')
                            
                        if not response:
                            self.logger.debug("User don't want to add the HTTPS server certificate to the Trusted CA list!")
                            self.view.focusUrlField()            
                            return False                    
                            
                        else:
                            SSLUtil.disableSSLCertificatesVerification()                
                            
                else:
                    # Any other error code must be shown
                    errormsg = sslUtil.getUntrustedCertificateCause( gecosAccessData.get_url() )
                    self.logger.debug("Error connecting to HTTPS server: %s"%(errormsg))
                    showerror_gtk(_("Can't connect to GECOS CC!") + "\n" +  _("SSL ERROR:") + ' ' + errormsg,
                         None)
                    self.view.focusUrlField()
                    return False       
            
        gecosCC = GecosCC()
        if not gecosCC.validate_credentials(gecosAccessData):
            self.logger.debug("Bad access data!")
            showerror_gtk(_("Can't connect to GECOS CC!") + "\n" +  _("Please double-check all the data and your network setup."),
                 None)
            self.view.focusPasswordField()            
            return False
        
        return True

    def _check_workstation_data(self, workstationData, check_ou):
        self.logger.debug("_check_workstation_data")
        # Validate Gecos workstation data
        if (workstationData.get_name() is None or
            workstationData.get_name().strip() == ''):
            self.logger.debug("Empty Node name!")
            showerror_gtk(_("The GECOS workstation name field is empty!") + "\n" + _("Please fill all the mandatory fields."),
                 self.view)
            self.view.focusWorkstationNameField()            
            return False     
        
        
        if workstationData.get_node_name() is None or workstationData.get_node_name().strip() == '':
            # Computer name must be unique
            gecosCC = GecosCC()
            computer_names = gecosCC.get_computer_names(self.view.get_gecos_access_data())
            is_in_computer_names = False
            for cn in computer_names:
                if cn['name'] == workstationData.get_name():
                    is_in_computer_names = True
                    break
                    
            
            if is_in_computer_names:  
                self.logger.debug("Existent node name!")
                showerror_gtk(_("The GECOS workstation name already exist!") + "\n" + _("Please choose a different name."),
                     self.view)
                self.view.focusWorkstationNameField()            
                return False     
                    
            # Create a new node_name
            node_name = self.accessDataDao.calculate_workstation_node_name()
            workstationData.set_node_name(node_name)

        if check_ou:
            if (workstationData.get_ou() is None or
                workstationData.get_ou().strip() == ''):
                self.logger.debug("Empty OU name!")
                showerror_gtk(_("You must select an OU!") + "\n" + _("Please fill all the mandatory fields."),
                     None)
                self.view.focusSeachFilterField()            
                return False   
            else:
                self.logger.debug("Selected OU: %s"%(workstationData.get_ou()))
        
        return True     

    def _remove_file(self, filename):
        try:
            if os.path.isfile(filename):
                os.remove(filename)
        except:
            self.logger.error("Error removing %s file"%(filename))
            self.logger.error(str(traceback.format_exc()))
            return False    
        
        return True
    
    
    def _save_secure_file(self, filename, filecontent):
        try:
            # Check if directory exists
            Template().check_directory_strutcture(os.path.dirname(filename))
            
            # Create empty file
            fd = open(filename, 'w')
            fd.truncate()
            fd.close()

            # Check the owner and permissions
            stat_info = os.stat(filename)
            uid = stat_info.st_uid
            gid = stat_info.st_gid

            current_usr = pwd.getpwuid(uid)[0]
            current_grp = grp.getgrgid(gid)[0]
            
            # Set the user to root
            if current_usr != 'root':
                uid = pwd.getpwnam('root').pw_uid
                if uid is None:
                    self.logger.error('Can not find user to be used as owner: ' + 'root')
                else:
                    os.chown(filename, uid, gid)  
                
            if current_grp != 'root':
                gid = grp.getgrnam('root').gr_gid
                if gid is None:
                    self.logger.error('Can not find group to be used as owner: ' + 'root')
                else:
                    os.chown(filename, uid, gid)  
                
            # Set permissions to 00600
            mode = 00600
            m = stat_info.st_mode & 00777
            if m != mode:
                os.chmod(filename, mode)

            # Write the content
            fd = open(filename, 'w')
            fd.write(filecontent)
            fd.close()

            
        except:
            self.logger.error("Error creating %s file"%(filename))
            self.logger.error(str(traceback.format_exc()))
            return False        
        
        
        return True
    
    def _execute_command(self, cmd, my_env={}):
        commandUtil = CommandUtil()
        return commandUtil.execute_command(cmd, my_env)
    
    def _clean_connection_files_on_error(self):
        self.logger.debug("_clean_connection_files_on_error")
        self._remove_file('/etc/chef/validation.pem')
        self._remove_file('/etc/chef/client.pem')        
        self._remove_file('/etc/chef/client.rb')        
        self._remove_file('/etc/chef/knife.rb')        
        self._remove_file('/etc/chef.control')        
        self._remove_file('/etc/gcc.control')        


    def _clean_disconnection_files_on_error(self):
        self.logger.debug("_clean_disconnection_files_on_error")
        self._remove_file('/etc/chef/validation.pem')
        
    
    def connect(self):
        self.logger.info("Connect to Gecos CC")

        self.processView = GecosCCSetupProgressView(self, self.mainController.window)
        self.processView.setLinkToChefLabel(_('Link to Chef'))
        self.processView.setRegisterInGecosLabel(_('Register in GECOS CC'))
        self.processView.show()
        
        # Check parameters
        self.logger.debug("Check parameters")
        self.processView.setCheckGecosCredentialsStatus(_('IN PROCESS'))
        
        if self.view.get_gecos_access_data() is None:
            self.logger.error("Strange error: GECOS access data is None")
            self.processView.setCheckGecosCredentialsStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            return False

        if self.view.get_workstation_data() is None:
            self.logger.error("Strange error: workstation data is None")
            self.processView.setCheckGecosCredentialsStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            return False

        
        if not self._check_gecosConnectionParameters(self.view.get_gecos_access_data()):
            self.processView.setCheckGecosCredentialsStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            return False
        
        self.processView.setCheckGecosCredentialsStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setCheckWorkstationDataStatus(_('IN PROCESS'))
        
        if not self._check_workstation_data(self.view.get_workstation_data(), True):
            self.processView.setCheckWorkstationDataStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            return False

        self.processView.setCheckWorkstationDataStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setChefCertificateRetrievalStatus(_('IN PROCESS'))

        # Save workstation data
        self.workstationDataDao.save(self.view.get_workstation_data())
        workstationData = self.view.get_workstation_data()

        
        # Get client.pem from server
        self.logger.debug("Get client.pem from server")
        gecosCC = GecosCC()
        
        if gecosCC.is_registered_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name()):
            # re-register
            client_pem = gecosCC.reregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
        else:
            # register
            client_pem = gecosCC.register_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            
        # Check the client_pem data
        if client_pem is False:
            self.processView.setChefCertificateRetrievalStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("There was an error while getting the client certificate"),
                 self.view)
            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            self._clean_connection_files_on_error()
            return False        
        
        # Save Chef client certificate in a PEM file
        if not self._save_secure_file('/etc/chef/client.pem', client_pem):
            self.processView.setChefCertificateRetrievalStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("There was an error while saving the client certificate"),
                 self.view)
            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            self._clean_connection_files_on_error()
            return False

        # Get autoconf data
        conf = gecosCC.get_json_autoconf(self.view.get_gecos_access_data())
            
        # Check configured GEMs repo
        if (conf is not None 
            and conf.has_key("gem_repo")):
            gem_repo = conf['gem_repo']
            if not gem_repo.endswith('/'):
                gem_repo = gem_repo + '/'
              
            # Check if GEMs repository is http://rubygems.org/
            if gem_repo == 'http://rubygems.org/':
                # Chef 12 warns about using 'http://rubygems.org/' and recommends 
                # using 'https://rubygems.org/' for security
                gem_repo = 'https://rubygems.org/'
                self.logger.debug("Switched from http://rubygems.org/ to https://rubygems.org/")

            # Check if GEMs repository is a HTTPS site
            if gem_repo.startswith('https://'):
                # Check server certificate
                sslUtil = SSLUtil()
                if not sslUtil.isServerCertificateTrusted(gem_repo):
                    if sslUtil.getUntrustedCertificateErrorCode(gem_repo) == SSL_R_CERTIFICATE_VERIFY_FAILED :
                        # Error code SSL_R_CERTIFICATE_VERIFY_FAILED means that the certificate is not trusted
                        
                        errorcode = sslUtil.getUntrustedCertificateErrorCode( gem_repo )
                        certificate = sslUtil.getServerCertificate(gem_repo)
                        info = sslUtil.getCertificateInfo(certificate)                

                        # Ask to the user if he want to trust this certificate
                        if info is not None:
                            if info.has_expired():
                                message = unicode(_("The certificate of this server is expired!"), 'utf-8')
                            else:
                                message = unicode(_("The certificate of this server is not trusted!"), 'utf-8')


                            response =  askyesno_gtk((message  + "\n" 
                                + unicode(_("Do you want to disable the SSL certificate verification?"), 'utf-8') + "\n" 
                                + "\n" 
                                + unicode(_("Subject:"), 'utf-8') + " " + (sslUtil.formatX509Name(info.get_subject())) + "\n" 
                                + unicode(_("Issuer:"), 'utf-8') + " " + (sslUtil.formatX509Name(info.get_issuer())) + "\n" 
                                + unicode(_("Serial Number:"), 'utf-8') + " " + str(info.get_serial_number()) + "\n" 
                                + unicode(_("Not before:"), 'utf-8') + " " + str(info.get_notBefore()) + " " + unicode(_("Not after:"), 'utf-8') + " " + str(info.get_notAfter()) + "\n" 
                                ), self.view, 'warning')
                                
                            if not response:
                                self.logger.debug("User don't want to add the HTTPS server certificate to the Trusted CA list!")
                                self.processView.setChefCertificateRetrievalStatus(_('ERROR'))
                                self.processView.enableAcceptButton()
                                gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
                                self._clean_connection_files_on_error()
                                return False                 
                                
                            else:
                                SSLUtil.disableSSLCertificatesVerification()
    
                    else:
                        # Any other error code must be shown
                        errormsg = sslUtil.getUntrustedCertificateCause( gem_repo )
                        self.logger.debug("Error connecting to HTTPS server: %s"%(errormsg))
                        self.processView.setChefCertificateRetrievalStatus(_('ERROR'))
                        self.processView.enableAcceptButton()
                        showerror_gtk(_("Can't connect to GEMs repository!") + "\n" +  _("SSL ERROR:") + ' ' + errormsg,
                             None)
                        gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
                        self._clean_connection_files_on_error()
                        return False       


            gemUtil = GemUtil()
            gemUtil.remove_all_gem_sources()
            gemUtil.clear_cache_gem_sources()
            if not gemUtil.add_gem_only_one_source(gem_repo):
                # Error adding GEMs repository
                self.processView.setChefCertificateRetrievalStatus(_('ERROR'))
                self.processView.enableAcceptButton()
                showerror_gtk(_("There was an error while adding the GEMs repository:" + "\n" + gem_repo),
                    self.view)
                gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
                self._clean_connection_files_on_error()
                return False

        # Check installed GEMs
        for gem_name in self.necessary_gems:
            if not gemUtil.is_gem_intalled(gem_name):
                if not gemUtil.install_gem(gem_name):
                    # Error installing a GEM
                    self.processView.setChefCertificateRetrievalStatus(_('ERROR'))
                    self.processView.enableAcceptButton()
                    showerror_gtk(_("There was an error while installing a required GEM:" + " " + gem_name),
                         self.view)
                    gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
                    self._clean_connection_files_on_error()
                    return False



        self.processView.setChefCertificateRetrievalStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setLinkToChefStatus(_('IN PROCESS'))
        
        # Link to Chef
        self.logger.debug("Link to Chef")
        
        # if a previous /etc/gcc.control file exist delete it
        self._remove_file('/etc/gcc.control')

        self.logger.debug("- Create /etc/chef/client.rb")
        
        chef_admin_name = self.view.get_gecos_access_data().get_login()
        chef_url = self.view.get_gecos_access_data().get_url()
        chef_url = chef_url.split('//')[1].split(':')[0]
        chef_url = "https://" + chef_url + '/'        
        
        if (conf is not None 
            and conf.has_key("chef")
            and conf["chef"].has_key("chef_server_uri")):
            chef_url = conf["chef"]["chef_server_uri"]
            self.logger.debug("chef_url retrieved from GECOS auto conf")        

        if (conf is not None 
            and conf.has_key("chef")
            and conf["chef"].has_key("chef_admin_name")):
            chef_admin_name = conf["chef"]["chef_admin_name"]
            self.logger.debug("chef_admin_name retrieved from GECOS auto conf")               

        # Check Chef HTTPS certificate
        if chef_url.startswith('https://'):
            # Check server certificate
            sslUtil = SSLUtil()
            if not sslUtil.isServerCertificateTrusted(chef_url):
                if sslUtil.getUntrustedCertificateErrorCode(chef_url) == SSL_R_CERTIFICATE_VERIFY_FAILED :
                    # Error code SSL_R_CERTIFICATE_VERIFY_FAILED means that the certificate is not trusted
                    
                    errorcode = sslUtil.getUntrustedCertificateErrorCode( chef_url )
                    certificate = sslUtil.getServerCertificate(chef_url)
                    info = sslUtil.getCertificateInfo(certificate)                

                    # Ask to the user if he want to trust this certificate
                    if info is not None:
                        if info.has_expired():
                            message = unicode(_("The certificate of this server is expired!"), 'utf-8')
                        else:
                            message = unicode(_("The certificate of this server is not trusted!"), 'utf-8')

                        response =  askyesno_gtk((message  + "\n" 
                            + unicode(_("Do you want to disable the SSL certificate verification?"), 'utf-8') + "\n" 
                            + "\n" 
                            + unicode(_("Subject:"), 'utf-8') + " " + (sslUtil.formatX509Name(info.get_subject())) + "\n" 
                            + unicode(_("Issuer:"), 'utf-8') + " " + (sslUtil.formatX509Name(info.get_issuer())) + "\n" 
                            + unicode(_("Serial Number:"), 'utf-8') + " " + str(info.get_serial_number()) + "\n" 
                            + unicode(_("Not before:"), 'utf-8') + " " + str(info.get_notBefore()) + " " + unicode(_("Not after:"), 'utf-8') + " " + str(info.get_notAfter()) + "\n" 
                            ), self.view, 'warning')
                            
                        if not response:
                            self.logger.debug("User don't want to add the HTTPS server certificate to the Trusted CA list!")
                            self.processView.setLinkToChefStatus(_('ERROR'))
                            self.processView.enableAcceptButton()
                            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
                            self._clean_connection_files_on_error()
                            return False                 
                            
                        else:
                            SSLUtil.disableSSLCertificatesVerification()
                            
                else:
                    # Any other error code must be shown
                    errormsg = sslUtil.getUntrustedCertificateCause( chef_url )
                    self.logger.debug("Error connecting to HTTPS server: %s"%(errormsg))
                    self.processView.setLinkToChefStatus(_('ERROR'))
                    self.processView.enableAcceptButton()
                    showerror_gtk(_("Can't connect to Chef Server!") + "\n" +  _("SSL ERROR:") + ' ' + errormsg,
                         None)
                    gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
                    self._clean_connection_files_on_error()
                    return False       

        template = Template()
        template.source = get_data_file('templates/client.rb')
        template.destination = '/etc/chef/client.rb'
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00644
        
        ssl_certificate_verification = ':verify_peer'
        if not SSLUtil.isSSLCertificatesVerificationEnabled():
            ssl_certificate_verification = ':verify_none'
        
        template.variables = { 'chef_url':  chef_url,
                              'chef_node_name':  workstationData.get_node_name(),
                              'ssl_certificate_verification': ssl_certificate_verification}
        
        if not template.save():
            self.processView.setLinkToChefStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't create/modify /etc/chef/client.rb file"),
                 None)
            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            self._clean_connection_files_on_error()
            return False            
        
      

        self.logger.debug('- Linking the chef server ')
        env = {'LANG': 'es_ES.UTF-8', 'LC_ALL': 'es_ES.UTF-8', 'HOME': os.environ['HOME']}
        result = self._execute_command('chef-client -j /usr/share/gecosws-config-assistant/base.json', env)
        self.logger.debug('chef-client -j /usr/share/gecosws-config-assistant/base.json --> %s'%(result))
        if not result:
            self.processView.setLinkToChefStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't link to chef server!"),
                 self.view)
            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            self._clean_connection_files_on_error()
            return False 
        
        self.logger.debug('- Start chef client service ')
        self._execute_command('service chef-client start')
        
        self.logger.debug('- Create a control file ')
        template = Template()
        template.source = get_data_file('templates/chef.control')
        template.destination = '/etc/chef.control'
        template.owner = 'root'
        template.group = 'root'
        template.mode = 00755
        template.variables = { 'chef_url':  chef_url,
                              'chef_admin_name':  chef_admin_name,
                              'chef_node_name':  workstationData.get_node_name()}                
        
        if not template.save():
            self.processView.setLinkToChefStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't create/modify /etc/chef.control file"),
                 self.view)
            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            self._clean_connection_files_on_error()
            return False    
    
        
        
        self.processView.setLinkToChefStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setRegisterInGecosStatus(_('IN PROCESS'))
        
        # Register from GECOS Control Center
        self.logger.debug('- register in GECOS CC ')
        ou = gecosCC.search_ou_by_text(self.view.get_gecos_access_data(), 
                                  workstationData.get_ou())
        
        if not gecosCC.register_computer(self.view.get_gecos_access_data(), 
                workstationData.get_node_name(), ou[0][0]):
            self.processView.setRegisterInGecosStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't register the computer in GECOS CC"),
                 self.view)
            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            self._clean_connection_files_on_error()
            return False          
        

        if not self.accessDataDao.save(self.view.get_gecos_access_data()):
            self.processView.setRegisterInGecosStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't save /etc/gcc.control file"),
                 self.view)
            gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), workstationData.get_node_name())
            self._clean_connection_files_on_error()
            return False    
        
        self.processView.setRegisterInGecosStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setCleanStatus(_('IN PROCESS'))
        
        # Clean setup files
        self._remove_file('/etc/chef/validation.pem')
        
        self.processView.setCleanStatus(_('DONE'))
        self.processView.addProgressFraction(0.2)
        
        self.processView.enableAcceptButton()
        
        return True

        
    def disconnect(self):
        self.logger.info("Disconnect from Gecos CC")
        
        if local_disconn_checkbox:
            # local disconnection
            self.logger.debug("Executing a local disconnection")

            self._remove_file('/etc/gcc.control')
            self._remove_file('/etc/chef.control')
            self._remove_file('/etc/chef/client.rb')
            self._remove_file('/etc/chef/client.pem')
            self._remove_file('/etc/chef/validation.pem')
            self._remove_file('/etc/chef/knife.rb')

            self.logger.debug("DONE.")
            showwarning_gtk(_("Local disconnection done!"), self)
        else:
        self.processView = GecosCCSetupProgressView(self, self.mainController.window)
        self.processView.setLinkToChefLabel(_('Unlink from Chef'))
        self.processView.setRegisterInGecosLabel(_('Unregister from GECOS CC'))
        self.processView.show()
        
        # Check parameters
        self.logger.debug("Check parameters")
        self.processView.setCheckGecosCredentialsStatus(_('IN PROCESS'))
        if not self._check_gecosConnectionParameters(self.view.get_gecos_access_data()):
            self.processView.setCheckGecosCredentialsStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            return False
        
        self.processView.setCheckGecosCredentialsStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setCheckWorkstationDataStatus(_('IN PROCESS'))
        
        if not self._check_workstation_data(self.view.get_workstation_data(), False):
            self.processView.setCheckWorkstationDataStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            return False

        self.processView.setCheckWorkstationDataStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setChefCertificateRetrievalStatus(_('IN PROCESS'))

        # Save workstation data
        self.workstationDataDao.save(self.view.get_workstation_data())

        # We don't need any certificate to unlink from Chef or GECOS CC

        self.processView.setChefCertificateRetrievalStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setLinkToChefStatus(_('IN PROCESS'))

        gecosCC = GecosCC()
        
        # Unregister from GECOS Control Center
        self.logger.debug("Unregister computer")

        workstationData = self.view.get_workstation_data()
        if not gecosCC.unregister_computer(self.view.get_gecos_access_data(), 
                workstationData.get_node_name()):
            self.processView.setRegisterInGecosStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't unregister the computer from GECOS CC"),
                 None)
            self._clean_disconnection_files_on_error()
            return False          

        
        # Unlink from Chef
        self.logger.debug("Unlink from Chef")
        
        self.logger.debug("- Remove control file")
        if not self._remove_file('/etc/chef.control'):
            self.processView.setLinkToChefStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't remove /etc/chef.control file"),
                 self.view)
            self._clean_disconnection_files_on_error()
            return False 

        self.logger.debug("- Remove client.pem")
        if not self._remove_file('/etc/chef/client.pem'):
            self.processView.setLinkToChefStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't remove /etc/chef/client.pem file"),
                 self.view)
            self._clean_disconnection_files_on_error()
            return False 


        self.logger.debug('- Deleting node ' + workstationData.get_node_name())
        if not gecosCC.unregister_chef_node(self.view.get_gecos_access_data(), 
                workstationData.get_node_name()):
            self.processView.setLinkToChefStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't delete Chef node"),
                 self.view)
            self._clean_disconnection_files_on_error()
            return False 
        
        self.logger.debug("- Remove chef-client-wrapper")
        if not self._remove_file('/usr/bin/chef-client-wrapper'):
            self.processView.setLinkToChefStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't remove /usr/bin/chef-client-wrapper file"),
                 self.view)
            self._clean_disconnection_files_on_error()
            return False         

        self.logger.debug('- Stop chef client service ')
        self._execute_command('service chef-client stop')
        
        
        self.processView.setLinkToChefStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setRegisterInGecosStatus(_('IN PROCESS'))
        
        if not self.accessDataDao.delete(self.view.get_gecos_access_data()):
            self.processView.setRegisterInGecosStatus(_('ERROR'))
            self.processView.enableAcceptButton()
            showerror_gtk(_("Can't remove /etc/gcc.control file"),
                 self.view)
            self._clean_disconnection_files_on_error()
            return False    
        
        self.processView.setRegisterInGecosStatus(_('DONE'))
        self.processView.addProgressFraction(0.16)
        
        self.processView.setCleanStatus(_('IN PROCESS'))
        
        # Clean setup files
        self._remove_file('/etc/chef/validation.pem')
        self._remove_file('/etc/chef/knife.rb')
        
        self.processView.setCleanStatus(_('DONE'))
        self.processView.addProgressFraction(0.2)
        
        self.processView.enableAcceptButton()

        return True
        
        

    def patternSearch(self, searchText):
        self.logger.debug("patternSearch")
        
        if not self._check_gecosConnectionParameters(self.view.get_gecos_access_data()):
            return False
        
        
        gecosCC = GecosCC()
        result = gecosCC.search_ou_by_text(self.view.get_gecos_access_data(), searchText)
        if not isinstance(result, (list, tuple)):
            self.logger.debug("Can't get OUs from GECOS CC")
            showerror_gtk(_("Can't get OUs from GECOS Control Center"),
                 self.view)
            self.view.focusPasswordField()            
            return False        
        
        return result 
        

    def proccess_dialog_accept(self, error_status):
        self.logger.debug("proccess_dialog_accept")
        self.processView.hide()
        if not error_status:
            self.hide()
