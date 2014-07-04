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
      node.set['job_status'][jid]['message'] = e.message
    end
  end
end

