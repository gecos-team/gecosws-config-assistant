#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: software_sources
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
action :setup do
  begin
    repo_list = new_resource.repo_list
    
    current_lists = []
    remote_lists = []    

    Dir.foreach('/etc/apt/sources.list.d') do |item|
      next if item == '.' or item == '..'
      current_lists.push(item)
    end

    if repo_list.any?
      repo_list.each do |repo|
        remote_lists.push("#{repo.repo_name}.list")        
        apt_repository repo.repo_name do
          uri repo.uri
          distribution repo.distribution
          components repo.components
          action "add"
          key repo.repo_key
          keyserver repo.key_server
          deb_src repo.deb_src 
        end
      end
    end

    files_to_remove = current_lists - remote_lists
    files_to_remove.each do |value|
      ::File.delete("/etc/apt/sources.list.d/#{value}")
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

