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
      package new_resource.package_list.join(" ")
    end

    if new_resource.pkgs_to_remove.any?
      Chef::Log.info("Desinstalando paquetes no asignados al nodo")
      package new_resource.pkgs_to_remove.join(" ") do
        action :purge
      end
    end

    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"

  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end
end

