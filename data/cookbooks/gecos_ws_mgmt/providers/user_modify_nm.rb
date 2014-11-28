#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: user_modify_nm
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)

      udisk_policy = "/var/lib/polkit-1/localauthority/50-local.d/org.freedesktop.NetworkManager.pkla"
      cookbook_file udisk_policy do
        source "nmapplet.policy"
        owner "root"
        group "root"
        mode "0644"
        action :nothing
      end.run_action(:create)

      users = new_resource.users 
      users.each_key do |user_key|
        username = user_key
        user = users[user_key]
        if user.can_modify
          group "netdev" do
  	        members username
  	        append true
            action :nothing
  	      end.run_action(:modify)
        else
          group "netdev" do
            excluded_members username
            append true
            action :nothing
          end.run_action(:modify)
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
      node.set['job_status'][jid]['message'] = e.message.force_encoding("utf-8")
    end
  ensure
    gecos_ws_mgmt_jobids "user_modify_nm_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end

