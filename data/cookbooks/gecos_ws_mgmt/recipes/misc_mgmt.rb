#
# Cookbook Name:: gecos-ws-mgmt
# Recipe:: misc_management
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

gecos_ws_mgmt_local_file 'manage local files' do
  delete_files node[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:delete_files]
  copy_files node[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:copy_files]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_scripts_launch 'launch commands on startup/shutdown' do
  on_startup node[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_startup]
  on_shutdown node[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_shutdown]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_tz_date 'localtime' do
  server node[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:server]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_desktop_background node[:gecos_ws_mgmt][:misc_mgmt][:desktop_background_res][:desktop_file] do
    action  :setup
end

