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

# It sets a fixed value for a dconf key at system level
action :set do
  dconfdb = 'gecos'
  schema = new_resource.schema
  key = new_resource.name
  value = new_resource.value

  if !key.nil? and !key.empty?
    ["/etc/dconf/profile", "/etc/dconf/db/#{dconfdb}.d/locks"].each do |dir|
      directory dir do
        recursive true
      end.run_action(:create)
    end
  end

  file "/etc/dconf/profile/user" do
    backup false
    content <<-eof
user-db:user
system-db:#{dconfdb}
    eof
  end.run_action(:create)

  file "/etc/dconf/db/#{dconfdb}.d/#{key}.key" do
    backup false
    content <<-eof
[#{schema}]
#{key}='#{value}'
    eof
  end.run_action(:create)

  execute "update-dconf" do
    command "dconf update"
  end
end

# Removes a system-level dconf fixed value
action :unset do
  dconfdb = 'gecos'
  schema = new_resource.schema
  key = new_resource.name
  value = new_resource.value

  file "/etc/dconf/db/#{dconfdb}.d/#{key}.key" do
    action :nothing
  end.run_action(:delete)

  execute "update-dconf" do
    command "dconf update"
  end
end

# It prevents users for changing the value of a dconf key
action :lock do
  dconfdb = 'gecos'
  schema = new_resource.schema
  key = new_resource.name
  value = new_resource.value

  if !key.nil? and !key.empty?
    ["/etc/dconf/profile", "/etc/dconf/db/#{dconfdb}.d/locks"].each do |dir|
      directory dir do
        recursive true
      end.run_action(:create)
    end
  end

  file "/etc/dconf/profile/user" do
    backup false
    content <<-eof
system-db:#{dconfdb}
user-db:user
    eof
  end.run_action(:create)

  key_path = '/' + schema.gsub('.','/') + '/' + key
  file "/etc/dconf/db/#{dconfdb}.d/locks/#{key}.lock" do
    backup false
    content <<-eof
#{key_path}
    eof
  end.run_action(:create)

  execute "update-dconf" do
    command "dconf update"
  end
end

# It removes the dconf key system-level locking
action :unlock do
  dconfdb = 'gecos'
  schema = new_resource.schema
  key = new_resource.name

  key_path = '/' + schema.gsub('.','/') + '/' + key
  file "/etc/dconf/db/#{dconfdb}.d/locks/#{key}.lock" do
    action :nothing
  end.run_action(:delete)

  execute "update-dconf" do
    command "dconf update"
  end
end