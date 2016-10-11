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

from gecosws_config_assistant.dao.GecosAccessDataDAO import GecosAccessDataDAO

import sys
import socket


if 'check' in sys.argv:
    # Mock view classes for testing purposses
    print "==> Loading mocks..."
    from gecosws_config_assistant.view.ViewMocks import showerror_gtk, askyesno_gtk, AutoSetupDialog, ADSetupDataElemView, ConnectWithGecosCCDialog
    from gecosws_config_assistant.util.UtilMocks import GecosCC
else:
    # Use real view classes
    from gecosws_config_assistant.view.AutoSetupDialog import AutoSetupDialog
    from gecosws_config_assistant.view.ADSetupDataElemView import ADSetupDataElemView
    from gecosws_config_assistant.view.CommonDialog import showerror_gtk, askyesno_gtk
    from gecosws_config_assistant.util.GecosCC import GecosCC
    from gecosws_config_assistant.view.ConnectWithGecosCCDialog import ConnectWithGecosCCDialog 


from gecosws_config_assistant.util.Validation import Validation
from gecosws_config_assistant.util.SSLUtil import SSLUtil, SSL_R_CERTIFICATE_VERIFY_FAILED


import logging
import traceback
import subprocess 


import gettext
from gettext import gettext as _
gettext.textdomain('gecosws-config-assistant')

class AutoSetupController(object):
    '''
    Controller class for the auto setup functionality.
    '''


    def __init__(self, mainController):
        '''
        Constructor
        '''
        self.view = None
        self.processView = None
        self.mainWindowController = mainController
        self.dao = GecosAccessDataDAO()
        
        self.logger = logging.getLogger('AutoSetupController')
        
        self.auto_setup_success = False
        self.conf = False

    def show(self, mainWindow):
        self.logger.debug('show - BEGIN')
        data = None
        if self.view is not None:
            data = self.view.get_data()
       
        self.view = AutoSetupDialog(mainWindow, self)
        
        if data is None:
            self.view.set_data(self.dao.load())
        else:
            self.view.set_data(data)
        
        self.view.show()   
        self.logger.debug('show - END')


    def cancel(self):
        self.logger.debug("cancel")
        self.mainWindowController.showRequirementsCheckDialog()
    
    def accept(self):
        self.logger.debug("accept")
        self.cancel()


    def _setup_validate_data(self, gecosAccessData):
        self.logger.debug("_setup_validate_data")
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

        if gecosAccessData.get_url().startswith('https://'):
            # Check server certificate
            sslUtil = SSLUtil()
            if not sslUtil.isServerCertificateTrusted(gecosAccessData.get_url()):
                if sslUtil.getUntrustedCertificateErrorCode(gecosAccessData.get_url()) == SSL_R_CERTIFICATE_VERIFY_FAILED :
                    # Error code SSL_R_CERTIFICATE_VERIFY_FAILED means that the certificate is not trusted
                    
                    errorcode = sslUtil.getUntrustedCertificateErrorCode( gecosAccessData.get_url() )
                    certificate = sslUtil.getServerCertificate(gecosAccessData.get_url())
                    info = sslUtil.getCertificateInfo(certificate)                

                    # Check if the certificate is expired
                    if info is not None and info.has_expired():
                        self.logger.debug("Server HTTPS certificate is expired!")
                        showerror_gtk(_("Can't connect to GECOS CC!") + "\n" +  _("The server HTTPS certificate is expired!"),
                             None)
                        self.view.focusUrlField()            
                        return False                    
                    
                    # Ask to the user if he want to trust this certificate
                    if info is not None:
                        response =  askyesno_gtk((_("The certificate of this server is not trusted!")  + "\n" 
                            + _("Do you wan't to add it to the trusted certificates list?") + "\n" 
                            + "\n" 
                            + _("Subject:") + " " + (sslUtil.formatX509Name(info.get_subject())) + "\n" 
                            + _("Issuer:") + " " + (sslUtil.formatX509Name(info.get_issuer())) + "\n" 
                            + _("Serial Number:") + " " + str(info.get_serial_number()) + "\n" 
                            + _("Not before:") + " " + str(info.get_notBefore()) + " " + _("Not after:") + " " + str(info.get_notAfter()) + "\n" 
                            ), self.view, 'warning')
                            
                        if not response:
                            self.logger.debug("User don'w want to add the HTTPS server certificate to the Trusted CA list!")
                            self.view.focusUrlField()            
                            return False                    
                            
                        else:
                            sslUtil.addCertificateToTrustedCAs(certificate, True)
                            
                            # Test again
                            if not sslUtil.isServerCertificateTrusted(gecosAccessData.get_url()):
                                # Trusted certificates produce connection errors
                                # due to many things. For example a bad name.
                                errormsg = sslUtil.getUntrustedCertificateCause( gecosAccessData.get_url() )
                                self.logger.debug("Error connecting to HTTPS server: %s"%(errormsg))
                                showerror_gtk(_("Can't connect to GECOS CC!") + "\n" +  _("SSL ERROR:") + ' ' + errormsg,
                                     None)
                                self.view.focusUrlField()            
                                return False                    
                            
                else:
                    # Any other error code must be shown
                    errormsg = sslUtil.getUntrustedCertificateCause( gecosAccessData.get_url() )
                    self.logger.debug("Error connecting to HTTPS server: %s"%(errormsg))
                    showerror_gtk(_("Can't connect to GECOS CC!") + "\n" +  _("SSL ERROR:") + ' ' + errormsg,
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

        gecosCC = GecosCC()
        if not gecosCC.validate_credentials(gecosAccessData):
            self.logger.debug("Bad access data!")
            showerror_gtk(_("Can't connect to GECOS CC!") + "\n" +  _("Please double-check all the data and your network setup."),
                 None)
            self.view.focusPasswordField()            
            return False
        
        return True

            

    def setup(self):
        self.logger.debug("setup")
        self.auto_setup_success = False
        gecosAccessData = self.view.get_data()
        
        # Validate Gecos access data
        if not self._setup_validate_data(gecosAccessData):
            return False


        # Show process view

        # Get auto setup JSON
        self.view.setAutoSetupDataLoadStatus(_('Please wait'))
        self.conf = False
        gecosCC = GecosCC()
        try:
            self.conf = gecosCC.get_json_autoconf(gecosAccessData)
        except:
            self.logger.error('Error loading auto setup data from GECOS')
            self.logger.error(str(traceback.format_exc()))
            
        if not self.conf:
            self.view.setAutoSetupDataLoadStatus(_('Error getting data'))
            showerror_gtk(_("Can't read auto setup configuration data from GECOS Control Center!"),
                 self.processView)            
            return False
            
        
        self.view.setAutoSetupDataLoadStatus(_('Success getting data from GECOS server'))
        
        # Auto setup success
        self.auto_setup_success = True
        
        return True

    def get_conf(self):
        return self.conf
    