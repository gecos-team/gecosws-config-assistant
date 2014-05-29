#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: power_conf
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin

    require 'time'

    package 'cpufrequtils' do
      action :nothing
    end.run_action(:install)

    package 'powernap' do
      action :nothing
    end.run_action(:install)

    cpu_freq_gov = new_resource.cpu_freq_gov
    auto_shutdown = new_resource.auto_shutdown
    usb_autosuspend = new_resource.usb_autosuspend

    min_cpu_file = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"

    unless cpu_freq_gov.empty?
      execute "Setting CPU freq governor to #{cpu_freq_gov}" do
        command "echo #{cpu_freq_gov} | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
        only_if { ::File.exists?(min_cpu_file) and ::File.readlines(min_cpu_file).grep(/#{cpu_freq_gov}/).empty? }
        notifies :restart, "service[cron]", :delayed
        action :nothing
      end.run_action(:run)
    end

    unless auto_shutdown.empty?
      service "cron" do
        supports :restart => true
        action :nothing
      end.run_action(:nothing)
      
      date = ::Time.parse("#{auto_shutdown.hour}:#{auto_shutdown.minute}")

      first_warn = date - 1800
      last_warn = date - 300

      first_warn_hour = first_warn.strftime("%H")
      first_warn_minute = first_warn.strftime("%M")

      last_warn_hour = last_warn.strftime("%H")
      last_warn_minute = last_warn.strftime("%M")

      template "/etc/cron.d/auto_shutdown" do
        source "auto_shutdown.erb"
        mode "0755"
        owner "root"
        variables({ :hour => auto_shutdown.hour, :minute => auto_shutdown.minute, :first_warn_hour => first_warn_hour,
         :first_warn_minute => first_warn_minute, :last_warn_hour => last_warn_hour, :last_warn_minute => last_warn_minute })
        notifies :restart, "service[cron]", :delayed
        action :nothing
      end.run_action(:create)
    else 
      file "/etc/cron.d/auto_shutdown" do
        action :nothing
      end.run_action(:delete)
    end

    unless usb_autosuspend.empty?
      if usb_autosuspend == "enable"
        execute "enable usb autosuspend" do
          command "powernap-action --enable usb_autosuspend"
          action :nothing
        end.run_action(:run)
      elsif usb_autosuspend == "disable"
        execute "disable usb autosuspend" do
          command "powernap-action --disable usb_autosuspend"
          action :nothing
        end.run_action(:run)
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
