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

gecos_ws_mgmt_sssd node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:domain_list] do
  enabled node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:enabled]
  workgroup node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:workgroup]
  job_ids node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:job_ids]
  action  :setup
end
