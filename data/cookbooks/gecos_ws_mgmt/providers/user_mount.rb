#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: user_mount
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    userslist = new_resource.users 

  
    udisk_policy = "/usr/share/polkit-1/actions/org.freedesktop.udisks.policy"
    cookbook_file udisk_policy do
      source "udisks.policy"
      owner "root"
      group "root"
      mode "0644"
      action :nothing
    end.run_action(:create)

    granted_users = Array.new

    userslist.each_key do |user_key|
      username = user_key
      user = userslist[user_key]
      next if user.can_mount == false
      granted_users << username

    end

    users = granted_users.uniq.inject("") do |users,user|
      users << ";unix-user:#{user}"
    end

    desktop_pkla = "/var/lib/polkit-1/localauthority/10-vendor.d/com.ubuntu.desktop.pkla"

    template desktop_pkla do
      source "com.ubuntu.desktop.pkla.erb"
      owner "root"
      group "root"
      mode "0644"
      variables :user_mount => users
      action :nothing
    end.run_action(:create)

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
      resource "user_mount_res"
    end.run_action(:reset)
  end
end
