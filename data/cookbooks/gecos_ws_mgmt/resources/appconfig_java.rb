#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: appconfig_java
#
# Copyright 2015, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :config_java, :kind_of => Object
attribute :job_ids, :kind_of => Array
attribute :support_os, :kind_of => Array
