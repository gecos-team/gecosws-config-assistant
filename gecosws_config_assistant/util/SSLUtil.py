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

import re
import logging
import requests
import traceback
import ssl
import os
from socket import socket
from OpenSSL import crypto
from pyasn1.codec.ber import decoder
from pyasn1_modules.rfc2459 import AuthorityInfoAccessSyntax, id_ad_caIssuers
import requests
import codecs

from gecosws_config_assistant.util.CommandUtil import CommandUtil

class SSLUtil(object):
    '''
    Utility class to work with SSL certificates.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('SSLUtil')
        self.timeout = 120

    def isServerCertificateTrusted(self, url):
        if url is None:
            return False
        
        # Check credentials
        try:
            r = requests.get(url, verify='/etc/ssl/certs/ca-certificates.crt', timeout=self.timeout)
            return True            
            
        except requests.exceptions.SSLError:
            self.logger.debug('Certifcate not trusted in URL: %s'%(url))
            
        except Exception:
            self.logger.warn('Error connecting to server: %s'%(url))
            self.logger.warn(str(traceback.format_exc()))
            
        return False    
        

    def getServerCertificate(self, url):
        if url is None:
            return None
        
        server_port = 443
        server_ip = ''
        if not url.startswith('https://'):
            return None
        else:
            url = url[8:]
            slashpos = url.find('/')
            if slashpos > 0:
                url = url[:slashpos]
            
            colonpos = url.find(':')
            
            if colonpos > 0:
                server_ip = url[:colonpos]
                server_port = int(url[(colonpos+1):])
            else:
                server_ip = url
            
        try:            
            self.logger.debug('server_ip: %s  server_port: %s'%(server_ip, server_port))
            s = socket()
            s.settimeout(self.timeout)
            c = ssl.wrap_socket(s,cert_reqs=ssl.CERT_NONE)
            c.connect((server_ip, server_port))
            
            return c.getpeercert(True)
            
        except Exception:
            self.logger.warn('Error connecting to server: %s'%(url))
            self.logger.warn(str(traceback.format_exc()))
            
        return None    
                    
    def isPEM(self, certificate):
        return (certificate.find('-----BEGIN CERTIFICATE-----') >= 0)
        
    def isSelfSigned(self, certificate_info):
        return (certificate_info.get_issuer() == certificate_info.get_subject())
        
    def getCertificateInfo(self, certificate):
        if certificate is None:
            return False
        
        filetype = crypto.FILETYPE_ASN1
        if self.isPEM(certificate):
            filetype = crypto.FILETYPE_PEM
            
        cert = crypto.load_certificate(crypto.FILETYPE_ASN1, certificate)
            
        return cert

    def getIssuerCertificateURL(self, certificate_info):
        url = None
        
        if certificate_info is None:
            return None
            
        if certificate_info.get_extension_count() <= 0:
            return None
           
        try:
            for i in range(0, certificate_info.get_extension_count()):
                ext = certificate_info.get_extension(i)
                if 'authorityInfoAccess' == ext.get_short_name():
                    data = decoder.decode(ext.get_data(), asn1Spec=AuthorityInfoAccessSyntax())
                    for authorityInfoAccessSyntax in data:
                        for i in range(len(authorityInfoAccessSyntax)):
                            accessDescription = authorityInfoAccessSyntax.getComponentByPosition(i)
                            if id_ad_caIssuers == accessDescription.getComponentByName('accessMethod'):
                                url = unicode(accessDescription.getComponentByName('accessLocation').getComponentByName('uniformResourceIdentifier'))
                                break
        except:
            self.logger.warn('Error trying to get issuer certificate URL from cetificate info!')
            self.logger.warn(str(traceback.format_exc()))
            
        return url
        
    def getCertificateFromURL(self, url):
        if url is None:
            return None

        certificate = None
        r = requests.get(url, verify=None, timeout=self.timeout)
        if r.ok:
            certificate = r.content                
        
        return certificate
        
    def addCertificateToTrustedCAs(self, certificate):
        if certificate is None:
            return
            
        if not os.path.isdir('/usr/share/ca-certificates/'):
            raise Exception('There is no /usr/share/ca-certificates/ directory')
            
        if not os.path.isfile('/etc/ca-certificates.conf'):
            raise Exception('There is no /etc/ca-certificates.conf file')
            
        if not os.path.isdir('/usr/share/ca-certificates/gecos'):
            os.mkdir('/usr/share/ca-certificates/gecos') 
        
        info = self.getCertificateInfo(certificate)
        filename = 'unknown'
        if info.get_subject().commonName is not None:
            filename = ("%s.crt"%(info.get_subject().commonName.lower())).replace('.', '_')
            
        if not self.isSelfSigned(info):
            # Is not a self signed certificate
            # We must get the Issuer CA certificate
            url = self.getIssuerCertificateURL(info)
            if url is None:
                raise Exception('Can\'t find issuer CA certificate URL!')
            
            certificate = self.getCertificateFromURL(url)
            filename = os.path.basename(url)     
            info = self.getCertificateInfo(certificate)

            if self.getIssuerCertificateURL(info) is not None:
                # Recursively add certificate to trusted CA
                self.addCertificateToTrustedCAs(certificate)
        
        # Write PEM certificate into /usr/share/ca-certificates/gecos/<certificate CN>.crt
        fd = open('/usr/share/ca-certificates/gecos/%s'%(filename), 'w')
        fd.write(self.convertDERcertificateToPEM(certificate))
        fd.close()
        
        # Check if there is a line for this certificate in /etc/ca-certificates.conf
        fd = codecs.open('/etc/ca-certificates.conf', 'r', encoding='utf-8')
        ca_certificates_conf = fd.read()
        fd.close()
        
        found = False
        ca_certificates = []
        for line in ca_certificates_conf.split('\n'):
            if line.startswith(u'gecos/%s'%(filename)):
                # The certificate already existed
                found = True
                
            if not line.startswith(u'!gecos/%s'%(filename)) and len(line.strip()) > 0:
                # Skip the deleted certificate
                ca_certificates.append(line)
        
        if not found:
            ca_certificates.append(u'gecos/%s'%(filename))
            ca_certificates.append(u'')
            ca_certificates_conf = '\n'.join(ca_certificates)
        
            # Overwrite the  /etc/ca-certificates.conf file
            fd = codecs.open('/etc/ca-certificates.conf', 'w', encoding='utf-8')
            fd.write(ca_certificates_conf)
            fd.close()            
        
            # Run update-ca-certificates
            commandUtil = CommandUtil()
            commandUtil.execute_command('/usr/sbin/update-ca-certificates')
        
    def removeCertificateFromTrustedCAs(self, certificate):
        if certificate is None:
            return
            
        if not os.path.isdir('/usr/share/ca-certificates/'):
            raise Exception('There is no /usr/share/ca-certificates/ directory')
            
        if not os.path.isfile('/etc/ca-certificates.conf'):
            raise Exception('There is no /etc/ca-certificates.conf file')
            
        if not os.path.isdir('/usr/share/ca-certificates/gecos'):
            # There are no certificates to remove
            return
        
        # Check if there is a line for this certificate in /etc/ca-certificates.conf
        info = self.getCertificateInfo(certificate)        
        filename = 'unknown'
        if info.get_subject().commonName is not None:        
            filename = ("%s.crt"%(info.get_subject().commonName.lower())).replace('.', '_')
        
        if not self.isSelfSigned(info):
            # Is not a self signed certificate
            # We must get the Issuer CA certificate
            url = self.getIssuerCertificateURL(info)
            if url is None:
                raise Exception('Can\'t find issuer CA certificate URL!')
            filename = os.path.basename(url)      
        
        
        fd = codecs.open('/etc/ca-certificates.conf', 'r', encoding='utf-8')
        ca_certificates_conf = fd.read()
        fd.close()
        
        found = False
        ca_certificates = []
        for line in ca_certificates_conf.split('\n'):
            if line.startswith(u'gecos/%s'%(filename)):
                # The certificate already exist
                found = True
                
            elif len(line.strip()) > 0:
                ca_certificates.append(line)
        
        if found:
            ca_certificates.append(u'!gecos/%s'%(filename))
            ca_certificates.append(u'')
            ca_certificates_conf = '\n'.join(ca_certificates)
      
        
            # Overwrite the  /etc/ca-certificates.conf file
            fd = codecs.open('/etc/ca-certificates.conf', 'w', encoding='utf-8')
            fd.write(ca_certificates_conf)
            fd.close()            
        
            # Run update-ca-certificates
            commandUtil = CommandUtil()
            commandUtil.execute_command('/usr/sbin/update-ca-certificates')        
        
        
    def convertDERcertificateToPEM(self, certificate):
        if certificate is None:
            return None
            
        if self.isPEM(certificate):
            return certificate
            
        pem = ssl.DER_cert_to_PEM_cert(certificate)
        return pem
        
    def convertPEMcertificateToDER(self, certificate):
        if certificate is None:
            return None
            
        if not self.isPEM(certificate):
            return certificate
            
        der = ssl.PEM_cert_to_DER_cert(certificate)
        return der
        