#
# Cookbook Name:: gecos_ws_mgmt
# Provider:: cert
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl


action :setup do
  begin
# OS identification moved to recipes/default.rb
#    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
#    if new_resource.support_os.include?(os)
    if new_resource.support_os.include?($gecos_os)

      
      # install depends
      package "libnss3-tools" do
        action :nothing
      end.run_action(:install)

      require 'fileutils'

      res_ca_root_certs = new_resource.ca_root_certs || node[:gecos_ws_mgmt][:misc_mgmt][:cert_res][:ca_root_certs]
      res_java_keystores = new_resource.java_keystores || node[:gecos_ws_mgmt][:misc_mgmt][:cert_res][:java_keystores]

      # TODO: improve poor performance of idempotenly execute this
      #   * maybe do it once?
      # import system certs into java keystores

      dir_ca_imported = "/usr/share/ca-certificates-imported/"
      directory dir_ca_imported do
        owner 'root'
        group 'root'
        mode '0755'
        action :nothing
      end.run_action(:create)

      res_java_keystores.each do |keystore|
        Dir["/usr/share/ca-certificates/*/*"].each do |cert|
          begin
            execute "importing '#{cert}' into java keystore" do
              command "/bin/bash -c \"echo '' | sudo keytool -cacert -keystore '#{keystore}' -file '#{cert}' &>/dev/null; exit 0\""
              action :nothing
              only_if do not ::File.exist?(dir_ca_imported + keystore + ::File.basename(cert)) end
            end.run_action(:run)
            directory dir_ca_imported + keystore do
              owner 'root'
              group 'root'
              mode '0755'
              action :nothing
            end.run_action(:create)
            remote_file "Copy '#{cert}' to imported folder" do
              path dir_ca_imported + keystore + ::File.basename(cert)
              source "file://" + cert
              owner 'root'
              group 'root'
              action :nothing
            end.run_action(:create_if_missing)
          rescue
            next
          end
        end



      end

      # import gecos custom certs into every mozilla profile 
      certs_path = '/usr/share/ca-certificates/gecos/'
      directory certs_path do
        owner 'root'
        group 'root'
        mode '0755'
        action :nothing
      end.run_action(:create)

      # TODO: improve poor performance of idempotenly execute this
      res_ca_root_certs.each do |cert|
        cert_file = certs_path + cert[:name].gsub(" ", "_")
        remote_file cert_file do
          source cert[:uri]
        end
        Dir["/home/*/.mozilla/firefox/*default"].each do |profile|
          begin
            execute "install root cert #{cert} for profile '#{profile}'" do
              command "/bin/bash -c \"certutil -A -n '#{cert[:name]}' -t 'TC,Cw,Tw' -i '#{cert_file}' -d '#{profile}' &>/dev/null; exit 0\""
              action :nothing
            end.run_action(:run)
          rescue
            next
          end
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
    gecos_ws_mgmt_jobids "cert_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "misc_mgmt"
    end.run_action(:reset)
  end
end
