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

from dto.NetworkInterface import NetworkInterface

import logging

import fcntl
import array
import struct
import socket
import platform

class NetworkInterfaceDAO(object):
    '''
    DAO class to manipulate NetworkInterface DTO objects.
    '''

    # Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NetworkInterfaceDAO, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance



    def __init__(self):
        '''
        Constructor
        '''
        
        self.logger = logging.getLogger('NetworkInterfaceDAO')
     
        

    def loadAll(self):
        self.logger.debug('loadAll - BEGIN')
        interfaces = []
        
        SIOCGIFCONF = 0x8912
        MAXBYTES = 8096
        
        arch = platform.architecture()[0]
        # I really don't know what to call these right now
        var1 = -1
        var2 = -1
        if arch == '32bit':
            var1 = 32
            var2 = 32
        elif arch == '64bit':
            var1 = 16
            var2 = 40
        else:
            raise OSError("Unknown architecture: %s" % arch)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        names = array.array('B', '\0' * MAXBYTES)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            sock.fileno(),
            SIOCGIFCONF,
            struct.pack('iL', MAXBYTES, names.buffer_info()[0])
            ))[0]
        
        namestr = names.tostring()
        ifaces = [(namestr[i:i + var1].split('\0', 1)[0], socket.inet_ntoa(namestr[i + 20:i + 24])) \
                for i in xrange(0, outbytes, var2)]
        
        for iface in ifaces:
            interface = NetworkInterface()
            interface.set_name(iface[0].strip())
            interface.set_ip_address(iface[1].strip())
            
            interfaces.append(interface)
        
        
        return interfaces


