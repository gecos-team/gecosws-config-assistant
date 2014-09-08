#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: user_launchers
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)
      users = new_resource.users 
      applications_path = "/usr/share/applications/"

      users.each_key do |user_key|
        username = user_key
        user = users[user_key]

        homedir = `eval echo ~#{username}`.gsub("\n","")
        desktop_path = "#{homedir}/Escritorio/"

        gid = Etc.getpwnam(username).gid
        user.launchers.each do |desktopfile|
          if FileTest.exist? applications_path + desktopfile and not desktopfile.empty?
            FileUtils.cp "#{applications_path}#{desktopfile}",  desktop_path
            FileUtils.chown(username, gid, desktop_path + desktopfile)
            FileUtils.chmod 0755, desktop_path + desktopfile
          end
        end

      end
    else
      Chef::Log.info("This resource are not support into your OS")
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
    gecos_ws_mgmt_jobids "user_launchers_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end
