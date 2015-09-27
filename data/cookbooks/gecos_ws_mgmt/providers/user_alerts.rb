#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: user_alerts
#
# Copyright 2014, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#
require 'chef/mixin/shell_out'
require 'date'
require 'json'
include Chef::Mixin::ShellOut

action :setup do

  begin
# OS identification moved to recipes/default.rb
#    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
#    if new_resource.support_os.include?(os)
    if new_resource.support_os.include?($gecos_os)

      # Installs the notify-send command
      package "libnotify-bin" do
        action :nothing
      end.run_action(:install)

      usernames = []

      users = new_resource.users
      users.each_key do |user_key|

        user = users[user_key]
        nameuser = user_key 
        username = nameuser.gsub('###','.')
        usernames << username
        homedir = `eval echo ~#{username}`.gsub("\n","")

        # Needed for notify-send to get the user display.
        # See: http://unix.stackexchange.com/questions/111188/using-notify-send-with-cron
        cron_vars = {"DISPLAY" => ":0.0", "XAUTHORITY" => "#{homedir}/.Xauthority"}
        now = DateTime.now
        
        icon = ''
        if user.attribute?("icon")
          icon = user.icon
        end

        change = false

        msg_hash = {}
        msg_hash['urgency'] = user.urgency
        msg_hash['icon'] = icon
        msg_hash['summary'] = user.summary
        msg_hash['body'] = user.body


        if ::File.exist?("#{homedir}/.user-alert")
          file = ::File.read("#{homedir}/.user-alert")
          json_file = JSON.parse(file)
          if not json_file == msg_hash
            change = true
          end
        end

        cron "user alert for '#{username}'" do
          environment cron_vars
          minute "#{now.minute + 5}" # In 5 mins from now
          hour "#{now.hour}"
          day "#{now.day}"
          month "#{now.month}"
          user "#{username}"
          command "/usr/bin/notify-send -u #{user.urgency} -i #{icon} \"#{user.summary}\" \"#{user.body}\""
          only_if do not ::File.exist?("#{homedir}/.user-alert") or change end
          action :nothing
        end.run_action(:create)

        ::File.open("#{homedir}/.user-alert","w") do |f|
          f.write(msg_hash.to_json)
        end
        
      end

      node['ohai_gecos']['users'].each do | user |
        if not usernames.include?(user[:username])
          file "#{user.home}/.user-alert" do
            owner user[:username]
            group user[:username]
            mode '0755'
            action :nothing
          end.run_action(:delete)

          cron "user alert for '#{user[:username]}'" do
            user "#{user[:username]}"
            action :nothing
          end.run_action(:delete)

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
    gecos_ws_mgmt_jobids "user_alerts_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end
