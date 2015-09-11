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

# Glogal variable $gecos_os created to reduce calls to external programs
$gecos_os = `lsb_release -d`.split(":")[1].chomp().lstrip()

execute "gecos-chef-snitch" do
  command "gecosws-chef-snitch-client --set-active true"
  action :nothing
end.run_action(:run)

Chef::Log.info("Installing wrapper")
cookbook_file "chef-client-wrapper" do
  path "/usr/bin/chef-client-wrapper"
  owner 'root'
  mode '0755'
  group 'root'
  action :nothing
end.run_action(:create_if_missing)

Chef::Log.info("Enabling GECOS Agent in cron")
  
cron "GECOS Agent"
    minute '30'
    command '/usr/bin/chef-client-wrapper'
    action :create
end

Chef::Log.info("Disabling old chef-client service")

service 'chef-client' do
    provider Chef::Provider::Service::Upstart
    supports :status => true, :restart => true, :reload => true
    action [:disable, :stop]
end

include_recipe "gecos_ws_mgmt::software_mgmt"
include_recipe "gecos_ws_mgmt::misc_mgmt"
include_recipe "gecos_ws_mgmt::network_mgmt"
include_recipe "gecos_ws_mgmt::users_mgmt"
include_recipe "gecos_ws_mgmt::printers_mgmt"


node.set['use_node']= {}
