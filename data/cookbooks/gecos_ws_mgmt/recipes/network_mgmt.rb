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

puts 

gecos_ws_mgmt_network "localhost" do
  connections node[:gecos_ws_mgmt][:network_mgmt][:network_res][:connections]
  job_ids node[:gecos_ws_mgmt][:network_mgmt][:network_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:network_mgmt][:network_res][:support_os]
  action  :setup
end
