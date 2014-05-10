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

      user.launchers.each do |desktopfile|
        if FileTest.exist? applications_path + desktopfile and not desktopfile.empty? 
          FileUtils.cp "#{applications_path}#{desktopfile}",  desktop_path
        end
      end

    end
    
    # TODO:
    # save current job ids (new_resource.job_ids) as "ok"

  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end
end