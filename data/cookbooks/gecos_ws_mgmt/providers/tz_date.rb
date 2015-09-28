#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: tz_date
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
# We moved OS identification to recipes/default.rb
# But this recipe launches alone, and default.rb is not executed
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)
#    if new_resource.support_os.include?($gecos_os)
      package 'ntpdate' do
        action :nothing
      end.run_action(:install)

      ntp_server = new_resource.server 

      unless ntp_server.nil? or ntp_server.empty?
        execute "ntpdate" do
          command "ntpdate-debian -u #{ntp_server}"
          action :nothing
        end.run_action(:run)
        template '/etc/default/ntpdate' do
          action :nothing
          source 'ntpdate.erb'
          owner 'root'
          group 'root'
          mode 00644
          variables ({
            :ntp_server => new_resource.server
          })
        end.run_action(:create)
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
    Chef::Log.error(e.message)
    # just save current job ids as "failed"
    # save_failed_job_ids
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
    gecos_ws_mgmt_jobids "tz_date_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "misc_mgmt"
    end.run_action(:reset)
  end
end

