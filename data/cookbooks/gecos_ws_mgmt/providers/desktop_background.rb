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
    p = package "dconf-tools" do
      action :nothing
    end
    p.run_action(:install) 
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
        action :create
      end
      directory "/etc/dconf/db/gecos.d/locks" do
        recursive true
        action :create
      end
      file "/etc/dconf/profile/user" do
        backup false
        content <<-eof
system-db:gecos
user-db:user
        eof
        action :create
      end
      file "/etc/dconf/db/gecos.d/locks/gecos.lock" do
        backup false
        content <<-eof
/org/gnome/desktop/background/picture-uri
/org/cinnamon/desktop/background/picture-uri
        eof
        action :create
      end
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
        action :create
        notifies :run, "execute[update-dconf]", :delayed
      end
    else
      file "/etc/dconf/db/gecos.d/locks/gecos.lock" do
        backup false
        action :delete
      end
      file "/etc/dconf/db/gecos.d/gecos.key" do
        backup false
        action :delete
      end
      file "/etc/dconf/profile/user" do
        backup false
        action :delete
      end 
      execute "update-dconf" do
        command "dconf update"
        action :run
      end
    end
  end
end
