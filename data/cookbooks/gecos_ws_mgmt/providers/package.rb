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
# OS identification moved to recipes/default.rb
#    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
#    if new_resource.support_os.include?(os)
    if new_resource.support_os.include?($gecos_os)
      if new_resource.package_list.any? 
        Chef::Log.info("Installing package list")
        new_resource.package_list.each do |pkg|
# Support for package version blocking
# Only ONE <package>=<version> per line accepted
	pkg.strip!
	if pkg =~ /\S+\s*=\s*\d+\S+\Z/
	  parts = pkg.split("=")
	  package parts[0].strip do
	    version parts[1].strip
# Added to support package downgrade
	    options "--force-yes"
            action :nothing
          end.run_action(:install)
          file '/etc/apt/preferences.d/'+parts[0].strip+'.ref' do
            content "Package: #{parts[0].strip}\nPin: version #{parts[1].strip}\nPin-Priority: 1000\n"
            mode '0644'
            owner 'root'
            group 'root'
            action :create
          end
        else
# Normal invocation of package resource: accepts one or more packages per line
          package pkg do
            action :nothing
          end.run_action(:install)
          file '/etc/apt/preferences.d/'+pkg.strip+'.ref' do
            action(:delete)
          end
	end
      end
    end

      if new_resource.pkgs_to_remove.any?
        Chef::Log.info("Uninstalling packages not assigned to node")
        new_resource.pkgs_to_remove.each do |pkg|
          package pkg do
            action :nothing
          end.run_action(:purge)
          file '/etc/apt/preferences.d/'+pkg.strip+'.ref' do
            action(:delete)
          end
        end
      end
    else
      Chef::Log.info("This resource is not support into your OS")
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
      if not e.message.frozen?
        node.set['job_status'][jid]['message'] = e.message.force_encoding("utf-8")
      else
        node.set['job_status'][jid]['message'] = e.message
      end
    end
  ensure
    gecos_ws_mgmt_jobids "package_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "software_mgmt"
    end.run_action(:reset)
  end
end

