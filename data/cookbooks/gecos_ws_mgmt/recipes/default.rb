#
# Cookbook Name:: gecos_ws_mgmt
# Recipe:: default
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

execute "gecos-chef-snitch" do
  command "gecosws-chef-snitch-client --set-active true"
  action :nothing
end.run_action(:run)

Chef::Log.info("Disable chef-client daemon to use wrapper")

service 'chef-client' do
  provider Chef::Provider::Service::Upstart
  supports :status => true, :restart => true, :reload => true
  action [:disable, :stop]
end

Chef::Log.info("Installing wrapper")
cookbook_file "chef-client-wrapper" do
  path "/usr/bin/chef-client-wrapper"
  owner 'root'
  mode '0755'
  group 'root'
  action :nothing
end.run_action(:create_if_missing)

Chef::Log.info("Enable chef-client-wrapper")

file "/var/spool/cron/crontabs/root" do
  owner 'root'
  group 'root'
  action :nothing
end.run_action(:create_if_missing)

bash "Added cron line for wrapper" do 
  user "root"
  cwd "/var/spool/cron/crontabs/"
  code <<-EOF
    grep chef-client-wrapper root
    if [[ $? -eq 1 ]]; then
       echo "*/30 * * * * chef-client-wrapper" >> root
    fi
  EOF
  not_if "grep chef-client-wrapper root"
end.run_action(:run)

include_recipe "gecos_ws_mgmt::software_mgmt"
include_recipe "gecos_ws_mgmt::misc_mgmt"
include_recipe "gecos_ws_mgmt::network_mgmt"
include_recipe "gecos_ws_mgmt::users_mgmt"
include_recipe "gecos_ws_mgmt::printers_mgmt"


node.set['use_node']= {}
