#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: gcc
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup
default_action :setup

attribute :uri_gcc,  :name_attribute => true, :kind_of => String
attribute :gcc_link, :kind_of => [ TrueClass, FalseClass ], :default => false
attribute :gcc_nodename, :kind_of => String
attribute :gcc_username, :kind_of => String
attribute :gcc_pwd_user, :kind_of => String
attribute :gcc_selected_ou, :kind_of => String
attribute :job_ids, :kind_of => Array

