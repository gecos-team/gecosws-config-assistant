#
# Cookbook Name:: gecos-ws-mgmt
# Recipe:: network_management
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

gecos_ws_mgmt_network "localhost" do
  gateway node[:gecos_ws_mgmt][:network_mgmt][:network_res][:gateway]
  ip_address node[:gecos_ws_mgmt][:network_mgmt][:network_res][:ip_address]
  netmask node[:gecos_ws_mgmt][:network_mgmt][:network_res][:netmask]
  network_type node[:gecos_ws_mgmt][:network_mgmt][:network_res][:network_type]
  use_dhcp node[:gecos_ws_mgmt][:network_mgmt][:network_res][:use_dhcp]
  dns_servers_array node[:gecos_ws_mgmt][:network_mgmt][:network_res][:dns_servers]
  users node[:gecos_ws_mgmt][:network_mgmt][:network_res][:users]
  job_ids node[:gecos_ws_mgmt][:network_mgmt][:network_res][:job_ids]
  action :setup
end
