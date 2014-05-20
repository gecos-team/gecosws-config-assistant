#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: auto_updates
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    onstart_update = new_resource.onstart_update
    onstop_update = new_resource.onstop_update
    days = new_resource.days
    date = new_resource.date

      Chef::Log.info("Setting automatic updates")
      log_file = '/var/log/automatic-updates.log'
      err_file = '/var/log/automatic-updates.err'
  
      if onstart_update; arrinit = ["2"]; end
      if onstop_update; arrhalt = ["6", "0"]; end

      if onstart_update or onstop_update or !days.empty? or !date.empty?
        template "/etc/init.d/auto_updates" do
          source "auto_updates.erb"
          mode "0755"
          owner "root"
          variables({ :log_file => log_file, :err_file => err_file, :arrinit => arrinit, :arrhalt => arrhalt })
        end.run_action(:create)
      else
        file "/etc/init.d/auto_updates" do
           action :nothing
        end.run_action(:delete)
      end

      if onstart_update
        bash "enable on start auto_update script" do
          code <<-EOH
          update-rc.d auto_updates start 60 2 .
          EOH
        end
      else
        link "/etc/rc2.d/S60auto_updates" do
          action :nothing
          only_if "test -L /etc/rc2.d/S60auto_updates"
        end.run_action(:delete)
      end
      
      if onstop_update 
        bash "enable on stop auto_update script" do
          code <<-EOH
        update-rc.d auto_updates start 60 6 0 .
        EOH
        end
      else
        link "/etc/rc6.d/S60auto_updates" do
          action :nothing
          only_if "test -L /etc/rc6.d/S60auto_updates"
        end.run_action(:delete)

        link "/etc/rc0.d/S60auto_updates" do
          action :nothing
          only_if "test -L /etc/rc0.d/S60auto_updates"
        end.run_action(:delete)
      end
  
      dmap = { :monday => 1, :tuesday => 2, :wednesday => 3, :thursday => 4, :friday => 5, :saturday => 6, :sunday => 7}

      unless days.empty? and date.empty?
        template "/etc/cron.d/apt_cron" do
          source "apt_cron.erb"
          mode "0755"
          owner "root"
          variables({ :date_cron => date, :days_cron => days, :days_map => dmap })
          action :nothing
        end.run_action(:create)
      else 
        file "/etc/cron.d/apt_cron" do
          action :nothing
        end.run_action(:delete) 
      end

## TODO: add script to init.d, both in start fucntion, on login in rc2 and on logout in rc6


    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"

  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end
end

