#
# Cookbook Name:: gecos_ws_mgmt
# Provider:: forticlient
#
# Copyright 2013, Junta de Andalucia
# http://www.juntadeandalucia.es/
#
# All rights reserved - EUPL License V 1.1
# http://www.osor.eu/eupl


action :setup do
  begin
    os = `lsb_release -d`.split(":")[1].chomp().lstrip()
    if new_resource.support_os.include?(os)

      res_proxyserver = new_resource.proxyserver || node[:gecos_ws_mgmt][:network_mgmt][:forticlientvpn_res][:proxyserver]
      res_proxyport = new_resource.proxyport || node[:gecos_ws_mgmt][:network_mgmt][:forticlientvpn_res][:proxyport]
      res_proxyuser = new_resource.proxyuser || node[:gecos_ws_mgmt][:network_mgmt][:forticlientvpn_res][:proxyuser]
      res_keepalive= new_resource.keepalive || node[:gecos_ws_mgmt][:network_mgmt][:forticlientvpn_res][:keepalive]
      res_autostart = new_resource.autostart || node[:gecos_ws_mgmt][:network_mgmt][:forticlientvpn_res][:autostart]
      res_connections = new_resource.connections || node[:gecos_ws_mgmt][:network_mgmt][:forticlientvpn_res][:connections]

      autostart_num = 0
      if res_autostart 
        autostart_num = 1
      end

      require 'fileutils'

      Dir["/home/*"].each do |homedir|
        user_fctlsslvpnhistory = homedir + "/.fctsslvpnhistory"
        if Kernel::test('f', user_fctlsslvpnhistory)
          current_profile_line = `grep "^current=" #{user_fctlsslvpnhistory}`.strip
          current_profile = current_profile_line.split("=")[1]
          # parse current conf file for already existant (pass saved) connections
          current_conns = Hash.new
          # TODO: remove bashisms
          file_conns = `grep "^profile\\|^p12passwd\\|^path\\|^password\\|^user\\|^port\\|^server" #{user_fctlsslvpnhistory}`
          open(user_fctlsslvpnhistory).grep(/^profile|^p12passwd|^path|^password|^user|^port|^server/).each do |fc|
#          file_conns.split("\n").each do |fc|
            fc = fc.strip
            key, val = fc.split("=")
            if key.include? "profile"
              current_profile = val
              current_conns[current_profile] = Hash.new
            end
            current_conns[current_profile][key] = val
          end
          connections = current_conns
        else
          connections = Hash.new
          current_profile = "default"
        end

        # add new connections if they do not already exist  

        res_connections.each do |conn|
          name = conn[:name]
          if connections[name].nil?
            connections[name] = Hash.new
            connections[name]["server"] = conn[:server]
            connections[name]["port"] = conn[:port]
            connections[name]["p12passwd"] = ''
            connections[name]["path"] = ''
            connections[name]["password"] = ''
            connections[name]["user"] = ''
          else
            # update host/port for connection if values were updated in node
            if connections[name]["server"] != conn[:server]
              connections[name]["server"] = conn[:server]
            end
            if connections[name]["port"] != conn[:port]
              connections[name]["port"] = conn[:port]
            end
          end
        end

        template user_fctlsslvpnhistory do
          source "fctlsslvpnhistory.erb"
          variables(
            :proxyserver => res_proxyserver,
            :proxyport => res_proxyport,
            :proxyuser => res_proxyuser,
            :current_profile => current_profile,
            :keepalive => res_keepalive,
            :autostart => autostart_num,
            :connections => connections
          )
        end
      end
    else
      Chef::Log.info("This resource is not support into your OS")
    end

    # save current job ids (new_resource.job_ids) as "ok"
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 0
    end

  rescue Exception => e
    # just save current job ids as "failed"
    # save_failed_job_ids
    Chef::Log.error(e.message)
    job_ids = new_resource.job_ids
    job_ids.each do |jid|
      node.set['job_status'][jid]['status'] = 1
      node.set['job_status'][jid]['message'] = e.message.force_encoding("utf-8")
    end
  ensure
    gecos_ws_mgmt_jobids "forticlientvpn_res" do
      provider "gecos_ws_mgmt_jobids"
      recipe "network_mgmt"
    end.run_action(:reset)
  end
end



