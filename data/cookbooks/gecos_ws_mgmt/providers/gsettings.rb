#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: gsettings
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#


require 'etc'
def initialize(*args)
  super
  @action = :set
  package 'xvfb' 

  dconf_cache_dir = "/home/#{new_resource.username}/.cache/dconf"
  unless Kernel::test('d', dconf_cache_dir)
    FileUtils.mkdir_p dconf_cache_dir
    gid = Etc.getpwnam(new_resource.username).gid
    FileUtils.chown_R(new_resource.username, gid, dconf_cache_dir)
  end
  begin
    dbus_file = Dir["/home/#{new_resource.username}/.dbus/session-bus/*0"].last
    @dbus_address = open(dbus_file).grep(/^DBUS_SESSION_BUS_ADDRESS=(.*)/){$1}[0]
  rescue Exception => e
    @dbus_address = nil
  end

end

action :set do
  dbus_address = @dbus_address
  unless dbus_address.nil?
    execute "set key" do
      command "sudo -iu #{new_resource.username} DBUS_SESSION_BUS_ADDRESS=\"#{dbus_address}\" gsettings set #{new_resource.schema} #{new_resource.name} #{new_resource.value}"
      action :nothing
    end.run_action(:run)
  else
    execute "set key" do
      action :nothing
      command "xvfb-run -w 0 sudo -iu #{new_resource.username} gsettings set #{new_resource.schema} #{new_resource.name} #{new_resource.value}"
    end.run_action(:run)
  end
end

action :unset do
  dbus_address = @dbus_address
  unless dbus_address.nil?
    execute "unset key" do
      action :nothing
      command "sudo -iu #{new_resource.username} DBUS_SESSION_BUS_ADDRESS=\"#{@dbus_address}\" gsettings reset #{new_resource.schema} #{new_resource.name}"
    end.run_action(:run)
  else
    execute "unset key" do
      action :nothing
      command "xvfb-run -w 0 sudo -iu #{new_resource.username} gsettings reset #{new_resource.schema} #{new_resource.name}"
    end.run_Action(:run)
  end
end

