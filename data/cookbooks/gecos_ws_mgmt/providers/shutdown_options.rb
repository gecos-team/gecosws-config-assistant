#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: shutdown_options
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
      package "dconf-tools" do
       action :nothing
      end.run_action(:install) 

      systemlock = new_resource.systemlock
      systemset = new_resource.systemset
      users = new_resource.users

      # System-level lock settings
      #system = gecos_ws_mgmt_system_settings "disable-log-out" do
      #    provider "gecos_ws_mgmt_system_settings"
      #    schema "org.cinnamon.desktop.lockdown"
      #    type "boolean"
      #    value "#{systemset}"
      #    action :nothing
      #end
      #system.run_action(:lock) if systemlock
      #system.run_action(:unlock) if !systemlock

      # User-level key values
      users.each_key do |user_key|
        username = user_key
        username.gsub!('###','.')
        user = users[user_key]

        disable_log_out = user.disable_log_out

        gecos_ws_mgmt_desktop_settings "disable-log-out" do
          provider "gecos_ws_mgmt_gsettings"
          schema "org.cinnamon.desktop.lockdown"
          type "boolean"
          username username
          value "#{disable_log_out}"
        end.run_action(:set)
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
    gecos_ws_mgmt_jobids "shutdown_options_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end
