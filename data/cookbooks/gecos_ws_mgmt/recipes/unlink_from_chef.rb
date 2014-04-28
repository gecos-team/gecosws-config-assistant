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
gecos_ws_mgmt_chef "unlink" do
  chef_link node[:gecos_ws_mgmt][:misc_mgmt][:chef_conf_res][:chef_link]
  chef_validation_pem "chef_validation_pem"
  chef_node_name "chef_node_name"
  chef_admin_name "chef_admin_name"
  action  :setup
end
