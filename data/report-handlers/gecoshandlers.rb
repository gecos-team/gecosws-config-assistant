require 'json'
require 'rest_client'
require 'chef/log'
require "resolv"
require 'uri'

module GECOSReports
  class StatusHandler < Chef::Handler

    def report
      gcc_control = {}
      
      if File.file?('/usr/bin/gecos-snitch-client')
        `gecos-snitch-client --set-active false`
      else
        `gecosws-chef-snitch-client --set-active false`
      end        
      
      if File.file?('/etc/gcc.control')
        File.open('/etc/gcc.control', 'r') do |f|
          gcc_control = JSON.load(f)
        end
        begin
          has_conection = false
          tries = 0
          dns_resolver = Resolv.new()
          while (not has_conection and tries < 10 and not gcc_control.nil? and 
                gcc_control.key?("uri_gcc") and not gcc_control['uri_gcc'].nil? and 
                not gcc_control['uri_gcc'].empty?)
            begin
              uri = URI(gcc_control['uri_gcc'])
              domain = uri.host
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
            # SSL certificate validation (enable by default)
            verify_ssl = true
            if gcc_control.key?('ssl_verify')
                verify_ssl = gcc_control['ssl_verify']
            end

            resource = RestClient::Resource.new(
                gcc_control['uri_gcc'] + '/chef/status/',
                :verify_ssl => verify_ssl)
            response = resource.put :node_id => gcc_control['gcc_nodename'], :gcc_username => gcc_control['gcc_username']
            if not response.code.between?(200,299)
              Chef::Log.error('Wrong response from GECOS Control Center')
            else
              response_json = JSON.load(response.to_str)
              if not response_json['ok']
                Chef::Log.error(response_json['message'])
              end
            end
          else
            Chef::Log.error('GECOS Control Center connection error')
          end
        rescue Exception => e
          Chef::Log.error(e)
        end
      end
    end
  end
end

