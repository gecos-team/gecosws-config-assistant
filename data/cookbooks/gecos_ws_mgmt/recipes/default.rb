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

# Global variable $gecos_os created to reduce calls to external programs
$gecos_os = `lsb_release -d`.split(":")[1].chomp().lstrip()

# Snitch, the chef notifier has been renamed
# TODO: move this to chef-client-wrapper
if ::File.exists?("/usr/bin/gecos-snitch-client")
  snitch_binary="/usr/bin/gecos-snitch-client"
else
  snitch_binary="/usr/bin/gecosws-chef-snitch-client"
end  

execute "gecos-snitch-client" do
  command "#{snitch_binary} --set-active true"
  action :nothing
end.run_action(:run)


# This should not be necessary, as wrapper is in new GECOS-Agent package. It is a transitional solution.
Chef::Log.info("Installing wrapper")
cookbook_file "gecos-chef-client-wrapper" do
  path "/usr/bin/gecos-chef-client-wrapper"
  owner 'root'
  mode '0700'
  group 'root'
  action :nothing
end.run_action(:create_if_missing)

Chef::Log.info("Enabling GECOS Agent in cron")
  
cron "GECOS Agent" do
    minute '30'
    command '/usr/bin/gecos-chef-client-wrapper'
    action :create
end

# This chef-client upstart service is not created anymore
#Chef::Log.info("Disabling old chef-client service")

#service 'chef-client' do
#    provider Chef::Provider::Service::Upstart
#    supports :status => true, :restart => true, :reload => true
#    action [:disable, :stop]
#end

include_recipe "gecos_ws_mgmt::software_mgmt"
include_recipe "gecos_ws_mgmt::misc_mgmt"
include_recipe "gecos_ws_mgmt::network_mgmt"
include_recipe "gecos_ws_mgmt::users_mgmt"
include_recipe "gecos_ws_mgmt::printers_mgmt"


node.set['use_node']= {}
