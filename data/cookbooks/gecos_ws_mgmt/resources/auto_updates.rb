#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: auto_updates
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :onstart_update, :kind_of => [NilClass, TrueClass, FalseClass]
attribute :onstop_update, :kind_of => [NilClass, TrueClass, FalseClass]
attribute :days, :kind_of => Array
attribute :date, :kind_of => Object
attribute :job_ids, :kind_of => Array

