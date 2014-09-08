#
# Cookbook Name:: gecos-ws-mgmt
# Resource:: jobids
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#


actions :reset
 
attribute :recipe, :kind_of => String, :required => true
attribute :resource, :kind_of => String,  :name_attribute => true, :required => true
