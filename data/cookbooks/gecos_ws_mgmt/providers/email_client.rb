#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: email_client
#
# Copyright 2014, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
require 'chef/mixin/shell_out'
require 'securerandom'
include Chef::Mixin::ShellOut

action :setup do

  begin
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()

    # Checking OS and Thunderbird
    if new_resource.support_os.include?(os) and ::File.exist?('/usr/bin/thunderbird')

      users = new_resource.users
      users.each_key do |user_key|

        user = users[user_key]

        username = user_key
        gid = Etc.getpwnam(username).gid

        homedir = `eval echo ~#{username}`.gsub("\n","")
        thunderbird_dir = "#{homedir}/.thunderbird"
        thunderbird_profiles = "#{homedir}/.thunderbird/profiles.ini"
        new_profile_hash = SecureRandom.hex

        ENV["DISPLAY"] = ":0.0"

        execute "Create new Profile" do
          command "sudo -iu #{username} thunderbird -CreateProfile #{new_profile_hash} #{homedir}/.thunderbird"
          action :nothing
        end.run_action(:run)

        ruby_block "Remove thunderbird default profile" do
          block do
            fe = Chef::Util::FileEdit.new(thunderbird_profiles)
            fe.search_file_delete_line("Default=1")
            fe.write_file
          end
          only_if { ::File.exist?(thunderbird_profiles) }
          action :nothing
        end.run_action(:run)
        
        dirprof =  Dir.glob("#{homedir}/.thunderbird/**#{new_profile_hash}")[0]
      
        template "#{dirprof}/user.js" do
          source "email_client_prefs.js.erb"
          owner username
          group gid
          variables(
            :identity_name => user.identity.name,
            :identity_email => user.identity.email,
            :imap_hostname => user.imap.hostname,
            :imap_port => user.imap.port,
            :imap_username => user.imap.username,
            :smtp_hostname => user.smtp.hostname,
            :smtp_port => user.smtp.port,
            :smtp_username => user.smtp.username
          )
          action :nothing
        end.run_action(:create)

        ruby_block "Add the last profile as default thunderbird profile" do
          block do 
            fe = Chef::Util::FileEdit.new(thunderbird_profiles)
            fe.insert_line_if_no_match("Default=1", "Default=1")
            fe.write_file
          end
          action :nothing
        end.run_action(:run)

        bash "chown #{username}" do
          code <<-EOH 
            chown -R #{username}:#{gid} #{thunderbird_dir}
            EOH
          action :nothing
        end.run_action(:run)

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
    gecos_ws_mgmt_jobids "email_client_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end