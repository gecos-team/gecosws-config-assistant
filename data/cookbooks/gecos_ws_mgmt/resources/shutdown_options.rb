#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: shutdown_options
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :systemset, :kind_of => [TrueClass, FalseClass]
attribute :systemlock, :kind_of => [TrueClass, FalseClass]

attribute :users, :kind_of => Array
attribute :job_ids, :kind_of => Array