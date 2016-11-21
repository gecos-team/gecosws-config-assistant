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

SSL_R_APP_DATA_IN_HANDSHAKE=100
SSL_R_ATTEMPT_TO_REUSE_SESSION_IN_DIFFERENT_CONTEXT=272
SSL_R_AT_LEAST_TLS_1_0_NEEDED_IN_FIPS_MODE=143
SSL_R_AT_LEAST_TLS_1_2_NEEDED_IN_SUITEB_MODE=158
SSL_R_BAD_CHANGE_CIPHER_SPEC=103
SSL_R_BAD_DATA=390
SSL_R_BAD_DATA_RETURNED_BY_CALLBACK=106
SSL_R_BAD_DECOMPRESSION=107
SSL_R_BAD_DH_VALUE=102
SSL_R_BAD_DIGEST_LENGTH=111
SSL_R_BAD_ECC_CERT=304
SSL_R_BAD_ECPOINT=306
SSL_R_BAD_HANDSHAKE_LENGTH=332
SSL_R_BAD_HELLO_REQUEST=105
SSL_R_BAD_LENGTH=271
SSL_R_BAD_PACKET_LENGTH=115
SSL_R_BAD_PROTOCOL_VERSION_NUMBER=116
SSL_R_BAD_RSA_ENCRYPT=119
SSL_R_BAD_SIGNATURE=123
SSL_R_BAD_SRP_A_LENGTH=347
SSL_R_BAD_SRP_PARAMETERS=371
SSL_R_BAD_SRTP_MKI_VALUE=352
SSL_R_BAD_SRTP_PROTECTION_PROFILE_LIST=353
SSL_R_BAD_SSL_FILETYPE=124
SSL_R_BAD_VALUE=384
SSL_R_BAD_WRITE_RETRY=127
SSL_R_BIO_NOT_SET=128
SSL_R_BLOCK_CIPHER_PAD_IS_WRONG=129
SSL_R_BN_LIB=130
SSL_R_CA_DN_LENGTH_MISMATCH=131
SSL_R_CA_KEY_TOO_SMALL=397
SSL_R_CA_MD_TOO_WEAK=398
SSL_R_CCS_RECEIVED_EARLY=133
SSL_R_CERTIFICATE_VERIFY_FAILED=134
SSL_R_CERT_CB_ERROR=377
SSL_R_CERT_LENGTH_MISMATCH=135
SSL_R_CIPHER_CODE_WRONG_LENGTH=137
SSL_R_CIPHER_OR_HASH_UNAVAILABLE=138
SSL_R_CLIENTHELLO_TLSEXT=226
SSL_R_COMPRESSED_LENGTH_TOO_LONG=140
SSL_R_COMPRESSION_DISABLED=343
SSL_R_COMPRESSION_FAILURE=141
SSL_R_COMPRESSION_ID_NOT_WITHIN_PRIVATE_RANGE=307
SSL_R_COMPRESSION_LIBRARY_ERROR=142
SSL_R_CONNECTION_TYPE_NOT_SET=144
SSL_R_CONTEXT_NOT_DANE_ENABLED=167
SSL_R_COOKIE_GEN_CALLBACK_FAILURE=400
SSL_R_COOKIE_MISMATCH=308
SSL_R_CUSTOM_EXT_HANDLER_ALREADY_INSTALLED=206
SSL_R_DANE_ALREADY_ENABLED=172
SSL_R_DANE_CANNOT_OVERRIDE_MTYPE_FULL=173
SSL_R_DANE_NOT_ENABLED=175
SSL_R_DANE_TLSA_BAD_CERTIFICATE=180
SSL_R_DANE_TLSA_BAD_CERTIFICATE_USAGE=184
SSL_R_DANE_TLSA_BAD_DATA_LENGTH=189
SSL_R_DANE_TLSA_BAD_DIGEST_LENGTH=192
SSL_R_DANE_TLSA_BAD_MATCHING_TYPE=200
SSL_R_DANE_TLSA_BAD_PUBLIC_KEY=201
SSL_R_DANE_TLSA_BAD_SELECTOR=202
SSL_R_DANE_TLSA_NULL_DATA=203
SSL_R_DATA_BETWEEN_CCS_AND_FINISHED=145
SSL_R_DATA_LENGTH_TOO_LONG=146
SSL_R_DECRYPTION_FAILED=147
SSL_R_DECRYPTION_FAILED_OR_BAD_RECORD_MAC=281
SSL_R_DH_KEY_TOO_SMALL=394
SSL_R_DH_PUBLIC_VALUE_LENGTH_IS_WRONG=148
SSL_R_DIGEST_CHECK_FAILED=149
SSL_R_DTLS_MESSAGE_TOO_BIG=334
SSL_R_DUPLICATE_COMPRESSION_ID=309
SSL_R_ECC_CERT_NOT_FOR_SIGNING=318
SSL_R_ECDH_REQUIRED_FOR_SUITEB_MODE=374
SSL_R_EE_KEY_TOO_SMALL=399
SSL_R_EMPTY_SRTP_PROTECTION_PROFILE_LIST=354
SSL_R_ENCRYPTED_LENGTH_TOO_LONG=150
SSL_R_ERROR_IN_RECEIVED_CIPHER_LIST=151
SSL_R_ERROR_SETTING_TLSA_BASE_DOMAIN=204
SSL_R_EXCESSIVE_MESSAGE_SIZE=152
SSL_R_EXTRA_DATA_IN_MESSAGE=153
SSL_R_FAILED_TO_INIT_ASYNC=405
SSL_R_FRAGMENTED_CLIENT_HELLO=401
SSL_R_GOT_A_FIN_BEFORE_A_CCS=154
SSL_R_HTTPS_PROXY_REQUEST=155
SSL_R_HTTP_REQUEST=156
SSL_R_ILLEGAL_SUITEB_DIGEST=380
SSL_R_INAPPROPRIATE_FALLBACK=373
SSL_R_INCONSISTENT_COMPRESSION=340
SSL_R_INCONSISTENT_EXTMS=104
SSL_R_INVALID_COMMAND=280
SSL_R_INVALID_COMPRESSION_ALGORITHM=341
SSL_R_INVALID_CONFIGURATION_NAME=113
SSL_R_INVALID_CT_VALIDATION_TYPE=212
SSL_R_INVALID_NULL_CMD_NAME=385
SSL_R_INVALID_SEQUENCE_NUMBER=402
SSL_R_INVALID_SERVERINFO_DATA=388
SSL_R_INVALID_SRP_USERNAME=357
SSL_R_INVALID_STATUS_RESPONSE=328
SSL_R_INVALID_TICKET_KEYS_LENGTH=325
SSL_R_LENGTH_MISMATCH=159
SSL_R_LENGTH_TOO_LONG=404
SSL_R_LENGTH_TOO_SHORT=160
SSL_R_LIBRARY_BUG=274
SSL_R_LIBRARY_HAS_NO_CIPHERS=161
SSL_R_MISSING_DSA_SIGNING_CERT=165
SSL_R_MISSING_ECDSA_SIGNING_CERT=381
SSL_R_MISSING_RSA_CERTIFICATE=168
SSL_R_MISSING_RSA_ENCRYPTING_CERT=169
SSL_R_MISSING_RSA_SIGNING_CERT=170
SSL_R_MISSING_SRP_PARAM=358
SSL_R_MISSING_TMP_DH_KEY=171
SSL_R_MISSING_TMP_ECDH_KEY=311
SSL_R_NO_CERTIFICATES_RETURNED=176
SSL_R_NO_CERTIFICATE_ASSIGNED=177
SSL_R_NO_CERTIFICATE_SET=179
SSL_R_NO_CIPHERS_AVAILABLE=181
SSL_R_NO_CIPHERS_SPECIFIED=183
SSL_R_NO_CIPHER_MATCH=185
SSL_R_NO_CLIENT_CERT_METHOD=331
SSL_R_NO_COMPRESSION_SPECIFIED=187
SSL_R_NO_GOST_CERTIFICATE_SENT_BY_PEER=330
SSL_R_NO_METHOD_SPECIFIED=188
SSL_R_NO_PEM_EXTENSIONS=389
SSL_R_NO_PRIVATE_KEY_ASSIGNED=190
SSL_R_NO_PROTOCOLS_AVAILABLE=191
SSL_R_NO_RENEGOTIATION=339
SSL_R_NO_REQUIRED_DIGEST=324
SSL_R_NO_SHARED_CIPHER=193
SSL_R_NO_SHARED_SIGNATURE_ALGORITHMS=376
SSL_R_NO_SRTP_PROFILES=359
SSL_R_NO_VALID_SCTS=216
SSL_R_NO_VERIFY_COOKIE_CALLBACK=403
SSL_R_NULL_SSL_CTX=195
SSL_R_NULL_SSL_METHOD_PASSED=196
SSL_R_OLD_SESSION_CIPHER_NOT_RETURNED=197
SSL_R_OLD_SESSION_COMPRESSION_ALGORITHM_NOT_RETURNED=344
SSL_R_PACKET_LENGTH_TOO_LONG=198
SSL_R_PARSE_TLSEXT=227
SSL_R_PATH_TOO_LONG=270
SSL_R_PEER_DID_NOT_RETURN_A_CERTIFICATE=199
SSL_R_PEM_NAME_BAD_PREFIX=391
SSL_R_PEM_NAME_TOO_SHORT=392
SSL_R_PIPELINE_FAILURE=406
SSL_R_PROTOCOL_IS_SHUTDOWN=207
SSL_R_PSK_IDENTITY_NOT_FOUND=223
SSL_R_PSK_NO_CLIENT_CB=224
SSL_R_PSK_NO_SERVER_CB=225
SSL_R_READ_BIO_NOT_SET=211
SSL_R_READ_TIMEOUT_EXPIRED=312
SSL_R_RECORD_LENGTH_MISMATCH=213
SSL_R_RECORD_TOO_SMALL=298
SSL_R_RENEGOTIATE_EXT_TOO_LONG=335
SSL_R_RENEGOTIATION_ENCODING_ERR=336
SSL_R_RENEGOTIATION_MISMATCH=337
SSL_R_REQUIRED_CIPHER_MISSING=215
SSL_R_REQUIRED_COMPRESSION_ALGORITHM_MISSING=342
SSL_R_SCSV_RECEIVED_WHEN_RENEGOTIATING=345
SSL_R_SCT_VERIFICATION_FAILED=208
SSL_R_SERVERHELLO_TLSEXT=275
SSL_R_SESSION_ID_CONTEXT_UNINITIALIZED=277
SSL_R_SHUTDOWN_WHILE_IN_INIT=407
SSL_R_SIGNATURE_ALGORITHMS_ERROR=360
SSL_R_SIGNATURE_FOR_NON_SIGNING_CERTIFICATE=220
SSL_R_SRP_A_CALC=361
SSL_R_SRTP_COULD_NOT_ALLOCATE_PROFILES=362
SSL_R_SRTP_PROTECTION_PROFILE_LIST_TOO_LONG=363
SSL_R_SRTP_UNKNOWN_PROTECTION_PROFILE=364
SSL_R_SSL3_EXT_INVALID_SERVERNAME=319
SSL_R_SSL3_EXT_INVALID_SERVERNAME_TYPE=320
SSL_R_SSL3_SESSION_ID_TOO_LONG=300
SSL_R_SSLV3_ALERT_BAD_CERTIFICATE=1042
SSL_R_SSLV3_ALERT_BAD_RECORD_MAC=1020
SSL_R_SSLV3_ALERT_CERTIFICATE_EXPIRED=1045
SSL_R_SSLV3_ALERT_CERTIFICATE_REVOKED=1044
SSL_R_SSLV3_ALERT_CERTIFICATE_UNKNOWN=1046
SSL_R_SSLV3_ALERT_DECOMPRESSION_FAILURE=1030
SSL_R_SSLV3_ALERT_HANDSHAKE_FAILURE=1040
SSL_R_SSLV3_ALERT_ILLEGAL_PARAMETER=1047
SSL_R_SSLV3_ALERT_NO_CERTIFICATE=1041
SSL_R_SSLV3_ALERT_UNEXPECTED_MESSAGE=1010
SSL_R_SSLV3_ALERT_UNSUPPORTED_CERTIFICATE=1043
SSL_R_SSL_COMMAND_SECTION_EMPTY=117
SSL_R_SSL_COMMAND_SECTION_NOT_FOUND=125
SSL_R_SSL_CTX_HAS_NO_DEFAULT_SSL_VERSION=228
SSL_R_SSL_HANDSHAKE_FAILURE=229
SSL_R_SSL_LIBRARY_HAS_NO_CIPHERS=230
SSL_R_SSL_NEGATIVE_LENGTH=372
SSL_R_SSL_SECTION_EMPTY=126
SSL_R_SSL_SECTION_NOT_FOUND=136
SSL_R_SSL_SESSION_ID_CALLBACK_FAILED=301
SSL_R_SSL_SESSION_ID_CONFLICT=302
SSL_R_SSL_SESSION_ID_CONTEXT_TOO_LONG=273
SSL_R_SSL_SESSION_ID_HAS_BAD_LENGTH=303
SSL_R_SSL_SESSION_ID_TOO_LONG=408
SSL_R_SSL_SESSION_VERSION_MISMATCH=210
SSL_R_TLSV1_ALERT_ACCESS_DENIED=1049
SSL_R_TLSV1_ALERT_DECODE_ERROR=1050
SSL_R_TLSV1_ALERT_DECRYPTION_FAILED=1021
SSL_R_TLSV1_ALERT_DECRYPT_ERROR=1051
SSL_R_TLSV1_ALERT_EXPORT_RESTRICTION=1060
SSL_R_TLSV1_ALERT_INAPPROPRIATE_FALLBACK=1086
SSL_R_TLSV1_ALERT_INSUFFICIENT_SECURITY=1071
SSL_R_TLSV1_ALERT_INTERNAL_ERROR=1080
SSL_R_TLSV1_ALERT_NO_RENEGOTIATION=1100
SSL_R_TLSV1_ALERT_PROTOCOL_VERSION=1070
SSL_R_TLSV1_ALERT_RECORD_OVERFLOW=1022
SSL_R_TLSV1_ALERT_UNKNOWN_CA=1048
SSL_R_TLSV1_ALERT_USER_CANCELLED=1090
SSL_R_TLSV1_BAD_CERTIFICATE_HASH_VALUE=1114
SSL_R_TLSV1_BAD_CERTIFICATE_STATUS_RESPONSE=1113
SSL_R_TLSV1_CERTIFICATE_UNOBTAINABLE=1111
SSL_R_TLSV1_UNRECOGNIZED_NAME=1112
SSL_R_TLSV1_UNSUPPORTED_EXTENSION=1110
SSL_R_TLS_HEARTBEAT_PEER_DOESNT_ACCEPT=365
SSL_R_TLS_HEARTBEAT_PENDING=366
SSL_R_TLS_ILLEGAL_EXPORTER_LABEL=367
SSL_R_TLS_INVALID_ECPOINTFORMAT_LIST=157
SSL_R_TOO_MANY_WARN_ALERTS=409
SSL_R_UNABLE_TO_FIND_ECDH_PARAMETERS=314
SSL_R_UNABLE_TO_FIND_PUBLIC_KEY_PARAMETERS=239
SSL_R_UNABLE_TO_LOAD_SSL3_MD5_ROUTINES=242
SSL_R_UNABLE_TO_LOAD_SSL3_SHA1_ROUTINES=243
SSL_R_UNEXPECTED_MESSAGE=244
SSL_R_UNEXPECTED_RECORD=245
SSL_R_UNINITIALIZED=276
SSL_R_UNKNOWN_ALERT_TYPE=246
SSL_R_UNKNOWN_CERTIFICATE_TYPE=247
SSL_R_UNKNOWN_CIPHER_RETURNED=248
SSL_R_UNKNOWN_CIPHER_TYPE=249
SSL_R_UNKNOWN_CMD_NAME=386
SSL_R_UNKNOWN_COMMAND=139
SSL_R_UNKNOWN_DIGEST=368
SSL_R_UNKNOWN_KEY_EXCHANGE_TYPE=250
SSL_R_UNKNOWN_PKEY_TYPE=251
SSL_R_UNKNOWN_PROTOCOL=252
SSL_R_UNKNOWN_SSL_VERSION=254
SSL_R_UNKNOWN_STATE=255
SSL_R_UNSAFE_LEGACY_RENEGOTIATION_DISABLED=338
SSL_R_UNSUPPORTED_COMPRESSION_ALGORITHM=257
SSL_R_UNSUPPORTED_ELLIPTIC_CURVE=315
SSL_R_UNSUPPORTED_PROTOCOL=258
SSL_R_UNSUPPORTED_SSL_VERSION=259
SSL_R_UNSUPPORTED_STATUS_TYPE=329
SSL_R_USE_SRTP_NOT_NEGOTIATED=369
SSL_R_VERSION_TOO_HIGH=166
SSL_R_VERSION_TOO_LOW=396
SSL_R_WRONG_CERTIFICATE_TYPE=383
SSL_R_WRONG_CIPHER_RETURNED=261
SSL_R_WRONG_CURVE=378
SSL_R_WRONG_SIGNATURE_LENGTH=264
SSL_R_WRONG_SIGNATURE_SIZE=265
SSL_R_WRONG_SIGNATURE_TYPE=370
SSL_R_WRONG_SSL_VERSION=266
SSL_R_WRONG_VERSION_NUMBER=267
SSL_R_X509_LIB=268
SSL_R_X509_VERIFICATION_SETUP_PROBLEMS=269

