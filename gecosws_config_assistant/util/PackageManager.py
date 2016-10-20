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
        self.logger.debug('is_package_installed BEGIN')
        if package_name is None:
            raise ValueError('package_name is None')

        self.logger.debug('is_package_installed(%s)'%(package_name))

        
        try:
            import apt
            cache = apt.Cache()
            self.logger.debug('is_package_installed(%s) APT: %s'%(package_name, 
                cache[package_name].is_installed))
            return cache[package_name].is_installed
        
        except ImportError:
            self.logger.info('No apt library available')

        # TODO: Yum version?
        
        
        return False

    def exists_package(self, package_name):
        self.logger.debug('exists_package BEGIN')
        if package_name is None:
            raise ValueError('package_name is None')
        
        self.logger.debug('exists_package(%s)'%(package_name))
        
        try:
            import apt
            cache = apt.Cache()
            return cache.has_key(package_name)
        
        except ImportError:
            self.logger.info('No apt library available')

        # TODO: Yum version?
        
        
        raise OSError('Package search failed!')


    def upgrade_package(self, package_name):
        self.logger.debug('upgrade_package BEGIN')
        if package_name is None:
            raise ValueError('package_name is None')
        
        self.logger.debug('upgrade_package(%s)'%(package_name))
        
        try:
            import apt
            cache = apt.Cache()
            pkg = cache[package_name]
            if pkg is None:
                self.logger.error('Package not found:' + package_name)
            elif not pkg.is_installed:
                self.logger.error('Package not installed:' + package_name)
            elif not pkg.is_upgradable:
                self.logger.error('Package not upgradable:' + package_name)
                return False
            else:
                pkg.mark_install()

                try:
                    cache.commit()
                    self.logger.debug('Package upgrade successfully')
                    return True
                except Exception:
                    self.logger.error('Package upgrade failed:' + package_name)
                    self.logger.error(str(traceback.format_exc()))
                
                
        
        except ImportError:
            self.logger.info('No apt library available')

        # TODO: Yum version?
        
        
        raise OSError('Package upgrade failed!')



    def install_package(self, package_name):
        self.logger.debug('install_package BEGIN')
        if package_name is None:
            raise ValueError('package_name is None')
        
        self.logger.debug('install_package(%s)'%(package_name))
        
        try:
            import apt
            cache = apt.Cache()
            pkg = cache[package_name]
            if pkg is None:
                self.logger.error('Package not found:' + package_name)
            elif pkg.is_installed:
                self.logger.error('Package already installed:' + package_name)
            else:
                pkg.mark_install()

                try:
                    cache.commit()
                    self.logger.debug('Package installed successfully')
                    return True
                except Exception:
                    self.logger.error('Package installation failed:' + package_name)
                    self.logger.error(str(traceback.format_exc()))
                
                
        
        except ImportError:
            self.logger.info('No apt library available')

        # TODO: Yum version?
        
        
        raise OSError('Package installation failed!')

    def update_cache(self):
        self.logger.debug('update_cache - BEGIN')
        
        try:
            import apt
            cache = apt.Cache()
            try:
                cache.update()
                self.logger.debug('Packages cache updated successfully')
                return True
            except Exception:
                self.logger.error('Package update failed!')
                self.logger.error(str(traceback.format_exc()))
                
                
        
        except ImportError:
            self.logger.info('No apt library available')

        # TODO: Yum version?
        
        
        raise OSError('Package cache update failed!')


    def get_package_version(self, package_name):
        self.logger.debug('get_package_version - BEGIN')
        
        if package_name is None:
            raise ValueError('package_name is None')
        
        self.logger.debug('get_package_version(%s)'%(package_name))
        
        
        try:
            import apt
            cache = apt.Cache()
            pkg = cache[package_name]
            if pkg is None:
                self.logger.error('Package not found:' + package_name)
            elif not pkg.is_installed:
                self.logger.error('Package is not installed:' + package_name)
            else:
                return pkg.installed.version
                
                
        
        except ImportError:
            self.logger.info('No apt library available')

        # TODO: Yum version?
        
        
        return None
 

    def remove_package(self, package_name):
        self.logger.debug('remove_package - BEGIN')
        
        if package_name is None:
            raise ValueError('package_name is None')
        
        self.logger.debug('remove_package(%s)'%(package_name))
        
        
        try:
            import apt
            cache = apt.Cache()
            pkg = cache[package_name]
            if pkg is None:
                self.logger.error('Package not found:' + package_name)
            elif not pkg.is_installed:
                self.logger.error('Package is not installed:' + package_name)
            else:
                pkg.mark_delete()

                try:
                    cache.commit()
                    self.logger.debug('Package removed successfully')
                    return True
                except Exception:
                    self.logger.error('Package removal failed:' + package_name)
                    self.logger.error(str(traceback.format_exc()))
                
                
        
        except ImportError:
            self.logger.info('No apt library available')

        # TODO: Yum version?
        
        
        raise OSError('Package removal failed!')
