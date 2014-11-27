provides 'ohai_gecos'

if ohai_gecos.nil?
  ohai_gecos Mash.new
end

require 'etc'
require 'rest_client'
require 'json'
users = []
users_send = []
# LikeWise create the user homes at /home/local/DOMAIN/
homedirs = Dir["/home/*"] + Dir["/home/local/*/*"]
grp_sudo = Etc.getgrnam('sudo')
homedirs.each do |homedir|
  temp=homedir.split('/')
  user=temp[temp.size()-1]
  begin
    entry=Etc.getpwnam(user)
    users << Mash.new(
      :username => entry.name,
      :home     => entry.dir,
      :gid      => entry.gid,
      :uid      => entry.uid,
      :sudo     => grp_sudo.mem.include?(entry.name)
    )
    users_send << entry.name
  rescue Exception => e
    puts 'User ' + user + ' doesn\'t exists'
  end
end

ohai_gecos['users'] = users

