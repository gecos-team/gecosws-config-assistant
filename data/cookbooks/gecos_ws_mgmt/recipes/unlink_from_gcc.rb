#
# Cookbook Name:: gecos-ws-mgmt
# Recipe:: local
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
gecos_ws_mgmt_gcc "unlink" do
  gcc_link node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_link]
  gcc_nodename node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_nodename]
  uri_gcc node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:uri_gcc]
  gcc_pwd_user node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_pwd_user]
  gcc_username node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:username]
  run_attr true
  job_ids []
  action  :setup
end