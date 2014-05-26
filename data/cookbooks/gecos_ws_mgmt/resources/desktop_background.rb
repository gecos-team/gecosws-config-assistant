#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: desktop_background
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup
default_action :setup

attribute :desktop_file, :name_attribute => true, :kind_of => String
attribute :job_ids, :kind_of => Array