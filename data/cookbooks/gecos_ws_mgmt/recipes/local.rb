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

#include_recipe "gecos_ws_mgmt::sssd_mgmt"



if not node[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res].nil?
  gecos_ws_mgmt_tz_date 'localtime' do
    server node[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:server]
    job_ids []
    support_os node[:gecos_ws_mgmt][:misc_mgmt][:tz_date_res][:support_os]
    action :setup
  end
end

if not node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_server_url].nil?
    
  Chef::Log.info("Installing GECOS Agent")

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
#  Chef::Log.info("Disabling old chef-client service")

#  service 'chef-client' do
#    provider Chef::Provider::Service::Upstart
#    supports :status => true, :restart => true, :reload => true
#    action [:disable, :stop]
#  end

  gecos_ws_mgmt_chef node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_server_url] do
    chef_link node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_link]
    chef_validation_pem node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_validation_pem]
    chef_node_name node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_node_name]
    chef_admin_name node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_admin_name]
    chef_link_existing node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_link_existing]
    job_ids []
    support_os node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:support_os]
    action  :setup
  end


end

if not node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:uri_gcc].nil?
  gecos_ws_mgmt_gcc node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:uri_gcc] do
    gcc_link node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_link]
    gcc_nodename node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_nodename]
    gcc_username node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_username]
    gcc_pwd_user node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_pwd_user]
    run_attr node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:run_attr]
    gcc_selected_ou node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:gcc_selected_ou]
    job_ids []
    support_os node[:gecos_ws_mgmt][:misc_mgmt][:gcc_res][:support_os]
    action  :setup
  end
end

if not node[:gecos_ws_mgmt][:network_mgmt][:sssd_res].nil?
  if not node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:krb5_url].nil? and 
    not node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:smb_url].nil? and
    not node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:sssd_url].nil? and
    not node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:mkhomedir_url].nil?

    gecos_ws_mgmt_sssd "configure sssd" do
      domain node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:domain]
      enabled node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:enabled]
      job_ids []
      krb5_url node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:krb5_url]
      smb_url node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:smb_url]
      sssd_url node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:sssd_url]
      mkhomedir_url node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:mkhomedir_url]
      support_os node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:support_os]
      action :setup 
    end

  else
    gecos_ws_mgmt_sssd "configure sssd" do
      domain node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:domain]
      enabled node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:enabled]
      support_os node[:gecos_ws_mgmt][:network_mgmt][:sssd_res][:support_os]
      job_ids []
      action  :setup
    end
  end

end

if not node[:gecos_ws_mgmt][:misc_mgmt][:local_users_res].nil?
  gecos_ws_mgmt_local_users 'manage local users' do
    users_list node[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:users_list]
    support_os node[:gecos_ws_mgmt][:misc_mgmt][:local_users_res][:support_os]
    job_ids []
    action :setup
  end
end  

node.set['use_node']= {}
