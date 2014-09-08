require 'json'
require 'rest_client'
require 'chef/log'
require "resolv"

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
          has_conection = false
          tries = 0
          dns_resolver = Resolv::DNS.new()
          while not has_conection and tries < 10
            begin
              domain = gcc_control['uri_gcc'].split(':')[1].split('/')[2]
              dns_resolver.getaddress(domain)
              has_conection = true
            rescue Resolv::ResolvError => e
              sleep(1)
              tries=tries+1
              Chef::Log.info(tries)
            end
          end
          if has_conection
            Chef::Log.info(gcc_control)
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
          else
            Chef::Log.error('there is no connectivity')
          end
        rescue Exception => e
          Chef::Log.error(e.message)
        end
      end
    end
  end
end

