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
  action :setup
end

gecos_ws_mgmt_user_launchers 'user launchers' do
  users node[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:user_launchers_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_user_shared_folders 'user shared folders' do
  users node[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:user_shared_folders_res][:job_ids]
  action :setup
end

#gecos_ws_mgmt_desktop_background node[:gecos_ws_mgmt][:users_mgmt][:desktop_background_res][:users] do
#    action  :setup
#end

gecos_ws_mgmt_screensaver 'localhost screensaver' do
  users node[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:screensaver_res][:job_ids]
  action :setup
end

gecos_ws_mgmt_web_browser 'web browser' do
  users node[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:users]
  job_ids node[:gecos_ws_mgmt][:users_mgmt][:web_browser_res][:job_ids]
  action :setup
end
