#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: chef
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup
default_action :setup

attribute :chef_server_url,  :name_attribute => true, :kind_of => String
attribute :chef_link, :kind_of => [ TrueClass, FalseClass ], :default => false
attribute :chef_node_name, :kind_of => String
attribute :chef_admin_name, :kind_of => String
attribute :chef_validation_pem, :kind_of => String
attribute :job_ids, :kind_of => Array

