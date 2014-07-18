#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: package
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    
    if new_resource.package_list.any? 
      Chef::Log.info("Instalando lista de paquetes")
      new_resource.package_list.each do |pkg|
        package pkg do
          action :nothing
        end.run_action(:install)
      end
    end

    if new_resource.pkgs_to_remove.any?
      Chef::Log.info("Desinstalando paquetes no asignados al nodo")
      new_resource.pkgs_to_remove.each do |pkg|
        package pkg do
          action :nothing
        end.run_action(:purge)
      end
    end

    # save current job ids (new_resource.job_ids) as "ok"
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 0
    end

  rescue Exception => e
    # just save current job ids as "failed"
    # save_failed_job_ids
    Chef::Log.error(e.message)
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  ensure
    gecos_ws_mgmt_jobids "software_mgmt" do
      provider "gecos_ws_mgmt_jobids"
      resource "package_res"
    end.run_action(:reset)
  end
end

