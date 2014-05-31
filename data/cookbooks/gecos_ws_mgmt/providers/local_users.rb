#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: local_users
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

    package "libshadow-ruby1.8" do
      action :nothing
    end.run_action(:install)

    users = new_resource.users_list
    users.each do |usrdata| 
      username = usrdata.user
      passwd = usrdata.password
      actiontorun = usrdata.actiontorun
      grps = usrdata.groups
      user_home = "/home/#{username}"

      
      if actiontorun == "delete"
        Chef::Log.info("Removing local user #{username}")
#TODO1 : check if user is not logged before removing process
        user username do
          action :nothing
        end.run_action(:remove)
      else
        Chef::Log.info("Managing local user #{username}")
        user username do
          password passwd
          home user_home
          comment "GECOS managed user"
          shell "/bin/bash"
          action :nothing
        end.run_action(:create)

        if !::File.directory?(user_home) 
          directory user_home do
            owner username
            group username
            action :nothing
          end.run_action(:create)
          bash "copy skel to #{username}" do
            code <<-EOH 
              cp /etc/skel/.* #{user_home}
              chown -R #{username}: #{user_home}
              EOH
            action :nothing
          end.run_action(:run)
        end

        grps.each do |g|
          begin
            info = Etc.getgrnam(g)
            group "#{g}" do
              append true
              members username
              action :nothing
            end.run_action(:modify)
          rescue ArgumentError => e
            Chef::Log.info("Group #{g} does not exist, ignoring..")
          end
        end
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
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  end
end

