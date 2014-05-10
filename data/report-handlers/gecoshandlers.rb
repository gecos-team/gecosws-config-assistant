require 'json'
require 'rest_client'

module GECOSReports
  class StatusHandler < Chef::Handler

    def report
      gcc_control = {}
      File.open('/etc/gcc.control', 'r') do |f|
        gcc_control = JSON.load(f)
      end
      resource = RestClient::Resource.new(gcc_control['uri_gcc'] + '/chef/status/')
      response = resource.post :node_id => gcc_control['gcc_nodename']
      if not response.code.between?(200,299)
        raise 'The GCC URI not response'
      end
    end
  end
end

