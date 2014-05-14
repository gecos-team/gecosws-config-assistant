provides 'ohai_gecos'

if ohai_gecos.nil?
  ohai_gecos Mash.new
end
begin
  pclabel = ''
  File.open('/etc/pclabel','r') do |pclabelfile|
    pclabel = pclabelfile.gets
  end
rescue Exception => e
  puts e.message
end

ohai_gecos['pclabel'] = pclabel
