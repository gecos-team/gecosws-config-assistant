#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: app_config
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :java_config, :kind_of => Object
attribute :firefox_config, :kind_of => Object
attribute :thunderbird_config, :kind_of => Object
attribute :citrix_config, :kind_of => Object
attribute :loffice_config, :kind_of => Object
attribute :job_ids, :kind_of => Array
attribute :support_os, :kind_of => Array