#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: remote_shutdown
#
# Copyright 2014, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
require 'chef/mixin/shell_out'
require 'date'
include Chef::Mixin::ShellOut

action :setup do

  begin
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)
      if not new_resource.shutdown_mode.empty?

        if new_resource.shutdown_mode == "halt"
          shutdown_command = "/sbin/shutdown -r now"
        else 
          shutdown_command = "/sbin/reboot"
        end
  
          now = DateTime.now

          change = false
  
          sc_hash = {}
          sc_hash['shutdown_command'] = shutdown_command

          if ::File.exist?("/etc/cron.shutdown")
            file = ::File.read("/etc/cron.shutdown")
            json_file = JSON.parse(file)
            if not json_file == sc_hash
              change = true
            end
          end
    
          
          cron "remote shutdown" do
            minute "#{now.minute + 5}" # In 5 mins from now
            hour "#{now.hour}"
            day "#{now.day}"
            month "#{now.month}"
            command "#{shutdown_command}"
            action :nothing
            only_if do not ::File.exist?("/etc/cron.shutdown") or change end
          end.run_action(:create)
          
    
          ::File.open("/etc/cron.shutdown","w") do |f|
            f.write(sc_hash.to_json)
          end

      else
        cron "remote shutdown" do
          action :nothing
        end.run_action(:delete)
        
        file "/etc/cron.shutdown" do
          owner 'root'
          group 'root'
          mode '0755'
          action :nothing
        end.run_action(:delete)

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
    gecos_ws_mgmt_jobids "remote_shutdown_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "misc_mgmt"
    end.run_action(:reset)
  end
end