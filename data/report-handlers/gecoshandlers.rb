require 'json'
require 'rest_client'
require 'chef/log'

module GECOSReports
  class StatusHandler < Chef::Handler

    def report
      gcc_control = {}
      
      `gecosws-chef-snitch-client --set-active false`
      
      if File.file?('/etc/gcc.control')
        File.open('/etc/gcc.control', 'r') do |f|
          gcc_control = JSON.load(f)
        end
        begin
          resource = RestClient::Resource.new(gcc_control['uri_gcc'] + '/chef/status/')
          response = resource.put :node_id => gcc_control['gcc_nodename'], :gcc_username => gcc_control['gcc_username']
          if not response.code.between?(200,299)
            Chef::Log.error('The GCC URI not response')
          else
            response_json = JSON.load(response.to_str)
            if not response_json['ok']
              Chef::Log.error(response_json['message'])
            end
          end
        rescue Exception => e
          Chef::Log.error(e.message)
        end
      end
    end
  end
end

