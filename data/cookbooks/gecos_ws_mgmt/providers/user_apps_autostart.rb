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
# OS identification moved to recipes/default.rb
#    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
#    if new_resource.support_os.include?(os)
    if new_resource.support_os.include?($gecos_os)
      users = new_resource.users 
      desktop_path = "/usr/share/applications/"

      users.each_key do |user_key|
        nameuser = user_key 
        username = nameuser.gsub('###','.')
        user = users[user_key]

        homedir = `eval echo ~#{username}`.gsub("\n","")
        autostart_path = "#{homedir}/.config/autostart/"
        unless Kernel::test('d', autostart_path)
          FileUtils.mkdir_p(autostart_path)
          gid = Etc.getpwnam(username).gid
          FileUtils.chown_R(username, gid, homedir+"/.config")
        end
      
        user.desktops.each do |desktopfile|
# Add ".desktop" if not present in launcher's name
          if ! desktopfile.include? "\.desktop"
	    desktopfile.concat(".desktop")
	  end
          if FileTest.exist? desktop_path + desktopfile and not desktopfile.empty? 
            FileUtils.cp "#{desktop_path}#{desktopfile}",  autostart_path
          end
        end
        user.desktops_to_remove.each do |desktopfile|
# Add ".desktop" if not present in launcher's name
          if ! desktopfile.include? "\.desktop"
	    desktopfile.concat(".desktop")
	  end
          if FileTest.exist? autostart_path + desktopfile and not desktopfile.empty? 
            FileUtils.rm "#{autostart_path}#{desktopfile}"
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
    gecos_ws_mgmt_jobids "user_apps_autostart_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "users_mgmt"
    end.run_action(:reset)
  end
end



