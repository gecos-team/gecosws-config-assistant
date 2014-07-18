#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: folder_sharing
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
action :setup do
  begin
    
    require 'etc'
  
    users = new_resource.users
    users_to_add = []
    users_to_remove = []
  
  # Default Samba group
    GRP_SAMBA = 'sambashare'
    samba_members = Etc.getgrnam(GRP_SAMBA).mem
  
    users.each_key do |user_key|
      username = user_key 
      user = users[user_key]
      if user.can_share 
        users_to_add << username
      else
        users_to_remove << username
      end
    end

    samba_members = samba_members + users_to_add
    samba_members = samba_members - users_to_remove
    samba_members.uniq!

    if samba_members.empty?
      samba_members << 'nobody'
    end

    group GRP_SAMBA do
      members samba_members
      append false
      action :nothing
    end.run_action(:manage)

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
    gecos_ws_mgmt_jobids "users_mgmt" do
      provider "gecos_ws_mgmt_jobids"
      resource "folder_sharing_res"
    end.run_action(:reset)
  end
end
