#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: desktop_background
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#


action :setup do
  begin
    package "dconf-tools" do
      action :nothing
    end.run_action(:install) 

    #if !new_resource.users.nil? and !new_resource.users.empty?
    if !new_resource.desktop_file.nil? and !new_resource.desktop_file.empty?
      #Chef::Log.info("Estableciendo fondo de escritorio #{new_resource.users[0].desktop_file}")
      Chef::Log.info("Estableciendo fondo de escritorio #{new_resource.desktop_file}")
      execute "update-dconf" do
        command "dconf update"
        action :nothing
      end
      directory "/etc/dconf/profile" do
        recursive true
        action :nothing
      end.run_action(:create)
      directory "/etc/dconf/db/gecos.d/locks" do
        recursive true
        action :nothing
      end.run_action(:create)
      file "/etc/dconf/profile/user" do
        backup false
        content <<-eof
system-db:gecos
user-db:user
        eof
        action :nothing
      end.run_action(:create)
      file "/etc/dconf/db/gecos.d/locks/gecos.lock" do
        backup false
        content <<-eof
/org/gnome/desktop/background/picture-uri
/org/cinnamon/desktop/background/picture-uri
        eof
        action :nothing
      end.run_action(:create)
      file "/etc/dconf/db/gecos.d/gecos.key" do
        backup false
        content <<-eof
[org/gnome/desktop/background]
picture-uri='file://#{new_resource.desktop_file}'
[org/cinnamon/desktop/background]
picture-uri='file://#{new_resource.desktop_file}'
        eof
#        content <<-eof
#        [org/gnome/desktop/background]
#        picture-uri='file://#{new_resource.users[0].desktop_file}'
#        [org/cinnamon/desktop/background]
#        picture-uri='file://#{new_resource.users[0].desktop_file}'
#        eof
        action :nothing
        notifies :run, "execute[update-dconf]", :delayed
      end.run_action(:create)
    else
      file "/etc/dconf/db/gecos.d/locks/gecos.lock" do
        backup false
        action :nothing
      end.run_action(:delete)
      file "/etc/dconf/db/gecos.d/gecos.key" do
        backup false
        action :nothing
      end.run_action(:delete)
      file "/etc/dconf/profile/user" do
        backup false
        action :nothing
      end.run_action(:delete)
      execute "update-dconf" do
        command "dconf update"
        action :nothing
      end.run_action(:run)
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