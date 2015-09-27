#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: local_groups
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

      groups_list = new_resource.groups_list

    	groups_list.each do |item|
    	  gid = item.group
    	  uids = item.users
    	  if item.attribute?(:remove_users)
    	    remove = item.remove_users
    	  else
    	    remove = false
    	  end
    	  if item.attribute?(:create)
    	    create = item.create
    	  else
    	    create = false
    	  end
    	  if create
    	    group "#{gid}" do
    	      members uids
    	      append true
    	      action :nothing
    	    end.run_action(:create)
    	  else
    	    if remove
    	      group "#{gid}" do
    	        excluded_members uids
    	        append true
    	        action :nothing
              end.run_action(:modify)
            else
  	      group "#{gid}" do
    	        members uids
    	        append true
    	        action :nothing
              end.run_action(:modify)
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
    gecos_ws_mgmt_jobids "local_groups_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "misc_mgmt"
    end.run_action(:reset)
  end
end
