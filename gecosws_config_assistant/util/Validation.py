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
__copyright__ = "Copyright (C) 2015, Junta de Andalucía" + \
    "<devmaster@guadalinex.org>"
__license__ = "GPL-2"

import re

class Validation(object):
    '''
    Utility class to validate data types.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def isUrl(self, url):
        ''' Validator for url '''

        if url is None:
            return False

        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return regex.match(str(url))

    def isLdapUri(self, url):
        ''' Validator for ldap uri '''

        if url is None:
            return False

        regex = re.compile(
            r'^(ldap)s?://' # ldap:// or ldaps://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return regex.match(str(url))

    def isLogin(self, login):
        ''' Validator for login '''

        if login is None:
            return False

        regex = re.compile("^[A-Za-z0-9_]+$")

        return regex.match(str(login))

    def isAscii(self, text):
        ''' Validator for ascii '''

        if text is None:
            return False

        try:
            asciiText = text.encode('ascii')

            return asciiText == text

        except Exception:
            return False

    def isValidNetbiosHostname(self, hostname):
        ''' Validator for netbios hostname '''
        hostname = str(hostname, "utf-8")
        # See https://support.microsoft.com/en-us/kb/909264
        if hostname is None:
            return False
        if len(hostname) < 1 or len(hostname) > 15:
            return False

        if hostname.startswith('.'):
            return False

        if (
            hostname.find('\\') >= 0 or
            hostname.find('/') >= 0 or
            hostname.find(':') >= 0 or
            hostname.find('*') >= 0 or
            hostname.find('?') >= 0 or
            hostname.find('"') >= 0 or
            hostname.find('<') >= 0 or
            hostname.find('>') >= 0 or
            hostname.find('|') >= 0
        ):
            return False

        return True
