#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: power_conf
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

actions :setup

attribute :cpu_freq_gov, :kind_of => String
attribute :auto_shutdown, :kind_of => Object
attribute :usb_autosuspend, :kind_of => String
attribute :job_ids, :kind_of => Array

