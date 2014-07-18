#
# Cookbook Name:: gecos_ws_mgmt
# Recipe:: software_management
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
include_recipe "apt"

gecos_ws_mgmt_software_sources 'apt sources list manage' do
  repo_list node[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:repo_list]
  job_ids node[:gecos_ws_mgmt][:software_mgmt][:software_sources_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_package 'install packages list' do
  package_list node[:gecos_ws_mgmt][:software_mgmt][:package_res][:package_list]
  pkgs_to_remove node[:gecos_ws_mgmt][:software_mgmt][:package_res][:pkgs_to_remove]
  job_ids node[:gecos_ws_mgmt][:software_mgmt][:package_res][:job_ids]
  action :setup
end

