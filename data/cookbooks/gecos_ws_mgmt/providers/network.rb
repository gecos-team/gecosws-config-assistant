#
# Cookbook Name:: gecos-ws-mgmt
# Provider:: network
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
    gem_depends = [ 'netaddr' ]

    gem_depends.each do |gem|

      r = gem_package gem do
        gem_binary("/opt/chef/embedded/bin/gem")
        action :nothing
      end
      r.run_action(:install)

    end
    Gem.clear_paths
    require 'netaddr'
    require 'fileutils'

    # setup system connections
    ip_address = node[:gecos_ws_mgmt][:network_mgmt][:network_res][:ip_address] if new_resource.ip_address.nil?
    gateway = node[:gecos_ws_mgmt][:network_mgmt][:network_res][:gateway] if new_resource.gateway.nil?
    netmask = node[:gecos_ws_mgmt][:network_mgmt][:network_res][:netmask] if new_resource.netmask.nil?
    network_type = node[:gecos_ws_mgmt][:network_mgmt][:network_res][:network_type] if new_resource.network_type.nil?
    use_dhcp = node[:gecos_ws_mgmt][:network_mgmt][:network_res][:use_dhcp] if new_resource.use_dhcp.nil?
    dns_servers_array = node[:gecos_ws_mgmt][:network_mgmt][:network_res][:dns_servers] if new_resource.dns_servers.nil?

    users_array = [] if not node[:gecos_ws_mgmt][:network_mgmt][:network_res][:users].nil?


    nm_conn_backup_dir = '/etc/NetworkManager/system-connections/chef-backups'
    nm_conn_production_dir = '/etc/NetworkManager/system-connections/chef-conns'
 
    unless Kernel::test('d', nm_conn_backup_dir)
      FileUtils.mkdir nm_conn_backup_dir
    end
    
    unless Kernel::test('d', nm_conn_production_dir)
      FileUtils.mkdir nm_conn_production_dir
    end
    
    
    nm_wired_dhcp_conn_source = 'wired-dhcp-conn.erb'
    nm_wired_static_ip_conn_source = 'wired-static-ip-conn.erb'
    
    nm_macaddress = node["macaddress"].gsub(/[0]([\w]:)/, '\\1')
    
    nm_conn_files = []
    Dir["/etc/NetworkManager/system-connections/*"].each do |conn_file|
      if Kernel::test('f', conn_file)
        unless open(conn_file).grep(/#{node["macaddress"]}/).empty? and open(conn_file).grep(/#{nm_macaddress}/).empty?
          nm_conn_files << conn_file
        end
      end
    end
    
    # parse dns servers
    dns_servers = ""
    dns_servers_array.each do |server|
      if dns_servers.empty?
        dns_servers = server + ";" unless server.empty?
      else
        dns_servers = dns_servers + server + ";" unless server.empty?
      end
    end
    
    if network_type == 'wired'
      if use_dhcp == true
        unless nm_conn_files.empty?
          nm_conn_files.each do |conn_file|
            FileUtils.cp(conn_file, nm_conn_backup_dir)
            basename = ::File.basename(conn_file)
            template_name = nm_conn_production_dir + "/" + basename
            template template_name do
              owner "root"
              group "root"
              mode 0600
              variables ( { :mac_address => nm_macaddress } )
              source nm_wired_dhcp_conn_source
            end
          end
        else
          conn_file = "/etc/NetworkManager/system-connections/chef-conns/chef-managed-connection"
          template conn_file do
            owner "root"
            group "root"
            mode 0600
            variables ( { :mac_address => nm_macaddress } )
            source nm_wired_dhcp_conn_source
          end
        end
      else
        netmask_int = NetAddr.netmask_to_i(netmask)
        netmask = NetAddr.i_to_bits(netmask_int)
        unless nm_conn_files.empty?
          nm_conn_files.each do |conn_file|
            FileUtils.cp(conn_file,nm_conn_backup_dir)
            basename = ::File.basename(conn_file)
            template_name = nm_conn_production_dir + "/" + basename
            template template_name do
              owner "root"
              group "root"
              mode 0600
              variables ( { :dns_servers => dns_servers,
                            :mac_address => nm_macaddress,
                            :ip_address => ip_address,
                            :netmask => netmask,
                            :gateway => gateway } )
              source nm_wired_static_ip_conn_source
            end
          end
        else
          conn_file = "/etc/NetworkManager/system-connections/chef-conns/chef-managed-connection"
          template conn_file do
            owner "root"
            group "root"
            mode 0600
            variables ( { :dns_servers => dns_servers,
                          :mac_address => nm_macaddress,
                          :ip_address => ip_address,
                          :netmask => netmask,
                          :gateway => gateway })
            source nm_wired_static_ip_conn_source
          end
        end
      end
    # TODO: else: wireless connection
    #else 
    
    end


    # setup user connections
    users_array.each do |user_conn|
      username = user_conn[:username]
    end

    cookbook_file "/etc/init/gecos-nm.conf" do
      source "gecos-nm.conf" 
      mode "0644"
      backup false
    end
    
    # TODO:
    # save current job ids as "ok"
  rescue
    # TODO:
    # just save current job ids as "failed"
    # save_failed_job_ids
    raise
  end
end
