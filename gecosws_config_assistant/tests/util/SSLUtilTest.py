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


import unittest
import os

from gecosws_config_assistant.util.SSLUtil import SSLUtil, SSL_R_CERTIFICATE_VERIFY_FAILED

class SSLUtilTest(unittest.TestCase):
    '''
    Unit test that check SSLUtil methods
    '''


    def runTest(self):
        sslUtil = SSLUtil()
        sslUtil.timeout = 10
		
        # Reset the test
        certificate = sslUtil.getServerCertificate('https://gecos.solutia-it.es:8443/')
        sslUtil.removeCertificateFromTrustedCAs(certificate)
        certificate = sslUtil.getServerCertificate('https://ws003.juntadeandalucia.es/')
        sslUtil.removeCertificateFromTrustedCAs(certificate)

        # Start the test
        
		self.assertFalse(sslUtil.isServerCertificateTrusted(None))
		self.assertFalse(sslUtil.isServerCertificateTrusted('https://ws003.juntadeandalucia.es/'))
		self.assertTrue(sslUtil.isServerCertificateTrusted('https://www.google.es/'))

        self.assertIsNotNone(sslUtil.getUntrustedCertificateCause('https://ws003.juntadeandalucia.es/'))
        print('Untrusted certificate cause: %s'%(sslUtil.getUntrustedCertificateCause('https://ws003.juntadeandalucia.es/')))
        
        self.assertIsNotNone(sslUtil.getUntrustedCertificateErrorCode('https://ws003.juntadeandalucia.es/'))
        self.assertEquals(sslUtil.getUntrustedCertificateErrorCode('https://ws003.juntadeandalucia.es/'), SSL_R_CERTIFICATE_VERIFY_FAILED)
        print('Untrusted certificate error code: %s'%(sslUtil.getUntrustedCertificateErrorCode('https://ws003.juntadeandalucia.es/')))
        
        
        self.assertIsNotNone(sslUtil.getUntrustedCertificateCause('https://192.168.0.15:8443/'))
        print('Untrusted certificate cause: %s'%(sslUtil.getUntrustedCertificateCause('https://192.168.0.15:8443/')))
        
        self.assertIsNotNone(sslUtil.getUntrustedCertificateErrorCode('https://192.168.0.15:8443/'))
        print('Untrusted certificate error code: %s'%(sslUtil.getUntrustedCertificateErrorCode('https://192.168.0.15:8443/')))
        
        self.assertIsNone(sslUtil.getServerCertificate(None))
        self.assertIsNotNone(sslUtil.getServerCertificate('https://ws003.juntadeandalucia.es/'))
        self.assertIsNone(sslUtil.getServerCertificate('https://ws003.juntadeandalucia.es:8443/'))

        # Self signed certificate
        certificate = sslUtil.getServerCertificate('https://gecos.solutia-it.es:8443/')
        info = sslUtil.getCertificateInfo(certificate)
        self.assertIsNotNone(info)
        
        print('=================== self signed certificate ===================')
        print('ISSUER: %s'%(sslUtil.formatX509Name(info.get_issuer()).encode('ascii', 'ignore')))
        print('NOT BEFORE: %s'%(info.get_notBefore()))
        print('NOT AFTER: %s'%(info.get_notAfter()))
        print('SERIAL NUMBER: %s'%(info.get_serial_number()))
        print('SUBJECT: %s'%(sslUtil.formatX509Name(info.get_subject()).encode('ascii', 'ignore')))
        print('SUBJECT CN: %s'%(info.get_subject().commonName))
        print('EXPIRED: %s'%(info.has_expired()))
        print('SELF SIGNED: %s'%(sslUtil.isSelfSigned(info)))
        
        issuerCertificateUrl = sslUtil.getIssuerCertificateURL(info)
        self.assertIsNone(issuerCertificateUrl)        

        sslUtil.addCertificateToTrustedCAs(certificate, True)
		self.assertTrue(sslUtil.isServerCertificateTrusted('https://gecos.solutia-it.es:8443/'))

        self.assertTrue(os.path.exists('/etc/chef/trusted_certs/gecos.solutia-it.es.crt'))

        self.assertIsNotNone(sslUtil.getUntrustedCertificateCause('https://192.168.0.15:8443/'))
        print('Untrusted certificate cause: %s'%(sslUtil.getUntrustedCertificateCause('https://192.168.0.15:8443/')))

        sslUtil.removeCertificateFromTrustedCAs(certificate)
		self.assertFalse(sslUtil.isServerCertificateTrusted('https://gecos.solutia-it.es:8443/'))
        self.assertFalse(os.path.exists('/etc/chef/trusted_certs/gecos.solutia-it.es.crt'))
        
        
        # Signed by other entity certificate
        certificate = sslUtil.getServerCertificate('https://ws003.juntadeandalucia.es/')
        info = sslUtil.getCertificateInfo(certificate)
        self.assertIsNotNone(info)
        
        print('=================== signed by other entity certificate ===================')
        print('ISSUER: %s'%(sslUtil.formatX509Name(info.get_issuer()).encode('ascii', 'ignore')))
        print('NOT BEFORE: %s'%(info.get_notBefore()))
        print('NOT AFTER: %s'%(info.get_notAfter()))
        print('SERIAL NUMBER: %s'%(info.get_serial_number()))
        print('SUBJECT: %s'%(sslUtil.formatX509Name(info.get_subject()).encode('ascii', 'ignore')))
        print('SUBJECT CN: %s'%(info.get_subject().commonName))
        print('EXPIRED: %s'%(info.has_expired()))
        print('SELF SIGNED: %s'%(sslUtil.isSelfSigned(info)))
        
        issuerCertificateUrl = sslUtil.getIssuerCertificateURL(info)
        self.assertIsNotNone(issuerCertificateUrl)
        print('ISSUER CERTIFICATE URL: %s'%(issuerCertificateUrl))        
        

        self.assertFalse(sslUtil.isPEM(certificate))
        
        pem = sslUtil.convertDERcertificateToPEM(certificate)
        self.assertIsNotNone(pem)
        self.assertTrue(sslUtil.isPEM(pem))
        
        der = sslUtil.convertPEMcertificateToDER(pem)
        self.assertIsNotNone(der)
        self.assertEqual(der, certificate)
        
        
        
        sslUtil.addCertificateToTrustedCAs(certificate)
		self.assertTrue(sslUtil.isServerCertificateTrusted('https://ws003.juntadeandalucia.es/'))

        sslUtil.removeCertificateFromTrustedCAs(certificate)
		self.assertFalse(sslUtil.isServerCertificateTrusted('https://ws003.juntadeandalucia.es/'))
		