UNKNOWN_ERROR=0x1000

SSL_verification_enabled = True

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

    @staticmethod
    def disableSSLCertificatesVerication():
        global SSL_verification_enabled
        SSL_verification_enabled = False

    @staticmethod
    def enableSSLCertificatesVerication():
        global SSL_verification_enabled
        SSL_verification_enabled = True

    @staticmethod
    def isSSLCertificatesVericationEnabled():
        global SSL_verification_enabled
        return SSL_verification_enabled



    def isServerCertificateTrusted(self, url):
        if url is None:
            return False

        if not SSLUtil.isSSLCertificatesVericationEnabled():
            # SSL certificate verification is disabled
            return True
        
        # Check credentials
        try:
            r = requests.get(url, verify=True, timeout=self.timeout)
            return True            
            
        except requests.exceptions.SSLError:
            self.logger.debug('Certifcate not trusted in URL: %s'%(url))
            
        except Exception:
            self.logger.warn('Error connecting to server: %s'%(url))
            self.logger.warn(str(traceback.format_exc()))
            
        return False    

    def getUntrustedCertificateCause(self, url):
        if url is None:
            return None
        
        if not SSLUtil.isSSLCertificatesVericationEnabled():
            # SSL certificate verification is disabled
            return None

        # Check credentials
        try:
            r = requests.get(url, verify=True, timeout=self.timeout)
            
        except requests.exceptions.SSLError as e:
            msg = str(e)
            self.logger.warn('Untrusted Certificate Cause: %s'%(msg))
            
            # Check if the error message is similar to '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)'
            p = re.compile('\\[SSL: (?P<constant>[A-Z_]+)\\] (?P<message>[^\\(]+)')
            m = p.match(msg)
            if m is not None:
                if m.groups('message') is not None:
                    return m.groups('message')[0].strip()
            
            # If not we simply suppose that the error message is at the end
            if msg.rfind(':') > 0:
                msg = msg[(msg.rfind(':')+1):]
            
            
            return msg
            
        except Exception as e:
            return str(e)
            
        return None    

    def _getSSLError(self, e):
        if isinstance(e, ssl.SSLError):
            return e

        for arg in e.args:
            if isinstance(arg, ssl.SSLError):
                return arg
                
            if isinstance(arg, Exception):
                return self._getSSLError(arg)
            
        return None

        
    def getUntrustedCertificateErrorCode(self, url):
        if url is None:
            return None
        
        if not SSLUtil.isSSLCertificatesVericationEnabled():
            # SSL certificate verification is disabled
            return None

        # Check credentials
        try:
            r = requests.get(url, verify=True, timeout=self.timeout)
            
        except requests.exceptions.SSLError as e:
            self.logger.warn('Untrusted Certificate Cause to error code: %s'%(str(e)))
            sslError = self._getSSLError(e)
            if not sslError is None:
                msg = str(sslError)
                self.logger.debug('SSLError: %s'%(msg))
                errornum = None
                
                # Check if the error message is similar to '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)'
                p = re.compile('\\[SSL: (?P<constant>[A-Z_]+)\\] (?P<message>[^\\(]+)')
                m = p.match(msg)
                if m is not None:
                    if m.groups('constant') is not None:
                        constant = m.groups('message')[0].strip()
                        try:
                            errornum = eval('SSL_R_%s'%(constant))
                        except:
                            self.logger.warn('Error evaluating constant: %s'%(constant))
                
                # If not look for a packed error number
                if msg.rfind('error:') > 0:
                    msg = msg[(msg.find('error:')+6):]
                    errornum = msg[:(msg.find(':'))]
                    errornum = int('0x'+errornum, 16)
                    
                    # Unpack the reason
                    errornum = errornum & 0xFFF
                
                return errornum

            else:
                return UNKNOWN_ERROR
            
        except Exception as e:
            return None
            
        return None    
        
        
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
            return None
        
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
        
    def addCertificateToTrustedCAs(self, certificate, isChefCertificate = False):
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
            filename = ("%s.crt"%(info.get_subject().commonName.lower()))
            
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

        # Chef server certificates must be also included inside /etc/chef/trusted_certs path
        # (At least for embedded Chef clients that use /opt/chef/embedded/ssl/certs)
        if isChefCertificate and not os.path.exists('/etc/chef/trusted_certs/%s'%(filename)):
            if not os.path.isdir('/etc/chef'): 
                os.mkdir('/etc/chef')

            if not os.path.isdir('/etc/chef/trusted_certs'): 
                os.mkdir('/etc/chef/trusted_certs')

            os.symlink('/usr/share/ca-certificates/gecos/%s'%(filename), '/etc/chef/trusted_certs/%s'%(filename))

        
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
        
    def formatX509Name(self, x509Name):
        str = '';
        
        if x509Name.commonName is not None:
            str = str + 'CN='+x509Name.commonName+', '

        if x509Name.organizationalUnitName is not None:
            str = str + 'OU='+x509Name.organizationalUnitName+', '

        if x509Name.organizationName is not None:
            str = str + 'O='+x509Name.organizationName+', '
            
        if x509Name.localityName is not None:
            str = str + 'L='+x509Name.localityName+', '
            
        if x509Name.stateOrProvinceName is not None:
            str = str + 'ST='+x509Name.stateOrProvinceName+', '
            
        if x509Name.countryName is not None:
            str = str + 'C='+x509Name.countryName+', '
        
        if str.endswith(', '):
            str = str[:-2]
        
        return str
        
        
        
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
            filename = ("%s.crt"%(info.get_subject().commonName.lower()))
        
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

        if os.path.lexists('/etc/chef/trusted_certs/%s'%(filename)):
            os.unlink('/etc/chef/trusted_certs/%s'%(filename))
            

        
        
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
        