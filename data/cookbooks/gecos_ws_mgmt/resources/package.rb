#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: package
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :package_list, :kind_of => Array
attribute :pkgs_to_remove, :kind_of => Array
attribute :job_ids, :kind_of => Array

