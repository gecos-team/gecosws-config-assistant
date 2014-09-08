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

gecos_ws_mgmt_sssd 'configure_sssd' do
  domain node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:domain]
  enabled node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:enabled]
  job_ids node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:support_os]
  action  :setup
end
