#
# Cookbook Name:: gecos_ws_mgmt
# Recipe:: default
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

include_recipe "gecos_ws_mgmt::software_mgmt"
include_recipe "gecos_ws_mgmt::misc_mgmt"
include_recipe "gecos_ws_mgmt::network_mgmt"
include_recipe "gecos_ws_mgmt::users_mgmt"
