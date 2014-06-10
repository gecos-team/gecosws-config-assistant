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

gecos_ws_mgmt_local_users 'manage local users' do
  users_list node[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:users_list]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_power_conf 'manage power conf' do
  cpu_freq_gov node[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:cpu_freq_gov]
  auto_shutdown node[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:auto_shutdown]
  usb_autosuspend node[:gecos_ws_mgmt][:misc_mgmt][:power_conf_res][:usb_autosuspend]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_scripts_launch 'launch commands on startup/shutdown' do
  on_startup node[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_startup]
  on_shutdown node[:gecos_ws_mgmt][:misc_mgmt][:scripts_launch_res][:on_shutdown]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:local_file_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_auto_updates 'manage auto updates' do
  onstart_update node[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:onstart_update]
  onstop_update node[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:onstop_update]
  days node[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:days]
  date node[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:auto_updates_rules][:date]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:auto_updates_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_tz_date 'localtime' do
  server node[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:server]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_desktop_background 'desktop background' do
  desktop_file node[:gecos_ws_mgmt][:misc_mgmt][:desktop_background_res][:desktop_file]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:desktop_background_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_local_groups 'add users to system local groups' do
  groups_list node[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:groups_list]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:local_groups_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_local_admin_users 'assert users list as sudoers' do
  local_admin_list node[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:local_admin_list]
  job_ids node[:gecos_ws_mgmt][:misc_mgmt][:local_admin_users_res][:job_ids]
  action :setup
end