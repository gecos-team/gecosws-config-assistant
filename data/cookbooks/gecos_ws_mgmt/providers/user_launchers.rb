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
    users = new_resource.users 
    applications_path = "/usr/share/applications/"

    users.each do |user|
      username = user.username
      homedir = `eval echo ~#{user.username}`.gsub("\n","")
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
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 0
    end   

  rescue Exception => e
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message
    end
  end
end
