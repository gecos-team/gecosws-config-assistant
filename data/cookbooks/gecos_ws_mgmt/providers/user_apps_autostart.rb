#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: user_apps_autostart
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#

action :setup do
  begin
    users = new_resource.users 
    desktop_path = "/usr/share/applications/"

    users.each do |user|
      username = user.username
      homedir = `eval echo ~#{user.username}`.gsub("\n","")
      autostart_path = "#{homedir}/.config/autostart/"
      unless Kernel::test('d', autostart_path)
        FileUtils.mkdir_p(autostart_path)
        gid = Etc.getpwnam(username).gid
        FileUtils.chown_R(username, gid, homedir+"/.config")
      end
    
      user.desktops.each do |desktopfile|
        if FileTest.exist? desktop_path + desktopfile and not desktopfile.empty? 
          FileUtils.cp "#{desktop_path}#{desktopfile}",  autostart_path
        end
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



