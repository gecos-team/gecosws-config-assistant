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

import logging
import traceback


class PackageManager(object):
    '''
    Utility class to manipulate packages.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('PackageManager')
        

    def is_package_installed(self, package_name):
        if package_name is None:
            raise ValueError('package_name is None')
        
        try:
            import apt
            cache = apt.Cache()
            return cache[package_name].is_installed
        
        except ImportError:
            self.logger.info(_('No apt library available'))

        # TODO: Yum version?
        
        
        return False


    def install_package(self, package_name):
        if package_name is None:
            raise ValueError('package_name is None')
        
        try:
            import apt
            cache = apt.Cache()
            pkg = cache[package_name]
            if pkg is None:
                self.logger.error(_('Package not found:'), package_name)
            elif pkg.is_installed:
                self.logger.error(_('Package already installed:'), package_name)
            else:
                pkg.mark_install()

                try:
                    cache.commit()
                    return
                except Exception:
                    self.logger.error(_('Package installation failed:'), package_name)
                    self.logger.error(str(traceback.format_exc()))
                
                
        
        except ImportError:
            self.logger.info(_('No apt library available'))

        # TODO: Yum version?
        
        
        raise OSError(_('Package installation failed!'))


    def remove_package(self, package_name):
        if package_name is None:
            raise ValueError('package_name is None')
        
        try:
            import apt
            cache = apt.Cache()
            pkg = cache[package_name]
            if pkg is None:
                self.logger.error(_('Package not found:'), package_name)
            elif not pkg.is_installed:
                self.logger.error(_('Package is not installed:'), package_name)
            else:
                pkg.mark_delete()

                try:
                    cache.commit()
                    return
                except Exception:
                    self.logger.error(_('Package removal failed:'), package_name)
                    self.logger.error(str(traceback.format_exc()))
                
                
        
        except ImportError:
            self.logger.info(_('No apt library available'))

        # TODO: Yum version?
        
        
        raise OSError(_('Package removal failed!'))
