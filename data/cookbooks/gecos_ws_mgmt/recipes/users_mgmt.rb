#
# Cookbook Name:: gecos-ws-mgmt
# Recipe:: users_management
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

gecos_ws_mgmt_user_apps_autostart 'user apps autostart' do
  users node[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:user_apps_autostart_res][:support_os]
  action :setup
end

gecos_ws_mgmt_user_launchers 'user launchers' do
  users node[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:support_os]
  action :setup
end

gecos_ws_mgmt_user_shared_folders 'user shared folders' do
  users node[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:support_os]
  action :setup
end

gecos_ws_mgmt_desktop_background 'desktop background' do
  users node[:gecos_ws_mgmt][:users_mgmt][:desktop_background_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:desktop_background_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:desktop_background_res][:support_os]
  action  :setup
end

gecos_ws_mgmt_screensaver 'localhost screensaver' do
  users node[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:support_os]
  action :setup
end

gecos_ws_mgmt_web_browser 'web browser' do
  users node[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:support_os]
  action :setup
end

gecos_ws_mgmt_shutdown_options 'shutdown options' do
  users node[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:users]
  systemset node[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:systemset]
  systemlock node[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:systemlock]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:shutdown_options_res][:support_os]
  action :setup
end
gecos_ws_mgmt_desktop_menu 'desktop menu' do
  users node[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:desktop_menu_res][:support_os]
  action :setup
end

gecos_ws_mgmt_file_browser 'file browser' do
  users node[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:file_browser_res][:support_os]
  action :setup
end

gecos_ws_mgmt_folder_sync 'folder syncr' do
  users node[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:folder_sync_res][:support_os]
  action :setup
end

gecos_ws_mgmt_folder_sharing 'folder sharing' do
  users node[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:folder_sharing_res][:support_os]
  action :setup
end

gecos_ws_mgmt_user_mount 'user mount' do
  users node[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:user_mount_res][:support_os]
  action :setup
end

gecos_ws_mgmt_user_modify_nm 'user modify nm' do
  users node[:gecos_ws_mgmt][:users_mgmt][:user_modify_nm_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:user_modify_nm_res][:job_ids]
  support_os node[:gecos_ws_mgmt][:users_mgmt][:user_modify_nm_res][:support_os]
  action :setup
end
