#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: app_config
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
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)

      if not new_resource.firefox_config.empty?
        app_update = new_resource.firefox_config['app_update']
        unless Kernel::test('d', '/etc/firefox/pref')
          FileUtils.mkdir_p '/etc/firefox/pref'
        end

        template "/etc/firefox/pref/update.js" do
          source "update.js.erb"
          action :nothing
          variables(
            :app_update => app_update
            )
        end.run_action(:create)


      end

      if not new_resource.java_config.empty?
        version = new_resource.java_config['version']
        plug_version = new_resource.java_config['plug_version']
        sec = new_resource.java_config['sec']
        crl = new_resource.java_config['crl']
        ocsp = new_resource.java_config['ocsp']
        warn_cert = new_resource.java_config['warn_cert']
        mix_code = new_resource.java_config['mix_code']
        array_attrs = new_resource.java_config['array_attrs']

        unless Kernel::test('d', '/etc/.java/deployment/')
          FileUtils.mkdir_p '/etc/.java/deployment/'
        end

        cookbook_file "deployment.config" do
          path "/etc/.java/deployment/deployment.config"
          action :nothing
        end.run_action(:create_if_missing)

        #Setting java version
        alternative_exists = shell_out("#{alternatives_cmd} --display java| grep #{version}").exitstatus == 0
        if alternative_exists
          Chef::Log.info("Setting alternative for java with value #{version}/jre/bin/java")
          set_cmd = shell_out("#{alternatives_cmd} --set java #{version}/jre/bin/java")
          unless set_cmd.exitstatus == 0
            Chef::Application.fatal!(%Q[ set alternative failed ])
          end
        end

        #Setting java plugin version
        alternative_exists = shell_out("#{alternatives_cmd} --display mozilla-javaplugin.so| grep #{version}").exitstatus == 0
        if alternative_exists
          Chef::Log.info("Setting alternative for mozilla-javaplugin.so with value #{version}/jre/lib/i386/libnpjp2.so")
          set_cmd = shell_out("#{alternatives_cmd} --set java #{version}/jre/lib/i386/libnpjp2.so")
          unless set_cmd.exitstatus == 0
            Chef::Application.fatal!(%Q[ set alternative failed ])
          end
        end

        #Setting deployment.properties with concrete properties
        template "/etc/.java/deployment/deployment.properties" do
          source "deployment.properties.erb"
          action :nothing
          variables(
            :sec => sec,
            :crl => crl,
            :ocsp => ocsp,
            :warn_cert => warn_cert,
            :mix_code => mix_code,
            :array_attrs => array_attrs
            )
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
    # just save current job ids as "failed"
    # save_failed_job_ids
    Chef::Log.error(e.message)
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  ensure
    gecos_ws_mgmt_jobids "app_config_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "software_mgmt"
    end.run_action(:reset)
  end
end