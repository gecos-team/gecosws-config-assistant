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
    unless ntp_server.nil?
      execute "ntpdate" do
        command "ntpdate-debian -u #{ntp_server}"
        action :run
      end
    end
  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end

end

