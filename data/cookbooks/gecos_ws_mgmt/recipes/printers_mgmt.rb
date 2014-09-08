#
# Cookbook Name:: gecos-ws-mgmt
# Recipe:: printers_management
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

gecos_ws_mgmt_printers 'printers list to set' do
  printers_list node[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:printers_list]
  job_ids node[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:printers_mgmt][:printers_res][:support_os]
  action :setup
end

