#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: mobile_broadband
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl
#


action :setup do

  begin
    # setup resource depends
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)
      gem_depends = [ 'activesupport', 'json' ]

      gem_depends.each do |gem|

        r = gem_package gem do
          gem_binary("/opt/chef/embedded/bin/gem")
          action :nothing
        end
        r.run_action(:install)

      end
      Gem.clear_paths
      require 'securerandom'
      require 'json'
      require 'active_support/core_ext/hash'

      # setup system connections
      connections = new_resource.connections
      Chef::Log.info("Connections: #{connections}")

      nm_conn_path = '/etc/NetworkManager/system-connections'
      id_con = 0
      node[:gecos_ws_mgmt][:network_mgmt][:mobile_broadband_res][:connections].each do |conn|
        provider = conn[:provider]
        Chef::Log.info("Setting '#{provider}' broadband connection")
        conn_uuid = SecureRandom.uuid

        # start providers xml parsing
        # some bash rationale (extracts spanish providers' names):
        # cat /usr/share/mobile-broadband-provider-info/serviceproviders.xml | xml2json| jq .serviceproviders.country 
        # | sed -e 's|@code|code|g' -e 's|#tail|tail|g' -e 's|#text|text|g' /var/tmp/countries.json|jq '.[] | select(.code=="es")'|jq .provider[].name.text
        providers_hash = Hash.from_xml(::File.read "/usr/share/mobile-broadband-provider-info/serviceproviders.xml")
        conn_country = conn['country']
        dig1 = providers_hash["serviceproviders"]["country"].select {|country| country["code"] == conn_country }
        providers = dig1[0]["provider"]
        provider_info = providers.select {|p| p["name"] == provider }
        provider_info.sort!
        case provider_info[0]
          when Array
            gsm_object = provider_info[0][1]["gsm"]
          when Hash
            gsm_object = provider_info[0]["gsm"]
        end
        case gsm_object["apn"]
          when Array
            apn_object = gsm_object["apn"][0]
          when Hash
            apn_object = gsm_object["apn"]
        end

        conn_apn = apn_object["value"]
        conn_username = apn_object["username"]
        
        template "#{nm_conn_path}/Gecos_GSM_#{id_con}" do
          source "nm_mobile_broadband.erb"
          action :nothing
          mode '0600'
          variables(
            :conn_name => "Gecos_GSM_#{id_con}",
            :conn_uuid => conn_uuid,
            :conn_username => conn_username,
            :conn_apn => conn_apn
          )
        end.run_action(:create)
        id_con += 1
      end
      # save current job ids (new_resource.job_ids) as "ok"
      job_ids = new_resource.job_ids
      job_ids.each do |jid|
        node.set['job_status'][jid]['status'] = 0
      end
    else
      Chef::Log.info("This resource is not support into your OS")
    end
  rescue Exception => e
    # just save current job ids as "failed"
    # save_failed_job_ids
    Chef::Log.error(e)
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      if not e.message.frozen?
        node.set['job_status'][jid]['message'] = e.message.force_encoding("utf-8")
      else
        node.set['job_status'][jid]['message'] = e.message
      end
    end
  ensure
    gecos_ws_mgmt_jobids "mobile_broadband_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "network_mgmt"
    end.run_action(:reset)
  end
end
