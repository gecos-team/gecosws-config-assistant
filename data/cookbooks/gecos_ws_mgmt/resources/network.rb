#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: network
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :ip_address, :kind_of => String
attribute :gateway, :kind_of => String
attribute :netmask, :kind_of => String
attribute :network_type, :kind_of => String
attribute :use_dhcp, :kind_of => [NilClass, TrueClass, FalseClass]
attribute :dns_servers_array, :kind_of => Array
attribute :users, :kind_of => Hash
attribute :job_ids, :kind_of => Array
