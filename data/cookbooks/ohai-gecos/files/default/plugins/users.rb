provides 'ohai_gecos'

if ohai_gecos.nil?
  ohai_gecos Mash.new
end

require 'etc'
require 'rest_client'
require 'json'
users = []
# LikeWise create the user homes at /home/local/DOMAIN/
homedirs = Dir["/home/*"] + Dir["/home/local/*/*"]
homedirs.each do |homedir|
  temp=homedir.split('/')
  user=temp[temp.size()-1]
  begin
    entry=Etc.getpwnam(user)
    users << Mash.new(
      :username => entry.name,
      :home     => entry.dir,
      :gid      => entry.gid,
      :uid      => entry.uid
    )
  rescue Exception => e
    puts 'User ' + user + ' doesn\'t exists'
  end
end

if not users == ohai_gecos['users']
  users_report = users.join(',')
  gcc_control = {}
  File.open('/etc/gcc.control', "r") do |f|
    gcc_control = JSON.load(f)
  end
  begin
    resource = RestClient::Resource.new(gcc_control['uri_gcc'] + '/register/user/')
    response = resource.put :node_id => gcc_control['gcc_nodename'],:users=>users_report, :content_type => :json, :accept => :json
  rescue Exception => e
    puts e.message
  end
end

ohai_gecos['users'] = users

