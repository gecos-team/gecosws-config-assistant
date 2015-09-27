#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: appconfig_thunderbird
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

require 'chef/mixin/shell_out'
include Chef::Mixin::ShellOut

action :setup do
  begin
    alternatives_cmd = 'update-alternatives'
     if new_resource.support_os.include?($gecos_os)
#      if not new_resource.loffice_config.empty?
       if not new_resource.config_thunderbird.empty?
#        app_update = new_resource.loffice_config['app_update']
         app_update = new_resource.config_thunderbird['app_update']

        if app_update
          execute "enable thunderbird upgrades" do
            command "apt-mark unhold thunderbird thunderbird*"
            action :nothing
          end.run_action(:run)
        else
          execute "disable thunderbird upgrades" do
            command "apt-mark hold thunderbird thunderbird*"
            action :nothing
          end.run_action(:run)
        end
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
    gecos_ws_mgmt_jobids "appconfig_thunderbird_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "software_mgmt"
    end.run_action(:reset)
  end
end
